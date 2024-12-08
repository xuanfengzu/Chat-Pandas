import os
import io
import json

import pandas as pd

from .agent import *
from .prompt import *
from .config import *
from .logger import configure_logger

logger = configure_logger(__name__)


class History:
    def __init__(self, config):
        self.file_folder = config.file_folder
        self.file_name = config.file_name
        self.history = []  # 存储历史记录
        self.history_lengths = []  # 记录每次写入的代码长度
        
        # 创建一个空的历史记录文件,覆盖掉原来的脚本文件
        with open(os.path.join(self.file_folder, self.file_name), "w") as f:
            f.write("import pandas as pd\n")
            
    def add_history(self, code):
        logger.info("Adding history...")
        self.history.append(code)
        self.history_lengths.append(len(code))  # 记录当前代码长度
        
        # 将代码追加写入文件
        with open(os.path.join(self.file_folder, self.file_name), "a") as f:
            f.write("\n" + code)
            
        return code
    
    def load_history(self):
        logger.info("Loading history...")
        return self.history
    
    def clear_history(self):
        logger.info("Clearing history...")
        self.history = []  # 清空内存中的历史记录
        self.history_lengths = []  # 清空记录的代码长度
        
        # 重置文件内容
        with open(os.path.join(self.file_folder, self.file_name), "w") as f:
            f.write("import pandas as pd\n\ndf = pd.read_csv('df.csv')")
            
    def pop_history(self):
        logger.info("Popping history...")
        
        if not self.history:
            logger.warning("No history to pop!")
            return None
        
        # 从历史记录中移除最后一段代码
        last_code = self.history.pop()
        self.history_lengths.pop()
        
        # 读取当前文件内容
        file_path = os.path.join(self.file_folder, self.file_name)
        with open(file_path, "r") as f:
            file_content = f.readlines()
        
        # 移除文件中的最后一段代码
        if len(file_content) > 1:
            last_code_lines = last_code.count("\n") + 1  # 获取最后代码段的行数
            updated_content = file_content[:-last_code_lines]  # 移除对应行
        else:
            updated_content = ["import pandas as pd\n"]  # 保留基础内容
        
        # 重写文件
        with open(file_path, "w") as f:
            f.writelines(updated_content)
        
        return last_code

class ChatPandas:
    def __init__(self, agent_config, history_config, prompt_config):
        self.history = History(history_config)
        self.agent = Agent(agent_config)
        self.prompt = Prompt(prompt_config)
        
    def chat(self, request, df, use_key=False):
        logger.info("Chatting...")
        
        buffer = io.StringIO()
        df.info(buf=buffer)
        info = buffer.getvalue()
        buffer.close()
        
        head = df.head().to_string()
        
        previous = self.history.load_history()
        
        prompt = self.prompt.get_one_step_prompt(request, previous, info, head)
        # print(prompt)
        
        if use_key:
            answer = self.agent.chat(prompt)
        else:
            answer = self.agent.chat_test(prompt)
        
        if not answer:
            return None
        
        try:
            answer = json.loads(answer)
            return answer
        except Exception as e:
            logger.error(f"Error parsing answer: {e}")
            return None
        
        
        
        
        
        
        
        
        

