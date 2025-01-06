import sys
import logging

def setup_default_logger(debug: bool = False) -> None:
    logging.basicConfig(
        format="[%(asctime)s - %(relativeCreated)9d] %(levelname)-8s | %(module)s:%(lineno)s:%(funcName)s | %(message)s",
        level=logging.DEBUG if debug else logging.INFO,
        handlers=[
            logging.StreamHandler(sys.stdout),
        ],
    )