from loguru import logger
import pathlib

logger.add("test.log", format="{time} {file} {level} {message}",\
            level="INFO", rotation="1 week", backtrace=True, diagnose=True)

logger.info("HII")
