# MathLab Computacional

## Visão Geral

MathLab Computacional é um laboratório interativo desenvolvido em Streamlit para apoiar a disciplina **Matemática Computacional Aplicada**. O projeto conecta teoria matemática com implementação visual de algoritmos, permitindo execução passo a passo, análise de estados intermediários e interpretação didática.

## Objetivos Pedagógicos

* Transformar conceitos abstratos em visualizações concretas.
* Relacionar matemática discreta com algoritmos reais.
* Permitir experimentação com entradas diferentes.
* Estimular raciocínio lógico e análise de complexidade.
* Apoiar aulas expositivas, práticas e estudos autônomos.

---

# Tecnologias Utilizadas

* Python 3.11+
* Streamlit
* Plotly
* Estrutura modular em pacotes Python

## Estrutura do Projeto

```text
mathlab_computacional/
├── app.py
├── requirements.txt
├── README.md
├── algorithms/
│   ├── sorting_algorithms.py
│   ├── search_algorithms.py
│   ├── matrix_algorithms.py
│   ├── graph_algorithms.py
│   └── combinatorics_algorithms.py
├── modules/
│   ├── home.py
│   ├── sorting.py
│   ├── binary_search.py
│   ├── matrix_traversal.py
│   ├── graph_bfs.py
│   └── path_counting.py
├── components/
│   ├── renderers.py
│   ├── metrics.py
│   └── panels.py
└── assets/
```

---

# Instalação

## 1. Criar ambiente virtual

```bash
python -m venv .venv
```

## 2. Ativar ambiente

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows

```bash
.venv\\Scripts\\activate
```

## 3. Instalar dependências

```bash
pip install -r requirements.txt
```

## 4. Executar aplicação

```bash
streamlit run app.py
```

A aplicação abrirá no navegador local.

---

# Arquitetura Técnica

## app.py

Arquivo principal. Responsável por:

* configurar página Streamlit
* montar menu lateral
* controlar navegação entre módulos
* carregar telas

## modules/

Contém a interface de cada módulo. Cada arquivo renderiza uma tela específica.

## algorithms/

Contém a lógica pura dos algoritmos. Os algoritmos retornam **estados intermediários** para visualização.

## components/

Funções reutilizáveis de interface:

* gráficos
* painéis
* métricas
* renderizações visuais

---

# Conceito Central: Estados Intermediários

Os algoritmos não retornam apenas o resultado final. Eles geram uma sequência de estados.

Exemplo:

```python
{
  "array": [4,2,7,1],
  "active": [0,1],
  "comparisons": 1,
  "message": "Comparando 4 e 2"
}
```

Benefícios:

* passo a passo
* animação
* explicação didática
* depuração fácil
* reuso da lógica

---

# Módulos do Sistema

# Módulo 1 — Ordenação Visual

## Algoritmos

* Bubble Sort
* Selection Sort

## Conceitos Matemáticos

* relações de ordem
* lógica condicional
* funções
* contagem de operações

## O que o aluno observa

* comparações
* trocas
* vetor evoluindo até ordenar
* custo operacional

## Uso em aula

Excelente para introduzir como decisões simples constroem um processo completo.

---

# Módulo 2 — Busca Binária

## Conceitos Matemáticos

* intervalos
* lógica proposicional
* funções de busca
* relações (> < =)

## O que o aluno observa

* início, meio e fim
* descarte de metade do espaço de busca
* elemento encontrado ou não

## Uso em aula

Ideal para mostrar eficiência algorítmica comparada à busca linear.

---

# Módulo 3 — Percurso em Matrizes

## Modos de Percurso

* linha por linha
* coluna por coluna
* diagonal principal
* vizinhança 4 direções

## Conceitos Matemáticos

* pares ordenados
* produto cartesiano
* relações espaciais
* contagem

## Uso em aula

Excelente para introduzir estruturas bidimensionais e grids computacionais.

---

# Módulo 4 — Grafos com BFS

## Conceitos Matemáticos

* conjuntos
* relações
* adjacência
* subconjuntos visitados
* níveis de expansão

## O que o aluno observa

* fila da BFS
* ordem de visita
* nós descobertos
* expansão por camadas

## Uso em aula

Ponte direta entre matemática discreta e ciência da computação.

---

# Módulo 5 — Caminhos em Tabuleiro

## Problema

Quantos caminhos existem entre origem e destino em uma grade, movendo apenas para direita e baixo?

## Conceitos Matemáticos

* princípios de contagem
* combinatória
* programação dinâmica
* espaço de possibilidades

## O que o aluno observa

* grade
* obstáculos
* número de caminhos por célula
* total final de caminhos

## Uso em aula

Excelente para conectar fórmula matemática e solução computacional.

---

# Boas Práticas de Código

* Separação entre interface e regra de negócio.
* Funções pequenas e reutilizáveis.
* Estado controlado via Streamlit session_state.
* Código modular para expansão futura.

---

# Possíveis Evoluções

* DFS
* Dijkstra
* Recursão visual
* Backtracking
* Árvores binárias
* Complexidade Big-O comparativa
* Exportação de relatórios
* Modo avaliação para alunos

---

# Troubleshooting

## set_page_config error

Garanta que `st.set_page_config()` exista apenas em `app.py` e seja o primeiro comando Streamlit.

## Botão Próximo Passo não funciona

Verifique sincronização entre `session_state` e sliders.

## Dependências

Atualize pip:

```bash
python -m pip install --upgrade pip
```

---

# Licença de Uso

Uso acadêmico e educacional.

---

# Autor / Contexto

Projeto concebido para ensino universitário de Ciência da Computação, focado em aprendizagem visual de matemática aplicada a algoritmos. Criado por Marco Antônio Calijorne Soares
