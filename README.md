# 🗂️ Organizador de Arquivos

![Python](https://img.shields.io/badge/Python-3.12-3776AB?style=flat&logo=python&logoColor=white)
![PyYAML](https://img.shields.io/badge/PyYAML-6.0-blue?style=flat)
![pytest](https://img.shields.io/badge/pytest-8.0-0A9EDC?style=flat&logo=pytest&logoColor=white)

Script de automação em Python que organiza os arquivos de uma pasta em subpastas por categoria (imagens, documentos, planilhas, código etc.), com base em um mapeamento de extensões configurável via YAML. Feito para resolver aquele problema clássico de pasta de Downloads/Área de Trabalho virando um caos.

## 📦 Projeto

| Arquivo | O quê | Tecnologia |
|---|---|---|
| `main.py` | CLI de entrada | argparse |
| `organizer.py` | Lógica de categorização e movimentação | pathlib, shutil |
| `config.yaml` | Mapeamento extensão → categoria | PyYAML |
| `tests/test_organizer.py` | Testes unitários | pytest |

## 🧠 Conceitos implementados

- ✅ **Categorização por extensão**: mapeamento configurável em `config.yaml`, sem precisar tocar no código para adicionar novas categorias.
- ✅ **Dry-run**: `--dry-run` simula toda a organização e mostra no log o que seria movido, sem tocar em nenhum arquivo — importante antes de rodar em pasta de verdade.
- ✅ **Modo recursivo**: `--recursivo` varre também as subpastas em vez de só o nível raiz.
- ✅ **Organização por data**: opção `organizar_por_data: true` no config cria subpastas por ano/mês com base na data de modificação do arquivo.
- ✅ **Resolução de conflito de nome**: se já existe um arquivo com o mesmo nome no destino, o script gera automaticamente `arquivo (1).txt`, `arquivo (2).txt` etc., sem sobrescrever nada.

## 🚀 Como rodar localmente

### Pré-requisitos
- [Python 3.10+](https://www.python.org/downloads/)

### 1. Instalar dependências

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Rodar

```bash
# Organiza a pasta Downloads
python main.py ~/Downloads

# Simula antes de rodar de verdade (recomendado na primeira vez)
python main.py ~/Downloads --dry-run

# Organiza incluindo subpastas
python main.py ~/Downloads --recursivo

# Usando um config customizado
python main.py ~/Downloads --config minha_config.yaml
```

## 🔍 Testando

```bash
# cria uma pasta de teste com alguns arquivos
mkdir -p /tmp/teste_pasta
touch /tmp/teste_pasta/foto.jpg /tmp/teste_pasta/doc.pdf /tmp/teste_pasta/planilha.xlsx

# roda em dry-run pra ver o que aconteceria
python main.py /tmp/teste_pasta --dry-run
```

Repare que os arquivos são agrupados por categoria (`Imagens/`, `Documentos/`, `Planilhas/`...) conforme o mapeamento em `config.yaml` — extensões não mapeadas caem em `Outros/`.

## ⚙️ Configuração

Edite `config.yaml` para adicionar ou alterar categorias e extensões:

```yaml
categorias:
  Imagens:
    - jpg
    - png
  Documentos:
    - pdf
    - docx
categoria_outros: Outros
organizar_por_data: false
```

## ✅ Testes automatizados

```bash
pytest -v
```

5 testes cobrindo categorização, dry-run, resolução de conflito de nome, extensão desconhecida e pasta de origem inválida.

## 🗺️ Estrutura

```
organizador-arquivos/
├── main.py                   # CLI
├── organizer.py               # Lógica principal
├── config.yaml                 # Mapeamento de categorias
├── requirements.txt
├── tests/
│   └── test_organizer.py
└── README.md
```

## 🔮 Possíveis evoluções

- Watch mode: monitorar a pasta em tempo real com `watchdog`
- Interface gráfica simples (Tkinter) ou TUI
- Undo da última organização (log de movimentações reversível)

---

© 2026 Gabriel Teramae Chan
