import sys
import os
import logging

__chat_pandas_path = (
    "/".join(
        os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[:-1]
    )
)
sys.path.append(__chat_pandas_path)

import streamlit as st

from ChatPandas.logger import set_log_level



set_log_level("debug")


st.set_page_config(page_title="Chat-Pandas", page_icon="🐼", layout="wide")

st.sidebar.title("导航")
st.sidebar.markdown(
    """
- **主页**  
- **配置界面**
- **分析界面**
"""
)
# st.sidebar.info("切换页面使用顶部导航栏。")

pg = st.navigation(
    [
        st.Page("./pages/homepage.py"),
        st.Page("./pages/config.py"),
        st.Page("./pages/analysis.py"),
        st.Page("./pages/regression.py")
    ]
)  # , st.Page("./pages/jupyter.py")])
pg.run()
