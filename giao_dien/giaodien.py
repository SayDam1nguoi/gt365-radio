"""
Các hàm giao diện cho GT365 Radio News Script Generator.
"""

from datetime import datetime

import streamlit as st

from .styles import get_custom_css_string


def setup_page_config():
    """Cấu hình trang Streamlit."""
    st.set_page_config(
        page_title="GT365 Radio - News Script Generator",
        page_icon="🎙️",
        layout="wide",
        initial_sidebar_state="collapsed",
    )


def load_custom_css():
    """Nạp CSS tùy biến."""
    st.markdown(f"<style>{get_custom_css_string()}</style>", unsafe_allow_html=True)


def render_header():
    """Hiển thị khối mở đầu."""
    st.markdown(
        """
        <div class="hero-shell">
            <div class="hero-eyebrow">GT365 Radio Workspace</div>
            <h1 class="hero-title">Biến bài báo thành kịch bản phát thanh rõ ràng, nhanh và chuyên nghiệp.</h1>
            <p class="hero-copy">
                Dán link bài báo, mô tả phong cách bạn muốn và tạo ngay kịch bản để dùng cho radio,
                podcast, video tin tức hoặc bản đọc tổng hợp nội bộ.
            </p>
            <div class="hero-grid">
                <div class="hero-stat">
                    <span>Đầu vào</span>
                    <strong>11+ trang báo Việt Nam</strong>
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


def _render_section_header(icon: str, title: str, subtitle: str = "", note: str = ""):
    """Hiển thị tiêu đề section."""
    note_html = f'<div class="pill-note">{note}</div>' if note else ""
    subtitle_html = f'<p class="section-subtitle">{subtitle}</p>' if subtitle else ""

    st.markdown(
        f"""
        <div class="section-card fade-in">
            <div class="section-head">
                <div class="section-title-wrap">
                    <div class="section-icon">{icon}</div>
                    <div class="section-copy">
                        <div class="section-kicker">Mục nội dung</div>
                        <h3 class="section-title">{title}</h3>
                        {subtitle_html}
                    </div>
                </div>
                {note_html}
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_input_section():
    """Hiển thị phần nhập danh sách link bài báo."""
    _render_section_header(
        "📰",
        "Nguồn tin đầu vào",
        "Nhập các đường dẫn bài báo mà bạn muốn tổng hợp thành kịch bản.",
        "Input",
    )

    if "num_url_inputs" not in st.session_state:
        st.session_state.num_url_inputs = 3

    if "clear_all_flag" not in st.session_state:
        st.session_state.clear_all_flag = False

    if st.session_state.clear_all_flag:
        for i in range(st.session_state.num_url_inputs):
            st.session_state.pop(f"url_input_{i}", None)
        st.session_state.clear_all_flag = False

    news_urls = []
    valid_urls = 0

    for i in range(st.session_state.num_url_inputs):
        url = st.text_input(
            f"Link bài báo {i + 1}",
            placeholder="Dán link bài báo hợp lệ vào đây",
            key=f"url_input_{i}",
        )

        if url.strip():
            if url.startswith(("http://", "https://")):
                news_urls.append(url.strip())
                valid_urls += 1
                st.markdown(
                    f'<div class="inline-valid">URL {i + 1} hợp lệ</div>',
                    unsafe_allow_html=True,
                )
            else:
                st.markdown(
                    f'<div class="inline-error">URL {i + 1} chưa hợp lệ, cần bắt đầu bằng http hoặc https</div>',
                    unsafe_allow_html=True,
                )

    col_add, col_remove, col_clear = st.columns(3)

    with col_add:
        if st.button("Thêm link", use_container_width=True):
            if st.session_state.num_url_inputs < 10:
                st.session_state.num_url_inputs += 1
                st.rerun()

    with col_remove:
        if st.button("Bớt link", use_container_width=True):
            if st.session_state.num_url_inputs > 1:
                st.session_state.num_url_inputs -= 1
                st.rerun()

    with col_clear:
        if st.button("Xóa tất cả", use_container_width=True):
            st.session_state.clear_all_flag = True
            st.rerun()

    if valid_urls > 0:
        st.markdown(
            f"""
            <div class="success-box status-box">
                <strong>Sẵn sàng xử lý:</strong> Đã nhận {valid_urls} URL hợp lệ.
            </div>
            """,
            unsafe_allow_html=True,
        )

    return news_urls


def render_prompt_section():
    """Hiển thị vùng nhập prompt."""
    _render_section_header(
        "✍️",
        "Yêu cầu biên tập",
        "Mô tả giọng điệu, độ dài và cách triển khai bạn muốn cho kịch bản.",
        "Prompt",
    )

    return st.text_area(
        "Mô tả yêu cầu của bạn",
        placeholder=(
            "Ví dụ:\n"
            "- Viết kịch bản podcast 8 phút, giọng điệu chuyên nghiệp nhưng dễ nghe\n"
            "- Tạo bản tin ngắn 3 phút, mở đầu trực diện, ưu tiên số liệu quan trọng\n"
            "- Viết script YouTube có intro mạnh, nội dung phân tích sâu và kết thúc gọn\n"
            "- Tạo kịch bản trang trọng cho bản đọc nội bộ doanh nghiệp"
        ),
        height=170,
    )


def render_config_section():
    """Hiển thị cấu hình tạo kịch bản."""
    _render_section_header(
        "⚙️",
        "Cấu hình đầu ra",
        "Chọn thời lượng và số phiên bản muốn tạo.",
        "Output",
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
        )

    with col_config2:
        custom_length = (
            st.number_input("Số phút", min_value=1, max_value=30, value=5)
            if script_length == "Tùy chỉnh"
            else None
        )

    with col_config3:
        num_scripts = st.number_input("Số lượng phiên bản", min_value=1, max_value=3, value=1)

    return script_length, custom_length, num_scripts


def render_progress_bar(progress_value, status_text):
    """Giữ lại để tương thích, hiện không dùng loading riêng."""
    st.info(f"{status_text} ({progress_value}%)")
    return None, None


def render_results_tab():
    """Hiển thị khu vực kết quả."""
    if "scripts" not in st.session_state or not st.session_state.scripts:
        st.markdown(
            """
            <div class="empty-state">
                <h3>Chưa có kịch bản nào</h3>
                <p>Tạo kịch bản ở tab đầu tiên, kết quả sẽ hiển thị tại đây.</p>
            </div>
            """,
            unsafe_allow_html=True,
        )
        return

    scripts = st.session_state.scripts
    article_info = st.session_state.article_info

    _render_section_header(
        "📁",
        "Tổng quan kết quả",
        "Tóm tắt nhanh dữ liệu đầu vào và số lượng kịch bản đã tạo.",
        "Overview",
    )

    title = article_info.get("title", "N/A")
    short_title = title if len(title) <= 56 else f"{title[:56]}..."

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
        word_count = len(script.split())
        char_count = len(script)
        estimated_time = word_count / 160

        st.markdown(
            f"""
            <div class="result-card fade-in">
                <div class="result-head">
                    <div class="result-title-wrap">
                        <div class="result-index">{i:02d}</div>
                        <div>
                            <h3>Kịch bản {i}</h3>
                            <p>Bản nội dung đã được tối ưu để biên tập và đọc thu âm.</p>
                        </div>
                    </div>
                    <div class="result-badge">Phiên bản {i}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            f"Nội dung kịch bản {i}",
            value=script,
            height=380,
            key=f"script_display_{i}",
            label_visibility="collapsed",
        )

        col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

        with col_stat1:
            st.markdown(
                f'<div class="metric-card"><h4>Số từ</h4><h2>{word_count:,}</h2><p>đơn vị từ</p></div>',
                unsafe_allow_html=True,
            )
        with col_stat2:
            st.markdown(
                f'<div class="metric-card"><h4>Ký tự</h4><h2>{char_count:,}</h2><p>toàn bộ nội dung</p></div>',
                unsafe_allow_html=True,
            )
        with col_stat3:
            st.markdown(
                f'<div class="metric-card"><h4>Thời lượng</h4><h2>{estimated_time:.1f}</h2><p>phút đọc</p></div>',
                unsafe_allow_html=True,
            )
        with col_stat4:
            if "agent" in st.session_state:
                try:
                    doc_buffer = st.session_state.agent.create_document(script, i)
                    st.download_button(
                        label="Tải xuống .docx",
                        data=doc_buffer,
                        file_name=f"GT365_Script_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_script_{i}",
                        use_container_width=True,
                    )
                except Exception as exc:
                    st.error(f"Lỗi tạo file: {exc}")

        st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)


def render_footer():
    """Giữ lại để tương thích."""
    return


def show_success_message(num_scripts, num_articles):
    """Hiển thị thông báo tạo thành công."""
    st.markdown(
        f"""
        <div class="success-banner">
            <div class="success-banner__icon">✅</div>
            <div>
                <h3>Tạo kịch bản thành công!</h3>
                <p>Đã tạo {num_scripts} kịch bản từ {num_articles} bài báo.</p>
                <span>Đã tạo xong kịch bản, nhấn tab Kết quả ở trên để xem nội dung.</span>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def show_error_message(error_msg):
    """Hiển thị lỗi."""
    st.markdown(
        f'<div class="error-box status-box"><strong>Lỗi:</strong> {error_msg}</div>',
        unsafe_allow_html=True,
    )


def show_warning_message(warning_msg):
    """Hiển thị cảnh báo."""
    st.markdown(
        f'<div class="warning-box status-box"><strong>Lưu ý:</strong> {warning_msg}</div>',
        unsafe_allow_html=True,
    )


def render_supported_sources():
    """Hiển thị danh sách các nguồn báo được hỗ trợ."""
    sources_list = [
        ("Quân Đội Nhân Dân", "qdnd.vn"),
        ("VTV Tin tức", "vtv.vn"),
        ("Nhân Dân", "nhandan.vn"),
        ("Tuổi Trẻ Online", "tuoitre.vn"),
        ("VnExpress", "vnexpress.net"),
        ("Dân trí", "dantri.com.vn"),
        ("Thanh Niên", "thanhnien.vn"),
        ("Lao Động", "laodong.vn"),
        ("Người Lao Động", "nld.com.vn"),
        ("Công an Nhân dân", "cand.com.vn"),
        ("Báo Pháp luật Việt Nam", "baophapluat.vn"),
    ]

    _render_section_header(
        "🌐",
        "Các trang báo được hỗ trợ",
        "Hệ thống tự động crawl nội dung từ nhiều nguồn báo điện tử phổ biến tại Việt Nam.",
        "Sources",
    )

    cols = st.columns(4)
    for idx, (name, domain) in enumerate(sources_list):
        with cols[idx % 4]:
            st.markdown(
                f"""
                <div class="source-chip">
                    <div class="source-chip__name">{name}</div>
                    <div class="source-chip__domain">{domain}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )
