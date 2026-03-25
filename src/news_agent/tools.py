"""
Tools cho News Agent - Các công cụ cơ bản
"""
import requests
from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import time
import random
import logging
from typing import Optional, Dict, Any
import openai
import anthropic
from docx import Document
import io
from datetime import datetime

class UniversalWebCrawlerTool:
    """Tool để crawl web từ bất kỳ trang báo nào"""
    
    def __init__(self):
        self.session = requests.Session()
        self.ua = UserAgent()
        self.logger = logging.getLogger(__name__)
        
        # Setup session headers
        self.session.headers.update({
            'User-Agent': self.ua.random,
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'vi-VN,vi;q=0.9,en;q=0.8',
            'Accept-Encoding': 'gzip, deflate',
            'Connection': 'keep-alive',
        })
    
    def fetch_page(self, url: str, retries: int = 3) -> Optional[BeautifulSoup]:
        """Lấy nội dung trang web"""
        for attempt in range(retries):
            try:
                # Random delay để tránh bị block
                time.sleep(random.uniform(0.5, 2.0))
                
                # Random user agent
                self.session.headers['User-Agent'] = self.ua.random
                
                response = self.session.get(
                    url,
                    timeout=30,
                    allow_redirects=True
                )
                
                if response.status_code == 200:
                    soup = BeautifulSoup(response.content, 'html.parser')
                    self.logger.info(f"Crawl thành công: {url}")
                    return soup
                else:
                    self.logger.warning(f"HTTP {response.status_code}: {url}")
                    
            except Exception as e:
                self.logger.error(f"Lỗi crawl (attempt {attempt + 1}): {e}")
                if attempt < retries - 1:
                    time.sleep(2 ** attempt)  # Exponential backoff
        
        return None
    
    def auto_extract_content(self, soup: BeautifulSoup, url: str) -> Optional[Dict[str, str]]:
        """Tự động trích xuất nội dung từ bất kỳ trang báo nào"""
        try:
            # Detect source from URL
            source = self._detect_source_from_url(url)
            
            # Try multiple strategies to extract content
            title = self._extract_title(soup)
            content = self._extract_main_content(soup)
            publish_time = self._extract_publish_time(soup)
            
            if title and content and len(content) > 100:
                return {
                    'title': title,
                    'content': content,
                    'source': source,
                    'publish_time': publish_time,
                    'url': url
                }
            
            return None
            
        except Exception as e:
            self.logger.error(f"Lỗi auto extract từ {url}: {e}")
            return None
    
    def _detect_source_from_url(self, url: str) -> str:
        """Tự động detect nguồn từ URL"""
        url_lower = url.lower()
        
        # Known sources
        if 'nhandan.vn' in url_lower:
            return 'nhandan'
        elif 'vtv.vn' in url_lower:
            return 'vtv'
        elif 'qdnd.vn' in url_lower:
            return 'qdnd'
        elif 'vnexpress.net' in url_lower:
            return 'vnexpress'
        elif 'tuoitre.vn' in url_lower:
            return 'tuoitre'
        elif 'thanhnien.vn' in url_lower:
            return 'thanhnien'
        elif 'dantri.com.vn' in url_lower:
            return 'dantri'
        elif 'vietnamnet.vn' in url_lower:
            return 'vietnamnet'
        elif 'baomoi.com' in url_lower:
            return 'baomoi'
        else:
            # Extract domain name
            from urllib.parse import urlparse
            domain = urlparse(url).netloc
            return domain.replace('www.', '').replace('.vn', '').replace('.com', '').replace('.net', '')
    
    def _extract_title(self, soup: BeautifulSoup) -> Optional[str]:
        """Trích xuất tiêu đề bằng nhiều cách"""
        # Try multiple selectors for title
        title_selectors = [
            'h1',
            '.title',
            '.article-title',
            '.post-title',
            '.entry-title',
            '[class*="title"]',
            'title'
        ]
        
        for selector in title_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 10 and len(text) < 200:
                    return text
        
        # Fallback to page title
        title_tag = soup.find('title')
        if title_tag:
            return title_tag.get_text(strip=True)
        
        return None
    
    def _extract_main_content(self, soup: BeautifulSoup) -> Optional[str]:
        """Trích xuất nội dung chính bằng nhiều cách"""
        # Try multiple strategies
        content_parts = []
        
        # Strategy 1: Common article selectors
        article_selectors = [
            'article',
            '.article-content',
            '.post-content',
            '.entry-content',
            '.content',
            '[class*="content"]',
            '.article-body',
            '.post-body'
        ]
        
        for selector in article_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Extract paragraphs from this element
                paragraphs = element.find_all(['p', 'div'], recursive=True)
                for p in paragraphs:
                    text = p.get_text(strip=True)
                    if text and len(text) > 20:
                        content_parts.append(text)
        
        # Strategy 2: Direct paragraph extraction
        if not content_parts:
            # Look for paragraphs with specific classes
            paragraph_selectors = [
                'p.t1',  # Nhân Dân
                'p[class*="content"]',
                'p[class*="text"]',
                'div[class*="content"] p',
                'article p',
                'p'
            ]
            
            for selector in paragraph_selectors:
                elements = soup.select(selector)
                for element in elements:
                    text = element.get_text(strip=True)
                    if text and len(text) > 20:
                        content_parts.append(text)
        
        if content_parts:
            # Clean and combine content
            raw_content = ' '.join(content_parts)
            return ContentCleanerTool.clean_text(raw_content)
        
        return None
    
    def _extract_publish_time(self, soup: BeautifulSoup) -> Optional[str]:
        """Trích xuất thời gian đăng bài"""
        time_selectors = [
            'time',
            '.publish-time',
            '.date',
            '[class*="time"]',
            '[class*="date"]',
            'meta[property="article:published_time"]',
            'meta[name="pubdate"]'
        ]
        
        for selector in time_selectors:
            elements = soup.select(selector)
            for element in elements:
                # Try to get datetime attribute first
                datetime_attr = element.get('datetime') or element.get('content')
                if datetime_attr:
                    return datetime_attr
                
                # Fallback to text content
                text = element.get_text(strip=True)
                if text and len(text) > 5:
                    return text
        
        return None

