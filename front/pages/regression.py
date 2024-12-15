import sys
import os
from copy import deepcopy
from io import StringIO
import time
import subprocess
import socket

import streamlit as st
import pandas as pd
from autogluon.tabular import TabularPredictor
from sklearn.preprocessing import OneHotEncoder
import ray

__chat_pandas_path = (
    "/".join(
        os.path.dirname(os.path.abspath(__file__)).replace("\\", "/").split("/")[:-2]
    )
)
sys.path.append(__chat_pandas_path)

from ChatPandas.config import *
from ChatPandas.logger import configure_logger
from ChatPandas.cp import *
from ChatPandas.prompt import *


logger = configure_logger(__name__)


# 模拟用户登录
def login(username, password):
    return username == "admin" and password == "123456"

def logout():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
        
def get_local_ip():
    # 获取本机的局域网 IP 地址
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.settimeout(0)
    try:
        # 连接到一个外部地址（这里我们使用Google的公共 DNS）
        s.connect(('10.254.254.254', 1))  
        ip = s.getsockname()[0]  # 获取本机的 IP 地址
    except Exception:
        ip = '127.0.0.1'  # 如果没有连接成功，则返回 localhost 地址
    finally:
        s.close()
    return "127.0.0.1"
def start_ray():
    if not ray.is_initialized():
        ray.init(ignore_reinit_error=True)  # 初始化 Ray
    local_ip = get_local_ip()  # 获取本机局域网 IP 地址
    return f"http://{local_ip}:8265"  # 返回 Ray 仪表盘的 URL

# 2. 使用 AutoGluon 进行模型训练
def fit_auto_gluon_model(train_data, label_column):
    # 启动 Ray 和获取仪表盘 URL
    ray_dashboard_url = start_ray()
    # 嵌入 Ray 仪表盘的 iframe
    st.write("### Ray 仪表盘：")
    st.components.v1.iframe(ray_dashboard_url, height=1200)

    # 训练 AutoGluon 模型
    predictor = TabularPredictor(label=label_column).fit(train_data, verbosity=4)

    # 返回模型预测器和 Ray 仪表盘 URL
    return predictor

# 显示模型拟合结果
def display_results(predictor):
    results = predictor.leaderboard(silent=True)
    st.write("模型拟合结果", results)

# 左侧登录栏
if "logged_in" not in st.session_state:
    st.sidebar.title("登录")
    username = st.sidebar.text_input("用户名")
    password = st.sidebar.text_input("密码", type="password")
    if st.sidebar.button("登录"):
        if login(username, password):
            st.session_state["logged_in"] = True
            st.session_state["username"] = username
            st.sidebar.success("登录成功！")
        else:
            st.session_state["logged_in"] = False
            st.sidebar.error("用户名或密码错误！")
else:
    if st.sidebar.button("登出"):
        logout()


if st.session_state.get("logged_in", False):
    st.title("机器学习")
    # 显示数据集的部分，供用户选择
    df = st.session_state["df"][-1]
    st.write("数据预览", df.head())

    # 创建下拉框选择目标列
    label_column = st.selectbox('选择目标列(label)', df.columns)

    # 创建多选框选择特征列
    feature_columns = st.multiselect('选择特征列(features)', df.columns.tolist(), default=df.columns.tolist())

    # 创建True/False按钮来选择是否对特征进行One-Hot编码
    one_hot_encoding = st.radio('是否进行One-Hot编码？', ('True', 'False'))

    if st.button("开始训练模型"):
        # 处理数据
        if one_hot_encoding == 'True':
            # One-Hot编码
            encoder = OneHotEncoder()
            feature_data = encoder.fit_transform(df[feature_columns])
            feature_columns = encoder.get_feature_names_out(feature_columns)
            feature_data = pd.DataFrame(feature_data, columns=feature_columns)
        else:
            # 不进行编码
            feature_data = df[feature_columns]
            
        # 将label列和特征列组合起来
        train_data = pd.concat([feature_data, df[label_column]], axis=1)


        # 用于捕获标准输出
        log_container = st.empty()  # 用于显示日志的容器

        # 用于保存日志的StringIO对象
        log_output = io.StringIO()
        sys.stdout = log_output 

        # 训练并实时更新日志
        with st.spinner('训练中...'):
            st.session_state["predictor"] = fit_auto_gluon_model(train_data, label_column)
            

    # 显示模型拟合结果
    def display_results(predictor):
        results = predictor.leaderboard(silent=True)
        print(results)
        st.write("模型拟合结果", results)

    # 显示训练结果
    if st.button("显示模型结果"):
        display_results(st.session_state["predictor"])



    
