import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="N2沉浸式通关引擎 - 教辅满载版", page_icon="⛩️", layout="wide")

# ==========================================
# 核心 HTML/CSS/JS (极致丝滑防跳动 + 悬浮解析 + 无痕翻译)
# ==========================================
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { font-family: 'Noto Sans JP', sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 20px; display: flex; justify-content: center; }
    .main-container { width: 100%; max-width: 1100px; margin: 0 auto; }
    
    /* --- 无痕防作弊翻译 (颜色与卡片背景一致，悬停变金) --- */
    .hidden-tr { color: #161b22; transition: color 0.3s ease; cursor: default; user-select: none; font-weight: bold; }
    .hidden-tr:hover { color: #fbbf24; }

    /* 播放按钮 */
    .play-btn { background: #2ea043; color: white; border: none; border-radius: 4px; padding: 6px 15px; cursor: pointer; font-size: 0.95rem; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.3);}
    .play-btn:hover { background: #3fb950; transform: scale(1.05); }

    /* 词性色彩罗盘 */
    .pos-verb { color: #ff7b72; font-weight: bold; border-bottom: 1px dashed #ff7b72; } 
    .pos-adv { color: #79c0ff; font-weight: bold; border-bottom: 1px dashed #79c0ff; } 
    .pos-conj { color: #d2a8ff; font-weight: bold; border-bottom: 1px dashed #d2a8ff; } 
    .pos-pron { color: #2ea043; font-weight: bold; border-bottom: 1px dashed #2ea043; } 
    .pos-adj { color: #ffa657; font-weight: bold; border-bottom: 1px dashed #ffa657; } 
    .pos-noun { color: #a5d6ff; font-weight: bold; border-bottom: 1px dashed #a5d6ff; } 
    
    /* 右下角图例 */
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.95); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); z-index: 1000; font-size: 0.9rem; backdrop-filter: blur(5px);}
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }

    /* --- 思维导图样式 --- */
    .mindmap-box { display: flex; align-items: stretch; background: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 25px; transition: 0.3s; }
    .mindmap-box:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.4); border-color:#58a6ff; }
    .mm-root { flex: 0 0 220px; background: #21262d; text-align: center; padding: 30px 20px; border-right: 3px solid #58a6ff; display: flex; flex-direction: column; justify-content: center; align-items: center;}
    .mm-word { font-size: 2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .mm-branches { flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #0d1117; padding: 15px; border-radius: 8px; border-left: 4px solid #8957e5; }
    .mm-usage { font-size: 1.1rem; color: #e6edf3; font-weight: bold; margin-bottom: 10px; }
    .mm-sentence { font-size: 1.25rem; color: #c9d1d9; margin-bottom: 10px; line-height: 1.6; }
    
    /* --- 🚀 N2 长文：绝对不跳动的聚光灯特效 --- */
    .essay-container { font-size: 1.35rem; line-height: 2.4; background: #161b22; padding: 40px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #30363d; text-align: justify; letter-spacing: 0.5px; transition: 0.3s; position: relative;}
    
    /* 句子基础样式：不改变大小，防止跳动 */
    .sen-span { transition: all 0.3s ease; padding: 2px 4px; border-radius: 5px; cursor: pointer; }
    
    /* 悬停文章时，所有句子虚化 */
    .essay-container.is-hovering .sen-span { filter: blur(4px); opacity: 0.3; }
    
    /* 被悬停的句子：解除虚化，背景高亮，不改变font-size */
    .essay-container.is-hovering .sen-span.active-hover { filter: blur(0); opacity: 1; background: #21262d; box-shadow: 0 2px 10px rgba(0,0,0,0.5); border-bottom: 2px solid #58a6ff; z-index: 10; }

    /* 句末内嵌语音按钮 (默认隐藏，悬停显示) */
    .inline-play-btn { opacity: 0; pointer-events: none; margin-left: 10px; font-size: 0.95rem; background: #2ea043; border: none; border-radius: 4px; color: white; padding: 4px 10px; cursor: pointer; transition: 0.2s; vertical-align: middle;}
    .sen-span.active-hover .inline-play-btn { opacity: 1; pointer-events: auto; }
    .inline-play-btn:hover { background: #3fb950; transform: scale(1.1); }

    /* 悬浮解析框 (Tooltip) - 绝对定位，彻底告别页面跳动 */
    .floating-box { position: absolute; background: #0d1117; border: 1px solid #30363d; border-top: 4px solid #fbbf24; border-radius: 8px; padding: 25px; width: 600px; box-shadow: 0 10px 30px rgba(0,0,0,0.8); z-index: 1000; display: none; pointer-events: none; /* 让鼠标可以穿透它，防止闪烁 */ }
    .analysis-title { color: #fbbf24; font-size: 1.15rem; font-weight: bold; margin-bottom: 12px; border-bottom: 1px dashed #30363d; padding-bottom: 8px;}
    .analysis-content { color: #c9d1d9; line-height: 1.8; font-size: 1.05rem; }
    
    /* 30词网格 */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 20px 15px; border-radius: 8px; text-align: center; transition: 0.3s; }
    .grid-item:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.4); border-color: #58a6ff;}
</style>

<script>
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    // 悬浮解析与聚光灯逻辑
    let floatBox = null;
    window.onload = function() { floatBox = document.getElementById('global-floating-box'); }

    function onSenEnter(e, id) {
        let sen = document.getElementById('sen_' + id);
        let container = document.getElementById('essay-box');
        
        container.classList.add('is-hovering');
        sen.classList.add('active-hover');
        
        // 抓取隐藏的解析数据注入悬浮框
        floatBox.innerHTML = document.getElementById('data_' + id).innerHTML;
        floatBox.style.display = 'block';
        
        // 动态定位：悬浮在鼠标正下方 30px 处
        floatBox.style.top = (e.pageY + 30) + 'px';
        floatBox.style.left = Math.max(20, e.pageX - 300) + 'px'; // 保证不超出左边界
    }
    
    function onSenMove(e) {
        // 让悬浮窗跟随鼠标移动，如影随形
        if(floatBox && floatBox.style.display === 'block') {
            floatBox.style.top = (e.pageY + 30) + 'px';
            floatBox.style.left = Math.max(20, e.pageX - 300) + 'px';
        }
    }

    function onSenLeave(id) {
        let sen = document.getElementById('sen_' + id);
        let container = document.getElementById('essay-box');
        container.classList.remove('is-hovering');
        sen.classList.remove('active-hover');
        floatBox.style.display = 'none';
    }
</script>
"""

# ==========================================
# 侧边栏与导航
# ==========================================
st.sidebar.title("🏮 N2 冲刺系统")
selected_lesson = st.sidebar.radio("📚 选择课时", ["Day 1 - 第1课时 (职场15词)", "Day 1 - 第2课时 (状态进阶)"])
st.sidebar.markdown("---")

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center; color: #e6edf3;'>{selected_lesson}</h2>", unsafe_allow_html=True)
    st.markdown("---")

# ==========================================
# 动态加载数据 (全满载 15 词)
# ==========================================
if "第1课时" in selected_lesson:
    # 满载 15 个核心词
    words_data = [
        {"word": "捗る", "kana": "はかどる", "direct_tr": "进展顺利", "usages": [{"meaning": "事物或工作顺利进展", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。"}]},
        {"word": "割り当てる", "kana": "わりあてる", "direct_tr": "分配/分摊", "usages": [{"meaning": "分配任务或资源", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。"}]},
        {"word": "備え付ける", "kana": "そなえつける", "direct_tr": "设置/装备", "usages": [{"meaning": "固定安装机械、家具", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。"}]},
        {"word": "打ち合わせる", "kana": "うちあわせる", "direct_tr": "商量/碰头", "usages": [{"meaning": "事前商量细节", "jp": "会議の前に詳細を打ち合わせる。", "pure": "かいぎのまえにしょうさいをうちあわせる", "tr": "会议前商量一下细节。"}]},
        {"word": "見合わせる", "kana": "みあわせる", "direct_tr": "暂停/推迟", "usages": [{"meaning": "暂时搁置计划", "jp": "悪天候のため、出発を見合わせる。", "pure": "あくてんこうのため、しゅっぱつをみあわせる", "tr": "因为天气恶劣，推迟出发。"}]},
        {"word": "堪える", "kana": "こたえる", "direct_tr": "吃不消", "usages": [{"meaning": "强烈刺激让人难以忍受", "jp": "この寒さは体に応える。", "pure": "このさむさはからだにこたえる", "tr": "这寒冷真让身体吃不消。"}]},
        {"word": "補う", "kana": "おぎなう", "direct_tr": "弥补/补充", "usages": [{"meaning": "弥补不足之处", "jp": "経験の不足を努力で補う。", "pure": "けいけんのふそくをどりょくでおぎなう", "tr": "用努力来弥补经验的不足。"}]},
        {"word": "廃れる", "kana": "すたれる", "direct_tr": "过时/衰落", "usages": [{"meaning": "不再流行", "jp": "古い慣習は次第に廃れていく。", "pure": "ふるいかんしゅうはしだいにすたれていく", "tr": "旧习俗渐渐衰落了。"}]},
        {"word": "朗らか", "kana": "ほがらか", "direct_tr": "开朗/晴朗", "usages": [{"meaning": "性格开朗，无忧无虑", "jp": "彼女は朗らかな性格で人気がある。", "pure": "かのじょはほがらかなせいかくで人気がある", "tr": "她性格开朗很受欢迎。"}]},
        {"word": "妥協", "kana": "だきょう", "direct_tr": "妥协", "usages": [{"meaning": "双方让步达成一致", "jp": "品質については絶対に妥協しない。", "pure": "ひんしつについてはぜったいにだきょうしない", "tr": "在品质上绝对不妥协。"}]},
        {"word": "執着", "kana": "しゅうちゃく", "direct_tr": "留恋/执着", "usages": [{"meaning": "迷恋事物不肯放弃", "jp": "過去の栄光に執着する。", "pure": "かこのえいこうにしゅうちゃくする", "tr": "执着于过去的辉煌。"}]},
        {"word": "漠然", "kana": "ばくぜん", "direct_tr": "模糊/含糊", "usages": [{"meaning": "不清晰，没有具体形态", "jp": "将来に対して漠然とした不安を抱く。", "pure": "しょうらいにたいしてばくぜんとしたふあんをいだく", "tr": "对未来抱有模糊的不安。"}]},
        {"word": "閲覧", "kana": "えつらん", "direct_tr": "阅读/浏览", "usages": [{"meaning": "查阅资料、网页等", "jp": "図書館の貴重な資料を閲覧する。", "pure": "としょかんのきちょうなしりょうをえつらんする", "tr": "查阅图书馆的珍贵资料。"}]},
        {"word": "兆し", "kana": "きざし", "direct_tr": "前兆", "usages": [{"meaning": "事情发生前的迹象", "jp": "景気回復の兆しが見え始めた。", "pure": "けいきかいふくのきざしがみえはじめた", "tr": "开始显现出经济复苏的迹象。"}]},
        {"word": "合致", "kana": "がっち", "direct_tr": "一致/吻合", "usages": [{"meaning": "意见、条件等完全符合", "jp": "双方の意見が完全に合致した。", "pure": "そうほうのいけんがかんぜんにがっちした", "tr": "双方的意见完全一致。"}]}
    ]
    
    # 超过 150 字的 N2 实战长文
    essay_full_text = "最近、多くの企業でリモートワークが導入され、働き方が一変した。それに伴い、自宅での仕事がとても捗ると感じる人がいる一方で、対面でのコミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も頻繁に聞かれる。また、自宅に仕事用のデスクや高性能なパソコンを備え付けるための費用も、無視できない課題となっている。しかし、環境の変化にただ嘆くのではなく、決して妥協せずに、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが必ず見えてくるだろう。古い慣習が徐々に廃れるのは時代の必然的な流れであり、私たちは互いに足りない部分を補う努力を怠ってはならない。"
    
    sentences = [
        {"id": 1, "audio": "最近、多くの企業でリモートワークが導入され、働き方が一変した。",
         "jp": "<span class='pos-noun'>最近</span>、多くの<span class='pos-noun'>企業</span>でリモートワークが導入され、働き方が一変した。",
         "html": "<b>【翻訳】</b>最近，许多企业引入了远程办公，工作方式发生了巨变。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>～が導入される</b>：被动语态。N2阅读常考，描述客观事实。<br>🔹 <b>一変（いっぺん）した</b>：名词+する。表示“完全改变”。"},
        {"id": 2, "audio": "それに伴い、自宅での仕事がとても捗ると感じる人がいる一方で、対面でのコミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も頻繁に聞かれる。",
         "jp": "<span class='pos-conj'>それに伴い</span>、自宅での仕事が<span class='pos-adv'>とても</span><span class='pos-verb'>捗る</span>と感じる人がいる<span class='pos-conj'>一方で</span>、対面でのコミュニケーションの不足から、業務を適切に<span class='pos-verb'>割り当てる</span>ことが難しくなったという声も<span class='pos-adv'>頻繁に</span>聞かれる。",
         "html": "<b>【翻訳】</b>伴随于此，一方面有人觉得在家的工作进展顺利，另一方面由于缺乏面对面沟通，也有人表示难以妥善分配业务。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>～に伴い（にともない）</b>：随着前项变化，后项也变化。<br>🔹 <b>～一方で（いっぽうで）</b>：N2核心！表示同一事物的两个相对面。<br>🔹 <b>とても + 捗る</b>：效率极高。<br>🔹 <b>割り当てる</b>：本课核心动词，分配。"},
        {"id": 3, "audio": "また、自宅に仕事用のデスクや高性能なパソコンを備え付けるための費用も、無視できない課題となっている。",
         "jp": "<span class='pos-conj'>また</span>、自宅に仕事用のデスクや高性能なパソコンを<span class='pos-verb'>備え付ける</span><span class='pos-conj'>ための</span>費用も、無視できない課題となっている。",
         "html": "<b>【翻訳】</b>此外，为了在家里配备办公桌和电脑的费用，也成了一个不可忽视的课题。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>備え付ける（そなえつける）</b>：动词，安装、配备（固定设施）。<br>🔹 <b>ための</b>：接动词原形后，修饰名词“費用”，表示目的。"},
        {"id": 4, "audio": "しかし、環境の変化にただ嘆くのではなく、決して妥協せずに、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが必ず見えてくるだろう。",
         "jp": "<span class='pos-conj'>しかし</span>、環境の変化にただ嘆くのではなく、<span class='pos-adv'>決して</span><span class='pos-verb'>妥協</span>せずに、オンラインで<span class='pos-adv'>こまめに</span><span class='pos-verb'>打ち合わせる</span>ことで、新しい働き方の<span class='pos-noun'>兆し</span>が必ず見えてくるだろう。",
         "html": "<b>【翻訳】</b>然而，不要仅仅哀叹变化，只要绝不妥协，在线上勤加商量，就一定会看到新工作方式的曙光。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>決して～ない</b>：N2副词呼应。“绝不...”。<br>🔹 <b>こまめに</b>：频繁地、勤加（高频词）。<br>🔹 <b>兆し（きざし）</b>：本课核心词，前兆、曙光。"},
        {"id": 5, "audio": "古い慣習が徐々に廃れるのは時代の必然的な流れであり、私たちは互いに足りない部分を補う努力を怠ってはならない。",
         "jp": "古い<span class='pos-noun'>慣習</span>が<span class='pos-adv'>徐々に</span><span class='pos-verb'>廃れる</span>のは時代の必然的な流れであり、<span class='pos-pron'>私たち</span>は互いに足りない部分を<span class='pos-verb'>補う</span>努力を怠ってはならない。",
         "html": "<b>【翻訳】</b>旧习惯的衰落是时代必然趋势，我们绝不能懈怠去努力弥补不足。<br><br><b>【文型・文法解剖】</b><br>🔹 <b>廃れる（すたれる）/ 補う（おぎなう）</b>：本课核心动词，衰落 / 弥补。<br>🔹 <b>～てはならない</b>：N2强烈禁止语法，“绝不能...”。"}
    ]

else:
    # --- 第 2 课时 数据 ---
    words_data = [
        {"word": "堪える", "kana": "こたえる", "direct_tr": "吃不消", "usages": [{"meaning": "难以忍受外在刺激", "jp": "今年の夏の暑さは体に応える。", "pure": "ことしのなつのあつさはからだにこたえる", "tr": "今年夏天的炎热真让身体吃不消。"}]},
        {"word": "執着", "kana": "しゅうちゃく", "direct_tr": "留恋/执着", "usages": [{"meaning": "迷恋事物不肯放弃", "jp": "過去の栄光に執着しても意味がない。", "pure": "かこのえいこうにしゅうちゃくしてもいみが無い", "tr": "对过去的辉煌斤斤计较也没有意义。"}]}
    ]
    essay_full_text = "人は年齢を重ねるとともに、徹夜の仕事が体に応えるようになる。かつての体力にむやみに執着するよりも、衰えゆく自分を素直に受け入れることが大切だ。"
    sentences = [
        {"id": 1, "audio": "人は年齢を重ねるとともに、徹夜の仕事が体に応えるようになる。", "jp": "<span class='pos-noun'>人</span>は年齢を重ねる<span class='pos-conj'>とともに</span>、徹夜の仕事が体に<span class='pos-verb'>応える</span>ようになる。", "html": "<b>【翻訳】</b>随着年龄的增长，熬夜工作变得让身体吃不消了。<br><br><b>【解剖】</b><br>🔹 <b>～とともに</b>：随着...同时发生。"}
    ]

# 统一 30 词冲刺包 (含假名)
sprint_30_data = [
    ("合致", "がっち", "一致"), ("兆し", "きざし", "前兆"), ("素朴", "そぼく", "纯朴"), ("妥協", "だきょう", "妥协"), ("漠然", "ばくぜん", "模糊"),
    ("閲覧", "えつらん", "阅读"), ("一転", "いってん", "突然改变"), ("安堵", "あんど", "放心"), ("会得", "えとく", "领会"), ("概説", "がいせつ", "概论"),
    ("該当", "がいとう", "符合"), ("介入", "かいにゅう", "干预"), ("各界", "かくかい", "各界"), ("拡充", "かくじゅう", "扩充"), ("確保", "かくほ", "确保"),
    ("加味", "かみ", "加入"), ("関与", "かんよ", "参与"), ("慣習", "かんしゅう", "习俗"), ("棄権", "きけん", "弃权"), ("規制", "きせい", "管制"),
    ("拒絶", "きょぜつ", "拒绝"), ("許容", "きょよう", "许可"), ("起用", "きよう", "启用"), ("議決", "ぎけつ", "表决"), ("却下", "きゃっか", "驳回"),
    ("救済", "きゅうさい", "救济"), ("強要", "きょうよう", "强迫"), ("均衡", "きんこう", "平衡"), ("駆使", "くし", "运用自如"), ("駆除", "くじょ", "驱除")
]

# ==========================================
# 渲染页面 (Tabs)
# ==========================================
with st.container():
    c_left, c_mid, c_right = st.columns([1, 14, 1])
    with c_mid:
        tab1, tab2, tab3 = st.tabs(["📖 核心词满载库", "📝 N2 阅读实战解剖", "🚀 课后 30 词冲刺"])

        # ------------------------------------------
        # TAB 1: 核心词解剖 (隐形翻译)
        # ------------------------------------------
        with tab1:
            mindmap_html = common_head + '<div class="main-container">'
            for data in words_data:
                mindmap_html += f"""
                <div class="mindmap-box">
                    <div class="mm-root">
                        <div class="mm-word">{data['word']}</div>
                        <div style="color:#8b949e; font-size:1.1rem; margin-bottom:15px;">{data['kana']}</div>
                        <div class="hidden-tr">👁️ 翻译: {data['direct_tr']}</div>
                        <button class="play-btn" style="margin-top:20px; width:100%; margin-left:0;" onclick="speak('{data['word']}')">🔊 朗读原词</button>
                    </div>
                    <div class="mm-branches">
                """
                for u in data['usages']:
                    mindmap_html += f"""
                        <div class="mm-branch">
                            <div class="mm-usage">{u['meaning']}</div>
                            <div class="mm-sentence">{u['jp']} <button class="play-btn" onclick="speak('{u['pure']}')">🔊</button></div>
                            <div class="hidden-tr">🇨🇳 {u['tr']}</div>
                        </div>
                    """
                mindmap_html += "</div></div>"
            mindmap_html += "</div>"
            components.html(mindmap_html, height=800, scrolling=True)

        # ------------------------------------------
        # TAB 2: N2 阅读解剖 (终极不跳动聚光灯)
        # ------------------------------------------
        with tab2:
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
            
            for s in sentences:
                essay_html += f"""
                <span class='sen-span' id='sen_{s['id']}' onmouseenter=\"onSenEnter(event, '{s['id']}')\" onmousemove=\"onSenMove(event)\" onmouseleave=\"onSenLeave('{s['id']}')\">
                    {s['jp']}
                    <button class='inline-play-btn' onclick=\"speak('{s['audio']}', event)\">🔊</button>
                </span>
                """
                
            essay_html += """
                </div>
                <div id="global-floating-box" class="floating-box">
                    <div class="analysis-title"><span>🧠 教辅级解剖</span></div>
                    <div class="analysis-content" id="analysis-inner"></div>
                </div>
            </div>
            """
            components.html(essay_html, height=850, scrolling=True)

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
                    <div style="margin-bottom:15px;"><span class="hidden-tr">👁️ {trans}</span></div>
                    <button class="play-btn" style="width: 80%; margin:0;" onclick="speak('{word}')">🔊 读音</button>
                </div>
                """
            sprint_html += "</div></div>"
            components.html(sprint_html, height=800, scrolling=True)
