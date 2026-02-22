
import streamlit as st
import time

# --- 页面基础配置 ---
st.set_page_config(page_title="N2沉浸式通关引擎", page_icon="🏮", layout="wide")

# --- 沉浸式 CSS 样式 ---
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;500&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Noto Sans JP', sans-serif;
        background-color: #0e1117;
        color: #ffffff;
    }
    .stApp { background: linear-gradient(135deg, #0f172a 0%, #1e1b4b 100%); }
    
    /* 学习卡片样式 */
    .lesson-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        padding: 25px;
        border-radius: 20px;
        margin-bottom: 20px;
        backdrop-filter: blur(10px);
    }
    .vocab-row {
        display: flex;
        align-items: center;
        justify-content: space-between;
        padding: 10px;
        border-bottom: 1px solid rgba(255, 255, 255, 0.05);
    }
    .jp-text { font-size: 1.2rem; font-weight: 500; color: #60a5fa; }
    .tr-text { color: #94a3b8; font-size: 0.9rem; transition: 0.3s; opacity: 0.1; }
    .vocab-row:hover .tr-text { opacity: 1; }
    
    /* 播放按钮样式 */
    .play-btn {
        background: none;
        border: none;
        color: #fbbf24;
        cursor: pointer;
        font-size: 1.2rem;
    }
    </style>
    """, unsafe_allow_html=True)

# --- JavaScript 语音引擎 (Web Speech API) ---
def play_audio(text):
    js_code = f"""
    <script>
    var msg = new SpeechSynthesisUtterance('{text}');
    msg.lang = 'ja-JP';
    msg.rate = 0.8;
    window.speechSynthesis.speak(msg);
    </script>
    """
    st.components.v1.html(js_code, height=0)

# --- 侧边栏：导航与进度 ---
st.sidebar.title("🏮 90天 N2 计划")
current_day = st.sidebar.select_slider("选择日期", options=list(range(1, 91)), value=1)
current_lesson = st.sidebar.radio("选择课时", ["第1课时 (核心精讲)", "第2课时 (强化训练)"])

st.sidebar.markdown("---")
st.sidebar.metric("学习时长累计", f"{current_day*80} 分钟")
st.sidebar.progress(current_day / 90)

# --- 主界面逻辑 ---
st.title(f"Day {current_day}: {current_lesson}")

# 1. 课前 2 分钟回顾测试 (非第一天第一课时)
if not (current_day == 1 and current_lesson == "第1课时 (核心精讲)"):
    with st.expander("🔔 课前 2 分钟：昨日词汇抽测", expanded=True):
        st.write("请写出下列单词的读音或意思：")
        st.info("捗る (はかどる) / 堪える (こたえる) / 補う (おぎなう)")
        ans = st.text_input("在这里输入答案...", placeholder="输入答案后按回车")
        if ans: st.success("复习得不错！进入今日新课。")

# 2. 核心教学区
col1, col2 = st.columns([2, 1])

with col1:
    st.markdown('<div class="lesson-card">', unsafe_allow_html=True)
    st.subheader("📖 核心词汇与句型精讲")
    
    # 这里定义每一课的内容逻辑 (以第一天为例)
    content = {
        "核心词": [
            ("割り当てる", "わりあてる", "分配、分摊"),
            ("見なす", "みなす", "看作、认为"),
            ("執着", "しゅうちゃく", "执着、留恋")
        ],
        "例句": [
            ("仕事を各チームに割り当てる。", "把工作分配给各小组。"),
            ("それは一種の拒否と見なされる。", "那被看作是一种拒绝。")
        ]
    }

    st.write("点击 🔊 听发音并查看翻译：")
    for word, kana, trans in content["核心词"]:
        c_p, c_t, c_btn = st.columns([2, 3, 1])
        with c_p: st.markdown(f"<span class='jp-text'>{word}</span> <br><small>{kana}</small>", unsafe_allow_html=True)
        with c_t: st.markdown(f"<span class='tr-text'>{trans}</span>", unsafe_allow_html=True)
        with c_btn:
            if st.button("🔊", key=word):
                play_audio(word)

    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    st.subheader("⏱️ 专注计时")
    if st.button("开启 40 分钟沉浸模式"):
        st.toast("计时开始，手机请静音")
        with st.empty():
            for i in range(40*60, 0, -10):
                st.write(f"⏳ 剩余时间: {i//60}分{i%60}秒")
                time.sleep(0.1) # 演示用

# 3. 课后：30个 N2 真题常用单词
st.markdown("---")
st.subheader("🎯 课后冲刺：N2 真题高频词 (30个)")

# 模拟30个真题词汇
exam_words = [
    ("合致", "一致、符合"), ("兆し", "征兆"), ("素朴", "淳朴"),
    ("妥協", "妥协"), ("漠然", "模糊"), ("閲覧", "阅读")
] # 实际可扩充至30个

cols = st.columns(3)
for i, (w, m) in enumerate(exam_words):
    with cols[i % 3]:
        st.markdown(f"""
        <div style="background:rgba(255,255,255,0.03); padding:10px; border-radius:10px; margin:5px;">
            <b style="color:#fbbf24;">{w}</b>: {m}
        </div>
        """, unsafe_allow_html=True)

# 4. 页脚美化
st.markdown("<br><br><center style='color:#4b5563'>每一步努力，都在拉近你与日本的距离</center>", unsafe_allow_html=True)
