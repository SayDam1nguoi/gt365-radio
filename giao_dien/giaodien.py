"""
Các hàm giao diện cho GT365 Radio News Script Generator.
"""

from datetime import datetime
from html import escape

import streamlit as st

from .styles import get_custom_css_string


def _rerun_streamlit():
    """Rerun tương thích nhiều phiên bản Streamlit."""
    rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun")
    rerun_fn()


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
        <div class="hero-shell fade-in">
            <div class="hero-eyebrow">GT365 Radio Workspace</div>
            <h1 class="hero-title">Biến bài báo thành<br><em>kịch bản phát thanh</em></h1>
            <p class="hero-copy">
                Dán link bài báo, mô tả phong cách bạn muốn và nhận kịch bản sẵn sàng cho radio,
                podcast hoặc bản tin video trong vài chục giây.
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
                    <span>Tối ưu cho</span>
                    <strong>Biên tập và thu âm</strong>
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
                        <div class="section-title">{title}</div>
                        {subtitle_html}
                    </div>
                </div>
                {note_html}
            </div>
        </div>
        """,
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

    with st.expander("🌐  Các trang báo được hỗ trợ  ·  11 nguồn", expanded=False):
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


def render_input_section():
    """Hiển thị phần nhập danh sách link bài báo."""
    _render_section_header(
        "📰",
        "Nguồn tin đầu vào",
        "Nhập các đường dẫn bài báo muốn tổng hợp thành kịch bản.",
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
            f"Link {i + 1}",
            placeholder="https://vnexpress.net/...",
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
                    f'<div class="inline-error">URL {i + 1} phải bắt đầu bằng http:// hoặc https://</div>',
                    unsafe_allow_html=True,
                )

    col_add, col_remove, col_clear = st.columns(3)

    with col_add:
        if st.button("＋  Thêm link", use_container_width=True):
            if st.session_state.num_url_inputs < 10:
                st.session_state.num_url_inputs += 1
                st.rerun()

    with col_remove:
        if st.button("－  Bớt link", use_container_width=True):
            if st.session_state.num_url_inputs > 1:
                st.session_state.num_url_inputs -= 1
                st.rerun()

    with col_clear:
        if st.button("✕  Xóa tất cả", use_container_width=True):
            st.session_state.clear_all_flag = True
            st.rerun()

    if valid_urls > 0:
        st.markdown(
            f"""
            <div class="success-box status-box">
                <strong>{valid_urls} URL sẵn sàng xử lý.</strong>
                {"Tất cả link đã hợp lệ." if valid_urls == st.session_state.num_url_inputs else "Một số ô đang để trống."}
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
        "Mô tả giọng điệu, phong cách và cách triển khai bạn muốn.",
        "Prompt",
    )

    return st.text_area(
        "Mô tả yêu cầu",
        placeholder=(
            "Ví dụ:\n"
            "- Viết kịch bản podcast 8 phút, giọng điệu chuyên nghiệp nhưng dễ nghe\n"
            "- Bản tin ngắn 3 phút, mở đầu trực diện, ưu tiên số liệu quan trọng\n"
            "- Script YouTube có intro mạnh, phân tích sâu, kết thúc gọn\n"
            "- Kịch bản trang trọng cho bản đọc nội bộ doanh nghiệp"
        ),
        height=160,
    )


def render_config_section():
    """Hiển thị cấu hình tạo kịch bản."""
    _render_section_header(
        "⚙️",
        "Cấu hình đầu ra",
        "Chọn phong cách kịch bản, thời lượng và số phiên bản muốn tạo.",
        "Config",
    )

    col1, col2, col3 = st.columns([2, 1, 1])

    with col1:
        script_style = st.selectbox(
            "Phong cách kịch bản",
            options=[
                "Ngắn: Nói qua nhanh",
                "Bình thường: Nói tin tức, phân tích nhẹ nhàng",
                "Chuyên sâu: Phân tích kỹ càng, ảnh hưởng tích cực & tiêu cực",
            ],
        )

    with col2:
        duration = st.number_input("Thời lượng (phút)", min_value=1, max_value=30, value=5)

    with col3:
        num_scripts = st.number_input("Số phiên bản", min_value=1, max_value=3, value=1)

    return script_style, duration, num_scripts


def render_ai_section(model_options: dict):
    """Ẩn khỏi UI, giữ để tương thích với app."""
    model_labels = list(model_options.keys())
    default_label = model_labels[0]
    return default_label, model_options[default_label], ""


def render_ai_status(*args, **kwargs):
    """Ẩn khỏi UI."""
    return


