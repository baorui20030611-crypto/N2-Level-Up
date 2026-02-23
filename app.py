import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 页面配置与全局样式 (全面居中平衡排版)
# ==========================================
st.set_page_config(page_title="N2沉浸式通关引擎 - v6 闯关版", page_icon="⛩️", layout="wide")

# 全局 HTML/CSS 引擎 (包含思维导图、全图例、居中排版)
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { 
        font-family: 'Noto Sans JP', sans-serif; 
        background-color: #0d1117; color: #c9d1d9; 
        margin: 0; padding: 20px;
        /* 让所有内容居中，最大宽度限制，解决全挤在左边的视觉疲劳 */
        display: flex; justify-content: center;
    }
    .main-container { width: 100%; max-width: 1100px; margin: 0 auto; }
    
    /* 播放按钮 */
    .play-btn { background: #238636; color: white; border: none; border-radius: 4px; padding: 4px 10px; cursor: pointer; font-size: 0.9rem; margin-left:10px; transition: 0.2s;}
    .play-btn:hover { background: #2ea043; transform: scale(1.05); }
    
    /* --- 1. 思维导图样式 (Mind Map) --- */
    .mindmap-box { display: flex; align-items: center; background: #161b22; border: 1px solid #30363d; border-radius: 12px; padding: 20px; margin-bottom: 25px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); }
    .mm-root { flex: 0 0 200px; text-align: center; border-right: 3px solid #58a6ff; padding-right: 20px; }
    .mm-word { font-size: 2rem; color: #58a6ff; font-weight: bold; cursor: pointer; transition: 0.2s; }
    .mm-word:hover { text-shadow: 0 0 10px rgba(88,166,255,0.5); }
    .mm-branches { flex: 1; padding-left: 30px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #21262d; padding: 15px; border-radius: 8px; border-left: 4px solid #8957e5; position: relative; }
    /* 用法、例句、翻译分层 */
    .mm-usage { font-size: 1.1rem; color: #e6edf3; font-weight: bold; margin-bottom: 8px; }
    .mm-sentence { font-size: 1.15rem; color: #c9d1d9; background: #0d1117; padding: 10px; border-radius: 5px; margin-bottom: 8px;}
    .mm-trans { color: #8b949e; background: #161b22; padding: 5px 10px; border-radius: 4px; display: inline-block; cursor: help; border: 1px dashed #30363d; }
    .mm-trans:hover { color: #fbbf24; border-color: #fbbf24; background: rgba(251,191,36,0.1); }
    
    /* --- 2. 完形填空 & 多彩词性标签 --- */
    .essay-container { line-height: 2.4; font-size: 1.3rem; padding: 30px; background: #161b22; border-radius: 12px; box-shadow: 0 4px 12px rgba(0,0,0,0.2); text-align: justify; }
    .blank { display: inline-block; min-width: 60px; text-align: center; color: #58a6ff; cursor: pointer; font-weight: bold; border-bottom: 2px dashed #58a6ff; padding: 0 5px; margin: 0 5px; background: rgba(88,166,255,0.1); }
    .blank.revealed { color: #ff7b72; border-bottom: 2px solid #ff7b72; background: rgba(255,123,114,0.1); }
    
    /* 词性颜色库 */
    .pos-verb { color: #ff7b72; font-weight: bold; }       /* 动词：红 */
    .pos-adv { color: #79c0ff; font-weight: bold; }        /* 副词：蓝 */
    .pos-conj { color: #d2a8ff; font-weight: bold; }       /* 接续词：紫 */
    .pos-pron { color: #2ea043; font-weight: bold; }       /* 代词：绿 */
    .pos-adj { color: #ffa657; font-weight: bold; }        /* 连体词/形容词：橙 */
    .pos-int { color: #fbbf24; font-weight: bold; }        /* 感叹词：黄 */
    
    /* --- 3. 右下角全局图例 (Fixed Legend) --- */
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.9); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.5); backdrop-filter: blur(5px); z-index: 1000; font-size: 0.9rem; }
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }
    
    /* --- 4. 课后30词网格居中 --- */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 15px; border-radius: 8px; text-align: center; transition: 0.2s;}
    .grid-item:hover { transform: translateY(-3px); box-shadow: 0 4px 10px rgba(0,0,0,0.3); border-color: #58a6ff;}
    
    /* 解析盒子 */
    .analysis-box { margin-top: 25px; padding: 20px; background: #21262d; border-radius: 8px; display: none; border-left: 5px solid #ff7b72; }
</style>

<script>
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    function revealAns(id, word, pure, tr, audio, note) {
        let el = document.getElementById('b'+id);
        el.innerHTML = word; el.classList.add('revealed');
        speak(pure);
        
        let box = document.getElementById('analysis-box');
        box.style.display = 'block';
        document.getElementById('ans-content').innerHTML = "<b>🧠 词法提示：</b>" + note + "<br><br><b>🇨🇳 句子翻译：</b>" + tr;
        document.getElementById('ans-audio').onclick = function(){ speak(audio); };
    }
</script>
"""

# ==========================================
# 2. 界面顶栏 (营造闯关感)
# ==========================================
col1, col2, col3 = st.columns([2, 6, 2])
with col2:
    st.markdown("<h1 style='text-align: center; color: #e6edf3;'>⛩️ N2 沉浸式通关引擎</h1>", unsafe_allow_html=True)
    st.progress(0.05) # 闯关进度条
    st.markdown("<p style='text-align: center; color: #8b949e;'>🔥 进度：第 1 关 / 180 关 &nbsp;&nbsp;|&nbsp;&nbsp; 🏆 EXP: 150 / 9000</p>", unsafe_allow_html=True)
    st.markdown("---")

# ==========================================
# 3. 核心数据字典
# ==========================================
# 1. 思维导图讲义数据 (PPT1 的 3个词，用法全覆盖)
mindmap_data = [
    {
        "word": "捗る", "kana": "はかどる",
        "usages": [
            {"meaning": "▶ 用法1：事物或工作顺利进展（侧重效率）。", "jp": "計画が予定通りに捗っている。", "pure": "けいかくがよていどおりにはかどっている", "tr": "计划正按预期顺利进行。"},
            {"meaning": "▶ 用法2：常搭配副词【とても、順調に】。", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。"}
        ]
    },
    {
        "word": "割り当てる", "kana": "わりあてる",
        "usages": [
            {"meaning": "▶ 用法1：将任务、职责分配给具体的人。", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。"},
            {"meaning": "▶ 用法2：分配资源（时间、空间、预算）。", "jp": "一部屋に二人ずつ割り当てる。", "pure": "ひとへやにふたりずつわりあてる", "tr": "按每间房两个人进行分配。"}
        ]
    },
    {
        "word": "備え付ける", "kana": "そなえつける",
        "usages": [
            {"meaning": "▶ 用法1：在特定场所固定安装、配备（多指家具、机器）。", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。"},
            {"meaning": "▶ 考点辨析：与「備える」(防备) 不同，强调“物理安装”。", "jp": "消火器を廊下に備え付ける。", "pure": "しょうかきをろうかにそなえつける", "tr": "在走廊安装灭火器。"}
        ]
    }
]

# 2. 课后 30 词
sprint_30 = [
    ("合致", "一致"), ("兆し", "前兆"), ("素朴", "纯朴"), ("妥協", "妥协"), ("漠然", "模糊"),
    ("閲覧", "阅读"), ("一転", "突然改变"), ("安堵", "放心"), ("会得", "领会"), ("概説", "概论"),
    ("該当", "符合"), ("介入", "干预"), ("各界", "各界"), ("拡充", "扩充"), ("確保", "确保"),
    ("加味", "加入"), ("関与", "参与"), ("慣習", "习俗"), ("棄権", "弃权"), ("規制", "管制"),
    ("拒絶", "拒绝"), ("許容", "许可"), ("起用", "启用"), ("議決", "表决"), ("却下", "驳回"),
    ("救済", "救济"), ("強要", "强迫"), ("均衡", "平衡"), ("駆使", "运用自如"), ("駆除", "驱除")
]

# ==========================================
# 4. 渲染四大关卡 (居中容器内)
# ==========================================
with st.container():
    col_left, col_mid, col_right = st.columns([1, 10, 1]) # 利用比例让中间内容居中且不拥挤
    with col_mid:
        
        tab1, tab2, tab3, tab4 = st.tabs(["🎯 关卡 1: 课前热身", "📖 关卡 2: 思维导图心法", "📝 关卡 3: 终极连环阵 (小作文)", "🚀 关卡 4: 战利品 (30词)"])

        # --- 关卡 1: 简单热身 ---
        with tab1:
            st.info("💡 唤醒记忆：请回想【捗る】、【割り当てる】、【備え付ける】的意思。")
            st.button("✅ 我想起来了，进入下一关！")

        # --- 关卡 2: 思维导图精讲 (不再单调的说明书) ---
        with tab2:
            st.write("请选择要学习的卷轴：")
            ppt_selection = st.radio("", ["📜 卷一 (词1-3)", "📜 卷二 (词4-6)", "📜 卷三 (词7-9)", "📜 卷四 (词10-12)", "📜 卷五 (词13-15)"], horizontal=True, label_visibility="collapsed")
            
            html_mindmap = common_head + '<div class="main-container">'
            if ppt_selection == "📜 卷一 (词1-3)":
                for data in mindmap_data:
                    html_mindmap += f"""
                    <div class="mindmap-box">
                        <div class="mm-root" onclick="speak('{data['word']}')">
                            <div class="mm-word">{data['word']}</div>
                            <small style="color:#8b949e">{data['kana']}</small><br>
                            <button class="play-btn" style="margin: 10px 0 0 0;">🔊 发音</button>
                        </div>
                        <div class="mm-branches">
                    """
                    for u in data['usages']:
                        html_mindmap += f"""
                            <div class="mm-branch">
                                <div class="mm-usage">{u['meaning']}</div>
                                <div class="mm-sentence">{u['jp']} <button class="play-btn" onclick="speak('{u['pure']}')">🔊</button></div>
                                <div class="mm-trans">👁️ 悬停查看翻译：{u['tr']}</div>
                            </div>
                        """
                    html_mindmap += "</div></div>"
                html_mindmap += "</div>"
                components.html(html_mindmap, height=850, scrolling=True)
            else:
                st.warning("🚧 后续卷轴数据待灌入...")

        # --- 关卡 3: 11词联动小作文 (颜色词性 + 填空) ---
        with tab3:
            st.info("💡 操作指南：这段职场故事融合了本课 **11 个核心词**。注意观察代表不同词性的颜色。点击【数字】揭晓答案！")
            
            essay_html = common_head + """
            <div class="legend-box">
                <div class="legend-title">🧩 N2 词性色彩罗盘</div>
                <div class="legend-item"><div class="color-block" style="background:#ff7b72;"></div> 动词 (Verb)</div>
                <div class="legend-item"><div class="color-block" style="background:#79c0ff;"></div> 副词 (Adverb)</div>
                <div class="legend-item"><div class="color-block" style="background:#d2a8ff;"></div> 接续词 (Conj)</div>
                <div class="legend-item"><div class="color-block" style="background:#2ea043;"></div> 代词 (Pron)</div>
                <div class="legend-item"><div class="color-block" style="background:#ffa657;"></div> 连体/形容词 (Adj)</div>
            </div>

            <div class="main-container">
                <div class="essay-container">
                    <span class="pos-pron">彼ら</span>の今日の仕事は<span class="pos-adv">とても</span>
                    <span class='blank' id='b1' onclick="revealAns('1', '捗りました', 'はかどりました', '他们的今天工作进展非常顺利。', '彼らの今日の仕事はとても捗りました。', '【捗る】动词。')">【 1 】</span>。
                    
                    <span class="pos-conj">なぜなら</span>、新しい機材が
                    <span class='blank' id='b2' onclick="revealAns('2', '備え付けられて', 'そなえつけられて', '因为事先安装好了新设备。', 'なぜなら、新しい機材が備え付けられており、事前にしっかり打ち合わせることができたからです。', '【備え付ける】动词。')">【 2 】</span>おり、事前にしっかり
                    <span class='blank' id='b3' onclick="revealAns('3', '打ち合わせる', 'うちあわせる', '并且事前能够进行充分的商量。', '', '【打ち合わせる】动词，商量。')">【 3 】</span>ことができたからです。<br><br>
                    
                    最初、上司から膨大な仕事を
                    <span class='blank' id='b4' onclick="revealAns('4', '割り当てられた', 'わりあてられた', '最初被上司分配大量工作时...', '', '【割り当てる】动词，分配。')">【 4 】</span>時は、その量の多さに
                    <span class='blank' id='b5' onclick="revealAns('5', '堪えました', 'こたえました', '真是让人吃不消。', '', '【堪える】动词，难受/吃不消。')">【 5 】</span>が、チームの皆で互いの欠点を
                    <span class='blank' id='b6' onclick="revealAns('6', '補い', 'おぎない', '但是团队大家互相弥补了缺点。', '', '【補う】动词，弥补。')">【 6 】</span>ました。<br><br>
                    
                    古いやり方が
                    <span class='blank' id='b7' onclick="revealAns('7', '廃れる', 'すたれる', '旧的方法被淘汰是理所当然的。', '', '【廃れる】动词，过时/衰退。')">【 7 】</span>のは当然ですが、過去の成功に
                    <span class='blank' id='b8' onclick="revealAns('8', '執着', 'しゅうちゃく', '只要不执着于过去的成功...', '', '【執着】名词/动词，留恋/执着。')">【 8 】</span>せず、
                    <span class='blank pos-adj' id='b9' onclick="revealAns('9', '朗らかな', 'ほがらかな', '保持开朗的心情前进的话...', '', '【朗らかな】形容动词，开朗。')">【 9 】</span>気持ちで進めば、必ず成功の
                    <span class='blank' id='b10' onclick="revealAns('10', '兆し', 'きざし', '就一定能看到成功的前兆。', '', '【兆し】名词，前兆。')">【 10 】</span>が見えてきます。決して
                    <span class='blank' id='b11' onclick="revealAns('11', '妥協', 'だきょう', '决不妥协地努力吧！', '', '【妥協】动词，妥协。')">【 11 】</span>せずに頑張りましょう！
                </div>
                
                <div id="analysis-box" class="analysis-box">
                    <div id="ans-content" style="color: #c9d1d9; font-size: 1.1rem; margin-bottom: 10px;"></div>
                    <button class="play-btn" id="ans-audio">🔊 朗读此句</button>
                </div>
            </div>
            """
            components.html(essay_html, height=750, scrolling=True)

        # --- 关卡 4: 战利品 (30词全部找回，包含翻译与发音) ---
        with tab4:
            st.info("🎯 恭喜来到最终关卡！快速扫视以下 30 个历年真题核心词，点击 🔊 强化听觉记忆。")
            html_sprint = common_head + '<div class="main-container"><div class="grid-container">'
            for word, trans in sprint_30:
                html_sprint += f"""
                <div class="grid-item">
                    <div style="font-size: 1.3rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px;">{word}</div>
                    <div style="font-size: 1rem; color: #8b949e; margin-bottom: 10px;">{trans}</div>
                    <button class="play-btn" style="width: 100%; margin:0;" onclick="speak('{word}')">🔊 发音</button>
                </div>
                """
            html_sprint += "</div></div>"
            components.html(html_sprint, height=750, scrolling=True)
