# %(levelno)s：打印日志级别的数值
# %(levelname)s：打印日志级别的名称
# %(pathname)s：打印当前执行程序的路径，其实就是sys.argv[0]
# %(filename)s：打印当前执行程序名
# %(funcName)s：打印日志的当前函数
# %(lineno)d：打印日志的当前行号
# %(asctime)s：打印日志的时间
# %(thread)d：打印线程ID
# %(threadName)s：打印线程名称
# %(process)d：打印进程ID
# %(message)s：打印日志信息

class CommonLogger(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            import logging
            formatter_style = '%(asctime)s - %(name)s.%(funcName)s:%(lineno)d - [%(levelname)s] - %(message)s'
            formatter = logging.Formatter(formatter_style)
            logging.basicConfig(level=logging.DEBUG,
                                format=formatter_style)
            handler = logging.FileHandler("log.txt")
            handler.setFormatter(formatter)
            print(__name__)
            logger = logging.getLogger(__name__)
            logger.addHandler(handler)
            cls._instance = logger
        return cls._instance


def get(logger):
    logger.debug("get function debug")


logger = CommonLogger()

if __name__ == '__main__':
    logger.info("Start print log")
    logger.debug("Do something")
    logger.warning("Something maybe fail.")
    logger.info("Finish")
    get(logger)
    print(id(logger))
    import logger_test

    u = logger_test.User()
    u.get()
