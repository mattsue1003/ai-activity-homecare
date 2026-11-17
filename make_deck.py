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
    ("實作①　避免出現簡體字", "基本操作②　避免出現簡體字")))

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
    {prompt("清楚的指令（五要素都有）", "我是居家陪伴員，個案是 82 歲的阿嬤，以前在市場賣菜，喜歡聽台語老歌。她的視力不太好、手有點抖，可以坐著 30 分鐘。家裡有撲克牌、報紙和一台手機。請幫我設計 3 個一對一的活動，每個寫：玩法步驟、變簡單和變難的方法、帶領時可以說的一句話。用繁體中文。")}
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
    "我是居家陪伴員。個案是 82 歲阿嬤，以前在市場賣菜、很會算錢；視力不好，撲克牌上的小字看不清楚，手有點抖。我有一副撲克牌、一張深色桌墊。請幫我：1. 設計 3 個她看得到、拿得起來的撲克牌遊戲，每個 5–10 分鐘；2. 每個寫道具怎麼改、玩法步驟、變簡單和變難；3. 寫出邀請她玩的第一句話，讓她不覺得在考試。",
    ["<b>大字湊 10</b>：只用 A–9，牌放在深色桌墊上，一次翻 4 張，請阿嬤「當老闆找零錢」湊 10。",
     "<b>摸牌比大小</b>：把牌換成自製大字卡，兩人各翻一張，大的贏；看不清楚就用說的報數字。",
     "<b>紅黑分一分</b>：狀況不好時只分紅色、黑色兩堆，成功率高、手也有動到。",
     "<b>第一句話</b>：「阿嬤，我算錢算不好，妳教我一下，這兩張加起來多少？」"],
    "先玩她會成功的「紅黑分一分」，再進「湊 10」。牌太小？下一頁請 ChatGPT 做 A4 大字數字卡。", plab="ChatGPT 指令・改玩法"))

S.append(keep("教案⑥ ChatGPT 參考風格做學習單",
    ("教案設計⑥　紙本：ChatGPT 參考風格", "第四段　案例①　做道具：ChatGPT"),
    ("<h2>拿一張喜歡的海報當參考，做出同風格的學習單、海報</h2>", "<h2>做道具：請 ChatGPT 畫大字牌卡、題目卡、學習單</h2>"),
    ("內容換成自己的（示範主題：長者量六力）", "內容換成自己的（截圖示範的是一張衛教海報，牌卡、題目卡做法一樣）"),
    ("<b>小地方用 ChatGPT 改，大改到 Canva</b>", "<b>小地方用「標註」圈起來改</b>"),
    ("要改多處文字，下一頁用 Canva 魔法圖層更快。", "字有錯就圈起來請它改；改不好就直接說「整張重畫，只改這幾個字」。"),
    ('''請參考這張海報的 UI 設計（右側直排大標題、粉彩粉橘配淡藍、手繪線條人物、彩色小標籤標題、左下圓角「溫馨提醒」框），只參考版面與配色，不要複製它的文字、QR code 和標誌。幫我做一張 A4 直式活動海報：右側直排標題「祖孫遊戲日」，副標「一副牌玩一下午」。三個標籤段落：配對：找出一樣的牌；組合：兩張湊成 10；排序：從小排到大。溫馨提醒：輸贏不重要，一起笑最重要。繁體中文、字要大、不要錯字。''',
     '''幫我做一張 A4 直式、可以列印的「大字數字卡」：一頁 4 張卡（2×2），數字 1、2、3、4，每張卡中間一個很大的黑色粗體數字（占卡片一半高），下方畫同數量的大圓點，讓視力不好的長輩用數的也可以。白底、黑字、粗外框、卡片之間留裁切線。不要其他裝飾。繁體中文。'''),
    ("提示詞・參考海報風格", "ChatGPT 指令・大字數字卡"),
    new_title="案例① 做道具：ChatGPT 大字牌卡"))

