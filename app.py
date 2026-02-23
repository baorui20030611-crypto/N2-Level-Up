import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="N2沉浸式通关引擎 - 终极版", page_icon="⛩️", layout="wide")

# ==========================================
# 核心 HTML/CSS/JS 引擎 (包含刮刮乐防作弊、图例、句句发音)
# ==========================================
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { 
        font-family: 'Noto Sans JP', sans-serif; 
        background-color: #0d1117; color: #c9d1d9; 
        margin: 0; padding: 20px;
        display: flex; justify-content: center;
    }
    .main-container { width: 100%; max-width: 1100px; margin: 0 auto; }
    
    /* 播放按钮 */
    .play-btn { background: #2ea043; color: white; border: none; border-radius: 4px; padding: 4px 10px; cursor: pointer; font-size: 0.9rem; margin-left:10px; transition: 0.2s;}
    .play-btn:hover { background: #3fb950; transform: scale(1.05); }
    
    /* --- 绝对隐藏：刮刮乐防作弊特效 --- */
    .spoiler { 
        background-color: #30363d; color: transparent; 
        border-radius: 4px; padding: 2px 8px; 
        transition: all 0.3s ease; cursor: crosshair; 
        user-select: none;
    }
    .spoiler:hover { background-color: rgba(251,191,36,0.1); color: #fbbf24; border: 1px dashed #fbbf24; }

    /* --- 词性色彩罗盘 --- */
    .pos-verb { color: #ff7b72; font-weight: bold; }       /* 动词：红 */
    .pos-adv { color: #79c0ff; font-weight: bold; }        /* 副词：蓝 */
    .pos-conj { color: #d2a8ff; font-weight: bold; }       /* 接续词：紫 */
    .pos-pron { color: #2ea043; font-weight: bold; }       /* 代词：绿 */
    .pos-adj { color: #ffa657; font-weight: bold; }        /* 连体/形容词：橙 */
    .pos-noun { color: #a5d6ff; font-weight: bold; }       /* 名词：浅蓝 */
    
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.95); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); z-index: 1000; font-size: 0.9rem; }
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }

    /* --- 思维导图样式 --- */
    .mindmap-box { display: flex; align-items: stretch; background: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); overflow: hidden;}
    .mm-root { flex: 0 0 220px; background: #21262d; text-align: center; padding: 30px 20px; border-right: 3px solid #58a6ff; display: flex; flex-direction: column; justify-content: center; align-items: center;}
    .mm-word { font-size: 2.2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .mm-branches { flex: 1; padding: 20px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #0d1117; padding: 15px; border-radius: 8px; border-left: 4px solid #8957e5; }
    .mm-usage { font-size: 1.1rem; color: #e6edf3; font-weight: bold; margin-bottom: 10px; }
    .mm-sentence { font-size: 1.2rem; color: #c9d1d9; margin-bottom: 10px; line-height: 1.5; }
    
    /* --- 逐句解析小作文样式 --- */
    .sen-box { background: #161b22; border: 1px solid #30363d; border-left: 5px solid #2ea043; border-radius: 8px; padding: 20px; margin-bottom: 15px; cursor: pointer; transition: 0.2s; }
    .sen-box:hover { background: #21262d; transform: scale(1.01); }
    .sen-jp { font-size: 1.4rem; color: #ffffff; line-height: 1.6; }
    .blank { display: inline-block; min-width: 60px; text-align: center; color: transparent; border-bottom: 2px dashed #58a6ff; padding: 0 5px; margin: 0 5px; background: rgba(88,166,255,0.1); transition: 0.3s; }
    .blank.revealed { color: #ff7b72; border-bottom: 2px solid #ff7b72; background: rgba(255,123,114,0.1); }
    .sen-details { display: none; margin-top: 15px; border-top: 1px dashed #30363d; padding-top: 15px; }
    .analysis-title { color: #fbbf24; font-weight: bold; margin-bottom: 5px; font-size: 1.1rem; }
    .analysis-content { color: #8b949e; line-height: 1.6; margin-bottom: 10px; font-size: 1rem; background: #0d1117; padding: 10px; border-radius: 5px;}

    /* 30词网格 */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; text-align: center; }
</style>

<script>
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    function toggleSentence(id, blankId, blankWord, pureAudio) {
        // 揭晓填空（如果有）
        if (blankId) {
            let b = document.getElementById(blankId);
            if(b) { b.innerHTML = blankWord; b.classList.add('revealed'); }
        }
        // 展开解析面板
        let detail = document.getElementById('detail_' + id);
        if(detail.style.display === 'block') { detail.style.display = 'none'; } 
        else { detail.style.display = 'block'; }
    }
</script>
"""

# ==========================================
# 顶栏进度与全局 UI
# ==========================================
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown("<h2 style='text-align: center; color: #e6edf3;'>Day 1: 职场与生活效率篇</h2>", unsafe_allow_html=True)
    st.progress(0.01)
    st.markdown("---")

with st.container():
    c_left, c_mid, c_right = st.columns([1, 12, 1])
    with c_mid:
        tab1, tab2, tab3 = st.tabs(["📖 核心词解剖", "📝 教辅级长文精读", "🚀 课后真题 30 词"])

        # ==========================================
        # TAB 1: 核心词解剖 (直观翻译 + 绝对隐藏 + 句句发音)
        # ==========================================
        with tab1:
            mindmap_html = common_head + '<div class="main-container">'
            
            words_data = [
                {
                    "word": "捗る", "kana": "はかどる", "direct_tr": "进展顺利",
                    "usages": [
                        {"meaning": "① 事物或工作顺利进展", "jp": "計画が予定通りに捗っている。", "pure": "けいかくがよていどおりにはかどっている", "tr": "计划正按预期顺利进行。"},
                        {"meaning": "② 搭配副词（とても/順調に）", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。"}
                    ]
                },
                {
                    "word": "割り当てる", "kana": "わりあてる", "direct_tr": "分配/分摊",
                    "usages": [
                        {"meaning": "① 分配任务给具体的人", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。"},
                        {"meaning": "② 分配物理资源（房间、空间）", "jp": "一部屋に二人ずつ割り当てる。", "pure": "ひとへやにふたりずつわりあてる", "tr": "按每间房两个人进行分配。"}
                    ]
                },
                {
                    "word": "備え付ける", "kana": "そなえつける", "direct_tr": "设置/装备",
                    "usages": [
                        {"meaning": "① 在特定场所固定安装机器/家具", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。"}
                    ]
                }
            ]

            for data in words_data:
                mindmap_html += f"""
                <div class="mindmap-box">
                    <div class="mm-root">
                        <div class="mm-word">{data['word']}</div>
                        <div style="color:#8b949e; margin-bottom:10px;">{data['kana']}</div>
                        <div class="spoiler">翻译: {data['direct_tr']}</div>
                        <button class="play-btn" style="margin-top:15px; margin-left:0;" onclick="speak('{data['word']}')">🔊 读原词</button>
                    </div>
                    <div class="mm-branches">
                """
                for u in data['usages']:
                    mindmap_html += f"""
                        <div class="mm-branch">
                            <div class="mm-usage">{u['meaning']}</div>
                            <div class="mm-sentence">{u['jp']} <button class="play-btn" onclick="speak('{u['pure']}')">🔊 读例句</button></div>
                            <div class="spoiler">🇨🇳 {u['tr']}</div>
                        </div>
                    """
                mindmap_html += "</div></div>"
            mindmap_html += "</div>"
            components.html(mindmap_html, height=800, scrolling=True)

        # ==========================================
        # TAB 2: 教辅级长文精读 (融合、挖空、逐句解析、发音)
        # ==========================================
        with tab2:
            essay_html = common_head + """
            <div class="legend-box">
                <div class="legend-title">🧩 N2 词性色彩罗盘</div>
                <div class="legend-item"><div class="color-block" style="background:#ff7b72;"></div> 动词 (Verb)</div>
                <div class="legend-item"><div class="color-block" style="background:#79c0ff;"></div> 副词 (Adv)</div>
                <div class="legend-item"><div class="color-block" style="background:#d2a8ff;"></div> 接续词 (Conj)</div>
                <div class="legend-item"><div class="color-block" style="background:#2ea043;"></div> 代词 (Pron)</div>
                <div class="legend-item"><div class="color-block" style="background:#a5d6ff;"></div> 名词 (Noun)</div>
            </div>
            
            <div class="main-container">
            """
            
            # 逐句数据字典（部分挖空，部分直接标色，教辅级解析）
            sentences = [
                {
                    "id": 1, "blank_id": "b1", "blank_word": "捗りました", "audio": "彼らの今日の仕事はとても捗りました。",
                    "jp": "<span class='pos-pron'>彼ら</span>の今日の<span class='pos-noun'>仕事</span>は<span class='pos-adv'>とても</span><span class='blank' id='b1'>【 1 】</span>。",
                    "tr": "他们今天的工作进展非常顺利。",
                    "analysis": "<b>【N2考点拆解】</b><br>1. <b>とても + 捗る（はかどる）</b>：黄金搭配。表示工作、学习进度远超预期。<br>2. <b>彼ら（かれら）</b>：代词，他们。<br>3. <b>とても</b>：副词，修饰程度。"
                },
                {
                    "id": 2, "blank_id": "", "blank_word": "", "audio": "なぜなら、上司が適切に業務を割り当ててくれたからです。",
                    "jp": "<span class='pos-conj'>なぜなら</span>、上司が適切に業務を<span class='pos-verb'>割り当てて</span>くれたからです。",
                    "tr": "因为上司妥善地分配了任务。",
                    "analysis": "<b>【N2考点拆解】</b><br>1. <b>なぜなら～からだ</b>：N3/N2重点句型，表示补充说明原因。<br>2. <b>割り当てる（わりあてる）</b>：动词，将整体切割后分配给个体（如任务、房间）。本句没有挖空，直接复习用法。<br>3. <b>～てくれる</b>：表示他人为我（或我方）做某事，带感激之情。"
                },
                {
                    "id": 3, "blank_id": "b3", "blank_word": "備え付けられて", "audio": "会議室には新しいモニターが備え付けられており、スムーズに打ち合わせることができました。",
                    "jp": "会議室には新しいモニターが<span class='blank' id='b3'>【 2 】</span>おり、スムーズに<span class='pos-verb'>打ち合わせる</span>ことができました。",
                    "tr": "会议室里安装了新的显示器，沟通商量得非常顺畅。",
                    "analysis": "<b>【N2考点拆解】</b><br>1. <b>備え付ける（そなえつける）</b>：动词，常用于机械、家具的安装配备。这里填入其被动状态「備え付けられており」。<br>2. <b>打ち合わせる（うちあわせる）</b>：碰头、商量（工作细节）。"
                }
            ]

            for s in sentences:
                essay_html += f"""
                <div class="sen-box" onclick="toggleSentence({s['id']}, '{s['blank_id']}', '{s['blank_word']}', '{s['audio']}')">
                    <div class="sen-jp">{s['jp']}</div>
                    <div id="detail_{s['id']}" class="sen-details">
                        <div class="analysis-title">🇨🇳 句子翻译</div>
                        <div class="analysis-content">{s['tr']}</div>
                        <div class="analysis-title">🧠 深度解析</div>
                        <div class="analysis-content">{s['analysis']}</div>
                        <button class="play-btn" style="margin-left:0; margin-top:10px;" onclick="speak('{s['audio']}', event)">🔊 朗读此句</button>
                    </div>
                </div>
                """
            
            essay_html += "</div>"
            components.html(essay_html, height=850, scrolling=True)

        # ==========================================
        # TAB 3: 课后 30 词 (全发音 + 绝对隐藏翻译)
        # ==========================================
        with tab3:
            sprint_html = common_head + '<div class="main-container"><div class="grid-container">'
            sprint_30 = [("合致", "一致"), ("兆し", "前兆"), ("素朴", "纯朴"), ("妥協", "妥协"), ("漠然", "模糊"), ("閲覧", "阅读"), ("一転", "突然改变"), ("安堵", "放心"), ("会得", "领会"), ("概説", "概论")]
            
            for word, trans in sprint_30:
                sprint_html += f"""
                <div class="grid-item">
                    <div style="font-size: 1.4rem; color: #58a6ff; font-weight: bold; margin-bottom: 8px;">{word}</div>
                    <div class="spoiler" style="display:inline-block; margin-bottom: 15px;">{trans}</div>
                    <br>
                    <button class="play-btn" style="width: 80%; margin:0;" onclick="speak('{word}')">🔊 读音</button>
                </div>
                """
            sprint_html += "</div></div>"
            components.html(sprint_html, height=700, scrolling=True)
