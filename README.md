# 📰 News Script Generator - Universal News Agent

Hệ thống News Agent thông minh có thể crawl từ **bất kỳ trang báo nào** và tạo kịch bản theo **prompt tùy chỉnh** của người dùng.

## 🌟 Tính năng nổi bật

### 🌐 **Universal News Crawler**
- **Không giới hạn nguồn**: Crawl từ mọi trang báo Việt Nam
- **Tự động nhận diện**: Tự động detect và xử lý các trang khác nhau
- **Chiến lược đa dạng**: Sử dụng nhiều phương pháp trích xuất nội dung
- **Hỗ trợ rộng rãi**: VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí, VietnamNet, Báo Mới, VTV, QĐND, Nhân Dân, và nhiều nguồn khác

### 💭 **Prompt-Driven Generation**
- **Tính năng chính**: Agent thực hiện chính xác theo prompt người dùng
- **Linh hoạt tuyệt đối**: Tạo mọi loại kịch bản theo yêu cầu
- **Sáng tạo không giới hạn**: YouTube, TikTok, Podcast, Radio, Thuyết trình
- **Thích ứng thông minh**: Tự động điều chỉnh phong cách và định dạng

## 🎯 Ví dụ Prompt sáng tạo

### 📱 **Social Media Scripts**
```
Tạo kịch bản TikTok 60 giây về tin tức này:
- Giọng điệu Gen Z, có emoji 
- Hook đầu hấp dẫn trong 3 giây đầu
- 3 điểm chính ngắn gọn
- Kết thúc với call-to-action "Follow để cập nhật tin tức!"
```

### 🎙️ **Podcast Scripts**
```
Viết script podcast 15 phút phong cách Joe Rogan:
- Mở đầu casual, thân thiện
- Đi sâu vào phân tích, có góc nhìn cá nhân
- Đặt câu hỏi mở để khán giả suy nghĩ
- Kết nối với trải nghiệm đời thường
```

### 📺 **YouTube Scripts**
```
Tạo kịch bản YouTube 8 phút kiểu "explained":
- Intro hook trong 15 giây đầu
- Chia thành 3 phần rõ ràng với timestamp
- Có graphics cues và B-roll suggestions
- Kết thúc với teaser video tiếp theo
```

### 🎤 **Presentation Scripts**
```
Viết bài thuyết trình 10 phút cho hội nghị khoa học:
- Cấu trúc academic với introduction, body, conclusion
- Có slide cues và data visualization notes
- Ngôn ngữ formal, chuyên nghiệp
- Q&A preparation ở cuối
```

## ✨ Tính năng chính

### 🔗 Crawl tin tức
- Hỗ trợ các trang báo: **Nhân Dân**, **VTV**, **QĐND**
- Tự động trích xuất tiêu đề và nội dung
- Làm sạch dữ liệu, loại bỏ quảng cáo

### 🤖 Tạo kịch bản AI
- Hỗ trợ nhiều model: **GPT-3.5**, **GPT-4**, **Claude-3**
- Tùy chỉnh độ dài: 1-30 phút
- Tạo tối đa 3 kịch bản với phong cách khác nhau
- Prompt tùy chỉnh theo ý muốn

### 💾 Xuất file
- **Word (.docx)**: Định dạng chuyên nghiệp
- **JSON**: Dữ liệu có cấu trúc
- Thống kê chi tiết: số từ, thời lượng ước tính

## 🚀 Cài đặt và chạy

```bash
# Cài đặt dependencies
pip install -r requirements_app.txt

# Chạy ứng dụng
streamlit run app.py
```

Ứng dụng sẽ mở tại: `http://localhost:8501`

## 🔧 Cấu hình

### API Keys
Tạo file `.env` trong thư mục gốc với nội dung:

```
OPENAI_API_KEY=your_openai_key_here
```

Bạn cần API key từ một trong các nhà cung cấp:

- **OpenAI**: https://platform.openai.com/api-keys
- **Anthropic**: https://console.anthropic.com/

### Cấu trúc dự án
```
news-script-generator/
├── app.py                 # Ứng dụng Streamlit chính
├── requirements_app.txt   # Dependencies
├── .env                  # API keys (tự tạo)
├── src/
│   ├── news_agent/       # 🤖 News Agent System
│   │   ├── agent.py      #   - News Agent chính
│   │   ├── backend.py    #   - Backend xử lý
│   │   ├── tools.py      #   - Tools cơ bản
│   │   └── __init__.py   #   - Package init
│   ├── crawlers/         # Legacy crawlers
│   │   └── base_crawler.py
│   ├── models/           # Data models
│   │   └── news_article.py
│   └── script_generator.py # Legacy generator
├── config/
│   └── settings.py       # Cấu hình crawler
└── README.md
```

## 📖 Hướng dẫn sử dụng

### Bước 1: Nhập thông tin
1. **Link bài báo**: Dán URL từ VTV, QĐND, hoặc Nhân Dân
2. **Prompt tùy chỉnh**: Mô tả cách bạn muốn kịch bản được tạo
3. **Độ dài**: Chọn từ 1-30 phút
4. **Số lượng**: Tối đa 3 kịch bản

