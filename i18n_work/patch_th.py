# 태국어(th) 언어 추가 패치. tabishiori.html, backup pre, sitegen 화면 코드, gen.py에 같은 수정을 적용해요.
import json, os
J = lambda o: json.dumps(o, ensure_ascii=False, separators=(',', ':'))

PMETA_TH = {
 "t": {"guide_season": "เที่ยวญี่ปุ่นช่วงไหนดี – ซากุระ ฤดูฝน และใบไม้แดงแต่ละภูมิภาค พร้อมการแต่งกายตามฤดู",
       "guide_stay": "พักที่ไหนดีในญี่ปุ่น – ย่านที่พักแนะนำในโตเกียว โอซาก้า เกียวโต นาโกย่า ฮิโรชิม่า ชิโกกุ ฟุกุโอกะ ฮอกไกโด โอกินาว่า",
       "guide_entry": "เตรียมตัวเข้าญี่ปุ่น – วีซ่า Visit Japan Web และของต้องห้าม",
       "guide_money": "การใช้เงินเที่ยวญี่ปุ่น – แลกเงิน เงินสดกับบัตร และ ATM",
       "guide_connect": "อินเทอร์เน็ตเที่ยวญี่ปุ่น – เปรียบเทียบ eSIM พ็อกเก็ตไวไฟ ซิมการ์ด และโรมมิ่ง",
       "guide_etiquette": "มารยาทเที่ยวญี่ปุ่น – ออนเซ็น ศาลเจ้า การแยกขยะ รถไฟ และร้านอาหาร",
       "map": "แผนที่เที่ยวญี่ปุ่น – ที่เที่ยว เทศกาล ร้านอาหาร และที่ช้อปปิ้ง",
       "spots": "ที่เที่ยวแนะนำใน{a} · เที่ยว{c}", "festivals": "เทศกาลและงานใน{a} · เที่ยว{c}", "food": "ร้านอาหารแนะนำใน{a} · เที่ยว{c}",
       "transport": "การเดินทางใน{a} และจากสนามบิน · เที่ยว{c}", "shopping": "ช้อปปิ้งและของฝาก{a} · เที่ยว{c}",
       "all_spots": "ที่เที่ยวญี่ปุ่นแนะนำ – โตเกียว โอซาก้า เกียวโต ฟุกุโอกะ ฮอกไกโด โอกินาว่า",
       "all_festivals": "เทศกาลญี่ปุ่นเดือน{m} – ปฏิทินเทศกาลแต่ละภูมิภาค", "all_food": "อาหารญี่ปุ่นแนะนำ – TOP 5 แต่ละภูมิภาคและประเภท",
       "all_transport": "คู่มือการเดินทางในญี่ปุ่น – จากสนามบินเข้าเมือง และบัตรโดยสาร", "all_shopping": "ช้อปปิ้งและของฝากญี่ปุ่น – ถนนช้อปปิ้ง ปลอดภาษี และของขึ้นชื่อ",
       "saved": "ทริปของฉัน"},
 "d": {"guide_season": "ช่วงซากุระบาน ฤดูฝน และใบไม้แดง (ค่าเฉลี่ย) ของแต่ละภูมิภาค การแต่งกายตามฤดู และวิธีหลีกเลี่ยงไต้ฝุ่นและช่วงวันหยุดยาว",
       "guide_stay": "เปรียบเทียบย่านที่พักแต่ละภูมิภาค ข้อดีข้อเสีย และเหมาะกับใคร",
       "guide_entry": "สิ่งที่ต้องเช็กก่อนเข้าญี่ปุ่น: วีซ่า ขั้นตอน Visit Japan Web ของต้องห้าม เช่น เนื้อสัตว์ ผลไม้ และยา รวมถึงปริมาณปลอดภาษี",
       "guide_money": "ควรเตรียมเงินสดและบัตรเท่าไร วิธีแลกเงินและใช้ ATM และเคล็ดลับการจ่ายด้วยบัตรในญี่ปุ่น",
       "guide_connect": "เปรียบเทียบวิธีใช้อินเทอร์เน็ตในญี่ปุ่น: eSIM พ็อกเก็ตไวไฟ ซิมการ์ด และโรมมิ่ง พร้อมวิธีเลือก",
       "guide_etiquette": "วิธีใช้ออนเซ็น การไหว้ศาลเจ้าและวัด การแยกขยะ และมารยาทบนรถไฟและในร้านอาหาร",
       "map": "ดูที่เที่ยว เทศกาล ร้านอาหาร และที่ช้อปปิ้งบนแผนที่ญี่ปุ่น เลือกภูมิภาคและหมวดเพื่อดูตำแหน่งและข้อมูล",
       "spots": "ที่น่าไปใน{a}{L} พร้อมสภาพอากาศวันนี้ เส้นทางแนะนำ และการเดินทางในเมือง",
       "festivals": "เทศกาลและงานตามฤดูกาลใน{a}{L} วันที่ สถานที่ และวิธีเที่ยว",
       "food": "อาหารแนะนำใน{a}{L} TOP 5 ราเมง ซูชิ ยากินิกุ และอื่น ๆ พร้อมอาหารท้องถิ่นที่ต้องลอง",
       "transport": "คู่มือการเดินทางใน{a}: จากสนามบิน การเดินทางในเมือง และที่ซื้อบัตรโดยสาร",
       "shopping": "ช้อปปิ้งใน{a}{L} ถนนช้อปปิ้งและตลาด คู่มือปลอดภาษี ของขึ้นชื่อและของฝาก",
       "all_spots": "เลือกที่เที่ยวตามภูมิภาคในโตเกียว โอซาก้า เกียวโต นาโกย่า ฮิโรชิม่า ชิโกกุ ฟุกุโอกะ ฮอกไกโด และโอกินาว่า{L}",
       "all_festivals": "เทศกาลและงานตามฤดูกาลในญี่ปุ่นเดือน{m}{L} วันที่ สถานที่ และวิธีเที่ยว",
       "all_food": "อาหารแนะนำและอาหารท้องถิ่นที่ต้องลองในแต่ละภูมิภาคของญี่ปุ่น{L}",
       "all_transport": "วิธีเดินทางจากสนามบินเข้าเมือง การเดินทางระหว่างเมือง และคู่มือบัตรโดยสารอย่าง Suica และ ICOCA",
       "all_shopping": "ถนนช้อปปิ้งและตลาดในญี่ปุ่น ระบบปลอดภาษีใหม่ ของขึ้นชื่อและของฝากแต่ละภูมิภาค{L}"},
 "L": " – {n} และอื่น ๆ"}
