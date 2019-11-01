import os
from pydantic import BaseModel
from config import logger


class Cmd(BaseModel):
    cmd: str


async def local_run(cmd: Cmd):
    logger.info(cmd)
    result = {'result': os.popen(cmd.cmd).read()}
    logger.info(result)
    return result
