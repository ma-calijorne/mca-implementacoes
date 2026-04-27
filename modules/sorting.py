from __future__ import annotations

import random
from typing import List

import streamlit as st

from algorithms.sorting_algorithms import generate_sorting_states
from components.metrics import render_metrics_panel
from components.panels import render_math_box, render_step_box
from components.renderers import render_array_barchart


DEFAULT_VECTOR = [7, 3, 9, 2, 8, 1, 5, 4, 6]


def _parse_manual_array(raw_text: str) -> List[int]:
    cleaned = raw_text.replace(";", ",").replace(" ", "")
    if not cleaned:
        raise ValueError("Informe pelo menos um valor.")
    parts = [part for part in cleaned.split(",") if part != ""]
    if not parts:
        raise ValueError("Não foi possível interpretar os valores informados.")
    return [int(part) for part in parts]


def _reset_states() -> None:
    st.session_state.sort_states = []
    st.session_state.sort_step_index = 0


def _load_states(array: List[int], algorithm_name: str) -> None:
    st.session_state.sort_states = generate_sorting_states(array, algorithm_name)
    st.session_state.sort_step_index = 0



def render_sorting_module() -> None:
    st.title("Módulo 1 • Ordenação Visual")
    st.caption("Bubble Sort e Selection Sort com execução passo a passo e conexão explícita com a matemática estudada.")

    left, right = st.columns([1.1, 1.9], gap="large")

    with left:
        st.subheader("1. O problema")
        st.write(
            "Ordenar uma coleção de valores é uma tarefa central na computação. Aqui, o aluno observa como cada comparação e cada troca dependem de relações de ordem e decisões lógicas."
        )

        st.subheader("2. Conceitos matemáticos envolvidos")
        st.markdown(
            """
            - **Relações**: comparar elementos usando >, < e =.
            - **Lógica proposicional**: decidir se há ou não troca.
            - **Funções**: transformar entrada desordenada em saída ordenada.
            - **Princípios de contagem**: medir passos, comparações e trocas.
            """
        )

        st.subheader("3. Configuração")
        algorithm_name = st.selectbox(
            "Escolha o algoritmo",
            options=["Bubble Sort", "Selection Sort"],
        )

        input_mode = st.radio(
            "Forma de entrada",
            options=["Vetor aleatório", "Entrada manual"],
        )

        if input_mode == "Vetor aleatório":
            vector_size = st.slider("Quantidade de elementos", min_value=5, max_value=18, value=9)
            min_value, max_value = st.slider("Faixa dos valores", min_value=1, max_value=100, value=(1, 30))
            if st.button("Gerar novo vetor", width="stretch"):
                generated = random.sample(range(min_value, max_value + 1), k=vector_size)
                _load_states(generated, algorithm_name)
            current_array = st.session_state.sort_states[0]["array"] if st.session_state.sort_states else DEFAULT_VECTOR[:vector_size]
        else:
            raw_text = st.text_area(
                "Digite os valores separados por vírgula",
                value=",".join(map(str, DEFAULT_VECTOR)),
                help="Exemplo: 7,3,9,2,8,1,5",
            )
            if st.button("Carregar vetor manual", width="stretch"):
                try:
                    manual_array = _parse_manual_array(raw_text)
                    _load_states(manual_array, algorithm_name)
                except ValueError as exc:
                    st.error(str(exc))
            if st.session_state.sort_states:
                current_array = st.session_state.sort_states[0]["array"]
            else:
                try:
                    current_array = _parse_manual_array(raw_text)
                except ValueError:
                    current_array = DEFAULT_VECTOR

        st.divider()
        st.subheader("4. Controles de execução")

        control_col1, control_col2, control_col3 = st.columns(3)
        with control_col1:
            if st.button("Preparar execução", width="stretch"):
                _load_states(current_array, algorithm_name)
        with control_col2:
            if st.button("Próximo passo", width="stretch", disabled=not st.session_state.sort_states):
                if st.session_state.sort_step_index < len(st.session_state.sort_states) - 1:
                    st.session_state.sort_step_index += 1
        with control_col3:
            if st.button("Reiniciar", width="stretch"):
                _reset_states()

        if st.session_state.sort_states:
            total_steps = len(st.session_state.sort_states)
            st.session_state.sort_step_index = st.slider(
                "Passo atual",
                min_value=0,
                max_value=total_steps - 1,
                value=st.session_state.sort_step_index,
            )
        else:
            st.info("Clique em **Preparar execução** para gerar os estados do algoritmo.")

    with right:
        active_states = st.session_state.sort_states
        if not active_states:
            preview_states = generate_sorting_states(current_array, algorithm_name)
            current_state = preview_states[0]
        else:
            current_state = active_states[st.session_state.sort_step_index]

        st.subheader("Visualização do algoritmo")
        fig = render_array_barchart(current_state)
        st.plotly_chart(fig, width="stretch")

        render_metrics_panel(
            comparisons=current_state["comparisons"],
            swaps=current_state["swaps"],
            step_number=current_state["step_number"],
            total_steps=current_state["total_steps"],
        )

        render_step_box(
            title="Explicação do passo atual",
            message=current_state["message"],
        )

        render_math_box(
            title="Conceito matemático mobilizado neste passo",
            message=current_state["math_concept"],
        )

        st.subheader("Reflexão didática")
        st.markdown(
            """
            1. O algoritmo está usando apenas comparação, ou está fazendo algo mais sofisticado?
            2. O que acontece com a quantidade de comparações quando o vetor cresce?
            3. Em qual ponto a lógica condicional determina a troca entre dois elementos?
            4. Como a noção de ordem aparece formalmente no algoritmo?
            """
        )
