from __future__ import annotations

from typing import Any, Dict, List


State = Dict[str, Any]


HIGHLIGHT_COLORS = {
    "default": "#94a3b8",
    "active": "#2563eb",
    "swap": "#dc2626",
    "sorted": "#16a34a",
}



def _build_state(
    array: List[int],
    active_indices: List[int],
    sorted_indices: List[int],
    comparisons: int,
    swaps: int,
    message: str,
    math_concept: str,
    color_mode: str = "active",
) -> State:
    return {
        "array": array.copy(),
        "active_indices": active_indices.copy(),
        "sorted_indices": sorted_indices.copy(),
        "comparisons": comparisons,
        "swaps": swaps,
        "message": message,
        "math_concept": math_concept,
        "color_mode": color_mode,
    }



def _finalize_states(states: List[State]) -> List[State]:
    total_steps = len(states)
    for index, state in enumerate(states, start=1):
        state["step_number"] = index
        state["total_steps"] = total_steps
    return states



def _bubble_sort_states(array: List[int]) -> List[State]:
    arr = array.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    states: List[State] = []

    states.append(
        _build_state(
            array=arr,
            active_indices=[],
            sorted_indices=[],
            comparisons=comparisons,
            swaps=swaps,
            message="Estado inicial do vetor antes do início da ordenação.",
            math_concept="Função de transformação: o algoritmo receberá uma entrada desordenada e produzirá uma saída ordenada.",
            color_mode="default",
        )
    )

    for i in range(n):
        for j in range(0, n - i - 1):
            comparisons += 1
            states.append(
                _build_state(
                    array=arr,
                    active_indices=[j, j + 1],
                    sorted_indices=list(range(n - i, n)),
                    comparisons=comparisons,
                    swaps=swaps,
                    message=f"Comparando os elementos {arr[j]} e {arr[j + 1]}. O algoritmo avalia a relação de ordem entre eles.",
                    math_concept="Relação de ordem e decisão lógica: verifica-se se o elemento da esquerda é maior que o da direita.",
                    color_mode="active",
                )
            )
            if arr[j] > arr[j + 1]:
                arr[j], arr[j + 1] = arr[j + 1], arr[j]
                swaps += 1
                states.append(
                    _build_state(
                        array=arr,
                        active_indices=[j, j + 1],
                        sorted_indices=list(range(n - i, n)),
                        comparisons=comparisons,
                        swaps=swaps,
                        message=f"Como {arr[j + 1]} era maior que {arr[j]}, houve troca para preservar a ordem crescente.",
                        math_concept="Lógica condicional: a proposição 'esquerda > direita' foi verdadeira, então a troca foi executada.",
                        color_mode="swap",
                    )
                )
            else:
                states.append(
                    _build_state(
                        array=arr,
                        active_indices=[j, j + 1],
                        sorted_indices=list(range(n - i, n)),
                        comparisons=comparisons,
                        swaps=swaps,
                        message=f"Como {arr[j]} ≤ {arr[j + 1]}, não é necessário trocar os elementos.",
                        math_concept="Lógica condicional: a condição de troca foi falsa, então a ordem local já está correta.",
                        color_mode="active",
                    )
                )

    states.append(
        _build_state(
            array=arr,
            active_indices=[],
            sorted_indices=list(range(n)),
            comparisons=comparisons,
            swaps=swaps,
            message="Ordenação concluída. Todo o vetor está em ordem crescente.",
            math_concept="Síntese matemática: a repetição sistemática de comparações produziu uma sequência totalmente ordenada.",
            color_mode="sorted",
        )
    )

    return _finalize_states(states)



def _selection_sort_states(array: List[int]) -> List[State]:
    arr = array.copy()
    n = len(arr)
    comparisons = 0
    swaps = 0
    states: List[State] = []

    states.append(
        _build_state(
            array=arr,
            active_indices=[],
            sorted_indices=[],
            comparisons=comparisons,
            swaps=swaps,
            message="Estado inicial do vetor antes do início da ordenação.",
            math_concept="O algoritmo começa com um conjunto ainda não ordenado e buscará sucessivamente o menor elemento disponível.",
            color_mode="default",
        )
    )

    for i in range(n):
        min_idx = i
        states.append(
            _build_state(
                array=arr,
                active_indices=[i],
                sorted_indices=list(range(i)),
                comparisons=comparisons,
                swaps=swaps,
                message=f"Início da posição {i}. Assume-se inicialmente que o menor valor está no índice {i}.",
                math_concept="Hipótese inicial: o algoritmo define um candidato a mínimo dentro da parte ainda não ordenada do vetor.",
                color_mode="active",
            )
        )

        for j in range(i + 1, n):
            comparisons += 1
            states.append(
                _build_state(
                    array=arr,
                    active_indices=[min_idx, j],
                    sorted_indices=list(range(i)),
                    comparisons=comparisons,
                    swaps=swaps,
                    message=f"Comparando o mínimo atual {arr[min_idx]} com o elemento {arr[j]}.",
                    math_concept="Relação de ordem: o algoritmo verifica se existe um valor ainda menor na região não ordenada.",
                    color_mode="active",
                )
            )
            if arr[j] < arr[min_idx]:
                min_idx = j
                states.append(
                    _build_state(
                        array=arr,
                        active_indices=[i, min_idx],
                        sorted_indices=list(range(i)),
                        comparisons=comparisons,
                        swaps=swaps,
                        message=f"Novo mínimo encontrado: {arr[min_idx]} passa a ser o candidato para a posição {i}.",
                        math_concept="Escolha ótima local: o algoritmo atualiza o menor valor encontrado até o momento.",
                        color_mode="swap",
                    )
                )

        if min_idx != i:
            arr[i], arr[min_idx] = arr[min_idx], arr[i]
            swaps += 1
            states.append(
                _build_state(
                    array=arr,
                    active_indices=[i, min_idx],
                    sorted_indices=list(range(i + 1)),
                    comparisons=comparisons,
                    swaps=swaps,
                    message=f"Troca realizada: o menor elemento encontrado foi colocado na posição {i}.",
                    math_concept="Construção ordenada: a cada etapa, o menor elemento remanescente é posicionado corretamente.",
                    color_mode="swap",
                )
            )
        else:
            states.append(
                _build_state(
                    array=arr,
                    active_indices=[i],
                    sorted_indices=list(range(i + 1)),
                    comparisons=comparisons,
                    swaps=swaps,
                    message=f"Nenhuma troca foi necessária na posição {i}; o menor elemento já estava no lugar certo.",
                    math_concept="Estabilidade da ordem local: a posição já atendia ao critério de mínimo.",
                    color_mode="active",
                )
            )

    states.append(
        _build_state(
            array=arr,
            active_indices=[],
            sorted_indices=list(range(n)),
            comparisons=comparisons,
            swaps=swaps,
            message="Ordenação concluída. Todo o vetor está em ordem crescente.",
            math_concept="Síntese matemática: o vetor final é resultado de sucessivas escolhas do menor elemento disponível.",
            color_mode="sorted",
        )
    )

    return _finalize_states(states)



def generate_sorting_states(array: List[int], algorithm_name: str) -> List[State]:
    if algorithm_name == "Bubble Sort":
        return _bubble_sort_states(array)
    if algorithm_name == "Selection Sort":
        return _selection_sort_states(array)
    raise ValueError(f"Algoritmo não suportado: {algorithm_name}")
