"""
News agent chinh: dieu phoi va quan ly trang thai.
"""

from typing import Any, Dict, List, Optional
import logging

from .backend import NewsProcessorBackend, ScriptGeneratorBackend
from ..processing import NewsAgentProcessingMixin
from .tools import ContentCleanerTool
from ..models.news_article import NewsArticle


class NewsScriptPromptBuilder:
    """Xay dung prompt cho agent."""

    STYLES = [
        "trang trong va chuyen nghiep",
        "than thien va gan gui",
        "nang dong va hap dan",
    ]

    @staticmethod
    def _target_word_count(min_words: int, max_words: int) -> int:
        return (min_words + max_words) // 2

    def create_combined_prompt(self, user_prompt: str, article_count: int) -> str:
        default_prompt = "Viet mot kich ban mach lac, de doc thanh loi, co phan tich ro rang."
        return (
            f"Tao kich ban tong hop tu {article_count} bai bao. "
            f"Ket hop thong tin thanh mot mach ke chuyen thong nhat. "
            f"{user_prompt.strip() if user_prompt and user_prompt.strip() else default_prompt}"
        )

    def create_enhanced_prompt_for_script(
        self, user_prompt: str, style: str, script_number: int, total_scripts: int
    ) -> str:
        base_prompt = user_prompt.strip() if user_prompt and user_prompt.strip() else ""
        return (
            f"Kich ban so {script_number}/{total_scripts}. "
            f"Phong cach uu tien: {style}. "
            f"{base_prompt}".strip()
        )

    def create_script_system_prompt(
        self, target_length: str, style: str, min_words: int, max_words: int
    ) -> str:
        target_words = self._target_word_count(min_words, max_words)
        return f"""Ban la bien tap vien viet kich ban tin tuc tieng Viet cho radio/podcast.

Muc tieu thoi luong: {target_length}.
Muc tieu so tu: uu tien gan {target_words} tu nhat co the. Bat buoc nam trong {min_words}-{max_words} tu.

Quy tac bat buoc:
- Bam sat du kien tu bai nguon, khong them chi tiet khong co can cu.
- Viet thanh kich ban hoan chinh, mach lac, de doc thanh loi.
- Giu phong cach: {style}.
- Khong dung markdown dam, khong bullet list trong phan kich ban.
- Heading phai o dang van ban thuong:
Mo dau:
Noi dung chinh:
Ket luan:
- Uu tien dung muc tieu so tu hon viec viet ngan.

Cach trien khai:
- Mo dau tao hook nhanh va dat boi canh.
- Noi dung chinh la phan dai nhat, can dien giai du su kien, nguyen nhan, tac dong, y nghia.
- Ket luan chot thong diep, gon nhung khong cut y.
"""

    def create_script_user_prompt(
        self,
        article: NewsArticle,
        user_prompt: str,
        target_length: str,
        min_words: int,
        max_words: int,
    ) -> str:
        target_words = self._target_word_count(min_words, max_words)
        content = ContentCleanerTool.truncate_content(article.content, 3000)
        instruction = user_prompt.strip() if user_prompt and user_prompt.strip() else (
            "Viet tu nhien, ro y, de doc thanh loi va co chieu sau phan tich."
        )

        return f"""Yeu cau cua nguoi dung:
{instruction}

Muc tieu thoi luong: {target_length}
Muc tieu so tu: khoang {target_words} tu, bat buoc trong {min_words}-{max_words} tu.
Uu tien tuan thu so tu va thoi luong. Khong viet qua ngan.

Doi tuong nguoi nghe:
- Do tuoi: 25-60
- Quan tam: chinh sach, xa hoi, kinh te va tac dong toi cuoc song
- Ky vong: hieu van de ro hon sau khi nghe

Thong tin bai bao:
Tieu de: {article.title}
Nguon: {article.source.upper()}
Noi dung nguon:
{content}
"""

    def create_section_request(
        self,
        section_type: str,
        target_words: int,
        article: NewsArticle,
        user_prompt: str,
        style: str,
    ) -> Dict[str, str]:
        heading = {
            "intro": "Mo dau:",
            "main": "Noi dung chinh:",
            "outro": "Ket luan:",
        }.get(section_type, "")
        min_section_words = max(80, int(target_words * 0.9))
        max_section_words = int(target_words * 1.1)

        system_prompts = {
            "intro": (
                f"Viet rieng phan mo dau. Heading phai la '{heading}'. "
                f"Muc tieu {target_words} tu, chap nhan {min_section_words}-{max_section_words} tu. "
                f"Can co hook, boi canh va dan vao chu de. Phong cach: {style}. "
                "Khong markdown, khong bullet."
            ),
            "main": (
                f"Viet rieng phan noi dung chinh. Heading phai la '{heading}'. "
                f"Muc tieu {target_words} tu, chap nhan {min_section_words}-{max_section_words} tu. "
                "Day la phan dai nhat, phai khai thac du du kien, nguyen nhan, tac dong, dien giai va ket noi y. "
                f"Phong cach: {style}. Khong markdown, khong bullet."
            ),
            "outro": (
                f"Viet rieng phan ket luan. Heading phai la '{heading}'. "
                f"Muc tieu {target_words} tu, chap nhan {min_section_words}-{max_section_words} tu. "
                "Chot thong diep gon, ro va khong cut y. "
                f"Phong cach: {style}. Khong markdown, khong bullet."
            ),
        }

        return {
            "system_prompt": system_prompts.get(section_type, ""),
            "user_prompt": f"""Dua tren thong tin sau de viet phan {section_type}.

Yeu cau nguoi dung: {user_prompt}

Tieu de bai bao: {article.title}
Noi dung bai bao:
{ContentCleanerTool.truncate_content(article.content, 2200)}

Hay viet phan {section_type} gan {target_words} tu nhat co the, khong duoc thap hon {min_section_words} tu.""",
        }

    def create_section_retry_prompt(
        self, section_type: str, target_words: int, actual_words: int, user_content: str
    ) -> str:
        min_section_words = max(80, int(target_words * 0.9))
        max_section_words = int(target_words * 1.1)
        return f"""Phan {section_type} truoc do co {actual_words} tu nen chua dat muc tieu.
Hay viet lai gan {target_words} tu nhat co the, bat buoc nam trong {min_section_words}-{max_section_words} tu.

{user_content}

Tang do chi tiet, them chuyen y va dien giai de dat dung do dai."""

    def create_outline_request(
        self, article: NewsArticle, user_prompt: str, target_length: str, min_words: int
    ) -> Dict[str, str]:
        return {
            "system_prompt": (
                f"Tao outline cho kich ban {target_length}, toi thieu {min_words} tu. "
                "Outline phai chia ro mo dau, noi dung chinh, ket luan va du y de mo rong noi dung."
            ),
            "user_prompt": f"""Yeu cau: {user_prompt}

Tieu de: {article.title}
Noi dung:
{ContentCleanerTool.truncate_content(article.content, 2000)}""",
        }

    def create_base_script_request(
        self, article: NewsArticle, user_prompt: str, outline: str, style: str
    ) -> Dict[str, str]:
        return {
            "system_prompt": (
                f"Viet kich ban day du theo outline, giu phong cach {style}. "
                "Khong markdown dam. Giu heading dang van ban thuong."
            ),
            "user_prompt": f"""Outline:
{outline}

Yeu cau goc:
{user_prompt}

Noi dung bai bao:
{ContentCleanerTool.truncate_content(article.content, 2500)}""",
        }

    def create_expand_script_request(
        self, current_script: str, article: NewsArticle, user_prompt: str, words_needed: int
    ) -> Dict[str, str]:
        return {
            "system_prompt": (
                f"Mo rong kich ban hien tai them khoang {words_needed} tu. "
                "Giu nguyen cau truc, khong lap y, bo sung bang phan tich va chuyen y tu nhien."
            ),
            "user_prompt": f"""Kich ban hien tai:
{current_script}

Yeu cau goc:
{user_prompt}

Thong tin bo sung:
{ContentCleanerTool.truncate_content(article.content, 1500)}""",
        }

    def create_short_retry_prompt(
        self, user_content: str, word_count: int, min_words: int, max_words: int
    ) -> str:
        target_words = self._target_word_count(min_words, max_words)
        return f"""Kich ban truoc chi co {word_count} tu nen chua dat yeu cau.
Hay viet lai voi muc tieu khoang {target_words} tu, bat buoc trong {min_words}-{max_words} tu.

{user_content}

Them dien giai, tac dong va chuyen y de dat dung thoi luong."""


