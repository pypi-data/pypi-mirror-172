import datetime
import logging

# Create a logger
logger = logging.getLogger(__name__)

# Add a file handler
now = datetime.datetime.now().strftime("%Y%m%d")
fh = logging.FileHandler(f"pylabrobot-{now}.log")
fh.setLevel(logging.DEBUG)
fh.setFormatter(logging.Formatter("%(asctime)s - %(name)s - %(levelname)s - %(message)s"))
logger.addHandler(fh)
