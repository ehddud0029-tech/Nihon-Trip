# 술 페이지 '사 가면 좋은 술' 추가 24개(2026-11-11, 도시마다 3개). 직접 쓴 설명, 가격대는 일본 매장 기준 대략.
# 실행: python3 i18n_work/drink_more.py → sitegen/drink_view.js의 DRMORE 블록 + tr_58.tsv·zh_59.tsv·th_59.tsv, 그다음 patch_drink.py
import json, re
W = {
 'dept': ("백화점 주류 코너, 주류 전문점", "Department-store liquor floors, specialist liquor shops", "百貨店の酒売り場、酒専門店", "Secciones de licores de grandes almacenes, tiendas especializadas", "Rayons alcools des grands magasins, cavistes", "百货店酒类柜台、酒类专卖店", "แผนกเครื่องดื่มในห้างสรรพสินค้า ร้านเหล้าเฉพาะทาง"),
 'conv': ("편의점, 슈퍼, 공항 면세점", "Convenience stores, supermarkets, airport duty-free", "コンビニ、スーパー、空港免税店", "Konbini, supermercados, duty-free del aeropuerto", "Konbini, supermarchés, duty-free de l'aéroport", "便利店、超市、机场免税店", "ร้านสะดวกซื้อ ซูเปอร์มาร์เก็ต ร้านปลอดภาษีสนามบิน"),
 'gift': ("주류 전문점, 공항·역 기념품점", "Specialist liquor shops, airport and station gift shops", "酒専門店、空港・駅の土産店", "Tiendas especializadas, tiendas de recuerdos de aeropuertos y estaciones", "Cavistes, boutiques de souvenirs des aéroports et des gares", "酒类专卖店、机场和车站的特产店", "ร้านเหล้าเฉพาะทาง ร้านของฝากในสนามบินและสถานี"),
 'super': ("슈퍼, 주류 전문점, 돈키호테", "Supermarkets, liquor shops, Don Quijote", "スーパー、酒専門店、ドン・キホーテ", "Supermercados, licorerías, Don Quijote", "Supermarchés, cavistes, Don Quijote", "超市、酒类专卖店、唐吉诃德", "ซูเปอร์มาร์เก็ต ร้านเหล้า ดองกิโฮเต้"),
}
# 도시: [(종류, 이름7(ko,en,ja,es,fr,zh,th), 일본어 이름, 설명7, 파는 곳 키, 가격(한국어 형식), 맛7)]
D = {
'tokyo': [
 ('beer', ("에비스 맥주","Yebisu Beer","ヱビスビール","Cerveza Yebisu","Bière Yebisu","惠比寿啤酒","เบียร์เยบิสึ"), "ヱビスビール",
  ("도쿄 에비스에서 태어난 맥주. 맥아만 써서 맛이 진하고, 일본 어디서나 살 수 있어요.","A beer born in Ebisu, Tokyo. All-malt and full-flavoured, and sold everywhere in Japan.","東京・恵比寿生まれのビール。麦芽100%でコクがあり、日本中どこでも買えます。","Cerveza nacida en Ebisu, Tokio. Solo malta, con cuerpo, y se vende en todo Japón.","Bière née à Ebisu, à Tokyo. Pur malt, bien charpentée, vendue partout au Japon.","诞生于东京惠比寿的啤酒。只用麦芽，味道浓郁，日本各地都能买到。","เบียร์ที่เกิดในย่านเอบิสึ โตเกียว ใช้มอลต์ล้วน รสเข้ม หาซื้อได้ทั่วญี่ปุ่น"),
  'conv', "350ml 캔 약 250~300엔",
  ("맛: 맥아 향이 진하고 쓴맛이 또렷해요.","Taste: rich malt aroma with a clear bitterness.","味：麦芽の香りが濃く、苦みがはっきり。","Sabor: aroma intenso a malta y amargor marcado.","Goût : arôme de malt intense et amertume nette.","口味：麦芽香浓，苦味鲜明。","รสชาติ: กลิ่นมอลต์เข้ม ขมชัด")),
 ('sake', ("다마지만","Tamajiman","多満自慢","Tamajiman","Tamajiman","多满自慢","ทามะจิมัง"), "多満自慢",
  ("도쿄 훗사의 이시카와 주조가 빚는 도쿄 사케. 양조장 안에 식당과 매장이 있어요.","A Tokyo sake brewed by Ishikawa Brewery in Fussa. The brewery has restaurants and a shop on site.","東京・福生の石川酒造が造る東京の地酒。蔵の敷地に食事処と売店があります。","Sake de Tokio elaborado por la bodega Ishikawa, en Fussa. La bodega tiene restaurantes y tienda.","Saké de Tokyo brassé par la maison Ishikawa à Fussa. Restaurants et boutique sur place.","东京福生市石川酒造酿造的东京清酒。酒厂内有餐厅和商店。","สาเกโตเกียวจากโรงสาเกอิชิกาวะในเมืองฟุสสะ ในโรงมีร้านอาหารและร้านขาย"),
  'dept', "720ml 약 1,300~2,500엔",
  ("맛: 부드럽고 쌀의 단맛이 은은해요.","Taste: soft, with a gentle rice sweetness.","味：やわらかく、米の甘みがほんのり。","Sabor: suave, con un dulzor ligero de arroz.","Goût : souple, avec une légère douceur de riz.","口味：柔和，带淡淡的米甜。","รสชาติ: นุ่ม หวานข้าวอ่อน ๆ")),
 ('whisky', ("이치로즈 몰트 & 그레인 화이트 라벨","Ichiro's Malt & Grain White Label","イチローズモルト＆グレーン ホワイトラベル","Ichiro's Malt & Grain White Label","Ichiro's Malt & Grain White Label","Ichiro's Malt & Grain 白标","อิจิโรส์ มอลต์ แอนด์ เกรน ไวท์เลเบิล"), "イチローズモルト ホワイトラベル",
  ("도쿄 근교 사이타마 지치부의 작은 증류소가 만드는 블렌디드 위스키. 도쿄 주류 전문점에서 비교적 구하기 쉬워요.","A blended whisky from a small distillery in Chichibu, Saitama, near Tokyo. Fairly easy to find in Tokyo liquor shops.","東京近郊、埼玉・秩父の小さな蒸溜所が造るブレンデッドウイスキー。東京の酒専門店で比較的手に入りやすい一本。","Whisky blended de una pequeña destilería de Chichibu (Saitama), cerca de Tokio. Bastante fácil de encontrar en licorerías de Tokio.","Blend d'une petite distillerie de Chichibu (Saitama), près de Tokyo. Assez facile à trouver chez les cavistes de Tokyo.","东京近郊埼玉秩父的小蒸馏厂出品的调和威士忌。在东京的酒类专卖店比较容易买到。","วิสกี้เบลนด์จากโรงกลั่นเล็กในชิจิบุ ไซตามะ ใกล้โตเกียว หาซื้อได้ค่อนข้างง่ายในร้านเหล้าโตเกียว"),
  'dept', "700ml 약 3,800~5,000엔",
  ("맛: 가볍고 과일 향이 나며 하이볼로 좋아요.","Taste: light and fruity; good as a highball.","味：軽やかでフルーティー、ハイボール向き。","Sabor: ligero y afrutado; va bien en highball.","Goût : léger et fruité ; parfait en highball.","口味：轻盈带果香，适合做嗨棒。","รสชาติ: เบา มีกลิ่นผลไม้ เหมาะทำไฮบอล")),
],
'osaka': [
 ('whisky', ("산토리 가쿠빈","Suntory Kakubin","サントリー角瓶","Suntory Kakubin","Suntory Kakubin","三得利角瓶","ซันโทรี่ คาคุบิน"), "サントリー角瓶",
  ("오사카에서 시작한 산토리의 대표 위스키. 거북 등 무늬 병이 특징이고 값이 부담 없어요.","The signature whisky of Suntory, which started in Osaka. Known for its tortoiseshell-cut bottle and easy price.","大阪で創業したサントリーの定番ウイスキー。亀甲模様の瓶が目印で、手ごろな価格。","El whisky emblemático de Suntory, fundada en Osaka. Botella con relieve de caparazón de tortuga y precio asequible.","Le whisky emblématique de Suntory, fondée à Osaka. Bouteille à motif d'écaille et prix doux.","创立于大阪的三得利的代表威士忌。龟甲纹酒瓶是标志，价格实惠。","วิสกี้ตัวหลักของซันโทรี่ซึ่งก่อตั้งที่โอซาก้า ขวดลายกระดองเต่า ราคาไม่แพง"),
  'super', "700ml 약 1,700~2,200엔",
  ("맛: 달콤한 향에 끝맛이 깔끔해 하이볼의 기본이에요.","Taste: sweet aroma and a clean finish; the classic highball base.","味：甘い香りにすっきりした後味、ハイボールの定番。","Sabor: aroma dulce y final limpio; la base clásica del highball.","Goût : nez sucré et finale nette ; la base classique du highball.","口味：香气甜，收尾干净，是嗨棒的基本款。","รสชาติ: หอมหวาน จบสะอาด เป็นพื้นฐานของไฮบอล")),
 ('beer', ("미노오 맥주","Minoh Beer","箕面ビール","Cerveza Minoh","Bière Minoh","箕面啤酒","เบียร์มิโนะ"), "箕面ビール",
  ("오사카 북쪽 미노오의 크래프트 맥주. 세계 대회에서 상을 받은 스타우트와 W-IPA가 유명해요.","Craft beer from Minoh, north of Osaka. Its award-winning stout and W-IPA are the best known.","大阪北部・箕面のクラフトビール。世界の品評会で受賞したスタウトやW-IPAが有名。","Cerveza artesanal de Minoh, al norte de Osaka. Famosas su stout y su W-IPA, premiadas internacionalmente.","Bière artisanale de Minoh, au nord d'Osaka. Sa stout et sa W-IPA primées sont les plus connues.","大阪北部箕面的精酿啤酒。在世界大赛获奖的世涛和W-IPA很有名。","คราฟต์เบียร์จากมิโนะ ทางเหนือของโอซาก้า สเตาต์และ W-IPA ที่ได้รางวัลระดับโลกมีชื่อเสียง"),
  'dept', "330ml 병 약 450~600엔",
  ("맛: 종류마다 다르고, 스타우트는 커피 같은 구수함이 있어요.","Taste: varies by style; the stout has a roasty, coffee-like note.","味：種類によりさまざま、スタウトはコーヒーのような香ばしさ。","Sabor: depende del estilo; la stout tiene notas tostadas, como de café.","Goût : selon le style ; la stout a des notes torréfiées, proches du café.","口味：因款式而异，世涛有咖啡般的焦香。","รสชาติ: ต่างกันตามชนิด สเตาต์หอมคั่วคล้ายกาแฟ")),
 ('sake', ("아키시카","Akishika","秋鹿","Akishika","Akishika","秋鹿","อากิชิกะ"), "秋鹿",
  ("오사카 북쪽 노세에서 쌀 농사부터 직접 짓는 양조장의 사케. 쌀로만 빚는 준마이만 만들어요.","Sake from a brewery in Nose, north of Osaka, that grows its own rice. It makes only junmai (pure-rice) sake.","大阪北部・能勢で米作りから手がける蔵の酒。純米酒だけを造ります。","Sake de una bodega de Nose, al norte de Osaka, que cultiva su propio arroz. Solo elabora junmai.","Saké d'une maison de Nose, au nord d'Osaka, qui cultive son propre riz. Uniquement du junmai.","大阪北部能势一家从种稻开始的酒厂的清酒。只酿纯米酒。","สาเกจากโรงในโนเสะ ทางเหนือของโอซาก้า ที่ปลูกข้าวเอง ทำเฉพาะจุนไม"),
  'dept', "720ml 약 1,500~2,800엔",
  ("맛: 산미가 또렷하고 묵직해서 데워 마셔도 좋아요.","Taste: firm acidity and body; also good warmed.","味：酸がしっかりして力強く、燗にしてもおいしい。","Sabor: acidez marcada y cuerpo; también bueno templado.","Goût : acidité franche et du corps ; bon aussi tiédi.","口味：酸度鲜明、酒体厚实，温着喝也好。","รสชาติ: เปรี้ยวชัด เนื้อหนัก อุ่นดื่มก็อร่อย")),
],
'fukuoka': [
 ('shochu', ("하쿠타케 시로","Hakutake Shiro","白岳しろ","Hakutake Shiro","Hakutake Shiro","白岳Shiro","ฮาคุทาเกะ ชิโระ"), "白岳しろ",
  ("구마모토 히토요시의 쌀 소주. 규슈 어디서나 볼 수 있고 향이 순해서 소주가 처음이어도 편해요.","Rice shochu from Hitoyoshi, Kumamoto. Sold all over Kyushu and mild enough for shochu beginners.","熊本・人吉の米焼酎。九州のどこでも見かけ、香りがおだやかで焼酎が初めてでも飲みやすい。","Shochu de arroz de Hitoyoshi (Kumamoto). Se vende en todo Kyushu y es suave para principiantes.","Shochu de riz de Hitoyoshi (Kumamoto). Vendu partout à Kyushu, assez doux pour les débutants.","熊本人吉的米烧酒。九州各地都有卖，香气温和，第一次喝烧酒也容易入口。","โชจูข้าวจากฮิโตโยชิ คุมาโมโตะ มีขายทั่วคิวชู กลิ่นอ่อน เหมาะกับมือใหม่"),
  'super', "720ml 약 1,000~1,400엔",
  ("맛: 깨끗하고 은은한 단맛, 얼음이나 물을 타서 마셔요.","Taste: clean with a faint sweetness; drink on the rocks or with water.","味：すっきりとほのかな甘み、ロックや水割りで。","Sabor: limpio y ligeramente dulce; con hielo o con agua.","Goût : net, légèrement sucré ; avec glaçons ou allongé d'eau.","口味：清爽微甜，加冰或兑水喝。","รสชาติ: สะอาด หวานอ่อน ดื่มกับน้ำแข็งหรือผสมน้ำ")),
 ('sake', ("다나카 로쿠주고","Tanaka Rokujugo","田中六五","Tanaka Rokujugo","Tanaka Rokujugo","田中六五","ทานากะ โรคุจูโกะ"), "田中六五",
  ("후쿠오카 이토시마의 야마다니시키 쌀로 빚는 준마이 사케. 후쿠오카 식당에서 자주 보여요.","A junmai sake made with Yamada Nishiki rice from Itoshima, Fukuoka. Often on menus in Fukuoka restaurants.","福岡・糸島産の山田錦で造る純米酒。福岡の飲食店でよく見かけます。","Sake junmai elaborado con arroz Yamada Nishiki de Itoshima (Fukuoka). Habitual en restaurantes de Fukuoka.","Saké junmai au riz Yamada Nishiki d'Itoshima (Fukuoka). Souvent à la carte des restaurants de Fukuoka.","用福冈糸岛产山田锦酿造的纯米酒。在福冈的餐馆经常见到。","สาเกจุนไมจากข้าวยามาดะนิชิกิของอิโตชิมะ ฟุกุโอกะ พบบ่อยในร้านอาหารฟุกุโอกะ"),
  'dept', "720ml 약 1,600~2,200엔",
  ("맛: 깔끔하고 쌀 맛이 부드럽게 퍼져서 음식과 잘 맞아요.","Taste: clean with a gentle rice flavour; easy with food.","味：すっきりして米の旨みがやさしく広がり、食事に合う。","Sabor: limpio, con un suave sabor a arroz; acompaña bien la comida.","Goût : net, avec une douce saveur de riz ; facile à table.","口味：清爽，米的鲜味柔和，适合配餐。","รสชาติ: สะอาด รสข้าวนุ่ม เข้ากับอาหาร")),
 ('liqueur', ("아마오 딸기 술","Amaou strawberry liqueur","あまおう苺のお酒","Licor de fresa Amaou","Liqueur de fraise Amaou","甘王草莓酒","เหล้าสตรอว์เบอร์รีอามาโอ"), "あまおう 苺 リキュール",
  ("후쿠오카 특산 딸기 '아마오'로 만든 달콤한 술. 병이 예뻐서 선물로 많이 사 가요.","A sweet liqueur made with Fukuoka's Amaou strawberries. The pretty bottles make it a popular gift.","福岡特産のいちご「あまおう」で造る甘いお酒。瓶がかわいく、お土産に人気。","Licor dulce elaborado con fresas Amaou de Fukuoka. Sus botellas bonitas lo hacen un regalo popular.","Liqueur douce aux fraises Amaou de Fukuoka. Ses jolies bouteilles en font un cadeau apprécié.","用福冈特产草莓“甘王”做的甜酒。瓶子好看，很适合当礼物。","เหล้าหวานจากสตรอว์เบอร์รีอามาโอของฟุกุโอกะ ขวดสวย นิยมซื้อเป็นของฝาก"),
  'gift', "500ml 약 1,300~1,800엔",
  ("맛: 딸기 향이 진하고 달아서 탄산수나 우유에 타면 좋아요.","Taste: rich strawberry and sweet; good with soda or milk.","味：いちごの香りが濃く甘口、ソーダやミルク割りで。","Sabor: fresa intensa y dulce; rico con soda o leche.","Goût : fraise intense et sucré ; bon avec de l'eau gazeuse ou du lait.","口味：草莓香浓、偏甜，兑苏打水或牛奶都好。","รสชาติ: หอมสตรอว์เบอร์รีเข้ม หวาน ผสมโซดาหรือนมอร่อย")),
],
'hokkaido': [
 ('sake', ("가미카와 다이세쓰","Kamikawa Taisetsu","上川大雪","Kamikawa Taisetsu","Kamikawa Taisetsu","上川大雪","คามิคาวะ ไทเซ็ตสึ"), "上川大雪",
  ("다이세쓰산 기슭 가미카와의 새 양조장이 홋카이도 쌀로만 빚는 사케. 조금씩 만들어서 홋카이도 안에서 주로 팔아요.","Sake from a young brewery in Kamikawa at the foot of the Daisetsuzan range, made only with Hokkaido rice. Small batches, sold mostly within Hokkaido.","大雪山のふもと・上川の新しい蔵が北海道産米だけで造る酒。少量仕込みで、主に道内で販売。","Sake de una bodega joven de Kamikawa, al pie del Daisetsuzan, solo con arroz de Hokkaido. Lotes pequeños, se vende sobre todo en Hokkaido.","Saké d'une jeune maison de Kamikawa, au pied du Daisetsuzan, uniquement au riz de Hokkaido. Petites cuvées, vendu surtout à Hokkaido.","大雪山脚下上川的新酒厂只用北海道米酿造的清酒。小批量酿造，主要在北海道内销售。","สาเกจากโรงใหม่ในคามิคาวะ เชิงเขาไดเซ็ตสึซัง ใช้ข้าวฮอกไกโดล้วน ผลิตน้อย ขายในฮอกไกโดเป็นหลัก"),
  'gift', "720ml 약 1,700~2,800엔",
  ("맛: 맑고 부드러우며 끝맛이 짧고 깔끔해요.","Taste: clear and soft with a short, clean finish.","味：澄んでやわらかく、後味は短くきれい。","Sabor: limpio y suave, con un final corto y nítido.","Goût : pur et souple, finale courte et nette.","口味：清澈柔和，回味短而干净。","รสชาติ: ใส นุ่ม จบสั้นและสะอาด")),
 ('wine', ("도카치 와인","Tokachi Wine","十勝ワイン","Vino Tokachi","Vin de Tokachi","十胜葡萄酒","ไวน์โทคาจิ"), "十勝ワイン",
  ("도카치 이케다초가 마을에서 직접 만드는 와인. 추위에 강한 포도로 만들어 산미가 살아 있어요.","Wine made by the town of Ikeda in Tokachi itself. Cold-hardy grapes give it lively acidity.","十勝・池田町が町営で造るワイン。寒さに強いぶどうを使い、酸がいきいき。","Vino elaborado por el propio pueblo de Ikeda, en Tokachi. Uvas resistentes al frío le dan una acidez viva.","Vin produit par la commune d'Ikeda, à Tokachi. Des cépages résistants au froid lui donnent une acidité vive.","十胜池田町由町营酿造的葡萄酒。使用耐寒葡萄，酸度鲜活。","ไวน์ที่เมืองอิเคดะในโทคาจิผลิตเอง ใช้องุ่นทนหนาว จึงมีความเปรี้ยวสดชื่น"),
  'gift', "720ml 약 1,300~2,800엔",
  ("맛: 산미가 또렷한 레드가 대표적이고 고기 요리와 잘 맞아요.","Taste: best known for crisp, acidic reds that suit meat dishes.","味：酸のきいた赤が代表的で、肉料理によく合う。","Sabor: destacan sus tintos de acidez marcada, buenos con carne.","Goût : surtout des rouges à l'acidité franche, parfaits avec la viande.","口味：以酸度鲜明的红酒为代表，适合配肉菜。","รสชาติ: ไวน์แดงเปรี้ยวชัดเป็นตัวเด่น เข้ากับอาหารเนื้อ")),
 ('beer', ("아바시리 유빙 드래프트","Abashiri Ryuhyo Draft","網走ビール 流氷ドラフト","Abashiri Ryuhyo Draft","Abashiri Ryuhyo Draft","网走流冰生啤","อาบาชิริ รีวเฮียวดราฟต์"), "流氷ドラフト",
  ("오호츠크해의 유빙을 녹인 물로 만든 파란색 발포주. 색이 신기해서 홋카이도 기념품으로 인기예요.","A blue sparkling brew made with melted drift ice from the Sea of Okhotsk. Its colour makes it a popular Hokkaido souvenir.","オホーツク海の流氷を仕込み水に使った青い発泡酒。色が珍しく、北海道土産に人気。","Bebida espumosa azul elaborada con agua de hielo a la deriva del mar de Ojotsk. Su color la hace un recuerdo popular de Hokkaido.","Boisson pétillante bleue brassée avec de l'eau de glace dérivante de la mer d'Okhotsk. Sa couleur en fait un souvenir prisé de Hokkaido.","用鄂霍次克海流冰融水酿造的蓝色发泡酒。颜色新奇，是很受欢迎的北海道伴手礼。","เครื่องดื่มมอลต์สีฟ้า ใช้น้ำจากน้ำแข็งลอยทะเลโอค็อตสค์ สีแปลกตา เป็นของฝากยอดนิยมของฮอกไกโด"),
  'gift', "350ml 캔 약 350~450엔",
  ("맛: 가볍고 쓴맛이 적어 산뜻해요.","Taste: light and refreshing with little bitterness.","味：軽くて苦みが少なく、さわやか。","Sabor: ligera y refrescante, poco amarga.","Goût : légère et rafraîchissante, peu amère.","口味：清淡，苦味少，很清爽。","รสชาติ: เบา ขมน้อย สดชื่น")),
],
'okinawa': [
 ('awamori', ("즈이센","Zuisen","瑞泉","Zuisen","Zuisen","瑞泉","ซุยเซ็น"), "瑞泉 泡盛",
  ("슈리성 옆 양조장의 아와모리. 슈리에서 가까워 견학 뒤 사기 좋고, 오래 숙성한 구스도 다양해요.","Awamori from a distillery beside Shuri Castle. Handy to buy after a visit, with a wide range of aged kusu.","首里城のそばの酒造所の泡盛。首里から近く見学のあとに買いやすく、古酒の種類も豊富。","Awamori de una destilería junto al castillo de Shuri. Fácil de comprar tras la visita, con muchos kusu añejos.","Awamori d'une distillerie voisine du château de Shuri. Pratique après la visite, avec un large choix de kusu vieillis.","首里城旁酒造所的泡盛。离首里近，参观后顺路购买，陈年古酒种类也多。","อาวาโมริจากโรงกลั่นข้างปราสาทชูริ ซื้อได้สะดวกหลังเที่ยวชม มีคูซุบ่มนานหลายแบบ"),
  'gift', "720ml 약 1,200~2,500엔",
  ("맛: 향이 화사하고 구스는 바닐라 같은 단 향이 나요.","Taste: fragrant; aged kusu has a sweet, vanilla-like aroma.","味：香り華やか、古酒はバニラのような甘い香り。","Sabor: aromático; el kusu añejo tiene un aroma dulce, como de vainilla.","Goût : parfumé ; le kusu vieilli a un nez sucré, vanillé.","口味：香气华丽，古酒有香草般的甜香。","รสชาติ: หอมฟุ้ง คูซุมีกลิ่นหวานคล้ายวานิลลา")),
 ('awamori', ("구메지마노 구메센","Kumejima no Kumesen","久米島の久米仙","Kumejima no Kumesen","Kumejima no Kumesen","久米岛的久米仙","คุเมจิมะ โนะ คุเมเซ็น"), "久米島の久米仙",
  ("구메섬의 샘물로 만드는 아와모리. 오키나와 슈퍼와 편의점 어디에나 있고 순해서 처음 마시기 좋아요.","Awamori made with spring water on Kume Island. In every Okinawan supermarket and convenience store, and mild for a first try.","久米島の湧き水で造る泡盛。沖縄のスーパーやコンビニのどこにでもあり、まろやかで初めてでも飲みやすい。","Awamori elaborado con agua de manantial de la isla de Kume. Está en todos los supermercados y konbini de Okinawa, suave para empezar.","Awamori à l'eau de source de l'île de Kume. Dans tous les supermarchés et konbini d'Okinawa, doux pour une première fois.","用久米岛泉水酿造的泡盛。冲绳的超市、便利店到处都有，口感柔和，适合第一次喝。","อาวาโมริจากน้ำพุของเกาะคุเมะ มีขายทุกซูเปอร์และร้านสะดวกซื้อในโอกินาวา นุ่ม เหมาะกับครั้งแรก"),
  'conv', "720ml 약 1,100~1,600엔",
  ("맛: 부드럽고 살짝 달아서 물과 얼음을 타서 마셔요.","Taste: smooth and slightly sweet; drink with water and ice.","味：まろやかでほんのり甘く、水割りで。","Sabor: suave y algo dulce; con agua y hielo.","Goût : rond, légèrement sucré ; avec eau et glaçons.","口味：柔和微甜，加水加冰喝。","รสชาติ: นุ่ม หวานนิด ๆ ดื่มผสมน้ำกับน้ำแข็ง")),
 ('liqueur', ("시콰사 술","Shikuwasa liqueur","シークヮーサーのお酒","Licor de shikuwasa","Liqueur de shikuwasa","香檬酒","เหล้าชีควาซ่า"), "シークヮーサー リキュール",
  ("오키나와 감귤 시콰사 즙을 넣은 새콤한 술. 아와모리가 부담스러운 사람에게 좋은 선물이에요.","A tangy liqueur made with juice of shikuwasa, Okinawa's citrus. A good gift for people who find awamori too strong.","沖縄の柑橘シークヮーサーの果汁を使った甘酸っぱいお酒。泡盛が強すぎる人へのお土産に。","Licor ácido con zumo de shikuwasa, el cítrico de Okinawa. Buen regalo para quien encuentra fuerte el awamori.","Liqueur acidulée au jus de shikuwasa, l'agrume d'Okinawa. Un bon cadeau pour ceux qui trouvent l'awamori trop fort.","加入冲绳柑橘香檬果汁的酸甜酒。适合送给觉得泡盛太烈的人。","เหล้าเปรี้ยวหวานผสมน้ำชีควาซ่า ส้มของโอกินาวา เหมาะเป็นของฝากสำหรับคนที่ว่าอาวาโมริแรงไป"),
  'gift', "500ml 약 1,000~1,600엔",
  ("맛: 라임처럼 새콤하고 살짝 써서 탄산수에 타면 시원해요.","Taste: lime-like tartness with a slight bitterness; refreshing with soda.","味：ライムのような酸味とほのかな苦み、ソーダ割りが爽快。","Sabor: ácido como la lima y algo amargo; refrescante con soda.","Goût : acidulé comme le citron vert, un peu amer ; rafraîchissant avec de l'eau gazeuse.","口味：像青柠一样酸，略带苦味，兑苏打水很清爽。","รสชาติ: เปรี้ยวคล้ายมะนาว ขมนิด ผสมโซดาแล้วสดชื่น")),
],
'nagoya': [
 ('sake', ("가모시비토 구헤이지","Kamoshibito Kuheiji","醸し人九平次","Kamoshibito Kuheiji","Kamoshibito Kuheiji","酿人九平次","คาโมชิบิโตะ คุเฮจิ"), "醸し人九平次",
  ("나고야 시내 양조장이 빚는 사케. 와인처럼 산미와 향을 살려 프랑스 식당에서도 내놓아요.","Sake from a brewery inside Nagoya city. Made with wine-like acidity and aroma, and served in French restaurants too.","名古屋市内の蔵が造る酒。ワインのように酸と香りを生かし、フランスのレストランでも提供されます。","Sake de una bodega dentro de la ciudad de Nagoya. Con acidez y aroma al estilo del vino, se sirve también en restaurantes franceses.","Saké d'une maison située dans Nagoya même. Acidité et arômes façon vin ; servi aussi dans des restaurants en France.","名古屋市内酒厂酿造的清酒。像葡萄酒一样突出酸度和香气，法国餐厅也有供应。","สาเกจากโรงในตัวเมืองนาโกย่า เน้นความเปรี้ยวและกลิ่นแบบไวน์ มีเสิร์ฟในร้านอาหารฝรั่งเศสด้วย"),
  'dept', "720ml 약 2,200~4,500엔",
  ("맛: 과일 향과 산미가 살아 있어 와인잔에 마시면 좋아요.","Taste: fruity with lively acidity; nice in a wine glass.","味：果実の香りと酸がいきいき、ワイングラスで。","Sabor: afrutado y de acidez viva; mejor en copa de vino.","Goût : fruité, acidité vive ; à boire dans un verre à vin.","口味：果香和酸度鲜活，用葡萄酒杯喝更好。","รสชาติ: หอมผลไม้ เปรี้ยวสดชื่น ดื่มในแก้วไวน์จะดี")),
 ('sake', ("호라이센","Houraisen","蓬莱泉","Houraisen","Houraisen","蓬莱泉","โฮไรเซ็น"), "蓬莱泉",
  ("아이치 산골 시타라의 양조장 사케. 아이치 사람들이 선물로 많이 고르는 이름이에요.","Sake from a brewery in the mountain town of Shitara, Aichi. A name Aichi locals often choose for gifts.","愛知の山あい・設楽の蔵の酒。愛知の人が贈り物によく選ぶ銘柄。","Sake de una bodega del pueblo de montaña de Shitara (Aichi). Marca que la gente de Aichi elige a menudo para regalar.","Saké d'une maison de Shitara, bourg de montagne d'Aichi. Une marque que les habitants d'Aichi offrent volontiers.","爱知山区设乐的酒厂出品的清酒。是爱知人送礼常选的品牌。","สาเกจากโรงในเมืองภูเขาชิตาระ ไอจิ เป็นยี่ห้อที่คนไอจินิยมเลือกเป็นของขวัญ"),
  'dept', "720ml 약 1,500~3,300엔",
  ("맛: 달콤하고 부드러워 술이 약한 사람도 마시기 편해요.","Taste: sweet and smooth; easy even for light drinkers.","味：甘くなめらかで、お酒に弱い人にも飲みやすい。","Sabor: dulce y suave; fácil incluso para quien bebe poco.","Goût : doux et soyeux ; facile même pour les petits buveurs.","口味：甘甜顺滑，不太能喝酒的人也容易入口。","รสชาติ: หวาน นุ่ม ดื่มง่ายแม้คนดื่มไม่เก่ง")),
 ('beer', ("히다 다카야마 맥주","Hida Takayama Beer","飛騨高山麦酒","Cerveza Hida Takayama","Bière Hida Takayama","飞驒高山麦酒","เบียร์ฮิดะทาคายามะ"), "飛騨高山麦酒",
  ("다카야마의 작은 양조장이 만드는 크래프트 맥주. 뭉툭한 병이 귀엽고 옛 거리 가게에서 팔아요.","Craft beer from a small brewery in Takayama. Sold in stubby bottles at shops in the old town.","高山の小さな醸造所のクラフトビール。ずんぐりした瓶がかわいく、古い町並みの店で買えます。","Cerveza artesanal de una pequeña fábrica de Takayama. En botellas chatas, a la venta en el casco antiguo.","Bière artisanale d'une petite brasserie de Takayama. En bouteilles trapues, vendue dans la vieille ville.","高山小酿酒厂的精酿啤酒。矮胖的酒瓶很可爱，在古街的店里有卖。","คราฟต์เบียร์จากโรงเล็กในทาคายามะ ขวดป้อมน่ารัก มีขายในร้านย่านเมืองเก่า"),
  'gift', "500ml 병 약 600~750엔",
  ("맛: 효모가 살아 있어 향이 진하고 묵직해요.","Taste: unfiltered with live yeast; rich aroma and body.","味：酵母が生きていて、香り豊かで飲みごたえあり。","Sabor: con levadura viva; aroma intenso y cuerpo.","Goût : levure vivante ; nez riche et du corps.","口味：保留活酵母，香气浓、酒体厚。","รสชาติ: มียีสต์มีชีวิต กลิ่นเข้ม เนื้อหนัก")),
],
'hiroshima': [
 ('sake', ("우고노쓰키","Ugo no Tsuki","雨後の月","Ugo no Tsuki","Ugo no Tsuki","雨后之月","อุโกะ โนะ สึกิ"), "雨後の月",
  ("구레의 양조장이 빚는 사케. '비 갠 뒤의 달'이라는 이름처럼 맑은 맛으로 알려져 있어요.","Sake from a brewery in Kure. Known for a clarity that matches its name, 'the moon after rain'.","呉の蔵が造る酒。「雨上がりの月」という名のとおり、澄んだ味わいで知られます。","Sake de una bodega de Kure. Conocido por una limpieza a la altura de su nombre, «la luna tras la lluvia».","Saké d'une maison de Kure. Réputé pour une pureté digne de son nom, « la lune après la pluie ».","吴市酒厂酿造的清酒。正如“雨后之月”这个名字，以清澈的口味闻名。","สาเกจากโรงในคุเระ ขึ้นชื่อเรื่องรสใสสมชื่อ 'พระจันทร์หลังฝน'"),
  'dept', "720ml 약 1,600~3,300엔",
  ("맛: 과일 향이 은은하고 맑고 깨끗해요.","Taste: gently fruity, clear and clean.","味：果実の香りがほんのり、澄んできれい。","Sabor: ligeramente afrutado, limpio y nítido.","Goût : légèrement fruité, pur et net.","口味：果香淡雅，清澈干净。","รสชาติ: หอมผลไม้อ่อน ๆ ใสและสะอาด")),
 ('sake', ("다케쓰루","Taketsuru (sake)","竹鶴","Taketsuru (sake)","Taketsuru (saké)","竹鹤（清酒）","ทาเคสึรุ (สาเก)"), "竹鶴 日本酒 竹原",
  ("다케하라의 다케쓰루 주조가 빚는 사케. 닛카 위스키를 만든 다케쓰루 마사타카의 본가예요.","Sake from Taketsuru Brewery in Takehara, the family home of Masataka Taketsuru, founder of Nikka Whisky.","竹原の竹鶴酒造の酒。ニッカウヰスキー創業者・竹鶴政孝の生家です。","Sake de la bodega Taketsuru de Takehara, casa natal de Masataka Taketsuru, fundador de Nikka Whisky.","Saké de la maison Taketsuru à Takehara, maison natale de Masataka Taketsuru, fondateur de Nikka Whisky.","竹原的竹鹤酒造酿造的清酒。这里是日果威士忌创始人竹鹤政孝的老家。","สาเกจากโรงทาเคสึรุในทาเคฮาระ บ้านเกิดของมาซาทากะ ทาเคสึรุ ผู้ก่อตั้งนิกกะวิสกี้"),
  'dept', "720ml 약 1,500~2,800엔",
  ("맛: 산미와 감칠맛이 진해서 데워 마시면 더 좋아요.","Taste: strong acidity and umami; even better warmed.","味：酸と旨みが濃く、燗でさらにおいしい。","Sabor: acidez y umami intensos; mejor aún templado.","Goût : acidité et umami marqués ; encore meilleur tiédi.","口味：酸度和鲜味浓厚，温着喝更好。","รสชาติ: เปรี้ยวและอูมามิเข้ม อุ่นดื่มยิ่งอร่อย")),
 ('beer', ("미야지마 맥주","Miyajima Beer","宮島ビール","Cerveza Miyajima","Bière Miyajima","宫岛啤酒","เบียร์มิยาจิมะ"), "宮島ビール",
  ("미야지마 섬 안 양조장의 크래프트 맥주. 오모테산도 상점가에서 갓 만든 생맥주도 마실 수 있어요.","Craft beer from a brewery on Miyajima island. You can also drink it fresh on tap along Omotesando shopping street.","宮島の島内にある醸造所のクラフトビール。表参道商店街でできたての生ビールも飲めます。","Cerveza artesanal de una fábrica en la isla de Miyajima. También se toma de barril en la calle comercial Omotesando.","Bière artisanale d'une brasserie de l'île de Miyajima. À boire aussi à la pression dans la rue commerçante Omotesando.","宫岛岛内酿酒厂的精酿啤酒。在表参道商店街还能喝到现酿生啤。","คราฟต์เบียร์จากโรงบนเกาะมิยาจิมะ ดื่มเบียร์สดได้ที่ถนนช้อปปิ้งโอโมเตะซันโด"),
  'gift', "330ml 병 약 500~650엔",
  ("맛: 종류가 여러 가지이고 페일 에일은 향긋하고 가벼워요.","Taste: several styles; the pale ale is fragrant and light.","味：種類はいろいろ、ペールエールは香りよく軽やか。","Sabor: varios estilos; la pale ale es aromática y ligera.","Goût : plusieurs styles ; la pale ale est parfumée et légère.","口味：有多种款式，淡色艾尔香气好、口感轻。","รสชาติ: มีหลายแบบ เพลเอลหอมและเบา")),
],
'shikoku': [
 ('sake', ("이시즈치","Ishizuchi","石鎚","Ishizuchi","Ishizuchi","石鎚","อิชิซึจิ"), "石鎚 日本酒",
  ("에히메 사이조에서 이시즈치산 물로 빚는 사케. 음식과 함께 마시는 술로 평이 좋아요.","Sake brewed in Saijo, Ehime, with water from Mount Ishizuchi. Well regarded as a sake to drink with food.","愛媛・西条で石鎚山の水を使って造る酒。食中酒として評判です。","Sake elaborado en Saijo (Ehime) con agua del monte Ishizuchi. Muy apreciado para acompañar la comida.","Saké brassé à Saijo (Ehime) avec l'eau du mont Ishizuchi. Très apprécié à table.","在爱媛西条用石鎚山的水酿造的清酒。作为佐餐酒评价很好。","สาเกจากไซโจ เอฮิเมะ ใช้น้ำจากภูเขาอิชิซึจิ ขึ้นชื่อว่าเหมาะดื่มคู่อาหาร"),
  'dept', "720ml 약 1,600~3,300엔",
  ("맛: 향이 차분하고 끝맛이 깔끔해 질리지 않아요.","Taste: restrained aroma and a clean finish you don't tire of.","味：香りは控えめ、後味すっきりで飲み飽きしない。","Sabor: aroma discreto y final limpio; no cansa.","Goût : nez discret, finale nette ; on ne s'en lasse pas.","口味：香气内敛，收尾干净，喝不腻。","รสชาติ: กลิ่นนุ่มนวล จบสะอาด ดื่มไม่เบื่อ")),
 ('sake', ("나루토타이","Narutotai","鳴門鯛","Narutotai","Narutotai","鸣门鲷","นารุโตะไท"), "鳴門鯛",
  ("도쿠시마 나루토의 양조장 사케. 알루미늄 캔에 담은 생원주가 유명해서 가져가기 편해요.","Sake from a brewery in Naruto, Tokushima. Famous for its undiluted fresh sake in an aluminium can, easy to carry home.","徳島・鳴門の蔵の酒。アルミ缶入りの生原酒が有名で、持ち帰りやすい。","Sake de una bodega de Naruto (Tokushima). Famoso su sake fresco sin diluir en lata de aluminio, fácil de llevar.","Saké d'une maison de Naruto (Tokushima). Célèbre pour son saké frais non dilué en canette d'aluminium, facile à emporter.","德岛鸣门酒厂的清酒。装在铝罐里的生原酒很有名，方便携带。","สาเกจากโรงในนารุโตะ โทคุชิมะ ขึ้นชื่อเรื่องสาเกสดไม่เจือจางในกระป๋องอะลูมิเนียม พกกลับสะดวก"),
  'gift', "720ml 약 1,500~2,800엔",
  ("맛: 진하고 달콤한 과일 향, 도수가 높으니 얼음을 넣어도 좋아요.","Taste: rich, sweet and fruity; it's strong, so ice works too.","味：濃厚で甘い果実の香り、度数が高いのでロックでも。","Sabor: intenso, dulce y afrutado; es fuerte, así que admite hielo.","Goût : riche, doux et fruité ; il est fort, donc bon aussi avec glaçons.","口味：浓郁的甜果香，度数高，加冰也好。","รสชาติ: เข้มข้น หอมผลไม้หวาน ดีกรีสูง ใส่น้ำแข็งก็ดี")),
 ('liqueur', ("스다치 술","Sudachi liqueur","すだち酒","Licor de sudachi","Liqueur de sudachi","酢橘酒","เหล้าสุดาจิ"), "すだち酒 徳島",
  ("도쿠시마 특산 감귤 스다치로 만든 술. 새콤하고 도수가 낮아 식전에 마시기 좋아요.","A liqueur made with sudachi, Tokushima's citrus. Tart and low in alcohol, good before a meal.","徳島特産の柑橘・すだちで造るお酒。甘酸っぱく度数も低めで、食前酒に。","Licor de sudachi, el cítrico de Tokushima. Ácido y de baja graduación, bueno como aperitivo.","Liqueur au sudachi, l'agrume de Tokushima. Acidulée et peu alcoolisée, idéale en apéritif.","用德岛特产柑橘酢橘做的酒。酸甜、度数低，适合餐前喝。","เหล้าจากสุดาจิ ส้มขึ้นชื่อของโทคุชิมะ เปรี้ยว ดีกรีต่ำ เหมาะดื่มก่อนอาหาร"),
  'gift', "500ml 약 1,000~1,600엔",
  ("맛: 상큼한 감귤 향에 단맛이 적당해 탄산수와 잘 맞아요.","Taste: fresh citrus with moderate sweetness; pairs well with soda.","味：さわやかな柑橘の香りにほどよい甘さ、ソーダ割りが合う。","Sabor: cítrico fresco y dulzor moderado; va bien con soda.","Goût : agrume frais, sucre modéré ; s'accorde bien avec de l'eau gazeuse.","口味：清新的柑橘香，甜度适中，适合兑苏打水。","รสชาติ: หอมส้มสดชื่น หวานพอดี เข้ากับโซดา")),
],
}
UNIT = {"캔": ("can", "缶", "lata", "canette", "罐", "กระป๋อง"), "병": ("bottle", "瓶", "botella", "bouteille", "瓶", "ขวด")}
def price(p, L):  # L: 0 en 1 ja 2 es 3 fr 4 zh 5 th
    m = re.match(r'^(\d+)ml (?:(캔|병) )?약 ([\d,]+)~([\d,]+)엔$', p); assert m, p
    vol, u, a, b = m.groups(); uu = UNIT[u][L] if u else ''
    if L == 0: return ' '.join(x for x in [f'{vol} ml', uu, f'approx. ¥{a}–{b}'] if x)
    if L == 1: return f'{vol}ml{uu} 約{a}〜{b}円'
    if L == 2: return (f'{uu} de {vol} ml' if uu else f'{vol} ml') + f', aprox. {a.replace(",",".")}–{b.replace(",",".")} ¥'
    if L == 3: return (f'{uu} de {vol} ml' if uu else f'{vol} ml') + f', env. {a.replace(","," ")}–{b.replace(","," ")} ¥'
    if L == 4: return f'{vol}ml{uu} 约{a}~{b}日元'
    if L == 5: return ' '.join(x for x in [uu, f'{vol} มล.', f'ประมาณ {a}–{b} เยน'] if x)