class AIModelTool:
    """Tool để giao tiếp với AI models"""
    
    def __init__(self, model: str, api_key: str):
        self.model = model
        self.api_key = api_key
        self.logger = logging.getLogger(__name__)
        
        # Khởi tạo client AI
        if "gpt" in model.lower():
            openai.api_key = api_key
            self.client_type = "openai"
        elif "claude" in model.lower():
            self.client = anthropic.Anthropic(api_key=api_key)
            self.client_type = "anthropic"
        else:
            raise ValueError(f"Model {model} không được hỗ trợ")
    
    def generate_text(self, system_prompt: str, user_prompt: str, max_tokens: int = 2000, temperature: float = 0.7) -> Optional[str]:
        """Tạo text từ AI model với kiểm tra độ dài và xử lý lỗi token"""
        try:
            # Ước tính số tokens (1 token ≈ 3 ký tự cho tiếng Việt)
            total_chars = len(system_prompt) + len(user_prompt)
            estimated_tokens = total_chars // 3  # Conservative estimate
            
            # Giới hạn cho GPT-3.5-turbo là 16,385 tokens
            max_input_tokens = 14000  # Để lại buffer cho response
            
            if estimated_tokens > max_input_tokens:
                self.logger.warning(f"Input quá dài: {estimated_tokens} tokens, đang cắt ngắn...")
                
                # Cắt ngắn user_prompt nếu cần
                max_user_chars = max_input_tokens * 3 - len(system_prompt)
                if len(user_prompt) > max_user_chars:
                    user_prompt = user_prompt[:max_user_chars] + "\n[...nội dung đã được cắt ngắn để phù hợp với AI...]"
            
            if self.client_type == "openai":
                response = openai.ChatCompletion.create(
                    model=self.model,
                    messages=[
                        {"role": "system", "content": system_prompt},
                        {"role": "user", "content": user_prompt}
                    ],
                    max_tokens=max_tokens,
                    temperature=temperature
                )
                return response.choices[0].message.content.strip()
            
            elif self.client_type == "anthropic":
                response = self.client.messages.create(
                    model=self.model,
                    max_tokens=max_tokens,
                    temperature=temperature,
                    system=system_prompt,
                    messages=[
                        {"role": "user", "content": user_prompt}
                    ]
                )
                return response.content[0].text.strip()
                
        except Exception as e:
            error_msg = str(e).lower()
            
            # Xử lý đặc biệt cho lỗi token limit
            if 'context_length_exceeded' in error_msg or 'maximum context length' in error_msg:
                self.logger.error(f"Token limit exceeded, trying with shorter content...")
                
                # Thử lại với nội dung ngắn hơn
                if len(user_prompt) > 2000:
                    shortened_prompt = user_prompt[:2000] + "\n[...nội dung đã được rút gọn do giới hạn AI...]"
                    return self.generate_text(system_prompt, shortened_prompt, max_tokens, temperature)
                else:
                    self.logger.error("Không thể rút gọn thêm, bỏ qua request này")
                    return None
            else:
                self.logger.error(f"Lỗi AI generation: {e}")
                return None

