# 由 11/15 雲林「玩轉世代」簡報（../intergen-ai-play/deck.html）改成
# 線上預錄 60 分鐘「不知道帶個案玩什麼？讓 AI 想點子做出好玩活動」（長照居家陪伴，只用 ChatGPT、Gemini）
# python3 make_deck.py → deck.html；zsh build.sh → index.html
import re, html, pathlib
ROOT = pathlib.Path(__file__).parent
SRC = (ROOT.parent / "intergen-ai-play" / "deck.html").read_text()
GH = "https://mattsue1003.github.io/"
DECK_URL = GH + "ai-activity-homecare/"
esc = html.escape

first = SRC.index('<!-- 1 封面 -->') if '<!-- 1 封面 -->' in SRC else SRC.index('<section')
head = SRC[:first]
last = SRC.rindex('</section>') + len('</section>')
tail = SRC[last:]
old = {m.group(1): m.group(0) for m in re.finditer(r'<section class="slide[^"]*"[^>]*data-title="([^"]+)".*?</section>', SRC, re.S)}

def keep(title, *subs, new_title=None):
    s = old[title]
    for a, b in subs:
        assert a in s, (title, a[:50])
        s = s.replace(a, b)
    if new_title:
        s = s.replace(f'data-title="{esc(title)}"', f'data-title="{esc(new_title)}"', 1)
    return s + "\n"

css = """
/* ── 居家陪伴版新增 ── */
.pain{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:20px;flex:1;min-height:0;max-height:520px}
.pain .box{justify-content:flex-start;padding:22px;border-top:6px solid var(--c);gap:10px}
.pain .q{font-size:24px;font-weight:900;line-height:1.45;color:var(--ink)}
.pain .a{margin-top:auto;font-size:16px;color:var(--muted);line-height:1.55;border-top:1px dashed var(--line);padding-top:10px}
.pain .a b{color:var(--c)}
.learn{display:flex;flex-wrap:wrap;gap:10px}
.learn span{border:1.5px solid var(--ink);border-radius:999px;padding:6px 14px;font-weight:700;font-size:15px}
.can{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px}
.can .box{justify-content:flex-start;padding:18px;border-top:6px solid var(--c)}
.can h3{font-size:22px;color:var(--c)}.can p{font-size:16px;line-height:1.55}
.can .eg{font-size:14px;color:var(--muted);border-top:1px dashed var(--line);padding-top:8px;margin-top:auto}
.two{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:22px;flex:1;min-height:0;max-height:560px}
.two .box{justify-content:flex-start;padding:20px;border-top:6px solid var(--c);gap:10px}
.two h3{font-size:26px;color:var(--c)}.two .sub{font-size:14px;color:var(--muted)}
.ol{margin:0;padding-left:1.3em;display:flex;flex-direction:column;gap:7px;font-size:16.5px;line-height:1.55}
.formula{display:grid;grid-template-columns:repeat(5,minmax(0,1fr));gap:10px}
.formula div{border-radius:12px;padding:12px 14px;background:color-mix(in srgb,var(--c) 12%,var(--paper));border:1.5px solid color-mix(in srgb,var(--c) 45%,var(--paper))}
.formula b{display:block;font-size:20px;color:var(--c)}.formula small{display:block;font-size:14px;line-height:1.45;color:var(--ink)}
.bad{border:2px dashed var(--line);border-radius:12px;padding:12px 16px;font-size:16px;line-height:1.6;color:var(--muted)}
.bad b{color:var(--mag)}
.adj{width:100%;border-collapse:collapse}.adj th,.adj td{border-bottom:1px solid var(--line);padding:9px 10px;text-align:left;font-size:16px;line-height:1.5;vertical-align:top}
.adj th{font-size:14px;color:var(--muted)}.adj td:first-child{font-weight:900;white-space:nowrap;color:var(--c,var(--ink))}
.case .box{justify-content:flex-start;gap:8px;padding:18px}
.case h3{font-size:19px}.case .who{font-size:17px;line-height:1.6}
.case .res{counter-reset:r;list-style:none;margin:0;padding:0;display:flex;flex-direction:column;gap:8px}
.case .res li{display:grid;grid-template-columns:26px 1fr;gap:10px;font-size:16px;line-height:1.5}
.case .res li::before{counter-increment:r;content:counter(r);width:26px;height:26px;border-radius:7px;background:var(--c);color:#fff;display:grid;place-items:center;font-weight:900;font-size:13px;margin-top:1px}
.case .tagline{font-size:13px;color:var(--muted)}
.noterow{display:grid;grid-template-columns:repeat(var(--k),minmax(0,1fr));gap:14px}
a.go{color:var(--blue);font-weight:700;text-decoration:underline;text-underline-offset:3px;white-space:nowrap}a.go:hover{color:var(--ink)}
.wsrow{display:grid;grid-template-columns:repeat(4,minmax(0,1fr));gap:16px;flex:1;min-height:0}
.wsc{margin:0;display:flex;flex-direction:column;gap:6px;min-height:0;border:1px solid var(--line);border-top:5px solid var(--c);border-radius:10px;padding:8px;background:var(--paper)}
.wsc>a{flex:1;min-height:0;display:block;background:#fff;border-radius:6px;overflow:hidden}
.wsc img{width:100%;height:100%;object-fit:contain;display:block}
.wsc figcaption{display:flex;align-items:center;gap:8px;font-size:15px}.wsc figcaption b{font-size:17px}
.wsc .tool{font-size:12.5px;color:var(--c);font-weight:700}.wsc figcaption .go{margin-left:auto;font-size:13px}
.adj.ch td{font-size:14px;padding:5px 8px}.adj.ch td:first-child{color:var(--blue)}
.case .note{flex:none!important}.case .cols>div>.box{flex:1}
.pain{max-height:430px}
@media (max-width:900px){.noterow,.pain,.can,.two,.formula{grid-template-columns:minmax(0,1fr);max-height:none}}
"""
head = head.replace("</style>", css + "</style>", 1)
head = re.sub(r"<title>[^<]*</title>", "<title>讓 AI 想點子做出好玩活動｜長照居家陪伴</title>", head, count=1)
head = head.replace('<b>PLAY × AI</b><span>玩轉世代：AI 賦能幼老代間遊戲與創意教學設計</span>',
                    '<b>AI × 陪伴</b><span>不知道帶個案玩什麼？讓 AI 想點子做出好玩活動</span>')
assert 'AI × 陪伴' in head
tail = tail.replace("intergenai-", "aiact-")
tail = re.sub(r'<a class="cta g" href="https://line\.me[^"]*"[^>]*>LINE 社群</a>', '', tail)
assert 'line.me' not in tail

def ex(slug, title, desc):
    return (f'<a class="ex" href="{GH}{slug}/" target="_blank" rel="noopener"><div class="ph"><img src="img/ex/{slug}.jpg" alt="{esc(title)} 畫面" loading="lazy"></div>'
            f'<div class="row"><span><b>{esc(title)}</b><small>{esc(desc)}</small></span><img class="q" src="img/qr/{slug}.svg" alt="{esc(title)} QR code"></div></a>')
def exs(items, m=3):
    return f'<div class="exgrid" style="--m:{m}">' + "".join(ex(*i) for i in items) + "</div>"
def A(url, text):
    return f'<a class="go" href="{url}" target="_blank" rel="noopener">{text} ↗</a>'
def stepper(eyebrow_c, eyebrow, title, h2, steps, right_extra, frame_bg=""):
    lis = "".join(f'<li data-img="{img}" data-cap="{esc(cap)}"><span class="n">{i+1}</span><div><b>{b}</b><p>{p}</p></div></li>' for i, (img, cap, b, p) in enumerate(steps))
    return f'''<section class="slide" data-title="{esc(title)}">
  <div class="eyebrow" style="--c:{eyebrow_c}"><span class="sq"></span>{eyebrow}</div>
  <h2>{h2}</h2>
  <div class="stepper" data-stepper>
    <ol class="steps">{lis}</ol>
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <figure class="shot" style="flex:1"><div class="stepbar"></div><div class="frame"{frame_bg}><img alt=""></div><figcaption><span class="cap"></span><span class="hint">↓ 下一步</span></figcaption></figure>
      {right_extra}
    </div>
  </div>
</section>
'''

def prompt(lab, text):
    return f'<div class="prompt"><div class="lab">{lab}<button class="copy">複製</button></div>{text}</div>'

S = []

