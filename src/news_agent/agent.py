"""
News Agent chính - điều phối và giữ trạng thái.
"""
from typing import Any, Dict, List, Optional
import logging

from .backend import NewsProcessorBackend, ScriptGeneratorBackend
from ..processing import NewsAgentProcessingMixin
from .tools import ContentCleanerTool
from ..models.news_article import NewsArticle


class NewsScriptPromptBuilder:
    """Chịu trách nhiệm xây dựng prompt cho agent."""

    STYLES = [
        "trang trọng và chuyên nghiệp",
        "thân thiện và gần gũi",
        "năng động và hấp dẫn",
    ]

    def create_combined_prompt(self, user_prompt: str, article_count: int) -> str:
        return f"""Tạo kịch bản từ nội dung tổng hợp của {article_count} bài báo.

Yêu cầu đặc biệt:
- Tổng hợp thông tin từ tất cả các bài báo
- Tạo ra nội dung mạch lạc và liền mạch
- Không lặp lại thông tin
- Ưu tiên thông tin quan trọng nhất

{user_prompt}"""

    def create_enhanced_prompt_for_script(
        self, user_prompt: str, style: str, script_number: int, total_scripts: int
    ) -> str:
        if not user_prompt or not user_prompt.strip():
            return f"Tạo kịch bản chuyên nghiệp với phong cách {style}."

        return f"""KỊCH BẢN SỐ {script_number}/{total_scripts} - PHONG CÁCH: {style.upper()}

YÊU CẦU GỐC CỦA NGƯỜI DÙNG:
{user_prompt}

HƯỚNG DẪN CHI TIẾT:
1. Tuân thủ đầy đủ yêu cầu của người dùng
2. Áp dụng phong cách "{style}"
3. Đảm bảo đúng độ dài yêu cầu
4. Có đủ mở đầu, nội dung chính và kết luận
5. Nếu người dùng yêu cầu cấu trúc cụ thể thì phải bám theo
6. Nếu người dùng yêu cầu thời lượng cụ thể thì phải đảm bảo độ dài phù hợp"""

    def create_script_system_prompt(
        self, target_length: str, style: str, min_words: int, max_words: int
    ) -> str:
        return f"""Bạn là chuyên gia viết kịch bản tin tức chuyên nghiệp. Nhiệm vụ: tạo kịch bản chính xác {target_length}.

YÊU CẦU ĐỘ DÀI:
- Viết từ {min_words} đến {max_words} từ
- Không được ngắn hơn {min_words} từ

CẤU TRÚC:
1. Mở đầu
2. Nội dung chính
3. Kết luận

TIÊU CHÍ:
- Phong cách: {style}
- Thông tin chính xác từ nguồn bài báo
- Văn phong rõ ràng, dễ hiểu, không sến"""

    def create_script_user_prompt(self, article: NewsArticle, user_prompt: str) -> str:
        content = ContentCleanerTool.truncate_content(article.content, 3000)
        if user_prompt and user_prompt.strip():
            instruction = f"""YÊU CẦU CỦA NGƯỜI DÙNG:
{user_prompt}

HƯỚNG DẪN:
- Làm đúng yêu cầu trên
- Dùng thông tin từ bài báo làm nội dung chính
- Đảm bảo có đủ mở đầu, nội dung chính và kết luận"""
        else:
            instruction = """YÊU CẦU MẶC ĐỊNH:
Tạo kịch bản chuyên nghiệp với đủ mở đầu, nội dung chính và kết luận."""

        return f"""{instruction}

NGUỒN THÔNG TIN:
Tiêu đề: {article.title}
Nguồn: {article.source.upper()}

Nội dung bài báo:
{content}"""

    def create_section_request(
        self,
        section_type: str,
        target_words: int,
        article: NewsArticle,
        user_prompt: str,
        style: str,
    ) -> Dict[str, str]:
        section_prompts = {
            "intro": f"""Viết phần MỞ ĐẦU với đúng {target_words} từ.
- Hook hấp dẫn
- Giới thiệu bối cảnh
- Nêu vấn đề chính
Phong cách: {style}""",
            "main": f"""Viết phần NỘI DUNG CHÍNH với đúng {target_words} từ.
- Phân tích hiện trạng và nguyên nhân
- Tác động và hệ quả
- Giải pháp hoặc góc nhìn quan trọng
Phong cách: {style}""",
            "outro": f"""Viết phần KẾT LUẬN với đúng {target_words} từ.
- Tóm tắt ý chính
- Nhấn mạnh thông điệp
- Kết thúc gọn và rõ
Phong cách: {style}""",
        }
        return {
            "system_prompt": section_prompts.get(section_type, ""),
            "user_prompt": f"""Dựa trên thông tin sau để viết phần {section_type.upper()}:

YÊU CẦU NGƯỜI DÙNG: {user_prompt}

THÔNG TIN BÀI BÁO:
Tiêu đề: {article.title}
Nội dung: {ContentCleanerTool.truncate_content(article.content, 2000)}

Viết phần {section_type} với đúng {target_words} từ.""",
        }

    def create_section_retry_prompt(
        self, section_type: str, target_words: int, actual_words: int, user_content: str
    ) -> str:
        return f"""Phần {section_type} trước chỉ có {actual_words} từ, cần viết lại với ít nhất {target_words} từ.

{user_content}

Hãy thêm chi tiết, ví dụ cụ thể và phân tích sâu hơn."""

    def create_outline_request(
        self, article: NewsArticle, user_prompt: str, target_length: str, min_words: int
    ) -> Dict[str, str]:
        return {
            "system_prompt": f"""Tạo outline chi tiết cho kịch bản {target_length} ({min_words} từ).
- Chia thành nhiều phần nhỏ
- Có mở đầu, nội dung chính, kết luận
- Đảm bảo tổng thể đạt độ dài mục tiêu""",
            "user_prompt": f"""YÊU CẦU: {user_prompt}

Tiêu đề: {article.title}
Nội dung: {ContentCleanerTool.truncate_content(article.content, 2000)}""",
        }

    def create_base_script_request(
        self, article: NewsArticle, user_prompt: str, outline: str, style: str
    ) -> Dict[str, str]:
        return {
            "system_prompt": f"""Viết kịch bản đầy đủ theo outline. Phong cách: {style}.""",
            "user_prompt": f"""OUTLINE:
{outline}

YÊU CẦU GỐC: {user_prompt}

THÔNG TIN BÀI BÁO:
{ContentCleanerTool.truncate_content(article.content, 2500)}""",
        }

    def create_expand_script_request(
        self, current_script: str, article: NewsArticle, user_prompt: str, words_needed: int
    ) -> Dict[str, str]:
        return {
            "system_prompt": f"""Mở rộng kịch bản hiện tại thêm {words_needed} từ.
- Giữ nguyên cấu trúc
- Không lặp ý
- Bổ sung tự nhiên và liền mạch""",
            "user_prompt": f"""KỊCH BẢN HIỆN TẠI:
{current_script}

YÊU CẦU GỐC: {user_prompt}

THÔNG TIN BỔ SUNG:
{ContentCleanerTool.truncate_content(article.content, 1500)}""",
        }

    def create_short_retry_prompt(self, user_content: str, word_count: int, min_words: int) -> str:
        return f"""Kịch bản trước chỉ có {word_count} từ, cần viết lại với ít nhất {min_words} từ.

{user_content}

Hãy thêm chi tiết, ví dụ và phân tích sâu hơn."""


class NewsScriptAgent(NewsAgentProcessingMixin):
    """News Agent chính để tạo kịch bản từ tin tức."""

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
