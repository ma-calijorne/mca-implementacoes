from __future__ import annotations

from typing import Any, Dict, List


SearchState = Dict[str, Any]


def _build_state(
    array: List[int],
    target: int,
    left: int,
    right: int,
    mid: int | None,
    comparisons: int,
    discarded_indices: List[int],
    found_index: int | None,
    message: str,
    math_concept: str,
    status: str = "searching",
) -> SearchState:
    return {
        "array": array.copy(),
        "target": target,
        "left": left,
        "right": right,
        "mid": mid,
        "comparisons": comparisons,
        "discarded_indices": discarded_indices.copy(),
        "found_index": found_index,
        "message": message,
        "math_concept": math_concept,
        "status": status,
    }



def _finalize_states(states: List[SearchState]) -> List[SearchState]:
    total_steps = len(states)
    for index, state in enumerate(states, start=1):
        state["step_number"] = index
        state["total_steps"] = total_steps
    return states



def generate_binary_search_states(array: List[int], target: int) -> List[SearchState]:
    if not array:
        raise ValueError("O vetor não pode estar vazio.")

    arr = sorted(array)
    left = 0
    right = len(arr) - 1
    comparisons = 0
    discarded: set[int] = set()
    states: List[SearchState] = []

    states.append(
        _build_state(
            array=arr,
            target=target,
            left=left,
            right=right,
            mid=None,
            comparisons=comparisons,
            discarded_indices=sorted(discarded),
            found_index=None,
            message=(
                "Estado inicial da busca. O vetor já está ordenado, condição necessária para aplicar a busca binária."
            ),
            math_concept=(
                "Pré-condição algorítmica: a ordenação permite dividir o espaço de busca em intervalos lógicos."
            ),
            status="initial",
        )
    )

    while left <= right:
        mid = (left + right) // 2
        comparisons += 1

        states.append(
            _build_state(
                array=arr,
                target=target,
                left=left,
                right=right,
                mid=mid,
                comparisons=comparisons,
                discarded_indices=sorted(discarded),
                found_index=None,
                message=(
                    f"Calcula-se o índice médio: ({left} + {right}) // 2 = {mid}. "
                    f"Agora o algoritmo compara o alvo {target} com o valor central {arr[mid]}."
                ),
                math_concept=(
                    "Divisão do intervalo e comparação lógica: a busca testa uma proposição no elemento central para reduzir metade do problema."
                ),
                status="searching",
            )
        )

        if arr[mid] == target:
            states.append(
                _build_state(
                    array=arr,
                    target=target,
                    left=left,
                    right=right,
                    mid=mid,
                    comparisons=comparisons,
                    discarded_indices=sorted(discarded),
                    found_index=mid,
                    message=(
                        f"Sucesso: o valor central {arr[mid]} é exatamente o alvo {target}. O elemento foi encontrado no índice {mid}."
                    ),
                    math_concept=(
                        "Equivalência lógica: a proposição 'valor do meio = alvo' é verdadeira, encerrando a busca."
                    ),
                    status="found",
                )
            )
            return _finalize_states(states)

        if target < arr[mid]:
            new_discards = list(range(mid, right + 1))
            discarded.update(new_discards)
            states.append(
                _build_state(
                    array=arr,
                    target=target,
                    left=left,
                    right=right,
                    mid=mid,
                    comparisons=comparisons,
                    discarded_indices=sorted(discarded),
                    found_index=None,
                    message=(
                        f"Como {target} < {arr[mid]}, o alvo só pode estar à esquerda do índice {mid}. "
                        f"A metade direita é descartada."
                    ),
                    math_concept=(
                        "Relação de ordem: se o alvo é menor que o valor central, todo elemento à direita também deixa de ser candidato."
                    ),
                    status="discard-right",
                )
            )
            right = mid - 1
        else:
            new_discards = list(range(left, mid + 1))
            discarded.update(new_discards)
            states.append(
                _build_state(
                    array=arr,
                    target=target,
                    left=left,
                    right=right,
                    mid=mid,
                    comparisons=comparisons,
                    discarded_indices=sorted(discarded),
                    found_index=None,
                    message=(
                        f"Como {target} > {arr[mid]}, o alvo só pode estar à direita do índice {mid}. "
                        f"A metade esquerda é descartada."
                    ),
                    math_concept=(
                        "Relação de ordem: se o alvo é maior que o valor central, todo elemento à esquerda deixa de pertencer ao conjunto de busca."
                    ),
                    status="discard-left",
                )
            )
            left = mid + 1

    states.append(
        _build_state(
            array=arr,
            target=target,
            left=left,
            right=right,
            mid=None,
            comparisons=comparisons,
            discarded_indices=sorted(discarded),
            found_index=None,
            message=(
                f"Busca encerrada sem sucesso. O intervalo de busca tornou-se vazio, portanto o valor {target} não está no vetor."
            ),
            math_concept=(
                "Prova por exaustão lógica do intervalo: após sucessivos descartes válidos, não restou nenhum candidato possível."
            ),
            status="not-found",
        )
    )

    return _finalize_states(states)
