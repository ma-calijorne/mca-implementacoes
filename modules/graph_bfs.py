from __future__ import annotations

import streamlit as st

from algorithms.graph_algorithms import build_sample_graph, generate_bfs_states, generate_random_graph
from components.metrics import render_graph_metrics_panel
from components.panels import render_math_box, render_step_box
from components.renderers import render_graph_bfs_view


def _reset_states() -> None:
    st.session_state.graph_states = []
    st.session_state.graph_step_index = 0
    st.session_state.graph_step_slider = 0


def _load_states(adjacency: dict[int, list[int]], positions: dict[int, tuple[float, float]], start_node: int) -> None:
    st.session_state.graph_states = generate_bfs_states(adjacency, positions, start_node)
    st.session_state.graph_step_index = 0
    st.session_state.graph_step_slider = 0


def _get_graph_from_session_or_default() -> tuple[dict[int, list[int]], dict[int, tuple[float, float]]]:
    if "graph_current" not in st.session_state:
        adjacency, positions = build_sample_graph()
        st.session_state.graph_current = {"adjacency": adjacency, "positions": positions}
    graph_data = st.session_state.graph_current
    return graph_data["adjacency"], graph_data["positions"]


def render_graph_bfs_module() -> None:
    st.title("Módulo 4 • Grafos com BFS")
    st.caption(
        "Busca em largura em grafos, conectando conjuntos, relações de adjacência, fila, pertinência e níveis de visita."
    )

    left, right = st.columns([1.15, 1.85], gap="large")

    with left:
        st.subheader("1. O problema")
        st.write(
            "Grafos modelam redes, rotas, dependências, conexões sociais e estados de sistemas. A BFS percorre o grafo por camadas, visitando primeiro os vizinhos mais próximos do nó inicial."
        )

        st.subheader("2. Conceitos matemáticos envolvidos")
        st.markdown(
            """
            - **Conjuntos**: vértices, arestas, descobertos e visitados.
            - **Relações**: cada aresta representa uma relação de adjacência entre dois nós.
            - **Pertinência**: o algoritmo testa se um nó já pertence ao conjunto de descobertos.
            - **Funções**: a BFS associa cada nó descoberto a um nível e, quando aplicável, a um nó pai.
            - **Lógica proposicional**: decisões do tipo `se vizinho não foi descoberto, então adicionar à fila`.
            """
        )

        st.subheader("3. Configuração")
        graph_mode = st.radio(
            "Tipo de grafo",
            options=["Grafo didático fixo", "Grafo aleatório conectado"],
            key="graph_mode",
        )

        if graph_mode == "Grafo didático fixo":
            if st.button("Carregar grafo didático", width="stretch"):
                adjacency, positions = build_sample_graph()
                st.session_state.graph_current = {"adjacency": adjacency, "positions": positions}
                _reset_states()
        else:
            node_count = st.slider("Quantidade de nós", min_value=5, max_value=14, value=9)
            edge_probability = st.slider("Probabilidade de arestas extras", min_value=0.0, max_value=0.8, value=0.25, step=0.05)
            seed = st.number_input("Semente aleatória", min_value=0, max_value=9999, value=42, step=1)
            if st.button("Gerar grafo aleatório", width="stretch"):
                adjacency, positions = generate_random_graph(node_count, edge_probability, int(seed))
                st.session_state.graph_current = {"adjacency": adjacency, "positions": positions}
                _reset_states()

        adjacency, positions = _get_graph_from_session_or_default()
        node_options = sorted(adjacency.keys())
        start_node = st.selectbox("Nó inicial", options=node_options, index=0)

        st.divider()
        st.subheader("4. Controles de execução")
        c1, c2, c3 = st.columns(3)
        with c1:
            if st.button("Preparar execução", width="stretch"):
                _load_states(adjacency, positions, int(start_node))
        with c2:
            if st.button("Próximo passo", width="stretch", disabled=not st.session_state.graph_states):
                if st.session_state.graph_step_index < len(st.session_state.graph_states) - 1:
                    st.session_state.graph_step_index += 1
                    st.session_state.graph_step_slider = st.session_state.graph_step_index
        with c3:
            if st.button("Reiniciar", width="stretch"):
                _reset_states()

        if st.session_state.graph_states:
            total_steps = len(st.session_state.graph_states)
            if st.session_state.graph_step_slider > total_steps - 1:
                st.session_state.graph_step_slider = total_steps - 1

            def _sync_graph_slider() -> None:
                st.session_state.graph_step_index = st.session_state.graph_step_slider

            st.slider(
                "Passo atual",
                min_value=0,
                max_value=total_steps - 1,
                key="graph_step_slider",
                on_change=_sync_graph_slider,
            )
            st.session_state.graph_step_index = st.session_state.graph_step_slider
        else:
            st.info("Clique em **Preparar execução** para gerar os estados da BFS.")

    with right:
        active_states = st.session_state.graph_states
        if not active_states:
            current_state = generate_bfs_states(adjacency, positions, int(start_node))[0]
        else:
            current_state = active_states[st.session_state.graph_step_index]

        st.subheader("Visualização do grafo")
        fig = render_graph_bfs_view(current_state)
        st.plotly_chart(fig, width="stretch")

        render_graph_metrics_panel(
            node_count=len(current_state["adjacency"]),
            edge_count=len(current_state["edges"]),
            discovered_count=current_state["discovered_count"],
            visited_count=current_state["visited_count"],
            current=current_state.get("current"),
            step_number=current_state["step_number"],
            total_steps=current_state["total_steps"],
            queue=current_state.get("queue", []),
        )

        render_step_box("Explicação do passo atual", current_state["message"])
        render_math_box("Conceito matemático mobilizado neste passo", current_state["math_concept"])

        st.subheader("Ordem de descoberta e visita")
        c1, c2 = st.columns(2)
        c1.write("**Descobertos:**")
        c1.code(str(current_state.get("discovered_order", [])))
        c2.write("**Visitados/expandidos:**")
        c2.code(str(current_state.get("visited_order", [])))

        st.subheader("Reflexão didática")
        st.markdown(
            """
            1. Como o conjunto de descobertos evita que um nó seja inserido várias vezes na fila?
            2. Por que a BFS visita o grafo por níveis ou camadas?
            3. Como uma aresta representa formalmente uma relação entre dois vértices?
            4. Em quais problemas computacionais a ideia de menor número de arestas até um nó é útil?
            """
        )
