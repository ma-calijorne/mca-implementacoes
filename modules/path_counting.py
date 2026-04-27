from __future__ import annotations

from typing import Any, Dict, List, Set, Tuple

import plotly.graph_objects as go
import streamlit as st

from algorithms.combinatorics_algorithms import (
    build_obstacles,
    count_paths_without_obstacles_formula,
    generate_grid_path_states,
)
from components.panels import render_math_box, render_step_box

Cell = Tuple[int, int]


def _reset_path_states() -> None:
    st.session_state.path_states = []
    st.session_state.path_step_index = 0
    st.session_state.path_step_slider = 0


def _load_path_states(rows: int, cols: int, obstacles: Set[Cell]) -> None:
    st.session_state.path_states = generate_grid_path_states(rows, cols, obstacles)
    st.session_state.path_step_index = 0
    st.session_state.path_step_slider = 0


def _render_path_metrics(state: Dict[str, Any], pattern: str) -> None:
    rows = state["rows"]
    cols = state["cols"]
    obstacles = state.get("obstacles", [])
    processed = state.get("processed", [])
    path_count = state.get("path_count", 0)

    st.subheader("Métricas da execução")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Linhas", rows)
    c2.metric("Colunas", cols)
    c3.metric("Obstáculos", len(obstacles))
    c4.metric("Processadas", len(processed))
    c5.metric("Caminhos", path_count)
    c6.metric("Passo", f"{state['step_number']}/{state['total_steps']}")
    st.caption(f"Padrão de obstáculos: {pattern}")


