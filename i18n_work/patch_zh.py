# 중국어 간체(zh)·번체(tw) 언어 추가 패치. tabishiori.html, backup pre, sitegen 화면 코드에 같은 수정을 적용해요.
import json, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw

def tw(o):
    if isinstance(o, str): return s2tw(o)
    if isinstance(o, list): return [tw(x) for x in o]
    return {k: tw(v) for k, v in o.items()}

PMETA_ZH = {
 "t": {"guide_season": "日本旅游最佳季节 – 各地樱花·梅雨·红叶时间与四季穿衣",
       "guide_stay": "日本住哪里 – 东京·大阪·京都·名古屋·广岛·四国·福冈·北海道·冲绳住宿区域推荐",
       "guide_entry": "入境准备 – 日本签证、Visit Japan Web登记、禁止携带物品",
       "guide_money": "日本旅游花钱指南 – 换汇、现金与刷卡、ATM",
       "guide_connect": "日本旅游上网 – eSIM·随身Wi-Fi·SIM卡·漫游比较",
       "guide_etiquette": "日本旅游礼仪 – 温泉、神社参拜、垃圾分类、公共交通、餐厅",
       "map": "日本旅游地图 – 景点·节庆·美食·购物位置",
       "spots": "{a}景点推荐 · {c}旅游", "festivals": "{a}节庆·活动 · {c}旅游", "food": "{a}美食推荐 · {c}旅游",
       "transport": "{a}交通·机场出发攻略 · {c}旅游", "shopping": "{a}购物·伴手礼 · {c}旅游",
       "all_spots": "日本景点推荐 – 东京·大阪·京都·福冈·北海道·冲绳名胜",
       "all_festivals": "日本{m}节庆·活动 – 各地祭典日历", "all_food": "日本美食推荐 – 各地区·各类别TOP 5",
       "all_transport": "日本交通指南 – 机场到市区、交通卡", "all_shopping": "日本购物·伴手礼 – 购物街、免税、特产",
       "saved": "我的旅行"},
 "d": {"guide_season": "各地樱花开花、梅雨、红叶最佳期（平年值）与四季穿衣，以及避开台风和长假的方法。",
       "guide_stay": "比较各地适合住宿的区域，包括优缺点和适合人群。",
       "guide_entry": "入境日本前需确认的签证、Visit Japan Web登记步骤、肉类·水果·药品等禁止携带物品及免税额度。",
       "guide_money": "在日本准备多少现金和卡、如何换汇和使用ATM、刷卡小贴士。",
       "guide_connect": "比较在日本上网的方法：eSIM、随身Wi-Fi、SIM卡、漫游的优缺点和选择方法。",
       "guide_etiquette": "温泉使用方法、神社寺院参拜、垃圾分类、电车和餐厅礼仪一览。",
       "map": "在日本地图上一览景点、节庆、美食和购物地点。选择地区和类别即可查看位置和信息。",
       "spots": "{a}值得去的地方{L}。今日天气、推荐路线和市内交通一目了然。",
       "festivals": "{a}举办的节庆和季节活动{L}。日期、地点和玩法。",
       "food": "{a}美食推荐{L}。拉面、寿司、烤肉等各类别TOP 5和必吃乡土料理。",
       "transport": "{a}交通指南：从机场出发的方法、市内交通、交通卡购买地点。",
       "shopping": "{a}购物{L}。购物街和市场、免税指南、值得买的特产和伴手礼。",
       "all_spots": "按地区挑选东京、大阪、京都、名古屋、广岛、四国、福冈、北海道、冲绳的景点{L}。",
       "all_festivals": "日本{m}举办的节庆和季节活动{L}。日期、地点和玩法。",
       "all_food": "日本各地区美食推荐和必吃乡土料理{L}。",
       "all_transport": "从日本各机场到市区的方法、城市间交通、Suica·ICOCA等交通卡指南。",
       "all_shopping": "日本的购物街和市场、新免税制度、各地特产和伴手礼推荐{L}。"},
 "L": "（{n}等）"}
PT_ZH = {"spot": "{n} – 门票·营业时间·交通（{a}）", "fest": "{n} – 日期·地点·游玩贴士（{a}）",
         "shop": "{n} – 购物信息·推荐清单（{a}）", "food": "{n} – {a}乡土料理和品尝地点"}
IT_ZH = {"about": "关于本站", "contact": "联系我们", "privacy": "隐私政策",
         "d": "Go Nihon Trip网站介绍、信息来源、联系方式与隐私政策。"}
