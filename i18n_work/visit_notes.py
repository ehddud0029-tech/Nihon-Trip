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
"hepfive-wheel": (["s_hepfive", "hepfive"], (
"HEP FIVE 관람차는 밤에 타는 걸 추천해요. 우메다 야경을 내려다볼 수 있고, 곤돌라 안에서 휴대폰 음악을 연결해 들을 수 있어서 분위기 좋게 야경을 즐길 수 있었어요. 오사카 주유패스가 있으면 무료로 탈 수 있어서, 주유패스를 쓴다면 꼭 타 보세요. (패스에 포함된 시설은 바뀔 수 있으니 미리 확인하세요.)",
"I recommend riding the HEP FIVE Ferris wheel at night. You look out over the lights of Umeda, and you can connect your phone to play your own music in the gondola, which makes the night view really atmospheric. It's free with the Osaka Amazing Pass, so if you have one, don't miss it. (Facilities included in the pass can change, so check before you go.)",
"HEP FIVEの観覧車は夜に乗るのがおすすめです。梅田の夜景を見下ろせて、ゴンドラの中でスマホの音楽をつないで流せるので、いい雰囲気で夜景を楽しめました。大阪周遊パスがあれば無料で乗れるので、周遊パスを使うならぜひ乗ってみてください。（パスの対象施設は変わることがあるので事前に確認してください。）",
"Recomiendo subir a la noria de HEP FIVE de noche. Se ven las luces de Umeda y puedes conectar el móvil para poner tu propia música en la cabina, así que la vista nocturna resulta muy especial. Es gratis con el Osaka Amazing Pass, así que si lo tienes, no te la pierdas. (Las atracciones incluidas en el pase pueden cambiar; compruébalo antes.)",
"Je recommande de faire la grande roue de HEP FIVE le soir. On domine les lumières d'Umeda et on peut connecter son téléphone pour écouter sa musique dans la cabine : l'ambiance est parfaite pour la vue nocturne. Elle est gratuite avec l'Osaka Amazing Pass, alors si vous l'avez, ne la manquez pas. (Les sites inclus dans le pass peuvent changer, vérifiez avant de partir.)",
"推荐晚上去坐HEP FIVE摩天轮。可以俯瞰梅田的夜景，还能在车厢里连接手机播放自己的音乐，看夜景的氛围特别好。持大阪周游卡可以免费乘坐，如果用周游卡的话一定要去坐坐。（周游卡包含的设施可能会变，请提前确认。）",
"แนะนำให้นั่งชิงช้าสวรรค์ HEP FIVE ตอนกลางคืน มองเห็นวิวกลางคืนของอุเมดะ และต่อมือถือเปิดเพลงของตัวเองในกระเช้าได้ บรรยากาศชมวิวกลางคืนจึงดีมาก ถ้ามีโอซาก้า อเมซิ่ง พาส นั่งได้ฟรี ถ้าใช้พาสอยู่ต้องลองนั่ง (สถานที่ที่รวมในพาสอาจเปลี่ยนได้ ควรเช็กก่อนไป)")),
"umeda-sky": (["umeda"], (
"우메다 공중정원도 야경을 보기에 정말 좋은 곳이에요. 아주 높아서 조금 무섭긴 했지만, 오사카 시내를 한눈에 내려다볼 수 있어서 추천하는 곳이에요.",
"The Umeda Sky Building's Floating Garden is another great spot for night views. It's so high that it felt a little scary, but you can see all of Osaka at a glance, so I recommend it.",
"梅田スカイビルの空中庭園も夜景を見るのに本当にいい場所です。とても高いので少し怖かったですが、大阪の街を一望できるのでおすすめです。",
"El Jardín Flotante del Umeda Sky Building es otro lugar estupendo para ver la ciudad de noche. Está tan alto que da un poco de miedo, pero se ve todo Osaka de un vistazo, así que lo recomiendo.",
"Le jardin flottant de l'Umeda Sky Building est un autre excellent endroit pour la vue nocturne. C'est si haut que ça fait un peu peur, mais on voit tout Osaka d'un seul coup d'œil, alors je le recommande.",
"梅田蓝天大厦的空中庭园也是看夜景的好地方。因为特别高，有点吓人，但能把大阪市区尽收眼底，所以很推荐。",
"สวนลอยฟ้าของอุเมดะสกายบิลดิงก็เป็นจุดชมวิวกลางคืนที่ดีมาก สูงมากจนรู้สึกน่ากลัวนิดหน่อย แต่มองเห็นเมืองโอซาก้าได้ทั้งหมดในครั้งเดียว จึงแนะนำ")),
"dotonbori": (["dotonbori"], (
"도톤보리는 관광객이 가장 많이 찾는 곳 중 하나예요. 맛집이 많이 모여 있고 쇼핑도 할 수 있어서, 한곳에서 모든 걸 할 수 있다는 게 가장 큰 장점이에요. 다만 사람이 너무 많아서 맛집은 웨이팅이 길고, 줄을 받지 않는 가게도 있을 정도예요. 꼭 가고 싶은 가게는 미리 예약하는 걸 추천해요.",
"Dotonbori is one of the places tourists visit most. With lots of famous restaurants and shopping in one area, its biggest advantage is that you can do everything in one place. But it's so crowded that the popular restaurants have long waits, and some don't even take walk-in queues. For places you really want to try, I recommend booking ahead.",
"道頓堀は観光客が最も多く訪れる場所の一つです。グルメ店がたくさん集まっていて買い物もできるので、一か所で何でもできるのが一番の魅力です。ただ人がとても多いので人気店は待ち時間が長く、行列を受け付けないお店もあるほどです。どうしても行きたいお店は予約するのがおすすめです。",
"Dotonbori es uno de los lugares más visitados por los turistas. Reúne muchos restaurantes famosos y tiendas, así que su gran ventaja es que puedes hacerlo todo en un mismo sitio. Pero hay tanta gente que en los restaurantes populares las esperas son largas, y algunos ni siquiera admiten cola. Para los sitios que de verdad quieras probar, recomiendo reservar.",
"Dotonbori est l'un des lieux les plus visités par les touristes. Avec de nombreux restaurants réputés et des boutiques réunis, son grand atout est de pouvoir tout faire au même endroit. Mais il y a tellement de monde que les restaurants populaires ont de longues files, et certains n'acceptent même pas la file d'attente. Pour les adresses qui vous tiennent à cœur, je recommande de réserver.",
"道顿堀是游客最常去的地方之一。美食店很多，也能购物，最大的优点是在一个地方就能把所有事情做完。不过人实在太多，热门餐厅要排很久，甚至有的店不接受排队。特别想去的店建议提前预约。",
"โดทงโบริเป็นหนึ่งในที่ที่นักท่องเที่ยวไปมากที่สุด มีร้านอาหารดังรวมกันอยู่เยอะและช้อปปิ้งได้ด้วย ข้อดีที่สุดคือทำทุกอย่างได้ในที่เดียว แต่คนเยอะมาก ร้านดังจึงต้องรอคิวนาน บางร้านถึงขั้นไม่รับคิวเลย ร้านที่อยากไปจริง ๆ แนะนำให้จองล่วงหน้า")),
"kiyomizu": (["kiyomizu", "sannenzaka", "s_ninenzaka"], (
"기요미즈데라로 가는 길은 정말 사람이 많아요. 조금이라도 여유롭게 구경하고 싶다면 새벽 일찍 출발하는 게 가장 좋아요. 올라가고 내려오는 길에 가게가 많아서 구경하는 재미도 있어요.",
"The road up to Kiyomizu-dera is really crowded. If you want to look around with a bit more room, setting out very early in the morning is best. There are lots of shops along the way up and down, so browsing is part of the fun.",
"清水寺へ向かう道は本当に人が多いです。少しでもゆったり見て回りたいなら、早朝に出発するのが一番です。上り下りの道にお店がたくさんあるので、見て歩く楽しさもあります。",
"El camino hacia Kiyomizu-dera está lleno de gente. Si quieres verlo con algo más de calma, lo mejor es salir muy temprano por la mañana. Hay muchas tiendas en la subida y la bajada, así que curiosear también es parte de la diversión.",
"Le chemin vers le Kiyomizu-dera est vraiment bondé. Pour visiter un peu plus tranquillement, le mieux est de partir très tôt le matin. Il y a beaucoup de boutiques à la montée comme à la descente, ce qui rend la balade amusante.",
"去清水寺的路上人真的很多。想稍微轻松一点地游览的话，一大早出发最好。上山和下山的路上有很多小店，逛起来也很有乐趣。",
"ทางไปวัดคิโยมิสึเดระคนเยอะมากจริง ๆ ถ้าอยากเที่ยวแบบสบายขึ้นสักหน่อย ออกเดินทางตั้งแต่เช้าตรู่ดีที่สุด ระหว่างทางขึ้นและลงมีร้านค้าเยอะ เดินดูก็สนุก")),
}
UI = [
("직접 다녀온 이야기", "From our own visit", "実際に行ってみて", "Nuestra visita", "Notre visite", "亲身体验", "จากการไปเที่ยวจริง"),
("Go Nihon Trip 운영자가 직접 다녀와서 쓴 글이에요.", "Written by the Go Nihon Trip editor after visiting in person.", "Go Nihon Tripの運営者が実際に訪れて書いた文章です。", "Escrito por el editor de Go Nihon Trip tras visitarlo en persona.", "Écrit par l'éditeur de Go Nihon Trip après une visite sur place.", "这是Go Nihon Trip运营者亲自去过后写的内容。", "เขียนโดยผู้ดูแล Go Nihon Trip หลังจากไปเที่ยวด้วยตัวเอง"),
]
