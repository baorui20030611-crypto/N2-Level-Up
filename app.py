
import streamlit as st

# ==========================================
# 1. 页面配置与核心 CSS / JS 引擎
# ==========================================
st.set_page_config(page_title="N2沉浸式通关引擎 - 第一周", page_icon="⛩️", layout="wide")

st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@300;400;700&display=swap');
    
    .stApp { background-color: #0d1117; color: #c9d1d9; font-family: 'Noto Sans JP', sans-serif; }
    
    /* 核心词汇卡片 */
    .word-card {
        background: #161b22; border: 1px solid #30363d; border-radius: 10px;
        padding: 15px; margin-bottom: 15px; display: flex; align-items: center; justify-content: space-between;
    }
    .word-jp { font-size: 1.4rem; color: #58a6ff; font-weight: bold; width: 30%; }
    .word-tr { font-size: 1rem; color: #8b949e; opacity: 0; transition: opacity 0.3s ease; width: 60%; }
    .word-card:hover .word-tr { opacity: 1; color: #e6edf3; } /* 鼠标悬停显现翻译 */
    
    /* 句子解剖交互盒子 */
    .sentence-box {
        background: #21262d; border-left: 4px solid #8957e5; border-radius: 8px;
        padding: 15px; margin-bottom: 15px; cursor: pointer;
        transition: all 0.3s ease; overflow: hidden; height: 60px;
    }
    .sentence-box.expanded { height: auto; background: #161b22; transform: scale(1.02); border-color: #2ea043; }
    .sen-jp { font-size: 1.3rem; color: #c9d1d9; margin-bottom: 10px; }
    .sen-tr { display: none; color: #fbbf24; font-size: 1rem; border-top: 1px dashed #30363d; padding-top: 10px; }
    .sen-note { display: none; color: #8b949e; font-size: 0.9rem; margin-top: 8px; }
    .sentence-box.expanded .sen-tr, .sentence-box.expanded .sen-note { display: block; }
    
    /* 前端语音按钮 (瞬间响应) */
    .play-btn {
        background: #238636; color: white; border: none; border-radius: 5px;
        padding: 5px 10px; cursor: pointer; font-size: 1rem; margin-left: 10px;
    }
    .play-btn:hover { background: #2ea043; }
    
    /* 词性颜色标签 */
    .tag-core { color: #ff7b72; font-weight: bold; } /* 核心词 红色 */
    .tag-adv { color: #79c0ff; font-weight: bold; }  /* 副词 蓝色 */
    .tag-conj { color: #d2a8ff; font-weight: bold; } /* 连接词 紫色 */
    </style>

    <script>
    function speakJS(text, event) {
        if(event) event.stopPropagation(); // 阻止点击事件冒泡，防止触发盒子的缩放
        window.speechSynthesis.cancel();   // 停止上一个语音
        let msg = new SpeechSynthesisUtterance(text);
        msg.lang = 'ja-JP'; msg.rate = 0.85; msg.pitch = 1.0;
        window.speechSynthesis.speak(msg);
    }
    function toggleBox(element) {
        element.classList.toggle('expanded');
    }
    </script>
""", unsafe_allow_html=True)


# ==========================================
# 2. 课程数据结构 (此处以 Day 1 - L1 为例)
# ==========================================
# 未来 180 节课的数据都可以按这个格式填充
database = {
    "Day1_L1": {
        "title": "职场与生活效率篇 (动词精讲)",
        "core_words": [
            ("捗る", "はかどる", "进展顺利。例：仕事が捗る。", "はかどる"),
            ("割り当てる", "わりあてる", "分配。例：仕事を割り当てる。", "わりあてる"),
            ("備え付ける", "そなえつける", "设置/装备。例：エアコンを備え付ける。", "そなえつける"),
            ("打ち合わせる", "うちあわせる", "商量。例：詳細を打ち合わせる。", "うちあわせる"),
            ("見合わせる", "みあわせる", "暂停/推迟。例：出発を見合わせる。", "みあわせる")
        ],
        "essay": [
            {
                "jp": "今日の仕事は<span class='tag-adv'>とても</span><span class='tag-core'>捗りました</span>。",
                "pure_jp": "今日の仕事はとても捗りました。", # 用于语音朗读的纯文本
                "tr": "今天的工作进展非常顺利。",
                "note": "【とても】副词，修饰后面的核心动词【捗る】(进展顺利)。"
            },
            {
                "jp": "<span class='tag-conj'>なぜなら</span>、上司が適切に業務を<span class='tag-core'>割り当てて</span>くれたからです。",
                "pure_jp": "なぜなら、上司が適切に業務を割り当ててくれたからです。",
                "tr": "因为上司妥善地分配了任务。",
                "note": "【なぜなら】因果连接词；【割り当てる】核心动词，分配。"
            },
            {
                "jp": "会議室には新しいモニターが<span class='tag-core'>備え付けられて</span>おり、スムーズに<span class='tag-core'>打ち合わせる</span>ことができました。",
                "pure_jp": "会議室には新しいモニターが備え付けられており、スムーズに打ち合わせることができました。",
                "tr": "会议室里安装了新的显示器，沟通商量得非常顺畅。",
                "note": "【備え付ける】安装/装备；【打ち合わせる】碰头商量。"
            }
        ],
        "sprint_30": ["合致", "兆し", "素朴", "妥協", "漠然", "閲覧", "一転", "安堵", "会得", "概説", 
                      "該当", "介入", "各界", "拡充", "確保", "加味", "関与", "慣習", "棄権", "規制", 
                      "拒絶", "許容", "起用", "議決", "却下", "救済", "強要", "均衡", "駆使", "駆除"]
    }
}


# ==========================================
# 3. 侧边栏导航 (第一周专属)
# ==========================================
st.sidebar.title("🏮 第一周：筑基期 (Day 1 - 7)")
day = st.sidebar.slider("选择学习天数", 1, 7, 1)
lesson = st.sidebar.radio("选择课时", ["第1课时 (核心精讲)", "第2课时 (强化演练)"])

course_key = f"Day{day}_L{1 if '第1' in lesson else 2}"

st.sidebar.markdown("---")
st.sidebar.write("🎵 **专注环境控制**")
if st.sidebar.button("▶️ 播放纯音乐 (Lo-Fi)"):
    st.sidebar.audio("https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3", format="audio/mp3")

# ==========================================
# 4. 主界面渲染逻辑
# ==========================================
# 获取当前课时数据，如果没有则显示开发中
data = database.get(course_key, None)

if data:
    st.title(f"⚓ Day {day} - {lesson}：{data['title']}")

    # --- 模块 A: 课前 2 分钟回顾 ---
    if day > 1 or "第2" in lesson:
        with st.expander("🔔 课前抽测 (点击展开)"):
            st.info("凭借记忆写出昨日重点词的意思：")
            st.text_input("1. 捗る (はかどる)", key="review1")
            st.text_input("2. 割り当てる (わりあてる)", key="review2")

    # --- 模块 B: 核心单词精讲 ---
    st.markdown("### 📚 核心精讲区")
    st.caption("💡 提示：鼠标悬停在卡片上显示翻译，点击 🔊 瞬间朗读。")
    
    for word, kana, trans, pure_jp in data['core_words']:
        html_word = f"""
        <div class="word-card">
            <div class="word-jp">{word} <span style="font-size:0.8rem;color:#8b949e">({kana})</span></div>
            <div class="word-tr">{trans}</div>
            <button class="play-btn" onclick="speakJS('{pure_jp}')">🔊</button>
        </div>
        """
        st.markdown(html_word, unsafe_allow_html=True)

    # --- 模块 C: 沉浸式小作文解剖 (新增极其灵敏的发音) ---
    st.markdown("---")
    st.markdown("### 📝 沉浸式小作文解剖")
    st.caption("💡 提示：点击整个句子方块可**放大并查看解析**。点击句子内的 🔊 按钮可**单独朗读该句**。")
    
    for i, sen in enumerate(data['essay']):
        html_sentence = f"""
        <div class="sentence-box" onclick="toggleBox(this)">
            <div class="sen-jp">
                {sen['jp']}
                <button class="play-btn" onclick="speakJS('{sen['pure_jp']}', event)">🔊 读此句</button>
            </div>
            <div class="sen-tr">🇨🇳 翻译：{sen['tr']}</div>
            <div class="sen-note">🔍 解析：{sen['note']}</div>
        </div>
        """
        st.markdown(html_sentence, unsafe_allow_html=True)

    # --- 模块 D: 课后 30 词冲刺 ---
    st.markdown("---")
    st.markdown("### 🎯 课后 30 词极速扫描")
    
    cols = st.columns(6)
    for i, word in enumerate(data['sprint_30']):
        with cols[i % 6]:
            st.markdown(f"<div style='background:#161b22; padding:8px; text-align:center; border-radius:5px; margin-bottom:10px; border:1px solid #30363d;'>{word}</div>", unsafe_allow_html=True)

else:
    st.warning(f"🚧 恭喜你太超前了！{course_key} 的教案数据正在按计划编写导入中，请先复习已有课程。")