### Bước 2: Cấu hình AI
1. Chọn model AI (GPT-3.5, GPT-4, Claude-3)
2. Nhập API key
3. Chọn nguồn báo

### Bước 3: Tạo kịch bản
1. Nhấn "🚀 Tạo kịch bản"
2. Chờ AI xử lý (30-60 giây)
3. Xem kết quả và thống kê

### Bước 4: Tải xuống
1. **Word**: File .docx định dạng đẹp
2. **JSON**: Dữ liệu có cấu trúc

## 🎯 Logic xử lý mới - Tổng hợp thông minh

### Quy trình xử lý nhiều URL
```python
from src.news_agent import NewsScriptAgent

# Khởi tạo News Agent
agent = NewsScriptAgent("gpt-3.5-turbo", "your-api-key")

# Xử lý nhiều URL - LOGIC MỚI
urls = [
    "https://nhandan.vn/...",
    "https://vtv.vn/...",
    "https://qdnd.vn/..."
]

# Tổng hợp nội dung từ 3 bài báo → Tạo 2 kịch bản tổng hợp
success, results = agent.process_multiple_news_to_script(
    urls=urls,
    prompt="Tạo kịch bản radio tổng hợp",
    length="5 phút",
    num_scripts=2  # CHỈ 2 kịch bản tổng hợp, KHÔNG phải 3*2=6
)

if success:
    # Kết quả: 2 kịch bản chứa thông tin tổng hợp từ 3 bài báo
    scripts = results['scripts']  # 2 scripts, not 6
    combined_info = results['metadata']['combined_info']
```

### So sánh Logic Cũ vs Mới

#### ❌ Logic Cũ (SAI):
```
Input: 3 URLs + 2 scripts per article
Process: URL1 → 2 scripts, URL2 → 2 scripts, URL3 → 2 scripts  
Output: 6 scripts riêng lẻ
Problem: Thông tin bị lặp lại, không tổng hợp
```

#### ✅ Logic Mới (ĐÚNG):
```
Input: 3 URLs + 2 scripts total
Process: 
  Step 1: Extract all 3 articles
  Step 2: Combine content intelligently  
  Step 3: Generate 2 comprehensive scripts
Output: 2 scripts tổng hợp từ 3 nguồn
Benefit: Thông tin mạch lạc, không lặp lại
```

### Input → News Agent → Output
```
📥 INPUT:
- URLs: [url1, url2, url3] (3 bài báo khác nhau)
- Prompt: "Tạo kịch bản radio tổng hợp"
- Length: "5 phút"  
- Scripts: 2 (TỔNG CỘNG, không phải mỗi bài)

🤖 NEWS AGENT PROCESSING:
Step 1: Extract Articles ✅ (3 articles)
Step 2: Combine Content ✅ (1 combined content)
Step 3: Generate Scripts ✅ (2 comprehensive scripts)
Step 4: Prepare Outputs ✅

📤 OUTPUT:
- Scripts: 2 tổng hợp (chứa thông tin từ cả 3 bài)
- Metadata: Thông tin chi tiết về 3 bài gốc
- Documents: 2 file Word tổng hợp
```

### Ưu điểm Logic Mới
- **Tổng hợp thông minh**: Kết hợp thông tin từ nhiều nguồn
- **Không lặp lại**: Loại bỏ thông tin trùng lặp
- **Mạch lạc**: Kịch bản liền mạch, dễ đọc
- **Hiệu quả**: Ít kịch bản hơn nhưng chất lượng cao hơn
- **Tiết kiệm**: Ít API calls, nhanh hơn

## 🔍 Tính năng nâng cao

### Phong cách kịch bản
- **Trang trọng**: Phù hợp tin chính trị, kinh tế
- **Thân thiện**: Phù hợp tin xã hội, văn hóa
- **Năng động**: Phù hợp tin thể thao, giải trí

### Thống kê chi tiết
- Số từ, ký tự
- Thời lượng ước tính (150 từ/phút)
- Số đoạn văn

### Xuất file Word
- Header với thông tin bài báo gốc
- Định dạng chuyên nghiệp
- Thống kê cho từng kịch bản

## ⚠️ Lưu ý

1. **API Key**: Cần có API key hợp lệ
2. **Mạng**: Cần kết nối internet để crawl và gọi AI
3. **Chất lượng**: Kết quả phụ thuộc vào chất lượng bài báo gốc
4. **Chi phí**: Sử dụng API có tính phí theo usage

## 🐛 Troubleshooting

### Lỗi thường gặp
- **"Không thể crawl"**: Kiểm tra link và kết nối mạng
- **"API Error"**: Kiểm tra API key và quota
- **"Không tạo được kịch bản"**: Thử model khác hoặc rút ngắn prompt

### Liên hệ hỗ trợ
- Tạo issue trên GitHub
- Email: support@example.com

## 📄 License

MIT License - Xem file LICENSE để biết chi tiết.

---

**Phát triển bởi**: News Script Generator Team  
**Phiên bản**: 1.0.0  
**Cập nhật**: 24/03/2026