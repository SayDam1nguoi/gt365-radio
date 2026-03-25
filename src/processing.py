"""
Xử lý dữ liệu và điều phối workflow cho News Agent.
"""
from datetime import datetime
from typing import Any, Dict, List, Tuple

from .models.news_article import NewsArticle


class NewsAgentProcessingMixin:
    """Mixin chứa phần xử lý dữ liệu của agent."""

    def understand_request(self, user_input: Dict[str, Any]) -> Dict[str, Any]:
        """Phân tích yêu cầu người dùng và lập kế hoạch xử lý."""
        try:
            urls = user_input.get("urls", [])
            if not urls and user_input.get("url"):
                urls = [user_input["url"]]

            if not urls:
                return {"success": False, "error": "Thiếu URL bài báo", "plan": None}

            if not self.api_key:
                return {"success": False, "error": "Thiếu API key cho AI model", "plan": None}

            is_multi = len(urls) > 1
            plan = {
                "task_type": "generate_combined_script" if is_multi else "generate_news_script",
                "steps": (
                    ["extract_articles", "combine_content", "generate_scripts", "prepare_outputs"]
                    if is_multi
                    else ["extract_article", "generate_scripts", "prepare_outputs"]
                ),
                "parameters": {
                    "urls": urls,
                    "source": user_input.get("source"),
                    "user_prompt": user_input.get("prompt", ""),
                    "target_length": user_input.get("length", "3-5 phút"),
                    "num_scripts": user_input.get("num_scripts", 1),
                },
                "estimated_time": self._estimate_processing_time(
                    len(urls),
                    user_input.get("num_scripts", 1),
                ),
            }
            self.logger.info(f"Đã phân tích yêu cầu: {plan['task_type']} với {len(urls)} URLs")
            return {"success": True, "error": None, "plan": plan}
        except Exception as exc:
            self.logger.error(f"Lỗi phân tích yêu cầu: {exc}")
            return {"success": False, "error": str(exc), "plan": None}

    def execute_multiple_plan(self, plan: Dict[str, Any]) -> Dict[str, Any]:
        """Thực hiện kế hoạch xử lý nhiều URL."""
        results = {
            "success": True,
            "steps_completed": [],
            "articles": [],
            "combined_content": "",
            "scripts": [],
            "metadata": {},
            "errors": [],
        }
        try:
            params = plan["parameters"]
            urls = params["urls"]

            self.logger.info(f"Bước 1: Trích xuất {len(urls)} bài báo...")
            articles = []
            for i, url in enumerate(urls, 1):
                self.logger.info(f"  Đang xử lý bài báo {i}/{len(urls)}: {url[:50]}...")
                article = self.news_processor.extract_article_from_url(url)
                if article:
                    articles.append(article)
                    self.logger.info(f"  OK bài báo {i}: {article.title[:30]}...")
                else:
                    self.logger.warning(f"  Lỗi bài báo {i}: Không thể trích xuất")
                    results["errors"].append(f"Không thể trích xuất bài báo từ URL {i}")

            if not articles:
                return {
                    "success": False,
                    "error": "Không thể trích xuất bất kỳ bài báo nào",
                    "steps_completed": ["extract_articles"],
                    "articles": [],
                    "scripts": [],
                    "metadata": {},
                    "errors": results["errors"],
                }

            results["articles"] = articles
            results["steps_completed"].append("extract_articles")

            self.logger.info("Bước 2: Tổng hợp nội dung...")
            combined_content = self._combine_articles_content(articles)
            results["combined_content"] = combined_content
            results["steps_completed"].append("combine_content")

            self.logger.info("Bước 3: Tạo kịch bản tổng hợp...")
            scripts = self._generate_scripts_from_combined_content(
                combined_content,
                articles,
                params["user_prompt"],
                params["target_length"],
                params["num_scripts"],
            )

            if not scripts:
                return {
                    "success": False,
                    "error": "Không thể tạo kịch bản từ nội dung tổng hợp",
                    "steps_completed": results["steps_completed"] + ["generate_scripts"],
                    "articles": articles,
                    "scripts": [],
                    "metadata": {},
                    "errors": results["errors"] + ["Script generation failed"],
                }

            results["scripts"] = scripts
            results["steps_completed"].append("generate_scripts")

            self.logger.info("Bước 4: Chuẩn bị kết quả...")
            metadata = self._prepare_combined_metadata(articles, scripts, params)
            results["metadata"] = metadata
            results["steps_completed"].append("prepare_outputs")

            self.current_article = None
            self.current_scripts = scripts
            self.current_combined_metadata = metadata
            self.processing_history.append(
                {
                    "timestamp": datetime.now(),
                    "urls": urls,
                    "num_articles": len(articles),
                    "num_scripts": len(scripts),
                    "success": True,
                }
            )

            self.logger.info(f"Hoàn thành tạo {len(scripts)} kịch bản từ {len(articles)} bài báo")
            return results
        except Exception as exc:
            self.logger.error(f"Lỗi thực hiện kế hoạch nhiều URLs: {exc}")
            return {
                "success": False,
                "error": str(exc),
                "steps_completed": results.get("steps_completed", []),
                "articles": results.get("articles", []),
                "scripts": results.get("scripts", []),
                "metadata": results.get("metadata", {}),
                "errors": results.get("errors", []) + [str(exc)],
            }

    def _estimate_processing_time(self, num_urls: int, num_scripts: int) -> int:
        """Ước tính thời gian xử lý."""
        return num_urls * 8 + num_scripts * 15 + 10

    def _combine_articles_content(self, articles: List[NewsArticle]) -> str:
        """Tổng hợp nội dung từ nhiều bài báo."""
        combined_parts = []
        max_content_per_article = 1000

        for i, article in enumerate(articles, 1):
            content = article.content
            if len(content) > max_content_per_article:
                half = max_content_per_article // 2
                content = content[:half] + "\n[...nội dung đã được rút gọn...]\n" + content[-half:]

            part = f"=== BÀI BÁO {i}: {article.title} ===\n"
            part += f"Nguồn: {article.source.upper()}\n"
            if article.publish_time:
                part += f"Thời gian: {article.publish_time}\n"
            part += f"\nNội dung:\n{content}\n"
            combined_parts.append(part)

        combined_content = "\n" + "=" * 50 + "\n".join(combined_parts) + "=" * 50 + "\n"
        max_total_length = 8000
        if len(combined_content) > max_total_length:
            combined_content = (
                combined_content[:max_total_length]
                + "\n[...nội dung đã được cắt ngắn để phù hợp với AI...]"
            )
        return combined_content

    def _generate_scripts_from_combined_content(
        self,
        combined_content: str,
        articles: List[NewsArticle],
        user_prompt: str,
        target_length: str,
        num_scripts: int,
    ) -> List[str]:
        """Tạo kịch bản từ nội dung tổng hợp."""
        if not self.script_generator:
            return []

        combined_article = NewsArticle(
            url="combined_articles",
            title=f"Tổng hợp từ {len(articles)} bài báo",
            content=combined_content,
            source="combined",
            summary=(
                f"Tổng hợp nội dung từ {len(articles)} bài báo: "
                + ", ".join([f"{a.title[:30]}..." for a in articles[:3]])
            ),
        )
        combined_prompt = self.prompt_builder.create_combined_prompt(user_prompt, len(articles))
        return self.script_generator.generate_multiple_scripts(
            combined_article,
            combined_prompt,
            target_length,
            num_scripts,
        )

    def _prepare_combined_metadata(
        self, articles: List[NewsArticle], scripts: List[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Chuẩn bị metadata cho kết quả tổng hợp."""
        return {
            "articles_info": [
                {
                    "title": article.title,
                    "url": article.url,
                    "source": article.source,
                    "word_count": article.get_word_count(),
                    "publish_time": article.publish_time,
                }
                for article in articles
            ],
            "combined_info": {
                "total_articles": len(articles),
                "total_word_count": sum(article.get_word_count() for article in articles),
                "sources": list(set(article.source for article in articles)),
            },
            "generation_info": {
                "ai_model": self.ai_model,
                "user_prompt": params["user_prompt"],
                "target_length": params["target_length"],
                "num_scripts_requested": params["num_scripts"],
                "num_scripts_generated": len(scripts),
                "created_at": datetime.now().isoformat(),
            },
            "scripts_stats": [self.get_script_statistics(script) for script in scripts],
        }

    def _prepare_metadata(
        self, article: NewsArticle, scripts: List[str], params: Dict[str, Any]
    ) -> Dict[str, Any]:
        """Chuẩn bị metadata cho kết quả một bài."""
        return {
            "article_info": {
                "title": article.title,
                "url": article.url,
                "source": article.source,
                "word_count": article.get_word_count(),
                "publish_time": article.publish_time,
            },
            "generation_info": {
                "ai_model": self.ai_model,
                "user_prompt": params["user_prompt"],
                "target_length": params["target_length"],
                "num_scripts_requested": params["num_scripts"],
                "num_scripts_generated": len(scripts),
                "created_at": datetime.now().isoformat(),
            },
            "scripts_stats": [self.get_script_statistics(script) for script in scripts],
        }

    def process_multiple_news_to_script(
        self,
        urls: List[str],
        prompt: str = "",
        length: str = "3-5 phút",
        num_scripts: int = 1,
        source: str = None,
    ) -> Tuple[bool, Dict[str, Any]]:
        """Xử lý nhiều URL thành kịch bản tổng hợp."""
        understanding = self.understand_request(
            {
                "urls": urls,
                "prompt": prompt,
                "length": length,
                "num_scripts": num_scripts,
                "source": source,
            }
        )
        if not understanding["success"]:
            return False, understanding

        results = self.execute_multiple_plan(understanding["plan"])
        return results["success"], results
