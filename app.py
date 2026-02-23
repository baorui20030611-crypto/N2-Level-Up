import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="N2沉浸式通关引擎 - 实战版", page_icon="⛩️", layout="wide")

# ==========================================
# 核心 HTML/CSS/JS 引擎 (全局悬停放大 + 刮刮乐防作弊 + 零延迟语音)
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
    .play-btn { background: #2ea043; color: white; border: none; border-radius: 4px; padding: 5px 12px; cursor: pointer; font-size: 0.95rem; margin-left:10px; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.2);}
    .play-btn:hover { background: #3fb950; transform: scale(1.05); }
    
    /* --- 全局悬停放大特效 --- */
    .hover-enlarge { transition: all 0.3s cubic-bezier(0.25, 0.8, 0.25, 1); cursor: pointer; }
    .hover-enlarge:hover { transform: scale(1.02); box-shadow: 0 10px 20px rgba(0,0,0,0.4); z-index: 10; border-color: #58a6ff !important; }

    /* --- 绝对隐藏：刮刮乐防作弊特效 --- */
    .spoiler { 
        background-color: #30363d; color: transparent; 
        border-radius: 4px; padding: 4px 10px; 
        transition: all 0.3s ease; user-select: none;
        display: inline-block; border: 1px solid transparent;
    }
    .spoiler:hover { background-color: rgba(251,191,36,0.1); color: #fbbf24; border: 1px dashed #fbbf24; }

    /* --- 词性色彩罗盘 --- */
    .pos-verb { color: #ff7b72; font-weight: bold; }       /* 动词：红 */
    .pos-adv { color: #79c0ff; font-weight: bold; }        /* 副词：蓝 */
    .pos-conj { color: #d2a8ff; font-weight: bold; }       /* 接续词：紫 */
    .pos-pron { color: #2ea043; font-weight: bold; }       /* 代词：绿 */
    .pos-adj { color: #ffa657; font-weight: bold; }        /* 连体/形容词：橙 */
    .pos-noun { color: #a5d6ff; font-weight: bold; }       /* 名词：浅蓝 */
    
    /* 图例固定在右下角 */
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.95); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); z-index: 1000; font-size: 0.9rem; backdrop-filter: blur(5px);}
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }

    /* --- 思维导图说明书样式 --- */
    .mindmap-box { display: flex; align-items: stretch; background: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 25px; overflow: hidden; }
    .mm-root { flex: 0 0 240px; background: #21262d; text-align: center; padding: 30px 20px; border-right: 3px solid #58a6ff; display: flex; flex-direction: column; justify-content: center; align-items: center;}
    .mm-word { font-size: 2.2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .mm-branches { flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #0d1117; padding: 15px; border-radius: 8px; border-left: 4px solid #8957e5; }
    .mm-usage { font-size: 1.1rem; color: #e6edf3; font-weight: bold; margin-bottom: 10px; }
    .mm-sentence { font-size: 1.25rem; color: #c9d1d9; margin-bottom: 15px; line-height: 1.6; }
    
    /* --- N2 长文阅读样式 --- */
    .essay-fulltext { font-size: 1.25rem; line-height: 2.2; background: #161b22; padding: 30px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #30363d; text-align: justify; letter-spacing: 0.5px;}
    .sen-box { background: #161b22; border: 1px solid #30363d; border-left: 5px solid #2ea043; border-radius: 8px; padding: 20px; margin-bottom: 15px; }
    .sen-jp { font-size: 1.35rem; color: #ffffff; line-height: 1.7; }
    .sen-details { display: none; margin-top: 15px; border-top: 1px dashed #30363d; padding-top: 15px; }
    .analysis-title { color: #fbbf24; font-weight: bold; margin-bottom: 5px; font-size: 1.1rem; }
    .analysis-content { color: #8b949e; line-height: 1.6; margin-bottom: 15px; font-size: 1.05rem; background: #0d1117; padding: 15px; border-radius: 5px;}

    /* --- 30词网格 (新增假名注音) --- */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 20px 15px; border-radius: 8px; text-align: center; }
    .grid-kana { font-size: 0.85rem; color: #8b949e; margin-bottom: 2px; }
</style>

<script>
    // 零延迟语音引擎
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    // 句子解析展开逻辑
    function toggleSentence(id) {
        let detail = document.getElementById('detail_' + id);
        if(detail.style.display === 'block') { detail.style.display = 'none'; } 
        else { detail.style.display = 'block'; }
    }
</script>
"""

# ==========================================
# 侧边栏：课程导航与专注音乐
# ==========================================
st.sidebar.title("🏮 N2 冲刺计划")
selected_lesson = st.sidebar.radio("📚 选择今日课时", ["Day 1 - 第1课时 (基础动作篇)", "Day 1 - 第2课时 (状态进阶篇)"])

st.sidebar.markdown("---")
st.sidebar.write("🎵 **专注氛围控制**")
# 提供民谣/纯音乐的陪伴感
music_choice = st.sidebar.selectbox("背景音乐", ["无", "沉浸 Lo-Fi 纯音", "舒缓民谣吉他"])
if music_choice == "沉浸 Lo-Fi 纯音":
    st.sidebar.audio("https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3", format="audio/mp3")
elif music_choice == "舒缓民谣吉他":
    st.sidebar.audio("https://cdn.pixabay.com/download/audio/2022/02/10/audio_fc8eb4c7cd.mp3", format="audio/mp3")

# ==========================================
# 顶部全局进度与标题
# ==========================================
col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center; color: #e6edf3;'>{selected_lesson}</h2>", unsafe_allow_html=True)
    st.progress(0.02)
    st.markdown("---")

# ==========================================
# 动态加载两节课的数据字典
# ==========================================
if "第1课时" in selected_lesson:
    # --- 第 1 课时 数据 ---
    words_data = [
        {"word": "捗る", "kana": "はかどる", "direct_tr": "进展顺利",
         "usages": [{"meaning": "① 事物或工作顺利进展", "jp": "計画が予定通りに捗っている。", "pure": "けいかくがよていどおりにはかどっている", "tr": "计划正按预期顺利进行。"},
                    {"meaning": "② 搭配副词（とても/順調に）", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。"}]},
        {"word": "割り当てる", "kana": "わりあてる", "direct_tr": "分配/分摊",
         "usages": [{"meaning": "① 分配任务给具体的人", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。"},
                    {"meaning": "② 分配物理资源（时间、房间）", "jp": "一部屋に二人ずつ割り当てる。", "pure": "ひとへやにふたりずつわりあてる", "tr": "按每间房两个人进行分配。"}]},
        {"word": "備え付ける", "kana": "そなえつける", "direct_tr": "设置/装备",
         "usages": [{"meaning": "① 在特定场所固定安装机器/家具", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。"}]}
    ]
    
    # 150字 N2 真实阅读长文
    essay_full_text = "最近、多くの企業でリモートワークが導入されている。そのため、自宅での仕事がとても捗ると感じる人がいる一方で、コミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も聞かれる。また、自宅に仕事用のデスクやパソコンを備え付けるための費用も課題となっている。しかし、環境の変化に妥協せず、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが見えてくるだろう。古い慣習が廃れるのは時代の流れであり、私たちは足りない部分を補う努力が必要だ。"
    
    essay_sentences = [
        {"id": 1, "audio": "最近、多くの企業でリモートワークが導入されている。",
         "jp": "<span class='pos-noun'>最近</span>、多くの<span class='pos-noun'>企業</span>でリモートワークが導入されている。",
         "tr": "最近，很多企业都引入了远程办公。",
         "analysis": "<b>【N2考点拆解】</b><br>1. <b>導入（どうにゅう）される</b>：被动语态，表示“被引入”。在N2阅读中，客观事实多用被动。"},
        {"id": 2, "audio": "そのため、自宅での仕事がとても捗ると感じる人がいる一方で、コミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も聞かれる。",
         "jp": "<span class='pos-conj'>そのため</span>、自宅での仕事が<span class='pos-adv'>とても</span><span class='pos-verb'>捗る</span>と感じる人がいる<span class='pos-conj'>一方で</span>、コミュニケーションの不足から、業務を適切に<span class='pos-verb'>割り当てる</span>ことが難しくなったという声も聞かれる。",
         "tr": "因此，一方面有人觉得在家的工作进展非常顺利，但另一方面，也有声音表示由于缺乏沟通，妥善分配业务变得困难了。",
         "analysis": "<b>【N2考点拆解】</b><br>1. <b>～一方で（いっぽうで）</b>：N2核心语法。表示同一事物的两个相对的方面（一方面...另一方面...）。<br>2. <b>とても + 捗る（はかどる）</b>：黄金搭配。表示工作进度远超预期。<br>3. <b>割り当てる（わりあてる）</b>：动词，将整体切割后分配给个体。"},
        {"id": 3, "audio": "また、自宅に仕事用のデスクやパソコンを備え付けるための費用も課題となっている。",
         "jp": "<span class='pos-conj'>また</span>、自宅に仕事用のデスクやパソコンを<span class='pos-verb'>備え付ける</span><span class='pos-conj'>ための</span>費用も課題となっている。",
         "tr": "另外，为了在家里安装工作用的书桌和电脑的费用也成了一个课题。",
         "analysis": "<b>【N2考点拆解】</b><br>1. <b>備え付ける（そなえつける）</b>：动词，常用于机械、家具的安装配备。<br>2. <b>～ための</b>：接在动词原形后，修饰名词“费用”，表示“为了...的(费用)”。"},
        {"id": 4, "audio": "しかし、環境の変化に妥協せず、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが見えてくるだろう。",
         "jp": "<span class='pos-conj'>しかし</span>、環境の変化に<span class='pos-verb'>妥協</span>せず、オンラインでこまめに<span class='pos-verb'>打ち合わせる</span>ことで、新しい働き方の<span class='pos-noun'>兆し</span>が見えてくるだろう。",
         "tr": "但是，如果不向环境的变化妥协，通过在线上勤加商量沟通，就能看到新工作方式的前兆吧。",
         "analysis": "<b>【N2考点拆解】</b><br>1. <b>こまめに</b>：副词，勤奋地、频繁地。考点词！<br>2. <b>打ち合わせる（うちあわせる）</b>：碰头、商量（工作细节）。<br>3. <b>～だろう</b>：推测，作者的主张通常藏在推测句中。"},
        {"id": 5, "audio": "古い慣習が廃れるのは時代の流れであり、私たちは足りない部分を補う努力が必要だ。",
         "jp": "古い慣習が<span class='pos-verb'>廃れる</span>のは時代の流れであり、<span class='pos-pron'>私たち</span>は足りない部分を<span class='pos-verb'>補う</span>努力が必要だ。",
         "tr": "旧习惯的衰落是时代的洪流，我们有必要努力去弥补不足的部分。",
         "analysis": "<b>【N2考点拆解】</b><br>1. <b>廃れる（すたれる）</b>：动词，过时、衰落。常接在“流行、慣習”后面。<br>2. <b>補う（おぎなう）</b>：动词，弥补、补充（欠点、不足部分）。"}
    ]
    
    sprint_30_data = [
        ("合致", "がっち", "一致"), ("兆し", "きざし", "前兆"), ("素朴", "そぼく", "纯朴"), ("妥協", "だきょう", "妥协"), ("漠然", "ばくぜん", "模糊"),
        ("閲覧", "えつらん", "阅读"), ("一転", "いってん", "突然改变"), ("安堵", "あんど", "放心"), ("会得", "えとく", "领会"), ("概説", "がいせつ", "概论"),
        ("該当", "がいとう", "符合"), ("介入", "かいにゅう", "干预"), ("各界", "かくかい", "各界"), ("拡充", "かくじゅう", "扩充"), ("確保", "かくほ", "确保"),
        ("加味", "かみ", "加入"), ("関与", "かんよ", "参与"), ("慣習", "かんしゅう", "习俗"), ("棄権", "きけん", "弃权"), ("規制", "きせい", "管制"),
        ("拒絶", "きょぜつ", "拒绝"), ("許容", "きょよう", "许可"), ("起用", "きよう", "启用"), ("議決", "ぎけつ", "表决"), ("却下", "きゃっか", "驳回"),
        ("救済", "きゅうさい", "救济"), ("強要", "きょうよう", "强迫"), ("均衡", "きんこう", "平衡"), ("駆使", "くし", "运用自如"), ("駆除", "くじょ", "驱除")
    ]

else:
    # --- 第 2 课时 数据 (结构同上，词汇不同) ---
    words_data = [
        {"word": "堪える", "kana": "こたえる", "direct_tr": "吃不消",
         "usages": [{"meaning": "① 身体或精神上难以忍受（多指天气、劳累）", "jp": "今年の夏の暑さは体に応える。", "pure": "ことしのなつのあつさはからだにこたえる", "tr": "今年夏天的炎热真让身体吃不消。"}]},
        {"word": "朗らか", "kana": "ほがらか", "direct_tr": "开朗/晴朗",
         "usages": [{"meaning": "① 性格阳光、开朗", "jp": "彼女はいつも朗らかな笑顔を見せる。", "pure": "かのじょはいつもほがらかなえがおをみせる", "tr": "她总是展现出开朗的笑容。"}]},
        {"word": "執着", "kana": "しゅうちゃく", "direct_tr": "留恋/执着",
         "usages": [{"meaning": "① 对事物的深深迷恋，不肯放弃", "jp": "過去の栄光に執着しても意味がない。", "pure": "かこのえいこうにしゅうちゃくしてもいみが無い", "tr": "对过去的辉煌斤斤计较也没有意义。"}]}
    ]
    essay_full_text = "人は年齢を重ねると、徹夜の仕事が体に応えるようになる。かつての体力に執着するよりも、今の自分を受け入れることが大切だ。朗らかな気持ちで毎日を過ごせば、心身のバランスは保たれるだろう。"
    essay_sentences = [
        {"id": 1, "audio": "人は年齢を重ねると、徹夜の仕事が体に応えるようになる。",
         "jp": "人は年齢を重ねると、徹夜の仕事が体に<span class='pos-verb'>応える</span>ようになる。",
         "tr": "人一旦上了年纪，熬夜工作就会让身体吃不消。",
         "analysis": "<b>【N2考点拆解】</b><br><b>応える（こたえる）</b>：表示外界强烈的刺激让身体或内心受不了。常搭配“体、暑さ、寒さ”。"},
        {"id": 2, "audio": "かつての体力に執着するよりも、今の自分を受け入れることが大切だ。",
         "jp": "かつての体力に<span class='pos-verb'>執着する</span>よりも、今の自分を受け入れることが大切だ。",
         "tr": "与其对过去的体力耿耿于怀，不如接受现在的自己。",
         "analysis": "<b>【N2考点拆解】</b><br><b>～に執着（しゅうちゃく）する</b>：固定搭配，对前面接续的名词表示执着。"},
        {"id": 3, "audio": "朗らかな気持ちで毎日を過ごせば、心身のバランスは保たれるだろう。",
         "jp": "<span class='pos-adj'>朗らかな</span>気持ちで毎日を過ごせば、心身のバランスは保たれるだろう。",
         "tr": "只要以开朗的心情度过每一天，身心的平衡就能保持下去吧。",
         "analysis": "<b>【N2考点拆解】</b><br><b>朗らか（ほがらか）な</b>：形容动词，修饰名词时加な。形容性格开朗、天气晴朗。"}
    ]
    sprint_30_data = [
        ("錯覚", "さっかく", "错觉"), ("搾取", "さくしゅ", "榨取"), ("察知", "さっち", "察觉"), ("指図", "さしず", "指示"), ("自覚", "じかく", "自觉"),
        ("失脚", "しっきゃく", "倒台"), ("執筆", "しっぴつ", "执笔"), ("借用", "しゃくよう", "借用"), ("修飾", "しゅうしょく", "修饰"), ("手記", "しゅき", "手记"),
        ("熟睡", "じゅくすい", "熟睡"), ("出現", "しゅつげん", "出现"), ("主導", "しゅどう", "主导"), ("樹立", "じゅりつ", "树立"), ("奨励", "しょうれい", "奖励"),
        ("助言", "じょげん", "建议"), ("指令", "しれい", "指令"), ("処置", "しょち", "处置"), ("審査", "しんさ", "审查"), ("親善", "しんぜん", "亲善"),
        ("推進", "すいしん", "推进"), ("遂行", "すいこう", "完成"), ("推測", "すいそく", "推测"), ("崇拝", "すうはい", "崇拜"), ("制圧", "せいあつ", "压制"),
        ("制裁", "せいさい", "制裁"), ("精算", "せいさん", "精算"), ("生還", "せいかん", "生还"), ("切除", "せつじょ", "切除"), ("窃盗", "せっとう", "盗窃")
    ]

# ==========================================
# 渲染页面核心内容 (Tabs)
# ==========================================
with st.container():
    c_left, c_mid, c_right = st.columns([1, 14, 1])
    with c_mid:
        tab1, tab2, tab3 = st.tabs(["📖 核心词说明书", "📝 N2 阅读实战解剖", "🚀 课后 30 词冲刺"])

        # ------------------------------------------
        # TAB 1: 核心词解剖
        # ------------------------------------------
        with tab1:
            mindmap_html = common_head + '<div class="main-container">'
            for data in words_data:
                mindmap_html += f"""
                <div class="mindmap-box hover-enlarge">
                    <div class="mm-root">
                        <div class="mm-word">{data['word']}</div>
                        <div style="color:#8b949e; font-size:1.1rem; margin-bottom:15px;">{data['kana']}</div>
                        <div class="spoiler">🔑 核心词义: {data['direct_tr']}</div>
                        <button class="play-btn" style="margin-top:20px; width:100%; margin-left:0;" onclick="speak('{data['word']}')">🔊 朗读原词</button>
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

        # ------------------------------------------
        # TAB 2: N2 阅读解剖 (真实长文 + 逐句)
        # ------------------------------------------
        with tab2:
            essay_html = common_head + f"""
            <div class="legend-box">
                <div class="legend-title">🧩 N2 词性色彩罗盘</div>
                <div class="legend-item"><div class="color-block" style="background:#ff7b72;"></div> 动词 (Verb)</div>
                <div class="legend-item"><div class="color-block" style="background:#79c0ff;"></div> 副词 (Adv)</div>
                <div class="legend-item"><div class="color-block" style="background:#d2a8ff;"></div> 接续词 (Conj)</div>
                <div class="legend-item"><div class="color-block" style="background:#2ea043;"></div> 代词 (Pron)</div>
                <div class="legend-item"><div class="color-block" style="background:#a5d6ff;"></div> 名词 (Noun)</div>
            </div>
            
            <div class="main-container">
                <div class="essay-fulltext">
                    <div style="color:#fbbf24; font-weight:bold; margin-bottom:10px;">📖 本课实战长文：</div>
                    {essay_full_text}
                    <button class="play-btn" style="display:block; margin-top:20px; margin-left:0;" onclick="speak('{essay_full_text}')">🔊 一键朗读全文</button>
                </div>
            """
            
            for s in essay_sentences:
                essay_html += f"""
                <div class="sen-box hover-enlarge" onclick="toggleSentence({s['id']})">
                    <div class="sen-jp">{s['jp']} <button class="play-btn" style="float:right;" onclick="speak('{s['audio']}', event)">🔊 朗读此句</button></div>
                    <div id="detail_{s['id']}" class="sen-details">
                        <div class="analysis-title">🇨🇳 句子翻译</div>
                        <div class="analysis-content">{s['tr']}</div>
                        <div class="analysis-title">🧠 深度解析</div>
                        <div class="analysis-content">{s['analysis']}</div>
                    </div>
                </div>
                """
            essay_html += "</div>"
            components.html(essay_html, height=900, scrolling=True)

        # ------------------------------------------
        # TAB 3: 课后 30 词 (加入拼写假名 + 刮刮乐)
        # ------------------------------------------
        with tab3:
            sprint_html = common_head + '<div class="main-container"><div class="grid-container">'
            for word, kana, trans in sprint_30_data:
                sprint_html += f"""
                <div class="grid-item hover-enlarge">
                    <div style="font-size: 1.5rem; color: #58a6ff; font-weight: bold; margin-bottom: 2px;">{word}</div>
                    <div class="grid-kana">{kana}</div>
                    <div style="margin-top:10px; margin-bottom:15px;"><span class="spoiler">{trans}</span></div>
                    <button class="play-btn" style="width: 80%; margin:0;" onclick="speak('{word}')">🔊 读音</button>
                </div>
                """
            sprint_html += "</div></div>"
            components.html(sprint_html, height=800, scrolling=True)