# 1 封面
S.append(f'''<!-- 1 封面 -->
<section class="slide cover" data-title="封面">
  <div class="confetti" aria-hidden="true">
    <i style="left:62%;top:7%;width:46px;height:46px;background:var(--blue)"></i>
    <i style="left:76%;top:12%;width:20px;height:20px;background:var(--lime);animation-delay:-2s"></i>
    <i style="left:92%;top:8%;width:30px;height:30px;background:var(--mag);animation-delay:-1s"></i>
    <i style="left:58%;top:52%;width:16px;height:16px;background:var(--mag);animation-delay:-2.5s"></i>
    <i style="left:62%;top:84%;width:56px;height:56px;background:var(--amber);animation-delay:-3s"></i>
    <i style="left:91%;top:84%;width:34px;height:34px;background:var(--sky);animation-delay:-1.5s"></i>
  </div>
  <div class="cover-grid">
  <div class="cover-main">
  <div class="eyebrow"><span class="sq"></span>長照居家陪伴　線上課程</div>
  <h1><span class="en">AI <b>×</b> 陪伴</span>不知道帶個案玩什麼？</h1>
  <p class="lede" style="font-size:26px;color:var(--ink);font-weight:900">讓 AI 想點子，做出好玩活動</p>
  <p class="lede">陪伴服務不只看電視、聊聊天。用 ChatGPT、Gemini 想點子、依個案狀況調整玩法、做出大字牌卡和小遊戲，三個案例一步一步帶你做。</p>
  <div class="meta">
    <div><small>課程長度</small><strong>60 分鐘</strong></div>
    <div><small>使用工具</small><strong>ChatGPT、Gemini</strong></div>
    <div><small>適合對象</small><strong>居服員、陪伴員、家屬</strong></div>
    <div><small>講師</small><strong>鍾孟修 職能治療師</strong></div>
  </div>
  </div>
  <div class="coverqrs">
  <div class="coverqr"><img src="img/qr-deck.svg" alt="掃描開啟本網頁型簡報"><span><b>帶走簡報</b>mattsue1003.github.io/ai-activity-homecare</span></div>
  </div>
  </div>
</section>
''')

S.append(keep("講師介紹"))

# 3 你是不是也遇過
S.append('''<!-- 痛點 -->
<section class="slide" data-title="你是不是也遇過？">
  <div class="eyebrow" style="--c:var(--mag)"><span class="sq"></span>先想一想</div>
  <h2>你是不是也遇過這三種狀況？</h2>
  <div class="pain">
    <div class="box" style="--c:var(--blue)"><div class="q">「陪伴服務不知道要做什麼，只能陪著看電視、聊聊天。」</div><div class="a"><b>今天的答案</b>：請 AI 依他的興趣和年代想點子，看電視也能變成聊天和小遊戲。<br>→ 案例②</div></div>
    <div class="box" style="--c:var(--amber)"><div class="q">「每次都玩那幾種，個案玩到好無聊，不想參加。」</div><div class="a"><b>今天的答案</b>：同一個題目換玩法，用 Gemini 做一個只屬於他的小遊戲。<br>→ 案例③</div></div>
    <div class="box" style="--c:var(--green)"><div class="q">「買了撲克牌，但個案說看不到，沒辦法一起玩。」</div><div class="a"><b>今天的答案</b>：把個案的狀況告訴 AI，請它改玩法、做大字牌卡。<br>→ 案例①</div></div>
  </div>
  <div class="note" style="--c:var(--mag)"><b>今天的原則</b><span>AI 負責<b>想點子、做道具</b>；你負責<b>認識個案、把關安全</b>。最懂個案的人是你。</span></div>
</section>
''')

S.append("@@AGENDA@@")

S.append(keep("先玩一下：猜歌、好味島、馬賽克",
    ("先玩一下　掃 QR 或看大螢幕一起猜", "先玩一下　暫停影片，手機掃 QR 玩一題"),
    ("<h2>先當學員玩三題：老歌、家鄉味、馬賽克景點</h2>", "<h2>先當個案玩一題：老歌、家鄉味、馬賽克景點</h2>"),
    ("聽前奏猜歌名：選一個年代，祖孫一起搶答", "聽前奏猜歌名：選他年輕時的年代，一起哼"),
    ("等一下就教大家怎麼用 AI 做出來。", "這三個都是用 AI 做的，帶到個案家裡，用手機或平板就能玩。")))

# 6 認識 AI 活動設計
S.append('''<!-- AI 能幫什麼 -->
<section class="slide" data-title="認識 AI 活動設計：AI 能幫你做的四件事">
  <div class="eyebrow" style="--c:var(--blue)"><span class="sq"></span>第一段　認識 AI 活動設計</div>
  <h2>AI 是你的活動小幫手：它能幫你做四件事</h2>
  <div class="can">
    <div class="box" style="--c:var(--blue)"><h3>① 想點子</h3><p>告訴它個案喜歡什麼、家裡有什麼，30 秒給你 10 個活動。</p><p class="eg">例：家裡只有撲克牌、報紙、寶特瓶，能玩什麼？</p></div>
    <div class="box" style="--c:var(--amber)"><h3>② 依個案調整</h3><p>看不清楚、手會抖、記憶不好、坐輪椅，請它改成做得到的玩法。</p><p class="eg">例：把這個遊戲改成視力不好也能玩。</p></div>
    <div class="box" style="--c:var(--green)"><h3>③ 做道具</h3><p>大字牌卡、題目卡、學習單、聊天題卡，印出來就能用。</p><p class="eg">例：做 A4 大字數字卡，每頁 4 張。</p></div>
    <div class="box" style="--c:var(--mag)"><h3>④ 做小遊戲</h3><p>用平板、手機玩的搶答、配對、猜謎，題目換成他熟悉的。</p><p class="eg">例：做一個猜台灣小吃的搶答遊戲。</p></div>
  </div>
  <div class="noterow" style="--k:2">
    <div class="note" style="--c:var(--blue)"><b>AI 不知道的事</b><span>個案今天精神好不好、吞嚥和跌倒風險、家人的期待。這些要你判斷。</span></div>
    <div class="note" style="--c:var(--mag)"><b>保護個資</b><span>不要輸入個案姓名、地址、照片、病歷號，寫「82 歲阿嬤、視力不好」就夠了。</span></div>
  </div>
</section>
''')

# 7 ChatGPT vs Gemini
S.append('''<!-- 工具 -->
<section class="slide" data-title="ChatGPT 和 Gemini 怎麼選">
  <div class="eyebrow" style="--c:var(--ink)"><span class="sq"></span>今天只用兩個工具</div>
  <h2>ChatGPT 和 Gemini：免費版就能用，各有拿手的事</h2>
  <div class="two">
    <div class="box" style="--c:#10A37F"><h3>ChatGPT</h3><span class="sub">chatgpt.com・手機 App「ChatGPT」</span>
      <ul class="bio" style="font-size:17px;gap:8px"><li><b>想點子、改玩法</b>：講話很像在跟同事討論</li><li><b>做圖</b>：大字牌卡、海報、學習單</li><li><b>出檔案</b>：Word、PDF 直接下載列印</li></ul>
      <p class="ai3-today" style="margin-top:auto"><b>今天做</b>案例①：撲克牌改玩法＋大字牌卡</p></div>
    <div class="box" style="--c:var(--blue)"><h3>Gemini</h3><span class="sub">gemini.google.com・手機 App「Gemini」</span>
      <ul class="bio" style="font-size:17px;gap:8px"><li><b>看得懂 YouTube</b>：老歌、影片整理成聊天題目</li><li><b>Canvas 做小遊戲</b>：講清楚玩法，做出能點的遊戲</li><li><b>用 Google 帳號就能登入</b></li></ul>
      <p class="ai3-today" style="margin-top:auto"><b>今天做</b>案例②：老歌聊天；案例③：專屬小遊戲</p></div>
  </div>
  <div class="note" style="--c:var(--amber)"><b>兩個都會出錯</b><span>規則、數字、健康說法，帶活動前自己玩一次、看一次。哪一個回答不好，就換另一個問。</span></div>
</section>
''')