IM_ZH = ["日本旅行推荐行程 – 东京·大阪·京都·福冈·北海道·冲绳路线", "{t} – 推荐行程",
         "东京、大阪、京都、名古屋、广岛、四国、福冈、北海道、冲绳的多日推荐行程，每日路线和门票一目了然。"]
DESC_ZH = "东京、大阪、名古屋、广岛、四国、福冈、北海道、冲绳及周边城市的景点、节庆、美食、交通、购物信息与实时天气。"

J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))
ZHTW = lambda o: f'zh:{J(o)},tw:{J(tw(o))}'

R = [  # (old, new) — 찾지 못하면 그 파일에선 건너뜀
 ('var ok=["en","ja","es","fr"], l=null;', 'var ok=["en","ja","es","fr","zh","tw"], l=null;'),
 ('if(ok.indexOf(l)>=0){ document.documentElement.lang=l;', 'if(ok.indexOf(l)>=0){ document.documentElement.lang=l==="zh"?"zh-Hans":l==="tw"?"zh-Hant":l;'),
 ('if(I.lang==="ja") return g[k]+"月";', 'if(I.lang==="ja"||I.lang==="zh"||I.lang==="tw") return g[k]+"月";'),
 ('avec la météo en direct."};', 'avec la météo en direct.",' + f'zh:{J(DESC_ZH)},tw:{J(s2tw(DESC_ZH))}' + '};'),
 ('{en:"en_US",ja:"ja_JP",es:"es_ES",fr:"fr_FR"}[I.lang]', '{en:"en_US",ja:"ja_JP",es:"es_ES",fr:"fr_FR",zh:"zh_CN",tw:"zh_TW"}[I.lang]'),
 # 다국어 객체: 중국어는 사전(D)에서 한국어로 찾아요
 (' const t = o => o ? (o[L()]||o.ko) : "";', ' const t = o => o ? (o[L()]||(window.I18N&&window.I18N.D&&window.I18N.D[o.ko])||o.ko) : "";'),
 ('l==="ja"?"ja-JP":l==="es"?"es-ES":l==="fr"?"fr-FR":"en-US"', 'l==="ja"?"ja-JP":l==="es"?"es-ES":l==="fr"?"fr-FR":l==="zh"?"zh-CN":l==="tw"?"zh-TW":"en-US"'),
 ('if(l==="ko") return n+"엔"+(from?"~":""); if(l==="ja") return n+"円"+(from?"〜":"");',
  'if(l==="ko") return n+"엔"+(from?"~":""); if(l==="ja") return n+"円"+(from?"〜":""); if(l==="zh") return n+"日元"+(from?"起":""); if(l==="tw") return n+"日圓"+(from?"起":"");'),
 ('if(l==="ko"||l==="ja") return `${m}/${d}`;', 'if(l==="ko"||l==="ja"||l==="zh"||l==="tw") return `${m}/${d}`;'),
 ('return l==="ko"?`${a}월`:l==="ja"?`${a}月`:MON[l][a-1]; }', 'return l==="ko"?`${a}월`:(l==="ja"||l==="zh"||l==="tw")?`${a}月`:MON[l][a-1]; }'),
 ('if(l==="ko") return `${a}~${b}월`; if(l==="ja") return `${a}〜${b}月`;', 'if(l==="ko") return `${a}~${b}월`; if(l==="ja") return `${a}〜${b}月`; if(l==="zh"||l==="tw") return `${a}～${b}月`;'),
 ('${L()==="ja"?"〜":L()==="ko"?"~":"–"}', '${L()==="ja"?"〜":(L()==="zh"||L()==="tw")?"～":L()==="ko"?"~":"–"}'),
 ('l==="ja"?`（最終入場${x}）`:', 'l==="ja"?`（最終入場${x}）`:l==="zh"?`（最后入场${x}）`:l==="tw"?`（最後入場${x}）`:'),
 ('const colon = L2 => (L2==="ja"?"：":', 'const colon = L2 => (L2==="ja"||L2==="zh"||L2==="tw"?"：":'),
 ('l==="ja"?`毎月第${c.n}${w}`:', 'l==="ja"?`毎月第${c.n}${w}`:l==="zh"?`每月第${c.n}个${w}`:l==="tw"?`每月第${c.n}個${w}`:'),
 # 추천 일정
 ('l==="ja"?`${n}泊${n+1}日`:', '(l==="zh"||l==="tw")?`${n}晚${n+1}天`:l==="ja"?`${n}泊${n+1}日`:'),
 ('l==="ja"?`${i}日目`:', '(l==="zh"||l==="tw")?`第${i}天`:l==="ja"?`${i}日目`:'),
 ('l==="ja"?`${n}か所`:', 'l==="zh"?`${n}个地点`:l==="tw"?`${n}個地點`:l==="ja"?`${n}か所`:'),
 # 지도 글자: 중국어는 중국어 이름 → 현지(일본어) 이름
 ('const nm = lang==="ja" ? ["get","name"] :', 'const nm = lang==="ja" ? ["get","name"] : lang==="zh" ? ["coalesce",["get","name:zh-Hans"],["get","name:zh"],["get","name"]] : lang==="tw" ? ["coalesce",["get","name:zh-Hant"],["get","name:zh"],["get","name"]] :'),
 ('document.documentElement.lang=LANG;', 'document.documentElement.lang=LANG==="zh"?"zh-Hans":LANG==="tw"?"zh-Hant":LANG;'),
 # 주소
 ('p = p.replace(/^(en|ja|es|fr)(\\/|$)/,"");', 'p = p.replace(/^(en|ja|es|fr|zh|tw)(\\/|$)/,"");'),
 # 메타
 ('c = {ko:"일본",en:"Japan",ja:"日本",es:"Japón",fr:"Japon"}[L];', 'c = {ko:"일본",en:"Japan",ja:"日本",es:"Japón",fr:"Japon",zh:"日本",tw:"日本"}[L];'),
 ('const mon = L==="ko" ? st.month+"월" : L==="ja" ? st.month+"月" :', 'const mon = L==="ko" ? st.month+"월" : (L==="ja"||L==="zh"||L==="tw") ? st.month+"月" :'),
 ('const sep = L==="ja" ? "、" :', 'const sep = (L==="ja"||L==="zh"||L==="tw") ? "、" :'),
 ('const LANGS=[["ko","KR","한국어"],["en","EN","English"],["ja","JP","日本語"],["es","ES","Español"],["fr","FR","Français"]];',
  'const LANGS=[["ko","KR","한국어"],["en","EN","English"],["ja","JP","日本語"],["zh","简","简体中文"],["tw","繁","繁體中文"],["es","ES","Español"],["fr","FR","Français"]];'),
 # 소개 페이지 문구: 지원 언어에 중국어 추가
 ('한국어·영어·일본어·스페인어·프랑스어로 제공해요.', '한국어·영어·일본어·중국어·스페인어·프랑스어로 제공해요.'),
]

