import logging
import os
import sys


def setup_logging(
    log_level=logging.INFO, log_to_file=True, log_file_path="logs/bot.log"
):
    os.makedirs(os.path.dirname(log_file_path), exist_ok=True)

    handlers = [logging.StreamHandler(sys.stdout)]
    if log_to_file:
        handlers.append(logging.FileHandler(log_file_path))

    logging.basicConfig(
        level=log_level,
        format="%(asctime)s - %(levelname)s - %(message)s",
        handlers=handlers,
    )