PT_TH = {"spot": "{n} – ค่าเข้าชม เวลาเปิด และการเดินทาง ({a})", "fest": "{n} – วันที่ สถานที่ และเคล็ดลับ ({a})",
         "shop": "{n} – ของน่าซื้อและการเดินทาง ({a})", "food": "{n} – อาหารขึ้นชื่อของ{a}และที่กิน"}
IT_TH = {"about": "เกี่ยวกับเรา", "contact": "ติดต่อ", "privacy": "นโยบายความเป็นส่วนตัว",
         "d": "เกี่ยวกับ Go Nihon Trip แหล่งข้อมูล วิธีติดต่อ และนโยบายความเป็นส่วนตัว"}
IM_TH = ["แผนเที่ยวญี่ปุ่นแนะนำ – โตเกียว โอซาก้า เกียวโต ฟุกุโอกะ ฮอกไกโด โอกินาว่า", "{t} – แผนเที่ยวแนะนำ",
         "แผนเที่ยวหลายวันในโตเกียว โอซาก้า เกียวโต นาโกย่า ฮิโรชิม่า ชิโกกุ ฟุกุโอกะ ฮอกไกโด และโอกินาว่า พร้อมเส้นทางรายวันและค่าเข้าชม"]
DESC_TH = "ที่เที่ยว เทศกาล ร้านอาหาร การเดินทาง และช้อปปิ้งในโตเกียว โอซาก้า นาโกย่า ฮิโรชิม่า ชิโกกุ ฟุกุโอกะ ฮอกไกโด โอกินาว่า และเมืองใกล้เคียง พร้อมสภาพอากาศสด"
CSS_TH = 'html:lang(th){--f-body:"Noto Sans Thai","Leelawadee UI","Thonburi","Tahoma",system-ui,sans-serif;--f-display:"Noto Serif Thai","Noto Sans Thai","Leelawadee UI",serif}\n'