# 案例②
S.append(case("②", "var(--blue)", "案例② 只看電視的阿公：老歌＋懷舊聊天", "案例②：陪伴只能看電視？用老歌打開話匣子", "Gemini",
    "阿公 78 歲，以前在台中做木工，退休後每天看電視，問他什麼都說「沒什麼」。家裡有手機可以放 YouTube，喜歡<b>洪一峰、文夏</b>的歌。",
    "我是居家陪伴員，要陪一位 78 歲阿公 40 分鐘。他年輕時在台中做木工，喜歡洪一峰、文夏的台語老歌，平常話不多。請幫我設計一個「聽老歌、聊往事」的活動：1. 推薦 3 首他年輕時流行的歌，附上歌名和歌手；2. 每首歌設計 3 個聊天問題，從簡單（喜不喜歡）到回憶（那時候你在做什麼）；3. 最後加一個跟著拍手或打拍子的小動作。用繁體中文。",
    ["<b>暖身</b>：先放他點名的歌，問「這首你以前常聽嗎？」只要點頭就算成功。",
     "<b>聊天三層</b>：喜不喜歡 → 那時候在哪裡聽 → 那時候你在做什麼工作。",
     "<b>請他教你</b>：「木工最難的是什麼？」把話題從歌帶到他的拿手事。",
     "<b>收尾動作</b>：副歌跟著拍手或敲桌子打拍子，動一動再結束。"],
    "歌名、歌手 AI 可能記錯，先上 YouTube 搜尋確認；聊到難過的事，停下來陪他，不用急著回到活動。", plab="Gemini 指令・老歌聊天"))

S.append(keep("實作② 讀影片：YouTube 摘要、Gemini 與 ChatGPT",
    ("實作②　讀影片：簡報影片教案的第一步", "第四段　案例②　實作：Gemini 讀影片"),
    ("<h2>影片交給 Gemini：都是 Google，讀得懂 YouTube</h2>", "<h2>影片交給 Gemini：貼上 YouTube 網址，整理出聊天題目</h2>"),
    ("逐段整理、每段附時間碼（示範影片是長者量六力）。", "逐段整理、每段附時間碼（截圖示範的是衛教影片；老歌 MV、懷舊影片一樣）。"),
    ("影片的事交給 Gemini。</p>", "影片的事交給 Gemini。</p><p><b>指令範例：</b>「看這支影片，挑 3 個可以停下來問長輩的畫面，附時間碼和問題。」</p>"),
    new_title="案例② 實作：Gemini 讀 YouTube"))

# 案例③
S.append(case("③", "var(--mag)", "案例③ 每次都玩那幾種：做一個專屬小遊戲", "案例③：玩到不想玩？用他熟悉的題目做一個小遊戲", "Gemini Canvas",
    "阿嬤 75 歲，宜蘭人，很會煮菜，每週陪伴都玩一樣的賓果，最近說「又是這個」。家裡有一台平板。想做一個<b>她熟悉的題目</b>、點螢幕就能玩的遊戲。",
    "請用 Canvas 幫我做一個平板上玩的小遊戲網頁「阿嬤的灶腳」：一對一陪伴長輩用。共 10 題，每題顯示一道台灣家常菜的名字（例如菜脯蛋、滷肉），下方 3 個大按鈕選「主要材料」，答對有掌聲和一句稱讚，答錯顯示正確答案，不扣分。字要非常大、按鈕要大、配色溫暖、繁體中文，最後一頁顯示「今天答對幾題」和一句「下次換阿嬤教我煮」。",
    ["<b>題目換成她的</b>：家常菜、宜蘭名產、她以前常去的市場。",
     "<b>不扣分</b>：答錯也給正確答案和鼓勵，沒有失敗感。",
     "<b>一題一聊</b>：答完問「這道妳都怎麼煮？」遊戲變成聊天的開頭。",
     "<b>下次換玩法</b>：同一份題目改成配對、翻牌、猜猜看，不會又是同一個。"],
    "題目和答案你先看一次；做好後按「分享」產生連結，存在平板的書籤，下次直接開。", plab="Gemini Canvas 指令・專屬小遊戲"))

