"""
Các thành phần UI/UX thuần túy cho GT365 Radio News Script Generator.
Chứa các hàm vẽ khối HTML, CSS, thông báo... Không xử lý logic rẽ nhánh phức tạp.
"""

from html import escape
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
        <div class="hero-shell fade-in">
            <div class="hero-inner">
                <div class="hero-content">
                    <div class="hero-eyebrow">GT365 Radio Workspace · Version 2.0</div>
                    <div class="hero-title">Biến bài báo thành<br><em>kịch bản phát thanh</em></div>
                    <p class="hero-copy">
                        Dán tự do link bài báo, cấu hình phong cách mong muốn và nhận ngay kịch bản được phân tích chuẩn xác,
                        tối ưu hoàn toàn cho giọng đọc radio, podcast hoặc bản tin video chuyên nghiệp.
                    </p>
                    <div class="hero-badges">
                        <span class="h-badge">⚡ Tốc độ xử lý đa luồng</span>
                        <span class="h-badge">🎯 Tối ưu văn phong đọc</span>
                        <span class="h-badge">🎙️ Sẵn sàng bóc băng TTS</span>
                    </div>
                </div>
                <div class="hero-stats-panel">
                    <div class="hero-stat">
                        <span>Đầu vào</span>
                        <strong>11+ trang báo Việt Nam</strong>
                        <div class="stat-bar"></div>
                    </div>
                    <div class="hero-stat">
                        <span>Đầu ra</span>
                        <strong>Cấu trúc tin tức rành mạch</strong>
                        <div class="stat-bar"></div>
                    </div>
                    <div class="hero-stat">
                        <span>Lưu trữ</span>
                        <strong>Hỗ trợ tải Audio & Word</strong>
                        <div class="stat-bar"></div>
                    </div>
                </div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_header(icon: str, title: str, subtitle: str = "", note: str = ""):
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
        
        st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
        st.warning(
            "⚠️ **Lưu ý:** Các trang báo như **Dân Trí, Người Lao Động, CAND, Pháp Luật** "
            "đôi khi bị chặn tự động bởi bảo mật (Cookie/Cloudflare). Bạn nên cân nhắc "
            "ghi chèn link của các nguồn này vào thẳng ô 'Yêu cầu biên tập' bên dưới để bot "
            "tham khảo thêm thông tin kịch bản."
        )


def render_tab_navigation_header():
    """Hiển thị header điều hướng tab (phần text)."""
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


def render_empty_state_results():
    """Trạng thái khi chưa có kết quả nào."""
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


def render_result_overview(short_title, source, word_count, scripts_count):
    """Hiển thị thẻ tổng quan kết quả."""
    st.markdown(
        f"""
        <div class="soft-grid fade-in">
            <div class="soft-stat">
                <span>Tiêu đề</span>
                <strong>{short_title}</strong>
            </div>
            <div class="soft-stat">
                <span>Nguồn</span>
                <strong>{source}</strong>
            </div>
            <div class="soft-stat">
                <span>Số từ gốc</span>
                <strong>{word_count:,}</strong>
            </div>
            <div class="soft-stat">
                <span>Kịch bản</span>
                <strong>{scripts_count} phiên bản</strong>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_result_item_card(i):
    """Hiển thị tiêu đề của một kịch bản kết quả."""
    st.markdown(
        f"""
        <div class="result-card fade-in">
            <div class="result-head">
                <div class="result-title-wrap">
                    <div class="result-index">{i:02d}</div>
                    <div class="result-copy">
                        <div class="result-title">Kịch bản {i}</div>
                        <div class="result-subtitle">Kịch bản đã sẵn sàng.</div>
                    </div>
                </div>
                <div class="result-badge">Phiên bản {i}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_metric_card(label, value, note):
    """Hiển thị thẻ chỉ số cho kịch bản (Số từ, ký tự, v.v.)."""
    html = f'<div class="metric-card"><div class="metric-label">{label}</div><div class="metric-value">{value}</div><div class="metric-note">{note}</div></div>'
    st.markdown(html, unsafe_allow_html=True)


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


def render_ai_section(model_options: dict):
    """Ẩn khỏi UI, giữ để tương thích với app."""
    model_labels = list(model_options.keys())
    default_label = model_labels[0]
    return default_label, model_options[default_label], ""


def render_ai_status(*args, **kwargs):
    """Ẩn khỏi UI."""
    return


def render_footer():
    """Tương thích ngược."""
    return