class NewsScriptAgent(NewsAgentProcessingMixin):
    """News agent tao kich ban tu tin tuc."""

    def __init__(self, ai_model: str = "gpt-3.5-turbo", api_key: str = None):
        self.ai_model = ai_model
        self.api_key = api_key
        self.news_processor = NewsProcessorBackend()
        self.prompt_builder = NewsScriptPromptBuilder()
        self.script_generator = (
            ScriptGeneratorBackend(ai_model, api_key, self.prompt_builder) if api_key else None
        )

        logging.basicConfig(level=logging.INFO)
        self.logger = logging.getLogger(__name__)

        self.current_article = None
        self.current_scripts: List[str] = []
        self.current_combined_metadata: Optional[Dict[str, Any]] = None
        self.processing_history: List[Dict[str, Any]] = []

    def create_document(self, script: str, script_number: int = 1) -> bytes:
        """Tao document Word cho kich ban."""
        if self.current_combined_metadata:
            article_info = {
                "title": (
                    f"Tong hop tu "
                    f"{self.current_combined_metadata['combined_info']['total_articles']} bai bao"
                ),
                "url": f"{self.current_combined_metadata['combined_info']['total_articles']} URLs",
                "source": ", ".join(self.current_combined_metadata["combined_info"]["sources"]),
                "word_count": self.current_combined_metadata["combined_info"]["total_word_count"],
            }
        elif self.current_article:
            article_info = {
                "title": self.current_article.title,
                "url": self.current_article.url,
                "source": self.current_article.source,
                "word_count": self.current_article.get_word_count(),
            }
        else:
            raise ValueError("Khong co bai bao hien tai de tao document")

        return self.news_processor.create_document_for_script(script, article_info, script_number)

    def get_script_statistics(self, script: str) -> Dict[str, Any]:
        """Lay thong ke cho kich ban."""
        return self.news_processor.get_script_statistics(script)

    def get_agent_status(self) -> Dict[str, Any]:
        """Lay trang thai hien tai cua agent."""
        return {
            "ai_model": self.ai_model,
            "has_api_key": bool(self.api_key),
            "current_article": (
                {
                    "title": self.current_article.title,
                    "url": self.current_article.url,
                    "word_count": self.current_article.get_word_count(),
                }
                if self.current_article
                else None
            ),
            "current_scripts_count": len(self.current_scripts),
            "processing_history_count": len(self.processing_history),
            "last_processing": self.processing_history[-1] if self.processing_history else None,
        }