# 8 基本操作① 打開與登入
S.append('''<!-- 基本操作① -->
<section class="slide" data-title="基本操作① 打開、登入、開新對話">
  <div class="eyebrow" style="--c:var(--blue)"><span class="sq"></span>第二段　基本操作①</div>
  <h2>打開、登入、開新對話：三分鐘就能開始</h2>
  <div class="two">
    <div class="box" style="--c:#10A37F"><h3>ChatGPT</h3>
      <ol class="ol"><li>電腦打開 <b>chatgpt.com</b>；手機下載「ChatGPT」App</li><li>按「登入」，用 Google 帳號或 Email 登入</li><li>左上角「新聊天」：每個活動開一個新對話</li><li>下方輸入框打字，按 Enter 或↑送出</li><li>左邊清單是以前的對話，可以回頭找</li></ol></div>
    <div class="box" style="--c:var(--blue)"><h3>Gemini</h3>
      <ol class="ol"><li>電腦打開 <b>gemini.google.com</b>；手機下載「Gemini」App</li><li>用 Google 帳號登入（有 Gmail 就有）</li><li>左上角「發起新對話」</li><li>輸入框旁的「+」可以上傳照片、檔案</li><li>做小遊戲時，在工具裡選「Canvas」</li></ol></div>
  </div>
  <div class="noterow" style="--k:3">
    <div class="note" style="--c:var(--blue)"><b>一個活動一個對話</b><span>不同個案分開問，答案才不會混在一起。</span></div>
    <div class="note" style="--c:var(--amber)"><b>不滿意就追問</b><span>「再簡單一點」「換成不用道具」，不用重打。</span></div>
    <div class="note" style="--c:var(--green)"><b>免費版就夠</b><span>今天的三個案例，免費帳號都做得到。</span></div>
  </div>
</section>
''')

S.append(keep("實作① 不用安裝：ChatGPT、Gemini 的麥克風",
    ("實作①　用說的：不用安裝", "第二段　基本操作②　用說的"),
    ("<h2>沒有 Typeless？ChatGPT、Gemini 的麥克風就能語音轉文字</h2>", "<h2>不想打字？按麥克風，用說的就好</h2>"),
    ("最接近 Typeless 的用法。", "在個案家門口、在車上想到點子，講完就送出。"),
    new_title="基本操作② 按麥克風用說的"))
S.append(keep("語音轉文字設定成繁體中文",
    ("實作①　避免出現簡體字", "基本操作②　避免出現簡體字"),
    ('<b>手機</b><span>iPhone、Android 的鍵盤加「注音」，按注音鍵盤上的麥克風說話，轉出來就是繁體。已經出現簡體：說「請把上面轉成繁體中文，內容不要改」。</span>',
     '<b>兩個小撇步</b><span><b>① 手機用說的：</b>手機的「設定」裡加一個「注音」鍵盤，要輸入時切換到注音鍵盤，按鍵盤上的麥克風說話，打出來的字就是繁體中文。<br><b>② AI 回答變成簡體字：</b>直接再打一句「請把上面轉成繁體中文，內容不要改」，它就會改回來。</span>')))

# 11 好指令公式
S.append(f'''<!-- 好指令 -->
<section class="slide" data-title="基本操作③ 好指令五要素">
  <div class="eyebrow" style="--c:var(--amber)"><span class="sq"></span>基本操作③　有效指令</div>
  <h2>好指令五要素：把個案說清楚，AI 才想得準</h2>
  <div class="formula">
    <div style="--c:var(--blue)"><b>① 個案是誰</b><small>年齡、能力、喜歡什麼（不寫姓名）</small></div>
    <div style="--c:var(--amber)"><b>② 有什麼道具</b><small>撲克牌、報紙、手機、家裡現有的東西</small></div>
    <div style="--c:var(--green)"><b>③ 時間場地</b><small>一對一、30 分鐘、在客廳坐著</small></div>
    <div style="--c:var(--mag)"><b>④ 限制</b><small>看不清楚、手會抖、不能久站</small></div>
    <div style="--c:var(--ink)"><b>⑤ 要什麼格式</b><small>3 個玩法、步驟、變簡單變難、帶領說法</small></div>
  </div>
  <div class="cols" style="--n:2;gap:18px">
    <div style="display:flex;flex-direction:column;gap:10px;min-width:0">
      <div class="bad"><b>不夠清楚</b>　「給我一些老人活動。」<br>→ AI 只能給你很普通的答案：唱歌、做操、畫畫。</div>
      <div class="note" style="--c:var(--amber)"><b>追問三句</b><span>「再簡單一點」「改成不用道具」「把帶領時要說的話寫出來」。</span></div>
      <div class="note" style="--c:var(--blue)"><b>不知道怎麼寫</b><span>最後加一句：「開始前，先問我 5 個你需要知道的問題。」</span></div>
    </div>
    {prompt("清楚的指令（五要素都有）", "我是居家服務員，個案是 82 歲的阿嬤，以前在市場賣菜，喜歡聽台語老歌。她的視力不太好、手有點抖，可以坐著 30 分鐘。家裡有撲克牌、報紙和一台手機。請幫我設計 3 個一對一的活動，每個寫：玩法步驟、變簡單和變難的方法、帶領時可以說的一句話。用繁體中文。")}
  </div>
</section>
''')

# 12 能力階梯
S.append('''<!-- 原則：能力階梯 -->
<section class="slide" data-title="好玩的原則① 從他做得到的那一層開始">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>第三段　好玩的原則①</div>
  <h2>從他「做得到」的那一層開始，再往上一層</h2>
  <div class="dev">
    <div class="ladder" style="--c:var(--sky)">
      <p class="muted" style="font-weight:700">遊戲能力的階梯（能力退化時，會由上往下退）</p>
      <div style="--c:var(--mag)"><i>4</i><span><b>自主、複雜規則</b><small>策略、計分、輪流出題。能力好的個案，可以請他當出題的人</small></span></div>
      <div class="mid" style="--c:var(--amber)"><i>3</i><span><b>簡單規則</b><small>一句話講得完的規則：「湊到 10 就拿走」</small></span></div>
      <div class="mid" style="--c:var(--green)"><i>2</i><span><b>配對、分類</b><small>找一樣的、分顏色、排大小。失智或剛開始的個案從這裡</small></span></div>
      <div style="--c:var(--blue)"><i>1</i><span><b>感覺、動作</b><small>摸、拍、丟、握。臥床或很累的時候也能玩</small></span></div>
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <div class="box"><h3 style="color:var(--green)">一對一陪伴怎麼用</h3>
        <ul class="bio" style="margin-top:8px;font-size:16px;gap:8px">
          <li><b>先觀察</b>：他現在在哪一層？會配對嗎？聽得懂一句話的規則嗎？</li>
          <li><b>暖身放低一層</b>：先成功，才會想玩下去</li>
          <li><b>挑戰只加一點</b>：牌多 2 張、多一個步驟就好</li>
          <li><b>請他當老師</b>：他拿手的事（煮菜、種田、唱歌）請他教你</li>
        </ul></div>
      <div class="note" style="--c:var(--green)"><b>跟 AI 說</b><span>「他會配對，但兩個步驟的規則會忘記」——AI 就知道要設計在第 2、3 層。</span></div>
    </div>
  </div>
</section>
''')

def mech(color, name, how, easy, hard, say, ig):
    return f'<div class="box" style="--c:{color}"><h3>{name}</h3><p><b>做法</b>　{how}</p><p><b>變簡單</b>　{easy}</p><p><b>變難</b>　{hard}</p><p class="ig"><b>陪伴時</b>　{ig}</p><p class="say">「{say}」</p></div>'

S.append(f'''<!-- 原則：撲克四大機制 -->
<section class="slide" data-title="好玩的原則② 一副撲克牌四種玩法">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>第三段　好玩的原則②　一副撲克牌</div>
  <h2>一副撲克牌，四種動腦方式：配對、組合、排序、線索</h2>
  <div class="mech">
    {mech("var(--mag)","配對","翻開 6 張，找數字一樣的兩張湊一對。","只分紅色、黑色。","牌蓋著翻，記位置找一對。","這張 5 的好朋友在哪裡？","你出一張，請他找一樣的；再交換。")}
    {mech("var(--amber)","組合","兩張加起來等於 10（A 當 1，人頭牌先拿掉）。","只用 A–5，湊 6。","三張湊 15。","7 要配哪一張才是 10？","以前做生意的個案，請他當算帳的老闆。")}
    {mech("var(--blue)","排序","同一花色 A–10 打亂，從小排到大。","只用 A–5。","抽掉一張，問少了哪一張。","幫我排好，我老是亂掉。","請他幫你的忙，比「考他」更願意做。")}
    {mech("var(--green)","線索","你心裡想一張牌，他用是非題問：「紅色嗎？比 5 大嗎？」","桌上只留 4 張讓他猜。","換他想、你來問。","我心裡想一張，你問我。","最後一題讓他贏，帶著成功結束。")}
  </div>
  <div class="note" style="--c:var(--green)"><b>帶法</b><span>不說「我們來上課」，說「陪我玩一下牌」｜一次 5–10 分鐘｜答錯不糾正，陪他再找一次。</span></div>
</section>
''')

