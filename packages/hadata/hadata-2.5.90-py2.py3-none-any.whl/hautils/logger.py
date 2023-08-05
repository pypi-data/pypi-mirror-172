import logging
from uvicorn.logging import ColourizedFormatter


logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

standard = logging.StreamHandler()
standard.setLevel(logging.INFO)

formatter = ColourizedFormatter(fmt=(
    "%(levelprefix)-8s %(asctime)-15s - "
    "%(filename)10s:%(lineno)-3d - %(message)s"))

standard.setFormatter(formatter)
logger.addHandler(standard)