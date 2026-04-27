from __future__ import annotations

from math import comb
from typing import Any, Dict, List, Sequence, Set, Tuple

Cell = Tuple[int, int]
State = Dict[str, Any]


def build_obstacles(rows: int, cols: int, pattern: str) -> Set[Cell]:
    """Cria padrões didáticos de obstáculos sem bloquear início e fim."""
    obstacles: Set[Cell] = set()
    start = (0, 0)
    end = (rows - 1, cols - 1)

    if pattern == "Sem obstáculos":
        return obstacles

    if pattern == "Barreira central":
        middle_col = cols // 2
        gap_row = rows // 2
        for r in range(rows):
            cell = (r, middle_col)
            if cell not in {start, end, (gap_row, middle_col)}:
                obstacles.add(cell)

    elif pattern == "Escada":
        limit = min(rows, cols)
        for i in range(1, limit - 1):
            if i % 2 == 1:
                cell = (i, i - 1)
                if cell not in {start, end}:
                    obstacles.add(cell)

    elif pattern == "Zigue-zague":
        for r in range(1, rows - 1):
            c = 1 if r % 2 else cols - 2
            if 0 <= c < cols:
                cell = (r, c)
                if cell not in {start, end}:
                    obstacles.add(cell)

    return obstacles


def count_paths_without_obstacles_formula(rows: int, cols: int) -> int:
    """Conta caminhos quando só são permitidos movimentos para direita e baixo."""
    if rows <= 0 or cols <= 0:
        return 0
    down_moves = rows - 1
    right_moves = cols - 1
    return comb(down_moves + right_moves, down_moves)


def _make_state(
    *,
    rows: int,
    cols: int,
    obstacles: Set[Cell],
    dp: List[List[int]],
    current: Cell | None,
    processed: Sequence[Cell],
    message: str,
    math_concept: str,
    step_number: int,
    total_steps: int,
) -> State:
    return {
        "rows": rows,
        "cols": cols,
        "obstacles": sorted(obstacles),
        "dp": [row[:] for row in dp],
        "current": current,
        "processed": list(processed),
        "start": (0, 0),
        "end": (rows - 1, cols - 1),
        "message": message,
        "math_concept": math_concept,
        "step_number": step_number,
        "total_steps": total_steps,
        "path_count": dp[rows - 1][cols - 1] if rows > 0 and cols > 0 else 0,
    }


def generate_grid_path_states(rows: int, cols: int, obstacles: Set[Cell]) -> List[State]:
    """
    Gera estados intermediários para contagem de caminhos em tabuleiro.

    Regra: o robô parte de (0, 0), chega em (rows-1, cols-1) e pode mover
    apenas para a direita ou para baixo. A contagem é feita por programação
    dinâmica: caminhos[r][c] = caminhos[r-1][c] + caminhos[r][c-1].
    """
    if rows <= 0 or cols <= 0:
        return []

    start = (0, 0)
    end = (rows - 1, cols - 1)
    sanitized_obstacles = {cell for cell in obstacles if cell not in {start, end}}

    dp = [[0 for _ in range(cols)] for _ in range(rows)]
    processed: List[Cell] = []
    states: List[State] = []

    total_steps = rows * cols + 1
    states.append(
        _make_state(
            rows=rows,
            cols=cols,
            obstacles=sanitized_obstacles,
            dp=dp,
            current=None,
            processed=processed,
            message=(
                "Início da contagem. Cada célula armazenará quantos caminhos diferentes chegam até ela. "
                "Movimentos permitidos: apenas direita e baixo."
            ),
            math_concept=(
                "Espaço de possibilidades: cada caminho é uma sequência finita de decisões entre mover para a direita ou para baixo."
            ),
            step_number=1,
            total_steps=total_steps,
        )
    )

    step = 2
    for r in range(rows):
        for c in range(cols):
            cell = (r, c)
            processed.append(cell)

            if cell in sanitized_obstacles:
                dp[r][c] = 0
                message = f"A célula ({r}, {c}) é um obstáculo. Portanto, nenhum caminho pode passar por ela."
                math_concept = "Conjunto de restrições: obstáculos removem elementos do espaço de caminhos válidos."

            elif cell == start:
                dp[r][c] = 1
                message = "A célula inicial (0, 0) recebe valor 1, pois existe exatamente uma forma de estar no início."
                math_concept = "Caso base: a contagem começa com uma condição inicial definida."

            else:
                from_top = dp[r - 1][c] if r > 0 else 0
                from_left = dp[r][c - 1] if c > 0 else 0
                dp[r][c] = from_top + from_left
                message = (
                    f"Na célula ({r}, {c}), somamos os caminhos que chegam de cima ({from_top}) "
                    f"com os que chegam da esquerda ({from_left}). Total: {dp[r][c]}."
                )
                math_concept = (
                    "Princípio aditivo da contagem: quando alternativas são mutuamente separadas, somamos as possibilidades."
                )

            states.append(
                _make_state(
                    rows=rows,
                    cols=cols,
                    obstacles=sanitized_obstacles,
                    dp=dp,
                    current=cell,
                    processed=processed,
                    message=message,
                    math_concept=math_concept,
                    step_number=step,
                    total_steps=total_steps,
                )
            )
            step += 1

    return states
