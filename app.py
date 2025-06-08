import streamlit as st
import pandas as pd
import plotly.express as px
# python -m streamlit run app.py

st.set_page_config(page_title="📊 Controle Completo de Estoque", layout="wide")
st.title("📦 Controle de Estoque")

# ===== Funções =====

def filter_date(df, col, condition):
    df[col] = pd.to_datetime(df[col], errors='coerce')
    mask = df[col].notna() & condition(df[col])
    return df[mask]

def filter_stock(df, col, limit, less_equal=True):
    return df[df[col] <= limit] if less_equal else df[df[col] > limit]

def apply_filters(df, filters):
    for col, val in filters.items():
        if val != 'Todos':
            df = df[df[col] == val]
    return df

def display_table(df, columns=None, expand_key=None):
    if df.empty:
        st.success("✅ Nenhum dado encontrado.")
        return
    expand = st.checkbox(f"Expandir tabela completa {expand_key or ''}", key=expand_key)
    to_show = df if expand else df.head(2)
    st.dataframe(to_show[columns] if columns else to_show)

def check_file_size(uploaded_file, max_mb=10):
    return (uploaded_file.size / (1024 * 1024)) <= max_mb

def validate_columns(df):
    numeric_cols = ['Quantidade', 'Custo Unitário', 'Preço Unitário']
    date_cols = ['Data Validade', 'Última Saída', 'Última Entrada']
    for col in numeric_cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce').dt.date
    return df

# ===== Upload =====

uploaded_file = st.file_uploader("📤 Faça upload do Excel", type=["xlsx"])

if uploaded_file and uploaded_file.name.endswith('.xlsx') and check_file_size(uploaded_file):
    try:
        excel_data = pd.read_excel(uploaded_file, sheet_name=None)
        selected_sheet = st.selectbox("Selecione a aba", list(excel_data.keys()))
        df = excel_data[selected_sheet]

        expected_cols = [
            'Código', 'Produto', 'Categoria', 'Fornecedor', 'Quantidade',
            'Preço Unitário', 'Custo Unitário', 'Data Validade', 'Última Entrada', 'Última Saída'
        ]

        if list(df.columns) != expected_cols:
            st.error("❌ Colunas incorretas ou fora de ordem.")
            st.stop()

        df = validate_columns(df)

        # ===== Filtros =====
        filtros = {}
        for col in ['Categoria', 'Fornecedor', 'Produto']:
            options = ['Todos'] + sorted(df[col].dropna().unique())
            filtros[col] = st.sidebar.selectbox(f"Filtrar por {col}", options)

        df_filtrado = apply_filters(df, filtros)

        st.subheader("📁 Visualização da Tabela Filtrada")
        display_table(df_filtrado, expand_key="filtrado")

        st.markdown("---")
        col1, col2 = st.columns(2)

        # Estoque baixo
        with col1:
            st.subheader("📦 Estoque Baixo")
            limite = st.slider("Limite mínimo de estoque", 1, 100, 10)
            estoque_baixo = filter_stock(df_filtrado, 'Quantidade', limite)
            if not estoque_baixo.empty:
                display_table(estoque_baixo, ['Código', 'Produto', 'Quantidade'], "estoque")
            else:
                st.success("✅ Nenhum item com estoque baixo.")

        # Validade próxima
        with col2:
            st.subheader("⏰ Validade Próxima")
            vencendo = filter_date(df_filtrado, 'Data Validade', lambda d: d <= pd.Timestamp.now() + pd.Timedelta(days=30))
            if not vencendo.empty:
                display_table(vencendo, ['Código', 'Produto', 'Data Validade'], "validade")
            else:
                st.success("✅ Nenhum produto vencendo em breve.")

        # Produtos inativos
        st.markdown("---")
        st.subheader("😴 Produtos sem movimentação (últimos 30 dias)")
        inativos = filter_date(df_filtrado, 'Última Saída', lambda d: d <= pd.Timestamp.now() - pd.Timedelta(days=30))
        if not inativos.empty:
            display_table(inativos, ['Código', 'Produto', 'Última Saída'], "inativos")
        else:
            st.success("✅ Todos os produtos tiveram movimentação recente.")

        # Gráficos
        st.markdown("---")
        st.subheader("📈 Gráficos de Estoque")

        col3, col4 = st.columns(2)
        with col3:
            fig1 = px.bar(df_filtrado, x='Produto', y='Quantidade', title="Estoque por Produto")
            st.plotly_chart(fig1, use_container_width=True)

        with col4:
            df_filtrado['Custo Total'] = df_filtrado['Custo Unitário'] * df_filtrado['Quantidade']
            fig2 = px.pie(df_filtrado, names='Categoria', values='Custo Total', title="Distribuição do Custo por Categoria")
            st.plotly_chart(fig2, use_container_width=True)

    except Exception as e:
        st.error(f"Erro ao processar o arquivo: {e}")
