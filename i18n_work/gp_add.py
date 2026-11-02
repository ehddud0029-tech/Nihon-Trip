"""AutoReserve 목록이 없는 지역의 구글 지도 기준 추천 가게 (2026년 11월 2일 정리)
- 여러 맛집 소개 글(mapple 등)에 함께 오르는 오래되고 유명한 가게만 골랐어요. 별점·리뷰는 저장하지 않아요.
- 가게: (한국어 이름, 일본어 이름, 영어 이름, 구글 지도 검색어, 대표 메뉴 X(...), 특징 X(...), 예산)
region_inject.py 가 읽어 autoreserve.js(AR_SLUG) · google_picks.js 에 넣고, 번역 줄을 tr_35 · zh_35 · arnames_5 로 내보내요."""

TR, ZH, NAMES = {}, {}, []
def X(ko, en, ja, es, fr, zh):
    TR[ko] = (ko, en, ja, es, fr); ZH[ko] = zh
    return ko
def S(ko, ja, en, q, dish, feat, b):
    NAMES.append((ko, ja, en))
    return [ko, q, dish, feat, b]

HOTO = X("호토", "Hoto noodles", "ほうとう", "Hoto", "Hoto", "馎饦")
YOSHIDA = X("요시다 우동", "Yoshida udon", "吉田のうどん", "Udon de Yoshida", "Udon de Yoshida", "吉田乌冬")
YUDOFU = X("유도후 코스", "Yudofu course", "湯豆腐コース", "Menú de yudofu", "Menu yudofu", "汤豆腐套餐")
PARFAIT = X("말차 파르페", "Matcha parfait", "抹茶パフェ", "Parfait de matcha", "Parfait au matcha", "抹茶芭菲")

FUJI = {
 "local": [
  S("호토 후도 히가시코이지점", "名物ほうとう不動 東恋路店", "Hoto Fudo Higashi-Koiji", "ほうとう不動 東恋路店 河口湖", HOTO, X("구름 모양 건물, 메뉴는 호토 한 가지", "Cloud-shaped building; hoto is the only dish", "雲の形の建物、メニューはほうとう一品", "Edificio con forma de nube; solo sirven hoto", "Bâtiment en forme de nuage ; un seul plat, le hoto", "云朵造型建筑，只卖馎饦一道菜"), "¥1,000~¥2,000"),
  S("고사쿠 가와구치코점", "甲州ほうとう 小作 河口湖店", "Kosaku Kawaguchiko", "小作 河口湖店", X("호박 호토", "Pumpkin hoto", "かぼちゃほうとう", "Hoto de calabaza", "Hoto au potiron", "南瓜馎饦"), X("호토 종류가 10가지쯤 되는 큰 가게", "Big restaurant with about ten kinds of hoto", "ほうとうが10種類ほどある大型店", "Local grande con unos diez tipos de hoto", "Grande adresse avec une dizaine de hoto", "有约10种馎饦的大型店"), "¥1,000~¥2,000"),
  S("아사마 차야 본점", "浅間茶屋 本店", "Sengen Chaya Honten", "浅間茶屋 本店 富士吉田", X("버섯 호토", "Mushroom hoto", "きのこほうとう", "Hoto de setas", "Hoto aux champignons", "蘑菇馎饦"), X("후지요시다의 호토·정식 가게", "Hoto and set meals in Fujiyoshida", "富士吉田のほうとう・定食の店", "Hoto y menús en Fujiyoshida", "Hoto et menus à Fujiyoshida", "富士吉田的馎饦·定食店"), "¥1,000~¥2,000"),
  S("미우라 우동", "みうらうどん", "Miura Udon", "みうらうどん 富士吉田", YOSHIDA, X("고기 우동이 대표인 수타 우동집", "Homemade noodles; meat udon is the signature", "手打ち麺、肉うどんが看板", "Fideos caseros; el udon con carne es la estrella", "Nouilles maison ; l'udon à la viande est la spécialité", "手打面，招牌是肉乌冬"), "~¥1,000"),
  S("멘쿄카이덴", "麺許皆伝", "Menkyo Kaiden", "麺許皆伝 富士吉田", YOSHIDA, X("토핑을 듬뿍 올린 '욕심쟁이 우동'", "'Greedy udon' piled with toppings", "具だくさんの「欲ばりうどん」", "'Udon codicioso' con montones de ingredientes", "« Udon gourmand » couvert de garnitures", "配料满满的“贪心乌冬”"), "~¥1,000"),
 ]}
FUJI["all"] = FUJI["local"]

