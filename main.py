"""
main.py

CLI do organizador de arquivos.

Uso:
    python main.py /caminho/da/pasta
    python main.py /caminho/da/pasta --dry-run
    python main.py /caminho/da/pasta --recursivo --config minha_config.yaml
"""

import argparse
import logging
from pathlib import Path

from organizer import carregar_config, organizar_pasta

DEFAULT_CONFIG = Path(__file__).parent / "config.yaml"


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Organiza arquivos de uma pasta em subpastas por categoria (extensão)."
    )
    parser.add_argument("pasta", type=Path, help="Caminho da pasta a ser organizada")
    parser.add_argument(
        "--config",
        type=Path,
        default=DEFAULT_CONFIG,
        help="Caminho do arquivo config.yaml (padrão: config.yaml na raiz do projeto)",
    )
    parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Simula a organização sem mover nenhum arquivo de fato",
    )
    parser.add_argument(
        "--recursivo",
        action="store_true",
        help="Organiza também os arquivos em subpastas",
    )
    parser.add_argument(
        "-v", "--verbose",
        action="store_true",
        help="Ativa log detalhado (DEBUG)",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()

    logging.basicConfig(
        level=logging.DEBUG if args.verbose else logging.INFO,
        format="%(asctime)s | %(levelname)-8s | %(message)s",
        datefmt="%H:%M:%S",
    )
    logger = logging.getLogger("organizador")

    try:
        config = carregar_config(args.config)
    except (FileNotFoundError, ValueError) as e:
        logger.error(str(e))
        raise SystemExit(1)

    resultados = organizar_pasta(
        origem=args.pasta,
        config=config,
        dry_run=args.dry_run,
        recursivo=args.recursivo,
    )

    modo = "seriam movidos (dry-run)" if args.dry_run else "movidos"
    logger.info("Concluído: %d arquivo(s) %s.", len(resultados), modo)


if __name__ == "__main__":
    main()