js = {}; rows = {}
def add(ko, tr6):
    if ko in rows: assert rows[ko] == tr6, ko
    rows[ko] = tr6
for c, items in D.items():
    js[c] = []
    for k, n, ja, d, w, p, t in items:
        js[c].append({"k": k, "n": n[0], "ja": ja, "d": d[0], "w": W[w][0], "p": p, "t": t[0]})
        if any(x != n[0] for x in n[1:]): add(n[0], list(n[1:]))
        add(d[0], list(d[1:])); add(W[w][0], list(W[w][1:])); add(t[0], list(t[1:]))
        add(p, [price(p, L) for L in range(6)])
B = '/home/claude/i18n_work/'
open(B + 'tr_58.tsv', 'w', encoding='utf-8').write(''.join('\t'.join([ko] + v[:4]) + '\n' for ko, v in rows.items()))
open(B + 'zh_59.tsv', 'w', encoding='utf-8').write(''.join(ko + '\t' + v[4] + '\n' for ko, v in rows.items()))
open(B + 'th_59.tsv', 'w', encoding='utf-8').write(''.join(ko + '\t' + v[5] + '\n' for ko, v in rows.items()))
p = '/home/claude/sitegen/drink_view.js'; s = open(p, encoding='utf-8').read()
blk = '/*DRMORE_BEGIN*/Object.entries(' + json.dumps(js, ensure_ascii=False) + ').forEach(([c,a])=>{ (DRINK_BUY[c]=DRINK_BUY[c]||[]).push(...a); });/*DRMORE_END*/'
if '/*DRMORE_BEGIN*/' in s:
    i = s.index('/*DRMORE_BEGIN*/'); j = s.index('/*DRMORE_END*/') + len('/*DRMORE_END*/'); s = s[:i] + blk + s[j:]
else:
    a = 'const DRINK_TABS = '; assert s.count(a) == 1 and s.index('const DRINK_BUY') < s.index(a)
    s = s.replace(a, blk + '\n' + a)
open(p, 'w', encoding='utf-8').write(s)
print('items', sum(len(v) for v in js.values()), 'rows', len(rows))
