import streamlit as st



def render_step_box(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="mathlab-step-box">
            <h4 style="margin-top:0;">{title}</h4>
            <p style="margin-bottom:0;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )



def render_math_box(title: str, message: str) -> None:
    st.markdown(
        f"""
        <div class="mathlab-math-box">
            <h4 style="margin-top:0;">{title}</h4>
            <p style="margin-bottom:0;">{message}</p>
        </div>
        """,
        unsafe_allow_html=True,
    )
