import streamlit as st



def render_metrics_panel(comparisons: int, swaps: int, step_number: int, total_steps: int) -> None:
    st.subheader("Métricas da execução")
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Comparações", comparisons)
    c2.metric("Trocas", swaps)
    c3.metric("Passo atual", step_number)
    c4.metric("Total de passos", total_steps)



def render_search_metrics_panel(
    comparisons: int,
    left: int,
    right: int,
    mid: int | None,
    step_number: int,
    total_steps: int,
    found_index: int | None,
) -> None:
    st.subheader("Métricas da execução")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Comparações", comparisons)
    c2.metric("Início", left if left >= 0 else "—")
    c3.metric("Meio", mid if mid is not None else "—")
    c4.metric("Fim", right if right >= 0 else "—")
    c5.metric("Encontrado", found_index if found_index is not None else "Não")
    c6.metric("Passo", f"{step_number}/{total_steps}")



def render_matrix_metrics_panel(
    rows: int,
    cols: int,
    visited_count: int,
    current: tuple[int, int] | None,
    step_number: int,
    total_steps: int,
    mode: str,
    queue: list[tuple[int, int]] | None = None,
) -> None:
    st.subheader("Métricas da execução")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Linhas", rows)
    c2.metric("Colunas", cols)
    c3.metric("Visitadas", visited_count)
    c4.metric("Atual", str(current) if current is not None else "—")
    c5.metric("Modo", mode)
    c6.metric("Passo", f"{step_number}/{total_steps}")
    if queue is not None:
        st.caption(f"Fila de expansão atual: {queue}")


def render_graph_metrics_panel(
    node_count: int,
    edge_count: int,
    discovered_count: int,
    visited_count: int,
    current: int | None,
    step_number: int,
    total_steps: int,
    queue: list[int],
) -> None:
    st.subheader("Métricas da execução")
    c1, c2, c3, c4, c5, c6 = st.columns(6)
    c1.metric("Nós", node_count)
    c2.metric("Arestas", edge_count)
    c3.metric("Descobertos", discovered_count)
    c4.metric("Visitados", visited_count)
    c5.metric("Atual", current if current is not None else "—")
    c6.metric("Passo", f"{step_number}/{total_steps}")
    st.caption(f"Fila BFS atual: {queue if queue else 'vazia'}")
