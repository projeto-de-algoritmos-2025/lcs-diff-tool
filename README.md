# LCS Diff Tool

Um visualizador de diferenças entre arquivos que utiliza Programação Dinâmica (algoritmo LCS - Longest Common Subsequence) para identificar e destacar mudanças de forma inteligente.

## Sobre o Projeto

Este projeto implementa um comparador de arquivos que:

- Usa o algoritmo **LCS (Longest Common Subsequence)** com programação dinâmica
- Oferece visualização tanto no **terminal** quanto via **Streamlit**
- Destaca adições, remoções e linhas inalteradas com cores diferentes
- Calcula estatísticas detalhadas das diferenças

## Funcionalidades

- **Comparação inteligente** usando algoritmo LCS otimizado
- **Visualização colorida** no terminal e interface web
- **Estatísticas detalhadas** (linhas adicionadas, removidas, modificadas)
- **Performance otimizada** com memoização
- **Múltiplos formatos** de saída (terminal, web, HTML)
- **Interface responsiva** no Streamlit

## Como Funciona

### Algoritmo LCS (Longest Common Subsequence)

1. **Construção da matriz DP**: Compara linha por linha dos arquivos
2. **Preenchimento otimizado**: Usa programação dinâmica para evitar recálculos
3. **Reconstrução do caminho**: Determina quais operações foram realizadas
4. **Classificação das mudanças**: Identifica inserções, deleções e linhas iguais

```
Complexidade: O(m × n) onde m e n são o número de linhas dos arquivos
Espaço: O(m × n) para a matriz DP
```

## Instalação e configuração

### Pré-requisitos

- **Python 3.10+**
- **uv** (recomendado) ou pip

### Instalando uv (se não tiver)

```bash
# macOS e Linux
curl -LsSf https://astral.sh/uv/install.sh | sh

# Ou via pip
pip install uv
```

### Configuração do Projeto

#### 1. Clone o repositório

```bash
git clone https://github.com/seu-usuario/dp-diff-visualizer.git
cd dp-diff-visualizer
```

#### 2. Inicializar projeto uv

```bash
# Criar ambiente virtual e instalar dependências
uv sync

# Ou se preferir instalar manualmente
uv venv
uv pip install -e .
```

#### 3. Ativar ambiente (opcional)

```bash
# Linux/macOS
source .venv/bin/activate

```

## Como Executar

### Interface Web (Streamlit)

```bash
# Com uv (recomendado)
uv run streamlit run app/main.py

# Com ambiente ativado
streamlit run app/main.py
```

## 📄 Licença

Este projeto está sob a licença MIT. Veja o arquivo [LICENSE](LICENSE) para mais detalhes.
