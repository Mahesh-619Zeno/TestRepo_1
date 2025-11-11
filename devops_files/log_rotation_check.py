import logging
from logging.handlers import RotatingFileHandler

handler = RotatingFileHandler("app.log", maxBytes=2000, backupCount=3)
logger = logging.getLogger("rotation_test")
logger.setLevel(logging.INFO)
logger.addHandler(handler)

for i in range(100):
    logger.info(f"Log entry {i}")

print("✅ Log rotation test completed. Check generated log files.")
