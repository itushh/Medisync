import logging

logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

console_handler = logging.StreamHandler()
console_handler.setLevel(logging.INFO)

formatter = logging.Formatter(
    "[%(asctime)s] [%(levelname)s] [%(name)s]: %(message)s"
)
console_handler.setFormatter(formatter)

logger.addHandler(console_handler)

""" USE CASE
logger.info("Server started")
logger.error("Something went wrong")
"""