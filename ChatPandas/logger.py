import logging

# 定义全局日志级别
GLOBAL_LOG_LEVEL = logging.DEBUG

# 自定义日志级别名称和数值
ITEM_LOG_LEVEL_NAME = "ITEM"
ITEM_LOG_LEVEL = 25  # 在 INFO 和 WARNING 之间的级别

# 注册自定义日志级别
logging.addLevelName(ITEM_LOG_LEVEL, ITEM_LOG_LEVEL_NAME)

class ColoredFormatter(logging.Formatter):
    # 定义前景色和背景色的转义序列
    COLOR_CODES = {
        "DEBUG": "\033[94m",   # 蓝色
        "INFO": "\033[92m",    # 绿色
        "WARNING": "\033[93m",  # 黄色
        "ERROR": "\033[91m",    # 红色
        "CRITICAL": "\033[91m", # 红色
        "ITEM": "\033[95m",     # 紫色
        "RESET": "\033[0m"      # 重置颜色
    }

    def format(self, record):
        msg = super().format(record)
        color = self.COLOR_CODES.get(record.levelname, self.COLOR_CODES["RESET"])
        return f'{color}{msg}{self.COLOR_CODES["RESET"]}'
    


def configure_logger(name):
    # 创建日志记录器
    logger = logging.getLogger(name)
    if not logger.hasHandlers():  # 确保只配置一次
        # 设置全局日志级别
        logger.setLevel(GLOBAL_LOG_LEVEL)
        
        # 创建控制台处理器并设置日志级别
        ch = logging.StreamHandler()
        ch.setLevel(GLOBAL_LOG_LEVEL)
        
        # 创建格式化器并将其添加到处理器
        formatter = ColoredFormatter('[%(asctime)s] - file: %(name)s - level: [%(levelname)s] : %(message)s')
        ch.setFormatter(formatter)
        
        # 将处理器添加到日志记录器
        if not logger.handlers:  # 避免重复添加处理器
            logger.addHandler(ch)
    
    return logger

# 自定义日志级别方法
def item_log(self, message, *args, **kws):
    if self.isEnabledFor(ITEM_LOG_LEVEL):
        self._log(ITEM_LOG_LEVEL, message, args, **kws)

# 给 logger 类添加自定义日志级别的方法
logging.Logger.item = item_log

def set_log_level(level):
    assert level in ["info", "error", "debug"]
    _level_dict = {
        "info": logging.INFO,
        "error": logging.ERROR,
        "debug": logging.DEBUG,
        "item": ITEM_LOG_LEVEL
    }
    global GLOBAL_LOG_LEVEL
    GLOBAL_LOG_LEVEL = _level_dict[level]
    logging.getLogger().setLevel(GLOBAL_LOG_LEVEL)
    
# set_log_level("info")