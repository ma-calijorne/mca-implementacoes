from __future__ import annotations

import random
from typing import List

import streamlit as st

from algorithms.search_algorithms import generate_binary_search_states
from components.metrics import render_search_metrics_panel
from components.panels import render_math_box, render_step_box
from components.renderers import render_binary_search_view


DEFAULT_SORTED_VECTOR = [3, 5, 8, 12, 15, 19, 23, 27, 31, 36]



def _parse_manual_array(raw_text: str) -> List[int]:
    cleaned = raw_text.replace(";", ",").replace(" ", "")
    if not cleaned:
        raise ValueError("Informe pelo menos um valor.")
    parts = [part for part in cleaned.split(",") if part != ""]
    values = [int(part) for part in parts]
    if not values:
        raise ValueError("Não foi possível interpretar os valores informados.")
    return sorted(set(values))



def _reset_states() -> None:
    st.session_state.binary_states = []
    st.session_state.binary_step_index = 0
    st.session_state.binary_step_slider = 0



def _load_states(array: List[int], target: int) -> None:
    st.session_state.binary_states = generate_binary_search_states(array, target)
    st.session_state.binary_step_index = 0
    st.session_state.binary_step_slider = 0



def render_binary_search_module() -> None:
    st.title("Módulo 2 • Busca Binária")
    st.caption(
        "Busca em vetor ordenado com divisão do intervalo, descarte visual de metades e conexão explícita com lógica, funções e relações."
    )

    left, right = st.columns([1.1, 1.9], gap="large")

    with left:
        st.subheader("1. O problema")
        st.write(
            "A busca binária localiza um valor em um vetor ordenado reduzindo repetidamente o espaço de busca pela metade. Isso mostra, de forma visual, como uma decisão lógica pode eliminar muitos casos de uma vez."
        )

        st.subheader("2. Conceitos matemáticos envolvidos")
        st.markdown(
            """
            - **Lógica proposicional**: decidir se o alvo é igual, menor ou maior que o elemento central.
            - **Relações**: usar `<`, `>` e `=` para comparar valores.
            - **Funções**: a busca transforma entrada + alvo em índice encontrado ou ausência.
            - **Conjuntos e intervalos**: o algoritmo mantém apenas o subconjunto ainda possível.
            """
        )

        st.subheader("3. Configuração")
        input_mode = st.radio(
            "Forma de entrada",
            options=["Vetor aleatório ordenado", "Entrada manual"],
            key="binary_input_mode",
        )

        if input_mode == "Vetor aleatório ordenado":
            vector_size = st.slider(
                "Quantidade de elementos", min_value=5, max_value=20, value=10, key="binary_size"
            )
            min_value, max_value = st.slider(
                "Faixa dos valores", min_value=1, max_value=150, value=(1, 60), key="binary_range"
            )
            if st.button("Gerar novo vetor ordenado", width="stretch"):
                generated = sorted(random.sample(range(min_value, max_value + 1), k=vector_size))
                st.session_state.binary_current_array = generated
            current_array = st.session_state.get("binary_current_array", DEFAULT_SORTED_VECTOR[:vector_size])
            current_array = sorted(current_array)[:vector_size] if len(current_array) >= vector_size else sorted(current_array)
        else:
            raw_text = st.text_area(
                "Digite os valores separados por vírgula",
                value=",".join(map(str, DEFAULT_SORTED_VECTOR)),
                help="A busca binária exige vetor ordenado. O app ordena automaticamente a entrada e remove duplicados.",
            )
            if st.button("Carregar vetor manual", width="stretch"):
                try:
                    manual_array = _parse_manual_array(raw_text)
                    st.session_state.binary_current_array = manual_array
                except ValueError as exc:
                    st.error(str(exc))

            if "binary_current_array" in st.session_state:
                current_array = st.session_state.binary_current_array
            else:
                try:
                    current_array = _parse_manual_array(raw_text)
                except ValueError:
                    current_array = DEFAULT_SORTED_VECTOR

        target_default = current_array[len(current_array) // 2] if current_array else 10
        target = st.number_input("Valor a buscar", value=int(target_default), step=1)

        st.divider()
        st.subheader("4. Controles de execução")
        control_col1, control_col2, control_col3 = st.columns(3)
        with control_col1:
            if st.button("Preparar execução", width="stretch"):
                _load_states(current_array, int(target))
        with control_col2:
            if st.button(
                "Próximo passo",
                width="stretch",
                disabled=not st.session_state.binary_states,
            ):
                if st.session_state.binary_step_index < len(st.session_state.binary_states) - 1:
                    st.session_state.binary_step_index += 1
                    st.session_state.binary_step_slider = st.session_state.binary_step_index
        with control_col3:
            if st.button("Reiniciar", width="stretch"):
                _reset_states()

        if st.session_state.binary_states:
            total_steps = len(st.session_state.binary_states)
            if st.session_state.binary_step_slider > total_steps - 1:
                st.session_state.binary_step_slider = total_steps - 1

            def _sync_binary_slider() -> None:
                st.session_state.binary_step_index = st.session_state.binary_step_slider

            st.slider(
                "Passo atual",
                min_value=0,
                max_value=total_steps - 1,
                key="binary_step_slider",
                on_change=_sync_binary_slider,
            )
            st.session_state.binary_step_index = st.session_state.binary_step_slider
        else:
            st.info("Clique em **Preparar execução** para gerar os estados da busca binária.")

    with right:
        active_states = st.session_state.binary_states
        if not active_states:
            preview_states = generate_binary_search_states(current_array, int(target))
            current_state = preview_states[0]
        else:
            current_state = active_states[st.session_state.binary_step_index]

        st.subheader("Visualização do algoritmo")
        fig = render_binary_search_view(current_state)
        st.plotly_chart(fig, width="stretch")

        render_search_metrics_panel(
            comparisons=current_state["comparisons"],
            left=current_state["left"],
            right=current_state["right"],
            mid=current_state["mid"],
            step_number=current_state["step_number"],
            total_steps=current_state["total_steps"],
            found_index=current_state["found_index"],
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
            1. Por que a busca binária exige que o vetor esteja ordenado?
            2. Em que momento a lógica elimina metade dos casos possíveis?
            3. O que significa dizer que o intervalo de busca é um subconjunto do vetor original?
            4. Por que esse algoritmo tende a ser mais eficiente que a busca sequencial em vetores grandes?
            """
        )