def render_tab_navigation():
    """Hiển thị điều hướng tab có thể điều khiển bằng session state."""
    st.markdown(
        """
        <div class="tab-nav-shell fade-in">
            <div class="tab-nav-copy">
                <span>Không gian làm việc</span>
                <strong>Chuyển nhanh giữa phần tạo kịch bản và kết quả</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    active_tab = st.session_state.get("active_tab", "Tạo kịch bản")
    col_create, col_result = st.columns(2)

    with col_create:
        if st.button(
            "● Tạo kịch bản" if active_tab == "Tạo kịch bản" else "Tạo kịch bản",
            key="nav_create_tab",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.active_tab = "Tạo kịch bản"
            _rerun_streamlit()

    with col_result:
        if st.button(
            "● Kết quả" if active_tab == "Kết quả" else "Kết quả",
            key="nav_result_tab",
            type="secondary",
            use_container_width=True,
        ):
            st.session_state.active_tab = "Kết quả"
            _rerun_streamlit()

    st.markdown("<div style='height: 0.8rem;'></div>", unsafe_allow_html=True)
    return active_tab


def render_progress_bar(progress_value, status_text, detail_text="", caption_text="", hosts=None):
    """Hiển thị panel tiến trình xử lý theo trạng thái thực tế."""
    safe_status = escape(str(status_text))
    panel_html = f"""
        <div class="progress-shell fade-in">
            <div class="progress-head">
                <div>
                    <div class="progress-kicker">Đang xử lý</div>
                    <div class="progress-status">{safe_status}</div>
                </div>
                <div class="progress-percent">{progress_value}%</div>
            </div>
        </div>
        """

    if hosts:
        hosts["panel"].markdown(panel_html, unsafe_allow_html=True)
        hosts["bar"].progress(max(0, min(100, int(progress_value))) / 100)

        if detail_text:
            hosts["detail"].markdown(
                f"<div class='progress-detail'>{escape(str(detail_text))}</div>",
                unsafe_allow_html=True,
            )
        else:
            hosts["detail"].empty()

        if caption_text:
            hosts["caption"].caption(str(caption_text))
        else:
            hosts["caption"].empty()
        return None, None

    st.markdown(panel_html, unsafe_allow_html=True)
    st.progress(max(0, min(100, int(progress_value))) / 100)

    if detail_text:
        st.markdown(
            f"<div class='progress-detail'>{escape(str(detail_text))}</div>",
            unsafe_allow_html=True,
        )
    if caption_text:
        st.caption(str(caption_text))

    return None, None


def render_result_switch_button():
    """Hiển thị nút đưa người dùng sang tab kết quả."""
    return st.button("Mở tab kết quả", use_container_width=True)


def render_results_tab():
    """Hiển thị khu vực kết quả."""
    if "scripts" not in st.session_state or not st.session_state.scripts:
        st.markdown(
            """
            <div class="empty-state fade-in">
                <div class="empty-state-icon">🎙️</div>
                <h3>Chưa có kịch bản nào</h3>
                <p>Tạo kịch bản ở tab <strong>Tạo kịch bản</strong>, kết quả sẽ hiển thị tại đây.</p>
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
        "Thông tin bài báo gốc và số lượng kịch bản đã tạo.",
        "Overview",
    )

    title = article_info.get("title", "N/A")
    short_title = title if len(title) <= 52 else f"{title[:52]}…"

    st.markdown(
        f"""
        <div class="soft-grid fade-in">
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
                <strong>{article_info.get("word_count", 0):,}</strong>
            </div>
            <div class="soft-stat">
                <span>Kịch bản</span>
                <strong>{len(scripts)} phiên bản</strong>
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
                        <div class="result-copy">
                            <div class="result-title">Kịch bản {i}</div>
                            <div class="result-subtitle">Đã tối ưu để biên tập và đọc thu âm.</div>
                        </div>
                    </div>
                    <div class="result-badge">Phiên bản {i}</div>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.text_area(
            f"script_{i}",
            value=script,
            height=360,
            key=f"script_display_{i}",
            label_visibility="collapsed",
            disabled=True,
        )

        col1, col2, col3, col4 = st.columns(4)

        with col1:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Số từ</div><div class="metric-value">{word_count:,}</div><div class="metric-note">từ</div></div>',
                unsafe_allow_html=True,
            )
        with col2:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Ký tự</div><div class="metric-value">{char_count:,}</div><div class="metric-note">ký tự</div></div>',
                unsafe_allow_html=True,
            )
        with col3:
            st.markdown(
                f'<div class="metric-card"><div class="metric-label">Thời lượng</div><div class="metric-value">{estimated_time:.1f}</div><div class="metric-note">phút đọc</div></div>',
                unsafe_allow_html=True,
            )
        with col4:
            if "agent" in st.session_state:
                try:
                    doc_buffer = st.session_state.agent.create_document(script, i)
                    st.download_button(
                        label="⬇  Tải xuống .docx",
                        data=doc_buffer,
                        file_name=f"GT365_Script_{i}_{datetime.now().strftime('%Y%m%d_%H%M%S')}.docx",
                        mime="application/vnd.openxmlformats-officedocument.wordprocessingml.document",
                        key=f"download_script_{i}",
                        use_container_width=True,
                    )
                except Exception as exc:
                    st.error(f"Lỗi tạo file: {exc}")

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)


def render_footer():
    """Tương thích ngược."""
    return


def show_success_message(num_scripts, num_articles):
    """Hiển thị thông báo tạo thành công."""
    st.markdown(
        f"""
        <div class="success-banner fade-in">
            <div class="success-banner__icon">✅</div>
            <div>
                <h3>Tạo kịch bản thành công</h3>
                <p>Đã tạo <strong>{num_scripts} kịch bản</strong> từ {num_articles} bài báo.</p>
                <span>Chuyển sang tab <strong>Kết quả</strong> để xem và tải xuống.</span>
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
