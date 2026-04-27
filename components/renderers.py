from __future__ import annotations

from typing import Any, Dict, List

import plotly.graph_objects as go



def _resolve_colors(state: Dict[str, Any]) -> List[str]:
    array = state["array"]
    colors: List[str] = ["#94a3b8"] * len(array)

    for index in state.get("sorted_indices", []):
        if 0 <= index < len(array):
            colors[index] = "#16a34a"

    active_color = "#2563eb"
    if state.get("color_mode") == "swap":
        active_color = "#dc2626"
    elif state.get("color_mode") == "sorted":
        active_color = "#16a34a"

    for index in state.get("active_indices", []):
        if 0 <= index < len(array):
            colors[index] = active_color

    return colors



def render_array_barchart(state: Dict[str, Any]) -> go.Figure:
    array = state["array"]
    positions = list(range(len(array)))
    colors = _resolve_colors(state)

    fig = go.Figure(
        data=[
            go.Bar(
                x=positions,
                y=array,
                text=array,
                textposition="outside",
                marker_color=colors,
                hovertemplate="Índice %{x}<br>Valor %{y}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=470,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Índice do vetor",
        yaxis_title="Valor",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(dtick=1, showgrid=False)
    fig.update_yaxes(showgrid=True, gridcolor="rgba(148, 163, 184, 0.25)")
    return fig



def render_binary_search_view(state: Dict[str, Any]) -> go.Figure:
    array = state["array"]
    positions = list(range(len(array)))

    colors: List[str] = []
    for idx in positions:
        if idx == state.get("found_index"):
            colors.append("#16a34a")
        elif idx in state.get("discarded_indices", []):
            colors.append("#cbd5e1")
        elif idx == state.get("mid"):
            colors.append("#dc2626")
        elif idx == state.get("left") or idx == state.get("right"):
            colors.append("#2563eb")
        else:
            colors.append("#94a3b8")

    customdata = []
    for idx, value in enumerate(array):
        role = []
        if idx == state.get("left"):
            role.append("início")
        if idx == state.get("mid"):
            role.append("meio")
        if idx == state.get("right"):
            role.append("fim")
        if idx == state.get("found_index"):
            role.append("encontrado")
        if idx in state.get("discarded_indices", []):
            role.append("descartado")
        customdata.append(", ".join(role) if role else "candidato")

    fig = go.Figure(
        data=[
            go.Bar(
                x=positions,
                y=[1] * len(array),
                text=[str(v) for v in array],
                textposition="inside",
                insidetextanchor="middle",
                marker_color=colors,
                customdata=customdata,
                hovertemplate="Índice %{x}<br>Valor %{text}<br>Status %{customdata}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=320,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Índice do vetor ordenado",
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
        uniformtext_minsize=12,
        uniformtext_mode="show",
    )
    fig.update_xaxes(dtick=1, showgrid=False)
    return fig



def render_matrix_view(state: Dict[str, Any]) -> go.Figure:
    matrix = state["matrix"]
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0

    z = []
    text_grid = []
    visited_set = set(state.get("visited_order", []))
    current = state.get("current")
    start = state.get("start")

    for r in range(rows):
        z_row = []
        text_row = []
        for c in range(cols):
            pos = (r, c)
            if pos == current:
                z_row.append(3)
            elif pos == start and state.get("mode") == "Vizinhança 4 direções":
                z_row.append(2.5)
            elif pos in visited_set:
                z_row.append(2)
            else:
                z_row.append(0)
            text_row.append(f"{matrix[r][c]}<br>({r},{c})")
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
                    [0.0, "#e2e8f0"],
                    [0.49, "#e2e8f0"],
                    [0.5, "#93c5fd"],
                    [0.74, "#93c5fd"],
                    [0.75, "#34d399"],
                    [0.89, "#34d399"],
                    [0.9, "#f97316"],
                    [1.0, "#f97316"],
                ],
                zmin=0,
                zmax=3,
                showscale=False,
                hovertemplate="%{text}<extra></extra>",
            )
        ]
    )

    fig.update_layout(
        height=max(360, rows * 90),
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis_title="Coluna",
        yaxis_title="Linha",
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_xaxes(dtick=1, side="top", showgrid=False)
    fig.update_yaxes(dtick=1, autorange="reversed", showgrid=False)
    return fig


def render_graph_bfs_view(state: Dict[str, Any]) -> go.Figure:
    positions = state["positions"]
    edges = state["edges"]
    visited = set(state.get("visited", []))
    visited_order = set(state.get("visited_order", []))
    current = state.get("current")
    inspected_neighbor = state.get("inspected_neighbor")
    active_edge = state.get("active_edge")
    start_node = state.get("start_node")

    fig = go.Figure()

    for edge in edges:
        source, target = edge
        x0, y0 = positions[source]
        x1, y1 = positions[target]
        is_active = active_edge == edge
        fig.add_trace(
            go.Scatter(
                x=[x0, x1],
                y=[y0, y1],
                mode="lines",
                line=dict(width=5 if is_active else 2, color="#dc2626" if is_active else "#cbd5e1"),
                hoverinfo="skip",
                showlegend=False,
            )
        )

    node_ids = sorted(positions.keys())
    x_values = [positions[node][0] for node in node_ids]
    y_values = [positions[node][1] for node in node_ids]
    colors: List[str] = []
    sizes: List[int] = []
    labels: List[str] = []

    for node in node_ids:
        if node == current:
            colors.append("#f97316")
            sizes.append(38)
        elif node == inspected_neighbor:
            colors.append("#dc2626")
            sizes.append(34)
        elif node in visited_order:
            colors.append("#16a34a")
            sizes.append(32)
        elif node in visited:
            colors.append("#2563eb")
            sizes.append(32)
        elif node == start_node:
            colors.append("#0891b2")
            sizes.append(32)
        else:
            colors.append("#94a3b8")
            sizes.append(28)
        labels.append(str(node))

    hover_text = []
    level = state.get("level", {})
    parent = state.get("parent", {})
    for node in node_ids:
        hover_text.append(
            f"Nó {node}<br>Nível: {level.get(node, '—')}<br>Pai: {parent.get(node, '—')}"
        )

    fig.add_trace(
        go.Scatter(
            x=x_values,
            y=y_values,
            mode="markers+text",
            text=labels,
            textposition="middle center",
            marker=dict(size=sizes, color=colors, line=dict(width=2, color="white")),
            textfont=dict(color="white", size=14),
            hovertext=hover_text,
            hovertemplate="%{hovertext}<extra></extra>",
            showlegend=False,
        )
    )

    fig.update_layout(
        height=520,
        margin=dict(l=20, r=20, t=30, b=20),
        xaxis=dict(visible=False),
        yaxis=dict(visible=False),
        plot_bgcolor="white",
        paper_bgcolor="white",
    )
    fig.update_yaxes(scaleanchor="x", scaleratio=1)
    return fig
