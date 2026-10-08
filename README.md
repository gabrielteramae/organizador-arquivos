# Organizador de Arquivos — pastas por extensão

![Python](https://img.shields.io/badge/Python-3.10%20%7C%203.12-3776AB?logo=python&logoColor=white)
![PyYAML](https://img.shields.io/badge/PyYAML-6.0+-CB171E?logo=yaml&logoColor=white)
![pytest](https://img.shields.io/badge/pytest-8.0+-0A9EDC?logo=pytest&logoColor=white)

CLI que move os arquivos de uma pasta para subpastas definidas pela extensão em `config.yaml`. Extensão fora do mapa vai para `Outros`. Nome repetido no destino vira `arquivo (1).ext`, sem sobrescrever. `--dry-run` só registra o que seria movido.

## Stack

- Python 3.10, 3.11 e 3.12 no workflow (matriz)
- PyYAML >= 6.0
- pytest >= 8.0
- biblioteca padrão: `argparse`, `pathlib`, `shutil`, `logging`

## Estrutura

```
.
├── main.py                         # argumentos da CLI
├── organizer.py                    # mapa, destino, conflito e move
├── config.yaml                     # extensão → categoria
├── requirements.txt
├── tests/test_organizer.py         # seis testes
└── .github/workflows/python-package.yml
```

Categorias no YAML entregue: Imagens, Documentos, Planilhas, Apresentacoes, Videos, Audios, Compactados, Codigo. `organizar_por_data` está `false`; com `true`, o destino ganha `ano/mês` pela data de modificação. O modo recursivo ignora arquivo que já está dentro de uma pasta de categoria, link simbólico, nome com ponto na frente, `thumbs.db` e `desktop.ini`.

## Como rodar

```bash
git clone https://github.com/gabrielteramae/organizador-arquivos.git
cd organizador-arquivos
python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python main.py /caminho/da/pasta --dry-run
python main.py /caminho/da/pasta
python main.py /caminho/da/pasta --recursivo --config config.yaml -v
```

O primeiro argumento é a pasta de origem. Se ela não existir ou não for diretório, `organizar_pasta` levanta `NotADirectoryError`. Config ausente ou sem a chave `categorias` encerra o processo com código 1.

## Testes realizados

`tests/test_organizer.py`, seis testes, com pasta temporária:

- `.jpg` vai para `Imagens`, `.pdf` para `Documentos`, `.exe` para `Outros`
- dry-run devolve um resultado e não cria a pasta de destino
- `resolver_conflito` gera `arquivo (1).txt` se o nome já existe
- extensão `.xyz` cai em `Outros`
- origem inexistente levanta `NotADirectoryError`
- no modo recursivo, `Imagens/foto.jpg` não é aninhado de novo em `Imagens/Imagens`

```bash
pytest -v
```

O workflow roda esse pytest e o flake8 nas três versões de Python.

---

© 2026 Gabriel Teramae Chan
