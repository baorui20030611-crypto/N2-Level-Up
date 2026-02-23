import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 1. 页面配置
# ==========================================
st.set_page_config(page_title="N2沉浸式通关引擎 - 完形填空版", page_icon="⛩️", layout="wide")

st.title("⚓ Day 1 - 第1课时：职场与生活效率篇")
st.markdown("---")

# ==========================================
# 2. 公共 HTML 头部 (包含 CSS 和 JS 语音引擎)
# ==========================================
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { font-family: 'Noto Sans JP', sans-serif; background-color: #0e1117; color: #c9d1d9; margin: 0; padding: 10px; }
    
    /* 核心词汇卡片 */
    .word-card { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 15px; margin-bottom: 12px; display: flex; align-items: center; justify-content: space-between; }
    .word-jp { font-size: 1.4rem; color: #58a6ff; font-weight: bold; width: 35%; }
    .word-kana { font-size: 0.9rem; color: #8b949e; font-weight: normal; }
    .word-tr { font-size: 1.1rem; color: #c9d1d9; width: 50%; }
    
    /* 30词网格 */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 10px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 10px; border-radius: 6px; text-align: center; }
    .grid-jp { font-size: 1.2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .grid-tr { font-size: 0.9rem; color: #8b949e; margin-bottom: 8px; }
    
    /* --- 新增：完形填空小作文样式 --- */
    .essay-container { line-height: 2.2; font-size: 1.3rem; padding: 25px; background: #161b22; border-radius: 10px; border: 1px solid #30363d; margin-bottom: 20px;}
    .blank { display: inline-block; min-width: 50px; text-align: center; color: #58a6ff; cursor: pointer; font-weight: bold; transition: all 0.2s; border-bottom: 2px dashed #58a6ff; padding: 0 5px; margin: 0 5px; background: rgba(88, 166, 255, 0.1); border-radius: 4px;}
    .blank:hover { background: rgba(88, 166, 255, 0.2); transform: scale(1.05); }
    .blank.revealed { color: #ff7b72; border-bottom: 2px solid #ff7b72; background: rgba(255, 123, 114, 0.1); }
    
    .analysis-box { margin-top: 20px; padding: 20px; background: #21262d; border-left: 5px solid #2ea043; border-radius: 8px; display: none; animation: fadeIn 0.3s; }
    @keyframes fadeIn { from { opacity: 0; transform: translateY(-10px); } to { opacity: 1; transform: translateY(0); } }
    
    /* 播放按钮 */
    .play-btn { background: #238636; color: white; border: none; border-radius: 4px; padding: 6px 12px; cursor: pointer; font-size: 1rem; }
    .play-btn:hover { background: #2ea043; }
</style>
<script>
    // 零延迟前端语音引擎
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    // 完形填空揭晓逻辑
    function revealAns(id, word, pure_word, note, tr, sentence_audio) {
        // 1. 填入单词并改变样式
        let el = document.getElementById('b' + id);
        el.innerHTML = word;
        el.classList.add('revealed');
        
        // 2. 朗读填入的这个词
        speak(pure_word);
        
        // 3. 显示下方的解析盒子
        let box = document.getElementById('analysis-box');
        box.style.display = 'block';
        document.getElementById('ans-note').innerHTML = "<b>📖 词汇解析：</b>" + note;
        document.getElementById('ans-tr').innerHTML = "<b>🇨🇳 句子翻译：</b>" + tr;
        
        // 4. 更新“朗读此句”按钮的语音内容
        let audioBtn = document.getElementById('ans-audio');
        audioBtn.onclick = function() { speak(sentence_audio); };
    }
</script>
"""

# ==========================================
# 3. 数据层
# ==========================================
core_words = [
    ("捗る", "はかどる", "进展顺利"), ("割り当てる", "わりあてる", "分配"),
    ("備え付ける", "そなえつける", "设置/装备"), ("打ち合わせる", "うちあわせる", "碰头商量"),
    ("見合わせる", "みあわせる", "暂停/推迟"), ("堪える", "こたえる", "吃不消/难受"),
    ("補う", "おぎなう", "弥补/补偿"), ("廃れる", "すたれる", "过时/衰落"),
    ("朗らか", "ほがらか", "开朗"), ("妥協", "だきょう", "妥协"),
    ("執着", "しゅうちゃく", "留恋/执着"), ("漠然", "ばくぜん", "含糊/模糊"),
    ("閲覧", "えつらん", "阅读/浏览"), ("兆し", "きざし", "前兆/兆头"),
    ("合致", "がっち", "一致/吻合")
]

# N2 完形填空大段落数据
essay_full_text = "今日の仕事はとても{b1}。なぜなら、上司が適切に業務を{b2}くれたからです。会議室には新しいモニターが{b3}おり、スムーズに{b4}ことができました。一度は予算の都合で計画を{b5}こともありましたが、{b6}せずに進めば、成功の{b7}が見え、目標に{b8}するはずです。"

essay_blanks = [
    {"id": 1, "word": "捗りました", "pure": "はかどりました", "note": "【捗る】(はかどる)：进展顺利。副词「とても」常与其搭配。", "tr": "今天的工作进展非常顺利。", "audio": "今日の仕事はとても捗りました。"},
    {"id": 2, "word": "割り当てて", "pure": "わりあてて", "note": "【割り当てる】(わりあてる)：分配。将工作分给合适的人。", "tr": "因为上司妥善地分配了任务。", "audio": "なぜなら、上司が適切に業務を割り当ててくれたからです。"},
    {"id": 3, "word": "備え付けられて", "pure": "そなえつけられて", "note": "【備え付ける】(そなえつける)：安装、配备。这里使用了状态形式。", "tr": "会议室里安装了新的显示器。", "audio": "会議室には新しいモニターが備え付けられており、スムーズに打ち合わせることができました。"},
    {"id": 4, "word": "打ち合わせる", "pure": "うちあわせる", "note": "【打ち合わせる】(うちあわせる)：碰头、商量细节。", "tr": "大家沟通商量得非常顺畅。", "audio": "会議室には新しいモニターが備え付けられており、スムーズに打ち合わせることができました。"},
    {"id": 5, "word": "見合わせる", "pure": "みあわせる", "note": "【見合わせる】(みあわせる)：推迟、暂缓。計画を見合わせる = 暂缓计划。", "tr": "虽然一度因为预算问题暂缓过计划。", "audio": "一度は予算の都合で計画を見合わせることもありましたが、妥協せずに進めば、成功の兆しが見え、目標に合致するはずです。"},
    {"id": 6, "word": "妥協", "pure": "だきょう", "note": "【妥協】(だきょう)：妥协。妥協せずに = 不妥协地。", "tr": "但如果不妥协地推进...", "audio": "一度は予算の都合で計画を見合わせることもありましたが、妥協せずに進めば、成功の兆しが見え、目標に合致するはずです。"},
    {"id": 7, "word": "兆し", "pure": "きざし", "note": "【兆し】(きざし)：前兆。成功の兆し = 成功的前兆。", "tr": "就能看到成功的前兆...", "audio": "一度は予算の都合で計画を見合わせることもありましたが、妥協せずに進めば、成功の兆しが見え、目標に合致するはずです。"},
    {"id": 8, "word": "合致", "pure": "がっち", "note": "【合致】(がっち)：一致。目標に合致する = 符合目标。", "tr": "最终一定能符合我们的目标。", "audio": "一度は予算の都合で計画を見合わせることもありましたが、妥協せずに進めば、成功の兆しが見え、目標に合致するはずです。"}
]

sprint_30 = [
    ("合致", "一致"), ("兆し", "前兆"), ("素朴", "纯朴"), ("妥協", "妥协"), ("漠然", "模糊"),
    ("閲覧", "阅读"), ("一転", "突然改变"), ("安堵", "放心"), ("会得", "领会"), ("概説", "概论"),
    ("該当", "符合"), ("介入", "干预"), ("各界", "各界"), ("拡充", "扩充"), ("確保", "确保"),
    ("加味", "加入"), ("関与", "参与"), ("慣習", "习俗"), ("棄権", "弃权"), ("規制", "管制"),
    ("拒絶", "拒绝"), ("許容", "许可"), ("起用", "启用"), ("議決", "表决"), ("却下", "驳回"),
    ("救済", "救济"), ("強要", "强迫"), ("均衡", "平衡"), ("駆使", "运用自如"), ("駆除", "驱除")
]

# ==========================================
# 4. PPT 翻页式布局 (Tabs)
# ==========================================
tab1, tab2, tab3, tab4 = st.tabs(["🎯 1. 课前抽测", "📖 2. 核心精讲 (15词)", "📝 3. N2完形填空实战", "🚀 4. 课后30词扫描"])

with tab1:
    st.subheader("🔔 课前 2 分钟回顾")
    st.info("学习外语最重要的是提取记忆！请在脑海中回想这些词的意思：")
    st.write("1. 捗る (はかどる)  /  2. 割り当てる (わりあてる)  /  3. 備え付ける (そなえつける)")

with tab2:
    html_core = common_head + "<div>"
    for word, kana, trans in core_words:
        html_core += f'<div class="word-card"><div class="word-jp">{word} <span class="word-kana">({kana})</span></div><div class="word-tr">{trans}</div><button class="play-btn" onclick="speak(\'{word}\')">🔊 读音</button></div>'
    html_core += "</div>"
    components.html(html_core, height=600, scrolling=True)

# --- PPT 页面 3：完形填空实战重构 ---
with tab3:
    st.info("💡 操作指南：通读全段，根据上下文猜测空缺处。**点击【数字】即可揭晓答案并朗读，下方会自动弹出该句的详细解析。**")
    
    # 动态生成带点击事件的填空 HTML
    generated_essay = essay_full_text
    for blank in essay_blanks:
        span_html = f"<span class='blank' id='b{blank['id']}' onclick=\"revealAns('{blank['id']}', '{blank['word']}', '{blank['pure']}', '{blank['note']}', '{blank['tr']}', '{blank['audio']}')\">【 {blank['id']} 】</span>"
        generated_essay = generated_essay.replace(f"{{b{blank['id']}}}", span_html)

    html_essay = common_head + f"""
    <div class="essay-container">
        {generated_essay}
    </div>
    
    <button class="play-btn" onclick="speak('今日の仕事はとても捗りました。なぜなら、上司が適切に業務を割り当ててくれたからです。会議室には新しいモニターが備え付けられており、スムーズに打ち合わせることができました。一度は予算の都合で計画を見合わせることもありましたが、妥協せずに進めば、成功の兆しが見え、目標に合致するはずです。')">🔊 一键朗读完整段落</button>
    
    <div id="analysis-box" class="analysis-box">
        <div id="ans-note" style="color: #fbbf24; font-size: 1.1rem; margin-bottom: 10px;"></div>
        <div id="ans-tr" style="color: #c9d1d9; font-size: 1rem; margin-bottom: 15px; border-bottom: 1px dashed #30363d; padding-bottom: 10px;"></div>
        <button class="play-btn" id="ans-audio">🔊 朗读此句</button>
    </div>
    """
    components.html(html_essay, height=700, scrolling=True)

with tab4:
    html_sprint = common_head + '<div class="grid-container">'
    for word, trans in sprint_30:
        html_sprint += f'<div class="grid-item"><div class="grid-jp">{word}</div><div class="grid-tr">{trans}</div><button class="play-btn" style="font-size:0.8rem; padding:4px 8px;" onclick="speak(\'{word}\')">🔊</button></div>'
    html_sprint += "</div>"
    components.html(html_sprint, height=600, scrolling=True)
