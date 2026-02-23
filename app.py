import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="N2沉浸式通关引擎 - 殿堂版", page_icon="⛩️", layout="wide")

# ==========================================
# 核心 HTML/CSS/JS (PPT分页 + 悬浮解析 + 无痕翻译 + 复习游戏)
# ==========================================
common_head = """
<style>
    @import url('https://fonts.googleapis.com/css2?family=Noto+Sans+JP:wght@400;700&display=swap');
    body { font-family: 'Noto Sans JP', sans-serif; background-color: #0d1117; color: #c9d1d9; margin: 0; padding: 15px; display: flex; justify-content: center; }
    .main-container { width: 100%; max-width: 1100px; margin: 0 auto; }
    
    /* 播放按钮 */
    .play-btn { background: #2ea043; color: white; border: none; border-radius: 4px; padding: 6px 15px; cursor: pointer; font-size: 0.95rem; transition: 0.2s; box-shadow: 0 2px 5px rgba(0,0,0,0.3);}
    .play-btn:hover { background: #3fb950; transform: scale(1.05); }

    /* 无痕防作弊翻译 (同背景色，悬停变金) */
    .hidden-tr { color: #161b22; transition: color 0.3s ease; cursor: default; user-select: none; font-weight: bold; background: #161b22; border-radius: 4px;}
    .hidden-tr:hover { color: #fbbf24; background: transparent;}

    /* 词性色彩罗盘 */
    .pos-verb { color: #ff7b72; font-weight: bold; border-bottom: 1px dashed #ff7b72; padding-bottom: 2px;} 
    .pos-adv { color: #79c0ff; font-weight: bold; border-bottom: 1px dashed #79c0ff; padding-bottom: 2px;} 
    .pos-conj { color: #d2a8ff; font-weight: bold; border-bottom: 1px dashed #d2a8ff; padding-bottom: 2px;} 
    .pos-pron { color: #2ea043; font-weight: bold; border-bottom: 1px dashed #2ea043; padding-bottom: 2px;} 
    .pos-adj { color: #ffa657; font-weight: bold; border-bottom: 1px dashed #ffa657; padding-bottom: 2px;} 
    .pos-noun { color: #a5d6ff; font-weight: bold; border-bottom: 1px dashed #a5d6ff; padding-bottom: 2px;} 
    
    /* 右下角图例 */
    .legend-box { position: fixed; bottom: 20px; right: 20px; background: rgba(22,27,34,0.95); border: 1px solid #30363d; padding: 15px; border-radius: 10px; box-shadow: 0 4px 15px rgba(0,0,0,0.8); z-index: 1000; font-size: 0.9rem; backdrop-filter: blur(5px);}
    .legend-title { font-weight: bold; color: #e6edf3; margin-bottom: 10px; text-align: center; border-bottom: 1px solid #30363d; padding-bottom: 5px;}
    .legend-item { margin-bottom: 5px; display: flex; align-items: center; }
    .color-block { width: 12px; height: 12px; border-radius: 3px; margin-right: 8px; }

    /* --- 教辅级词汇精讲卡片 --- */
    .mindmap-box { display: flex; align-items: stretch; background: #161b22; border: 1px solid #30363d; border-radius: 12px; margin-bottom: 25px; transition: 0.3s; }
    .mindmap-box:hover { box-shadow: 0 8px 20px rgba(0,0,0,0.4); border-color:#58a6ff; }
    .mm-root { flex: 0 0 220px; background: #21262d; text-align: center; padding: 30px 20px; border-right: 3px solid #58a6ff; display: flex; flex-direction: column; justify-content: center; align-items: center; border-radius: 12px 0 0 12px;}
    .mm-word { font-size: 2.2rem; color: #58a6ff; font-weight: bold; margin-bottom: 5px; }
    .mm-branches { flex: 1; padding: 25px; display: flex; flex-direction: column; gap: 15px; }
    .mm-branch { background: #0d1117; padding: 20px; border-radius: 8px; border-left: 4px solid #8957e5; }
    .mm-usage { font-size: 1.15rem; color: #fbbf24; font-weight: bold; margin-bottom: 12px; border-bottom: 1px solid #30363d; padding-bottom: 8px;}
    .mm-sentence { font-size: 1.3rem; color: #c9d1d9; margin-bottom: 12px; line-height: 1.6; }
    .mm-note { font-size: 1rem; color: #8b949e; margin-bottom: 10px; background: #161b22; padding: 8px; border-radius: 4px;}
    
    /* --- 聚光灯长文阅读 (绝对不跳动) --- */
    .essay-container { font-size: 1.35rem; line-height: 2.5; background: #161b22; padding: 40px; border-radius: 12px; margin-bottom: 30px; border: 1px solid #30363d; text-align: justify; letter-spacing: 0.5px; position: relative;}
    .sen-span { transition: all 0.3s ease; padding: 4px 6px; border-radius: 6px; cursor: pointer; }
    
    .essay-container.is-hovering .sen-span { filter: blur(4px); opacity: 0.3; }
    .essay-container.is-hovering .sen-span.active-hover { filter: blur(0); opacity: 1; background: #21262d; box-shadow: 0 2px 10px rgba(0,0,0,0.6); border-bottom: 2px solid #58a6ff; z-index: 10; }

    /* 句末内嵌语音按钮 */
    .inline-play-btn { opacity: 0; pointer-events: none; margin-left: 10px; font-size: 0.95rem; background: #2ea043; border: none; border-radius: 4px; color: white; padding: 4px 10px; cursor: pointer; transition: 0.2s; vertical-align: middle;}
    .sen-span.active-hover .inline-play-btn { opacity: 1; pointer-events: auto; }
    .inline-play-btn:hover { background: #3fb950; transform: scale(1.1); }

    /* 悬浮解析框 (Tooltip) */
    .floating-box { position: absolute; background: #0d1117; border: 1px solid #30363d; border-top: 4px solid #fbbf24; border-radius: 8px; padding: 25px; width: 650px; box-shadow: 0 10px 40px rgba(0,0,0,0.9); z-index: 1000; display: none; pointer-events: none; }
    .analysis-title { color: #fbbf24; font-size: 1.15rem; font-weight: bold; margin-bottom: 12px; border-bottom: 1px dashed #30363d; padding-bottom: 8px;}
    .analysis-content { color: #c9d1d9; line-height: 1.8; font-size: 1.05rem; }
    
    /* --- 课前复习小游戏 --- */
    .game-box { background: #161b22; padding: 25px; border-radius: 12px; border: 1px solid #30363d; margin-bottom:20px; display: flex; align-items: center; justify-content: space-between; border-left: 5px solid #ff7b72;}
    .game-q { font-size: 1.6rem; color: #58a6ff; font-weight: bold; width: 30%;}
    .game-opts { width: 65%; display: flex; gap: 10px; }
    .game-opt { flex: 1; background: #21262d; border: 1px solid #30363d; color: #c9d1d9; padding: 15px; border-radius: 6px; cursor: pointer; font-size: 1.1rem; transition: 0.2s; text-align: center; }
    .game-opt:hover { background: #30363d; border-color: #58a6ff; }
    .game-opt.correct { background: #238636; color: white; border-color: #2ea043; pointer-events: none; }
    .game-opt.wrong { background: #da3633; color: white; border-color: #f85149; pointer-events: none; }

    /* 30词网格 */
    .grid-container { display: grid; grid-template-columns: repeat(5, 1fr); gap: 15px; }
    .grid-item { background: #161b22; border: 1px solid #30363d; padding: 20px 15px; border-radius: 8px; text-align: center; transition: 0.3s; }
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
        
        floatBox.innerHTML = document.getElementById('data_' + id).innerHTML;
        floatBox.style.display = 'block';
        
        // 解析框紧贴在鼠标下方
        floatBox.style.top = (e.pageY + 30) + 'px';
        floatBox.style.left = Math.max(20, e.pageX - 325) + 'px'; 
    }
    
    function onSenMove(e) {
        if(floatBox && floatBox.style.display === 'block') {
            floatBox.style.top = (e.pageY + 30) + 'px';
            floatBox.style.left = Math.max(20, e.pageX - 325) + 'px';
        }
    }

    function onSenLeave(id) {
        let sen = document.getElementById('sen_' + id);
        let container = document.getElementById('essay-box');
        container.classList.remove('is-hovering');
        sen.classList.remove('active-hover');
        floatBox.style.display = 'none';
    }

    // 复习游戏检查
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
# 数据中枢 (Day 1 - 课时1 & 课时2 满载数据)
# ==========================================
# 课时 1 核心词 (展示前6个作为示例，保证多重用法)
l1_words = [
    {"word": "捗る", "kana": "はかどる", "direct_tr": "进展顺利", "usages": [
        {"meaning": "用法①：事物或工作顺利进展", "jp": "計画が予定通りに捗っている。", "pure": "けいかくがよていどおりにはかどっている", "tr": "计划正按预期顺利进行。", "note": "【考点】常与「仕事」「勉強」搭配。"},
        {"meaning": "用法②：搭配副词（とても/順調に）", "jp": "今日は涼しいので、勉強がとても捗る。", "pure": "きょうはすずしいので、べんきょうがとてもはかどる", "tr": "今天很凉快，所以学习效率非常高。", "note": "【考点】在完形填空中，看到「とても」要能联想到状态的极致。"}
    ]},
    {"word": "割り当てる", "kana": "わりあてる", "direct_tr": "分配/分摊", "usages": [
        {"meaning": "用法①：分配任务给具体的人", "jp": "新入社員に簡単な仕事を割り当てる。", "pure": "しんにゅうしゃいんにかんたんなしごとをわりあてる", "tr": "把简单的工作分配给新员工。", "note": "【辨析】「分ける」是单纯分开，「割り当てる」强调按比例或角色分配。"},
        {"meaning": "用法②：分配物理资源", "jp": "一部屋に二人ずつ割り当てる。", "pure": "ひとへやにふたりずつわりあてる", "tr": "按每间房两个人进行分配。", "note": "【考点】常搭配表示基准的「～ずつ」。"}
    ]},
    {"word": "備え付ける", "kana": "そなえつける", "direct_tr": "设置/装备", "usages": [
        {"meaning": "用法①：在特定场所固定安装", "jp": "各部屋にエアコンを備え付けてある。", "pure": "かくへやにエアコンをそなえつけてある", "tr": "每个房间都配备了空调。", "note": "【辨析】与「備える」(防备/具备) 不同，强烈暗示物理上的“安装”。"}
    ]},
    {"word": "見合わせる", "kana": "みあわせる", "direct_tr": "暂停/推迟/互看", "usages": [
        {"meaning": "用法①：暂停、推迟计划", "jp": "悪天候のため、出発を見合わせる。", "pure": "あくてんこうのため、しゅっぱつをみあわせる", "tr": "因为天气恶劣，推迟出发。", "note": "【考点】N2听力中极高频词，听到这个词说明活动取消或延期。"},
        {"meaning": "用法②：互相看着对方", "jp": "二人は顔を見合わせて笑った。", "pure": "ふたりはかおをみあわせてわらった", "tr": "两人面面相觑笑了起来。", "note": "【考点】字面原始意思，结合「顔を」使用。"}
    ]},
    {"word": "堪える", "kana": "こたえる", "direct_tr": "吃不消/难受", "usages": [
        {"meaning": "用法①：外在刺激让身心难以忍受", "jp": "この寒さは体に応える。", "pure": "このさむさはからだにこたえる", "tr": "这寒冷真让身体吃不消。", "note": "【辨析】读音是こたえる，不要和「たえる」(忍耐) 搞混。"}
    ]},
    {"word": "補う", "kana": "おぎなう", "direct_tr": "弥补/补充", "usages": [
        {"meaning": "用法①：弥补不足之处", "jp": "経験の不足を努力で補う。", "pure": "けいけんのふそくをどりょくでおぎなう", "tr": "用努力来弥补经验的不足。", "note": "【考点】接续词「補足（ほそく）」的动词形态。"}
    ]}
]

# 课时 2 核心词
l2_words = [
    {"word": "錯覚", "kana": "さっかく", "direct_tr": "错觉/误会", "usages": [
        {"meaning": "用法①：感官上的错觉", "jp": "線が曲がっているように見えるのは目の錯覚だ。", "pure": "せんがまがっているようにみえるのはめのさっかくだ", "tr": "看起来线弯曲了，这只是视觉错觉。", "note": "【考点】常搭配「目の～」。"},
        {"meaning": "用法②：认知上的误会（自作多情）", "jp": "彼が私を好きだと錯覚していた。", "pure": "かれがわたしをすきだとはっかくしていた", "tr": "我产生了他喜欢我的错觉。", "note": "【考点】用于心理活动，表示想多了。"}
    ]},
    {"word": "察知", "kana": "さっち", "direct_tr": "察觉/感知", "usages": [
        {"meaning": "用法①：提前察觉到危险或变化", "jp": "危険をいち早く察知して避難する。", "pure": "きけんをいちはやくさっちしてひなんする", "tr": "尽早察觉到危险并避难。", "note": "【考点】常接「危険を～」「変化を～」。"}
    ]},
    {"word": "指図", "kana": "さしず", "direct_tr": "指示/命令", "usages": [
        {"meaning": "用法①：以上对下的命令（常带不满语气）", "jp": "他人からあれこれ指図されるのは不愉快だ。", "pure": "たにんからあれこれさしずされるのはふゆかいだ", "tr": "被别人指手画脚让人很不愉快。", "note": "【考点】被动语态「指図される」在阅读中常用来表达作者的不满。"}
    ]},
    {"word": "自覚", "kana": "じかく", "direct_tr": "自觉/意识到", "usages": [
        {"meaning": "用法①：清楚认识到自己的立场或状态", "jp": "プロとしての自覚が足りない。", "pure": "ぷろとしてのじかくがたりない", "tr": "作为专业人士的自觉性不够。", "note": "【考点】「自覚を持つ」「自覚が足りない」为固定搭配。"}
    ]},
    {"word": "失脚", "kana": "しっきゃく", "direct_tr": "下台/垮台", "usages": [
        {"meaning": "用法①：因失去信任而失去地位", "jp": "スキャンダルが原因で大臣が失脚した。", "pure": "すきゃんだるがげんいんでだいじんがしっきゃくした", "tr": "因为丑闻大臣下台了。", "note": "【考点】新闻日语高频词。"}
    ]},
    {"word": "執筆", "kana": "しっぴつ", "direct_tr": "执笔/写作", "usages": [
        {"meaning": "用法①：写文章、写书", "jp": "現在、新しい小説を執筆中です。", "pure": "げんざい、あたらしいしょうせつをしっぴつちゅうです", "tr": "目前正在写新的小说。", "note": "【辨析】比「書く」更正式，专指创作类写作。"}
    ]}
]

# 课时 1 N2 级别阅读长文 (150+字，深度解析)
l1_sentences = [
    {"id": "s1", "audio": "最近、多くの企業でリモートワークが導入され、働き方が一変した。",
     "jp": "<span class='pos-noun'>最近</span>、多くの<span class='pos-noun'>企業</span>でリモートワークが導入され、働き方が<span class='pos-verb'>一変した</span>。",
     "html": "<b>【翻訳】</b>最近，许多企业引入了远程办公，工作方式发生了巨变。<br><br><b>【教辅级解析】</b><br>🔹 <b>～が導入される</b>：被动语态。N2阅读极爱考察被动，客观描述社会现象。<br>🔹 <b>一変（いっぺん）した</b>：名词+する。表示状态发生彻底改变。"},
    {"id": "s2", "audio": "それに伴い、自宅での仕事がとても捗ると感じる人がいる一方で、対面でのコミュニケーションの不足から、業務を適切に割り当てることが難しくなったという声も頻繁に聞かれる。",
     "jp": "<span class='pos-conj'>それに伴い</span>、自宅での仕事が<span class='pos-adv'>とても</span><span class='pos-verb'>捗る</span>と感じる人がいる<span class='pos-conj'>一方で</span>、対面でのコミュニケーションの不足から、業務を適切に<span class='pos-verb'>割り当てる</span>ことが難しくなったという声も<span class='pos-adv'>頻繁に</span>聞かれる。",
     "html": "<b>【翻訳】</b>伴随于此，一方面有人觉得在家的工作进展非常顺利，另一方面由于缺乏面对面沟通，也有人表示难以妥善分配业务。<br><br><b>【教辅级解析】</b><br>🔹 <b>～に伴い（にともない）</b>：随着前项变化，后项也变化。<br>🔹 <b>～一方で（いっぽうで）</b>：N2核心接续！表示事物的正反两面。<br>🔹 <b>とても + 捗る</b>：本课核心词，效率极高。<br>🔹 <b>割り当てる</b>：本课核心词，分配任务。"},
    {"id": "s3", "audio": "また、自宅に仕事用のデスクや高性能なパソコンを備え付けるための費用も、無視できない課題となっている。",
     "jp": "<span class='pos-conj'>また</span>、自宅に仕事用のデスクや高性能なパソコンを<span class='pos-verb'>備え付ける</span><span class='pos-conj'>ための</span>費用も、無視できない課題となっている。",
     "html": "<b>【翻訳】</b>此外，为了在家里配备办公桌和电脑的费用，也成了一个不可忽视的课题。<br><br><b>【教辅级解析】</b><br>🔹 <b>備え付ける（そなえつける）</b>：动词，安装、配备（固定设施）。<br>🔹 <b>ための</b>：接动词原形后，修饰名词“費用”，表示目的。"},
    {"id": "s4", "audio": "しかし、環境の変化にただ嘆くのではなく、決して妥協せずに、オンラインでこまめに打ち合わせることで、新しい働き方の兆しが必ず見えてくるだろう。",
     "jp": "<span class='pos-conj'>しかし</span>、環境の変化にただ嘆くのではなく、<span class='pos-adv'>決して</span><span class='pos-verb'>妥協</span>せずに、オンラインで<span class='pos-adv'>こまめに</span><span class='pos-verb'>打ち合わせる</span>ことで、新しい働き方の<span class='pos-noun'>兆し</span>が必ず見えてくるだろう。",
     "html": "<b>【翻訳】</b>然而，不要仅仅哀叹变化，只要绝不妥协，在线上勤加商量，就一定会看到新工作方式的曙光。<br><br><b>【教辅级解析】</b><br>🔹 <b>決して～ない</b>：N2副词呼应。“绝不...”。<br>🔹 <b>こまめに</b>：频繁地、勤加（高频词）。<br>🔹 <b>兆し（きざし）</b>：本课核心词，前兆、曙光。"},
    {"id": "s5", "audio": "古い慣習が徐々に廃れるのは時代の必然的な流れであり、私たちは互いに足りない部分を補う努力を怠ってはならない。",
     "jp": "古い<span class='pos-noun'>慣習</span>が<span class='pos-adv'>徐々に</span><span class='pos-verb'>廃れる</span>のは時代の必然的な流れであり、<span class='pos-pron'>私たち</span>は互いに足りない部分を<span class='pos-verb'>補う</span>努力を怠ってはならない。",
     "html": "<b>【翻訳】</b>旧习惯的衰落是时代必然趋势，我们绝不能懈怠去努力弥补不足。<br><br><b>【教辅级解析】</b><br>🔹 <b>廃れる（すたれる）/ 補う（おぎなう）</b>：本课核心动词，衰落 / 弥补。<br>🔹 <b>～てはならない</b>：N2强烈禁止语法，“绝不能...”。"}
]

# 课时 2 N2 阅读长文
l2_sentences = [
    {"id": "s1", "audio": "若手社員の中には、自分が会社の中心であると錯覚している者が少なくない。",
     "jp": "若手社員の中には、<span class='pos-pron'>自分</span>が会社の中心であると<span class='pos-verb'>錯覚している</span>者が少なくない。",
     "html": "<b>【翻訳】</b>在年轻员工中，有不少人错觉自己是公司的核心。<br><br><b>【教辅级解析】</b><br>🔹 <b>錯覚（さっかく）している</b>：产生错觉。"},
    {"id": "s2", "audio": "彼らは、上司から少しでも指図されると、すぐに不満を顔に出す。",
     "jp": "<span class='pos-pron'>彼ら</span>は、上司から<span class='pos-adv'>少しでも</span><span class='pos-verb'>指図される</span>と、すぐに不満を顔に出す。",
     "html": "<b>【翻訳】</b>他们只要被上司稍微指示一下，就会立刻把不满写在脸上。<br><br><b>【教辅级解析】</b><br>🔹 <b>指図（さしず）される</b>：被指示、被命令。带消极色彩。"},
    {"id": "s3", "audio": "しかし、組織の中で働く以上、周囲の空気を察知し、自覚を持って行動することが求められる。",
     "jp": "<span class='pos-conj'>しかし</span>、組織の中で働く<span class='pos-conj'>以上</span>、周囲の空気を<span class='pos-verb'>察知し</span>、<span class='pos-noun'>自覚</span>を持って行動することが求められる。",
     "html": "<b>【翻訳】</b>但是，既然在组织中工作，就被要求要能察觉周围的气氛，并带着自觉性去行动。<br><br><b>【教辅级解析】</b><br>🔹 <b>～以上（いじょう）</b>：N2语法。既然...就必须...。<br>🔹 <b>察知（さっち） / 自覚（じかく）</b>：本课核心词。"}
]

sprint_30_data = [
    ("合致", "がっち", "一致"), ("兆し", "きざし", "前兆"), ("素朴", "そぼく", "纯朴"), ("妥協", "だきょう", "妥协"), ("漠然", "ばくぜん", "模糊"),
    ("閲覧", "えつらん", "阅读"), ("一転", "いってん", "突然改变"), ("安堵", "あんど", "放心"), ("会得", "えとく", "领会"), ("概説", "がいせつ", "概论"),
    ("該当", "がいとう", "符合"), ("介入", "かいにゅう", "干预"), ("各界", "かくかい", "各界"), ("拡充", "かくじゅう", "扩充"), ("確保", "かくほ", "确保")
] # 篇幅限制，展示前15个作为冲刺包

# ==========================================
# 侧边栏与导航
# ==========================================
st.sidebar.title("🏮 N2 冲刺系统")
selected_lesson = st.sidebar.radio("📚 选择课时", ["Day 1 - 第1课时 (基础)", "Day 1 - 第2课时 (进阶)"])
st.sidebar.markdown("---")

col1, col2, col3 = st.columns([1, 8, 1])
with col2:
    st.markdown(f"<h2 style='text-align: center; color: #e6edf3;'>{selected_lesson}</h2>", unsafe_allow_html=True)
    st.markdown("---")

# ==========================================
# 渲染页面 (Tabs)
# ==========================================
with st.container():
    c_left, c_mid, c_right = st.columns([1, 15, 1])
    with c_mid:
        
        # 针对第二课，增加课前复习游戏 Tab
        if "第2课时" in selected_lesson:
            tabs = st.tabs(["🎮 课前复习(Day1)", "📖 核心词精讲", "📝 聚光灯阅读", "🚀 30词冲刺"])
            tab_game, tab_core, tab_reading, tab_sprint = tabs[0], tabs[1], tabs[2], tabs[3]
            
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
                components.html(html_game, height=400)
        else:
            tabs = st.tabs(["📖 核心词精讲", "📝 聚光灯阅读", "🚀 30词冲刺"])
            tab_core, tab_reading, tab_sprint = tabs[0], tabs[1], tabs[2]

        # ------------------------------------------
        # 核心词解剖 (PPT 分页模式)
        # ------------------------------------------
        with tab_core:
            st.info("💡 提示：为了保护视力和专注度，已开启【PPT分页模式】。每次只学 3 个词，深度掌握多重用法。")
            ppt_page = st.radio("选择讲义页码：", ["📜 第1页 (词1-3)", "📜 第2页 (词4-6)"], horizontal=True, label_visibility="collapsed")
            
            current_words = l1_words if "第1课时" in selected_lesson else l2_words
            display_words = current_words[0:3] if "第1页" in ppt_page else current_words[3:6]
            
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
                            <div class="hidden-tr">🇨🇳 {u['tr']}</div>
                        </div>
                    """
                mindmap_html += "</div></div>"
            mindmap_html += "</div>"
            components.html(mindmap_html, height=850, scrolling=True)

        # ------------------------------------------
        # N2 阅读解剖 (终极不跳动聚光灯)
        # ------------------------------------------
        with tab_reading:
            current_sentences = l1_sentences if "第1课时" in selected_lesson else l2_sentences
            
            hidden_data_html = ""
            for s in current_sentences:
                hidden_data_html += f"<div id='data_{s['id']}' style='display:none;'>{s['html']}</div>"
            
            essay_html = common_head + hidden_data_html + f"""
            <div class="legend-box">
                <div class="legend-title">🧩 N2 色彩罗盘</div>
                <div class="legend-item"><div class="color-block" style="background:#ff7b72;"></div> 动词 (Verb)</div>
                <div class="legend-item"><div class="color-block" style="background:#79c0ff;"></div> 副词 (Adv)</div>
                <div class="legend-item"><div class="color-block" style="background:#d2a8ff;"></div> 接续词 (Conj)</div>
                <div class="legend-item"><div class="color-block" style="background:#2ea043;"></div> 代词 (Pron)</div>
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

        # ------------------------------------------
        # 课后 30 词
        # ------------------------------------------
        with tab_sprint:
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
