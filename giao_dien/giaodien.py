"""
Các hàm điều hướng và xử lý logic kết nối UI cho GT365 Radio News Script Generator.
"""

import os
import hashlib
from datetime import datetime
import time
import streamlit as st
from src.tts import TTSService

# Export tất cả các thành phần UI để app.py có thể lấy qua giaodien.py (do app.py đang import *)
from .ui import *


def cleanup_old_audio_files(dir_path: str, max_age_hours: int = 24):
    """Xóa các file audio cũ trong thư mục để tránh tràn ổ cứng (Bug Fix BE/FE)."""
    if not os.path.exists(dir_path):
        return
    now = time.time()
    for filename in os.listdir(dir_path):
        file_path = os.path.join(dir_path, filename)
        if os.path.isfile(file_path):
            # Nếu file cũ hơn max_age_hours, xóa đi
            if os.stat(file_path).st_mtime < now - (max_age_hours * 3600):
                try:
                    os.remove(file_path)
                except Exception:
                    pass


def _rerun_streamlit():
    """Rerun tương thích nhiều phiên bản Streamlit."""
    rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun")
    rerun_fn()


def render_input_section():
    """Xử lý phần nhập danh sách link bài báo."""
    render_section_header(
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
                _rerun_streamlit()

    with col_remove:
        if st.button("－  Bớt link", use_container_width=True):
            if st.session_state.num_url_inputs > 1:
                st.session_state.num_url_inputs -= 1
                _rerun_streamlit()

    with col_clear:
        if st.button("✕  Xóa tất cả", use_container_width=True):
            st.session_state.clear_all_flag = True
            _rerun_streamlit()

    if valid_urls > 0:
        msg_suffix = "Tất cả link đã hợp lệ." if valid_urls == st.session_state.num_url_inputs else "Một số ô đang để trống."
        st.markdown(
            f"""
            <div class="success-box status-box">
                <strong>{valid_urls} URL sẵn sàng xử lý.</strong>
                {msg_suffix}
            </div>
            """,
            unsafe_allow_html=True,
        )

    return news_urls


def render_prompt_section():
    """Hiển thị và xử lý vùng nhập prompt."""
    render_section_header(
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
    render_section_header(
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
                "Ngắn",
                "Bình thường",
                "Chuyên sâu",
            ],
        )

    with col2:
        duration = st.number_input("Thời lượng (phút)", min_value=1, max_value=30, value=5)

    with col3:
        num_scripts = st.number_input("Số phiên bản", min_value=1, max_value=3, value=1)

    return script_style, duration, num_scripts


def render_tab_navigation():
    """Quản lý điều hướng tab có thể điều khiển bằng session state."""
    render_tab_navigation_header()

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


def render_results_tab():
    """Quản lý logic và hiển thị khu vực kết quả."""
    if "scripts" not in st.session_state or not st.session_state.scripts:
        render_empty_state_results()
        return

    scripts = st.session_state.scripts
    article_info = st.session_state.article_info

    render_section_header(
        "📁",
        "Tổng quan kết quả",
        "Thông tin bài báo gốc và số lượng kịch bản đã tạo.",
        "Overview",
    )

    title = article_info.get("title", "N/A")
    short_title = title if len(title) <= 52 else f"{title[:52]}…"
    
    render_result_overview(
        short_title=short_title,
        source=article_info.get("source", "N/A"),
        word_count=article_info.get("word_count", 0),
        scripts_count=len(scripts)
    )

    for i, script in enumerate(scripts, 1):
        word_count = len(script.split())
        char_count = len(script)
        estimated_time = word_count / 130

        render_result_item_card(i)

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
            render_metric_card("Số từ", f"{word_count:,}", "từ")
        with col2:
            render_metric_card("Ký tự", f"{char_count:,}", "ký tự")
        with col3:
            render_metric_card("Thời lượng", f"{estimated_time:.1f}", "phút đọc")
        
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
                
                # Thêm chức năng TTS
                # Băm nội dung kịch bản để tạo key duy nhất, tránh dùng lại audio cũ cho kịch bản mới
                script_hash = hashlib.md5(script.encode('utf-8')).hexdigest()
                audio_key = f"audio_path_{i}_{script_hash}"
                
                if audio_key in st.session_state and os.path.exists(st.session_state[audio_key]):
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                    st.audio(st.session_state[audio_key])
                else:
                    st.markdown("<div style='height: 0.5rem;'></div>", unsafe_allow_html=True)
                    if st.button("🗣️ Nói (TTS)", key=f"speak_btn_{i}_{script_hash[:8]}", use_container_width=True):
                        with st.spinner("Đang tạo audio..."):
                            tts = TTSService()
                            os.makedirs("output_audio", exist_ok=True)
                            cleanup_old_audio_files("output_audio", max_age_hours=2)
                            
                            out_path = f"output_audio/script_audio_{i}_{datetime.now().strftime('%M%S')}.wav"
                            success = tts.generate_audio(script, out_path)
                            
                            if success:
                                st.session_state[audio_key] = out_path
                                _rerun_streamlit()
                            else:
                                st.error("Lỗi tạo giọng đọc. Vui lòng xem log Console.")

        st.markdown("<div style='height: 1.2rem;'></div>", unsafe_allow_html=True)