R = [  # (old, new) — 찾지 못하면 그 파일에선 건너뜀
 ('var ok=["en","ja","es","fr","zh","tw"], l=null;', 'var ok=["en","ja","es","fr","zh","tw","th"], l=null;'),
 ('fr:"Sites, fêtes, restaurants, transports et shopping à Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa et dans les villes voisines, avec la météo en direct.",zh:',
  'fr:"Sites, fêtes, restaurants, transports et shopping à Tokyo, Osaka, Nagoya, Hiroshima, Shikoku, Fukuoka, Hokkaido, Okinawa et dans les villes voisines, avec la météo en direct.",th:' + J(DESC_TH) + ',zh:'),
 ('zh:"zh_CN",tw:"zh_TW"}[I.lang]', 'zh:"zh_CN",tw:"zh_TW",th:"th_TH"}[I.lang]'),
 ('l==="tw"?"zh-TW":"en-US"', 'l==="tw"?"zh-TW":l==="th"?"th-TH":"en-US"'),
 ('if(l==="tw") return n+"日圓"+(from?"起":"");', 'if(l==="tw") return n+"日圓"+(from?"起":""); if(l==="th") return (from?"ตั้งแต่ ":"")+n+" เยน";'),
 (',fr:["janv."', ',th:["ม.ค.","ก.พ.","มี.ค.","เม.ย.","พ.ค.","มิ.ย.","ก.ค.","ส.ค.","ก.ย.","ต.ค.","พ.ย.","ธ.ค."],fr:["janv."'),
 ('l==="tw"?`（最後入場${x}）`:', 'l==="tw"?`（最後入場${x}）`:l==="th"?` (เข้าครั้งสุดท้าย ${x})`:'),
 ('l==="tw"?`每月第${c.n}個${w}`:', 'l==="tw"?`每月第${c.n}個${w}`:l==="th"?`${w}ที่ ${c.n} ของทุกเดือน`:'),
 ('(l==="zh"||l==="tw")?`${n}晚${n+1}天`:', '(l==="zh"||l==="tw")?`${n}晚${n+1}天`:l==="th"?`${n} คืน ${n+1} วัน`:'),
 ('(l==="zh"||l==="tw")?`第${i}天`:', '(l==="zh"||l==="tw")?`第${i}天`:l==="th"?`วันที่ ${i}`:'),
 ('l==="tw"?`${n}個地點`:', 'l==="tw"?`${n}個地點`:l==="th"?`${n} แห่ง`:'),
 ('p = p.replace(/^(en|ja|es|fr|zh|tw)(\\/|$)/,"");', 'p = p.replace(/^(en|ja|es|fr|zh|tw|th)(\\/|$)/,"");'),
 ('fr:"Japon",zh:"日本",tw:"日本"}[L];', 'fr:"Japon",zh:"日本",tw:"日本",th:"ญี่ปุ่น"}[L];'),
 ('["tw","繁","繁體中文"],', '["tw","繁","繁體中文"],["th","TH","ไทย"],'),
 ('tw:["門票","開放","交通","推薦"]}[L]', 'tw:["門票","開放","交通","推薦"],th:["ค่าเข้าชม","เวลาเปิด","การเดินทาง","ของน่าซื้อ"]}[L]'),
 ('html:lang(ja){--f-body:', CSS_TH + 'html:lang(ja){--f-body:'),
 ('html:lang(fr) .mcats,html:lang(ja) .mcats{', 'html:lang(fr) .mcats,html:lang(th) .mcats,html:lang(ja) .mcats{'),
 # 소개 페이지: 지원 언어에 태국어 추가
 ('한국어·영어·일본어·중국어·스페인어·프랑스어로 제공해요.', '한국어·영어·일본어·중국어·태국어·스페인어·프랑스어로 제공해요.'),
 # gen.py
 ("LANGS = ['ko', 'en', 'ja', 'zh', 'tw', 'es', 'fr']", "LANGS = ['ko', 'en', 'ja', 'zh', 'tw', 'th', 'es', 'fr']"),
 ("'zh': 'zh_CN', 'tw': 'zh_TW'}", "'zh': 'zh_CN', 'tw': 'zh_TW', 'th': 'th_TH'}"),
 ("    'fr': 'Sites, fêtes", f"    'th': {DESC_TH!r},\n    'fr': 'Sites, fêtes"),
 ('(en|ja|zh|tw|es|fr)', '(en|ja|zh|tw|th|es|fr)'),
 ('(ko|en|ja|zh|tw|es|fr)', '(ko|en|ja|zh|tw|th|es|fr)'),
]

def patch_meta(s):
    a = ' /*PMETA_ZH_DONE*/'
    if a in s and 'PMETA_TH_DONE' not in s:
        s = s.replace(a, ',th:' + J(PMETA_TH) + ' /*PMETA_TH_DONE*/' + a, 1)
    a = '"food":"{n} – {a}鄉土料理和品嚐地點"}};'
    if a in s and '"food":"{n} – อาหารขึ้นชื่อ' not in s:
        s = s.replace(a, a[:-2] + ',th:' + J(PT_TH) + '};', 1)
    a = '"d":"Go Nihon Trip網站介紹、資訊來源、聯絡方式與隱私政策。"}}'
    if a in s:
        s = s.replace(a, a[:-1] + ',th:' + J(IT_TH) + '}', 1)
    a = '每日路線和門票一目瞭然。"]}'
    if a in s:
        s = s.replace(a, a[:-1] + ',th:' + J(IM_TH) + '}', 1)
    return s

W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html',
         f'{W}/sitegen/spot_info_view.js', f'{W}/i18n_work/backup/spot_info_view.pre.js',
         f'{W}/sitegen/itin_view.js', f'{W}/sitegen/map_view.js', f'{W}/sitegen/gen.py']
if __name__ == '__main__':
    for f in FILES:
        if not os.path.exists(f): print('missing', f); continue
        s = open(f, encoding='utf-8').read(); n = 0
        for a, b in R:
            if a in s and b not in s:
                s = s.replace(a, b); n += 1
        s2 = patch_meta(s); n += s2 != s; s = s2
        open(f, 'w', encoding='utf-8').write(s)
        print(f.split('/')[-1], n, 'changes')
