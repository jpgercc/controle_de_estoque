# 📊 Controle Completo de Estoque

Aplicação web para gerenciamento e análise de estoque desenvolvida com Streamlit, Pandas e Plotly.

## 🚀 Funcionalidades

- 📤 Upload de arquivos Excel com validação de estrutura
- 🔍 Filtros dinâmicos por categoria, fornecedor e produto
- 📦 Identificação de estoque baixo com limite ajustável
- ⏰ Alertas de produtos com validade próxima (30 dias)
- 😴 Detecção de produtos inativos (sem movimentação em 30 dias)
- 📊 Visualizações gráficas interativas:
  - Estoque por produto (gráfico de barras)
  - Distribuição de custo por categoria (gráfico de pizza)

## 🛠️ Requisitos

- Python 3.7+
- Bibliotecas:
  - streamlit
  - pandas
  - plotly
  - openpyxl (para leitura de Excel)

## ⚙️ Instalação

1. Clone o repositório ou baixe o arquivo `app.py`
2. Instale as dependências:
   ```bash
   pip install streamlit pandas plotly openpyxl
3. Execute a aplicação:

    ```bash
      streamlit run app.py
ou alternativamente usando o comando abaixo:

  ```bash  
      python -m streamlit run app.py
