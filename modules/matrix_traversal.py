from __future__ import annotations

import random
from typing import List

import streamlit as st

from algorithms.matrix_algorithms import generate_matrix_traversal_states
from components.metrics import render_matrix_metrics_panel
from components.panels import render_math_box, render_step_box
from components.renderers import render_matrix_view


DEFAULT_MATRIX = [
    [1, 2, 3, 4],
    [5, 6, 7, 8],
    [9, 10, 11, 12],
]



def _parse_manual_matrix(raw_text: str) -> List[List[int]]:
    rows_raw = [line.strip() for line in raw_text.strip().splitlines() if line.strip()]
    if not rows_raw:
        raise ValueError("Informe pelo menos uma linha de valores.")

    matrix: List[List[int]] = []
    expected_cols = None
    for line in rows_raw:
        cleaned = line.replace(";", ",")
        values = [int(part.strip()) for part in cleaned.split(",") if part.strip()]
        if not values:
            raise ValueError("Cada linha deve possuir pelo menos um número.")
        if expected_cols is None:
            expected_cols = len(values)
        elif len(values) != expected_cols:
            raise ValueError("Todas as linhas devem ter a mesma quantidade de colunas.")
        matrix.append(values)
    return matrix



def _generate_random_matrix(rows: int, cols: int, min_value: int, max_value: int) -> List[List[int]]:
    return [[random.randint(min_value, max_value) for _ in range(cols)] for _ in range(rows)]



def _reset_states() -> None:
    st.session_state.matrix_states = []
    st.session_state.matrix_step_index = 0
    st.session_state.matrix_step_slider = 0



def _load_states(matrix: List[List[int]], mode: str, start: tuple[int, int] | None = None) -> None:
    st.session_state.matrix_states = generate_matrix_traversal_states(matrix, mode, start)
    st.session_state.matrix_step_index = 0
    st.session_state.matrix_step_slider = 0



