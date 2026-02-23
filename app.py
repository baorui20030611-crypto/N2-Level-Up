import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="N2沉浸式通关引擎 - 教辅实战版", page_icon="⛩️", layout="wide")

# ==========================================
# 核心 HTML/CSS/JS 引擎 (聚光灯特效 + 刮刮乐 + 图例)
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
    .play-btn { background: #2ea043; color: white; border: none; border-radius: 4px; padding: 6px 15px; cursor: pointer; font-size: 1rem; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.3);}
    .play-btn:hover { background: #3fb950; transform: scale(1.05); }

    /* --- 绝对隐藏：刮刮乐防作弊特效 --- */
    .spoiler { 
        background-color: #30363d; color: transparent; 
        border-radius: 4px; padding: 4px 10px; 
        transition: all 0.3s ease; user-select: none; display: inline-block;
    }
    .spoiler:hover { background-color: rgba(251,191,36,0.1); color: #fbbf24; border: 1px dashed #fbbf24; }

    /* --- 词性色彩罗盘 (文章内高亮) --- */
    .pos-verb { color: #ff7b72; font-weight: bold; border-bottom: 1px dashed #ff7b72; padding-bottom:1px;} 
    .pos-adv { color: #79c0ff; font-weight: bold; border-bottom: 1px dashed #79c0ff; padding-bottom:1px;} 
    .pos-conj { color: #d2a8ff; font-weight: bold; border-bottom: 1px dashed #d2a8ff; padding-bottom:1px;} 
    .pos-pron { color: #2ea043; font-weight: bold; border-bottom: 1px dashed #2ea043; padding-bottom:1px;} 
    .pos-adj { color: #ffa657; font-weight: bold; border-bottom: 1px dashed #ffa657; padding-bottom:1px;} 
    .pos-noun { color: #a5d6ff; font-weight: bold; border-bottom: 1px dashed #a5d6ff; padding-bottom:1px;} 
    
    /* 右下角固定图例 */
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.95); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); z-index: 1000; font-size: 0.9rem; backdrop-filter: blur(5px);}
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }

    /* --- 思维导图样式 --- */
    .mindmap-box { display: flex; align-items: stretch; background: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 25px; transition: 0.3s; overflow:hidden;}
    .mindmap-box:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.5); border-color:#58a6ff; }
    .mm-root { flex: 0 0 240px; background: #21262d; text-align: center; padding: 30px 20px; border-right: 3px solid #58a6ff; display: flex; flex-direction: column; justify-content: center; align-items: center;}
    .mm-word { font-size: 2.2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .mm-branches { flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #0d1117; padding: 15px; border-radius: 8px; border-left: 4px solid #8957e5; }
    .mm-usage { font-size: 1.1rem; color: #e6edf3; font-weight: bold; margin-bottom: 10px; }
    .mm-sentence { font-size: 1.25rem; color: #c9d1d9; margin-bottom: 15px; line-height: 1.6; }
    
    /* --- 🚀 N2 长文阅读：聚光灯特效 (Spotlight Blur) --- */
    .essay-container { font-size: 1.35rem; line-height: 2.4; background: #161b22; padding: 40px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #30363d; text-align: justify; letter-spacing: 0.5px; transition: 0.3s;}
    .sen-span { transition: all 0.3s ease; padding: 2px 5px; border-radius: 5px; cursor: pointer; }
    
    /* 当容器被 Hover 时，所有句子变暗虚化 */
    .essay-container.is-hovering .sen-span { filter: blur(3px); opacity: 0.3; }
    
    /* 被 Hover 的那句话，解除虚化，放大高亮 */
    .essay-container.is-hovering .sen-span.active-hover { filter: blur(0); opacity: 1; font-size: 1.05em; background: rgba(88,166,255,0.15); box-shadow: 0 0 15px rgba(88,166,255,0.2); text-shadow: 0 0 5px rgba(255,255,255,0.2); z-index: 10; border-bottom: 2px solid #58a6ff; }

    /* 底部硬核解析盒子 */
    .analysis-box { background: #0d1117; border: 1px solid #30363d; border-top: 5px solid #fbbf24; border-radius: 8px; padding: 25px; margin-top: 20px; display: none; box-shadow: 0 10px 30px rgba(0,0,0,0.5); }
    .analysis-title { color: #fbbf24; font-size: 1.2rem; font-weight: bold; margin-bottom: 15px; border-bottom: 1px solid #30363d; padding-bottom: 10px; display: flex; justify-content: space-between; align-items: center;}
    .analysis-content { color: #c9d1d9; line-height: 1.8; font-size: 1.1rem; }
    
    /* 30词网格 */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 20px 15px; border-radius: 8px; text-align: center; transition: 0.3s; }
    .grid-item:hover { transform: translateY(-5px); box-shadow: 0 5px 15px rgba(0,0,0,0.4); border-color: #58a6ff;}
</style>

<script>
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    // 聚光灯特效与解析联动逻辑
    function onSenEnter(id, audioText) {
        let container = document.getElementById('essay-box');
        let sen = document.getElementById('sen_' + id);
        
        container.classList.add('is-hovering');
        sen.classList.add('active-hover');
        
        // 抓取隐藏 div 里的教辅解析，注入到展示盒子里
        let content = document.getElementById('data_' + id).innerHTML;
        let box = document.getElementById('analysis-box');
        box.style.display = 'block';
        document.getElementById('analysis-inner').innerHTML = content;
        
        // 绑定语音按钮
        document.getElementById('ans-audio').onclick = function(e){ speak(audioText, e); };
    }
    
    function onSenLeave(id) {
        let container = document.getElementById('essay-box');
        let sen = document.getElementById('sen_' + id);
        container.classList.remove('is-hovering');
        sen.classList.remove('active-hover');
        // 解析盒子保持显示，方便用户点击语音或阅读
    }
</script>
"""

# ==========================================
# 侧边栏与导航
# ==========================================
st.sidebar.title("🏮 N2 冲刺系统")
selected_lesson = st.sidebar.radio("📚 选择课时", ["Day 1 - 第1课时 (职场效率)", "Day 1 - 第2课时 (身心状态)"])
st.sidebar.markdown("---")
st.sidebar.write("🎵 **专注氛围**")
if st.sidebar.button("▶️ 播放白噪音/轻音乐"):
    st.sidebar.audio("https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3", format="audio/mp3")

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center; color: #e6edf3;'>{selected_lesson}</h2>", unsafe_allow_html=True)
    st.markdown("---")

# ==========================================
# 动态加载数据 (极度硬核的教辅解析)
# ==========================================
if "第1课时" in selected_lesson:
    words_data = [
        {"word": "捗る", "kana": "はかどる", "direct_tr": "进展顺利",
         "usages": [{"meaning": "① 进展顺利 (常接とても/順調に)", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。"}]},
        {"word": "割り当てる", "kana": "わりあてる", "direct_tr": "分配",
         "usages": [{"meaning": "① 分配任务/资源", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。"}]},
        {"word": "備え付ける", "kana": "そなえつける", "direct_tr": "设置/装备",
         "usages": [{"meaning": "① 固定安装", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。"}]}
    ]
    
    # 超过 150 字的 N2 实战长文
    sentences = [
        {"id": "s1", "audio": "最近、多くの企業でリモートワークが導入され、働き方が一変した。",
         "jp": "<span class='pos-noun'>最近</span>、多くの<span class='pos-noun'>企業</span>でリモートワークが導入され、働き方が一変した。",
         "html": "<b>【翻訳】</b>最近，许多企业引入了远程办公，工作方式发生了巨变。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>～が導入（どうにゅう）される</b>：被动语态。在 N2 阅读中，描述社会普遍现象或客观事实时，极高频使用被动语态。<br>🔹 <b>一変（いっぺん）した</b>：名词+する。表示“完全改变”。"},
        {"id": "s2", "audio": "それに伴い、自宅での仕事がとても捗ると感じる人がいる一方で、対面でのコミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も頻繁に聞かれる。",
         "jp": "<span class='pos-conj'>それに伴い</span>、自宅での仕事が<span class='pos-adv'>とても</span><span class='pos-verb'>捗る</span>と感じる人がいる<span class='pos-conj'>一方で</span>、対面でのコミュニケーションの不足から、業務を適切に<span class='pos-verb'>割り当てる</span>ことが難しくなったという声も<span class='pos-adv'>頻繁に</span>聞かれる。",
         "html": "<b>【翻訳】</b>伴随于此，一方面有人觉得在家的工作进展非常顺利，但另一方面，由于缺乏面对面的沟通，也有人频繁表示难以妥善分配业务。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>～に伴い（にともない）</b>：N2核心语法。表示随着前项的变化，后项也发生变化。<br>🔹 <b>～一方で（いっぽうで）</b>：N2重点！表示同一事物的两个相对面（一方面...另一方面）。<br>🔹 <b>とても + 捗る</b>：副词与动词的固定搭配，表示“效率极高”。<br>🔹 <b>割り当てる</b>：本课核心词，分配任务。"},
        {"id": "s3", "audio": "また、自宅に仕事用のデスクや高性能なパソコンを備え付けるための費用も、無視できない課題となっている。",
         "jp": "<span class='pos-conj'>また</span>、自宅に仕事用のデスクや高性能なパソコンを<span class='pos-verb'>備え付ける</span><span class='pos-conj'>ための</span>費用も、無視できない課題となっている。",
         "html": "<b>【翻訳】</b>此外，为了在家里配备办公桌和高性能电脑的费用，也成了一个不可忽视的课题。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>備え付ける（そなえつける）</b>：动词，安装、配备（固定设施）。<br>🔹 <b>ための</b>：接在动词原形后，修饰名词“費用”，表示目的。"},
        {"id": "s4", "audio": "しかし、環境の変化にただ嘆くのではなく、決して妥協せずに、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが必ず見えてくるだろう。",
         "jp": "<span class='pos-conj'>しかし</span>、環境の変化にただ嘆くのではなく、<span class='pos-adv'>決して</span><span class='pos-verb'>妥協</span>せずに、オンラインで<span class='pos-adv'>こまめに</span><span class='pos-verb'>打ち合わせる</span>ことで、新しい働き方の<span class='pos-noun'>兆し</span>が必ず見えてくるだろう。",
         "html": "<b>【翻訳】</b>然而，不要仅仅哀叹环境的变化，只要绝不妥协，在线上勤加商量，就一定会看到新工作方式的曙光吧。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>決して～ない</b>：N3/N2副词呼应。表示“绝不...”。<br>🔹 <b>こまめに</b>：N2核心副词，勤奋地、频繁地（常考点！）。<br>🔹 <b>～だろう</b>：推测。阅读题中，作者的主张通常藏在推测句的结尾。"},
        {"id": "s5", "audio": "古い慣習が徐々に廃れるのは時代の必然的な流れであり、私たちは互いに足りない部分を補う努力を怠ってはならない。",
         "jp": "古い<span class='pos-noun'>慣習</span>が<span class='pos-adv'>徐々に</span><span class='pos-verb'>廃れる</span>のは時代の必然的な流れであり、<span class='pos-pron'>私たち</span>は互いに足りない部分を<span class='pos-verb'>補う</span>努力を怠ってはならない。",
         "html": "<b>【翻訳】</b>旧习惯的逐渐衰落是时代的必然趋势，我们绝不能懈怠去努力弥补彼此的不足。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>徐々に（じょじょに）</b>：副词，渐渐地。<br>🔹 <b>廃れる（すたれる） / 補う（おぎなう）</b>：动词，衰落 / 弥补。<br>🔹 <b>～てはならない</b>：N2强烈禁止语法，“绝不能...”。"}
    ]
else:
    # --- 第 2 课时 数据 ---
    words_data = [
        {"word": "堪える", "kana": "こたえる", "direct_tr": "吃不消", "usages": [{"meaning": "① 难以忍受", "jp": "今年の夏の暑さは体に応える。", "pure": "ことしのなつのあつさはからだにこたえる", "tr": "今年夏天的炎热真让身体吃不消。"}]},
        {"word": "朗らか", "kana": "ほがらか", "direct_tr": "开朗", "usages": [{"meaning": "① 性格阳光", "jp": "彼女はいつも朗らかな笑顔を見せる。", "pure": "かのじょはいつもほがらかなえがおをみせる", "tr": "她总是展现出开朗的笑容。"}]},
        {"word": "執着", "kana": "しゅうちゃく", "direct_tr": "留恋/执着", "usages": [{"meaning": "① 迷恋，不肯放弃", "jp": "過去の栄光に執着しても意味がない。", "pure": "かこのえいこうにしゅうちゃくしてもいみが無い", "tr": "对过去的辉煌斤斤计较也没有意义。"}]}
    ]
    sentences = [
        {"id": "s1", "audio": "人は年齢を重ねるとともに、徹夜の仕事や無理なスケジュールが以前よりも体に応えるようになる。",
         "jp": "<span class='pos-noun'>人</span>は年齢を重ねる<span class='pos-conj'>とともに</span>、徹夜の仕事や無理なスケジュールが以前よりも体に<span class='pos-verb'>応える</span>ようになる。",
         "html": "<b>【翻訳】</b>随着年龄的增长，熬夜工作和勉强的日程安排变得比以前更让身体吃不消了。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>～とともに</b>：N2语法。表示“随着...同时发生”。<br>🔹 <b>応える（こたえる）</b>：强烈刺激让人受不了。"},
        {"id": "s2", "audio": "若い頃は一晩寝れば回復したかもしれないが、今はそうもいかない。",
         "jp": "若い頃は一晩寝れば回復した<span class='pos-conj'>かもしれない</span>が、今はそうもいかない。",
         "html": "<b>【翻訳】</b>年轻的时候也许睡一晚就恢复了，但现在可没那么容易。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>～かもしれない</b>：表示可能性。<br>🔹 <b>そうもいかない</b>：惯用表达，表示“事情没有那么简单/不能那样做”。"},
        {"id": "s3", "audio": "したがって、かつての体力にむやみに執着するよりも、衰えゆく今の自分を素直に受け入れることが何よりも大切だ。",
         "jp": "<span class='pos-conj'>したがって</span>、<span class='pos-adv'>かつて</span>の体力に<span class='pos-adv'>むやみに</span><span class='pos-verb'>執着する</span>よりも、衰えゆく今の自分を素直に受け入れることが何よりも大切だ。",
         "html": "<b>【翻訳】</b>因此，与其对过去的体力盲目执着，不如坦然接受正在衰老的现在的自己，这比什么都重要。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>したがって</b>：接续词，因此。<br>🔹 <b>むやみに</b>：副词，盲目地、胡乱地。<br>🔹 <b>執着（しゅうちゃく）する</b>：执着，留恋。"}
    ]

# 统一 30 词冲刺包
sprint_30_data = [
    ("合致", "がっち", "一致"), ("兆し", "きざし", "前兆"), ("素朴", "そぼく", "纯朴"), ("妥協", "だきょう", "妥协"), ("漠然", "ばくぜん", "模糊"),
    ("閲覧", "えつらん", "阅读"), ("一転", "いってん", "突然改变"), ("安堵", "あんど", "放心"), ("会得", "えとく", "领会"), ("概説", "がいせつ", "概论"),
    ("該当", "がいとう", "符合"), ("介入", "かいにゅう", "干预"), ("各界", "かくかい", "各界"), ("拡充", "かくじゅう", "扩充"), ("確保", "かくほ", "确保"),
    ("加味", "かみ", "加入"), ("関与", "かんよ", "参与"), ("慣習", "かんしゅう", "习俗"), ("棄権", "きけん", "弃权"), ("規制", "きせい", "管制"),
    ("拒絶", "きょぜつ", "拒绝"), ("許容", "きょよう", "许可"), ("起用", "きよう", "启用"), ("議決", "ぎけつ", "表决"), ("却下", "きゃっか", "驳回"),
    ("救済", "きゅうさい", "救济"), ("強要", "きょうよう", "强迫"), ("均衡", "きんこう", "平衡"), ("駆使", "くし", "运用自如"), ("駆除", "くじょ", "驱除")
]

# ==========================================
# 渲染页面核心内容 (Tabs)
# ==========================================
with st.container():
    c_left, c_mid, c_right = st.columns([1, 14, 1])
    with c_mid:
        tab1, tab2, tab3 = st.tabs(["📖 核心词说明书", "📝 聚光灯：长文精读", "🚀 课后 30 词冲刺"])

        # ------------------------------------------
        # TAB 1: 核心词解剖
        # ------------------------------------------
        with tab1:
            mindmap_html = common_head + '<div class="main-container">'
            for data in words_data:
                mindmap_html += f"""
                <div class="mindmap-box">
                    <div class="mm-root">
                        <div class="mm-word">{data['word']}</div>
                        <div style="color:#8b949e; font-size:1.1rem; margin-bottom:15px;">{data['kana']}</div>
                        <div class="spoiler" style="color:transparent;">{data['direct_tr']}</div>
                        <button class="play-btn" style="margin-top:20px; width:100%; margin-left:0;" onclick="speak('{data['word']}')">🔊 朗读原词</button>
                    </div>
                    <div class="mm-branches">
                """
                for u in data['usages']:
                    mindmap_html += f"""
                        <div class="mm-branch">
                            <div class="mm-usage">{u['meaning']}</div>
                            <div class="mm-sentence">{u['jp']} <button class="play-btn" onclick="speak('{u['pure']}')">🔊</button></div>
                            <div class="spoiler" style="color:transparent;">{u['tr']}</div>
                        </div>
                    """
                mindmap_html += "</div></div>"
            mindmap_html += "</div>"
            components.html(mindmap_html, height=800, scrolling=True)

        # ------------------------------------------
        # TAB 2: N2 阅读解剖 (终极聚光灯 + 隐藏教辅数据)
        # ------------------------------------------
        with tab2:
            # 提前把教辅解析写进隐藏的 div 中，供 JS 抓取，确保安全稳定
            hidden_data_html = ""
            for s in sentences:
                hidden_data_html += f"<div id='data_{s['id']}' style='display:none;'>{s['html']}</div>"
            
            essay_html = common_head + hidden_data_html + f"""
            <div class="legend-box">
                <div class="legend-title">🧩 N2 词性色彩罗盘</div>
                <div class="legend-item"><div class="color-block" style="background:#ff7b72;"></div> 动词 (Verb)</div>
                <div class="legend-item"><div class="color-block" style="background:#79c0ff;"></div> 副词 (Adv)</div>
                <div class="legend-item"><div class="color-block" style="background:#d2a8ff;"></div> 接续词 (Conj)</div>
                <div class="legend-item"><div class="color-block" style="background:#2ea043;"></div> 代词 (Pron)</div>
                <div class="legend-item"><div class="color-block" style="background:#a5d6ff;"></div> 名词 (Noun)</div>
            </div>
            
            <div class="main-container">
                <div class="essay-container" id="essay-box">
            """
            
            # 拼接句子
            for s in sentences:
                essay_html += f"<span class='sen-span' id='sen_{s['id']}' onmouseenter=\"onSenEnter('{s['id']}', '{s['audio']}')\" onmouseleave=\"onSenLeave('{s['id']}')\">{s['jp']}</span> "
                
            essay_html += """
                </div>
                
                <div id="analysis-box" class="analysis-box">
                    <div class="analysis-title">
                        <span>🧠 教辅级深度解剖</span>
                        <button class="play-btn" id="ans-audio" style="margin:0;">🔊 朗读此句</button>
                    </div>
                    <div class="analysis-content" id="analysis-inner">
                        </div>
                </div>
            </div>
            """
            components.html(essay_html, height=900, scrolling=True)

        # ------------------------------------------
        # TAB 3: 课后 30 词
        # ------------------------------------------
        with tab3:
            sprint_html = common_head + '<div class="main-container"><div class="grid-container">'
            for word, kana, trans in sprint_30_data:
                sprint_html += f"""
                <div class="grid-item">
                    <div style="font-size: 1.5rem; color: #58a6ff; font-weight: bold; margin-bottom: 2px;">{word}</div>
                    <div style="font-size: 0.85rem; color: #8b949e; margin-bottom: 5px;">{kana}</div>
                    <div style="margin-bottom:15px;"><span class="spoiler" style="color:transparent;">{trans}</span></div>
                    <button class="play-btn" style="width: 80%; margin:0;" onclick="speak('{word}')">🔊 读音</button>
                </div>
                """
            sprint_html += "</div></div>"
            components.html(sprint_html, height=800, scrolling=True)
