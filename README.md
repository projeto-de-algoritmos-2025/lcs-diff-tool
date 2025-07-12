## LCS Diff Tool 
Um visualizador de diferenças entre arquivos que utiliza Programação Dinâmica (algoritmo LCS - Longest Common Subsequence) para identificar e destacar mudanças de forma inteligente.

### Sobre o Projeto
Este projeto implementa um comparador de arquivos que:

- Usa o algoritmo LCS (Longest Common Subsequence) com programação dinâmica
- Oferece visualização tanto no terminal quanto via Streamlit
- Destaca adições, remoções e linhas inalteradas com cores diferentes
- Calcula estatísticas detalhadas das diferenças

### Funcionalidades
- Comparação inteligente usando algoritmo LCS otimizado
- Visualização colorida no terminal e interface web
- Estatísticas detalhadas (linhas adicionadas, removidas, modificadas)
- Performance otimizada com memoização
- Interface responsiva no Streamlit

### Como Funciona
Algoritmo LCS (Longest Common Subsequence)
- Construção da matriz DP: Compara linha por linha dos arquivos
- Preenchimento otimizado: Usa programação dinâmica para evitar recálculos
- Reconstrução do caminho: Determina quais operações foram realizadas
- Classificação das mudanças: Identifica inserções, deleções e linhas iguais
