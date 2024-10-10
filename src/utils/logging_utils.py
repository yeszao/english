import logging
from pathlib import Path


def init_logging(filename: Path):
    filename.parent.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(format='[%(asctime)s] [%(levelname)s] %(message)s',
                        datefmt='%Y-%d-%m %I:%M:%S',
                        level=logging.INFO,
                        handlers=[logging.FileHandler(filename), logging.StreamHandler()])
