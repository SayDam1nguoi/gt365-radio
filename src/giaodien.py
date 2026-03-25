"""
Giao diện người dùng cho GT365 Radio News Script Generator.
"""
from datetime import datetime

import streamlit as st


def setup_page_config():
    """Cấu hình trang."""
    st.set_page_config(
        page_title="GT365 Radio - News Script Generator",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def load_custom_css():
    """Nạp CSS cho giao diện."""
    st.markdown(
        """
        <style>
            @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

            html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
                background: #ffffff !important;
                color: #0f172a !important;
            }

            [data-testid="stHeader"] {
                background: #ffffff !important;
            }

            [data-testid="stToolbar"] {
                right: 1rem;
            }

            [data-testid="stMainBlockContainer"] {
                background: #ffffff !important;
            }

            .main {
                font-family: 'Inter', sans-serif;
                padding: 1rem;
                background: #ffffff;
            }

            .main-header {
                background: linear-gradient(135deg, #0f766e 0%, #1d4ed8 100%);
                padding: 2rem;
                border-radius: 15px;
                text-align: center;
                color: white;
                margin-bottom: 2rem;
                box-shadow: 0 10px 30px rgba(15, 23, 42, 0.12);
            }

            .main-header h1 {
                font-size: 2.5rem;
                font-weight: 700;
                margin: 0;
            }

            .main-header p {
                margin: 0.75rem 0 0;
                font-size: 1rem;
                opacity: 0.9;
            }

            .card {
                background: #ffffff;
                padding: 1.5rem;
                border-radius: 12px;
                box-shadow: 0 2px 8px rgba(15, 23, 42, 0.06);
                border: 1px solid #e2e8f0;
                margin-bottom: 1.5rem;
            }

            .card-header {
                display: flex;
                align-items: center;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #e2e8f0;
            }

            .card-icon {
                font-size: 1.5rem;
                margin-right: 0.5rem;
            }

            .card-title {
                font-size: 1.2rem;
                font-weight: 600;
                color: #0f172a;
                margin: 0;
            }

            .status-box {
                padding: 1rem;
                border-radius: 10px;
                margin: 1rem 0;
                border-left: 4px solid;
                font-weight: 500;
                background-color: #f8fafc;
                border: 1px solid #e2e8f0;
            }

            .success-box {
                background-color: #f0fdf4;
                border-left-color: #16a34a;
                color: #166534;
                border-color: #bbf7d0;
            }

            .error-box {
                background-color: #fef2f2;
                border-left-color: #dc2626;
                color: #b91c1c;
                border-color: #fecaca;
            }

            .info-box {
                background-color: #eff6ff;
                border-left-color: #2563eb;
                color: #1d4ed8;
                border-color: #bfdbfe;
            }

            .warning-box {
                background-color: #fffbeb;
                border-left-color: #d97706;
                color: #b45309;
                border-color: #fed7aa;
            }

            .stButton > button {
                background: linear-gradient(135deg, #0f766e 0%, #1d4ed8 100%);
                color: #ffffff !important;
                border: none;
                border-radius: 10px;
                padding: 0.75rem 1.25rem;
                font-weight: 600;
                transition: all 0.2s ease;
                box-shadow: 0 4px 15px rgba(29, 78, 216, 0.2);
                width: 100%;
            }

            .stButton > button * {
                color: #ffffff !important;
                fill: #ffffff !important;
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 8px 24px rgba(29, 78, 216, 0.22);
            }

            .stTextInput input,
            .stTextArea textarea,
            .stSelectbox select,
            .stNumberInput input {
                border-radius: 8px;
                background: #ffffff !important;
                color: #0f172a !important;
                border: 1px solid #cbd5e1 !important;
            }

            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {
                color: #64748b !important;
            }

            .metric-card {
                background: #f8fafc;
                padding: 1rem;
                border-radius: 10px;
                text-align: center;
                border: 1px solid #cbd5e1;
            }

            .progress-container {
                background: #f8fafc;
                border-radius: 10px;
                padding: 1rem;
                margin: 1rem 0;
                border: 1px solid #cbd5e1;
            }

            .script-container {
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 12px;
                padding: 1.25rem;
                margin: 1rem 0;
            }

            .script-header {
                display: flex;
                justify-content: space-between;
                align-items: center;
                margin-bottom: 1rem;
                padding-bottom: 0.5rem;
                border-bottom: 2px solid #e2e8f0;
            }

            @keyframes fadeIn {
                from { opacity: 0; transform: translateY(16px); }
                to { opacity: 1; transform: translateY(0); }
            }

            .fade-in {
                animation: fadeIn 0.4s ease-out;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 8px;
                border-bottom: 1px solid #e2e8f0;
            }

            .stTabs [data-baseweb="tab"] {
                height: 50px;
                padding-left: 20px;
                padding-right: 20px;
                color: #475569 !important;
                background: transparent !important;
            }

            .stTabs [aria-selected="true"] {
                color: #1d4ed8 !important;
            }

            .stMarkdown,
            .stTextInput label,
            .stTextArea label,
            .stNumberInput label,
            .stSelectbox label,
            p,
            span,
            label {
                color: #0f172a !important;
            }

            @media (max-width: 768px) {
                .main-header h1 {
                    font-size: 2rem;
                }

                .card {
                    padding: 1rem;
                }

                .main {
                    padding: 0.5rem;
                }
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def render_header():
    """Render phần header."""
    st.markdown(
        """
        <div class="main-header fade-in">
            <h1>🎙️ GT365 Radio - News Script Generator</h1>
            <p>Tạo kịch bản từ bài báo nhanh hơn, sạch hơn và dễ biên tập hơn.</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_section():
    """Render phần nhập URL."""
    st.markdown(
        """
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">🔗</span>
                <h3 class="card-title">Nguồn tin tức</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown(
        """
        <div class="info-box">
            <strong>🌐 Hỗ trợ đa nguồn:</strong> VnExpress, Tuổi Trẻ, Thanh Niên, Dân Trí, VTV,
            QĐND, Nhân Dân và nhiều trang báo khác.
        </div>
        """,
        unsafe_allow_html=True,
    )

    if "num_url_inputs" not in st.session_state:
        st.session_state.num_url_inputs = 3

    news_urls = []
    valid_urls = 0

    for i in range(st.session_state.num_url_inputs):
        url = st.text_input(
            f"🔗 Link bài báo {i + 1}",
            placeholder="https://vnexpress.net/... hoặc bất kỳ link bài báo hợp lệ nào",
            key=f"url_input_{i}",
            help="Dán link từ trang báo bạn muốn tổng hợp.",
        )

        if url.strip():
            if url.startswith(("http://", "https://")):
                news_urls.append(url.strip())
                valid_urls += 1
                st.markdown(
                    f'<small style="color: #16a34a;">✅ URL {i + 1} hợp lệ</small>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<small style="color: #dc2626;">❌ URL {i + 1} không hợp lệ, cần bắt đầu bằng http/https</small>',
                    unsafe_allow_html=True,
                )

    col_add, col_remove, col_clear = st.columns(3)

    with col_add:
        if st.button("➕ Thêm link", use_container_width=True):
            if st.session_state.num_url_inputs < 10:
                st.session_state.num_url_inputs += 1
                st.rerun()

    with col_remove:
        if st.button("➖ Bớt link", use_container_width=True):
            if st.session_state.num_url_inputs > 1:
                st.session_state.num_url_inputs -= 1
                st.rerun()

    with col_clear:
        if st.button("🗑️ Xóa tất cả", use_container_width=True):
            for i in range(st.session_state.num_url_inputs):
                st.session_state[f"url_input_{i}"] = ""
            st.rerun()

    if valid_urls > 0:
        st.markdown(
            f"""
            <div class="success-box">
                <strong>📊 Trạng thái:</strong> Đã nhập {valid_urls} URL hợp lệ, sẵn sàng xử lý.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="info-box">
                <strong>💡 Hướng dẫn:</strong> Nhập ít nhất một URL hợp lệ để bắt đầu.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return news_urls


def render_prompt_section():
    """Render phần nhập prompt."""
    st.markdown(
        """
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">💬</span>
                <h3 class="card-title">Prompt tùy chỉnh</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    user_prompt = st.text_area(
        "💬 Mô tả chi tiết yêu cầu của bạn",
        placeholder=(
            "Ví dụ:\n"
            "• Tạo kịch bản YouTube 8 phút về công nghệ, giọng điệu chuyên nghiệp nhưng dễ hiểu\n"
            "• Viết script podcast 15 phút, có intro hấp dẫn, phần chính phân tích sâu và outro có call-to-action\n"
            "• Tạo nội dung TikTok 90 giây, năng động, phù hợp Gen Z\n"
            "• Viết bài thuyết trình 10 phút cho doanh nghiệp, trang trọng và có số liệu cụ thể"
        ),
        height=140,
        help="Prompt càng rõ thì kết quả càng sát yêu cầu.",
    )

    return user_prompt


def render_config_section():
    """Render phần cấu hình."""
    st.markdown(
        """
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">⚙️</span>
                <h3 class="card-title">Cấu hình kịch bản</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_config1, col_config2, col_config3 = st.columns(3)

    with col_config1:
        script_length = st.selectbox(
            "⏱️ Độ dài",
            options=[
                "Ngắn (1-2 phút)",
                "Trung bình (3-5 phút)",
                "Dài (5-10 phút)",
                "Rất dài (10-15 phút)",
                "Tùy chỉnh",
            ],
            help="Chọn độ dài phù hợp với định dạng nội dung.",
        )

    with col_config2:
        if script_length == "Tùy chỉnh":
            custom_length = st.number_input("Số phút", min_value=1, max_value=30, value=5)
        else:
            custom_length = None

    with col_config3:
        num_scripts = st.number_input(
            "📄 Số lượng phiên bản",
            min_value=1,
            max_value=3,
            value=1,
            help="Tạo nhiều phiên bản nếu bạn muốn so sánh phong cách.",
        )

    return script_length, custom_length, num_scripts


def render_progress_bar(progress_value, status_text):
    """Render thanh tiến trình."""
    st.markdown(
        """
        <div class="progress-container">
            <h4>🤖 News Agent đang xử lý...</h4>
        </div>
        """,
        unsafe_allow_html=True,
    )

    progress_bar = st.progress(progress_value)
    status_display = st.empty()
    status_display.text(status_text)
    return progress_bar, status_display


def render_results_tab():
    """Hiển thị tab kết quả."""
    if "scripts" not in st.session_state or not st.session_state.scripts:
        st.markdown(
            """
            <div class="card">
                <div style="text-align: center; padding: 2rem;">
                    <h3>📄 Chưa có kịch bản nào</h3>
                    <p>Hãy tạo kịch bản ở tab "Tạo kịch bản" trước.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    scripts = st.session_state.scripts
    article_info = st.session_state.article_info

    st.markdown(
        """
        <div class="card fade-in">
            <div class="card-header">
                <span class="card-icon">📰</span>
                <h3 class="card-title">Thông tin nguồn</h3>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col_info1, col_info2, col_info3, col_info4 = st.columns(4)

    with col_info1:
        title = article_info.get("title", "N/A")
        short_title = title if len(title) <= 24 else f"{title[:24]}..."
        st.metric("📰 Tiêu đề", short_title)

    with col_info2:
        st.metric("🌐 Nguồn", article_info.get("source", "N/A"))

    with col_info3:
        st.metric("📝 Số từ gốc", article_info.get("word_count", 0))

    with col_info4:
        st.metric("📄 Kịch bản tạo", len(scripts))

    for i, script in enumerate(scripts, 1):
        st.markdown(
            f"""
            <div class="script-container fade-in">
                <div class="script-header">
                    <h3>📝 Kịch bản {i}</h3>
                    <span style="color: #64748b;">Phiên bản {i}</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            f"Nội dung kịch bản {i}",
            value=script,
            height=400,
            key=f"script_display_{i}",
            help="Có thể sao chép nội dung trực tiếp từ đây.",
        )

        word_count = len(script.split())
        char_count = len(script)
        estimated_time = word_count / 160

        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

        with col_stat1:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>📝 Số từ</h4>
                    <h2>{word_count:,}</h2>
                    <p>từ</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_stat2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>🔤 Ký tự</h4>
                    <h2>{char_count:,}</h2>
                    <p>ký tự</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_stat3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>⏱️ Thời lượng</h4>
                    <h2>{estimated_time:.1f}</h2>
                    <p>phút</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_stat4:
            if "agent" in st.session_state:
                try:
                    doc_buffer = st.session_state.agent.create_document(script, i)
                    st.download_button(
                        label="💾 Tải xuống",
                        data=doc_buffer,
                        file_name=f"GT365_Script_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_pro_{i}",
                        use_container_width=True,
                    )
                except Exception as exc:
                    st.error(f"Lỗi tạo file: {exc}")

        if i < len(scripts):
            st.markdown("---")


def render_footer():
    """Render footer."""
    st.markdown("---")
    st.markdown(
        """
        <div style="text-align: center; padding: 1.5rem; color: #64748b; background: #f8fafc; border-radius: 10px; margin-top: 2rem; border: 1px solid #e2e8f0;">
            <p><strong>🎙️ GT365 Radio - News Script Generator</strong></p>
            <p style="font-size: 0.9rem;">📧 support@gt365radio.com • 📱 1900-xxxx • 🌐 gt365radio.com</p>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_success_message(num_scripts, num_articles):
    """Hiển thị thông báo thành công."""
    st.markdown(
        f"""
        <div class="success-box fade-in">
            <strong>🎉 Thành công!</strong> Đã tạo {num_scripts} kịch bản từ {num_articles} bài báo.
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_error_message(error_msg):
    """Hiển thị thông báo lỗi."""
    st.markdown(f'<div class="error-box">❌ Lỗi: {error_msg}</div>', unsafe_allow_html=True)


def show_warning_message(warning_msg):
    """Hiển thị thông báo cảnh báo."""
    st.markdown(f'<div class="warning-box">⚠️ {warning_msg}</div>', unsafe_allow_html=True)
