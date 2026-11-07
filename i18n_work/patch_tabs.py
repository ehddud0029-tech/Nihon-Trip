# 페이지 안 탭(하위 페이지) 공통: 숙소(전체·도시), 술 전체, 날씨 도시, 공항 페이지 (2026-11)
# - st.sub: 지금 탭. 주소 끝에 붙어요: stay/hotels/, osaka/stay/booking/, drink/types/, tokyo/weather/outfit/, airport/kix/faq/ …
# - 탭 막대 subTabs(), 주소 읽기·만들기, 탭 클릭, 메뉴·다른 링크 누르면 첫 탭, 탭별 검색 제목(subMeta)
# 화면은 각 *_view.js가 그려요(st.sub 사용). html·backup pre에 같이 적용 (여러 번 돌려도 안전)
import json, os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from s2tw import s2tw
from patch_weather import block
W = '/home/claude'
FILES = [f'{W}/tabishiori.html', f'{W}/i18n_work/backup/tabishiori.pre.html']
SM = {
 'ko': {"stay:i:hotels": ["일본 추천 숙소 – 지역별 역 가까운 호텔 모음", "도쿄·오사카·후쿠오카·홋카이도·오키나와 등 지역별로 역이 가깝고 평이 좋은 추천 숙소를 모았어요."],
        "stay:i:booking": ["일본 숙소 예약 방법 – 예약 사이트 고르기와 확인할 점", "아고다·부킹닷컴·라쿠텐 트래블·에어비앤비 등 예약 사이트 고르는 법, 무료 취소·숙박세·체크인 시간 등 예약 전에 확인할 점을 정리했어요."],
        "stay:c:hotels": ["{a} 추천 숙소 – 역 가까운 호텔", "{a}에서 역이 가깝고 이동이 편한 추천 숙소를 모았어요. 동네와 가까운 역도 함께 보여 드려요."],
        "stay:c:booking": ["{a} 숙소 예약 방법과 확인할 점", "{a} 숙소를 예약할 때 쓰기 좋은 사이트와 무료 취소·숙박세·체크인 시간 등 확인할 점을 정리했어요."],
        "drink:i:types": ["일본 술 종류와 사케 라벨 읽는 법 – 주문할 때 알아 둘 말", "사케·소주·아와모리·맥주·위스키·우메슈의 차이, 준마이·긴조 등 사케 라벨 읽는 법과 이자카야에서 주문할 때 알아 둘 말을 정리했어요."],
        "drink:i:visit": ["일본 양조장·증류소 견학 팁 – 예약·시음·나이 제한", "일본 양조장·증류소 견학 전에 알아 둘 예약 방법, 시음 나이 제한, 운전자 시음 규칙을 정리했어요."],
        "drink:i:carry": ["일본 술 가지고 오는 법 – 면세 한도와 비행기 규칙", "일본 술을 가지고 올 때 면세 한도, 비행기에 실을 수 있는 양과 도수, 깨지지 않게 싸는 법을 정리했어요."],
        "weather:c:outfit": ["{a} 월별 옷차림 – 1월부터 12월까지 뭘 입을까", "{a}의 1월부터 12월까지 평균 기온에 맞춘 추천 옷차림과 챙기면 좋은 것을 정리했어요."],
        "weather:c:faq": ["{a} 날씨 자주 묻는 질문 – 가장 더운 달·추운 달·비 많은 달", "{a}에서 가장 더운 달과 추운 달, 비가 가장 많이 오는 달, 여행하기 좋은 달을 기상청 평년값으로 정리했어요."],
        "airport:a:all": ["{ap}에서 시내 가는 모든 방법 비교 – 기차·버스·걸리는 시간", "{ap}에서 시내와 관광지까지 갈 수 있는 기차·버스를 한눈에 비교하고, 걸리는 시간을 정리했어요."],
        "airport:a:faq": ["{ap} 교통 자주 묻는 질문 – 시내까지 걸리는 시간과 교통카드", "{ap}에서 시내·관광지까지 얼마나 걸리는지, 교통카드는 어디서 사는지 정리했어요."]},
 'en': {"stay:i:hotels": ["Recommended Hotels in Japan – Near-Station Picks by Region", "Recommended hotels close to stations in Tokyo, Osaka, Fukuoka, Hokkaido, Okinawa and more."],
        "stay:i:booking": ["How to Book Hotels in Japan – Booking Sites and What to Check", "How to choose between Agoda, Booking.com, Rakuten Travel and Airbnb, plus free cancellation, accommodation tax and check-in times."],
        "stay:c:hotels": ["Recommended Hotels in {a} – Close to Stations", "Recommended hotels in {a} that are close to stations and easy to get around from, with the nearest area and station."],
        "stay:c:booking": ["How to Book a Hotel in {a} – What to Check", "The best sites for booking in {a}, and what to check: free cancellation, accommodation tax and check-in times."],
        "drink:i:types": ["Types of Japanese Alcohol & How to Read a Sake Label", "The difference between sake, shochu, awamori, beer, whisky and umeshu, how to read junmai and ginjo labels, and words for ordering at an izakaya."],
        "drink:i:visit": ["Tips for Visiting Japanese Breweries & Distilleries", "Booking, tasting age limits and rules for drivers when you tour a brewery or distillery in Japan."],
        "drink:i:carry": ["Taking Japanese Alcohol Home – Allowances & Flight Rules", "Duty-free allowances, how much and how strong alcohol you can take on a plane, and how to pack bottles so they don't break."],
        "weather:c:outfit": ["What to Wear in {a} by Month – January to December", "Recommended clothing for each month in {a} based on average temperatures, plus what to pack."],
        "weather:c:faq": ["{a} Weather FAQ – Hottest, Coldest & Rainiest Months", "The hottest, coldest and rainiest months in {a} and the best months to visit, based on JMA climate normals."],
        "airport:a:all": ["All Ways from {ap} to the City – Trains, Buses & Times", "Compare every train and bus from {ap} to the city and major sights, with travel times."],
        "airport:a:faq": ["{ap} Transport FAQ – Travel Times & IC Cards", "How long it takes from {ap} to the city and sights, and where to buy an IC card."]},
 'ja': {"stay:i:hotels": ["日本のおすすめホテル – 地域別・駅近の宿", "東京・大阪・福岡・北海道・沖縄など地域別に、駅に近いおすすめの宿をまとめました。"],
        "stay:i:booking": ["日本の宿の予約方法 – 予約サイトの選び方と確認ポイント", "アゴダ・Booking.com・楽天トラベル・Airbnbなど予約サイトの選び方と、無料キャンセル・宿泊税・チェックイン時間など予約前の確認ポイント。"],
        "stay:c:hotels": ["{a}のおすすめホテル – 駅近の宿", "{a}で駅に近く移動しやすいおすすめの宿をまとめました。エリアと最寄り駅も紹介します。"],
        "stay:c:booking": ["{a}の宿の予約方法と確認ポイント", "{a}の宿を予約するときに便利なサイトと、無料キャンセル・宿泊税・チェックイン時間などの確認ポイント。"],
        "drink:i:types": ["日本のお酒の種類と日本酒ラベルの読み方 – 注文で使う言葉", "日本酒・焼酎・泡盛・ビール・ウイスキー・梅酒の違い、純米・吟醸などラベルの読み方、居酒屋で注文するときの言葉をまとめました。"],
        "drink:i:visit": ["酒蔵・蒸溜所見学のコツ – 予約・試飲・年齢制限", "日本の酒蔵や蒸溜所を見学する前に知っておきたい予約方法、試飲の年齢制限、運転する人のルール。"],
        "drink:i:carry": ["日本のお酒の持ち帰り方 – 免税範囲と飛行機のルール", "お酒を持ち帰るときの免税範囲、飛行機に載せられる量と度数、割れないように包むコツ。"],
        "weather:c:outfit": ["{a}の月別の服装 – 1月から12月まで何を着る？", "{a}の1月から12月までの平均気温に合わせたおすすめの服装と、持っていくと便利なもの。"],
        "weather:c:faq": ["{a}の天気よくある質問 – 一番暑い月・寒い月・雨が多い月", "{a}で一番暑い月と寒い月、雨が多い月、旅行におすすめの月を気象庁の平年値でまとめました。"],
        "airport:a:all": ["{ap}から市内へのすべての行き方比較 – 電車・バス・所要時間", "{ap}から市内や観光地へ行ける電車・バスを一覧で比較し、所要時間をまとめました。"],
        "airport:a:faq": ["{ap}の交通よくある質問 – 市内までの所要時間と交通系IC", "{ap}から市内・観光地までの所要時間と、交通系ICカードを買える場所。"]},
 'es': {"stay:i:hotels": ["Hoteles recomendados en Japón – Cerca de la estación, por región", "Hoteles recomendados cerca de estaciones en Tokio, Osaka, Fukuoka, Hokkaido, Okinawa y más."],
        "stay:i:booking": ["Cómo reservar alojamiento en Japón – Webs de reserva y qué revisar", "Cómo elegir entre Agoda, Booking.com, Rakuten Travel y Airbnb, y qué revisar: cancelación gratuita, impuesto de alojamiento y horario de entrada."],
        "stay:c:hotels": ["Hoteles recomendados en {a} – Cerca de la estación", "Hoteles recomendados en {a} cerca de estaciones y bien comunicados, con la zona y la estación más cercana."],
        "stay:c:booking": ["Cómo reservar hotel en {a} – Qué revisar", "Las mejores webs para reservar en {a} y qué revisar: cancelación gratuita, impuesto de alojamiento y horario de entrada."],
        "drink:i:types": ["Tipos de alcohol japonés y cómo leer una etiqueta de sake", "Diferencias entre sake, shochu, awamori, cerveza, whisky y umeshu, cómo leer etiquetas junmai y ginjo, y palabras para pedir en un izakaya."],
        "drink:i:visit": ["Consejos para visitar bodegas y destilerías en Japón", "Reservas, edad mínima para catar y normas para conductores al visitar una bodega o destilería en Japón."],
        "drink:i:carry": ["Llevar alcohol japonés a casa – Franquicias y normas de vuelo", "Franquicias, cuánto alcohol y de qué graduación puedes llevar en el avión, y cómo envolver las botellas."],
        "weather:c:outfit": ["Qué ropa llevar en {a} por mes – De enero a diciembre", "Ropa recomendada para cada mes en {a} según la temperatura media, y qué llevar en la maleta."],
        "weather:c:faq": ["Preguntas sobre el tiempo en {a} – Meses más cálidos, fríos y lluviosos", "Los meses más cálidos, fríos y lluviosos de {a} y los mejores para viajar, según los valores normales de la JMA."],
        "airport:a:all": ["Todas las formas de ir de {ap} a la ciudad – Trenes, autobuses y tiempos", "Compara todos los trenes y autobuses de {ap} a la ciudad y los principales lugares, con tiempos de viaje."],
        "airport:a:faq": ["Preguntas sobre transporte en {ap} – Tiempos y tarjetas IC", "Cuánto se tarda de {ap} a la ciudad y dónde comprar una tarjeta IC."]},
 'fr': {"stay:i:hotels": ["Hôtels recommandés au Japon – Près des gares, par région", "Hôtels recommandés près des gares à Tokyo, Osaka, Fukuoka, Hokkaido, Okinawa et ailleurs."],
        "stay:i:booking": ["Réserver un hébergement au Japon – Sites et points à vérifier", "Comment choisir entre Agoda, Booking.com, Rakuten Travel et Airbnb, et quoi vérifier : annulation gratuite, taxe de séjour et heure d'arrivée."],
        "stay:c:hotels": ["Hôtels recommandés à {a} – Près des gares", "Hôtels recommandés à {a}, près des gares et bien desservis, avec le quartier et la gare la plus proche."],
        "stay:c:booking": ["Réserver un hôtel à {a} – Points à vérifier", "Les meilleurs sites pour réserver à {a} et quoi vérifier : annulation gratuite, taxe de séjour et heure d'arrivée."],
        "drink:i:types": ["Types d'alcool japonais et lecture d'une étiquette de saké", "Différences entre saké, shochu, awamori, bière, whisky et umeshu, lecture des étiquettes junmai et ginjo, et mots utiles pour commander en izakaya."],
        "drink:i:visit": ["Conseils pour visiter brasseries et distilleries au Japon", "Réservation, âge minimum pour déguster et règles pour les conducteurs lors d'une visite au Japon."],
        "drink:i:carry": ["Rapporter de l'alcool japonais – Franchises et règles en avion", "Franchises, quantité et degré d'alcool autorisés en avion, et comment emballer les bouteilles."],
        "weather:c:outfit": ["Comment s'habiller à {a} selon le mois – De janvier à décembre", "Tenues conseillées pour chaque mois à {a} selon les températures moyennes, et quoi emporter."],
        "weather:c:faq": ["Questions sur la météo à {a} – Mois les plus chauds, froids et pluvieux", "Les mois les plus chauds, froids et pluvieux à {a} et les meilleurs pour voyager, d'après les normales de la JMA."],
        "airport:a:all": ["Tous les trajets de {ap} vers la ville – Trains, bus et durées", "Comparez tous les trains et bus de {ap} vers la ville et les principaux sites, avec les temps de trajet."],
        "airport:a:faq": ["Questions sur les transports à {ap} – Durées et cartes IC", "Combien de temps de {ap} vers la ville et où acheter une carte IC."]},
 'zh': {"stay:i:hotels": ["日本推荐住宿 – 各地区车站附近的酒店", "按地区整理了东京、大阪、福冈、北海道、冲绳等地靠近车站的推荐住宿。"],
        "stay:i:booking": ["日本住宿预订方法 – 预订网站怎么选与注意事项", "整理了Agoda、Booking.com、乐天旅行、Airbnb等预订网站的选择方法，以及免费取消、住宿税、入住时间等注意事项。"],
        "stay:c:hotels": ["{a}推荐住宿 – 车站附近的酒店", "整理了{a}靠近车站、交通方便的推荐住宿，并附上区域和最近的车站。"],
        "stay:c:booking": ["{a}住宿预订方法与注意事项", "整理了预订{a}住宿时好用的网站，以及免费取消、住宿税、入住时间等注意事项。"],
        "drink:i:types": ["日本酒类种类与清酒酒标的看法 – 点酒时要知道的词", "整理了清酒、烧酒、泡盛、啤酒、威士忌、梅酒的区别，纯米、吟酿等酒标的看法，以及在居酒屋点酒时要知道的词。"],
        "drink:i:visit": ["日本酒藏·蒸馏所参观小贴士 – 预约·试饮·年龄限制", "整理了参观日本酒藏和蒸馏所前要知道的预约方法、试饮年龄限制和开车者的规定。"],
        "drink:i:carry": ["日本酒带回国的方法 – 免税额度与航空规定", "整理了带酒回国时的免税额度、可带上飞机的数量和度数，以及防止破碎的包装方法。"],
        "weather:c:outfit": ["{a}每月穿搭 – 1月到12月穿什么", "根据{a}1月到12月的平均气温整理了推荐穿搭和需要准备的物品。"],
        "weather:c:faq": ["{a}天气常见问题 – 最热·最冷·雨最多的月份", "根据日本气象厅平年值整理了{a}最热、最冷、雨最多的月份和适合旅行的月份。"],
        "airport:a:all": ["{ap}到市区所有交通方式比较 – 电车·巴士·所需时间", "一次比较从{ap}到市区和主要景点的电车与巴士，并整理所需时间。"],
        "airport:a:faq": ["{ap}交通常见问题 – 到市区的时间与交通卡", "整理了从{ap}到市区和景点需要多长时间，以及在哪里买交通卡。"]},
 'th': {"stay:i:hotels": ["ที่พักแนะนำในญี่ปุ่น – โรงแรมใกล้สถานีแยกตามภูมิภาค", "รวมที่พักแนะนำใกล้สถานีในโตเกียว โอซาก้า ฟุกุโอกะ ฮอกไกโด โอกินาว่า และที่อื่น ๆ"],
        "stay:i:booking": ["วิธีจองที่พักในญี่ปุ่น – เลือกเว็บจองและสิ่งที่ต้องเช็ก", "วิธีเลือกระหว่าง Agoda, Booking.com, Rakuten Travel และ Airbnb พร้อมสิ่งที่ต้องเช็ก เช่น ยกเลิกฟรี ภาษีที่พัก และเวลาเช็กอิน"],
        "stay:c:hotels": ["ที่พักแนะนำใน{a} – โรงแรมใกล้สถานี", "รวมที่พักแนะนำใน{a} ที่ใกล้สถานีและเดินทางสะดวก พร้อมย่านและสถานีที่ใกล้ที่สุด"],
        "stay:c:booking": ["วิธีจองที่พักใน{a}และสิ่งที่ต้องเช็ก", "เว็บที่เหมาะสำหรับจองที่พักใน{a} และสิ่งที่ต้องเช็ก เช่น ยกเลิกฟรี ภาษีที่พัก และเวลาเช็กอิน"],
        "drink:i:types": ["ประเภทเหล้าญี่ปุ่นและวิธีอ่านฉลากสาเก – คำที่ควรรู้ตอนสั่ง", "ความต่างของสาเก โชจู อาวาโมริ เบียร์ วิสกี้ และอุเมะชุ วิธีอ่านฉลากจุนไมและกินโจ และคำที่ควรรู้ตอนสั่งในอิซากายะ"],
        "drink:i:visit": ["เคล็ดลับเที่ยวชมโรงสาเกและโรงกลั่นในญี่ปุ่น – จอง ชิม และอายุ", "วิธีจอง ข้อจำกัดอายุในการชิม และกฎสำหรับคนขับรถเมื่อเที่ยวชมโรงสาเกหรือโรงกลั่นในญี่ปุ่น"],
        "drink:i:carry": ["การนำเหล้าญี่ปุ่นกลับบ้าน – วงเงินปลอดภาษีและกฎบนเครื่องบิน", "วงเงินปลอดภาษี ปริมาณและดีกรีที่นำขึ้นเครื่องได้ และวิธีห่อขวดไม่ให้แตก"],
        "weather:c:outfit": ["การแต่งตัวใน{a}รายเดือน – มกราคมถึงธันวาคม", "การแต่งตัวที่แนะนำในแต่ละเดือนของ{a} ตามอุณหภูมิเฉลี่ย พร้อมของที่ควรเตรียม"],
        "weather:c:faq": ["คำถามเรื่องอากาศใน{a} – เดือนที่ร้อนที่สุด หนาวที่สุด ฝนมากที่สุด", "เดือนที่ร้อนที่สุด หนาวที่สุด ฝนตกมากที่สุด และเดือนที่เหมาะกับการเที่ยวใน{a} ตามค่าปกติของกรมอุตุนิยมวิทยาญี่ปุ่น"],
        "airport:a:all": ["ทุกวิธีเดินทางจาก{ap}เข้าเมือง – รถไฟ รถบัส และเวลา", "เปรียบเทียบรถไฟและรถบัสทั้งหมดจาก{ap}เข้าเมืองและสถานที่สำคัญ พร้อมเวลาเดินทาง"],
        "airport:a:faq": ["คำถามเรื่องการเดินทางที่{ap} – เวลาเข้าเมืองและบัตร IC", "ใช้เวลาเท่าไรจาก{ap}เข้าเมืองและไปสถานที่ท่องเที่ยว และซื้อบัตร IC ได้ที่ไหน"]},
}
SM['tw'] = {k: [s2tw(x) for x in v] for k, v in SM['zh'].items()}
CORE = """/*SUBTAB_BEGIN*/
function subOk(s){
  const t=s.sub; if(!t) return "";
  if(s.view==="stay") return (t==="booking"||(t==="hotels"&&typeof stayShowHotels==="function"&&stayShowHotels()))?t:"";
  if(s.view==="drink") return !DRINK_CITIES.includes(s.city)&&["types","visit","carry"].includes(t)?t:"";
  if(s.view==="weather") return WXN[s.city]&&s.city!=="all"&&!(s.wm>=1&&s.wm<=12)&&["outfit","faq"].includes(t)?t:"";
  if(s.view==="airport") return APS[s.ap]&&!(s.apk&&apOpts(s.ap,s.apk).length)&&["all","faq"].includes(t)?t:"";
  return "";
}
function subFromSeg(seg){
  const n=seg.length, l=seg[n-1];
  if(seg[0]==="stay"&&n===2&&["hotels","booking"].includes(l)) return l;
  if(CITIES[seg[0]]&&seg[1]==="stay"&&n===3&&["hotels","booking"].includes(l)) return l;
  if(seg[0]==="drink"&&n===2&&["types","visit","carry"].includes(l)) return l;
  if(CITIES[seg[0]]&&seg[1]==="weather"&&n===3&&["outfit","faq"].includes(l)) return l;
  if(seg[0]==="airport"&&n===3&&APS[seg[1]]&&["all","faq"].includes(l)) return l;
  return "";
}
function subTabs(list,cur){
  return `<nav class="dtabs sbtabs">${list.map(([k,l])=>`<a href="${ROUTED?window.NT_BASE+LPRE+pathOf({...st,sub:k}):"#"}" data-subtab="${k}"${k===cur?' class="on" aria-current="page"':""}>${esc(l)}</a>`).join("")}</nav>`;
}
function subMeta(){
  if(!subOk(st)) return null;
  const L=(window.I18N&&window.I18N.lang)||"ko", T=window.__tr||(x=>x), all=(""" + json.dumps(SM, ensure_ascii=False, separators=(',', ':')) + """), M=all[L]||all.ko;
  const f=(s,o)=>s.replace(/\\{(\\w+)\\}/g,(_,k)=>o[k]!=null?o[k]:"");
  let key, o={};
  if(st.view==="stay"){ const c=STAY_CITIES.includes(st.city)?st.city:""; key=`stay:${c?"c":"i"}:${st.sub}`; if(c) o.a=T(CITIES[c].ko); }
  else if(st.view==="drink") key=`drink:i:${st.sub}`;
  else if(st.view==="weather"){ key=`weather:c:${st.sub}`; o.a=T(CITIES[st.city].ko); }
  else if(st.view==="airport"){ key=`airport:a:${st.sub}`; o.ap=T(apName(st.ap)); }
  const m=M[key]; if(!m) return null;
  return {title:f(m[0],o)+" | Go Nihon Trip", desc:f(m[1],o)};
}
/*SUBTAB_END*/
"""
R = [
 # 주소 만들기: INFO_VIEWS 줄 뒤에 (patch_info 규칙을 깨지 않게)
 ('  if(INFO_VIEWS.includes(s.view)) return s.view+"/";\n',
  '  if(INFO_VIEWS.includes(s.view)) return s.view+"/";\n  if(!s.__sb){ const sb=subOk(s); if(sb) return pathOf({...s,__sb:1})+sb+"/"; }\n'),
 # 주소 읽기
 ('  const seg = p.split("/").filter(Boolean).map(decodeURIComponent);\n',
  '  const seg = p.split("/").filter(Boolean).map(decodeURIComponent);\n  st.sub=subFromSeg(seg); if(st.sub) seg.pop();\n'),
 # 탭 클릭 + 다른 화면 링크는 그 링크의 탭(data-sub, 없으면 첫 탭)으로
 ('  const wxl = e.target.closest("[data-wxc]");',
  '  const sbt = e.target.closest("[data-subtab]"); if(sbt){ e.preventDefault(); st.sub=sbt.dataset.subtab; render(); window.scrollTo({top:0}); return; }\n  { const sl = e.target.closest("[data-wxc],[data-apa],[data-stayc],[data-drc]"); if(sl) st.sub = sl.dataset.sub||""; }\n  const wxl = e.target.closest("[data-wxc]");'),
 # 메뉴 이동은 첫 탭
 ('  st.view=view; st.q="";\n', '  st.view=view; st.q=""; st.sub="";\n'),
 # 탭별 검색 제목
 ('  const pm = pageMeta();', '  const pm = subMeta() || pageMeta();'),
]
CSS = """/*SBCSS_BEGIN*/
.sbtabs{margin:16px 0 14px}
@media (max-width:599px){.sbtabs a{padding:8px 11px;font-size:14px}}
/*SBCSS_END*/
"""
def patch(s):
    s = block(s, '/*SUBTAB_BEGIN*/', '/*SUBTAB_END*/', CORE, 'V.place = function(){')
    s = block(s, '/*SBCSS_BEGIN*/', '/*SBCSS_END*/', CSS, 'footer{border-top:1px solid var(--line);')
    for a, b in R:
        if b in s: continue
        assert s.count(a) == 1, (a[:60], s.count(a))
        s = s.replace(a, b)
    return s
if __name__ == '__main__':
    for f in FILES:
        s = patch(open(f, encoding='utf-8').read())
        open(f, 'w', encoding='utf-8').write(s); print('patched', f)