KYOTOEKI = {
 "ramen": [
  S("혼케 다이이치아사히 다카바시 본점", "本家 第一旭 たかばし本店", "Honke Daiichi Asahi Takabashi", "本家 第一旭 たかばし本店", X("교토 쇼유 라멘", "Kyoto shoyu ramen", "京都醤油ラーメン", "Ramen de soja de Kioto", "Ramen au soja de Kyoto", "京都酱油拉面"), X("교토역 도보 5분, 줄 서는 노포", "5 min walk from Kyoto Sta.; a long-standing shop with queues", "京都駅から徒歩5分、行列の老舗", "A 5 min de la estación; clásico con cola", "À 5 min de la gare ; adresse historique avec file d'attente", "京都站步行5分钟，排队老店"), "~¥1,000"),
  S("신푸쿠사이칸 본점", "新福菜館 本店", "Shinpuku Saikan Honten", "新福菜館 本店 京都", X("검은 국물 쇼유 라멘·야키메시", "Dark shoyu ramen and fried rice", "黒い醤油ラーメン・ヤキメシ", "Ramen de soja oscuro y arroz frito", "Ramen au soja foncé et riz sauté", "黑汤酱油拉面·炒饭"), X("다이이치아사히 바로 옆 노포", "Old-timer right next to Daiichi Asahi", "第一旭のすぐ隣の老舗", "Veterano justo al lado de Daiichi Asahi", "Adresse historique juste à côté de Daiichi Asahi", "第一旭隔壁的老店"), "~¥1,000"),
  S("교토 라멘 고지", "京都拉麺小路", "Kyoto Ramen Koji", "京都拉麺小路 京都駅", X("전국 유명 라멘", "Famous ramen from around Japan", "全国の有名ラーメン", "Ramen famosos de todo Japón", "Ramens célèbres de tout le Japon", "日本各地名店拉面"), X("교토역 빌딩 10층 라멘 골목", "Ramen alley on the 10th floor of Kyoto Station Building", "京都駅ビル10階のラーメン街", "Callejón del ramen en la 10.ª planta del edificio de la estación", "Allée des ramens au 10e étage de la gare de Kyoto", "京都站大楼10楼的拉面街"), "~¥1,500"),
 ]}
KYOTOEKI["all"] = KYOTOEKI["ramen"]

ARASHIYAMA = {
 "local": [
  S("쇼라이안", "松籟庵", "Shoraian", "松籟庵 嵐山", X("두부 가이세키", "Tofu kaiseki", "豆腐懐石", "Kaiseki de tofu", "Kaiseki de tofu", "豆腐怀石"), X("호즈강 위 숲속 옛 별장", "A former villa in the woods above the Hozu River", "保津川を望む森の中の元別荘", "Antigua villa en el bosque sobre el río Hozu", "Ancienne villa dans les bois au-dessus de la Hozu", "俯瞰保津川的林中旧别墅"), "¥4,000~¥10,000"),
  S("유도후 사가노", "湯豆腐 嵯峨野", "Yudofu Sagano", "湯豆腐 嵯峨野 嵐山", YUDOFU, X("대나무숲 근처의 유도후 전문점", "Yudofu specialist near the bamboo grove", "竹林近くの湯豆腐専門店", "Especialista en yudofu cerca del bambú", "Spécialiste du yudofu près de la bambouseraie", "竹林附近的汤豆腐专门店"), "~¥4,000"),
  S("아라시야마 갸테이", "嵐山 ぎゃあてい", "Arashiyama Gyatei", "嵐山 ぎゃあてい", X("오반자이 정식", "Obanzai set", "おばんざい御膳", "Menú de obanzai", "Menu obanzai", "京都家常菜套餐"), X("교토 가정 반찬 열두어 가지", "About a dozen Kyoto home-style dishes", "京のおばんざい十数品", "Una docena de platos caseros de Kioto", "Une douzaine de petits plats de Kyoto", "十几道京都家常小菜"), "~¥3,000"),
 ],
 "cafe": [
  S("사보 코게쓰 아라시야마점", "茶房こげつ 嵐山店", "Sabo Kogetsu Arashiyama", "茶房こげつ 嵐山店", X("일본식 디저트", "Japanese desserts", "和スイーツ", "Postres japoneses", "Desserts japonais", "日式甜点"), X("말차를 쓴 단팥 디저트", "Sweet bean desserts with matcha", "抹茶を使ったあんこの甘味", "Postres de judía dulce con matcha", "Desserts aux haricots sucrés et matcha", "使用抹茶的红豆甜品"), "~¥1,000"),
  S("오이마쓰 아라시야마점", "老松 嵐山店", "Oimatsu Arashiyama", "老松 嵐山店", X("화과자와 말차", "Wagashi and matcha", "和菓子と抹茶", "Wagashi y matcha", "Wagashi et matcha", "和果子与抹茶"), X("교토 화과자 노포의 찻집", "Tea room of a long-established Kyoto confectioner", "京菓子の老舗の茶房", "Salón de té de una antigua confitería de Kioto", "Salon de thé d'un confiseur historique de Kyoto", "京都和果子老店的茶屋"), "~¥1,500"),
  S("고토키키 차야", "琴きき茶屋", "Kotokiki Chaya", "琴きき茶屋 嵐山", X("사쿠라모치", "Sakura mochi", "桜餅", "Sakura mochi", "Sakura mochi", "樱饼"), X("도게쓰교 앞 찻집", "Tea house by Togetsukyo Bridge", "渡月橋前の茶屋", "Casa de té junto al puente Togetsukyo", "Maison de thé près du pont Togetsukyo", "渡月桥前的茶屋"), "~¥1,000"),
 ]}
