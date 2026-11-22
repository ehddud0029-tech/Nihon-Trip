# 운영자가 직접 다녀온 이야기 (사용자가 보내 준 경험담을 다듬은 글). 장소 페이지 설명 아래 '직접 다녀온 이야기' 칸.
# NOTES: 글 키 → (장소 id 목록, (한국어, 영어, 일본어, 스페인어, 프랑스어, 간체, 태국어))
# 새 경험담은 여기에 더하고 python3 i18n_work/patch_visitnotes.py → build.py emit → 배포.
NOTES = {
"hakata-station-shopping": (["amu_hakata", "hakatahankyu"], (
"하카타역에는 아뮤 플라자, 하카타 한큐 같은 쇼핑몰이 여러 개 붙어 있고 입점한 가게도 아주 많아요. 처음 갔을 때는 너무 복잡해서 길을 잃기도 했고, 원하는 가게를 찾아가는 것도 쉽지 않았어요. 대신 유명한 맛집이 한곳에 모여 있어서 맛집 투어를 하기에는 오히려 편했어요.",
"Hakata Station has several malls joined together, like AMU Plaza and Hakata Hankyu, with a huge number of shops. On my first visit it was so complex that I got lost, and finding a particular shop wasn't easy. On the other hand, so many famous restaurants are gathered in one place that it was actually an easy spot for a food tour.",
"博多駅にはアミュプラザや博多阪急など複数のショッピングモールがつながっていて、入っているお店もとても多いです。初めて行ったときは複雑すぎて迷子になり、目当てのお店を探すのも大変でした。そのかわり有名なグルメ店が一か所に集まっているので、食べ歩きにはむしろ便利でした。",
"La estación de Hakata tiene varios centros comerciales conectados, como AMU Plaza y Hakata Hankyu, con muchísimas tiendas. La primera vez era tan laberíntica que me perdí y no fue fácil encontrar la tienda que buscaba. En cambio, reúne tantos restaurantes famosos en un mismo lugar que resultó muy cómoda para una ruta gastronómica.",
"La gare de Hakata regroupe plusieurs centres commerciaux reliés entre eux, comme AMU Plaza et Hakata Hankyu, avec un très grand nombre de boutiques. Lors de ma première visite, c'était si complexe que je me suis perdu et qu'il n'était pas facile de trouver une boutique précise. En revanche, tant de restaurants réputés y sont rassemblés que c'était plutôt pratique pour une tournée gourmande.",
"博多站连着阿缪广场、博多阪急等好几家商场，入驻的店铺非常多。第一次去的时候太复杂，还迷了路，想找的店也不好找。不过很多有名的美食店都集中在一个地方，用来吃美食反而很方便。",
"สถานีฮากาตะมีห้างหลายแห่งเชื่อมต่อกัน เช่น อามุพลาซ่าและฮากาตะฮันคิว และมีร้านค้าเยอะมาก ครั้งแรกที่ไปซับซ้อนจนหลงทาง และหาร้านที่ต้องการก็ไม่ง่ายเลย แต่เพราะมีร้านอาหารดัง ๆ รวมอยู่ที่เดียวกันเยอะ การตระเวนกินจึงกลับสะดวกกว่าที่คิด")),
"yufuin": (["s_kinrinko", "s_yufudake", "s_floral", "floral"], (
"유후인은 당일치기로 가볍게 다녀오기 좋은 동네예요. 동네가 작아서 하루면 충분히 둘러볼 수 있고, 온천이 유명해서 1박을 하며 목욕할 수 있는 료칸에 묵는 여행객도 많아요. 한국인 여행객은 버스 투어로 유후인과 벳푸를 함께 둘러보기도 해요.",
"Yufuin is a great town for an easy day trip. It's small enough to see in a day, and since it's famous for its hot springs, many travellers also stay a night at a ryokan where they can bathe. Many Korean visitors take a bus tour that covers both Yufuin and Beppu.",
"由布院は日帰りで気軽に行きやすい町です。町が小さいので1日で十分に見て回れますし、温泉が有名なので、1泊して入浴できる旅館に泊まる旅行者も多いです。韓国からの旅行者はバスツアーで由布院と別府をまとめて回ることもあります。",
"Yufuin es un pueblo ideal para una excursión de un día sin complicaciones. Es lo bastante pequeño para verlo en un día y, como es famoso por sus aguas termales, muchos viajeros también pasan una noche en un ryokan con baño. Muchos visitantes coreanos hacen un tour en autobús que incluye Yufuin y Beppu.",
"Yufuin est une ville parfaite pour une excursion facile à la journée. Elle est assez petite pour être visitée en un jour et, comme elle est célèbre pour ses sources chaudes, beaucoup de voyageurs passent aussi une nuit dans un ryokan avec bains. Beaucoup de visiteurs coréens font un circuit en bus qui combine Yufuin et Beppu.",
"由布院很适合轻松当天往返。小镇不大，一天就能逛得很充分；这里的温泉很有名，所以也有很多游客住一晚，选择可以泡汤的旅馆。韩国游客有时会参加巴士团，把由布院和别府一起玩。",
"ยูฟุอินเป็นเมืองที่เหมาะกับการไปเช้าเย็นกลับแบบสบาย ๆ เมืองเล็กจึงเที่ยวได้ทั่วในวันเดียว และเพราะขึ้นชื่อเรื่องออนเซ็น นักท่องเที่ยวจำนวนมากจึงค้างหนึ่งคืนที่เรียวกังที่แช่ออนเซ็นได้ นักท่องเที่ยวเกาหลีบางส่วนก็ไปทัวร์รถบัสที่เที่ยวทั้งยูฟุอินและเบปปุ")),
}
UI = [
("직접 다녀온 이야기", "From our own visit", "実際に行ってみて", "Nuestra visita", "Notre visite", "亲身体验", "จากการไปเที่ยวจริง"),
("Go Nihon Trip 운영자가 직접 다녀와서 쓴 글이에요.", "Written by the Go Nihon Trip editor after visiting in person.", "Go Nihon Tripの運営者が実際に訪れて書いた文章です。", "Escrito por el editor de Go Nihon Trip tras visitarlo en persona.", "Écrit par l'éditeur de Go Nihon Trip après une visite sur place.", "这是Go Nihon Trip运营者亲自去过后写的内容。", "เขียนโดยผู้ดูแล Go Nihon Trip หลังจากไปเที่ยวด้วยตัวเอง"),
]
