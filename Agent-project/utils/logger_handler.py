#日志工具，时刻输出日志

import logging
import os
from utils.path_tool import get_abs_path
from datetime import datetime


#日志保存的根目录
LOG_ROOT = get_abs_path("logs")

#确保日志的目录存在  (如果日志不存在，则创建这个目录)
os.makedirs(LOG_ROOT, exist_ok=True)

 
#日志的格式配置
DEFAULT_LOG_FORMAT = logging.Formatter(
    '%(asctime)s - %(name)s - %(levelname)s - %(filename)s:%(lineno)d - %(message)s'
)
    
#LHL

def get_logger(
        name: str = "agent",
        console_level: int = logging.INFO,  #输出info级别以上的日志
        file_level: int = logging.DEBUG,
        log_file = None,
) -> logging.Logger:
    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)

    #避免重复添加Handler  如果没写这个if日志会重复打印
    if logger.handlers:
        return logger

    #控制台Handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(console_handler)


    #文件Handler
    if not log_file:      #日志文件的存放路劲（绝对路径）
        log_file = os.path.join(LOG_ROOT,f"{name}_{datetime.now().strftime('%Y%m%d')}.log")
    
    file_handler = logging.FileHandler(log_file,encoding='utf-8')
    file_handler.setLevel(file_level)   #文件日志的级别
    file_handler.setFormatter(DEFAULT_LOG_FORMAT)

    logger.addHandler(file_handler)

    return logger


#快捷获取日志器
logger = get_logger()



if __name__ == '__main__':
    logger.info("信息日志")
    logger.error("错误日志")
    logger.warning("警告日志")
    logger.debug("调试日志")