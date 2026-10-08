"""
organizer.py

Lógica principal do organizador de arquivos.
Move arquivos de uma pasta de origem para subpastas baseadas em categoria
(definidas em config.yaml), com opção de dry-run e log de operações.
"""

from __future__ import annotations

import logging
import shutil
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

import yaml

logger = logging.getLogger("organizador")


@dataclass
class MoveResult:
    origem: Path
    destino: Path
    categoria: str


def carregar_config(config_path: Path) -> dict:
    """Carrega o mapeamento de extensões -> categoria a partir de um YAML."""
    if not config_path.exists():
        raise FileNotFoundError(f"Arquivo de config não encontrado: {config_path}")

    with config_path.open("r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}

    categorias = data.get("categorias", {})
    if not categorias:
        raise ValueError("Config inválido: nenhuma categoria definida em 'categorias'.")

    # normaliza extensões para minúsculo e com ponto
    normalizado: dict[str, str] = {}
    for categoria, extensoes in categorias.items():
        for ext in extensoes:
            ext_norm = ext.lower() if ext.startswith(".") else f".{ext.lower()}"
            normalizado[ext_norm] = categoria

    return {
        "extensao_para_categoria": normalizado,
        "categoria_outros": data.get("categoria_outros", "Outros"),
        "organizar_por_data": data.get("organizar_por_data", False),
    }


def categoria_do_arquivo(arquivo: Path, mapa_extensoes: dict[str, str], categoria_outros: str) -> str:
    ext = arquivo.suffix.lower()
    return mapa_extensoes.get(ext, categoria_outros)


def montar_destino(base: Path, categoria: str, arquivo: Path, organizar_por_data: bool) -> Path:
    pasta_destino = base / categoria
    if organizar_por_data:
        data_mod = datetime.fromtimestamp(arquivo.stat().st_mtime)
        pasta_destino = pasta_destino / f"{data_mod.year}" / f"{data_mod.month:02d}"
    return pasta_destino


def resolver_conflito(destino: Path) -> Path:
    """Se já existe um arquivo com o mesmo nome no destino, adiciona sufixo numérico."""
    if not destino.exists():
        return destino

    stem, suffix = destino.stem, destino.suffix
    contador = 1
    novo_destino = destino
    while novo_destino.exists():
        novo_destino = destino.with_name(f"{stem} ({contador}){suffix}")
        contador += 1
    return novo_destino


def organizar_pasta(
    origem: Path,
    config: dict,
    dry_run: bool = False,
    recursivo: bool = False,
) -> list[MoveResult]:
    """
    Organiza os arquivos de `origem` em subpastas por categoria.
    Retorna a lista de movimentações feitas (ou que seriam feitas, no dry-run).
    """
    if not origem.exists() or not origem.is_dir():
        raise NotADirectoryError(f"Pasta de origem inválida: {origem}")

    mapa_extensoes = config["extensao_para_categoria"]
    categoria_outros = config["categoria_outros"]
    organizar_por_data = config["organizar_por_data"]

    padrao_glob = "**/*" if recursivo else "*"
    resultados: list[MoveResult] = []

    for item in sorted(origem.glob(padrao_glob)):
        if item.is_symlink() or not item.is_file():
            continue
        if item.name.startswith(".") or item.name.lower() in {"thumbs.db", "desktop.ini"}:
            continue
        # não reprocessa o que já está numa pasta de categoria (senão o modo
        # recursivo aninha Imagens/foto.jpg de novo em Imagens/Imagens/)
        categorias_conhecidas = set(mapa_extensoes.values()) | {categoria_outros}
        if any(parte in categorias_conhecidas for parte in item.relative_to(origem).parts[:-1]):
            continue

        categoria = categoria_do_arquivo(item, mapa_extensoes, categoria_outros)
        pasta_destino = montar_destino(origem, categoria, item, organizar_por_data)
        destino_final = resolver_conflito(pasta_destino / item.name)

        resultados.append(MoveResult(origem=item, destino=destino_final, categoria=categoria))

        if dry_run:
            logger.info("[DRY-RUN] %s -> %s", item.name, destino_final.relative_to(origem))
            continue

        pasta_destino.mkdir(parents=True, exist_ok=True)
        shutil.move(str(item), str(destino_final))
        logger.info("Movido: %s -> %s", item.name, destino_final.relative_to(origem))

    return resultados