def _render_path_grid(state: Dict[str, Any]) -> go.Figure:
    rows = state["rows"]
    cols = state["cols"]
    obstacles = set(tuple(cell) for cell in state.get("obstacles", []))
    processed = set(tuple(cell) for cell in state.get("processed", []))
    current = tuple(state["current"]) if state.get("current") is not None else None
    start = tuple(state.get("start", (0, 0)))
    end = tuple(state.get("end", (rows - 1, cols - 1)))
    dp = state["dp"]

    z: List[List[int]] = []
    text_grid: List[List[str]] = []

    for r in range(rows):
        z_row: List[int] = []
        text_row: List[str] = []
        for c in range(cols):
            cell = (r, c)
            if cell in obstacles:
                z_row.append(0)
                label = "X"
            elif cell == current:
                z_row.append(4)
                label = str(dp[r][c])
            elif cell == start:
                z_row.append(3)
                label = str(dp[r][c])
            elif cell == end and cell in processed:
                z_row.append(5)
                label = str(dp[r][c])
            elif cell in processed:
                z_row.append(2)
                label = str(dp[r][c])
            else:
                z_row.append(1)
                label = ""
            text_row.append(f"{label}<br>({r},{c})")
        z.append(z_row)
        text_grid.append(text_row)

    fig = go.Figure(
        data=[
            go.Heatmap(
                z=z,
                text=text_grid,
                texttemplate="%{text}",
                textfont={"size": 14},
                colorscale=[
                    [0.0, "#334155"],
                    [0.16, "#334155"],
                    [0.17, "#e2e8f0"],
                    [0.33, "#e2e8f0"],
                    [0.34, "#93c5fd"],
                    [0.50, "#93c5fd"],
                    [0.51, "#22c55e"],
                    [0.67, "#22c55e"],
                    [0.68, "#f97316"],
                    [0.84, "#f97316"],
                    [0.85, "#a855f7"],
                    [1.0, "#a855f7"],
                ],
                zmin=0,
                zmax=5,
                showscale=False,
                hovertemplate="%{text}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=max(380, rows * 86),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Coluna",
        yaxis_title="Linha",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(dtick=1, side="top", showgrid=False)
    fig.update_yaxes(dtick=1, autorange="reversed", showgrid=False)
    return fig


def render_path_counting_module() -> None:
    st.title("Módulo 5 • Caminhos em Tabuleiro")
    st.caption(
        "Contagem de caminhos em uma grade, conectando combinatória, princípio aditivo, programação dinâmica e espaço de possibilidades."
    )

    left, right = st.columns([1.15, 1.85], gap="large")

    with left:
        st.subheader("1. O problema")
        st.write(
            "Um robô começa no canto superior esquerdo e precisa chegar ao canto inferior direito. "
            "A cada passo, ele só pode mover para a direita ou para baixo. O objetivo é contar quantos caminhos válidos existem."
        )

        st.subheader("2. Conceitos matemáticos envolvidos")
        st.markdown(
            """
            - **Princípios de contagem**: soma de possibilidades por célula.
            - **Combinações**: sem obstáculos, escolhemos a posição dos movimentos para baixo ou direita.
            - **Conjuntos**: células livres, células bloqueadas e células processadas.
            - **Funções**: cada posição `(linha, coluna)` recebe um número de caminhos.
            - **Relações**: cada célula depende da célula acima e da célula à esquerda.
            """
        )

        st.subheader("3. Configuração")
        rows = st.slider("Linhas", min_value=3, max_value=9, value=5, key="path_rows")
        cols = st.slider("Colunas", min_value=3, max_value=9, value=5, key="path_cols")
        pattern = st.selectbox(
            "Padrão de obstáculos",
            options=["Sem obstáculos", "Barreira central", "Escada", "Zigue-zague"],
            key="path_obstacle_pattern",
        )
        obstacles = build_obstacles(rows, cols, pattern)

        st.divider()
        st.subheader("4. Controles de execução")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Preparar execução", width="stretch", key="prepare_path_execution"):
                _load_path_states(rows, cols, obstacles)
        with c2:
            if st.button("Próximo passo", width="stretch", disabled=not st.session_state.path_states, key="next_path_step"):
                if st.session_state.path_step_index < len(st.session_state.path_states) - 1:
                    st.session_state.path_step_index += 1
                    st.session_state.path_step_slider = st.session_state.path_step_index
        with c3:
            if st.button("Reiniciar", width="stretch", key="reset_path_execution"):
                _reset_path_states()

        if st.session_state.path_states:
            total_steps = len(st.session_state.path_states)
            if st.session_state.path_step_slider > total_steps - 1:
                st.session_state.path_step_slider = total_steps - 1

            def _sync_path_slider() -> None:
                st.session_state.path_step_index = st.session_state.path_step_slider

            st.slider(
                "Passo atual",
                min_value=0,
                max_value=total_steps - 1,
                key="path_step_slider",
                on_change=_sync_path_slider,
            )
        else:
            st.info("Clique em **Preparar execução** para iniciar a contagem de caminhos.")

        st.subheader("Fórmula combinatória")
        if pattern == "Sem obstáculos":
            formula_value = count_paths_without_obstacles_formula(rows, cols)
            st.latex(r"Caminhos = \binom{(linhas-1)+(colunas-1)}{linhas-1}")
            st.success(f"Sem obstáculos, a fórmula combinatória retorna {formula_value} caminhos.")
        else:
            st.warning(
                "Com obstáculos, a fórmula simples não se aplica diretamente. A programação dinâmica conta apenas caminhos válidos."
            )

    with right:
        active_states = st.session_state.path_states
        if not active_states:
            preview_states = generate_grid_path_states(rows, cols, obstacles)
            current_state = preview_states[0]
        else:
            current_state = active_states[st.session_state.path_step_index]

        st.subheader("Visualização do tabuleiro")
        fig = _render_path_grid(current_state)
        st.plotly_chart(fig, width="stretch")

        _render_path_metrics(current_state, pattern)
        render_step_box("Explicação do passo atual", current_state["message"])
        render_math_box("Conceito matemático mobilizado neste passo", current_state["math_concept"])

        st.subheader("Tabela de caminhos acumulados")
        st.dataframe(current_state["dp"], width="stretch")

        st.subheader("Reflexão didática")
        st.markdown(
            """
            1. Por que a célula atual depende apenas da célula acima e da célula à esquerda?
            2. Onde aparece o princípio aditivo da contagem?
            3. O que muda quando introduzimos obstáculos no tabuleiro?
            4. Por que o número de possibilidades cresce rapidamente quando aumentamos a grade?
            """
        )