# 14 依狀況調整
S.append(f'''<!-- 原則：依狀況調整 -->
<section class="slide" data-title="好玩的原則③ 依個案狀況調整">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>第三段　好玩的原則③</div>
  <h2>同一個遊戲，依個案狀況調整，人人都能玩</h2>
  <div class="cols" style="--n:2;grid-template-columns:minmax(0,7fr) minmax(0,4fr);gap:20px">
    <div class="tbl"><table class="adj">
      <tr><th>個案狀況</th><th>可以這樣改</th></tr>
      <tr><td style="--c:var(--blue)">視力不好</td><td>放大字、深色底配亮色字、牌少一點；改用摸的、聽的</td></tr>
      <tr><td style="--c:var(--amber)">手會抖、握力差</td><td>牌卡做大做厚、放在止滑墊上；用指的、用說的代替拿</td></tr>
      <tr><td style="--c:var(--mag)">記憶不好、失智</td><td>規則一句話、每次示範一次；題目用他年輕時的事</td></tr>
      <tr><td style="--c:var(--green)">聽力不好</td><td>面對面、慢慢說；題目寫在紙上或平板上</td></tr>
      <tr><td style="--c:var(--sky)">臥床、坐輪椅</td><td>道具放在胸前高度；加一點手部、上半身的動作</td></tr>
      <tr><td style="--c:var(--ink)">沒興趣、不想玩</td><td>從他的工作、家鄉、拿手菜開始聊；請他教你</td></tr>
    </table></div>
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      {prompt("指令・依狀況改玩法", "這是一個（撲克牌配對）遊戲。我的個案（視力不好，看不清楚小字；手有點抖）。請幫我改成他做得到的版本：道具怎麼改、規則怎麼改、我要怎麼示範。再給一個更簡單的版本，給他狀況不好的時候用。")}
      <div class="note" style="--c:var(--green)"><b>小技巧</b><span>先寫「他做得到什麼」，再寫「他做不到什麼」，AI 比較不會把活動改得太簡單。</span></div>
    </div>
  </div>
</section>
''')

def case(no, color, title, h2, tool, who, ptext, results, how, plab="指令"):
    res = "".join(f"<li><span>{r}</span></li>" for r in results)
    return f'''<section class="slide case" data-title="{esc(title)}" style="--c:{color}">
  <div class="eyebrow" style="--c:{color}"><span class="sq"></span>第四段　案例{no}　{tool}</div>
  <h2>{h2}</h2>
  <div class="cols" style="--n:2;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:20px">
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <div class="box"><h3 style="color:{color}">情境</h3><p class="who">{who}</p></div>
      {prompt(plab, ptext)}
    </div>
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <div class="box" style="flex:1"><h3>AI 給的點子（回答重點整理）</h3><ol class="res">{res}</ol><p class="tagline">每次回答都會不一樣；挑適合的，不適合就追問。</p></div>
      <div class="note" style="--c:{color}"><b>帶的時候</b><span>{how}</span></div>
    </div>
  </div>
</section>
'''

# 案例①
S.append(case("①", "var(--green)", "案例① 撲克牌×視力不好的阿嬤", "案例①：買了撲克牌，阿嬤說看不到，怎麼辦？", "ChatGPT",
    "阿嬤 82 歲，以前在市場賣菜，算錢很快。白內障開過刀，<b>小字看不清楚</b>，手有點抖。服務時間 1 小時，她常說「我看不到，不要玩」。",
    "我是居家服務員。個案是 82 歲阿嬤，以前在市場賣菜、很會算錢；視力不好，撲克牌上的小字看不清楚，手有點抖。我有一副撲克牌、一張深色桌墊。請幫我：1. 設計 3 個她看得到、拿得起來的撲克牌遊戲，每個 5–10 分鐘；2. 每個寫道具怎麼改、玩法步驟、變簡單和變難；3. 寫出邀請她玩的第一句話，讓她不覺得在考試。",
    ["<b>大字湊 10</b>：只用 A–9，牌放在深色桌墊上，一次翻 4 張，請阿嬤「當老闆找零錢」湊 10。",
     "<b>摸牌比大小</b>：把牌換成自製大字卡，兩人各翻一張，大的贏；看不清楚就用說的報數字。",
     "<b>紅黑分一分</b>：狀況不好時只分紅色、黑色兩堆，成功率高、手也有動到。",
     "<b>第一句話</b>：「阿嬤，我算錢算不好，妳教我一下，這兩張加起來多少？」"],
    "先玩她會成功的「紅黑分一分」，再進「湊 10」。AI 做的牌卡或學習單不滿意？下一頁教你看著圖調整。", plab="ChatGPT 指令・改玩法"))

S.append(stepper("#10A37F", "第四段　案例①　做道具：看著圖片調整", "案例① 做道具：看著圖片調整",
    "圖不滿意？在圖上畫起來，告訴 ChatGPT 要改哪裡",
    [("img/ws/gpt_edit_tools.jpg", "點一下 ChatGPT 畫好的圖：下方有標註、留言、移除背景、擦除、調整大小", "點圖片，打開編輯工具",
      "先看整張圖：哪裡太小、哪個字錯、哪樣東西個案不熟悉。"),
     ("img/ws/gpt_edit_mark.jpg", "按「標註」，用紅筆在西瓜上畫叉叉，下方打字說要改什麼（11/17 實測）", "用「標註」把要改的地方畫起來",
      "畫圈、打叉都可以；再用一句話說清楚「改成什麼、其他不要動」。"),
     ("img/ws/gpt_edit_chat.jpg", "送出後，ChatGPT 會帶著你畫的記號重新畫一張", "送出，等它重畫",
      "約 1 分鐘。原本那張還在，改壞了可以回頭用。"),
     ("img/ws/ws_matching_edit.jpg", "改好了：西瓜換成芭樂、字也改成「芭樂」，其他都沒動", "檢查改好的地方",
      "只看改的那一格對不對；其他格子有沒有被亂改。滿意就下載列印。"),
    ],
    prompt("ChatGPT 指令・看著圖調整", "把我畫紅色叉叉的西瓜換成芭樂，右邊的「西瓜」也改成「芭樂」，其他都不要動。")
    + '''
      <div class="note" style="--c:#10A37F"><b>常用的調整</b><span>「字再大一倍」「換成阿嬤熟悉的東西」「拿掉背景」「改成 A4 直式」「這一格的圖跟字對不起來，請改成一樣」。</span></div>''',
    frame_bg=' style="background:var(--soft)"'))

# 案例②
S.append(case("②", "var(--blue)", "案例② 只看電視的阿公：老歌＋懷舊聊天", "案例②：陪伴只能看電視？用老歌打開話匣子", "Gemini",
    "阿公 78 歲，以前在台中做木工，退休後每天看電視，問他什麼都說「沒什麼」。家裡有手機可以放 YouTube，喜歡<b>洪一峰、文夏</b>的歌。",
    "我是居家服務員，要陪一位 78 歲阿公 40 分鐘。他年輕時在台中做木工，喜歡洪一峰、文夏的台語老歌，平常話不多。請幫我設計一個「聽老歌、聊往事」的活動：1. 推薦 3 首他年輕時流行的歌，附上歌名和歌手；2. 每首歌設計 3 個聊天問題，從簡單（喜不喜歡）到回憶（那時候你在做什麼）；3. 最後加一個跟著拍手或打拍子的小動作。用繁體中文。",
    ["<b>暖身</b>：先放他點名的歌，問「這首你以前常聽嗎？」只要點頭就算成功。",
     "<b>聊天三層</b>：喜不喜歡 → 那時候在哪裡聽 → 那時候你在做什麼工作。",
     "<b>請他教你</b>：「木工最難的是什麼？」把話題從歌帶到他的拿手事。",
     "<b>收尾動作</b>：副歌跟著拍手或敲桌子打拍子，動一動再結束。"],
    "下兩頁實作：先收集懷舊頻道，再請 Gemini 讀一支影片。聊到難過的事，停下來陪他，不用急著回到活動。", plab="Gemini 指令・老歌聊天"))

