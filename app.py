import streamlit as st
import streamlit.components.v1 as components

# ==========================================
# 0. 全局配置与页面初始化
# ==========================================
st.set_page_config(page_title="N2沉浸式通关引擎 - Day1完整版", page_icon="⛩️", layout="wide")

# ==========================================
# 1. 核心 HTML/CSS/JS 引擎 (主编级 UI + 全栈交互)
# ==========================================
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { font-family: 'Noto Sans JP', sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 15px; display: flex; justify-content: center; }
    .main-container { width: 100%; max-width: 1200px; margin: 0 auto; }
    
    /* --- 播放按钮 (统一圆润风格) --- */
    .play-btn { background: #2ea043; color: white; border: none; border-radius: 4px; padding: 5px 12px; cursor: pointer; font-size: 0.9rem; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.3); vertical-align: middle; margin-left: 8px;}
    .play-btn:hover { background: #3fb950; transform: scale(1.05); }

    /* --- 无痕防作弊翻译 (同背景色，悬停变金) --- */
    .hidden-tr { color: #161b22; transition: color 0.3s ease; cursor: default; user-select: none; font-weight: bold; background: #161b22; border-radius: 4px; padding: 2px 5px; display: inline-block;}
    .hidden-tr:hover { color: #fbbf24; background: transparent; }

    /* --- 词性色彩罗盘 (符合主编要求) --- */
    .pos-verb { color: #ff7b72; font-weight: bold; border-bottom: 2px solid rgba(255, 123, 114, 0.3); padding-bottom: 1px;} 
    .pos-adv { color: #79c0ff; font-weight: bold; border-bottom: 2px solid rgba(121, 192, 255, 0.3); padding-bottom: 1px;} 
    .pos-conj { color: #d2a8ff; font-weight: bold; border-bottom: 2px solid rgba(210, 168, 255, 0.3); padding-bottom: 1px;} 
    .pos-pron { color: #2ea043; font-weight: bold; border-bottom: 2px solid rgba(46, 160, 67, 0.3); padding-bottom: 1px;} 
    .pos-adj { color: #ffa657; font-weight: bold; border-bottom: 2px solid rgba(255, 166, 87, 0.3); padding-bottom: 1px;} 
    .pos-noun { color: #a5d6ff; font-weight: bold; border-bottom: 2px solid rgba(165, 214, 255, 0.3); padding-bottom: 1px;} 
    
    /* --- 右下角图例 (固定悬浮) --- */
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.95); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); z-index: 9999; font-size: 0.85rem; backdrop-filter: blur(5px);}
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }

    /* --- 核心词精讲卡片 (思维导图式，PPT分页) --- */
    .mindmap-box { display: flex; align-items: stretch; background: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 25px; transition: 0.3s; }
    .mindmap-box:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.4); border-color:#58a6ff; }
    .mm-root { flex: 0 0 240px; background: #21262d; text-align: center; padding: 30px 20px; border-right: 3px solid #58a6ff; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 12px 0 0 12px;}
    .mm-word { font-size: 2.2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .mm-branches { flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #0d1117; padding: 20px; border-radius: 8px; border-left: 4px solid #8957e5; position: relative;}
    .mm-usage { font-size: 1.15rem; color: #fbbf24; font-weight: bold; margin-bottom: 8px; border-bottom: 1px dashed #30363d; padding-bottom: 5px; display: inline-block;}
    .mm-sentence { font-size: 1.3rem; color: #c9d1d9; margin-bottom: 12px; line-height: 1.6; }
    .mm-note { font-size: 0.95rem; color: #8b949e; margin-bottom: 10px; background: rgba(56, 139, 253, 0.1); padding: 8px; border-radius: 4px; border-left: 3px solid #79c0ff;}
    
    /* --- 聚光灯长文阅读 (绝对不跳动) --- */
    .essay-container { font-size: 1.4rem; line-height: 2.6; background: #161b22; padding: 50px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #30363d; text-align: justify; letter-spacing: 0.5px; position: relative;}
    .sen-span { transition: all 0.3s ease; padding: 4px 6px; border-radius: 6px; cursor: pointer; }
    
    /* 悬停状态下，未选中的虚化 */
    .essay-container.is-hovering .sen-span { filter: blur(4px); opacity: 0.3; }
    /* 选中的高亮 */
    .essay-container.is-hovering .sen-span.active-hover { filter: blur(0); opacity: 1; background: #21262d; box-shadow: 0 4px 15px rgba(0,0,0,0.6); border-bottom: 2px solid #58a6ff; z-index: 10; position: relative;}

    /* 句末内嵌语音按钮 (默认隐藏，聚光灯打中时显示) */
    .inline-play-btn { opacity: 0; pointer-events: none; margin-left: 10px; font-size: 0.95rem; background: #2ea043; border: none; border-radius: 4px; color: white; padding: 2px 8px; cursor: pointer; transition: 0.2s; vertical-align: middle;}
    .sen-span.active-hover .inline-play-btn { opacity: 1; pointer-events: auto; }
    .inline-play-btn:hover { background: #3fb950; transform: scale(1.1); }

    /* 悬浮硬核解析框 (Tooltip) */
    .floating-box { position: absolute; background: #0d1117; border: 1px solid #30363d; border-top: 4px solid #fbbf24; border-radius: 8px; padding: 25px; width: 600px; box-shadow: 0 10px 40px rgba(0,0,0,0.95); z-index: 1000; display: none; pointer-events: none; }
    .analysis-title { color: #fbbf24; font-size: 1.1rem; font-weight: bold; margin-bottom: 12px; border-bottom: 1px dashed #30363d; padding-bottom: 8px;}
    .analysis-content { color: #c9d1d9; line-height: 1.8; font-size: 1.05rem; }
    
    /* --- 课前复习小游戏 --- */
    .game-box { background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; margin-bottom:20px; display: flex; align-items: center; justify-content: space-between; border-left: 5px solid #ff7b72;}
    .game-q { font-size: 1.6rem; color: #58a6ff; font-weight: bold; width: 30%;}
    .game-opts { width: 65%; display: flex; gap: 10px; }
    .game-opt { flex: 1; background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 15px; border-radius: 6px; cursor: pointer; font-size: 1.1rem; transition: 0.2s; text-align: center; }
    .game-opt:hover { background: #30363d; border-color: #58a6ff; }
    .game-opt.correct { background: #238636 !important; color: white !important; border-color: #2ea043 !important; pointer-events: none; }
    .game-opt.wrong { background: #da3633 !important; color: white !important; border-color: #f85149 !important; pointer-events: none; }

    /* 30词冲刺网格 */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 20px 15px; border-radius: 8px; text-align: center; transition: 0.3s; }
    .grid-item:hover { transform: translateY(-3px); box-shadow: 0 5px 15px rgba(0,0,0,0.4); border-color: #58a6ff;}
</style>

<script>
    // 前端发音函数 (SpeechSynthesis)
    function speak(text, event) {
        if(event) event.stopPropagation();
        window.speechSynthesis.cancel();
        let u = new SpeechSynthesisUtterance(text);
        u.lang = 'ja-JP'; u.rate = 0.85;
        window.speechSynthesis.speak(u);
    }
    
    // 聚光灯与悬浮窗逻辑
    let floatBox = null;
    window.onload = function() { floatBox = document.getElementById('global-floating-box'); }

    function onSenEnter(e, id) {
        let sen = document.getElementById('sen_' + id);
        let container = document.getElementById('essay-box');
        container.classList.add('is-hovering');
        sen.classList.add('active-hover');
        
        floatBox.innerHTML = document.getElementById('data_' + id).innerHTML;
        floatBox.style.display = 'block';
        
        // 动态计算，保证悬浮窗贴在鼠标下方
        // 增加 offset 防止遮挡
        let top = e.pageY + 40;
        let left = Math.max(20, e.pageX - 300);
        
        floatBox.style.top = top + 'px';
        floatBox.style.left = left + 'px'; 
    }
    
    function onSenMove(e) {
        if(floatBox && floatBox.style.display === 'block') {
             let top = e.pageY + 40;
             let left = Math.max(20, e.pageX - 300);
             floatBox.style.top = top + 'px';
             floatBox.style.left = left + 'px';
        }
    }

    function onSenLeave(id) {
        let sen = document.getElementById('sen_' + id);
        let container = document.getElementById('essay-box');
        container.classList.remove('is-hovering');
        sen.classList.remove('active-hover');
        floatBox.style.display = 'none';
    }

    // 复习游戏判定逻辑
    function checkGame(btn, isCorrect, wordAudio) {
        if(isCorrect) {
            btn.classList.add('correct'); btn.innerHTML += " ✅"; speak(wordAudio);
        } else {
            btn.classList.add('wrong'); btn.innerHTML += " ❌";
        }
    }
</script>
"""

# ==========================================
# 2. 数据工厂 (Day 1: Lesson 1 & Lesson 2)
# ==========================================

# -----------------
# Lesson 1 数据 (职场/效率)
# -----------------
l1_words = [
    {"word": "捗る", "kana": "はかどる", "direct_tr": "进展顺利", "usages": [
        {"meaning": "① 事物或工作顺利进展", "jp": "計画が予定通りに捗っている。", "pure": "けいかくがよていどおりにはかどっている", "tr": "计划正按预期顺利进行。", "note": "【N2考点】常与「仕事」「勉強」等搭配。"},
        {"meaning": "② 搭配副词（とても/順調に）", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。", "note": "【辨析】强调“速度快、效率高”，区别于「進む」(单纯的前进)。"}
    ]},
    {"word": "割り当てる", "kana": "わりあてる", "direct_tr": "分配/分摊", "usages": [
        {"meaning": "① 分配任务给具体的人", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。", "note": "【辨析】「分ける」是单纯分开，「割り当てる」强调按责任或比例分配。"},
        {"meaning": "② 分配物理资源", "jp": "一部屋に二人ずつ割り当てる。", "pure": "ひとへやにふたりずつわりあてる", "tr": "按每间房两个人进行分配。", "note": "【N2考点】阅读中常搭配表示基准的「～ずつ」。"}
    ]},
    {"word": "備え付ける", "kana": "そなえつける", "direct_tr": "设置/装备", "usages": [
        {"meaning": "① 在特定场所固定安装", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。", "note": "【辨析】与「備える」(防备/具备) 不同，强烈暗示物理上的“安装”。"}
    ]},
    {"word": "打ち合わせる", "kana": "うちあわせる", "direct_tr": "商量/碰头", "usages": [
        {"meaning": "① 事前商量细节", "jp": "会議の前に詳細を打ち合わせる。", "pure": "かいぎのまえにしょうさいをうちあわせる", "tr": "会议前商量一下细节。", "note": "【N2考点】名词形式「打ち合わせ」在职场日语中极高频。"}
    ]},
    {"word": "見合わせる", "kana": "みあわせる", "direct_tr": "暂停/推迟", "usages": [
        {"meaning": "① 暂停、推迟计划", "jp": "悪天候のため、出発を見合わせる。", "pure": "あくてんこうのため、しゅっぱつをみあわせる", "tr": "因为天气恶劣，推迟出发。", "note": "【N2考点】听力中高频词，听到这个词说明活动取消或延期。"},
        {"meaning": "② 互相看着对方", "jp": "二人は顔を見合わせて笑った。", "pure": "ふたりはかおをみあわせてわらった", "tr": "两人面面相觑笑了起来。", "note": "【固定搭配】结合「顔を」使用。"}
    ]},
    {"word": "堪える", "kana": "こたえる", "direct_tr": "吃不消/难受", "usages": [
        {"meaning": "① 外在刺激让身心难以忍受", "jp": "この寒さは体に応える。", "pure": "このさむさはからだにこたえる", "tr": "这寒冷真让身体吃不消。", "note": "【N2考点】读音是こたえる，切忌读成たえる(忍耐)。"}
    ]},
    {"word": "補う", "kana": "おぎなう", "direct_tr": "弥补/补充", "usages": [
        {"meaning": "① 弥补不足之处", "jp": "経験の不足を努力で補う。", "pure": "けいけんのふそくをどりょくでおぎなう", "tr": "用努力来弥补经验的不足。", "note": "【近义词】「カバーする」，填补空白或弱点。"}
    ]},
    {"word": "廃れる", "kana": "すたれる", "direct_tr": "过时/衰落", "usages": [
        {"meaning": "① 风俗或流行消退", "jp": "古い慣習は次第に廃れていく。", "pure": "ふるいかんしゅうはしだいにすたれていく", "tr": "旧习俗渐渐衰落了。", "note": "【近义词辨析】区别于「滅びる」(彻底灭亡)，仅表示不再流行。"}
    ]},
    {"word": "朗らか", "kana": "ほがらか", "direct_tr": "开朗/晴朗", "usages": [
        {"meaning": "① 性格阳光", "jp": "彼女は朗らかな性格で人気がある。", "pure": "かのじょはほがらかなせいかくで人気がある", "tr": "她性格开朗很受欢迎。", "note": "【词性】形容动词（～な）。"}
    ]},
    {"word": "妥協", "kana": "だきょう", "direct_tr": "妥协", "usages": [
        {"meaning": "① 双方让步达成一致", "jp": "品質については絶対に妥協しない。", "pure": "ひんしつについてはぜったいにだきょうしない", "tr": "在品质上绝对不妥协。", "note": "【固定搭配】妥協を許さない（绝不妥协）。"}
    ]},
    {"word": "執着", "kana": "しゅうちゃく", "direct_tr": "留恋/执着", "usages": [
        {"meaning": "① 迷恋事物不肯放弃", "jp": "過去の栄光に執着する。", "pure": "かこのえいこうにしゅうちゃくする", "tr": "执着于过去的辉煌。", "note": "【N2考点】常接助词「～に」。"}
    ]},
    {"word": "漠然", "kana": "ばくぜん", "direct_tr": "模糊/含糊", "usages": [
        {"meaning": "① 不清晰，没有具体形态", "jp": "将来に対して漠然とした不安を抱く。", "pure": "しょうらいにたいしてばくぜんとしたふあんをいだく", "tr": "对未来抱有模糊的不安。", "note": "【固定搭配】漠然とした（修饰名词）。"}
    ]},
    {"word": "閲覧", "kana": "えつらん", "direct_tr": "阅读/浏览", "usages": [
        {"meaning": "① 查阅资料或网页", "jp": "図書館の貴重な資料を閲覧する。", "pure": "としょかんのきちょうなしりょうをえつらんする", "tr": "查阅图书馆的珍贵资料。", "note": "【N2考点】正式文书用语。"}
    ]},
    {"word": "兆し", "kana": "きざし", "direct_tr": "前兆", "usages": [
        {"meaning": "① 事情发生前的迹象", "jp": "景気回復の兆しが見え始めた。", "pure": "けいきかいふくのきざしがみえはじめた", "tr": "开始显现出经济复苏的迹象。", "note": "【常考句型】～の兆しが見える（看到...的前兆）。"}
    ]},
    {"word": "合致", "kana": "がっち", "direct_tr": "一致/吻合", "usages": [
        {"meaning": "① 意见、条件等完全符合", "jp": "双方の意見が完全に合致した。", "pure": "そうほうのいけんがかんぜんにがっちした", "tr": "双方的意见完全一致。", "note": "【近义词】「一致する」。"}
    ]}
]

l1_sentences = [
    {"id": "s1", "audio": "最近、多くの企業でリモートワークが導入され、働き方が一変した。",
     "jp": " <span class='pos-noun'>最近</span>、多くの<span class='pos-noun'>企業</span>でリモートワークが導入され、働き方が<span class='pos-verb'>一変した</span>。",
     "html": "<b>【翻訳】</b>最近，许多企业引入了远程办公，工作方式发生了巨变。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>～が導入される</b>：被动语态。N2阅读极爱考察被动，客观描述社会现象。<br>🔹 <b>一変（いっぺん）した</b>：名词+する。表示状态发生彻底的改变。"},
    {"id": "s2", "audio": "それに伴い、自宅での仕事がとても捗ると感じる人がいる一方で、対面でのコミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も頻繁に聞かれる。",
     "jp": "<span class='pos-conj'>それに伴い</span>、自宅での仕事が<span class='pos-adv'>とても</span><span class='pos-verb'>捗る</span>と感じる<span class='pos-noun'>人</span>がいる<span class='pos-conj'>一方で</span>、対面でのコミュニケーションの不足から、業務を適切に<span class='pos-verb'>割り当てる</span>ことが難しくなったという声も<span class='pos-adv'>頻繁に</span>聞かれる。",
     "html": "<b>【翻訳】</b>伴随于此，一方面有人觉得在家的工作进展非常顺利，另一方面由于缺乏面对面沟通，也有人表示难以妥善分配业务。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>～に伴い（にともない）</b>：随着前项变化，后项也变化。<br>🔹 <b>～一方で（いっぽうで）</b>：N2核心接续！表示事物的正反两面。<br>🔹 <b>とても + 捗る</b>：本课核心动词，效率极高。<br>🔹 <b>割り当てる</b>：本课核心词，分配任务。"},
    {"id": "s3", "audio": "また、自宅に仕事用のデスクや高性能なパソコンを備え付けるための費用も、無視できない課題となっている。",
     "jp": "<span class='pos-conj'>また</span>、自宅に仕事用のデスクや高性能なパソコンを<span class='pos-verb'>備え付ける</span><span class='pos-conj'>ための</span>費用も、無視できない課題となっている。",
     "html": "<b>【翻訳】</b>此外，为了在家里配备办公桌和电脑的费用，也成了一个不可忽视的课题。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>備え付ける（そなえつける）</b>：动词，安装、配备（固定设施）。<br>🔹 <b>ための</b>：接动词原形后，修饰名词“費用”，表示目的。"},
    {"id": "s4", "audio": "しかし、環境の変化にただ嘆くのではなく、決して妥協せずに、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが必ず見えてくるだろう。",
     "jp": "<span class='pos-conj'>しかし</span>、環境の変化に<span class='pos-adv'>ただ</span>嘆くのではなく、<span class='pos-adv'>決して</span><span class='pos-verb'>妥協</span>せずに、オンラインで<span class='pos-adv'>こまめに</span><span class='pos-verb'>打ち合わせる</span>ことで、新しい働き方の<span class='pos-noun'>兆し</span>が<span class='pos-adv'>必ず</span>見えてくるだろう。",
     "html": "<b>【翻訳】</b>然而，不要仅仅哀叹变化，只要绝不妥协，在线上勤加商量，就一定会看到新工作方式的曙光。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>決して～ない</b>：N2副词呼应。“绝不...”。<br>🔹 <b>こまめに</b>：频繁地、勤加（高频词）。<br>🔹 <b>兆し（きざし）</b>：本课核心名词，前兆、曙光。"},
    {"id": "s5", "audio": "古い慣習が徐々に廃れるのは時代の必然的な流れであり、私たちは互いに足りない部分を補う努力を怠ってはならない。",
     "jp": "古い<span class='pos-noun'>慣習</span>が<span class='pos-adv'>徐々に</span><span class='pos-verb'>廃れる</span>のは時代の必然的な流れであり、<span class='pos-pron'>私たち</span>は互いに足りない部分を<span class='pos-verb'>補う</span>努力を怠ってはならない。",
     "html": "<b>【翻訳】</b>旧习惯的衰落是时代必然趋势，我们绝不能懈怠去努力弥补不足。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>廃れる / 補う</b>：本课核心动词，衰落 / 弥补。<br>🔹 <b>～てはならない</b>：N2强烈禁止语法，“绝不能...”。"}
]

sprint_30_l1 = [
    ("合致", "がっち", "一致"), ("兆し", "きざし", "前兆"), ("素朴", "そぼく", "纯朴"), ("妥協", "だきょう", "妥协"), ("漠然", "ばくぜん", "模糊"),
    ("閲覧", "えつらん", "阅读"), ("一転", "いってん", "突然改变"), ("安堵", "あんど", "放心"), ("会得", "えとく", "领会"), ("概説", "がいせつ", "概论"),
    ("該当", "がいとう", "符合"), ("介入", "かいにゅう", "干预"), ("各界", "かくかい", "各界"), ("拡充", "かくじゅう", "扩充"), ("確保", "かくほ", "确保"),
    ("加味", "かみ", "加入"), ("関与", "かんよ", "参与"), ("慣習", "かんしゅう", "习俗"), ("棄権", "きけん", "弃权"), ("規制", "きせい", "管制"),
    ("拒絶", "きょぜつ", "拒绝"), ("許容", "きょよう", "许可"), ("起用", "きよう", "启用"), ("議決", "ぎけつ", "表决"), ("却下", "きゃっか", "驳回"),
    ("救済", "きゅうさい", "救济"), ("強要", "きょうよう", "强迫"), ("均衡", "きんこう", "平衡"), ("駆使", "くし", "运用自如"), ("駆除", "くじょ", "驱除")
]

# -----------------
# Lesson 2 数据 (心理/状态)
# -----------------
l2_words = [
    {"word": "錯覚", "kana": "さっかく", "direct_tr": "错觉/误会", "usages": [
        {"meaning": "① 感官上的错觉", "jp": "線が曲がっているように見えるのは目の錯覚だ。", "pure": "せんがまがっているようにみえるのはめのさっかくだ", "tr": "看起来线弯曲了，这只是视觉错觉。", "note": "【考点】常搭配「目の～」。"},
        {"meaning": "② 认知上的自作多情", "jp": "彼が私を好きだと錯覚していた。", "pure": "かれがわたしをすきだとはっかくしていた", "tr": "我产生了他喜欢我的错觉。", "note": "【辨析】用于心理活动，表示想多了。"}
    ]},
    {"word": "察知", "kana": "さっち", "direct_tr": "察觉/感知", "usages": [
        {"meaning": "① 提前察觉到危险", "jp": "危険をいち早く察知して避難する。", "pure": "きけんをいちはやくさっちしてひなんする", "tr": "尽早察觉到危险并避难。", "note": "【固定搭配】常接「危険を～」「変化を～」。"}
    ]},
    {"word": "指図", "kana": "さしず", "direct_tr": "指示/命令", "usages": [
        {"meaning": "① 以上对下的指手画脚", "jp": "他人からあれこれ指図されるのは不愉快だ。", "pure": "たにんからあれこれさしずされるのはふゆかいだ", "tr": "被别人指手画脚让人很不愉快。", "note": "【N2考点】被动语态「指図される」常用来表达作者的不满。"}
    ]},
    {"word": "自覚", "kana": "じかく", "direct_tr": "自觉/意识到", "usages": [
        {"meaning": "① 认识到自己的状态", "jp": "プロとしての自覚が足りない。", "pure": "ぷろとしてのじかくがたりない", "tr": "作为专业人士的自觉性不够。", "note": "【固定搭配】「自覚を持つ」「自覚が足りない」。"}
    ]},
    {"word": "失脚", "kana": "しっきゃく", "direct_tr": "下台/垮台", "usages": [
        {"meaning": "① 失去地位", "jp": "スキャンダルが原因で大臣が失脚した。", "pure": "すきゃんだるがげんいんでだいじんがしっきゃくした", "tr": "因为丑闻大臣下台了。", "note": "【考点】新闻日语高频词。"}
    ]},
    {"word": "執筆", "kana": "しっぴつ", "direct_tr": "执笔/写作", "usages": [
        {"meaning": "① 写文章、写书", "jp": "現在、新しい小説を執筆中です。", "pure": "げんざい、あたらしいしょうせつをしっぴつちゅうです", "tr": "目前正在写新的小说。", "note": "【辨析】比「書く」更正式，专指创作类写作。"}
    ]},
    {"word": "借用", "kana": "しゃくよう", "direct_tr": "借用", "usages": [
        {"meaning": "① 借用物品或金钱", "jp": "会議室を一時的に借用する。", "pure": "かいぎしつをいちじてきにしゃくようする", "tr": "暂时借用会议室。", "note": "【考点】公文书面语。"}
    ]},
    {"word": "修飾", "kana": "しゅうしょく", "direct_tr": "修饰", "usages": [
        {"meaning": "① 语法上的修饰", "jp": "形容詞が名詞を修飾する。", "pure": "けいようしがめいしをしゅうしょくする", "tr": "形容词修饰名词。", "note": "【辨析】区别于「装飾」(物理上的装饰)。"}
    ]},
    {"word": "手記", "kana": "しゅき", "direct_tr": "手记/笔记", "usages": [
        {"meaning": "① 亲身经历的记录", "jp": "戦争の体験を手記にまとめる。", "pure": "せんそうのたいけんをしゅきにまとめる", "tr": "将战争的体验整理成手记。", "note": "【固定搭配】手記を残す（留存手记）。"}
    ]},
    {"word": "熟睡", "kana": "じゅくすい", "direct_tr": "熟睡", "usages": [
        {"meaning": "① 睡得很深", "jp": "疲れていたので、朝まで熟睡した。", "pure": "つかれていたので、あさまでじゅくすいした", "tr": "因为很累，熟睡到了天亮。", "note": "【近义词】「ぐっすり眠る」。"}
    ]},
    {"word": "出現", "kana": "しゅつげん", "direct_tr": "出现", "usages": [
        {"meaning": "① 出乎意料地出现", "jp": "空に未確認の飛行物体が出現した。", "pure": "そらにみかくにんのひこうぶったいがしゅつげんした", "tr": "空中出现了不明飞行物。", "note": "【辨析】带有突然性或神秘感。"}
    ]},
    {"word": "主導", "kana": "しゅどう", "direct_tr": "主导", "usages": [
        {"meaning": "① 起带头作用", "jp": "政府が主導して経済改革を進める。", "pure": "せいふがしゅどうしてけいざいかいかくをすすめる", "tr": "由政府主导推进经济改革。", "note": "【固定搭配】主導権を握る（掌握主导权）。"}
    ]},
    {"word": "樹立", "kana": "じゅりつ", "direct_tr": "树立/建立", "usages": [
        {"meaning": "① 建立国家或刷新纪录", "jp": "新しい世界記録が樹立された。", "pure": "あたらしいせかいきろくがじゅりつされた", "tr": "树立了新的世界纪录。", "note": "【固定搭配】新記録の樹立。"}
    ]},
    {"word": "奨励", "kana": "しょうれい", "direct_tr": "鼓励/奖励", "usages": [
        {"meaning": "① 鼓励做某事", "jp": "会社は資格の取得を奨励している。", "pure": "かいしゃはしかくのしゅとくをしょうれいしている", "tr": "公司鼓励员工考取资格证。", "note": "【辨析】侧重精神上的鼓舞和提倡。"}
    ]},
    {"word": "助言", "kana": "じょげん", "direct_tr": "建议/忠告", "usages": [
        {"meaning": "① 给予建议", "jp": "専門家から適切な助言をもらう。", "pure": "せんもんかからてきせつなじょげんをもらう", "tr": "从专家那里获得恰当的建议。", "note": "【近义词】「アドバイス」。"}
    ]}
]

l2_sentences = [
    {"id": "l2s1", "audio": "若手社員の中には、自分が会社の中心であると錯覚している者が少なくない。",
     "jp": " 若手社員の中には、<span class='pos-pron'>自分</span>が会社の中心であると<span class='pos-verb'>錯覚している</span>者が少なくない。",
     "html": "<b>【翻訳】</b>在年轻员工中，有不少人错觉自己是公司的核心。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>錯覚（さっかく）している</b>：本课核心动词，产生错觉。<br>🔹 <b>者が少なくない</b>：双重否定表肯定，表示“不在少数”。"},
    {"id": "l2s2", "audio": "彼らは、上司から少しでも指図されると、すぐに不満を顔に出す。",
     "jp": "<span class='pos-pron'>彼ら</span>は、上司から<span class='pos-adv'>少しでも</span><span class='pos-verb'>指図される</span>と、<span class='pos-adv'>すぐに</span>不満を顔に出す。",
     "html": "<b>【翻訳】</b>他们只要被上司稍微指示一下，就会立刻把不满写在脸上。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>指図（さしず）される</b>：被指示、被命令。带消极色彩。"},
    {"id": "l2s3", "audio": "しかし、組織の中で働く以上、周囲の空気を察知し、自覚を持って行動することが求められる。",
     "jp": "<span class='pos-conj'>しかし</span>、組織の中で働く<span class='pos-conj'>以上</span>、周囲の空気を<span class='pos-verb'>察知し</span>、<span class='pos-noun'>自覚</span>を持って行動することが求められる。",
     "html": "<b>【翻訳】</b>但是，既然在组织中工作，就被要求要能察觉周围的气氛，并带着自觉性去行动。<br><br><b>【《新完全掌握》文法解剖】</b><br>🔹 <b>～以上（いじょう）</b>：N2必考语法。既然...就必须...。<br>🔹 <b>察知 / 自覚</b>：本课核心词。"}
]

sprint_30_l2 = [
    ("錯覚", "さっかく", "错觉"), ("搾取", "さくしゅ", "榨取"), ("察知", "さっち", "察觉"), ("指図", "さしず", "指示"), ("自覚", "じかく", "自觉"),
    ("失脚", "しっきゃく", "倒台"), ("執筆", "しっぴつ", "执笔"), ("借用", "しゃくよう", "借用"), ("修飾", "しゅうしょく", "修饰"), ("手記", "しゅき", "手记"),
    ("熟睡", "じゅくすい", "熟睡"), ("出現", "しゅつげん", "出现"), ("主導", "しゅどう", "主导"), ("樹立", "じゅりつ", "树立"), ("奨励", "しょうれい", "奖励"),
    ("助言", "じょげん", "建议"), ("指令", "しれい", "指令"), ("処置", "しょち", "处置"), ("審査", "しんさ", "审查"), ("親善", "しんぜん", "亲善"),
    ("推進", "すいしん", "推进"), ("遂行", "すいこう", "完成"), ("推測", "すいそく", "推测"), ("崇拝", "すうはい", "崇拜"), ("制圧", "せいあつ", "压制"),
    ("制裁", "せいさい", "制裁"), ("精算", "せいさん", "精算"), ("生還", "せいかん", "生还"), ("切除", "せつじょ", "切除"), ("窃盗", "せっとう", "盗窃")
]

# ==========================================
# 3. 页面渲染逻辑
# ==========================================

# --- 侧边栏 ---
st.sidebar.title("🏮 N2 冲刺系统")
selected_lesson = st.sidebar.radio("📚 选择课时", ["Day 1 - 第1课时 (职场效率)", "Day 1 - 第2课时 (心理状态)"])
st.sidebar.markdown("---")
st.sidebar.write("🎵 **专注氛围**")
music_choice = st.sidebar.selectbox("背景音", ["无", "赵雷风舒缓民谣吉他", "沉浸 Lo-Fi 纯音"])
if music_choice == "赵雷风舒缓民谣吉他":
    st.sidebar.audio("https://cdn.pixabay.com/download/audio/2022/02/10/audio_fc8eb4c7cd.mp3", format="audio/mp3")
elif music_choice == "沉浸 Lo-Fi 纯音":
    st.sidebar.audio("https://cdn.pixabay.com/download/audio/2022/05/27/audio_1808fbf07a.mp3", format="audio/mp3")

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center; color: #e6edf3;'>{selected_lesson}</h2>", unsafe_allow_html=True)
    st.markdown("---")

# --- 页面容器 ---
with st.container():
    c_left, c_mid, c_right = st.columns([1, 15, 1])
    with c_mid:
        
        # 逻辑分支：第1课时 vs 第2课时
        if "第1课时" in selected_lesson:
            # Day 1 Lesson 1: 无复习环节
            tabs = st.tabs(["📖 核心词精讲", "📝 聚光灯阅读", "🚀 30词冲刺"])
            tab_core, tab_reading, tab_sprint = tabs[0], tabs[1], tabs[2]
            
            # 数据绑定
            current_words = l1_words
            current_sentences = l1_sentences
            current_sprint = sprint_30_l1

        else:
            # Day 1 Lesson 2: 必须包含“课前复习游戏”
            tabs = st.tabs(["🎮 课前复习(Day1)", "📖 核心词精讲", "📝 聚光灯阅读", "🚀 30词冲刺"])
            tab_game, tab_core, tab_reading, tab_sprint = tabs[0], tabs[1], tabs[2], tabs[3]
            
            # 数据绑定
            current_words = l2_words
            current_sentences = l2_sentences
            current_sprint = sprint_30_l2

            # --- 渲染复习游戏 ---
            with tab_game:
                st.info("💡 温故知新：根据中文选出上节课学过的正确日语单词！")
                html_game = common_head + """
                <div class="main-container">
                    <div class="game-box">
                        <div class="game-q">Q1. 进展顺利</div>
                        <div class="game-opts">
                            <button class="game-opt" onclick="checkGame(this, false, '')">A. そなえつける</button>
                            <button class="game-opt" onclick="checkGame(this, true, 'はかどる')">B. はかどる</button>
                            <button class="game-opt" onclick="checkGame(this, false, '')">C. みあわせる</button>
                        </div>
                    </div>
                    <div class="game-box">
                        <div class="game-q">Q2. 暂停、推迟</div>
                        <div class="game-opts">
                            <button class="game-opt" onclick="checkGame(this, true, 'みあわせる')">A. みあわせる</button>
                            <button class="game-opt" onclick="checkGame(this, false, '')">B. わりあてる</button>
                            <button class="game-opt" onclick="checkGame(this, false, '')">C. おぎなう</button>
                        </div>
                    </div>
                </div>
                """
                components.html(html_game, height=350)

        # --- 渲染核心词 (PPT分页逻辑) ---
        with tab_core:
            st.info("💡 提示：已开启【PPT分页模式】。每次只学 3 个词，深度掌握多重用法。")
            ppt_page = st.radio("选择讲义页码：", ["📜 第1页 (词1-3)", "📜 第2页 (词4-6)", "📜 第3页 (词7-9)", "📜 第4页 (词10-12)", "📜 第5页 (词13-15)"], horizontal=True, label_visibility="collapsed")
            
            # 分页切片逻辑
            start_idx = 0
            if "第2页" in ppt_page: start_idx = 3
            elif "第3页" in ppt_page: start_idx = 6
            elif "第4页" in ppt_page: start_idx = 9
            elif "第5页" in ppt_page: start_idx = 12
            
            display_words = current_words[start_idx : start_idx + 3]
            
            mindmap_html = common_head + '<div class="main-container">'
            for data in display_words:
                mindmap_html += f"""
                <div class="mindmap-box">
                    <div class="mm-root">
                        <div class="mm-word">{data['word']}</div>
                        <div style="color:#8b949e; font-size:1.1rem; margin-bottom:15px;">{data['kana']}</div>
                        <div class="hidden-tr">👁️ 翻译: {data['direct_tr']}</div>
                        <button class="play-btn" style="margin-top:20px; width:100%;" onclick="speak('{data['word']}')">🔊 读原词</button>
                    </div>
                    <div class="mm-branches">
                """
                for u in data['usages']:
                    mindmap_html += f"""
                        <div class="mm-branch">
                            <div class="mm-usage">{u['meaning']}</div>
                            <div class="mm-note">{u['note']}</div>
                            <div class="mm-sentence">{u['jp']} <button class="play-btn" onclick="speak('{u['pure']}')">🔊</button></div>
                            <div class="hidden-tr">🇨🇳 翻译: {u['tr']}</div>
                        </div>
                    """
                mindmap_html += "</div></div>"
            mindmap_html += "</div>"
            components.html(mindmap_html, height=850, scrolling=True)

        # --- 渲染聚光灯阅读 ---
        with tab_reading:
            # 预埋解析数据到隐藏 div
            hidden_data_html = ""
            for s in current_sentences:
                hidden_data_html += f"<div id='data_{s['id']}' style='display:none;'>{s['html']}</div>"
            
            essay_html = common_head + hidden_data_html + f"""
            <div class="legend-box">
                <div class="legend-title">🧩 N2 词性色彩罗盘</div>
                <div class="legend-item"><div class="color-block" style="background:#ff7b72;"></div> 动词 (Verb)</div>
                <div class="legend-item"><div class="color-block" style="background:#79c0ff;"></div> 副词 (Adv)</div>
                <div class="legend-item"><div class="color-block" style="background:#d2a8ff;"></div> 接续词 (Conj)</div>
                <div class="legend-item"><div class="color-block" style="background:#2ea043;"></div> 代词 (Pron)</div>
                <div class="legend-item"><div class="color-block" style="background:#ffa657;"></div> 形容词 (Adj)</div>
                <div class="legend-item"><div class="color-block" style="background:#a5d6ff;"></div> 名词 (Noun)</div>
            </div>
            
            <div class="main-container">
                <div class="essay-container" id="essay-box">
            """
            for s in current_sentences:
                essay_html += f"""
                <span class='sen-span' id='sen_{s['id']}' onmouseenter=\"onSenEnter(event, '{s['id']}')\" onmousemove=\"onSenMove(event)\" onmouseleave=\"onSenLeave('{s['id']}')\">
                    {s['jp']} <button class='inline-play-btn' onclick=\"speak('{s['audio']}', event)\">🔊</button>
                </span>
                """
            essay_html += """
                </div>
                <div id="global-floating-box" class="floating-box">
                    <div class="analysis-title"><span>🧠 新完全掌握 - 深度解剖</span></div>
                    <div class="analysis-content" id="analysis-inner"></div>
                </div>
            </div>
            """
            components.html(essay_html, height=750, scrolling=True)

        # --- 渲染30词冲刺 ---
        with tab_sprint:
            sprint_html = common_head + '<div class="main-container"><div class="grid-container">'
            for word, kana, trans in current_sprint:
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
