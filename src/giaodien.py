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
            @import url('https://fonts.googleapis.com/css2?family=Be+Vietnam+Pro:wght@400;500;600;700;800&display=swap');

            :root {
                --bg: #f5f7fb;
                --surface: #ffffff;
                --surface-soft: #f8fafc;
                --line: #dbe4f0;
                --text: #0f172a;
                --muted: #5b6b84;
                --brand-1: #0f766e;
                --brand-2: #2563eb;
                --brand-3: #0ea5e9;
                --success-bg: #effaf3;
                --success-border: #a7e0b8;
                --success-text: #166534;
                --warning-bg: #fff8e8;
                --warning-border: #f7d18a;
                --warning-text: #b45309;
                --error-bg: #fff1f2;
                --error-border: #f7b2bb;
                --error-text: #be123c;
                --info-bg: #eef5ff;
                --info-border: #b7d3ff;
                --info-text: #1d4ed8;
                --shadow: 0 18px 50px rgba(15, 23, 42, 0.08);
            }

            html, body, .stApp, [data-testid="stAppViewContainer"], [data-testid="stMain"] {
                background:
                    radial-gradient(circle at top left, rgba(14, 165, 233, 0.10), transparent 32%),
                    radial-gradient(circle at top right, rgba(37, 99, 235, 0.12), transparent 28%),
                    var(--bg) !important;
                color: var(--text) !important;
                font-family: 'Be Vietnam Pro', sans-serif !important;
            }

            [data-testid="stHeader"] {
                background: rgba(245, 247, 251, 0.85) !important;
                backdrop-filter: blur(10px);
            }

            [data-testid="stToolbar"] {
                right: 1rem;
            }

            [data-testid="stMainBlockContainer"] {
                max-width: 1180px;
                padding-top: 2rem;
                padding-bottom: 3rem;
            }

            .main {
                font-family: 'Be Vietnam Pro', sans-serif;
            }

            .hero-shell {
                position: relative;
                overflow: hidden;
                padding: 2.2rem 2.4rem;
                border-radius: 28px;
                background:
                    linear-gradient(135deg, rgba(15, 118, 110, 0.98) 0%, rgba(37, 99, 235, 0.98) 100%);
                color: #ffffff;
                box-shadow: var(--shadow);
                margin-bottom: 1.5rem;
            }

            .hero-shell::before {
                content: "";
                position: absolute;
                inset: auto -60px -80px auto;
                width: 260px;
                height: 260px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.08);
            }

            .hero-shell::after {
                content: "";
                position: absolute;
                inset: -70px auto auto -70px;
                width: 200px;
                height: 200px;
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.10);
            }

            .hero-eyebrow {
                position: relative;
                z-index: 1;
                display: inline-flex;
                align-items: center;
                gap: 0.45rem;
                font-size: 0.82rem;
                font-weight: 700;
                letter-spacing: 0.08em;
                text-transform: uppercase;
                padding: 0.5rem 0.85rem;
                border: 1px solid rgba(255, 255, 255, 0.22);
                border-radius: 999px;
                background: rgba(255, 255, 255, 0.08);
            }

            .hero-title {
                position: relative;
                z-index: 1;
                margin: 1rem 0 0.65rem;
                font-size: 2.35rem;
                line-height: 1.15;
                font-weight: 800;
                letter-spacing: -0.03em;
            }

            .hero-copy {
                position: relative;
                z-index: 1;
                max-width: 720px;
                margin: 0;
                font-size: 1rem;
                line-height: 1.7;
                color: rgba(255, 255, 255, 0.92);
            }

            .hero-grid {
                position: relative;
                z-index: 1;
                display: grid;
                grid-template-columns: repeat(3, minmax(0, 1fr));
                gap: 0.9rem;
                margin-top: 1.4rem;
            }

            .hero-stat {
                padding: 1rem 1.05rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.10);
                border: 1px solid rgba(255, 255, 255, 0.14);
            }

            .hero-stat span {
                display: block;
                color: rgba(255, 255, 255, 0.72) !important;
                font-size: 0.82rem;
                margin-bottom: 0.28rem;
            }

            .hero-stat strong {
                font-size: 1rem;
                color: #ffffff;
                font-weight: 700;
            }

            .section-card {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid rgba(219, 228, 240, 0.92);
                border-radius: 24px;
                padding: 1.35rem 1.35rem 1.15rem;
                box-shadow: 0 14px 36px rgba(15, 23, 42, 0.05);
                margin-bottom: 1.15rem;
                backdrop-filter: blur(8px);
            }

            .section-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                margin-bottom: 0.95rem;
            }

            .section-title-wrap {
                display: flex;
                align-items: center;
                gap: 0.8rem;
            }

            .section-icon {
                width: 42px;
                height: 42px;
                border-radius: 14px;
                display: inline-flex;
                align-items: center;
                justify-content: center;
                background: linear-gradient(135deg, rgba(15, 118, 110, 0.12), rgba(37, 99, 235, 0.12));
                font-size: 1.1rem;
            }

            .section-title {
                margin: 0;
                font-size: 1.1rem;
                font-weight: 700;
                color: var(--text);
            }

            .section-subtitle {
                margin: 0.18rem 0 0;
                color: var(--muted);
                font-size: 0.92rem;
                line-height: 1.5;
            }

            .pill-note {
                display: inline-flex;
                align-items: center;
                gap: 0.4rem;
                padding: 0.55rem 0.9rem;
                border-radius: 999px;
                background: #edf4ff;
                border: 1px solid #cfe0ff;
                color: #2458d3 !important;
                font-size: 0.84rem;
                font-weight: 600;
            }

            .status-box {
                border-radius: 18px;
                padding: 0.95rem 1rem;
                border: 1px solid;
                margin: 0.9rem 0 0.25rem;
                line-height: 1.6;
            }

            .success-box {
                background: var(--success-bg);
                border-color: var(--success-border);
                color: var(--success-text);
            }

            .warning-box {
                background: var(--warning-bg);
                border-color: var(--warning-border);
                color: var(--warning-text);
            }

            .error-box {
                background: var(--error-bg);
                border-color: var(--error-border);
                color: var(--error-text);
            }

            .info-box {
                background: var(--info-bg);
                border-color: var(--info-border);
                color: var(--info-text);
            }

            .stButton > button {
                min-height: 50px;
                border: none !important;
                border-radius: 16px !important;
                background: linear-gradient(135deg, var(--brand-1) 0%, var(--brand-2) 100%) !important;
                color: #ffffff !important;
                font-weight: 700 !important;
                box-shadow: 0 14px 28px rgba(37, 99, 235, 0.18);
                transition: transform 0.18s ease, box-shadow 0.18s ease;
            }

            .stButton > button:hover {
                transform: translateY(-1px);
                box-shadow: 0 18px 34px rgba(37, 99, 235, 0.22);
            }

            .stButton > button * {
                color: #ffffff !important;
                fill: #ffffff !important;
            }

            .stTextInput input,
            .stTextArea textarea,
            .stNumberInput input,
            .stSelectbox [data-baseweb="select"] > div {
                background: #ffffff !important;
                color: var(--text) !important;
                border: 1px solid var(--line) !important;
                border-radius: 16px !important;
                box-shadow: none !important;
            }

            .stTextInput input,
            .stNumberInput input {
                min-height: 50px;
            }

            .stTextArea textarea {
                min-height: 140px;
                line-height: 1.65;
            }

            .stTextInput input:focus,
            .stTextArea textarea:focus,
            .stNumberInput input:focus {
                border-color: #93c5fd !important;
                box-shadow: 0 0 0 4px rgba(37, 99, 235, 0.10) !important;
            }

            .stTextInput input::placeholder,
            .stTextArea textarea::placeholder {
                color: #8ca0bb !important;
            }

            .stTabs [data-baseweb="tab-list"] {
                gap: 0.65rem;
                padding: 0.35rem;
                border-radius: 18px;
                background: rgba(255, 255, 255, 0.82);
                border: 1px solid var(--line);
                margin-bottom: 1.2rem;
            }

            .stTabs [data-baseweb="tab"] {
                height: 46px;
                border-radius: 14px;
                color: var(--muted) !important;
                font-weight: 700;
                padding: 0 1rem;
                background: transparent !important;
            }

            .stTabs [aria-selected="true"] {
                background: linear-gradient(135deg, rgba(15, 118, 110, 0.10), rgba(37, 99, 235, 0.12)) !important;
                color: var(--text) !important;
            }

            .metric-card {
                background: linear-gradient(180deg, #ffffff 0%, #f8fbff 100%);
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
                text-align: center;
                min-height: 150px;
            }

            .metric-card h4 {
                margin: 0 0 0.35rem;
                color: var(--muted) !important;
                font-size: 0.88rem;
                font-weight: 700;
            }

            .metric-card h2 {
                margin: 0;
                font-size: 1.65rem;
                color: var(--text) !important;
                font-weight: 800;
            }

            .metric-card p {
                margin: 0.3rem 0 0;
                color: var(--muted) !important;
                font-size: 0.88rem;
            }

            .progress-shell {
                background: rgba(255, 255, 255, 0.94);
                border: 1px solid var(--line);
                border-radius: 22px;
                padding: 1.15rem;
                box-shadow: 0 12px 30px rgba(15, 23, 42, 0.05);
            }

            .result-card {
                background: rgba(255, 255, 255, 0.95);
                border: 1px solid var(--line);
                border-radius: 24px;
                padding: 1.2rem;
                box-shadow: 0 14px 36px rgba(15, 23, 42, 0.05);
                margin: 0.9rem 0 1rem;
            }

            .result-head {
                display: flex;
                align-items: center;
                justify-content: space-between;
                gap: 1rem;
                padding-bottom: 0.85rem;
                border-bottom: 1px solid var(--line);
                margin-bottom: 1rem;
            }

            .result-head h3 {
                margin: 0;
                font-size: 1.12rem;
                font-weight: 700;
                color: var(--text);
            }

            .result-badge {
                display: inline-flex;
                align-items: center;
                gap: 0.35rem;
                border-radius: 999px;
                padding: 0.42rem 0.8rem;
                background: #ecfdf5;
                color: #047857 !important;
                border: 1px solid #a7f3d0;
                font-size: 0.82rem;
                font-weight: 700;
            }

            .soft-grid {
                display: grid;
                grid-template-columns: repeat(4, minmax(0, 1fr));
                gap: 0.85rem;
                margin: 0.35rem 0 1rem;
            }

            .soft-stat {
                background: rgba(255, 255, 255, 0.92);
                border: 1px solid var(--line);
                border-radius: 18px;
                padding: 1rem;
            }

            .soft-stat span {
                display: block;
                color: var(--muted) !important;
                font-size: 0.82rem;
                margin-bottom: 0.28rem;
            }

            .soft-stat strong {
                color: var(--text);
                font-size: 1rem;
                font-weight: 800;
            }

            .stMarkdown,
            .stTextInput label,
            .stTextArea label,
            .stNumberInput label,
            .stSelectbox label,
            p,
            span,
            label {
                color: var(--text) !important;
            }

            @media (max-width: 900px) {
                .hero-grid,
                .soft-grid {
                    grid-template-columns: 1fr;
                }
            }

            @media (max-width: 768px) {
                [data-testid="stMainBlockContainer"] {
                    padding-top: 1.2rem;
                }

                .hero-shell {
                    padding: 1.4rem 1.2rem;
                    border-radius: 22px;
                }

                .hero-title {
                    font-size: 1.8rem;
                }

                .section-card,
                .result-card {
                    padding: 1rem;
                    border-radius: 20px;
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
        <div class="hero-shell">
            <div class="hero-eyebrow">🎙️ GT365 Radio Workspace</div>
            <h1 class="hero-title">Biến bài báo thành kịch bản phát thanh rõ ràng, nhanh và chuyên nghiệp.</h1>
            <p class="hero-copy">
                Dán link bài báo, mô tả phong cách bạn muốn và tạo ngay kịch bản để dùng cho radio,
                podcast, video tin tức hoặc bản đọc tổng hợp nội bộ.
            </p>
            <div class="hero-grid">
                <div class="hero-stat">
                    <span>Đầu vào</span>
                    <strong>Nhiều nguồn bài báo</strong>
                </div>
                <div class="hero-stat">
                    <span>Đầu ra</span>
                    <strong>Kịch bản có cấu trúc rõ ràng</strong>
                </div>
                <div class="hero-stat">
                    <span>Mục tiêu</span>
                    <strong>Tối ưu cho biên tập và đọc thu âm</strong>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def _render_section_header(icon: str, title: str, subtitle: str, note: str = ""):
    note_html = f'<div class="pill-note">{note}</div>' if note else ""
    st.markdown(
        f"""
        <div class="section-card fade-in">
            <div class="section-head">
                <div class="section-title-wrap">
                    <div class="section-icon">{icon}</div>
                    <div>
                        <h3 class="section-title">{title}</h3>
                        <p class="section-subtitle">{subtitle}</p>
                    </div>
                </div>
                {note_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_section():
    """Render phần nhập URL."""
    _render_section_header(
        "🔗",
        "Nguồn tin tức",
        "Nhập các link bài báo cần tổng hợp để tạo kịch bản.",
        "Đa nguồn",
    )

    st.markdown(
        """
        <div class="info-box">
            <strong>Gợi ý:</strong> Có thể nhập nhiều URL để gộp nội dung và tạo một kịch bản tổng hợp mạch lạc.
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
            f"Link bài báo {i + 1}",
            placeholder="Dán link bài báo hợp lệ vào đây",
            key=f"url_input_{i}",
            help="Chấp nhận URL bắt đầu bằng http:// hoặc https://",
        )

        if url.strip():
            if url.startswith(("http://", "https://")):
                news_urls.append(url.strip())
                valid_urls += 1
                st.markdown(
                    f'<small style="color:#15803d;font-weight:600;">✓ URL {i + 1} hợp lệ</small>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<small style="color:#be123c;font-weight:600;">✕ URL {i + 1} chưa hợp lệ, cần bắt đầu bằng http/https</small>',
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
        if st.button("🧹 Xóa tất cả", use_container_width=True):
            for i in range(st.session_state.num_url_inputs):
                st.session_state[f"url_input_{i}"] = ""
            st.rerun()

    if valid_urls > 0:
        st.markdown(
            f"""
            <div class="success-box">
                <strong>Sẵn sàng xử lý:</strong> Đã nhập {valid_urls} URL hợp lệ.
            </div>
            """,
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            """
            <div class="info-box">
                <strong>Bắt đầu tại đây:</strong> Nhập ít nhất một URL hợp lệ để Agent lấy nội dung bài báo.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return news_urls


def render_prompt_section():
    """Render phần nhập prompt."""
    _render_section_header(
        "💬",
        "Prompt tùy chỉnh",
        "Mô tả rõ phong cách, thời lượng và cấu trúc đầu ra bạn muốn.",
        "Creative brief",
    )

    return st.text_area(
        "Mô tả yêu cầu của bạn",
        placeholder=(
            "Ví dụ:\n"
            "• Viết kịch bản podcast 8 phút, giọng điệu chuyên nghiệp nhưng dễ nghe\n"
            "• Tạo bản tin ngắn 3 phút, mở đầu trực diện, ưu tiên số liệu quan trọng\n"
            "• Viết script YouTube có intro mạnh, nội dung phân tích sâu và kết thúc gọn\n"
            "• Tạo kịch bản trang trọng cho bản đọc nội bộ doanh nghiệp"
        ),
        height=150,
        help="Prompt càng rõ, kết quả càng sát yêu cầu.",
    )


def render_config_section():
    """Render phần cấu hình."""
    _render_section_header(
        "⚙️",
        "Cấu hình kịch bản",
        "Thiết lập độ dài và số phiên bản trước khi tạo nội dung.",
        "Output setup",
    )

    col_config1, col_config2, col_config3 = st.columns(3)

    with col_config1:
        script_length = st.selectbox(
            "Độ dài",
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
        custom_length = (
            st.number_input("Số phút", min_value=1, max_value=30, value=5)
            if script_length == "Tùy chỉnh"
            else None
        )

    with col_config3:
        num_scripts = st.number_input(
            "Số lượng phiên bản",
            min_value=1,
            max_value=3,
            value=1,
            help="Tạo nhiều phiên bản để so sánh phong cách trình bày.",
        )

    return script_length, custom_length, num_scripts


def render_progress_bar(progress_value, status_text):
    """Render thanh tiến trình."""
    st.markdown(
        """
        <div class="progress-shell">
            <strong>🤖 Agent đang xử lý yêu cầu của bạn</strong>
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
            <div class="section-card">
                <div style="text-align:center; padding:1.2rem 0.6rem;">
                    <h3 style="margin:0 0 0.45rem;">Chưa có kịch bản nào</h3>
                    <p style="margin:0; color:#5b6b84;">Tạo kịch bản ở tab đầu tiên, kết quả sẽ hiển thị tại đây.</p>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    scripts = st.session_state.scripts
    article_info = st.session_state.article_info

    _render_section_header(
        "📰",
        "Thông tin nguồn",
        "Tóm tắt nhanh dữ liệu đầu vào đã được dùng để tạo kịch bản.",
        "Overview",
    )

    title = article_info.get("title", "N/A")
    short_title = title if len(title) <= 48 else f"{title[:48]}..."

    st.markdown(
        f"""
        <div class="soft-grid">
            <div class="soft-stat">
                <span>Tiêu đề</span>
                <strong>{short_title}</strong>
            </div>
            <div class="soft-stat">
                <span>Nguồn</span>
                <strong>{article_info.get("source", "N/A")}</strong>
            </div>
            <div class="soft-stat">
                <span>Số từ gốc</span>
                <strong>{article_info.get("word_count", 0)}</strong>
            </div>
            <div class="soft-stat">
                <span>Số kịch bản</span>
                <strong>{len(scripts)}</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    for i, script in enumerate(scripts, 1):
        st.markdown(
            f"""
            <div class="result-card fade-in">
                <div class="result-head">
                    <h3>📝 Kịch bản {i}</h3>
                    <div class="result-badge">Phiên bản {i}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            f"Nội dung kịch bản {i}",
            value=script,
            height=420,
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
                    <h4>Số từ</h4>
                    <h2>{word_count:,}</h2>
                    <p>đơn vị từ</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_stat2:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>Ký tự</h4>
                    <h2>{char_count:,}</h2>
                    <p>toàn bộ nội dung</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_stat3:
            st.markdown(
                f"""
                <div class="metric-card">
                    <h4>Thời lượng</h4>
                    <h2>{estimated_time:.1f}</h2>
                    <p>phút đọc</p>
                </div>
                """,
                unsafe_allow_html=True,
            )

        with col_stat4:
            if "agent" in st.session_state:
                try:
                    doc_buffer = st.session_state.agent.create_document(script, i)
                    st.download_button(
                        label="💾 Tải xuống .docx",
                        data=doc_buffer,
                        file_name=f"GT365_Script_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_pro_{i}",
                        use_container_width=True,
                    )
                except Exception as exc:
                    st.error(f"Lỗi tạo file: {exc}")

        if i < len(scripts):
            st.markdown("<div style='height:0.5rem;'></div>", unsafe_allow_html=True)


def render_footer():
    """Giữ lại để tương thích, hiện không render footer."""
    return


def show_success_message(num_scripts, num_articles):
    """Hiển thị thông báo thành công."""
    st.markdown(
        f"""
        <div class="success-box fade-in">
            <strong>Hoàn tất:</strong> Đã tạo {num_scripts} kịch bản từ {num_articles} bài báo.
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_error_message(error_msg):
    """Hiển thị thông báo lỗi."""
    st.markdown(f'<div class="error-box"><strong>Lỗi:</strong> {error_msg}</div>', unsafe_allow_html=True)


def show_warning_message(warning_msg):
    """Hiển thị thông báo cảnh báo."""
    st.markdown(f'<div class="warning-box"><strong>Lưu ý:</strong> {warning_msg}</div>', unsafe_allow_html=True)
