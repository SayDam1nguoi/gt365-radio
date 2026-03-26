"""
News agent chính: điều phối và quản lý trạng thái.
"""

from typing import Any, Callable, Dict, List, Optional
import logging

from .backend import NewsProcessorBackend, ScriptGeneratorBackend
from ..processing import NewsAgentProcessingMixin
from .tools import ContentCleanerTool
from ..models.news_article import NewsArticle


class NewsScriptPromptBuilder:
    """Xây dựng prompt cho agent."""

    STYLES = [
        "Ngắn",
        "Bình thường",
        "Chuyên sâu",
    ]

    @staticmethod
    def _target_word_count(min_words: int, max_words: int) -> int:
        return (min_words + max_words) // 2

    def create_combined_prompt(self, user_prompt: str, article_count: int) -> str:
        default_prompt = "Viết một kịch bản mạch lạc, dễ đọc thành lời, có phân tích rõ ràng."
        return (
            f"Tạo kịch bản tổng hợp từ {article_count} bài báo. "
            f"Kết hợp thông tin thành một mạch kể chuyện thống nhất. "
            f"{user_prompt.strip() if user_prompt and user_prompt.strip() else default_prompt}"
        )

    def create_enhanced_prompt_for_script(
        self, user_prompt: str, style: str, script_number: int, total_scripts: int
    ) -> str:
        base_prompt = user_prompt.strip() if user_prompt and user_prompt.strip() else ""
        return (
            f"Kịch bản số {script_number}/{total_scripts}. "
            f"Phong cách ưu tiên: {style}. "
            f"{base_prompt}".strip()
        )

    def create_script_system_prompt(
        self, target_length: str, style: str, min_words: int, max_words: int
    ) -> str:
        target_words = self._target_word_count(min_words, max_words)
        
        # Hướng dẫn cụ thể cho mỗi phong cách
        style_instruction = ""
        if "Ngắn" in style:
            style_instruction = (
                "Phong cách NGẮN: Nói qua nhanh, vắn tắt, chỉ nêu những điểm chính, sự kiện then chốt. "
                "Không cần giải thích chi tiết, tập trung vào các thông tin quan trọng nhất."
            )
        elif "Chuyên sâu" in style:
            style_instruction = (
                "Phong cách CHUYÊN SÂU: Phân tích kỹ càng, nêu rõ ảnh hưởng tích cực và tiêu cực của vấn đề. "
                "Đi sâu vào nguyên nhân, hệ quả, quan điểm khác nhau và mong đợi phía trước. "
                "Cần khai thác đầy đủ bối cảnh, ý nghĩa và chiều sâu của sự kiện."
            )
        else:  # Bình thường
            style_instruction = (
                "Phong cách BÌNH THƯỜNG: Nói tin tức một cách tự nhiên, phân tích nhẹ nhàng, dễ hiểu cho công chúng rộng. "
                "Kết hợp thông tin cơ bản với phân tích cân bằng, không quá sâu nhưng cũng không thiếu sự liên kết."
            )
        
        return f"""Bạn là biên tập viên viết kịch bản tin tức tiếng Việt cho radio/podcast.

Mục tiêu thời lượng: {target_length}.
Mục tiêu số từ: ưu tiên gần {target_words} từ nhất có thể. Bắt buộc nằm trong {min_words}-{max_words} từ.

{style_instruction}

Quy tắc bắt buộc:
- Luôn viết bằng tiếng Việt có dấu đầy đủ và đúng chính tả.
- Bám sát dữ kiện từ bài nguồn.
- Viết thành kịch bản hoàn chỉnh, dễ đọc thành lời.
- Không dùng markdown đậm, không dùng bullet list trong phần kịch bản.
- Heading phải ở dạng văn bản thường:
Mở đầu:
Nội dung chính:
Kết luận:
- Ưu tiên đúng mục tiêu số từ hơn việc viết ngắn cho xong.

Cách triển khai:
- Mở đầu và đặt bối cảnh.
- Nội dung chính là phần dài nhất, phù hợp với phong cách đã chọn.
- Kết luận chốt thông điệp.
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
            "Viết rõ ý, dễ đọc thành lời và có phân tích."
        )

        return f"""Yêu cầu của người dùng:
{instruction}

Mục tiêu thời lượng: {target_length}
Mục tiêu số từ: khoảng {target_words} từ, bắt buộc trong {min_words}-{max_words} từ.
Ưu tiên tuân thủ số từ và thời lượng. Không viết quá ngắn.

Đối tượng người nghe:
- Độ tuổi: 25-60
- Quan tâm: chính sách, xã hội, kinh tế và tác động tới cuộc sống
- Kỳ vọng: hiểu vấn đề rõ hơn sau khi nghe

Yêu cầu ngôn ngữ:
- Bắt buộc dùng tiếng Việt có dấu đầy đủ ở toàn bộ kịch bản.