ARASHIYAMA["all"] = ARASHIYAMA["local"] + ARASHIYAMA["cafe"]

NANZENJI = {
 "local": [
  S("소혼케 유도후 오쿠탄 난젠지", "総本家ゆどうふ 奥丹 南禅寺", "Okutan Nanzenji", "奥丹 南禅寺", YUDOFU, X("에도 시대 초에 문을 연 유도후 노포", "A yudofu house open since the early Edo period", "江戸初期創業の湯豆腐の老舗", "Casa de yudofu abierta desde principios del periodo Edo", "Maison de yudofu ouverte depuis le début d'Edo", "江户初期创业的汤豆腐老店"), "¥3,000~¥4,000"),
  S("난젠지 준세이", "南禅寺 順正", "Nanzenji Junsei", "南禅寺 順正", X("유도후·가이세키", "Yudofu and kaiseki", "湯豆腐・会席", "Yudofu y kaiseki", "Yudofu et kaiseki", "汤豆腐·会席料理"), X("넓은 정원을 품은 유도후 가게", "Yudofu restaurant set in a large garden", "広い庭園のある湯豆腐の店", "Restaurante de yudofu con un gran jardín", "Restaurant de yudofu dans un grand jardin", "带宽敞庭园的汤豆腐店"), "¥3,000~¥12,000"),
  S("로쿠세이", "六盛", "Rokusei", "六盛 京都 岡崎", X("데오케 벤토", "Teoke bento", "手をけ弁当", "Bento teoke", "Bento teoke", "手桶便当"), X("나무통에 담은 교토 도시락", "Kyoto lunch box served in a wooden bucket", "木の手桶に詰めた京のお弁当", "Bento de Kioto servido en un cubo de madera", "Bento de Kyoto servi dans un seau en bois", "装在木桶里的京都便当"), "~¥4,000"),
 ],
 "washoku": [
  S("히노데 우동", "日の出うどん", "Hinode Udon", "日の出うどん 京都 南禅寺", X("카레 우동", "Curry udon", "カレーうどん", "Udon al curry", "Udon au curry", "咖喱乌冬"), X("매운 정도를 고를 수 있는 우동집", "Udon shop where you choose the spice level", "辛さを選べるうどん店", "Udon con el nivel de picante a elegir", "Udon au piquant réglable", "可选辣度的乌冬店"), "~¥1,500"),
  S("오멘 긴카쿠지 본점", "おめん 銀閣寺本店", "Omen Ginkakuji", "おめん 銀閣寺本店", X("오멘 (쓰케멘 우동)", "Omen (dipping udon)", "おめん（つけ麺うどん）", "Omen (udon para mojar)", "Omen (udon à tremper)", "OMEN（蘸面乌冬）"), X("은각사 근처 굵은 면 우동", "Thick dipping udon near Ginkaku-ji", "銀閣寺近くの太麺うどん", "Udon grueso para mojar cerca del Ginkaku-ji", "Udon épais à tremper près du Ginkaku-ji", "银阁寺附近的粗面乌冬"), "~¥1,500"),
  S("오카키타", "岡北", "Okakita", "岡北 京都 岡崎", X("기쓰네 우동", "Kitsune udon", "きつねうどん", "Udon kitsune", "Udon kitsune", "狐狸乌冬"), X("헤이안 신궁 앞 우동 노포", "Long-standing udon shop near Heian Shrine", "平安神宮近くのうどんの老舗", "Clásico del udon junto al santuario Heian", "Adresse historique d'udon près du sanctuaire Heian", "平安神宫附近的乌冬老店"), "~¥1,000"),
 ]}
NANZENJI["all"] = NANZENJI["local"] + NANZENJI["washoku"]

