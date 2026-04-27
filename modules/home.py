import streamlit as st


def render_home() -> None:
    st.markdown(
        """
        <div class="mathlab-hero">
            <h1 style="margin:0;">MathLab Computacional</h1>
            <p style="margin:0.6rem 0 0 0; font-size:1.05rem; line-height:1.5;">
                Um laboratório visual para conectar Matemática Computacional Aplicada à implementação de algoritmos.
                Nesta versão, o sistema já possui a base do app, o módulo de Ordenação, o módulo de Busca Binária e o módulo de Percurso em Matrizes.
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            """
            <div class="mathlab-card">
                <h3>Objetivo didático</h3>
                <p>
                    Mostrar como conceitos como lógica, relações, funções e contagem aparecem em algoritmos reais.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col2:
        st.markdown(
            """
            <div class="mathlab-card">
                <h3>Como usar</h3>
                <p>
                    Navegue pelos módulos no menu lateral, configure entradas, execute passo a passo e discuta a matemática envolvida.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )
    with col3:
        st.markdown(
            """
            <div class="mathlab-card">
                <h3>Versão atual</h3>
                <p>
                    Estrutura principal pronta, identidade visual do laboratório e quatro módulos iniciais: Ordenação, Busca Binária, Matrizes e Grafos com BFS.
                </p>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.subheader("O que já está disponível")
    st.markdown(
        """
        - **App único com menu lateral**, pronto para expansão por módulos.
        - **Módulo 1: Ordenação**, com geração aleatória de vetor e execução passo a passo.
        - **Visualização gráfica** com barras, métricas, explicação textual e conexão com a teoria.
        - **Módulo 3: Matrizes**, com diferentes regras de percurso e leitura por pares ordenados.
        - **Módulo 4: Grafos com BFS**, com visualização de adjacência, fila, descoberta e visitação por níveis.
        """
    )

    st.subheader("Temas matemáticos conectados ao módulo 1")
    st.markdown(
        """
        - Relações de ordem: comparar quem é maior ou menor.
        - Lógica condicional: decidir se deve ou não trocar elementos.
        - Funções: transformar uma sequência desordenada em ordenada.
        - Contagem: medir comparações, trocas e passos do algoritmo.
        """
    )

    st.info(
        "Dica para a aula: use o módulo de Ordenação primeiro em modo passo a passo. Isso ajuda os alunos a enxergar a decisão lógica acontecendo em cada comparação."
    )

    st.subheader("Temas matemáticos conectados ao módulo 3")
    st.markdown(
        """
        - Produto cartesiano: cada célula é representada por um par ordenado (linha, coluna).
        - Relações espaciais: vizinhança e diagonal são regras formais de ligação entre posições.
        - Funções de percurso: a mesma matriz pode gerar sequências diferentes conforme a regra de visita.
        - Contagem: o algoritmo mede quantas células foram visitadas e em qual ordem.
        """
    )

    st.subheader("Temas matemáticos conectados ao módulo 4")
    st.markdown(
        """
        - Conjuntos: vértices, arestas, nós descobertos e nós visitados.
        - Relações: cada aresta representa uma relação de adjacência entre dois vértices.
        - Pertinência: o algoritmo testa se um vizinho já pertence ao conjunto de descobertos.
        - Funções: a BFS associa nós a níveis e pais na árvore de busca.
        """
    )
