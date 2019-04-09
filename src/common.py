#!/usr/bin/env python3
from functools import wraps
from loguru import logger

logger.add("logs/%s.log" % __file__.rstrip('.py'), format="{time:MM-DD HH:mm:ss} {level} {message}")

def _try(func):
    @wraps(func)
    def wrapper(*args, **kw):
        try:
            return func(*args, **kw)
        except Exception as err:
            logger.info(err)
            return str(err)

    return wrapper
