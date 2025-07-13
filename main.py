from io import StringIO

import streamlit as st

st.set_page_config(
    page_title="DP Diff Visualizer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".html",
    ".css",
    ".java",
    ".cpp",
    ".c",
    ".php",
    ".rb",
    ".go",
    ".ts",
    ".jsx",
    ".tsx",
    ".vue",
    ".sql",
    ".sh",
    ".txt",
    ".md",
    ".json",
    ".xml",
    ".yaml",
    ".yml",
]


def is_supported_file(filename):
    return any(filename.lower().endswith(ext) for ext in SUPPORTED_EXTENSIONS)


def process_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        try:
            stringio = StringIO(uploaded_file.getvalue().decode("utf-8"))
            content = stringio.read()
            lines = content.splitlines()
            return lines, content
        except UnicodeDecodeError:
            st.error("Erro: Arquivo não está em formato UTF-8")
            return None, None
    return None, None


def main():
    st.title("🔍 LCS Diff Visualizer")
    st.markdown("**Visualizador de diferenças usando Algoritmo LCS (Longest Common Subsequence)**")

    with st.sidebar:
        st.header("⚙️ Configurações")

        show_line_numbers = st.checkbox("Mostrar números das linhas", value=True)
        ignore_whitespace = st.checkbox("Ignorar espaços em branco", value=False)

        st.divider()
        st.subheader("📁 Tipos Suportados")
        with st.expander("Ver extensões"):
            cols = st.columns(2)
            for i, ext in enumerate(SUPPORTED_EXTENSIONS):
                col = cols[i % 2]
                col.write(f"`{ext}`")

    col1, col2 = st.columns(2)
    with col1:
        st.subheader("📄 Arquivo Original")
        uploaded_file1 = st.file_uploader(
            "Escolha o primeiro arquivo",
            type=None,
            key="file1",
        )

        if uploaded_file1:
            if is_supported_file(uploaded_file1.name):
                lines1, content1 = process_uploaded_file(uploaded_file1)
                if lines1:
                    st.success(f"✅ {uploaded_file1.name} carregado ({len(lines1)} linhas)")

                    with st.expander("👀 Preview", expanded=False):
                        st.code(
                            content1[:500] + "..." if len(content1) > 500 else content1,
                            language=uploaded_file1.name.split(".")[-1] if "." in uploaded_file1.name else "text",
                        )
            else:
                st.error(f"❌ Tipo de arquivo não suportado: {uploaded_file1.name}")

    with col2:
        st.subheader("📄 Arquivo Modificado")
        uploaded_file2 = st.file_uploader("Escolha o segundo arquivo", type=None, key="file2")

        if uploaded_file2:
            if is_supported_file(uploaded_file2.name):
                lines2, content2 = process_uploaded_file(uploaded_file2)
                if lines2:
                    st.success(f"✅ {uploaded_file2.name} carregado ({len(lines2)} linhas)")

                    with st.expander("👀 Preview", expanded=False):
                        st.code(
                            content2[:500] + "..." if len(content2) > 500 else content2,
                            language=uploaded_file2.name.split(".")[-1] if "." in uploaded_file2.name else "text",
                        )
            else:
                st.error(f"❌ Tipo de arquivo não suportado: {uploaded_file2.name}")

    st.divider()
    if uploaded_file1 and uploaded_file2:
        if is_supported_file(uploaded_file1.name) and is_supported_file(uploaded_file2.name):
            col_btn1, col_btn2, col_btn3 = st.columns([1, 2, 1])
            with col_btn2:
                if st.button("🔍 Calcular Diferenças", type="primary", use_container_width=True):
                    with st.spinner("Processando com algoritmo LCS..."):
                        st.success("✅ Diferenças calculadas!")
                        st.subheader("📊 Resultados")

                        metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
                        with metric_col1:
                            st.metric("Linhas Iguais", "15")
                        with metric_col2:
                            st.metric("Adicionadas", "3", "3")
                        with metric_col3:
                            st.metric("Removidas", "2", "-2")
                        with metric_col4:
                            st.metric("Modificadas", "1")

                        st.subheader("🎨 Visualização das Diferenças")

                        st.info(
                            "🚧 **EM DESENVOLVIMENTO:** Aqui será exibida a comparação visual usando o algoritmo LCS"
                        )

                        tab1, tab2, tab3 = st.tabs([
                            "📋 Lado a Lado",
                            "📱 Unificado",
                            "📈 Estatísticas",
                        ])

                        with tab1:
                            st.write("Visualização lado a lado (TODO)")

                        with tab2:
                            st.write("Visualização unificada (TODO)")

                        with tab3:
                            st.write("Gráficos e estatísticas detalhadas (TODO)")

    else:
        st.info("📁 Faça upload de dois arquivos para comparar")

    st.divider()
    st.markdown(
        """
    <div style='text-align: center; color: #666;'>
        <small>
        🧮 <strong>Dynamic Programming</strong> (LCS Algorithm) | 
        </small>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