CH = [("豪記唱片 HCM Music", "台語老歌、那卡西、伴唱帶", "HCMMUSIC"),
      ("滾石唱片 ROCK RECORDS", "70–90 年代國語老歌、民歌", "RockRecordsTaipei"),
      ("LEICO 麗歌唱片", "黑膠時期台語、國語老歌", "leicorecord9198"),
      ("TFAI 國家影視聽中心", "早期新聞片、老台灣影像、台語片", "TWCTFA"),
      ("台灣演義", "台灣歷史、人物、城鎮故事", "FTVTaiwanHistory"),
      ("台視時光機", "台視老連續劇、歌仔戲、綜藝", "TTVClassic"),
      ("華視懷舊頻道", "華視老劇、歌仔戲、短劇", "cts_arch"),
      ("台灣真善美", "老街、古早味、傳統手藝職人", "taiwangooddeeds"),
      ("進擊的台灣", "傳統市場、農漁業、老店故事", "FoodinTaiwan"),
      ("寶島神很大", "廟宇、陣頭、地方習俗", "godBlessBaodao")]
ch_rows = "".join(f'<tr><td>{n}</td><td>{d}</td><td><a class="go" href="https://www.youtube.com/@{h}" target="_blank" rel="noopener">開啟</a></td></tr>' for n, d, h in CH)
P_CH = "我是居家服務員，要陪長輩看懷舊影片、聊往事。請幫我收集 YouTube 上適合台灣長輩的懷舊頻道（台語老歌、國語老歌、台灣老照片和老影片、早期電視節目、古早味或老街），做成一張表：頻道名稱、主要內容、適合的陪伴活動、頻道網址。只列真的存在、還有在播放的頻道，網址要正確，10 個就好。"
P_VID = "我從「台灣真善美」挑了這支影片：（貼上影片網址）。請看完影片，幫我挑 4 個可以按暫停、問長輩的畫面，做成表格：時間碼、畫面在演什麼、可以問長輩的問題（從簡單到回憶）。最後再給 1 個看完可以一起做的小活動。只根據影片內容，看不到的寫「影片未提及」。"

S.append(f'''<!-- 懷舊頻道資料庫 -->
<section class="slide" data-title="案例② 實作①：請 Gemini 收集懷舊頻道">
  <div class="eyebrow" style="--c:var(--blue)"><span class="sq"></span>第四段　案例②　實作①：收集 YouTube 懷舊頻道</div>
  <h2>先請 Gemini 收集懷舊頻道，做成自己的影片資料庫</h2>
  <div class="cols" style="--n:2;grid-template-columns:minmax(0,5fr) minmax(0,6fr);gap:20px">
    <div style="display:flex;flex-direction:column;gap:12px;min-width:0">
      <figure class="shot" style="margin:0;flex:1;min-height:0"><div class="frame"><img src="img/yt/channels.jpg" alt="Gemini 整理的懷舊頻道表"></div><figcaption><span>Gemini 整理成表格：頻道名稱、主要內容、陪伴活動、網址（11/17 實測）</span></figcaption></figure>
      {prompt("Gemini 指令・收集懷舊頻道", P_CH)}
    </div>
    <div style="display:flex;flex-direction:column;gap:10px;min-width:0">
      <div class="box" style="padding:14px 16px;justify-content:flex-start"><h3 style="font-size:18px">實測結果：10 個頻道網址都打得開</h3>
        <table class="adj ch">{ch_rows}</table></div>
      <div class="note" style="--c:var(--blue)"><b>一定要點開確認</b><span>AI 偶爾會編出不存在的頻道。每個網址點開看一次，確認還在、內容適合，再存進自己的資料庫（Google 試算表或 LINE 記事本）。</span></div>
    </div>
  </div>
</section>
''')

S.append(stepper("var(--blue)", "第四段　案例②　實作②：請 Gemini 讀一支影片", "案例② 實作②：Gemini 讀影片",
    "從資料庫挑一支影片，請 Gemini 讀完，整理出停格聊天題",
    [("img/yt/video.jpg", "示範影片：台灣真善美〈布袋傳統手拉麵線〉11 分 40 秒", "從頻道挑一支影片",
      "挑個案熟悉的主題：他的家鄉、做過的工作、愛吃的東西。複製影片網址。"),
     ("img/yt/fail.jpg", "實測：用預設模型，Gemini 回答「無法讀取這支 YouTube 影片」", "預設模型可能讀不到",
      "看到「無法觀看」不要放棄，換模型重問一次。"),
     ("img/yt/models.jpg", "輸入框右邊的模型選單：選「深度研究 3.1 Pro」，開新對話再貼一次", "換成 Pro 模型，開新對話",
      "讀影片用 Pro 最穩；每支影片開一個新對話。"),
     ("img/yt/answer.jpg", "Pro 讀完了：4 個停格畫面，附時間碼、畫面內容、從簡單到回憶的問題", "拿到停格題目表",
      "還附一個看完可以一起做的小活動：一起拌一碗古早味麵線。"),
     ("img/yt/check.jpg", "自己對時間碼：1:00 拉麵線、2:37 曬麵線、7:07 盤麵線、10:32 拌苦茶油，四個都對", "自己跳到時間碼看一次",
      "帶之前把每個時間碼點開確認畫面，對了再帶。"),
    ],
    prompt("Gemini 指令・讀影片做停格題", P_VID), frame_bg=' style="background:#000"'))

# 案例③
S.append(case("③", "var(--mag)", "案例③ 每次都玩那幾種：做一個專屬小遊戲", "案例③：玩到不想玩？用他熟悉的題目做一個小遊戲", "Gemini Canvas",
    "阿嬤 75 歲，宜蘭人，很會煮菜，每週陪伴都玩一樣的賓果，最近說「又是這個」。家裡有一台平板。想做一個<b>她熟悉的題目</b>、點螢幕就能玩的遊戲。",
    "請用 Canvas 幫我做一個平板上玩的小遊戲網頁「阿嬤的灶腳」：一對一陪伴長輩用。共 10 題，每題顯示一道台灣家常菜的名字（例如菜脯蛋、滷肉），下方 3 個大按鈕選「主要材料」，答對有掌聲和一句稱讚，答錯顯示正確答案，不扣分。字要非常大、按鈕要大、配色溫暖、繁體中文，最後一頁顯示「今天答對幾題」和一句「下次換阿嬤教我煮」。",
    ["<b>題目換成她的</b>：家常菜、宜蘭名產、她以前常去的市場。",
     "<b>不扣分</b>：答錯也給正確答案和鼓勵，沒有失敗感。",
     "<b>一題一聊</b>：答完問「這道妳都怎麼煮？」遊戲變成聊天的開頭。",
     "<b>下次換玩法</b>：同一份題目改成配對、翻牌、猜猜看，不會又是同一個。"],
    "題目和答案你先看一次；做好後按「分享」發布成連結，傳給家屬或存在平板（下下頁教）。", plab="Gemini Canvas 指令・專屬小遊戲"))

S.append(keep("教案① 實作：Gemini Canvas 搶答網頁",
    ("教案設計①　實作：Gemini Canvas", "第四段　案例③　實作：Gemini Canvas"),
    ("<h2>Gemini Canvas：講清楚玩法，兩分鐘做出搶答遊戲</h2>", "<h2>Gemini Canvas：講清楚玩法，兩分鐘做出小遊戲</h2>"),
    ("給誰用（祖孫一起玩）、內容（題目與題數）、互動（大按鈕、煙火、兩組計分）、外觀（大字、溫暖配色）", "給誰用（一對一陪伴長輩）、內容（題目與題數）、互動（大按鈕、答對鼓勵、不扣分）、外觀（大字、溫暖配色）"),
    ("投影到電視就能帶活動。要帶走：按「分享」產生連結，或「匯出」程式碼，再到實作⑦上架。", "平板、手機打開就能玩。要帶走：按「分享」發布成連結，下一頁一步一步教。"),
    ("題目的醫療說法由你把關。", "題目和答案由你把關。"),
    ("<b>答對有煙火、有衛教重點</b>", "<b>答對有鼓勵，看看成品</b>"),
    ("Gemini 還自己加了「朗讀題目」與「選題清單」。不要的功能直接說「拿掉朗讀」。", "Gemini 常會自己加功能（截圖是加了朗讀題目和兩隊計分）。不要的功能直接說「拿掉計分」。"),
    ('''提示詞・祖孫搶答網頁<button class="copy">複製</button></div>幫我做一個互動網頁：「阿公阿嬤的童年 vs 我的童年」搶答遊戲，給祖孫一起玩。10 題二選一（例：小時候玩彈珠還是玩平板？），大字、大按鈕，答完顯示一句「請阿公阿嬤分享當年」的提問，可分祖孫兩隊計分，答對放煙火。繁體中文，溫暖配色。''',
     '''Gemini 指令・不滿意就追問<button class="copy">複製</button></div>請幫我修改：1. 字再放大一倍，按鈕至少占螢幕寬度的一半；2. 拿掉計時和扣分；3. 每題答完多一句聊天問題，例如「這道菜妳都什麼時候煮？」；4. 其他地方不要改。'''),
    new_title="案例③ 實作：Gemini Canvas"))


