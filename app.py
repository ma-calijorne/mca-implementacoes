import streamlit as st

from modules.home import render_home
from modules.sorting import render_sorting_module
from modules.binary_search import render_binary_search_module
from modules.matrix_traversal import render_matrix_traversal_module
from modules.graph_bfs import render_graph_bfs_module
from modules.path_counting import render_path_counting_module

st.set_page_config(
    page_title="MathLab Computacional",
    page_icon="🧠",
    layout="wide",
    initial_sidebar_state="expanded",
)


def inject_global_styles() -> None:
    st.markdown(
        """
        <style>
            .main > div {
                padding-top: 1.2rem;
            }
            .mathlab-hero {
                padding: 1.25rem 1.5rem;
                border-radius: 18px;
                background: linear-gradient(135deg, #0f172a 0%, #1e293b 100%);
                color: white;
                border: 1px solid rgba(255,255,255,0.08);
                box-shadow: 0 10px 30px rgba(2, 6, 23, 0.18);
                margin-bottom: 1rem;
            }
            .mathlab-card {
                padding: 1rem 1.1rem;
                border-radius: 16px;
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                min-height: 140px;
            }
            .mathlab-metric-card {
                padding: 0.9rem 1rem;
                border-radius: 14px;
                background: white;
                border: 1px solid #e5e7eb;
                box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
            }
            .mathlab-step-box {
                padding: 1rem 1.1rem;
                border-radius: 16px;
                background: #f8fafc;
                border-left: 6px solid #2563eb;
                border-top: 1px solid #e2e8f0;
                border-right: 1px solid #e2e8f0;
                border-bottom: 1px solid #e2e8f0;
            }
            .mathlab-math-box {
                padding: 1rem 1.1rem;
                border-radius: 16px;
                background: #ecfeff;
                border-left: 6px solid #0891b2;
                border-top: 1px solid #cffafe;
                border-right: 1px solid #cffafe;
                border-bottom: 1px solid #cffafe;
            }
            .mathlab-footer-note {
                font-size: 0.95rem;
                color: #475569;
            }
        </style>
        """,
        unsafe_allow_html=True,
    )


def init_session_state() -> None:
    defaults = {
        "sort_states": [],
        "sort_step_index": 0,
        "sort_input_key": 0,
        "binary_states": [],
        "binary_step_index": 0,
        "binary_step_slider": 0,
        "matrix_states": [],
        "matrix_step_index": 0,
        "matrix_step_slider": 0,
        "graph_states": [],
        "graph_step_index": 0,
        "graph_step_slider": 0,
        "path_states": [],
        "path_step_index": 0,
        "path_step_slider": 0,
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


inject_global_styles()
init_session_state()

with st.sidebar:
    st.title("🧠 MathLab")
    st.caption("Laboratório Visual de Matemática Computacional Aplicada")
    selected_module = st.radio(
        "Escolha um módulo",
        options=["Início", "Módulo 1 • Ordenação", "Módulo 2 • Busca Binária", "Módulo 3 • Matrizes", "Módulo 4 • Grafos BFS", "Módulo 5 • Caminhos em Tabuleiro"],
        index=0,
    )
    st.divider()
    st.markdown("**Versão atual**")
    st.write("App base + Módulos 1, 2, 3, 4 e 5")

if selected_module == "Início":
    render_home()
elif selected_module == "Módulo 1 • Ordenação":
    render_sorting_module()
elif selected_module == "Módulo 2 • Busca Binária":
    render_binary_search_module()

elif selected_module == "Módulo 3 • Matrizes":
    render_matrix_traversal_module()
elif selected_module == "Módulo 4 • Grafos BFS":
    render_graph_bfs_module()
elif selected_module == "Módulo 5 • Caminhos em Tabuleiro":
    render_path_counting_module()
