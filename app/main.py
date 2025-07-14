from io import StringIO

import pandas as pd
import streamlit as st

from lcs_algorithm import LCSAlgorithm, Operation

st.set_page_config(
    page_title="DP Diff Visualizer",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

SUPPORTED_EXTENSIONS = [
    ".py",
    ".js",
    ".jsx",
    ".tsx",
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


def render_diff_side_by_side(operations, show_line_numbers=True):
    left_html = []
    right_html = []

    left_line_num = 1
    right_line_num = 1

    deleted_style = (
        "background-color: #3a2323; border-left: 4px solid #f44336; "
        "padding: 8px; font-family: monospace; font-size: 14px; color: #ffb3b3;"
    )
    inserted_style = (
        "background-color: #223a23; border-left: 4px solid #4caf50; "
        "padding: 8px; font-family: monospace; font-size: 14px; color: #b6ffb3;"
    )
    unchanged_style = (
        "background-color: #23272f; border-left: 2px solid #888; "
        "padding: 8px; font-family: monospace; font-size: 14px; color: #e0e0e0;"
    )
    empty_style = (
        "background-color: #23272f; color: #666; padding: 8px; "
        "font-family: monospace; text-align: center; font-size: 14px;"
    )

    for op in operations:
        content = op.content.replace("<", "&lt;").replace(">", "&gt;")

        if op.operation == Operation.DELETE:
            line_num = f"{left_line_num:3d}: " if show_line_numbers else ""
            left_html.append(
                f'<div style="{deleted_style}"><strong style="color: #f44336;">- {line_num}</strong>{content}</div>'
            )
            right_html.append(f'<div style="{empty_style}">---</div>')
            left_line_num += 1

        elif op.operation == Operation.INSERT:
            line_num = f"{right_line_num:3d}: " if show_line_numbers else ""
            left_html.append(f'<div style="{empty_style}">---</div>')
            right_html.append(
                f'<div style="{inserted_style}"><strong style="color: #4caf50;">+ {line_num}</strong>{content}</div>'
            )
            right_line_num += 1

        else:  # KEEP
            left_num = f"{left_line_num:3d}: " if show_line_numbers else ""
            right_num = f"{right_line_num:3d}: " if show_line_numbers else ""
            left_html.append(f'<div style="{unchanged_style}">  {left_num}{content}</div>')
            right_html.append(f'<div style="{unchanged_style}">  {right_num}{content}</div>')
            left_line_num += 1
            right_line_num += 1

    return "\n".join(left_html), "\n".join(right_html)


def render_diff_unified(operations, show_line_numbers=True):
    html_lines = []

    for op in operations:
        content = op.content.replace("<", "&lt;").replace(">", "&gt;")

        if op.operation == Operation.DELETE:
            style = "background-color: #ffebee; border-left: 4px solid #f44336; padding: 8px; font-family: monospace; font-size: 14px; margin: 1px 0;"
            line_num = f"{op.line_number_1:3d}: " if show_line_numbers and op.line_number_1 else ""
            html_lines.append(
                f'<div style="{style}"><strong style="color: #f44336;">- {line_num}</strong>{content}</div>'
            )

        elif op.operation == Operation.INSERT:
            style = "background-color: #e8f5e8; border-left: 4px solid #4caf50; padding: 8px; font-family: monospace; font-size: 14px; margin: 1px 0;"
            line_num = f"{op.line_number_2:3d}: " if show_line_numbers and op.line_number_2 else ""
            html_lines.append(
                f'<div style="{style}"><strong style="color: #4caf50;">+ {line_num}</strong>{content}</div>'
            )

        else:  # KEEP
            style = "background-color: #f9f9f9; border-left: 2px solid #ddd; padding: 8px; font-family: monospace; font-size: 14px; margin: 1px 0;"
            line_num = f"{op.line_number_1:3d}: " if show_line_numbers and op.line_number_1 else ""
            html_lines.append(f'<div style="{style}">  {line_num}{content}</div>')

    return "\n".join(html_lines)


def main():
    st.title("🔍 LCS Diff Visualizer")
    st.markdown("**Visualizador de diferenças usando Algoritmo LCS (Longest Common Subsequence)**")

    with st.sidebar:
        st.header("⚙️ Configurações")
        show_line_numbers = st.checkbox("Mostrar números das linhas", value=True)
        ignore_whitespace = st.checkbox("Ignorar espaços em branco", value=False)
        enable_memoization = st.checkbox("Habilitar memoização", value=True)

        st.divider()
        st.subheader("📁 Tipos Suportados")
        with st.expander("Ver extensões"):
            cols = st.columns(2)
            for i, ext in enumerate(SUPPORTED_EXTENSIONS):
                col = cols[i % 2]
                col.write(f"`{ext}`")

    col1, col2 = st.columns(2)
    lines1, content1, filename1 = None, None, None
    lines2, content2, filename2 = None, None, None

    with col1:
        st.subheader("📄 Arquivo Original")
        uploaded_file1 = st.file_uploader("Escolha o primeiro arquivo", type=None, key="file1")

        if uploaded_file1:
            filename1 = uploaded_file1.name
            if is_supported_file(filename1):
                lines1, content1 = process_uploaded_file(uploaded_file1)
                if lines1:
                    st.success(f"✅ {filename1} carregado ({len(lines1)} linhas)")
                    with st.expander("👀 Preview", expanded=False):
                        st.code(
                            content1[:500] + "..." if len(content1) > 500 else content1,
                            language=filename1.split(".")[-1] if "." in filename1 else "text",
                        )
            else:
                st.error(f"❌ Tipo de arquivo não suportado: {filename1}")

    with col2:
        st.subheader("📄 Arquivo Modificado")
        uploaded_file2 = st.file_uploader("Escolha o segundo arquivo", type=None, key="file2")

        if uploaded_file2:
            filename2 = uploaded_file2.name
            if is_supported_file(filename2):
                lines2, content2 = process_uploaded_file(uploaded_file2)
                if lines2:
                    st.success(f"✅ {filename2} carregado ({len(lines2)} linhas)")
                    with st.expander("👀 Preview", expanded=False):
                        st.code(
                            content2[:500] + "..." if len(content2) > 500 else content2,
                            language=filename2.split(".")[-1] if "." in filename2 else "text",
                        )
            else:
                st.error(f"❌ Tipo de arquivo não suportado: {filename2}")

    st.divider()

    if lines1 and lines2:
        col_btn1, col_btn2, col_btn3 = st.columns([1, 8, 1])
        with col_btn2:
            if st.button("🔍 Calcular Diferenças", type="primary", use_container_width=True):
                with st.spinner("Processando com algoritmo LCS..."):
                    processed_lines1 = [line.strip() if ignore_whitespace else line for line in lines1]
                    processed_lines2 = [line.strip() if ignore_whitespace else line for line in lines2]

                    lcs = LCSAlgorithm(enable_memoization=enable_memoization)
                    operations = lcs.compute_diff_operations(processed_lines1, processed_lines2)
                    stats = lcs.get_statistics(operations)

                    st.success("✅ Diferenças calculadas!")
                    st.subheader("📊 Resultados")
                    metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)

                    with metric_col1:
                        st.metric("Linhas Iguais", stats["lines_kept"])
                    with metric_col2:
                        st.metric(
                            "Adicionadas",
                            stats["lines_inserted"],
                            f"+{stats['lines_inserted']}" if stats["lines_inserted"] > 0 else "0",
                        )
                    with metric_col3:
                        st.metric(
                            "Removidas",
                            stats["lines_deleted"],
                            f"-{stats['lines_deleted']}" if stats["lines_deleted"] > 0 else "0",
                        )
                    with metric_col4:
                        similarity = (
                            (stats["lines_kept"] / stats["total_lines"] * 100) if stats["total_lines"] > 0 else 0
                        )
                        st.metric("Similaridade", f"{similarity:.1f}%")

                    st.subheader("🎨 Visualização das Diferenças")
                    tab1, tab2 = st.tabs(["📋 Lado a Lado", "📈 Estatísticas"])
                    with tab1:
                        st.markdown("### 📋 Comparação Lado a Lado")
                        left_diff, right_diff = render_diff_side_by_side(operations, show_line_numbers)

                        diff_col1, diff_col2 = st.columns(2)
                        with diff_col1:
                            st.markdown(f"**📄 {filename1 or 'Arquivo Original'}**")
                            st.markdown(
                                f'<div style="border: 2px solid #ddd; height: 500px; overflow-y: auto; background: white; border-radius: 5px;">{left_diff}</div>',
                                unsafe_allow_html=True,
                            )

                        with diff_col2:
                            st.markdown(f"**📄 {filename2 or 'Arquivo Modificado'}**")
                            st.markdown(
                                f'<div style="border: 2px solid #ddd; height: 500px; overflow-y: auto; background: white; border-radius: 5px;">{right_diff}</div>',
                                unsafe_allow_html=True,
                            )

                    with tab2:
                        st.markdown("### 📈 Análise do Algoritmo LCS")

                        col_alg1, col_alg2 = st.columns(2)
                        with col_alg1:
                            st.markdown("**Complexidade do Algoritmo:**")
                            st.write(
                                f"• **Tempo:** O(m × n) = O({len(lines1)} × {len(lines2)}) = {len(lines1) * len(lines2):,} operações"
                            )
                            st.write(f"• **Espaço:** O(m × n) = {len(lines1) * len(lines2):,} células na matriz")
                            st.write(
                                f"• **Memoização:** {'✅ Habilitada' if enable_memoization else '❌ Desabilitada'}"
                            )

                        with col_alg2:
                            st.markdown("**📊 Estatísticas das Operações:**")
                            st.write(f"• **Total de operações:** {stats['total_lines']}")
                            st.write(f"• **Linhas mantidas (LCS):** {stats['lines_kept']}")
                            st.write(f"• **Taxa de similaridade:** {similarity:.1f}%")

    else:
        st.info("📁 Faça upload de dois arquivos para comparar")

    st.divider()
    st.markdown(
        """
    <div style='text-align: center; color: #777;'>
        <small>🧮 <strong>Dynamic Programming</strong> (LCS Algorithm)</small>
    </div>
    """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