UJI = {
 "cafe": [
  S("나카무라 도키치 본점", "中村藤吉本店", "Nakamura Tokichi Honten", "中村藤吉本店 宇治", PARFAIT, X("에도 시대 말 창업한 차 가게의 카페", "Café of a tea merchant founded in the late Edo period", "幕末創業の茶商のカフェ", "Café de un comerciante de té fundado a finales de Edo", "Café d'un marchand de thé fondé à la fin d'Edo", "幕末创业茶商的咖啡馆"), "~¥2,000"),
  S("이토 큐에몬 본점", "伊藤久右衛門 本店", "Ito Kyuemon Honten", "伊藤久右衛門 本店 宇治", X("말차 파르페·말차 소바", "Matcha parfait and matcha soba", "抹茶パフェ・茶そば", "Parfait y soba de matcha", "Parfait et soba au matcha", "抹茶芭菲·茶荞麦面"), X("우지 차 가게가 직접 하는 찻집", "Tea room run by an Uji tea merchant", "宇治の茶舗直営の茶房", "Salón de té de un comerciante de té de Uji", "Salon de thé d'un marchand de thé d'Uji", "宇治茶铺直营茶屋"), "~¥2,000"),
  S("쓰지리헤이 본점", "辻利兵衛本店", "Tsujiri Hei Honten", "辻利兵衛本店 宇治", PARFAIT, X("옛 차 공장 건물의 카페", "Café in an old tea factory building", "古い茶工場を生かしたカフェ", "Café en una antigua fábrica de té", "Café dans une ancienne usine de thé", "利用老茶厂建筑的咖啡馆"), "~¥2,000"),
  S("쓰엔", "通圓", "Tsuen", "通圓 宇治", X("말차와 화과자", "Matcha and wagashi", "抹茶と和菓子", "Matcha y wagashi", "Matcha et wagashi", "抹茶与和果子"), X("우지바시 다리 앞의 오래된 찻집", "Historic tea house at Ujibashi Bridge", "宇治橋のたもとの老舗茶屋", "Casa de té histórica junto al puente Ujibashi", "Maison de thé historique au pont Ujibashi", "宇治桥头的老字号茶屋"), "~¥1,500"),
 ],
 "izakaya": [
  S("도리세이 본점", "鳥せい 本店", "Torisei Honten", "鳥せい 本店 伏見", X("닭 요리·사케", "Chicken dishes and sake", "鶏料理・日本酒", "Platos de pollo y sake", "Plats de poulet et saké", "鸡肉料理·清酒"), X("사케 양조장 건물을 고친 후시미 이자카야", "Fushimi izakaya in a converted sake brewery", "酒蔵を改装した伏見の居酒屋", "Izakaya de Fushimi en una antigua bodega de sake", "Izakaya de Fushimi dans une ancienne brasserie de saké", "由酒窖改建的伏见居酒屋"), "¥2,000~¥3,000"),
 ]}
UJI["all"] = UJI["cafe"] + UJI["izakaya"]

AREAS = {"fuji": FUJI, "kyotoeki": KYOTOEKI, "arashiyama": ARASHIYAMA, "nanzenji": NANZENJI, "uji": UJI}
SLUG = {k: "gp/" + k for k in AREAS}

CREDIT = X("리뷰가 많은 유명 가게를 Go Nihon Trip이 여러 맛집 소개 글로 확인해 골랐어요 (2026년 11월 기준). 별점과 영업시간은 가게마다 구글 지도 링크에서 확인하세요.",
 "Go Nihon Trip picked well-known, much-reviewed places after checking several restaurant guides (as of November 2026). Check ratings and opening hours via each Google Maps link.",
 "口コミの多い有名店を、Go Nihon Tripが複数のグルメ記事で確かめて選びました（2026年11月時点）。評価と営業時間は各店のGoogleマップでご確認ください。",
 "Go Nihon Trip eligió locales conocidos y con muchas reseñas tras consultar varias guías (noviembre de 2026). Consulta valoraciones y horarios en el enlace de Google Maps de cada uno.",
 "Go Nihon Trip a choisi des adresses réputées et très commentées après vérification dans plusieurs guides (novembre 2026). Consultez notes et horaires via le lien Google Maps de chaque adresse.",
 "Go Nihon Trip参考多篇美食介绍文章，挑选了评论较多的知名店铺（截至2026年11月）。评分和营业时间请通过各店的谷歌地图链接确认。")
X("카페", "Café", "カフェ", "Café", "Café", "咖啡馆")
X("향토요리", "Local cuisine", "郷土料理", "Cocina local", "Cuisine locale", "乡土料理")
