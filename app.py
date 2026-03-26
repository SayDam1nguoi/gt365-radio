"""
GT365 Radio News Script Generator - ứng dụng chính.
"""

import os
import sys

from dotenv import load_dotenv
import streamlit as st

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


def rerun_app():
    """Rerun tương thích nhiều phiên bản Streamlit."""
    rerun_fn = getattr(st, "rerun", None) or getattr(st, "experimental_rerun")
    rerun_fn()


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


def ensure_ui_state():
    """Khởi tạo state cho UI điều hướng và tiến trình."""
    if "total_scripts" not in st.session_state:
        st.session_state.total_scripts = 0
    if "active_tab" not in st.session_state:
        st.session_state.active_tab = "Tạo kịch bản"
    if "processing_state" not in st.session_state:
        st.session_state.processing_state = None
    if "result_navigation_ready" not in st.session_state:
        st.session_state.result_navigation_ready = False


def main():
    """Điểm vào chính của ứng dụng."""
    setup_page_config()
    load_custom_css()
    ensure_ui_state()
    render_header()

    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)
    render_supported_sources()
    st.markdown("<div style='height: 1rem;'></div>", unsafe_allow_html=True)

    active_tab = render_tab_navigation()
    if active_tab == "Tạo kịch bản":
        handle_script_creation()
    else:
        st.session_state.result_navigation_ready = False
        render_results_tab()


def handle_script_creation():
    """Xử lý form tạo kịch bản."""
    news_urls = render_input_section()
    user_prompt = render_prompt_section()
    script_style, duration, num_scripts = render_config_section()
    selected_label, selected_model, manual_api_key = render_ai_section(MODEL_OPTIONS)

    resolved_api_key, api_key_source = resolve_api_key(selected_model, manual_api_key)
    ensure_agent(selected_model, resolved_api_key)

    render_ai_status(selected_label, selected_model, api_key_source, bool(resolved_api_key))
    st.markdown("<div style='height: 0.6rem;'></div>", unsafe_allow_html=True)

    progress_hosts = {
        "panel": st.empty(),
        "bar": st.empty(),
        "detail": st.empty(),
        "caption": st.empty(),
    }

    if st.session_state.get("result_navigation_ready") and st.session_state.get("agent_results"):
        results = st.session_state.agent_results
        show_success_message(len(results.get("scripts", [])), len(results.get("articles", [])))
        if render_result_switch_button():
            st.session_state.active_tab = "Kết quả"
            st.session_state.result_navigation_ready = False
            rerun_app()

    def on_generate_click():
        st.session_state.is_generating = True

    is_generating = st.session_state.get("is_generating", False)
    generate_btn_container = st.empty()

    generate_btn_container.button(
        "Đang xử lý..." if is_generating else "Tạo kịch bản",
        type="primary",
        use_container_width=True,
        disabled=is_generating,
        on_click=on_generate_click,
        key="btn_generate_start"
    )

    if is_generating:
        st.session_state.is_generating = False

        if not news_urls:
            show_error_message("Vui lòng nhập ít nhất một link bài báo hợp lệ.")
            generate_btn_container.button("Tạo kịch bản", type="primary", use_container_width=True, on_click=on_generate_click, key="btn_generate_err1")
            return

        if not user_prompt.strip():
            show_warning_message("Vui lòng nhập prompt để Agent hiểu rõ yêu cầu của bạn.")
            generate_btn_container.button("Tạo kịch bản", type="primary", use_container_width=True, on_click=on_generate_click, key="btn_generate_err2")
            return

        if not resolved_api_key:
            show_error_message(
                f"Chưa có API key cho model đã chọn. Vui lòng nhập trực tiếp hoặc cấu hình biến môi trường {api_key_source}."
            )
            generate_btn_container.button("Tạo kịch bản", type="primary", use_container_width=True, on_click=on_generate_click, key="btn_generate_err3")
            return

        final_duration = f"{duration} phút"
        process_news_to_script(news_urls, user_prompt, script_style, final_duration, num_scripts, progress_hosts)
        
        generate_btn_container.button("Tạo kịch bản", type="primary", use_container_width=True, on_click=on_generate_click, key="btn_generate_done")


def render_processing_state(progress_hosts, payload):
    """Vẽ panel tiến trình trong đúng vùng UI hiện tại."""
    detail_parts = []
    current_item = payload.get("current_item")
    total_items = payload.get("total_items")
    current_script = payload.get("current_script")
    total_scripts = payload.get("total_scripts")
    completed_units = payload.get("completed_units")
    total_units = payload.get("total_units")

    if current_item and total_items:
        detail_parts.append(f"URL {current_item}/{total_items}")
    if current_script and total_scripts:
        detail_parts.append(f"Kịch bản {current_script}/{total_scripts}")

    detail_text = " · ".join(detail_parts)
    caption_text = ""
    if completed_units is not None and total_units:
        caption_text = f"Tiến độ thực tế theo khối lượng công việc: {completed_units}/{total_units}"

    render_progress_bar(
        payload.get("percent", 0),
        payload.get("status", "Đang xử lý..."),
        detail_text=detail_text,
        caption_text=caption_text,
        hosts=progress_hosts,
    )


def process_news_to_script(urls, prompt, script_style, duration, num_scripts, progress_hosts):
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

        st.session_state.processing_state = {"percent": 0, "status": "Đang chuẩn bị xử lý..."}
        st.session_state.result_navigation_ready = False
        render_processing_state(progress_hosts, st.session_state.processing_state)

        def progress_callback(payload):
            st.session_state.processing_state = payload
            render_processing_state(progress_hosts, payload)

        agent.set_progress_callback(progress_callback)

        success, results = agent.process_multiple_news_to_script(
            urls=urls,
            prompt=prompt,
            style=script_style,
            duration=duration,
            num_scripts=num_scripts,
            source="universal",
        )

        if success:
            save_results_to_session(results)
            st.session_state.result_navigation_ready = True
            st.session_state.processing_state = {
                **st.session_state.processing_state,
                "percent": 100,
                "status": "Hoàn tất tạo kịch bản. Bạn có thể chuyển sang tab kết quả.",
            }
            render_processing_state(progress_hosts, st.session_state.processing_state)
            show_success_message(len(results["scripts"]), len(results.get("articles", [])))
            if render_result_switch_button():
                st.session_state.active_tab = "Kết quả"
                st.session_state.result_navigation_ready = False
                rerun_app()
        else:
            show_error_message(results.get("error", "Không xác định"))
    except Exception as exc:
        show_error_message(f"Lỗi hệ thống: {exc}")
    finally:
        agent.set_progress_callback(None)


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