S.append(keep("教案① 實作：Gemini Canvas 搶答網頁",
    ("教案設計①　實作：Gemini Canvas", "第四段　案例③　實作：Gemini Canvas"),
    ("<h2>Gemini Canvas：講清楚玩法，兩分鐘做出搶答遊戲</h2>", "<h2>Gemini Canvas：講清楚玩法，兩分鐘做出小遊戲</h2>"),
    ("給誰用（祖孫一起玩）、內容（題目與題數）、互動（大按鈕、煙火、兩組計分）、外觀（大字、溫暖配色）", "給誰用（一對一陪伴長輩）、內容（題目與題數）、互動（大按鈕、答對鼓勵、不扣分）、外觀（大字、溫暖配色）"),
    ("投影到電視就能帶活動。要帶走：按「分享」產生連結，或「匯出」程式碼，再到實作⑦上架。", "平板、手機打開就能玩。要帶走：按「分享」產生連結，傳到自己的 LINE 或存成書籤。"),
    ("題目的醫療說法由你把關。", "題目和答案由你把關。"),
    ("<b>答對有煙火、有衛教重點</b>", "<b>答對有鼓勵，看看成品</b>"),
    ("Gemini 還自己加了「朗讀題目」與「選題清單」。不要的功能直接說「拿掉朗讀」。", "Gemini 常會自己加功能（截圖是加了朗讀題目和兩隊計分）。不要的功能直接說「拿掉計分」。"),
    ('''提示詞・祖孫搶答網頁<button class="copy">複製</button></div>幫我做一個互動網頁：「阿公阿嬤的童年 vs 我的童年」搶答遊戲，給祖孫一起玩。10 題二選一（例：小時候玩彈珠還是玩平板？），大字、大按鈕，答完顯示一句「請阿公阿嬤分享當年」的提問，可分祖孫兩隊計分，答對放煙火。繁體中文，溫暖配色。''',
     '''Gemini 指令・不滿意就追問<button class="copy">複製</button></div>請幫我修改：1. 字再放大一倍，按鈕至少占螢幕寬度的一半；2. 拿掉計時和扣分；3. 每題答完多一句聊天問題，例如「這道菜妳都什麼時候煮？」；4. 其他地方不要改。'''),
    new_title="案例③ 實作：Gemini Canvas"))

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
    {prompt("想點子", "我是居家陪伴員，個案（年齡、以前的工作、喜歡什麼），身體狀況（ ）。家裡有（道具）。請設計 5 個一對一、（30）分鐘內的活動，每個寫玩法步驟和帶領時說的第一句話。")}
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

S.append(keep("謝謝聆聽",
    ('<a class="fbcard" href="https://mattsue1003.github.io/intergen-ai-play/"', f'<a class="fbcard" href="{DECK_URL}"'),
    (re.search(r'\s*<a class="fbcard" href="https://line\.me.*?</a>', old["謝謝聆聽"], re.S).group(0), "")))

# 議程（依頁碼自動對應）
def idx(title):
    for i, s in enumerate(S):
        if f'data-title="{esc(title)}"' in s: return i + 1
    raise KeyError(title)
ag = [("var(--mag)", "開場：你也遇過嗎？", "三種陪伴困擾，先玩一題", "封面", "5′", "你是不是也遇過？"),
      ("var(--blue)", "認識 AI 活動設計", "AI 能幫你做的四件事、ChatGPT 和 Gemini 怎麼選", "", "8′", "認識 AI 活動設計：AI 能幫你做的四件事"),
      ("var(--blue)", "基本操作", "登入、開新對話、用說的、繁體設定、好指令五要素", "", "15′", "基本操作① 打開、登入、開新對話"),
      ("var(--green)", "好玩的原則", "能力階梯、撲克牌四種玩法、依狀況調整", "", "10′", "好玩的原則① 從他做得到的那一層開始"),
      ("var(--amber)", "三個案例", "① 撲克牌×視力不好　② 老歌聊天　③ 專屬小遊戲", "", "17′", "案例① 撲克牌×視力不好的阿嬤"),
      ("var(--sky)", "檢查與帶回去用", "檢查清單、現成工具、提示詞庫", "", "5′", "做好的工具也可以直接用")]
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
assert "intergen-ai-play" not in out, [out[m.start()-80:m.start()+40] for m in re.finditer("intergen-ai-play", out)][:3]
(ROOT / "deck.html").write_text(out)
print("slides:", len(S))
