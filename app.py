import streamlit as st
import random

# 设置页面
st.set_page_config(page_title="N2 Level-Up Engine", page_icon="🎮")

# 初始化游戏状态
if 'coins' not in st.session_state:
    st.session_state.coins = 0
if 'level' not in st.session_state:
    st.session_state.level = 1

st.title("⛩️ N2 日语通关引擎 v1.0")

# 侧边栏：状态栏
with st.sidebar:
    st.header("👤 玩家状态")
    st.metric("金币 (J-Coins)", st.session_state.coins)
    st.metric("等级 (Level)", st.session_state.level)
    st.write("---")
    st.write("🎧 正在播放：Alpha波专注音乐")
    # 这里可以插入音乐链接
    st.audio("https://www.soundhelix.com/examples/mp3/SoundHelix-Song-1.mp3") 

# 核心任务区
st.header("🔥 今日通关任务")
task_tab, code_tab = st.tabs(["核心知识点", "代码挑战"])

with task_tab:
    st.subheader("今日词汇 (Vocabulary)")
    # 这里以后放我每天发给你的数据
    words = ["先生 (Sensei)", "学校 (Gakkou)", "勉強 (Benkyou)"]
    for word in words:
        st.checkbox(f"已掌握：{word}")

with code_tab:
    st.code("""
    # Python 语法挑战：
    # 请补全这个 N2 '～たとたん' 的逻辑
    def on_event(action):
        if action == "站起来":
            print("突然头晕了") # 对应：立ち上がったとたん、めまいがした。
    """, language='python')

# 结算按钮
if st.button("完成今日任务并领取金币"):
    st.session_state.coins += 10
    st.balloons()
    st.success("获得 10 金币！今日份大脑记忆已同步。")
