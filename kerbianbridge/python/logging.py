import logging

def setup_logging(logfile="kerbianbridge.log"):
    logging.basicConfig(
        filename=logfile,
        filemode="a",
        format="%(asctime)s [%(levelname)s] %(message)s",
        level=logging.INFO
    )
    logger = logging.getLogger("KerbianBridge")
    return logger