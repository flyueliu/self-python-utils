from common_logger import CommonLogger
from slfj_logger import Sl4jLogger
logger = CommonLogger()


class User():

    def __init__(self):
        logger.debug("user init")

    def get(self):
        print(id(logger))
        logger.info("get user")


if __name__ == '__main__':
    logger.info("programmer execute")
    u = User()
    u.get()
