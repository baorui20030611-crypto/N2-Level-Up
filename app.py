import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(page_title="N2沉浸式通关引擎 - v5", page_icon="⛩️", layout="wide")
st.title("⚓ Day 1：职场与生活效率篇 (说明书精讲)")
st.markdown("---")

# ==========================================
# 2. 公共 HTML 头部 (CSS & JS)
# ==========================================
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { font-family: 'Noto Sans JP', sans-serif; background-color: #0e1117; color: #c9d1d9; margin: 0; padding: 10px; }
    
    /* 播放按钮 */
    .play-btn { background: #238636; color: white; border: none; border-radius: 4px; padding: 4px 10px; cursor: pointer; font-size: 0.9rem; margin-left:10px; }
    .play-btn:hover { background: #2ea043; }
    
    /* --- 悬停显义防作弊 (已恢复且升级) --- */
    .hide-tr { color: #8b949e; opacity: 0; transition: opacity 0.3s ease; border-bottom: 1px dashed #30363d; padding-bottom: 2px; }
    .hide-tr:hover { opacity: 1; color: #fbbf24; cursor: help; }
    
    /* --- 单词说明书样式 --- */
    .manual-card { background: #161b22; border: 1px solid #30363d; border-radius: 10px; padding: 20px; margin-bottom: 20px; border-left: 5px solid #58a6ff; }
    .m-header { font-size: 1.6rem; color: #58a6ff; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #30363d; padding-bottom: 10px; }
    .m-usage { margin-bottom: 15px; padding-left: 10px; border-left: 3px solid #2ea043; }
    .m-meaning { font-weight: bold; color: #e6edf3; font-size: 1.1rem; }
    .m-sentence { color: #c9d1d9; font-size: 1.1rem; margin: 5px 0; background: #0d1117; padding: 10px; border-radius: 5px; }
    
    /* --- 完形填空 & 语法高亮 --- */
    .essay-container { line-height: 2.2; font-size: 1.3rem; padding: 25px; background: #161b22; border-radius: 10px; }
    .blank { display: inline-block; min-width: 60px; text-align: center; color: #58a6ff; cursor: pointer; font-weight: bold; border-bottom: 2px dashed #58a6ff; padding: 0 5px; margin: 0 5px; background: rgba(88,166,255,0.1); }
    .blank.revealed { color: #ff7b72; border-bottom: 2px solid #ff7b72; background: rgba(255,123,114,0.1); }
    
    /* 副词/接续词的特殊颜色标签 */
    .grammar-tag { color: #d2a8ff; font-weight: bold; cursor: pointer; border-bottom: 1px dashed #d2a8ff; padding: 0 3px; }
    .grammar-tag:hover { background: rgba(210,168,255,0.2); }
    
    /* 底部解析盒子 */
    .analysis-box { margin-top: 20px; padding: 20px; background: #21262d; border-radius: 8px; display: none; border-left: 5px solid #ff7b72; }
    
    /* --- 课前小游戏样式 --- */
    .game-box { background: #161b22; padding: 20px; border-radius: 10px; text-align: center; margin-bottom:15px; }
    .game-q { font-size: 1.5rem; color: #58a6ff; margin-bottom: 15px; font-weight: bold; }
    .game-opt { background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 10px 20px; margin: 5px; border-radius: 5px; cursor: pointer; font-size: 1.1rem; transition: 0.2s; }
    .game-opt:hover { background: #30363d; }
    .game-opt.correct { background: #238636; color: white; border-color: #2ea043; }
    .game-opt.wrong { background: #da3633; color: white; border-color: #f85149; }
</style>

<script>
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    // 完形填空揭晓
    function revealAns(id, word, pure, tr, audio) {
        let el = document.getElementById('b'+id);
        el.innerHTML = word; el.classList.add('revealed');
        speak(pure);
        
        let box = document.getElementById('analysis-box');
        box.style.display = 'block'; box.style.borderLeftColor = '#ff7b72';
        document.getElementById('ans-content').innerHTML = "<b>🇨🇳 句子翻译：</b>" + tr;
        document.getElementById('ans-audio').onclick = function(){ speak(audio); };
        document.getElementById('ans-audio').style.display = 'inline-block';
    }
    
    // 语法词汇深度解析展示
    function showGrammar(word, usage) {
        let box = document.getElementById('analysis-box');
        box.style.display = 'block'; box.style.borderLeftColor = '#d2a8ff';
        document.getElementById('ans-content').innerHTML = "<b>🧠 词法拓展【" + word + "】：</b><br>" + usage;
        document.getElementById('ans-audio').style.display = 'none'; // 语法说明不全句朗读
    }
    
    // 课前抽测小游戏逻辑
    function checkGame(btn, isCorrect, wordAudio) {
        if(isCorrect) {
            btn.classList.add('correct');
            btn.innerHTML += " ✅";
            speak(wordAudio);
        } else {
            btn.classList.add('wrong');
            btn.innerHTML += " ❌";
        }
    }
</script>
"""

# ==========================================
# 3. 核心数据字典 (精细化说明书)
# ==========================================
# 这里为你编写了真正的“说明书式”教案（以 PPT 1 的 3 个词为例）
manual_data = {
    "ppt_1": [
        {
            "word": "捗る", "kana": "はかどる",
            "usages": [
                {"meaning": "用法1：事物或工作顺利进行（侧重于效率高）。", "jp": "計画が予定通りに捗っている。", "pure": "けいかくがよていどおりにはかどっている", "tr": "计划正按预期顺利进行。"},
                {"meaning": "用法2：通常搭配【副词：とても、順調に】。", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。"}
            ]
        },
        {
            "word": "割り当てる", "kana": "わりあてる",
            "usages": [
                {"meaning": "用法1：分配任务、配额给具体的人。", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。"},
                {"meaning": "用法2：分配时间、空间资源。", "jp": "一部屋に二人ずつ割り当てる。", "pure": "ひとへやにふたりずつわりあてる", "tr": "按每间房两个人进行分配。"}
            ]
        },
        {
            "word": "備え付ける", "kana": "そなえつける",
            "usages": [
                {"meaning": "用法1：在特定场所安装、配备（家具、电器等固定设备）。", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。"}
            ]
        }
    ]
}

# ==========================================
# 4. 页面主体渲染 (Tabs)
# ==========================================
tab1, tab2, tab3 = st.tabs(["🎯 1. 课前小游戏", "📖 2. 单词说明书 (精讲)", "📝 3. 完形填空实战"])

# --- Tab 1: 课前抽测小游戏 ---
with tab1:
    st.info("💡 游戏规则：点击你认为正确的中文意思。选对会变成绿色并自动发音！")
    html_game = common_head + """
    <div class="game-box">
        <div class="game-q">Q1. 捗る (はかどる)</div>
        <button class="game-opt" onclick="checkGame(this, false, '')">A. 推迟、暂缓</button>
        <button class="game-opt" onclick="checkGame(this, true, 'はかどる')">B. 进展顺利</button>
        <button class="game-opt" onclick="checkGame(this, false, '')">C. 分配</button>
    </div>
    <div class="game-box">
        <div class="game-q">Q2. 見合わせる (みあわせる)</div>
        <button class="game-opt" onclick="checkGame(this, true, 'みあわせる')">A. 暂停、推迟</button>
        <button class="game-opt" onclick="checkGame(this, false, '')">B. 互相看</button>
        <button class="game-opt" onclick="checkGame(this, false, '')">C. 一致</button>
    </div>
    """
    components.html(html_game, height=400)

# --- Tab 2: 单词说明书 (PPT 分页式) ---
with tab2:
    st.info("💡 提示：鼠标悬停在【灰色虚线处】即可查看中文翻译（防作弊机制）。")
    
    # 顶部的 PPT 切换器
    ppt_selection = st.radio("请选择讲义页码：", ["PPT 1 (词1-3)", "PPT 2 (词4-6)", "PPT 3 (词7-9)", "PPT 4 (词10-12)", "PPT 5 (词13-15)"], horizontal=True)
    
    # 根据选择渲染对应的 3 个单词的“说明书”
    html_manual = common_head + "<div>"
    
    if ppt_selection == "PPT 1 (词1-3)":
        for data in manual_data["ppt_1"]:
            html_manual += f"""
            <div class="manual-card">
                <div class="m-header">{data['word']} <span style="font-size:1rem; color:#8b949e">({data['kana']})</span> 
                    <button class="play-btn" onclick="speak('{data['word']}')">🔊 读原词</button>
                </div>
            """
            for idx, u in enumerate(data['usages']):
                html_manual += f"""
                <div class="m-usage">
                    <div class="m-meaning">{u['meaning']}</div>
                    <div class="m-sentence">
                        {u['jp']} <button class="play-btn" onclick="speak('{u['pure']}')">🔊 读例句</button>
                    </div>
                    <div class="hide-tr">🇨🇳 {u['tr']} (鼠标悬停查看)</div>
                </div>
                """
            html_manual += "</div>"
        components.html(html_manual, height=800, scrolling=True)
    else:
        st.warning(f"🚧 【{ppt_selection}】 的说明书数据稍后将依据此模板为您灌入。")

# --- Tab 3: 完形填空 & 语法词高亮查阅 ---
with tab3:
    st.info("💡 提示：点击【数字】填空。点击【紫色高亮词】查阅它的语法与多重用法。")
    
    # 注意看这里的とても和なぜなら，加入了 onclick 事件，触发 showGrammar 函数
    essay_html = common_head + """
    <div class="essay-container">
        今日の仕事は<span class="grammar-tag" onclick="showGrammar('とても', '<b>【当前用法】</b>表示程度极高（非常）。<br><b>【用法拓展】</b>后接否定形式时，表示“无论如何也（做不到）”。<br><i>例：この量はとても食べきれない。（这么多无论如何也吃不完。）</i>')">とても</span>
        <span class='blank' id='b1' onclick="revealAns('1', '捗りました', 'はかどりました', '今天的工作进展非常顺利。', '今日の仕事はとても捗りました。')">【 1 】</span>。
        
        <span class="grammar-tag" onclick="showGrammar('なぜなら', '<b>【当前用法】</b>用于句首，表示说明原因（因为...）。<br><b>【用法拓展】</b>句尾通常必须搭配「～からだ / ～ためだ」进行呼应。<br><i>例：なぜなら、時間がなかったからです。</i>')">なぜなら</span>、
        上司が適切に業務を
        <span class='blank' id='b2' onclick="revealAns('2', '割り当てて', 'わりあてて', '因为上司妥善地分配了任务。', 'なぜなら、上司が適切に業務を割り当ててくれたからです。')">【 2 】</span>くれたからです。
    </div>
    
    <div id="analysis-box" class="analysis-box">
        <div id="ans-content" style="color: #c9d1d9; font-size: 1.1rem; margin-bottom: 10px;"></div>
        <button class="play-btn" id="ans-audio" style="display:none;">🔊 朗读此句</button>
    </div>
    """
    components.html(essay_html, height=600)
