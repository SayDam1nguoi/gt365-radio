"""
Model cho bài báo tin tức
"""
from dataclasses import dataclass
from typing import Optional
from datetime import datetime
import json

@dataclass
class NewsArticle:
    """Class đại diện cho một bài báo tin tức"""
    
    url: str
    title: str
    content: str
    source: str
    summary: Optional[str] = None
    publish_time: Optional[str] = None
    author: Optional[str] = None
    category: Optional[str] = None
    tags: Optional[list] = None
    
    def __post_init__(self):
        """Xử lý sau khi khởi tạo"""
        if self.tags is None:
            self.tags = []
    
    def is_valid(self) -> bool:
        """Kiểm tra bài báo có hợp lệ không"""
        return bool(self.title and self.content and len(self.content.strip()) > 50)
    
    def get_word_count(self) -> int:
        """Đếm số từ trong bài báo"""
        return len(self.content.split())
    
    def get_summary(self, max_words: int = 50) -> str:
        """Lấy tóm tắt bài báo"""
        words = self.content.split()
        if len(words) <= max_words:
            return self.content
        return ' '.join(words[:max_words]) + '...'
    
    def to_dict(self) -> dict:
        """Chuyển đổi thành dictionary"""
        return {
            'url': self.url,
            'title': self.title,
            'content': self.content,
            'source': self.source,
            'summary': self.summary,
            'publish_time': self.publish_time,
            'author': self.author,
            'category': self.category,
            'tags': self.tags,
            'word_count': self.get_word_count()
        }
    
    def to_json(self) -> str:
        """Chuyển đổi thành JSON string"""
        return json.dumps(self.to_dict(), ensure_ascii=False, indent=2)
    
    @classmethod
    def from_dict(cls, data: dict) -> 'NewsArticle':
        """Tạo NewsArticle từ dictionary"""
        return cls(
            url=data['url'],
            title=data['title'],
            content=data['content'],
            source=data['source'],
            summary=data.get('summary'),
            publish_time=data.get('publish_time'),
            author=data.get('author'),
            category=data.get('category'),
            tags=data.get('tags', [])
        )
    
    @classmethod
    def from_json(cls, json_str: str) -> 'NewsArticle':
        """Tạo NewsArticle từ JSON string"""
        data = json.loads(json_str)
        return cls.from_dict(data)
    
    def __str__(self) -> str:
        """String representation"""
        return f"NewsArticle(title='{self.title[:50]}...', source='{self.source}', words={self.get_word_count()})"
    
    def __repr__(self) -> str:
        """Representation"""
        return self.__str__()