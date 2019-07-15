import sys


class Sl4jLogger(object):
    _instance = None

    def __new__(cls, *args, **kwargs):
        # 单例模式: cls: 相当于该类的Class对象
        if cls._instance is None:
            from loguru import logger
            # 如果有填充file 字段，则日志输出到该文件中
            # For scripts
            message_format = '''<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> |<level>{level: <5}</level> |<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>'''
            config = {
                "handlers": [
                    {"sink": sys.stdout,
                     # 输出日志的格式
                     "format": message_format,
                     # 只输出DEBUG级别以上的信息
                     'level': 'DEBUG',
                     },
                    {"sink": "file.log", 'level': 'DEBUG', 'format': message_format, 'encoding': 'utf-8'},
                ]
            }

            logger.configure(**config)
            # logger.info("No matter added sinks, this message is not displayed")
            # logger.info("This message however is propagated to the sinks")
            cls._instance = logger
        return cls._instance


if __name__ == '__main__':
    logger = Sl4jLogger()
    print(id(logger))
    logger.debug("{}", "debug formart")
    logger.info("If you're using Python {}, prefer {feature} of course!", 3.6, feature="f-strings")
    logger.debug("{name}", name="you name")
    try:
        a = 1 / 0
    except Exception as e:
        # 只输出异常的message
        logger.error("{}", e)
        # 输出异常的message+ 异常的堆栈信息
        logger.exception(e)
    import logger_test
    u=logger_test.User()
    u.get()