# 새 지역 보충: 하위 지역마다 쇼핑 장소 1곳 이상 + 화면 문구 번역
from guide_data import T

SHOPS_ADD = {
 "nagoya": [
  ("p_inuyamahonmachi", "상점가", T("이누야마 혼마치 거리", "Inuyama Honmachi street", "犬山 本町通り", "Calle Honmachi de Inuyama", "Rue Honmachi d'Inuyama"), "犬山 本町通り",
   T("이누야마성 아래 옛 거리. 꼬치 과자와 젓가락·잡화 가게가 이어져요.", "The old street below Inuyama Castle, lined with skewered snacks and chopstick and craft shops.", "犬山城下の古い通り。串スイーツや箸・雑貨の店が続きます。", "Calle antigua bajo el castillo, con dulces en brocheta y tiendas de palillos y artesanía.", "Vieille rue sous le château, avec douceurs en brochette, baguettes et artisanat."),
   T("메이테쓰 이누야마역 도보 10분", "10 min walk from Meitetsu Inuyama Sta.", "名鉄犬山駅から徒歩10分", "A 10 min a pie de la est. Meitetsu Inuyama", "À 10 min à pied de la gare Meitetsu d'Inuyama"),
   T("대부분 오후 5시 무렵 문을 닫아요.", "Most shops close around 5 p.m.", "多くの店は夕方5時ごろ閉店。", "La mayoría cierra hacia las 17 h.", "La plupart ferment vers 17 h."), "inuyama", 35.3855, 136.9445),
  ("p_takayamasanmachi", "기념품", T("다카야마 옛 거리 상점", "Takayama old-town shops", "高山 古い町並みの店", "Tiendas del casco antiguo de Takayama", "Boutiques de la vieille ville de Takayama"), "高山 さんまち通り",
   T("양조장, 히다 소고기 꼬치, 사루보보 인형 가게가 모인 옛 거리 상점들.", "Sake breweries, Hida beef skewers and sarubobo doll shops along the old streets.", "酒蔵、飛騨牛の串焼き、さるぼぼの店が集まる古い町並み。", "Bodegas de sake, brochetas de ternera de Hida y muñecos sarubobo en las calles antiguas.", "Brasseries de saké, brochettes de bœuf de Hida et poupées sarubobo dans les vieilles rues."),
   T("JR 다카야마역 도보 10분", "10 min walk from JR Takayama Sta.", "JR高山駅から徒歩10分", "A 10 min a pie de la est. JR Takayama", "À 10 min à pied de la gare JR de Takayama"),
   T("시음은 술잔 값을 내고 해요. 오후 5시면 대부분 닫아요.", "Sake tastings cost a small fee; most shops close by 5 p.m.", "試飲はおちょこ代が必要。夕方5時にはほぼ閉店。", "Las catas cuestan algo; casi todo cierra a las 17 h.", "Dégustations payantes ; presque tout ferme à 17 h."), "takayama", 36.1404, 137.2601),
  ("p_shirakawaogimachi", "기념품", T("시라카와고 오기마치 기념품 거리", "Ogimachi souvenir street, Shirakawa-go", "白川郷 荻町の土産通り", "Calle de recuerdos de Ogimachi (Shirakawa-go)", "Rue des souvenirs d'Ogimachi (Shirakawa-go)"), "白川郷 荻町",
   T("갓쇼즈쿠리 집을 쓴 기념품 가게와 찻집이 마을 큰길을 따라 있어요.", "Souvenir shops and tea rooms in thatched houses along the village's main street.", "合掌造りの土産店や茶屋が集落の大通り沿いに並びます。", "Tiendas de recuerdos y casas de té en casas de tejado de paja a lo largo de la calle principal.", "Boutiques et salons de thé dans des maisons au toit de chaume le long de la rue principale."),
   T("시라카와고 버스 터미널 도보 5분", "5 min walk from the Shirakawa-go bus terminal", "白川郷バスターミナルから徒歩5分", "A 5 min a pie de la terminal de autobuses", "À 5 min à pied de la gare routière"),
   T("현금만 받는 가게가 있어요.", "Some shops take cash only.", "現金のみの店もあります。", "Algunas tiendas solo aceptan efectivo.", "Certaines boutiques n'acceptent que les espèces."), "shirakawago", 36.2577, 136.9063)],
 "hiroshima": [
  ("p_onomichihondori", "상점가", T("오노미치 혼도리 상점가", "Onomichi Hondori shopping street", "尾道本通り商店街", "Calle comercial Hondori de Onomichi", "Rue commerçante Hondori d'Onomichi"), "尾道本通り商店街",
   T("역 앞에서 동쪽으로 1.6km 이어진 아케이드. 오래된 가게와 레트로 카페가 섞여 있어요.", "A 1.6 km arcade running east from the station, mixing old shops and retro cafés.", "駅前から東へ1.6km続くアーケード。老舗とレトロなカフェが混在します。", "Galería de 1,6 km hacia el este desde la estación, con tiendas antiguas y cafés retro.", "Galerie de 1,6 km vers l'est depuis la gare, entre vieilles boutiques et cafés rétro."),
   T("JR 오노미치역 도보 3분", "3 min walk from JR Onomichi Sta.", "JR尾道駅から徒歩3分", "A 3 min a pie de la est. JR Onomichi", "À 3 min à pied de la gare JR d'Onomichi"),
   T("고양이 굿즈와 감귤 과자 가게가 많아요.", "Plenty of cat goods and citrus sweets.", "猫グッズや柑橘菓子の店が多いです。", "Muchos artículos de gatos y dulces cítricos.", "Beaucoup d'objets chats et de douceurs aux agrumes."), "onomichi", 34.4088, 133.2010),
  ("p_kurashikihonmachi", "상점가", T("구라시키 혼마치 거리", "Kurashiki Honmachi street", "倉敷 本町通り", "Calle Honmachi de Kurashiki", "Rue Honmachi de Kurashiki"), "倉敷 本町通り",
   T("미관지구 뒤편 옛 골목. 구라시키 데님과 마스킹 테이프, 잡화 가게가 모여 있어요.", "Old lanes behind the Bikan Quarter with Kurashiki denim, masking tape and craft shops.", "美観地区の裏手の古い路地。倉敷デニムやマスキングテープ、雑貨の店が集まります。", "Callejuelas tras el barrio Bikan con denim de Kurashiki, cinta washi y artesanía.", "Ruelles derrière le quartier Bikan : denim de Kurashiki, ruban décoratif et artisanat."),
   T("JR 구라시키역 도보 15분", "15 min walk from JR Kurashiki Sta.", "JR倉敷駅から徒歩15分", "A 15 min a pie de la est. JR Kurashiki", "À 15 min à pied de la gare JR de Kurashiki"),
   T("데님 거리는 아이비 스퀘어 근처에 있어요.", "The denim street is near Ivy Square.", "デニムストリートはアイビースクエアの近く。", "La calle del denim está cerca de Ivy Square.", "La rue du denim est près d'Ivy Square."), "kurashiki", 34.5965, 133.7730)],
 "shikoku": [
  ("p_naoshimaport", "기념품", T("우미노에키 나오시마 (미야노우라항)", "Umi no Eki Naoshima (Miyanoura Port)", "海の駅なおしま（宮浦港）", "Umi no Eki Naoshima (puerto de Miyanoura)", "Umi no Eki Naoshima (port de Miyanoura)"), "海の駅なおしま",
   T("배 터미널 안 매점. 섬 기념품과 미술관 굿즈를 살 수 있어요.", "The shop inside the ferry terminal, selling island souvenirs and art goods.", "フェリーターミナル内の売店。島の土産やアートグッズが買えます。", "Tienda de la terminal del ferri con recuerdos de la isla y artículos de arte.", "Boutique du terminal de ferry : souvenirs de l'île et objets d'art."),
   T("미야노우라항", "Miyanoura Port", "宮浦港", "Puerto de Miyanoura", "Port de Miyanoura"),
   T("항구 앞 빨간 호박도 놓치지 마세요.", "Don't miss the red pumpkin by the port.", "港の赤かぼちゃもお見逃しなく。", "No te pierdas la calabaza roja del puerto.", "Ne manquez pas la citrouille rouge du port."), "naoshima", 34.4594, 133.9752)],
}
PICKS_ADD = {
 "p_inuyamahonmachi": [T("꼬치 디저트", "Skewered sweets", "串スイーツ", "Dulces en brocheta", "Douceurs en brochette"), T("젓가락·잡화", "Chopsticks and crafts", "箸・雑貨", "Palillos y artesanía", "Baguettes et artisanat"), T("하트 에마 기념품", "Heart-shaped ema charms", "ハート絵馬グッズ", "Recuerdos de ema en forma de corazón", "Souvenirs d'ema en forme de cœur")],
 "p_takayamasanmachi": [T("히다 지역 술", "Hida sake", "飛騨の地酒", "Sake de Hida", "Saké de Hida"), T("사루보보 인형", "Sarubobo dolls", "さるぼぼ", "Muñecos sarubobo", "Poupées sarubobo"), T("미타라시 당고", "Mitarashi dango", "みだらし団子", "Dango mitarashi", "Dango mitarashi")],
 "p_shirakawaogimachi": [T("갓쇼즈쿠리 미니어처", "Thatched-house miniatures", "合掌造りのミニチュア", "Miniaturas de casas de paja", "Maisons au toit de chaume miniatures"), T("도부로쿠(탁주) 과자", "Doburoku (cloudy sake) sweets", "どぶろく菓子", "Dulces de doburoku", "Douceurs au doburoku"), T("산나물 절임", "Pickled mountain vegetables", "山菜の漬物", "Verduras de montaña encurtidas", "Légumes de montagne marinés")],
 "p_onomichihondori": [T("고양이 굿즈", "Cat goods", "猫グッズ", "Artículos de gatos", "Objets à motif de chats"), T("레몬 과자", "Lemon sweets", "レモン菓子", "Dulces de limón", "Douceurs au citron"), T("오노미치 라멘 선물 세트", "Onomichi ramen gift sets", "尾道ラーメンの土産", "Packs de ramen de Onomichi", "Coffrets de ramen d'Onomichi")],
 "p_kurashikihonmachi": [T("구라시키 데님", "Kurashiki denim", "倉敷デニム", "Denim de Kurashiki", "Denim de Kurashiki"), T("마스킹 테이프", "Masking tape", "マスキングテープ", "Cinta washi", "Ruban adhésif décoratif"), T("복숭아·포도 과자", "Peach and grape sweets", "桃・ぶどうのお菓子", "Dulces de melocotón y uva", "Douceurs à la pêche et au raisin")],
 "p_naoshimaport": [T("호박 굿즈", "Pumpkin goods", "かぼちゃグッズ", "Artículos de la calabaza", "Objets citrouille"), T("미술관 엽서·도록", "Museum postcards and catalogs", "美術館のポストカード・図録", "Postales y catálogos de museo", "Cartes postales et catalogues"), T("섬 소금", "Island salt", "島の塩", "Sal de la isla", "Sel de l'île")],
}
UI = [
 T("맛집 추천은 준비 중이에요", "Restaurant picks coming soon", "おすすめ店は準備中です", "Recomendaciones de restaurantes próximamente", "Adresses bientôt disponibles"),
 T("마쓰야마", "Matsuyama", "松山", "Matsuyama", "Matsuyama"),
 T("구글 지도에서 맛집 찾기 ↗", "Find restaurants on Google Maps ↗", "Googleマップでお店を探す ↗", "Buscar restaurantes en Google Maps ↗", "Trouver des restaurants sur Google Maps ↗"),
 T("이 지역의 맛집 추천은 준비 중이에요. 아래 향토음식을 참고해 구글 지도에서 가게를 찾아보세요.", "Restaurant picks for this area are coming soon. Use the local dishes below to find places on Google Maps.", "このエリアのおすすめ店は準備中です。下の郷土料理を参考にGoogleマップでお店を探してみてください。", "Las recomendaciones de restaurantes de esta zona llegarán pronto. Usa los platos locales de abajo para buscar en Google Maps.", "Les adresses de cette zone arrivent bientôt. Servez-vous des plats locaux ci-dessous pour chercher sur Google Maps."),
 T("지역마다 이름이 다르지만, 오키나와 OKICA와 시코쿠 지역 카드를 빼면 서로 호환돼요. 카드 한 장이면 전국의 지하철·버스·편의점에서 쓸 수 있어요.", "Names differ by region, but apart from Okinawa's OKICA and Shikoku's local cards they're all interchangeable. One card works on subways, buses and in convenience stores nationwide.", "地域ごとに名前は違いますが、沖縄のOKICAと四国の地域カードを除いて相互利用できます。1枚あれば全国の地下鉄・バス・コンビニで使えます。", "Los nombres cambian según la región, pero salvo OKICA de Okinawa y las tarjetas locales de Shikoku, todas son compatibles. Con una sola tarjeta puedes usar metro, autobuses y tiendas de todo el país.", "Les noms varient selon la région, mais hormis l'OKICA d'Okinawa et les cartes locales de Shikoku, elles sont toutes compatibles. Une seule carte suffit pour le métro, les bus et les konbini dans tout le pays."),
]
