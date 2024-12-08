import streamlit as st

st.title("欢迎使用 Chat-Pandas")

st.markdown(
    """
    ### 页面介绍
    - 首页：显示页面介绍
    - 分析界面：登录后上传 CSV 文件，并显示文件的前 10 行内容
    """
)

st.markdown(
    """
    目前为测试版，功能不完善，可以提供自己的key来测试，也可以使用内置的随机代码来测试。
    """
)

st.markdown(
    """
    如您对该项目有任何意见，欢迎联系我们。
    """
)

st.info("切换到分析界面以体验功能！")