Thông tin bài báo:
Tiêu đề: {article.title}
Nguồn: {article.source.upper()}
Nội dung nguồn:
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
            "intro": "Mở đầu:",
            "main": "Nội dung chính:",
            "outro": "Kết luận:",
        }.get(section_type, "")
        min_section_words = max(80, int(target_words * 0.9))
        max_section_words = int(target_words * 1.1)

        system_prompts = {
            "intro": (
                f"Viết riêng phần mở đầu. Heading phải là '{heading}'. "
                f"Cần có hook, bối cảnh và dẫn vào chủ đề. Phong cách: {style}. "
                "Bắt buộc viết bằng tiếng Việt có dấu. Không markdown, không bullet."
            ),
            "main": (
                f"Viết riêng phần nội dung chính. Heading phải là '{heading}'. "
                "Đây là phần dài nhất, phải khai thác đủ dữ kiện, nguyên nhân, tác động, diễn giải và kết nối ý. "
                f"Phong cách: {style}. Bắt buộc viết bằng tiếng Việt có dấu. Không markdown, không bullet."
            ),
            "outro": (
                f"Viết riêng phần kết luận. Heading phải là '{heading}'. "
                "Chốt thông điệp rõ và không cụt ý. "
                f"Phong cách: {style}. Bắt buộc viết bằng tiếng Việt có dấu. Không markdown, không bullet."
            ),
        }

        return {
            "system_prompt": system_prompts.get(section_type, ""),
            "user_prompt": f"""Dựa trên thông tin sau để viết phần {section_type}.

Yêu cầu người dùng: {user_prompt}

Tiêu đề bài báo: {article.title}
Nội dung bài báo:
{ContentCleanerTool.truncate_content(article.content, 2200)}

Hãy viết phần {section_type} đầy đủ và phải dùng tiếng Việt có dấu.""",
        }

    def create_section_retry_prompt(
        self, section_type: str, target_words: int, actual_words: int, user_content: str
    ) -> str:
        return f"""Phần {section_type} trước đó chưa đạt yêu cầu.
Hãy viết lại đầy đủ và chi tiết hơn.

{user_content}

Tăng độ chi tiết, thêm chuyển ý và diễn giải để đạt đúng thời lượng. Bắt buộc giữ tiếng Việt có dấu."""

    def create_outline_request(
        self, article: NewsArticle, user_prompt: str, target_length: str, min_words: int
    ) -> Dict[str, str]:
        return {
            "system_prompt": (
                f"Tạo outline cho kịch bản {target_length}, tối thiểu {min_words} từ. "
                "Outline phải chia rõ mở đầu, nội dung chính, kết luận và đủ ý để mở rộng nội dung. "
                "Bắt buộc dùng tiếng Việt có dấu."
            ),
            "user_prompt": f"""Yêu cầu: {user_prompt}

Tiêu đề: {article.title}
Nội dung:
{ContentCleanerTool.truncate_content(article.content, 2000)}""",
        }

    def create_base_script_request(
        self, article: NewsArticle, user_prompt: str, outline: str, style: str
    ) -> Dict[str, str]:
        return {
            "system_prompt": (
                f"Viết kịch bản đầy đủ theo outline, giữ phong cách {style}. "
                "Không markdown đậm. Giữ heading dạng văn bản thường. Bắt buộc dùng tiếng Việt có dấu."
            ),
            "user_prompt": f"""Outline:
{outline}

Yêu cầu gốc:
{user_prompt}

Nội dung bài báo:
{ContentCleanerTool.truncate_content(article.content, 2500)}""",
        }

    def create_expand_script_request(
        self, current_script: str, article: NewsArticle, user_prompt: str
    ) -> Dict[str, str]:
        return {
            "system_prompt": (
                "Mở rộng kịch bản hiện tại bằng phân tích, diễn giải và chuyển ý tự nhiên. "
                "Giữ nguyên cấu trúc, không lặp ý. "
                "Bắt buộc dùng tiếng Việt có dấu."
            ),
            "user_prompt": f"""Kịch bản hiện tại:
{current_script}

Yêu cầu gốc:
{user_prompt}

Thông tin bổ sung:
{ContentCleanerTool.truncate_content(article.content, 1500)}""",
        }

    def create_short_retry_prompt(
        self, user_content: str, word_count: int, min_words: int, max_words: int
    ) -> str:
        return f"""Kịch bản trước chưa đạt yêu cầu. Hãy viết lại đầy đủ và chi tiết hơn.

{user_content}

Thêm diễn giải và chuyển ý để đạt đúng thời lượng. Bắt buộc dùng tiếng Việt có dấu."""


class NewsScriptAgent(NewsAgentProcessingMixin):
    """News agent tạo kịch bản từ tin tức."""

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
        self.progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None

    def create_document(self, script: str, script_number: int = 1) -> bytes:
        """Tạo document Word cho kịch bản."""
        if self.current_combined_metadata:
            article_info = {
                "title": (
                    f"Tổng hợp từ "
                    f"{self.current_combined_metadata['combined_info']['total_articles']} bài báo"
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
            raise ValueError("Không có bài báo hiện tại để tạo document")

        return self.news_processor.create_document_for_script(script, article_info, script_number)

    def get_script_statistics(self, script: str) -> Dict[str, Any]:
        """Lấy thống kê cho kịch bản."""
        return self.news_processor.get_script_statistics(script)

    def get_agent_status(self) -> Dict[str, Any]:
        """Lấy trạng thái hiện tại của agent."""
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

    def set_progress_callback(self, callback: Optional[Callable[[Dict[str, Any]], None]]) -> None:
        """Gắn callback để đẩy tiến trình xử lý ra UI."""
        self.progress_callback = callback
