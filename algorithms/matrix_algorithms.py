from __future__ import annotations

from collections import deque
from typing import Any, Dict, List, Tuple


MatrixState = Dict[str, Any]


Position = Tuple[int, int]


def _build_state(
    matrix: List[List[int]],
    visited_order: List[Position],
    current: Position | None,
    message: str,
    math_concept: str,
    mode: str,
    extra: Dict[str, Any] | None = None,
) -> MatrixState:
    state: MatrixState = {
        "matrix": [row.copy() for row in matrix],
        "visited_order": visited_order.copy(),
        "current": current,
        "visited_count": len(visited_order),
        "message": message,
        "math_concept": math_concept,
        "mode": mode,
    }
    if extra:
        state.update(extra)
    return state



def _finalize_states(states: List[MatrixState]) -> List[MatrixState]:
    total_steps = len(states)
    for index, state in enumerate(states, start=1):
        state["step_number"] = index
        state["total_steps"] = total_steps
    return states



def _row_major_positions(rows: int, cols: int) -> List[Position]:
    return [(r, c) for r in range(rows) for c in range(cols)]



def _column_major_positions(rows: int, cols: int) -> List[Position]:
    return [(r, c) for c in range(cols) for r in range(rows)]



def _main_diagonal_positions(rows: int, cols: int) -> List[Position]:
    return [(i, i) for i in range(min(rows, cols))]



def _neighbors_4(rows: int, cols: int, pos: Position) -> List[Position]:
    r, c = pos
    candidates = [(r - 1, c), (r, c + 1), (r + 1, c), (r, c - 1)]
    return [(nr, nc) for nr, nc in candidates if 0 <= nr < rows and 0 <= nc < cols]



def _positions_to_states(
    matrix: List[List[int]],
    positions: List[Position],
    mode: str,
    intro_message: str,
    intro_math: str,
) -> List[MatrixState]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    states: List[MatrixState] = [
        _build_state(
            matrix=matrix,
            visited_order=[],
            current=None,
            message=intro_message,
            math_concept=intro_math,
            mode=mode,
            extra={"rows": rows, "cols": cols},
        )
    ]

    visited: List[Position] = []
    for r, c in positions:
        visited.append((r, c))
        states.append(
            _build_state(
                matrix=matrix,
                visited_order=visited,
                current=(r, c),
                message=(
                    f"Visitando a célula ({r}, {c}), que contém o valor {matrix[r][c]}. "
                    f"Esta posição corresponde a um par ordenado da matriz."
                ),
                math_concept=(
                    "Produto cartesiano e pares ordenados: cada célula da matriz pode ser identificada por (linha, coluna)."
                ),
                mode=mode,
                extra={"rows": rows, "cols": cols},
            )
        )

    states.append(
        _build_state(
            matrix=matrix,
            visited_order=visited,
            current=None,
            message="Percurso concluído. Todas as posições previstas para este modo de varredura foram visitadas.",
            math_concept="Contagem e função de percurso: o algoritmo definiu uma ordem formal para percorrer posições da matriz.",
            mode=mode,
            extra={"rows": rows, "cols": cols},
        )
    )
    return _finalize_states(states)



def _bfs_neighbor_states(matrix: List[List[int]], start: Position) -> List[MatrixState]:
    rows = len(matrix)
    cols = len(matrix[0]) if rows else 0
    visited: set[Position] = {start}
    order: List[Position] = []
    queue: deque[Position] = deque([start])
    states: List[MatrixState] = [
        _build_state(
            matrix=matrix,
            visited_order=[],
            current=None,
            message=(
                f"Estado inicial da exploração por vizinhança. O ponto de partida é {start}. "
                "A visita será feita em largura usando vizinhos ortogonais."
            ),
            math_concept=(
                "Relações espaciais: cada célula se conecta a vizinhos pelas quatro direções básicas."
            ),
            mode="Vizinhança 4 direções",
            extra={"rows": rows, "cols": cols, "queue": list(queue), "start": start},
        )
    ]

    while queue:
        current = queue.popleft()
        order.append(current)
        r, c = current
        neighbors = _neighbors_4(rows, cols, current)
        new_neighbors: List[Position] = []
        for nb in neighbors:
            if nb not in visited:
                visited.add(nb)
                queue.append(nb)
                new_neighbors.append(nb)

        states.append(
            _build_state(
                matrix=matrix,
                visited_order=order,
                current=current,
                message=(
                    f"A célula atual é ({r}, {c}), com valor {matrix[r][c]}. "
                    f"Seus vizinhos válidos são {neighbors}. Novos vizinhos inseridos na fila: {new_neighbors or 'nenhum'}."
                ),
                math_concept=(
                    "Relação de adjacência e contagem: o algoritmo identifica células conectadas e expande a fronteira de visita."
                ),
                mode="Vizinhança 4 direções",
                extra={"rows": rows, "cols": cols, "queue": list(queue), "start": start},
            )
        )

    states.append(
        _build_state(
            matrix=matrix,
            visited_order=order,
            current=None,
            message="Exploração concluída. Todas as células alcançáveis pela relação de vizinhança foram visitadas.",
            math_concept=(
                "Fecho por conectividade: a repetição da relação de adjacência permite percorrer toda a matriz componente a componente."
            ),
            mode="Vizinhança 4 direções",
            extra={"rows": rows, "cols": cols, "queue": [], "start": start},
        )
    )
    return _finalize_states(states)



def generate_matrix_traversal_states(
    matrix: List[List[int]],
    mode: str,
    start: Position | None = None,
) -> List[MatrixState]:
    if not matrix or not matrix[0]:
        raise ValueError("A matriz não pode ser vazia.")

    rows = len(matrix)
    cols = len(matrix[0])
    if any(len(row) != cols for row in matrix):
        raise ValueError("Todas as linhas da matriz devem ter o mesmo tamanho.")

    if mode == "Linha por linha":
        return _positions_to_states(
            matrix,
            _row_major_positions(rows, cols),
            mode,
            intro_message="Estado inicial da matriz antes da varredura linha por linha.",
            intro_math="Função de mapeamento: o algoritmo percorrerá cada linha e, dentro dela, cada coluna.",
        )
    if mode == "Coluna por coluna":
        return _positions_to_states(
            matrix,
            _column_major_positions(rows, cols),
            mode,
            intro_message="Estado inicial da matriz antes da varredura coluna por coluna.",
            intro_math="Mudança de ordem de iteração: agora o percurso prioriza colunas antes de linhas.",
        )
    if mode == "Diagonal principal":
        return _positions_to_states(
            matrix,
            _main_diagonal_positions(rows, cols),
            mode,
            intro_message="Estado inicial da matriz antes do percurso pela diagonal principal.",
            intro_math="Restrição do domínio: somente pares ordenados do tipo (i, i) pertencem a este percurso.",
        )
    if mode == "Vizinhança 4 direções":
        start = start or (0, 0)
        if not (0 <= start[0] < rows and 0 <= start[1] < cols):
            raise ValueError("A posição inicial está fora dos limites da matriz.")
        return _bfs_neighbor_states(matrix, start)

    raise ValueError(f"Modo de percurso não suportado: {mode}")
