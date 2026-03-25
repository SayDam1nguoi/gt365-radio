"""
Cấu hình cho News Script Generator
"""

# Danh sách các trang báo và URL
NEWS_SOURCES = {
    'nhandan': {
        'base_url': 'https://nhandan.vn',
        'categories': [
            'https://nhandan.vn/chinhtri/',
            'https://nhandan.vn/phapluat/',
            'https://nhandan.vn/kinhte/',
            'https://nhandan.vn/giaoduc/',
            'https://nhandan.vn/y-te/',
            'https://nhandan.vn/khoahoc-congnghe/'
        ],
        'selectors': {
            'article_links': 'h2 a[href*=".html"]',
            'title': 'h1',
            'content': 'p.t1, p',
            'time': '.detail-time, .time-update, .publish-time, time',
            'summary': '.detail-sapo, .sapo, .article-summary'
        }
    },
    'vtv': {
        'base_url': 'https://vtv.vn',
        'categories': [
            'https://vtv.vn/chinh-tri.htm',
            'https://vtv.vn/xa-hoi.htm',
            'https://vtv.vn/phap-luat.htm',
            'https://vtv.vn/kinh-te.htm',
            'https://vtv.vn/y-te.htm',
            'https://vtv.vn/giao-duc.htm'
        ],
        'selectors': {
            'article_links': 'h3 a[href*=".htm"], h2 a[href*=".htm"]',
            'title': 'h1.title, h1.article-title, .article-title h1',
            'content': '.article-content, .content, .article-body',
            'time': '.time, .article-time, .publish-date',
            'summary': '.sapo, .article-sapo, .article-summary'
        }
    },
    'qdnd': {
        'base_url': 'https://www.qdnd.vn',
        'categories': [
            'https://www.qdnd.vn/chinh-tri',
            'https://www.qdnd.vn/kinh-te',
            'https://www.qdnd.vn/xa-hoi',
            'https://www.qdnd.vn/van-hoa',
            'https://www.qdnd.vn/giao-duc-khoa-hoc',
            'https://www.qdnd.vn/phap-luat'
        ],
        'selectors': {
            'article_links': 'h3 a[href*="/tin-tuc/"], a[href*="/tin-tuc/"]',
            'title': 'h1.title-detail, h1.article-title, .article-title h1',
            'content': '.detail-content, .article-body, .content-detail',
            'time': '.time-post, .publish-time, .article-time',
            'summary': '.sapo-detail, .article-summary, .article-sapo'
        }
    }
}

# Cấu hình crawling
CRAWL_CONFIG = {
    'delay_between_requests': 0.5,  # giây - giảm delay cho demo
    'max_articles_per_category': 2,  # Chỉ lấy 2 bài mỗi danh mục cho demo
    'timeout': 30,
    'max_retries': 2,  # Giảm retry cho demo nhanh hơn
    'user_agents': [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    ]
}

# Cấu hình xử lý nội dung
CONTENT_CONFIG = {
    'min_content_length': 100,
    'max_content_length': 5000,
    'remove_tags': ['script', 'style', 'nav', 'footer', 'header', 'aside'],
    'clean_patterns': [
        r'\s+',  # multiple spaces
        r'\n+',  # multiple newlines
        r'[^\w\s\.,!?;:\-\(\)]'  # special characters
    ]
}