class DocumentTool:
    """Tool để tạo và xử lý documents"""
    
    @staticmethod
    def create_word_document(title: str, content: str, metadata: Dict[str, Any]) -> bytes:
        """Tạo file Word từ nội dung"""
        doc = Document()
        
        # Tiêu đề chính
        main_title = doc.add_heading(title, 0)
        main_title.alignment = 1  # Center alignment
        
        # Metadata
        if metadata:
            doc.add_heading('Thông tin', level=1)
            for key, value in metadata.items():
                doc.add_paragraph(f'{key}: {value}')
        
        # Nội dung chính
        doc.add_heading('Nội dung', level=1)
        
        # Chia nội dung thành các đoạn
        paragraphs = content.split('\n\n')
        for paragraph in paragraphs:
            if paragraph.strip():
                doc.add_paragraph(paragraph.strip())
        
        # Thống kê
        word_count = len(content.split())
        estimated_time = word_count / 150
        
        doc.add_heading('Thống kê', level=2)
        stats = doc.add_paragraph()
        stats.add_run(f'Số từ: {word_count}\n')
        stats.add_run(f'Số ký tự: {len(content)}\n')
        stats.add_run(f'Thời lượng ước tính: {estimated_time:.1f} phút\n')
        stats.add_run(f'Thời gian tạo: {datetime.now().strftime("%d/%m/%Y %H:%M:%S")}')
        
        # Lưu vào buffer
        buffer = io.BytesIO()
        doc.save(buffer)
        buffer.seek(0)
        
        return buffer.getvalue()
    
    @staticmethod
    def calculate_reading_time(text: str, words_per_minute: int = 150) -> float:
        """Tính thời gian đọc ước tính"""
        words = len(text.split())
        return words / words_per_minute
    
    @staticmethod
    def get_text_stats(text: str) -> Dict[str, Any]:
        """Lấy thống kê văn bản"""
        return {
            'word_count': len(text.split()),
            'char_count': len(text),
            'paragraph_count': len([p for p in text.split('\n\n') if p.strip()]),
            'estimated_time': DocumentTool.calculate_reading_time(text)
        }

class ContentCleanerTool:
    """Tool để làm sạch nội dung"""
    
    @staticmethod
    def clean_text(text: str) -> str:
        """Làm sạch text"""
        if not text:
            return ""
        
        # Loại bỏ các ký tự không mong muốn
        import re
        
        # Loại bỏ multiple spaces
        text = re.sub(r'\s+', ' ', text)
        
        # Loại bỏ các thông tin liên hệ phổ biến
        contact_patterns = [
            r'Tel:\s*\([^)]+\)[^.]*',
            r'Fax:\s*\([^)]+\)[^.]*',
            r'E-mail:\s*[^\s]+@[^\s]+',
            r'Trụ sở[^.]*\.',
            r'Địa chỉ[^.]*\.',
            r'Liên hệ[^.]*\.',
            r'Hotline[^.]*\.',
            r'Website[^.]*\.',
        ]
        
        for pattern in contact_patterns:
            text = re.sub(pattern, '', text, flags=re.IGNORECASE)
        
        # Loại bỏ các dòng quảng cáo
        ad_keywords = [
            'quảng cáo', 'advertisement', 'sponsored', 'pr article',
            'bài pr', 'tài trợ', 'đăng ký nhận tin'
        ]
        
        lines = text.split('\n')
        cleaned_lines = []
        
        for line in lines:
            line = line.strip()
            if line and not any(keyword in line.lower() for keyword in ad_keywords):
                cleaned_lines.append(line)
        
        # Join lại và làm sạch cuối cùng
        cleaned_text = ' '.join(cleaned_lines)
        cleaned_text = re.sub(r'\s+', ' ', cleaned_text).strip()
        
        return cleaned_text
    
    @staticmethod
    def extract_main_content(soup: BeautifulSoup, content_selectors: list) -> str:
        """Trích xuất nội dung chính từ soup"""
        content_parts = []
        
        for selector in content_selectors:
            elements = soup.select(selector)
            for element in elements:
                text = element.get_text(strip=True)
                if text and len(text) > 20:  # Chỉ lấy text có ý nghĩa
                    content_parts.append(text)
        
        if content_parts:
            raw_content = ' '.join(content_parts)
            return ContentCleanerTool.clean_text(raw_content)
        
        return ""
    
    @staticmethod
    def truncate_content(content: str, max_length: int = 5000) -> str:
        """Cắt ngắn nội dung để phù hợp với AI"""
        if len(content) <= max_length:
            return content
        
        # Cắt tại câu gần nhất với max_length
        truncated = content[:max_length]
        last_sentence = truncated.rfind('.')
        
        if last_sentence > max_length * 0.8:  # Nếu tìm thấy câu gần cuối
            truncated = truncated[:last_sentence + 1]
        
        return truncated + "\n[...nội dung đã được rút gọn...]"