def patch_meta(s):
    # PMETA, 장소 제목, 소개 페이지, 일정 제목에 zh·tw 추가
    a = '\n};\nfunction pageMeta(){'
    if a in s and 'PMETA_ZH_DONE' not in s:
        s = s.replace(a, ',\n ' + ZHTW(PMETA_ZH) + ' /*PMETA_ZH_DONE*/' + a, 1)
    a = 'fr:{spot:"{n} – Tarifs, horaires et accès ({a})",fest:"{n} – Dates, lieu et conseils ({a})",shop:"{n} – Guide shopping et quoi acheter ({a})",food:"{n} – Spécialité de {a} et où la goûter"}};'
    if a in s:
        s = s.replace(a, a[:-2] + ',' + ZHTW(PT_ZH) + '};', 1)
    a = 'd:"À propos de Go Nihon Trip, sources des informations, comment nous contacter et politique de confidentialité."}}'
    if a in s:
        s = s.replace(a, a[:-1] + ',' + ZHTW(IT_ZH) + '}', 1)
    a = '"Itinéraires de plusieurs jours à Tokyo, Osaka, Kyoto, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido et Okinawa, avec trajets jour par jour et tarifs."]}'
    if a in s:
        s = s.replace(a, a[:-1] + ',' + ZHTW(IM_ZH) + '}', 1)
    return s

W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html',
         f'{W}/sitegen/spot_info_view.js', f'{W}/i18n_work/backup/spot_info_view.pre.js',
         f'{W}/sitegen/itin_view.js', f'{W}/sitegen/map_view.js']
for f in FILES:
    if not os.path.exists(f): print('missing', f); continue
    s = open(f, encoding='utf-8').read(); n = 0
    for a, b in R:
        if a in s and b not in s:
            s = s.replace(a, b); n += 1
    s2 = patch_meta(s); n += s2 != s; s = s2
    open(f, 'w', encoding='utf-8').write(s)
    print(f.split('/')[-1], n, 'changes')
