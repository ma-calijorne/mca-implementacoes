from __future__ import annotations

import math
import random
from collections import deque
from typing import Any, Dict, List, Set, Tuple

Adjacency = Dict[int, List[int]]
Position = Dict[int, Tuple[float, float]]


def build_sample_graph() -> tuple[Adjacency, Position]:
    adjacency: Adjacency = {
        0: [1, 2],
        1: [0, 3, 4],
        2: [0, 5],
        3: [1, 6],
        4: [1, 6],
        5: [2, 7],
        6: [3, 4, 8],
        7: [5, 8],
        8: [6, 7],
    }
    positions: Position = {
        0: (0.0, 2.0),
        1: (-1.6, 1.0),
        2: (1.6, 1.0),
        3: (-2.4, 0.0),
        4: (-0.8, 0.0),
        5: (1.6, 0.0),
        6: (-1.4, -1.0),
        7: (1.4, -1.0),
        8: (0.0, -2.0),
    }
    return adjacency, positions


def generate_random_graph(node_count: int, edge_probability: float, seed: int | None = None) -> tuple[Adjacency, Position]:
    rng = random.Random(seed)
    adjacency: Adjacency = {node: [] for node in range(node_count)}

    # Garante conectividade mínima com uma cadeia simples.
    for node in range(node_count - 1):
        adjacency[node].append(node + 1)
        adjacency[node + 1].append(node)

    for i in range(node_count):
        for j in range(i + 2, node_count):
            if rng.random() <= edge_probability:
                adjacency[i].append(j)
                adjacency[j].append(i)

    for node in adjacency:
        adjacency[node] = sorted(set(adjacency[node]))

    positions: Position = {}
    radius = 2.5
    for node in range(node_count):
        angle = 2 * math.pi * node / node_count
        positions[node] = (radius * math.cos(angle), radius * math.sin(angle))

    return adjacency, positions


def _edge_set(adjacency: Adjacency) -> Set[Tuple[int, int]]:
    edges: Set[Tuple[int, int]] = set()
    for source, neighbors in adjacency.items():
        for target in neighbors:
            edges.add(tuple(sorted((source, target))))
    return edges


def generate_bfs_states(adjacency: Adjacency, positions: Position, start_node: int) -> List[Dict[str, Any]]:
    if start_node not in adjacency:
        raise ValueError("O nó inicial não existe no grafo.")

    visited: Set[int] = {start_node}
    discovered_order: List[int] = [start_node]
    visited_order: List[int] = []
    queue: deque[int] = deque([start_node])
    parent: Dict[int, int | None] = {start_node: None}
    level: Dict[int, int] = {start_node: 0}
    states: List[Dict[str, Any]] = []
    edges = sorted(_edge_set(adjacency))

    def add_state(
        *,
        current: int | None,
        active_edge: Tuple[int, int] | None,
        inspected_neighbor: int | None,
        message: str,
        math_concept: str,
        event: str,
    ) -> None:
        states.append(
            {
                "adjacency": adjacency,
                "positions": positions,
                "edges": edges,
                "start_node": start_node,
                "current": current,
                "active_edge": active_edge,
                "inspected_neighbor": inspected_neighbor,
                "queue": list(queue),
                "visited": sorted(visited),
                "visited_order": list(visited_order),
                "discovered_order": list(discovered_order),
                "parent": dict(parent),
                "level": dict(level),
                "visited_count": len(visited_order),
                "discovered_count": len(visited),
                "event": event,
                "message": message,
                "math_concept": math_concept,
                "step_number": len(states) + 1,
                "total_steps": 0,
            }
        )

    add_state(
        current=None,
        active_edge=None,
        inspected_neighbor=None,
        event="inicializacao",
        message=f"Inicializamos a BFS pelo nó {start_node}. O nó entra na fila e passa a pertencer ao conjunto de descobertos.",
        math_concept="Conjuntos: o conjunto de nós descobertos começa com o nó inicial.",
    )

    while queue:
        current = queue.popleft()
        visited_order.append(current)
        add_state(
            current=current,
            active_edge=None,
            inspected_neighbor=None,
            event="visita",
            message=f"Removemos o nó {current} da fila. Agora ele será expandido, analisando seus vizinhos em ordem.",
            math_concept="Fila e relação de adjacência: BFS processa primeiro os nós descobertos há mais tempo.",
        )

        for neighbor in adjacency[current]:
            edge = tuple(sorted((current, neighbor)))
            if neighbor not in visited:
                visited.add(neighbor)
                discovered_order.append(neighbor)
                parent[neighbor] = current
                level[neighbor] = level[current] + 1
                queue.append(neighbor)
                add_state(
                    current=current,
                    active_edge=edge,
                    inspected_neighbor=neighbor,
                    event="descoberta",
                    message=f"O nó {neighbor} é vizinho de {current} e ainda não havia sido descoberto. Ele entra na fila no nível {level[neighbor]}.",
                    math_concept="Relações: a aresta define uma relação de adjacência. Pertinência: testamos se o vizinho já pertence ao conjunto de descobertos.",
                )
            else:
                add_state(
                    current=current,
                    active_edge=edge,
                    inspected_neighbor=neighbor,
                    event="ja_descoberto",
                    message=f"O nó {neighbor} também é vizinho de {current}, mas já pertence ao conjunto de descobertos. Por isso, não entra novamente na fila.",
                    math_concept="Conjuntos evitam repetição: o teste de pertinência impede visitas redundantes.",
                )

    add_state(
        current=None,
        active_edge=None,
        inspected_neighbor=None,
        event="fim",
        message="A fila ficou vazia. Todos os nós alcançáveis a partir do nó inicial foram descobertos pela BFS.",
        math_concept="Subconjunto alcançável: a BFS encontra o conjunto de vértices conectados ao nó inicial.",
    )

    total_steps = len(states)
    for index, state in enumerate(states, start=1):
        state["step_number"] = index
        state["total_steps"] = total_steps

    return states
