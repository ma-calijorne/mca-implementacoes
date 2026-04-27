# MathLab Computacional

Laboratório visual de Matemática Computacional Aplicada construído em Streamlit.

## Módulos disponíveis

1. **Ordenação Visual**
   - Bubble Sort
   - Selection Sort
   - Comparações, trocas e relações de ordem

2. **Busca Binária**
   - Vetor ordenado
   - Início, meio e fim
   - Descarte de intervalos
   - Decisões lógicas

3. **Percurso em Matrizes**
   - Linha por linha
   - Coluna por coluna
   - Diagonal principal
   - Vizinhança 4 direções
   - Pares ordenados, produto cartesiano e relações espaciais

4. **Grafos com BFS**
   - Grafo didático fixo
   - Grafo aleatório conectado
   - Fila da BFS
   - Nós descobertos e visitados
   - Relações de adjacência e níveis de busca

## Como rodar

```bash
cd mathlab_computacional
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
streamlit run app.py
```

No Windows:

```bash
cd mathlab_computacional
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
streamlit run app.py
```

## Arquitetura

A lógica dos algoritmos fica separada da interface. Cada algoritmo gera uma lista de estados intermediários, permitindo visualização passo a passo, métricas e explicação didática.

## Dependências

- Streamlit
- Plotly
