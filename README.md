# Organizador de Arquivos

Script de automação em Python que organiza os arquivos de uma pasta em
subpastas por categoria (imagens, documentos, planilhas, código etc.),
com base em um mapeamento de extensões configurável via YAML.

## Features

- Categorização por extensão de arquivo, configurável em `config.yaml`
- Modo `--dry-run` (simula sem mover nada)
- Modo `--recursivo` (organiza também subpastas)
- Organização opcional por ano/mês (`organizar_por_data: true`)
- Resolução automática de conflitos de nome (`arquivo (1).txt`)
- Log de todas as operações
- Testes unitários com `pytest`

## Instalação

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

## Uso

```bash
# Organiza a pasta Downloads
python main.py ~/Downloads

# Simula antes de rodar de verdade
python main.py ~/Downloads --dry-run

# Organiza incluindo subpastas
python main.py ~/Downloads --recursivo

# Usando um config customizado
python main.py ~/Downloads --config minha_config.yaml
```

## Configuração

Edite `config.yaml` para adicionar/alterar categorias e extensões:

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

## Testes

```bash
pytest -v
```

## Estrutura

```
organizador-arquivos/
├── main.py           # CLI
├── organizer.py       # Lógica principal
├── config.yaml         # Mapeamento de categorias
├── requirements.txt
├── tests/
│   └── test_organizer.py
└── README.md
```

## Possíveis evoluções

- Suporte a watch mode (monitorar pasta em tempo real com `watchdog`)
- Interface gráfica simples (Tkinter) ou TUI
- Undo da última organização (log de movimentações reversível)
