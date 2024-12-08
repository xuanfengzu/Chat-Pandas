import json

from openai import OpenAI

from .logger import configure_logger

logger = configure_logger(__file__)

class Agent:
    def __init__(self, config):
        self.reset(config)
        
    def reset(self, config):
        logger.info(f"Agent reset.")
        self.client = OpenAI(
            base_url = config.base_url,
            api_key = config.api_key,
        )
        self.model = config.model
        self.max_retrys = config.max_retrys
        
    def chat(self, prompt, model=None):
        for i in range(self.max_retrys):
            try:
                response = self.client.chat.completions.create(
                    model = model if model else self.model,
                    messages = [
                        {"role": "system", "content": "You are a helpful assistant."},
                        {"role": "user", "content": prompt},
                    ],
                )
                logger.info(f"API call succeeded.")
                return response.choices[0].message.content
            except:
                logger.warning(f"API call failed, retrying {i+1}/{self.max_retrys}")
                continue
        logger.error(f"API call failed after {self.max_retrys} retrys. Please check quota or proxies.")
        return None
    
    def chat_test(self, prompt):
        logger.debug("Using the test chat.")
        results = [
            json.dumps({
            "code": "```df.dropna(inplace=True)\ndf.iloc[0] = df.iloc[6].mean()```",
            "rationale": "The code first drops any rows with NaN values using `dropna()` with `inplace=True` to modify the dataframe directly. Then, it replaces the values in the first column (column 0) with the mean of that column, calculated by `df[0].mean()`."
        }),
            json.dumps({
                "code": "```python\ndf.iloc[:,1] = df.iloc[:,1].mean()```"
            })
        ]
        import random
        return random.choice(results)
        
        
        
        