def render_matrix_traversal_module() -> None:
    st.title("Módulo 3 • Percurso em Matrizes")
    st.caption(
        "Varreduras bidimensionais com destaque para pares ordenados, produto cartesiano, contagem e relações de vizinhança."
    )

    left, right = st.columns([1.15, 1.85], gap="large")

    with left:
        st.subheader("1. O problema")
        st.write(
            "Matrizes aparecem em imagens, tabuleiros, mapas, dados tabulares e problemas espaciais. Neste módulo, o aluno observa como uma matriz pode ser percorrida segundo regras diferentes."
        )

        st.subheader("2. Conceitos matemáticos envolvidos")
        st.markdown(
            """
            - **Conjuntos e produto cartesiano**: cada célula é identificada por um par ordenado `(linha, coluna)`.
            - **Funções**: o algoritmo define uma regra de visita para transformar uma matriz em uma sequência ordenada de posições.
            - **Relações espaciais**: vizinhança, diagonal e adjacência entre células.
            - **Princípios de contagem**: medir quantas células foram visitadas e em que ordem.
            """
        )

        st.subheader("3. Configuração")
        mode = st.selectbox(
            "Escolha o modo de percurso",
            options=["Linha por linha", "Coluna por coluna", "Diagonal principal", "Vizinhança 4 direções"],
        )

        input_mode = st.radio(
            "Forma de entrada",
            options=["Matriz aleatória", "Entrada manual"],
            key="matrix_input_mode",
        )

        if input_mode == "Matriz aleatória":
            rows = st.slider("Linhas", min_value=2, max_value=7, value=3)
            cols = st.slider("Colunas", min_value=2, max_value=7, value=4)
            min_value, max_value = st.slider("Faixa dos valores", min_value=0, max_value=99, value=(0, 20))
            if st.button("Gerar nova matriz", width="stretch"):
                st.session_state.matrix_current = _generate_random_matrix(rows, cols, min_value, max_value)
            current_matrix = st.session_state.get("matrix_current", _generate_random_matrix(rows, cols, min_value, max_value))
            if len(current_matrix) != rows or len(current_matrix[0]) != cols:
                current_matrix = _generate_random_matrix(rows, cols, min_value, max_value)
                st.session_state.matrix_current = current_matrix
        else:
            raw_text = st.text_area(
                "Digite a matriz (uma linha por linha, valores separados por vírgula)",
                value="1,2,3,4\n5,6,7,8\n9,10,11,12",
                help="Exemplo:\n1,2,3\n4,5,6\n7,8,9",
                height=140,
            )
            if st.button("Carregar matriz manual", width="stretch"):
                try:
                    st.session_state.matrix_current = _parse_manual_matrix(raw_text)
                except ValueError as exc:
                    st.error(str(exc))
            if "matrix_current" in st.session_state:
                current_matrix = st.session_state.matrix_current
            else:
                try:
                    current_matrix = _parse_manual_matrix(raw_text)
                except ValueError:
                    current_matrix = DEFAULT_MATRIX

        rows = len(current_matrix)
        cols = len(current_matrix[0])

        start_pos = None
        if mode == "Vizinhança 4 direções":
            st.markdown("**Ponto inicial da exploração**")
            start_row = st.number_input("Linha inicial", min_value=0, max_value=rows - 1, value=0, step=1)
            start_col = st.number_input("Coluna inicial", min_value=0, max_value=cols - 1, value=0, step=1)
            start_pos = (int(start_row), int(start_col))

        st.divider()
        st.subheader("4. Controles de execução")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Preparar execução", width="stretch"):
                _load_states(current_matrix, mode, start_pos)
        with c2:
            if st.button("Próximo passo", width="stretch", disabled=not st.session_state.matrix_states):
                if st.session_state.matrix_step_index < len(st.session_state.matrix_states) - 1:
                    st.session_state.matrix_step_index += 1
                    st.session_state.matrix_step_slider = st.session_state.matrix_step_index
        with c3:
            if st.button("Reiniciar", width="stretch"):
                _reset_states()

        if st.session_state.matrix_states:
            total_steps = len(st.session_state.matrix_states)
            if st.session_state.matrix_step_slider > total_steps - 1:
                st.session_state.matrix_step_slider = total_steps - 1

            def _sync_matrix_slider() -> None:
                st.session_state.matrix_step_index = st.session_state.matrix_step_slider

            st.slider(
                "Passo atual",
                min_value=0,
                max_value=total_steps - 1,
                key="matrix_step_slider",
                on_change=_sync_matrix_slider,
            )
            st.session_state.matrix_step_index = st.session_state.matrix_step_slider
        else:
            st.info("Clique em **Preparar execução** para gerar os estados do percurso na matriz.")

    with right:
        active_states = st.session_state.matrix_states
        if not active_states:
            preview_states = generate_matrix_traversal_states(current_matrix, mode, start_pos)
            current_state = preview_states[0]
        else:
            current_state = active_states[st.session_state.matrix_step_index]

        st.subheader("Visualização da matriz")
        fig = render_matrix_view(current_state)
        st.plotly_chart(fig, width="stretch")

        render_matrix_metrics_panel(
            rows=current_state["rows"],
            cols=current_state["cols"],
            visited_count=current_state["visited_count"],
            current=current_state.get("current"),
            step_number=current_state["step_number"],
            total_steps=current_state["total_steps"],
            mode=current_state["mode"],
            queue=current_state.get("queue"),
        )

        render_step_box("Explicação do passo atual", current_state["message"])
        render_math_box("Conceito matemático mobilizado neste passo", current_state["math_concept"])

        st.subheader("Reflexão didática")
        st.markdown(
            """
            1. Como um par ordenado `(linha, coluna)` identifica formalmente uma célula?
            2. O que muda quando o algoritmo percorre por linhas, colunas ou diagonal?
            3. Por que a vizinhança 4 direções pode ser vista como uma relação entre células?
            4. Como a ordem do percurso altera a sequência de saída, mesmo sem mudar a matriz original?
            """
        )
