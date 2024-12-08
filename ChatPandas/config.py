from dataclasses import dataclass

@dataclass
class OpenaiConfig:
    api_key: str
    model: str
    base_url: str
    max_retrys: int = 5
    
@dataclass
class HistoryConfig:
    file_folder: str
    file_name: str = "history.py"
    
@dataclass
class PromptConfig:
    use_rationale: bool = True
    need_df_header: bool = True
    

# def load_config(file_path):
#     with open(file_path, "r") as f:
#         lines = f.readlines()

#     config = {}
#     for line in lines:
#         key, value = line.strip().split("=")
#         config[key] = value

#     return OpenaiConfig(**config), History(**config), PromptConfig(**config)

    