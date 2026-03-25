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


MODEL_OPTIONS = {
    "OpenAI GPT-3.5 Turbo": "gpt-3.5-turbo",
    "OpenAI GPT-4": "gpt-4",
    "Claude 3 Haiku": "claude-3-haiku-20240307",
    "Claude 3 Sonnet": "claude-3-sonnet-20240229",
}


def get_provider_for_model(model_name: str) -> str:
    """Xác định provider từ tên model."""
    return "anthropic" if "claude" in model_name.lower() else "openai"


def get_env_key_name_for_model(model_name: str) -> str:
    """Trả về tên biến môi trường tương ứng với model."""
    return "ANTHROPIC_API_KEY" if get_provider_for_model(model_name) == "anthropic" else "OPENAI_API_KEY"


def resolve_api_key(model_name: str, manual_api_key: str) -> tuple[str, str]:
    """Ưu tiên key nhập tay, nếu không có thì fallback sang biến môi trường."""
    manual_api_key = (manual_api_key or "").strip()
    if manual_api_key:
        return manual_api_key, "manual"

    env_key_name = get_env_key_name_for_model(model_name)
    env_api_key = os.getenv(env_key_name, "").strip()
    if env_api_key:
        return env_api_key, env_key_name

    return "", env_key_name


def ensure_agent(model_name: str, api_key: str):
    """Khởi tạo hoặc làm mới agent khi model/key thay đổi."""
    current_model = st.session_state.get("agent_model")
    current_api_key = st.session_state.get("agent_api_key")

    if (
        "agent" not in st.session_state
        or current_model != model_name
        or current_api_key != api_key
    ):
        st.session_state.agent = NewsScriptAgent(model_name, api_key)
        st.session_state.agent_model = model_name
        st.session_state.agent_api_key = api_key


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

    tab_tao, tab_ket_qua = st.tabs(["Tạo kịch bản", "Kết quả"])

    with tab_tao:
        handle_script_creation()

    with tab_ket_qua:
        render_results_tab()


def handle_script_creation():
    """Xử lý form tạo kịch bản."""
    news_urls = render_input_section()
    user_prompt = render_prompt_section()
    script_length, custom_length, num_scripts = render_config_section()
    selected_label, selected_model, manual_api_key = render_ai_section(MODEL_OPTIONS)

    resolved_api_key, api_key_source = resolve_api_key(selected_model, manual_api_key)
    ensure_agent(selected_model, resolved_api_key)

    render_ai_status(selected_label, selected_model, api_key_source, bool(resolved_api_key))
    st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

    if st.button("Tạo kịch bản chuyên nghiệp", type="primary", use_container_width=True):
        if not news_urls:
            show_error_message("Vui lòng nhập ít nhất một link bài báo hợp lệ.")
            return

        if not user_prompt.strip():
            show_warning_message("Vui lòng nhập prompt để Agent hiểu rõ yêu cầu của bạn.")
            return

        if not resolved_api_key:
            show_error_message(
                f"Chưa có API key cho model đã chọn. Vui lòng nhập trực tiếp hoặc cấu hình biến môi trường {api_key_source}."
            )
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
            env_name = get_env_key_name_for_model(agent_status["ai_model"])
            show_error_message(
                f"News Agent chưa có API key. Vui lòng nhập trực tiếp hoặc cấu hình biến môi trường {env_name}."
            )
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