# ── 案例③ 分享出去（發布） ──

S.append(stepper("var(--mag)", "第四段　案例③　發布出去：分享連結", "案例③ 發布：Gemini 分享連結",
    "做好的遊戲發布出去：一個連結，個案、家屬、同事都能玩",
    [("img/ws/gem_canvas.jpg", "Canvas 右上角：程式碼／預覽、匯出、分享（＜ 形狀的圖示）", "按 Canvas 右上角的「分享」",
      "在預覽畫面上方，「匯出」右邊那個圖示。"),
     ("img/ws/gem_share.jpg", "按下去就產生公開連結，而且已經自動複製好了（11/17 實測）", "連結已經自動複製",
      "畫面出現 share.gemini.google 開頭的連結，直接到 LINE 貼上傳給家屬或自己。"),
     ("img/ws/gem_warn.jpg", "對方第一次打開：Gemini 會先提醒「這個應用程式是由他人打造」", "對方打開，先按「繼續」",
      "這是 Google 的安全提醒，跟家屬說：看到這個畫面按「繼續」就好。"),
     ("img/ws/gem_shared.jpg", "按繼續後就能玩，按鈕也能用（這是 Gemini 做的配對學習單）", "手機、平板打開就能玩",
      "平板用 Safari 打開，按「分享 → 加入主畫面」，下次點圖示就開。"),
    ],
    '''<div class="note" style="--c:var(--mag)"><b>發布前想一想</b><span>拿到連結的人都能打開：題目裡不要有個案姓名、照片、地址。不想分享了，到 Gemini「設定 → 你的公開連結」刪除。</span></div>
      <div class="note" style="--c:var(--blue)"><b>ChatGPT 做的圖片</b><span>圖片或 PDF 直接傳 LINE，或存在平板的「照片」裡，打開就能用。</span></div>'''))

# ── 做教具：四種學習單 ──
def wscard(img, title, tool, color, pdf):
    return (f'<figure class="wsc" style="--c:{color}"><a href="{img}" target="_blank" rel="noopener"><img src="{img}" alt="{esc(title)} 成品" loading="lazy"></a>'
            f'<figcaption><b>{title}</b><span class="tool">{tool}</span><a class="go" href="{pdf}" target="_blank" rel="noopener">A4 PDF</a></figcaption></figure>')

S.append(f'''<!-- 學習單總覽 -->
<section class="slide" data-title="做教具：四種學習單（真的成品）">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>第四段　做教具：學習單</div>
  <h2>四種學習單，ChatGPT、Gemini 都做得到：印出來、存 PDF、iPad 直接畫</h2>
  <div class="wsrow">
    {wscard("img/ws/ws_matching_chatgpt.jpg", "連連看", "ChatGPT 畫圖", "#10A37F", "pdf/連連看_ChatGPT.pdf")}
    {wscard("img/ws/ws_find_chatgpt.jpg", "找物品圈起來", "ChatGPT 畫圖", "#10A37F", "pdf/找物品圈起來_ChatGPT.pdf")}
    {wscard("img/ws/ws_compare_gemini.jpg", "比大小", "Gemini Canvas", "var(--blue)", "pdf/比大小_Gemini.pdf")}
    {wscard("img/ws/ws_pair_gemini.jpg", "配對圖片", "Gemini Canvas", "var(--blue)", "pdf/配對圖片_Gemini.pdf")}
  </div>
  <div class="noterow" style="--k:3">
    <div class="note" style="--c:var(--green)"><b>印出來</b><span>A4 直式、黑白也清楚；長輩用粗的彩色筆畫線、圈起來。</span></div>
    <div class="note" style="--c:var(--amber)"><b>存成 PDF</b><span>ChatGPT：說「做成 A4 PDF」；Gemini：按頁面上的「列印 / 存成 PDF」。</span></div>
    <div class="note" style="--c:var(--blue)"><b>iPad 直接玩</b><span>圖片存進「照片」→「編輯」→ 筆的圖示，用手指畫線、圈起來；按「復原」就能再玩一次。</span></div>
  </div>
  <p class="muted" style="font-size:13px">以上四張都是 11/17 用下一頁的指令實際做出來的成品，沒有修圖。點圖片看大圖，點「A4 PDF」下載列印。</p>
</section>
''')

P_MATCH = "幫我畫一張 A4 直式、可以列印的「連連看」學習單圖片，給視力不好的長輩：標題「菜市場連連看」。左邊一排 5 個大大的蔬菜水果圖（高麗菜、香蕉、番茄、地瓜、西瓜），右邊一排 5 個大字名稱，順序打亂，每個圖和名稱旁邊各有一個黑色大圓點，中間留大片空白讓長輩畫線。字要非常大、黑色粗體、白底、線條清楚、不要其他裝飾。繁體中文，不要錯字。"
P_FIND = "幫我畫一張 A4 直式、可以列印的「找找看，圈起來」學習單圖片，給視力不好的長輩：上方大標題「菜市場找找看」。中間是一張熱鬧但不複雜的台灣傳統菜市場攤位插圖，畫面裡清楚放著 5 樣東西：香蕉、一條魚、一盒雞蛋、竹菜籃、傳統秤。物品要畫大、輪廓清楚、不要互相重疊。最下方一排列出這 5 樣東西的小圖和大字名稱，旁邊各有一個空白方框可以打勾。白底、線條清楚、顏色明亮，繁體中文，不要錯字。"
P_COMPARE = "請用 Canvas 幫我做一個可以列印的 A4 直式學習單網頁「撲克牌比大小」，給視力不好的長輩：最上面大標題和一行說明「圈出數字比較大的那張牌」，下面 5 題，每題左右兩張很大的撲克牌（只用 A 到 10，紅心或黑桃，用程式畫出來，數字和花色要很大），題號大字。頁面上有「換一組題目」和「列印 / 存成 PDF」兩個大按鈕，按列印時按鈕不要印出來，剛好一張 A4。白底、黑色粗框、繁體中文。"
P_PAIR = "請用 Canvas 幫我做一個可以列印的 A4 直式學習單網頁「找一樣的：配對圖片」，給視力不好的長輩：最上面大標題和一行說明「把一樣的圖片用線連起來」。左右兩欄各 5 張大圖，畫長輩熟悉的生活用品（電鍋、雨傘、斗笠、菜籃、茶壺），用程式畫出大大的彩色圖案，右邊順序打亂；每張圖旁邊有一個黑色大圓點方便畫線。頁面上有「換一組順序」和「列印 / 存成 PDF」兩個大按鈕，列印時按鈕不要印出來，5 題剛好一張 A4。白底、黑色粗框、繁體中文。"

S.append(stepper("#10A37F", "第四段　做教具　ChatGPT 做法", "學習單 ChatGPT 做法：畫成圖片再轉 PDF",
    "ChatGPT 做法：請它「畫」一張學習單，再轉成 A4 PDF",
    [("img/ws/gpt_match_chat.jpg", "chatgpt.com：貼上指令，約 1 分鐘畫好（11/17 實測）", "貼指令，請它畫",
      "寫清楚：A4 直式、給誰（視力不好的長輩）、內容幾題、字要大、白底。"),
     ("img/ws/ws_matching_chatgpt.jpg", "成品：菜市場連連看", "逐字檢查",
      "名稱有沒有錯字、圖跟字對不對得起來。有錯就說「把右邊第 2 個字改成…，其他不要動」。"),
     ("img/ws/gpt_match_pdf.jpg", "說「做成 A4 PDF」，它直接給一個 PDF，右上角下載", "請它做成 A4 PDF",
      "再打一句：「請把這張圖做成 A4 大小的 PDF 檔讓我下載列印」。"),
     ("img/ws/ws_find_chatgpt.jpg", "同一招做「找物品圈起來」：菜市場攤位插圖", "換題目做下一張",
      "找物品圈起來、配對、比大小都一樣做法；指令在下一頁。"),
    ],
    prompt("ChatGPT 指令・連連看", P_MATCH), frame_bg=' style="background:var(--soft)"'))

