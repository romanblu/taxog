import logging, sys, json, time
def setup(level="INFO"):
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter(
        '{"ts":"%(asctime)s","lvl":"%(levelname)s","mod":"%(name)s","msg":%(message)s}'
    ))
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level)