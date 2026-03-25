"""
Backend cho News Agent: crawl tin tức, tạo tài liệu và sinh kịch bản.
"""

from typing import Any, Dict, List, Optional
import logging
import re
import time

from .tools import AIModelTool, DocumentTool, UniversalWebCrawlerTool
from ..models.news_article import NewsArticle


class NewsProcessorBackend:
    """Backend xử lý bài báo đầu vào."""

    def __init__(self):
        self.crawler_tool = UniversalWebCrawlerTool()
        self.document_tool = DocumentTool()
        self.logger = logging.getLogger(__name__)

    def extract_article_from_url(self, url: str, source: str = None) -> Optional[NewsArticle]:
        """Trích xuất bài báo từ URL."""
        try:
            self.logger.info(f"Đang crawl từ: {url}")

            soup = self.crawler_tool.fetch_page(url)
            if not soup:
                return None

            article_data = self.crawler_tool.auto_extract_content(soup, url)
            if not article_data:
                self.logger.warning(f"Không thể trích xuất nội dung từ: {url}")
                return None

            article = NewsArticle(
                url=article_data["url"],
                title=article_data["title"],
                content=article_data["content"],
                source=article_data["source"],
                publish_time=article_data.get("publish_time"),
            )

            if article.is_valid():
                self.logger.info(f"Trích xuất thành công từ {article.source}: {article.title[:60]}...")
                return article

            self.logger.warning(f"Bài báo không hợp lệ: {url}")
            return None
        except Exception as exc:
            self.logger.error(f"Lỗi trích xuất bài báo {url}: {exc}")
            return None

    def create_document_for_script(
        self, script: str, article_info: Dict[str, Any], script_number: int = 1
    ) -> bytes:
        """Tạo file Word cho kịch bản."""
        title = f"KỊCH BẢN {script_number}"
        metadata = {
            "Tiêu đề nguồn": article_info.get("title", "N/A"),
            "Nguồn": article_info.get("source", "N/A").upper(),
            "Số từ bài gốc": article_info.get("word_count", "N/A"),
        }
        return self.document_tool.create_word_document(title, script, metadata)

    def get_script_statistics(self, script: str) -> Dict[str, Any]:
        """Lấy thống kê kịch bản."""
        return self.document_tool.get_text_stats(script)


