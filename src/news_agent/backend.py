"""
Backend cho News Agent: crawl tin tức, tạo tài liệu và sinh kịch bản.
"""

from typing import Any, Callable, Dict, List, Optional
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

    @staticmethod
    def _emit_progress(
        callback: Optional[Callable[[Dict[str, Any]], None]],
        completed_units: int,
        status: str,
        **extra: Any,
    ) -> None:
        """Đẩy tiến trình sinh kịch bản ra ngoài."""
        if not callback:
            return

        callback(
            {
                "completed_units": max(0, int(completed_units)),
                "status": status,
                **extra,
            }
        )

    def _calculate_target_words(self, target_length: str) -> tuple[int, int]:
        """Tính khoảng số từ từ thời lượng mục tiêu."""
        words_per_minute = 130
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
            "MO DAU": "Mở đầu:",
            "NỘI DUNG CHÍNH": "Nội dung chính:",
            "NOI DUNG CHINH": "Nội dung chính:",
            "KẾT LUẬN": "Kết luận:",
            "KET LUAN": "Kết luận:",
            "INTRO": "Mở đầu:",
            "OUTRO": "Kết luận:",
        }

        for raw_heading, plain_heading in heading_map.items():
            pattern = rf"(?im)^\s*\*\*\s*{raw_heading}\s*:?\s*\*\*\s*$"
            script = re.sub(pattern, plain_heading, script)
            plain_pattern = rf"(?im)^\s*{raw_heading}\s*:?\s*$"
            script = re.sub(plain_pattern, plain_heading, script)

        script = re.sub(
            r"(?im)^\s*\*\*(Mở đầu|Nội dung chính|Kết luận)\s*:?\*\*\s*$",
            r"\1:",
            script,
        )
        script = re.sub(r"(?im)^\s*Mo dau\s*:?\s*$", "Mở đầu:", script)
        script = re.sub(r"(?im)^\s*Noi dung chinh\s*:?\s*$", "Nội dung chính:", script)
        script = re.sub(r"(?im)^\s*Ket luan\s*:?\s*$", "Kết luận:", script)
        return script.strip()

    def generate_script(
        self,
        article: NewsArticle,
        user_prompt: str = "",
        target_length: str = "3-5 phút",
        style: str = "trang trọng",
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        current_script: int = 1,
        total_scripts: int = 1,
    ) -> Optional[str]:
        """Tạo kịch bản từ bài báo."""
        try:
            min_words, max_words = self._calculate_target_words(target_length)
            self.logger.info(f"Tạo kịch bản {target_length}: cần {min_words}-{max_words} từ")

            if min_words >= 600:
                return self._generate_script_with_iterative_expansion(
                    article,
                    user_prompt,
                    target_length,
                    style,
                    min_words,
                    max_words,
                    progress_callback=progress_callback,
                    current_script=current_script,
                    total_scripts=total_scripts,
                )

            return self._generate_short_script(
                article,
                user_prompt,
                target_length,
                style,
                min_words,
                max_words,
                progress_callback=progress_callback,
                current_script=current_script,
                total_scripts=total_scripts,
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
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        current_script: int = 1,
        total_scripts: int = 1,
    ) -> Optional[str]:
        """Sinh kịch bản dài theo từng phần."""
        self.logger.info(f"Dùng chiến lược sinh từng phần cho kịch bản {target_length}")

        try:
            intro_words = max(180, int(min_words * 0.15))
            outro_words = max(160, int(min_words * 0.12))
            main_words = max(min_words - intro_words - outro_words, int(min_words * 0.7))

            self._emit_progress(
                progress_callback,
                0,
                f"Đang viết mở đầu cho kịch bản {current_script}/{total_scripts}...",
                current_script=current_script,
                total_scripts=total_scripts,
                section="intro",
            )
            intro = self._generate_script_section("intro", intro_words, article, user_prompt, style)
            self._emit_progress(
                progress_callback,
                4,
                f"Đã xong phần mở đầu, đang viết nội dung chính cho kịch bản {current_script}/{total_scripts}...",
                current_script=current_script,
                total_scripts=total_scripts,
                section="main",
            )
            main_content = self._generate_script_section("main", main_words, article, user_prompt, style)
            self._emit_progress(
                progress_callback,
                11,
                f"Đã xong nội dung chính, đang viết kết luận cho kịch bản {current_script}/{total_scripts}...",
                current_script=current_script,
                total_scripts=total_scripts,
                section="outro",
            )
            outro = self._generate_script_section("outro", outro_words, article, user_prompt, style)

            if not intro or not main_content or not outro:
                self._emit_progress(
                    progress_callback,
                    15,
                    f"Kịch bản {current_script}/{total_scripts} không tạo được đầy đủ các phần.",
                    current_script=current_script,
                    total_scripts=total_scripts,
                    section="failed",
                )
                return None

            full_script = f"{intro}\n\n{main_content}\n\n{outro}"
            final_words = len(full_script.split())
            self.logger.info(f"Tạo kịch bản dài thành công: {final_words} từ")
            self._emit_progress(
                progress_callback,
                15,
                f"Đã hoàn tất kịch bản {current_script}/{total_scripts}.",
                current_script=current_script,
                total_scripts=total_scripts,
                section="completed",
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

    def _generate_short_script(
        self,
        article: NewsArticle,
        user_prompt: str,
        target_length: str,
        style: str,
        min_words: int,
        max_words: int,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
        current_script: int = 1,
        total_scripts: int = 1,
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

            self._emit_progress(
                progress_callback,
                0,
                f"Đang tạo bản nháp cho kịch bản {current_script}/{total_scripts}...",
                current_script=current_script,
                total_scripts=total_scripts,
                section="draft",
            )
            script = self.ai_tool.generate_text(system_prompt, user_content, max_tokens=max_tokens)
            if not script:
                self._emit_progress(
                    progress_callback,
                    15,
                    f"Kịch bản {current_script}/{total_scripts} không tạo được bản nháp.",
                    current_script=current_script,
                    total_scripts=total_scripts,
                    section="failed",
                )
                return None

            word_count = len(script.split())
            self.logger.info(f"Tạo kịch bản ngắn thành công: {word_count} từ")

            if not self._is_word_count_acceptable(word_count, min_words, max_words):
                self._emit_progress(
                    progress_callback,
                    8,
                    f"Kịch bản {current_script}/{total_scripts} đang được cân chỉnh lại độ dài...",
                    current_script=current_script,
                    total_scripts=total_scripts,
                    section="retry",
                )
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

            self._emit_progress(
                progress_callback,
                15,
                f"Đã hoàn tất kịch bản {current_script}/{total_scripts}.",
                current_script=current_script,
                total_scripts=total_scripts,
                section="completed",
            )
            return self._normalize_script_format(script)
        except Exception as exc:
            self.logger.error(f"Lỗi tạo kịch bản ngắn: {exc}")
            return None

    def _append_references_to_script(self, script: str, articles_urls: List[str]) -> str:
        """Thêm tối đa 3 link nguồn ở cuối kịch bản."""
        clean_urls = [url.strip() for url in (articles_urls or []) if url and url.strip()]
        if not clean_urls:
            return script

        references_section = "\n\nNguồn tham khảo:\n"
        for index, url in enumerate(clean_urls[:3], 1):
            references_section += f"{index}. {url}\n"

        return script.rstrip() + "\n" + references_section.rstrip()

    def generate_multiple_scripts(
        self,
        article: NewsArticle,
        user_prompt: str = "",
        target_length: str = "3-5 phút",
        num_scripts: int = 1,
        articles_urls: List[str] = None,
        progress_callback: Optional[Callable[[Dict[str, Any]], None]] = None,
    ) -> List[str]:
        """Tạo nhiều phiên bản kịch bản với các phong cách khác nhau."""
        scripts: List[str] = []
        articles_urls = articles_urls or []
        units_per_script = 15

        for i in range(num_scripts):
            try:
                script_index = i + 1
                base_units = i * units_per_script
                self._emit_progress(
                    progress_callback,
                    base_units,
                    f"Đang chuẩn bị kịch bản {script_index}/{num_scripts}...",
                    current_script=script_index,
                    total_scripts=num_scripts,
                    section="setup",
                )
                style = self.prompt_builder.STYLES[i % len(self.prompt_builder.STYLES)]
                enhanced_prompt = self.prompt_builder.create_enhanced_prompt_for_script(
                    user_prompt, style, script_index, num_scripts
                )
                script = self.generate_script(
                    article,
                    enhanced_prompt,
                    target_length,
                    style,
                    progress_callback=(
                        lambda payload, base_units=base_units, script_index=script_index: self._emit_progress(
                            progress_callback,
                            base_units + payload.get("completed_units", 0),
                            payload.get("status", "Đang tạo kịch bản..."),
                            current_script=payload.get("current_script", script_index),
                            total_scripts=payload.get("total_scripts", num_scripts),
                            section=payload.get("section"),
                        )
                    ),
                    current_script=script_index,
                    total_scripts=num_scripts,
                )
                if script:
                    if articles_urls:
                        script = self._append_references_to_script(script, articles_urls)
                    scripts.append(script)
                else:
                    self._emit_progress(
                        progress_callback,
                        base_units + units_per_script,
                        f"Kịch bản {script_index}/{num_scripts} không tạo thành công.",
                        current_script=script_index,
                        total_scripts=num_scripts,
                        section="failed",
                    )

                if i < num_scripts - 1:
                    time.sleep(1)
            except Exception as exc:
                self.logger.error(f"Lỗi tạo kịch bản {i + 1}: {exc}")

        return scripts