S.append(stepper("var(--blue)", "第四段　做教具　Gemini 做法", "學習單 Gemini 做法：Canvas 可列印網頁",
    "Gemini 做法：用 Canvas 做「可以一直換題目」的學習單網頁",
    [("img/ws/gem_canvas.jpg", "Gemini Canvas 做好的學習單網頁：換一組順序、列印 / 存成 PDF", "請 Canvas 做學習單網頁",
      "指令加一句「有換一組題目和列印按鈕，列印時按鈕不要印出來」。"),
     ("img/ws/ws_compare_gemini.jpg", "按「列印 / 存成 PDF」：撲克牌比大小，剛好一張 A4", "按列印，或存成 PDF",
      "列印視窗裡「目的地」選「另存為 PDF」就變成檔案。"),
     ("img/ws/ws_compare_gemini.jpg", "第一次做第 5 題被切到下一頁；追問一句就改好", "印不下？追問一句",
      "實測第一次第 5 題被切掉，說「把每題縮小一點，5 題剛好一張 A4，其他不要改」就好了。"),
     ("img/ws/ws_pair_gemini.jpg", "同一招做「配對圖片」：電鍋、雨傘、斗笠、菜籃、茶壺", "按「換一組」就是新的一張",
      "每次陪伴印一張不一樣的，不怕個案背答案。"),
    ],
    prompt("Gemini 指令・比大小", P_COMPARE), frame_bg=' style="background:var(--soft)"'))

S.append(f'''<!-- 四種學習單指令 -->
<section class="slide" data-title="四種學習單指令">
  <div class="eyebrow" style="--c:var(--green)"><span class="sq"></span>第四段　做教具　指令帶回去用</div>
  <h2>四種學習單的指令：複製、改主題，就是你的學習單</h2>
  <div class="cols" style="--n:2">
    {prompt("連連看（ChatGPT）", P_MATCH)}
    {prompt("找物品圈起來（ChatGPT）", P_FIND)}
    {prompt("比大小（Gemini Canvas）", P_COMPARE)}
    {prompt("配對圖片（Gemini Canvas）", P_PAIR)}
  </div>
  <div class="note" style="--c:var(--green)"><b>改主題</b><span>菜市場換成「廚房用品」「台灣小吃」「老家農具」；變簡單：題目少一點；變難：換成影子配對、多 2 個干擾物。</span></div>
</section>
''')

# ── 懷舊應用：時光留聲機 ──
S.append(stepper("var(--amber)", "第四段　懷舊應用　帶大家一起操作", "懷舊應用：時光留聲機",
    "時光留聲機：陪長輩說故事，把人生錄成一張唱片",
    [("img/lsp/1_elder.jpg", "第一次打開：輸入長輩稱呼（出生年可不填）", "打開網頁，輸入長輩稱呼",
      "稱呼會印在故事書封面。手機可以「加到主畫面」，下次一點就開。"),
     ("img/lsp/2_home.jpg", "首頁：開始聊天，或隨機抽一題", "按「開始聊天」",
      "不知道從哪開始，按「隨機抽一題」。"),
     ("img/lsp/3_topics.jpg", "七段人生：童年時光、求學青春、工作打拼、成家相伴、家鄉味道、人生智慧、留給家人", "選一段人生，點一個問題",
      "從他最熟悉、最開心的那段開始，例如童年、家鄉味道。"),
     ("img/lsp/4_consent.jpg", "錄音前，先問長輩願不願意", "錄音前先問一聲",
      "「我想把您說的故事錄下來，留給家裡的孩子聽，好不好？」長輩答應了再錄。"),
     ("img/lsp/5_record.jpg", "唸題目、按開始錄音；下面有追問小卡和陪伴小提醒", "慢慢問，用追問小卡接話",
      "長輩停下來就點一張追問小卡；記錯不糾正、沉默先等十秒，一次 10～20 分鐘。"),
     ("img/lsp/6_label.jpg", "說完了：寫故事名稱、年代、重點，配一張老照片", "替這張唱片寫標籤",
      "只有名稱是必要的；配一張老照片，會印在唱片中間。"),
     ("img/lsp/7_book.jpg", "故事書：列印生命故事書、下載備份", "印成生命故事書送家人",
      "所有唱片整理成一本書，可以列印或存成 PDF；換手機前先「下載備份」。"),
    ],
    f'''<div class="note" style="--c:var(--amber)"><b>為什麼用懷舊</b><span>聊自己的人生，長輩最有共鳴、最想說；錄下來的聲音和故事，是留給家人的記憶。</span></div>
      <div class="note" style="--c:var(--blue)"><b>打開網頁</b><span>{A("https://mattsue1003.github.io/life-story-phonograph/", "mattsue1003.github.io/life-story-phonograph")}　聲音只存在這台裝置，不會上傳。</span></div>'''))

# 做好的工具直接用
S.append(f'''<!-- 現成工具 -->
<section class="slide" data-title="做好的工具也可以直接用">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>不用從零開始</div>
  <h2>這些都是 AI 做的：手機、平板打開，帶到個案家就能玩</h2>
  {exs([
    ("one-set-many-games","一題多玩","同一份題目換 27 種玩法，不怕玩膩"),
    ("order-different-slides","長者遊戲簡報生成器","找不同、數一數、規律接龍 8 種"),
    ("poker-icebreakers","撲克牌 7 種玩法","看動畫就會玩的撲克牌遊戲"),
    ("pop-song-guess","台灣金曲猜歌","國語台語 300 首，聽前奏猜歌名"),
    ("home-play-library","在家動一動 活動庫","居家版 78 個運動、認知活動"),
    ("sensory-play-lessons","感覺遊戲教案庫","100 個用家裡東西就能玩的遊戲"),
  ], m=3)}
</section>
''')

# 檢查
S.append('''<!-- 檢查 -->
<section class="slide" data-title="帶活動前的檢查清單">
  <div class="eyebrow" style="--c:var(--mag)"><span class="sq"></span>第五段　AI 會出錯</div>
  <h2>帶活動前，花兩分鐘檢查這五件事</h2>
  <div class="cols" style="--n:2">
    <ul class="check" id="safe">
      <li><label><input type="checkbox" id="k1"><span><b>個資沒有放進去</b><br><small class="muted">姓名、地址、照片、病歷號都不要給 AI。</small></span></label></li>
      <li><label><input type="checkbox" id="k2"><span><b>自己先玩一次</b><br><small class="muted">規則講得通嗎？會不會太難、太久？</small></span></label></li>
      <li><label><input type="checkbox" id="k3"><span><b>安全沒問題</b><br><small class="muted">小東西會不會被放進嘴巴？站起來會不會跌倒？</small></span></label></li>
      <li><label><input type="checkbox" id="k4"><span><b>內容是對的</b><br><small class="muted">歌名、歌手、數字、健康說法，上網查一次。</small></span></label></li>
      <li><label><input type="checkbox" id="k5"><span><b>準備一個更簡單的版本</b><br><small class="muted">個案今天狀況不好時，馬上換。</small></span></label></li>
    </ul>
    <div style="display:flex;flex-direction:column;gap:14px;min-width:0">
      <div class="note" style="--c:var(--mag)"><b>AI 很有自信</b><span>它講錯的時候語氣也很肯定。看到不確定的，請它「附上來源」，或換另一個 AI 問。</span></div>
      <div class="note" style="--c:var(--blue)"><b>看個案的反應</b><span>皺眉、不說話、一直看時鐘，就是太難或太久了，換玩法或休息。</span></div>
      <div class="note" style="--c:var(--green)"><b>記錄下來</b><span>今天玩了什麼、他喜歡什麼，下次寫進指令，AI 會越來越準。</span></div>
    </div>
  </div>
</section>
''')

# 提示詞庫
S.append(f'''<!-- 提示詞庫 -->
<section class="slide" data-title="提示詞庫">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>帶回去用</div>
  <h2>提示詞庫：把（ ）換掉就能用</h2>
  <div class="cols" style="--n:2">
    {prompt("想點子", "我是居家服務員，個案（年齡、以前的工作、喜歡什麼），身體狀況（ ）。家裡有（道具）。請設計 5 個一對一、（30）分鐘內的活動，每個寫玩法步驟和帶領時說的第一句話。")}
    {prompt("依狀況改玩法", "這是（遊戲名稱與玩法）。我的個案（做得到什麼、做不到什麼）。請改成他做得到的版本，並再給一個更簡單的版本。")}
    {prompt("一副道具玩四種", "我有一副（撲克牌／報紙／寶特瓶），請依「配對、組合、排序、線索」各設計一個一對一玩法，每個寫做法、變簡單、變難、帶領時說的一句話。")}
    {prompt("懷舊聊天題卡", "個案（年齡、家鄉、以前的工作）。請設計 10 個聊天問題，從簡單的是非題，到「那時候你在做什麼」的回憶題，避免讓人難過的話題。")}
    {prompt("做大字道具", "幫我做一張 A4 直式可以列印的（大字數字卡／題目卡），一頁 4 張，字要非常大、黑字白底、粗外框、有裁切線，繁體中文。")}
    {prompt("做小遊戲（Gemini Canvas）", "用 Canvas 做一個平板玩的小遊戲，給一對一陪伴長輩：主題（ ），10 題三選一，大字大按鈕，答對有鼓勵、答錯不扣分，最後顯示答對幾題。繁體中文。")}
  </div>
</section>
''')

