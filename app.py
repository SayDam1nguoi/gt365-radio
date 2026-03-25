"""
GT365 Radio News Script Generator - ứng dụng chính.
"""

import os
import sys

from dotenv import load_dotenv

load_dotenv()

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from giao_dien.giaodien import *  # noqa: F403
from src.news_agent import NewsScriptAgent


def main():
    """Điểm vào chính của ứng dụng."""
    setup_page_config()
    load_custom_css()
    render_header()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    render_supported_sources()
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    if "total_scripts" not in st.session_state:
        st.session_state.total_scripts = 0

    if "show_results_view" not in st.session_state:
        st.session_state.show_results_view = False

    tab_tao, tab_ket_qua = st.tabs(["Tạo kịch bản", "Kết quả"])

    with tab_tao:
        handle_script_creation()

    with tab_ket_qua:
        render_results_tab()


def handle_script_creation():
    """Xử lý form tạo kịch bản."""
    api_key = os.getenv("OPENAI_API_KEY", "")
    ai_model = "gpt-3.5-turbo"

    if "agent" not in st.session_state:
        st.session_state.agent = NewsScriptAgent(ai_model, api_key)

    news_urls = render_input_section()
    user_prompt = render_prompt_section()
    script_length, custom_length, num_scripts = render_config_section()

    st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

    if st.button("Tạo kịch bản chuyên nghiệp", type="primary", use_container_width=True):
        if not news_urls:
            show_error_message("Vui lòng nhập ít nhất một link bài báo hợp lệ.")
            return

        if not user_prompt.strip():
            show_warning_message("Vui lòng nhập prompt để Agent hiểu rõ yêu cầu của bạn.")
            return

        final_length = (
            f"{custom_length} phút" if script_length == "Tùy chỉnh" and custom_length else script_length
        )
        process_news_to_script(news_urls, user_prompt, final_length, num_scripts)


def process_news_to_script(urls, prompt, length, num_scripts):
    """Tạo kịch bản từ danh sách URL."""
    agent = st.session_state.agent

    try:
        agent_status = agent.get_agent_status()
        if not agent_status["has_api_key"]:
            show_error_message("News Agent chưa có API key. Vui lòng cấu hình trong file `.env`.")
            return

        success, results = agent.process_multiple_news_to_script(
            urls=urls,
            prompt=prompt,
            length=length,
            num_scripts=num_scripts,
            source="universal",
        )

        if success:
            save_results_to_session(results)
            show_success_message(len(results["scripts"]), len(results.get("articles", [])))
        else:
            show_error_message(results.get("error", "Không xác định"))
    except Exception as exc:
        show_error_message(f"Lỗi hệ thống: {exc}")


def save_results_to_session(results):
    """Lưu kết quả vào session state."""
    st.session_state.agent_results = results
    st.session_state.scripts = results["scripts"]
    st.session_state.total_scripts += len(results["scripts"])

    if "combined_info" in results["metadata"]:
        combined_info = results["metadata"]["combined_info"]
        article_info = {
            "title": f"Tổng hợp từ {combined_info['total_articles']} bài báo",
            "source": ", ".join(combined_info["sources"]),
            "word_count": combined_info["total_word_count"],
        }
    else:
        article_info = (
            results["metadata"]["articles_info"][0]
            if results["metadata"].get("articles_info")
            else {}
        )

    st.session_state.article_info = article_info


if __name__ == "__main__":
    main()