class ScriptGeneratorBackend:
    """Backend sinh kịch bản. Prompt được xây dựng ở agent."""

    def __init__(self, model: str, api_key: str, prompt_builder):
        self.ai_tool = AIModelTool(model, api_key)
        self.prompt_builder = prompt_builder
        self.logger = logging.getLogger(__name__)

    def _calculate_target_words(self, target_length: str) -> tuple[int, int]:
        """Tính khoảng số từ từ thời lượng mục tiêu."""
        words_per_minute = 160
        numbers = re.findall(r"\d+", target_length)

        if len(numbers) == 1:
            minutes = int(numbers[0])
            min_words = minutes * words_per_minute
            max_words = min_words + (words_per_minute // 2)
        elif len(numbers) == 2:
            min_words = int(numbers[0]) * words_per_minute
            max_words = int(numbers[1]) * words_per_minute
        else:
            min_words = 3 * words_per_minute
            max_words = 5 * words_per_minute

        return min_words, max_words

    @staticmethod
    def _is_word_count_acceptable(word_count: int, min_words: int, max_words: int) -> bool:
        return min_words <= word_count <= max_words

    def _normalize_script_format(self, script: str) -> str:
        """Chuẩn hóa heading về dạng văn bản thường."""
        if not script:
            return script

        heading_map = {
            "MỞ ĐẦU": "Mở đầu:",
            "NỘI DUNG CHÍNH": "Nội dung chính:",
            "KẾT LUẬN": "Kết luận:",
            "INTRO": "Mở đầu:",
            "OUTRO": "Kết luận:",
        }

        for raw_heading, plain_heading in heading_map.items():
            pattern = rf"(?im)^\s*\*\*\s*{raw_heading}\s*:?\s*\*\*\s*$"
            script = re.sub(pattern, plain_heading, script)

        script = re.sub(
            r"(?im)^\s*\*\*(Mở đầu|Nội dung chính|Kết luận)\s*:?\*\*\s*$",
            r"\1:",
            script,
        )
        return script.strip()

    def generate_script(
        self,
        article: NewsArticle,
        user_prompt: str = "",
        target_length: str = "3-5 phút",
        style: str = "trang trọng",
    ) -> Optional[str]:
        """Tạo kịch bản từ bài báo."""
        try:
            min_words, max_words = self._calculate_target_words(target_length)
            self.logger.info(f"Tạo kịch bản {target_length}: cần {min_words}-{max_words} từ")

            if min_words >= 800:
                return self._generate_script_with_iterative_expansion(
                    article, user_prompt, target_length, style, min_words, max_words
                )

            return self._generate_short_script(
                article, user_prompt, target_length, style, min_words, max_words
            )
        except Exception as exc:
            self.logger.error(f"Lỗi tạo kịch bản: {exc}")
            return None

    def _generate_script_with_iterative_expansion(
        self,
        article: NewsArticle,
        user_prompt: str,
        target_length: str,
        style: str,
        min_words: int,
        max_words: int,
    ) -> Optional[str]:
        """Sinh kịch bản dài theo từng phần."""
        self.logger.info(f"Dùng chiến lược sinh từng phần cho kịch bản {target_length}")

        try:
            intro_words = max(180, int(min_words * 0.15))
            outro_words = max(160, int(min_words * 0.12))
            main_words = max(min_words - intro_words - outro_words, int(min_words * 0.7))

            intro = self._generate_script_section("intro", intro_words, article, user_prompt, style)
            main_content = self._generate_script_section("main", main_words, article, user_prompt, style)
            outro = self._generate_script_section("outro", outro_words, article, user_prompt, style)

            if not intro or not main_content or not outro:
                return None

            full_script = f"{intro}\n\n{main_content}\n\n{outro}"
            final_words = len(full_script.split())
            self.logger.info(
                f"Tạo kịch bản dài thành công: {final_words} từ (mục tiêu: {min_words}-{max_words} từ)"
            )
            return self._normalize_script_format(full_script)
        except Exception as exc:
            self.logger.error(f"Lỗi tạo kịch bản dài: {exc}")
            return None

    def _generate_script_section(
        self,
        section_type: str,
        target_words: int,
        article: NewsArticle,
        user_prompt: str,
        style: str,
    ) -> Optional[str]:
        """Sinh một phần riêng của kịch bản."""
        request = self.prompt_builder.create_section_request(
            section_type, target_words, article, user_prompt, style
        )
        system_prompt = request.get("system_prompt", "")
        user_content = request.get("user_prompt", "")
        if not system_prompt or not user_content:
            return None

        try:
            max_tokens = min(4000, target_words * (4 if section_type == "main" else 3))
            max_tokens = max(1500, max_tokens)

            section_content = self.ai_tool.generate_text(
                system_prompt, user_content, max_tokens=max_tokens
            )
            if not section_content:
                return None

            actual_words = len(section_content.split())
            self.logger.info(f"Tạo phần {section_type}: {actual_words} từ")

            min_section_words = max(80, int(target_words * 0.9))
            max_section_words = int(target_words * 1.1)

            if actual_words < min_section_words or actual_words > max_section_words:
                retry_content = self.ai_tool.generate_text(
                    system_prompt,
                    self.prompt_builder.create_section_retry_prompt(
                        section_type, target_words, actual_words, user_content
                    ),
                    max_tokens=max_tokens,
                )
                if retry_content:
                    retry_words = len(retry_content.split())
                    if abs(retry_words - target_words) < abs(actual_words - target_words):
                        section_content = retry_content

            return section_content
        except Exception as exc:
            self.logger.error(f"Lỗi tạo phần {section_type}: {exc}")
            return None

    def _create_detailed_outline(
        self,
        article: NewsArticle,
        user_prompt: str,
        target_length: str,
        style: str,
        min_words: int,
    ) -> Optional[str]:
        """Tạo outline chi tiết cho kịch bản dài."""
        request = self.prompt_builder.create_outline_request(
            article, user_prompt, target_length, min_words
        )
        try:
            return self.ai_tool.generate_text(
                request["system_prompt"], request["user_prompt"], max_tokens=2000
            )
        except Exception as exc:
            self.logger.error(f"Lỗi tạo outline: {exc}")
            return None

    def _create_base_script_from_outline(
        self,
        article: NewsArticle,
        user_prompt: str,
        outline: str,
        style: str,
    ) -> Optional[str]:
        """Tạo bản nháp từ outline."""
        request = self.prompt_builder.create_base_script_request(
            article, user_prompt, outline, style
        )
        try:
            return self.ai_tool.generate_text(
                request["system_prompt"], request["user_prompt"], max_tokens=4000
            )
        except Exception as exc:
            self.logger.error(f"Lỗi tạo kịch bản cơ bản: {exc}")
            return None

    def _expand_script_to_target_length(
        self,
        base_script: str,
        article: NewsArticle,
        user_prompt: str,
        style: str,
        min_words: int,
        max_words: int,
    ) -> Optional[str]:
        """Mở rộng kịch bản tới số từ mục tiêu."""
        current_script = base_script
        current_words = len(current_script.split())

        if current_words >= min_words:
            return current_script

        for _ in range(3):
            words_needed = min_words - current_words
            if words_needed <= 0:
                break

            expanded_script = self._expand_script_content(
                current_script, article, user_prompt, style, words_needed
            )
            if not expanded_script or len(expanded_script) <= len(current_script):
                break

            current_script = expanded_script
            current_words = len(current_script.split())

        return current_script

    def _expand_script_content(
        self,
        current_script: str,
        article: NewsArticle,
        user_prompt: str,
        style: str,
        words_needed: int,
    ) -> Optional[str]:
        """Mở rộng nội dung kịch bản."""
        request = self.prompt_builder.create_expand_script_request(
            current_script, article, user_prompt, words_needed
        )
        try:
            max_tokens = min(4000, (len(current_script.split()) + words_needed) * 2)
            return self.ai_tool.generate_text(
                request["system_prompt"], request["user_prompt"], max_tokens=max_tokens
            )
        except Exception as exc:
            self.logger.error(f"Lỗi mở rộng kịch bản: {exc}")
            return None

    def _generate_short_script(
        self,
        article: NewsArticle,
        user_prompt: str,
        target_length: str,
        style: str,
        min_words: int,
        max_words: int,
    ) -> Optional[str]:
        """Sinh kịch bản ngắn bằng một hoặc hai lần gọi AI."""
        try:
            estimated_tokens = int(max_words * 2.5) + 1000
            max_tokens = min(4000, max(2500, estimated_tokens))

            system_prompt = self.prompt_builder.create_script_system_prompt(
                target_length, style, min_words, max_words
            )
            user_content = self.prompt_builder.create_script_user_prompt(
                article, user_prompt, target_length, min_words, max_words
            )

            script = self.ai_tool.generate_text(system_prompt, user_content, max_tokens=max_tokens)
            if not script:
                return None

            word_count = len(script.split())
            self.logger.info(
                f"Tạo kịch bản ngắn thành công: {word_count} từ (mục tiêu: {min_words}-{max_words} từ)"
            )

            if not self._is_word_count_acceptable(word_count, min_words, max_words):
                retry_script = self.ai_tool.generate_text(
                    system_prompt,
                    self.prompt_builder.create_short_retry_prompt(
                        user_content, word_count, min_words, max_words
                    ),
                    max_tokens=max_tokens,
                )
                if retry_script:
                    retry_words = len(retry_script.split())
                    target_words = (min_words + max_words) // 2
                    if self._is_word_count_acceptable(retry_words, min_words, max_words):
                        script = retry_script
                    elif abs(retry_words - target_words) < abs(word_count - target_words):
                        script = retry_script

            return self._normalize_script_format(script)
        except Exception as exc:
            self.logger.error(f"Lỗi tạo kịch bản ngắn: {exc}")
            return None

    def generate_multiple_scripts(
        self,
        article: NewsArticle,
        user_prompt: str = "",
        target_length: str = "3-5 phút",
        num_scripts: int = 1,
    ) -> List[str]:
        """Tạo nhiều phiên bản kịch bản với các phong cách khác nhau."""
        scripts: List[str] = []

        for i in range(num_scripts):
            try:
                style = self.prompt_builder.STYLES[i % len(self.prompt_builder.STYLES)]
                enhanced_prompt = self.prompt_builder.create_enhanced_prompt_for_script(
                    user_prompt, style, i + 1, num_scripts
                )
                script = self.generate_script(article, enhanced_prompt, target_length, style)
                if script:
                    scripts.append(script)

                if i < num_scripts - 1:
                    time.sleep(1)
            except Exception as exc:
                self.logger.error(f"Lỗi tạo kịch bản {i + 1}: {exc}")

        return scripts