# 帶走三件事
S.append('''<!-- 帶走 -->
<section class="slide" data-title="今天帶走三件事">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>課後試試看</div>
  <h2>下一次陪伴前，先試這三件事</h2>
  <div class="cols" style="--n:2">
    <ul class="check">
      <li><label><input type="checkbox" id="h1"><span><b>打開 ChatGPT 或 Gemini</b>，用五要素寫一個個案的活動指令</span></label></li>
      <li><label><input type="checkbox" id="h2"><span><b>用撲克牌</b>，設計配對、組合、排序、線索各一個玩法</span></label></li>
      <li><label><input type="checkbox" id="h3"><span><b>做一張大字道具</b>，或用 Gemini 做一個他熟悉的小遊戲</span></label></li>
    </ul>
    <div style="display:flex;flex-direction:column;gap:14px;min-width:0">
      <div class="note" style="--c:var(--blue)"><b>今天三重點</b><span>AI 想點子、你認識個案｜指令寫清楚五要素｜從他做得到的開始，最後讓他成功。</span></div>
      <div class="note" style="--c:var(--mag)"><b>記得</b><span>不放個案姓名、照片給 AI；AI 做的規則和內容，帶之前自己玩一次。</span></div>
      <div class="note" style="--c:var(--lime)"><b>勾選</b><span>打勾會記在這台電腦的瀏覽器裡，下次打開還在。</span></div>
    </div>
  </div>
</section>
''')


# 資料庫（最後面）
S.append(f'''<!-- 資料庫 -->
<section class="slide" data-title="更多資料庫：帶回去慢慢用">
  <div class="eyebrow" style="--c:var(--sky)"><span class="sq"></span>帶回去用　資料庫</div>
  <h2>更多資料庫：聽歌、猜圖、認識鳥蟲花、聊天、團康</h2>
  {exs([
    ("oldsongdata","懷舊點唱機：回憶金曲 200","依年代找長輩年輕時的歌，一起聽"),
    ("oldpicguess","看照片猜藝人","臺灣資深藝人老照片，猜猜是誰"),
    ("bird-guess-quiz","猜猜我是誰：台灣鳥朋友","一步一步給提示，還有真實鳥叫聲"),
    ("insect-guess-quiz","猜猜我是誰：台灣昆蟲朋友","看特徵猜昆蟲，附影片"),
    ("flower-guess-quiz","猜猜我是什麼花","台灣四季花朋友，分段提示猜花"),
    ("home-chat-db","居家陪伴聊天庫","36 主題懷舊聊天題，附接話範例"),
    ("home-chat-local","居家聊天在地篇","依身分背景、家鄉找話題"),
    ("group-building-games","團康活動影片資料庫","破冰、合作、律動，看影片就會帶"),
    ("japan-dayservice-activity-videos","日照團康影片資料庫","日本日照中心團康與體操，中文整理"),
    ("life-story-phonograph","時光留聲機","陪長輩說故事，錄成唱片和故事書"),
  ], m=5)}
</section>
''')

S.append(keep("謝謝聆聽",
    ('<a class="fbcard" href="https://mattsue1003.github.io/intergen-ai-play/"', f'<a class="fbcard" href="{DECK_URL}"'),
    (re.search(r'\s*<a class="fbcard" href="https://line\.me.*?</a>', old["謝謝聆聽"], re.S).group(0), "")))

# 議程（依頁碼自動對應）
def idx(title):
    for i, s in enumerate(S):
        if f'data-title="{esc(title)}"' in s: return i + 1
    raise KeyError(title)
ag = [("var(--mag)", "開場：你也遇過嗎？", "三種陪伴困擾，先玩一題", "封面", "5′", "你是不是也遇過？"),
      ("var(--blue)", "認識 AI 活動設計", "AI 能幫你做的四件事、ChatGPT 和 Gemini 怎麼選", "", "6′", "認識 AI 活動設計：AI 能幫你做的四件事"),
      ("var(--blue)", "基本操作", "登入、開新對話、用說的、繁體設定、好指令五要素", "", "10′", "基本操作① 打開、登入、開新對話"),
      ("var(--green)", "好玩的原則", "能力階梯、撲克牌四種玩法、依狀況調整", "", "7′", "好玩的原則① 從他做得到的那一層開始"),
      ("var(--amber)", "三個案例＋發布", "① 撲克牌×視力不好　② 老歌聊天　③ 專屬小遊戲＋分享連結", "", "14′", "案例① 撲克牌×視力不好的阿嬤"),
      ("var(--green)", "做教具：四種學習單", "連連看、找物品、比大小、配對：ChatGPT 與 Gemini 做法", "", "8′", "做教具：四種學習單（真的成品）"),
      ("var(--amber)", "懷舊應用：時光留聲機", "陪長輩說故事，錄成唱片、印成故事書", "", "6′", "懷舊應用：時光留聲機"),
      ("var(--sky)", "檢查與資料庫", "檢查清單、提示詞庫、更多資料庫", "", "4′", "帶活動前的檢查清單")]
links = "".join(f'<a href="#s{idx(t)}"><span class="no" style="--c:{c}">{i}</span><span><strong>{a}</strong><small>{b}</small></span><em>{m}</em></a>'
                for i, (c, a, b, _, m, t) in enumerate(ag))
S[S.index("@@AGENDA@@")] = f'''<!-- 地圖 -->
<section class="slide" data-title="今天的地圖">
  <div class="eyebrow" style="--c:var(--amber)"><span class="sq"></span>今天的地圖　60 分鐘</div>
  <h2>先學會基本操作，再用三個案例做出好玩活動</h2>
  <nav class="agenda" aria-label="課程地圖">{links}</nav>
  <div class="learn"><span>上完課你會：認識 AI 工具的基本操作</span><span>用有效指令產出活動設計</span><span>把 AI 用在每天的陪伴</span></div>
</section>
'''

out = head + "".join(S) + tail

# 網址都做成可以點的連結（開新分頁）
LINKS = [
    ('<p>網址 myaccount.google.com/language → ', '<p>網址 ' + A("https://myaccount.google.com/language", "myaccount.google.com/language") + ' → '),
    ('<span class="sub">chatgpt.com・', '<span class="sub">' + A("https://chatgpt.com/", "chatgpt.com") + '・'),
    ('<span class="sub">gemini.google.com・', '<span class="sub">' + A("https://gemini.google.com/", "gemini.google.com") + '・'),
    ('電腦打開 <b>chatgpt.com</b>', '電腦打開 ' + A("https://chatgpt.com/", "<b>chatgpt.com</b>")),
    ('電腦打開 <b>gemini.google.com</b>', '電腦打開 ' + A("https://gemini.google.com/", "<b>gemini.google.com</b>")),
    ('<p>左下角頭像 → 設定 → 聲音 → 語言。', '<p>' + A("https://chatgpt.com/#settings/Speech", "打開 ChatGPT") + '：左下角頭像 → 設定 → 聲音 → 語言。'),
    ('<p>個人化 → 自訂指示 → ChatGPT，', '<p>' + A("https://chatgpt.com/#settings/Personalization", "打開 ChatGPT 個人化") + '：個人化 → 自訂指示 → ChatGPT，'),
    ('<p>左下齒輪 → 個人化智慧服務 → 給 Gemini 的指令，', '<p>' + A("https://gemini.google.com/", "打開 Gemini") + '：左下齒輪 → 個人化智慧服務 → 給 Gemini 的指令，'),
]
for a, b in LINKS:
    assert a in out, a
    out = out.replace(a, b)
assert "intergen-ai-play" not in out, [out[m.start()-80:m.start()+40] for m in re.finditer("intergen-ai-play", out)][:3]
(ROOT / "deck.html").write_text(out)
print("slides:", len(S))
