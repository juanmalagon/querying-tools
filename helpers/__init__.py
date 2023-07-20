import logging
from helpers.handler import Handler

# Set up logging
logging.basicConfig(
    level=logging.DEBUG,
    format="%(asctime)-s %(levelname)-s [%(module)s|%(funcName)s]%(message)s"
    )

# Create handler
handler = Handler()
