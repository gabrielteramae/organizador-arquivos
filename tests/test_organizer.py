import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).parent.parent))

from organizer import carregar_config, organizar_pasta, resolver_conflito  # noqa: E402


@pytest.fixture
def config(tmp_path_factory):
    config_dir = tmp_path_factory.mktemp("config_dir")
    config_yaml = config_dir / "config.yaml"
    config_yaml.write_text(
        """
categorias:
  Imagens:
    - jpg
    - png
  Documentos:
    - pdf
    - txt
categoria_outros: Outros
organizar_por_data: false
""",
        encoding="utf-8",
    )
    return carregar_config(config_yaml)


def criar_arquivo(pasta: Path, nome: str, conteudo: str = "x") -> Path:
    arquivo = pasta / nome
    arquivo.write_text(conteudo)
    return arquivo


def test_organiza_por_extensao(tmp_path, config):
    criar_arquivo(tmp_path, "foto.jpg")
    criar_arquivo(tmp_path, "relatorio.pdf")
    criar_arquivo(tmp_path, "script.exe")

    resultados = organizar_pasta(tmp_path, config)

    assert (tmp_path / "Imagens" / "foto.jpg").exists()
    assert (tmp_path / "Documentos" / "relatorio.pdf").exists()
    assert (tmp_path / "Outros" / "script.exe").exists()
    assert len(resultados) == 3


def test_dry_run_nao_move_nada(tmp_path, config):
    criar_arquivo(tmp_path, "foto.png")

    resultados = organizar_pasta(tmp_path, config, dry_run=True)

    assert (tmp_path / "foto.png").exists()  # continua na origem
    assert not (tmp_path / "Imagens").exists()
    assert len(resultados) == 1


def test_resolve_conflito_de_nome(tmp_path):
    destino = tmp_path / "arquivo.txt"
    destino.write_text("original")

    novo_destino = resolver_conflito(destino)

    assert novo_destino != destino
    assert novo_destino.name == "arquivo (1).txt"


def test_extensao_desconhecida_vai_para_outros(tmp_path, config):
    criar_arquivo(tmp_path, "dados.xyz")

    organizar_pasta(tmp_path, config)

    assert (tmp_path / "Outros" / "dados.xyz").exists()


def test_pasta_origem_invalida_lanca_erro(tmp_path, config):
    with pytest.raises(NotADirectoryError):
        organizar_pasta(tmp_path / "nao_existe", config)
