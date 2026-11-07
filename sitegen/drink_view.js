/*DRINK_BEGIN*/
/* 술 여행: drink/ (일본 술 종류·라벨 읽는 법·주문 팁·가져오기 규칙 + 지역별 양조장), <도시>/drink/ (지역 술 특징 + 견학·시음할 수 있는 곳 + 자주 묻는 질문)
   양조장·증류소 정보는 2026년 11월 각 공식 사이트 기준. 요금·예약 방식이 자주 바뀌어서 카드마다 공식 사이트 링크를 붙여요. */
const DRINK_CITIES = ["tokyo","osaka","fukuoka","hokkaido","okinawa","nagoya","hiroshima","shikoku"];
const DRINK_KIND = {sake:"사케", beer:"맥주", whisky:"위스키", awamori:"아와모리", shochu:"소주", umeshu:"우메슈", wine:"와인", liqueur:"리큐어"};
const DRINK_INTRO = {
 tokyo:"도쿄에는 전국의 술이 모여요. 시내에서는 일본 술 정보관이나 에비스 양조장에서 가볍게 맛보고, 하루를 내면 오메의 사케 양조장이나 후지산·야마나시의 위스키 증류소까지 다녀올 수 있어요.",
 osaka:"간사이는 사케의 본고장이에요. 고베의 나다와 교토의 후시미는 일본을 대표하는 사케 산지이고, 오사카와 교토 사이에는 일본 첫 몰트위스키 증류소인 야마자키가 있어요.",
 fukuoka:"규슈는 소주(쇼추)의 고장이에요. 후쿠오카 시내에는 하카타의 오래된 사케 양조장이 있고, 맥주 공장 견학은 아사쿠라의 기린 공장에서 할 수 있어요. 아사히 맥주 하카타 공장은 견학을 끝냈어요.",
 hokkaido:"삿포로 맥주의 고향이자 닛카 위스키가 시작된 요이치가 있는 곳이에요. 오타루와 아사히카와에서는 추운 기후에서 빚는 사케 양조장을 무료로 둘러볼 수 있어요.",
 okinawa:"오키나와의 술은 아와모리예요. 타이 쌀과 검은 누룩으로 빚는 증류주로, 3년 넘게 숙성한 것을 구스(古酒)라고 불러요. 맥주는 오리온이 대표예요.",
 nagoya:"나고야 근처에서는 기린 맥주 공장을 견학할 수 있어요. 다카야마 옛 거리에는 처마에 삼나무 공(스기다마)을 단 사케 양조장이 모여 있어요. 아사히 맥주 나고야 공장은 견학을 끝냈어요.",
 hiroshima:"히로시마현 사이조는 '사케의 도시'로 불려요. 역 근처 거리에 양조장이 모여 있어 걸어서 돌아보며 시음할 수 있어요.",
 shikoku:"에히메 도고온천에서는 온천 뒤에 지역 맥주를, 가가와 고토히라에서는 곤피라 참배길 입구의 사케 박물관을 들러 보세요."
};
const DRINKS = [
 {city:"tokyo", k:"beer", n:"YEBISU BREWERY TOKYO", ja:"YEBISU BREWERY TOKYO", area:"에비스", d:"에비스 맥주가 처음 만들어진 곳에 있는 양조장 겸 박물관. 박물관은 무료로 둘러볼 수 있고, 탭룸에서 이곳 맥주를 마실 수 있어요.",
  fee:"박물관 무료 · 가이드 투어 유료", rv:"가이드 투어만 인터넷 예약", h:"평일 12:00–20:00 · 주말·공휴일 11:00–19:00", cl:"화요일 (공휴일이면 다음 날)", st:"에비스 가든 플레이스 안", u:"https://www.sapporobeer.jp/brewery/y_museum/"},
 {city:"tokyo", k:"sake", n:"일본 술 정보관", ja:"日本の酒情報館", area:"도라노몬", d:"일본주조조합중앙회가 운영하는 곳. 전국의 사케·소주 약 50가지를 한 잔씩 비교해 마실 수 있어요.",
  fee:"시음 유료 (한 잔 100엔부터)", rv:"필요 없음", h:"평일 10:00–18:00", cl:"토·일요일, 공휴일", st:"도쿄 메트로 도라노몬역 9번 출구에서 걸어서 3분", u:"https://japansake.or.jp/JSScenter/"},
 {city:"tokyo", k:"sake", n:"사와노이 (오자와 주조)", ja:"澤乃井 小澤酒造", area:"오메 (도쿄 서쪽)", d:"오쿠타마 계곡 옆 양조장. 시음이 포함된 약 40분 견학이 있고, 강가 정원과 식당도 있어요.",
  fee:"견학 유료 (20세 미만 무료)", rv:"전날까지 인터넷 예약", h:"평일 11:00·13:00 · 주말·공휴일 11:00·12:30·14:00 출발", cl:"월요일 (공휴일이면 다음 날)", st:"JR 오메선 사와이역 인근", u:"https://www.sawanoi-sake.com/"},
 {city:"tokyo", k:"whisky", n:"기린 후지고텐바 증류소", ja:"キリンディスティラリー富士御殿場蒸溜所", area:"후지산 기슭 (시즈오카현 고텐바)", d:"후지산 기슭의 위스키 증류소. 약 80분 투어 끝에 위스키 두 가지를 시음해요. 전시 공간은 예약 없이 무료로 볼 수 있어요.",
  fee:"투어 유료 (20세 이상)", rv:"투어는 예약 필요", cl:"월요일 (공휴일이면 다음 평일)", u:"https://www.kirin.co.jp/experience/factory/gotemba/"},
 {city:"tokyo", k:"whisky", n:"산토리 하쿠슈 증류소", ja:"サントリー白州蒸溜所", area:"야마나시현 호쿠토 (도쿄에서 당일치기)", d:"숲속에 있는 위스키 증류소. 견학은 유료 예약제이고, 증류소에서만 마실 수 있는 위스키를 내는 유료 테이스팅 라운지가 있어요.",
  fee:"견학 유료", rv:"견학은 예약 필요", h:"9:30–16:30 (입장 16:00까지)", cl:"연말연시, 공장 휴업일", u:"https://www.suntory.co.jp/factory/hakushu/"},
 {city:"osaka", k:"whisky", n:"산토리 야마자키 증류소", ja:"サントリー山崎蒸溜所", area:"오사카와 교토 사이 (시마모토)", d:"일본 첫 몰트위스키 증류소. 견학은 유료 예약제로, 예약 접수 기간이 정해져 있으니 공식 사이트 공지를 확인하세요. 유료 테이스팅 카운터도 있어요.",
  fee:"견학 유료", rv:"견학은 예약 필요", h:"10:00–16:45 (입장 16:30까지)", cl:"연말연시, 공장 휴업일", st:"JR 야마자키역·한큐 오야마자키역에서 걸어서 약 10분", u:"https://www.suntory.co.jp/factory/yamazaki/"},
 {city:"osaka", k:"sake", n:"겟케이칸 오쿠라 기념관", ja:"月桂冠大倉記念館", area:"교토 후시미", d:"후시미 사케 마을의 대표 양조장 박물관. 입장료에 작은 술잔 기념품과 사케 3가지 시음이 들어 있어요. 운전자는 시음 대신 작은 병 사케를 받을 수 있어요.",
  fee:"유료 (성인 600엔)", rv:"필요 없음", h:"9:30–16:30 (입장 16:00까지)", cl:"오봉, 연말연시", st:"게이한 주쇼지마역에서 걸어서 약 5분", u:"https://www.gekkeikan.co.jp/enjoy/museum/"},
 {city:"osaka", k:"sake", n:"기쿠마사무네 주조 기념관", ja:"菊正宗酒造記念館", area:"고베 나다", d:"옛날 술 빚는 도구와 과정을 볼 수 있는 기념관이에요.",
  fee:"무료", rv:"10명 미만은 필요 없음", h:"9:30–16:30", cl:"화요일 (공휴일이면 다음 날), 연말연시", st:"롯코 라이너 미나미우오자키역에서 걸어서 약 2분 · 한신 우오자키역에서 약 10분", u:"https://www.kikumasamune.co.jp/kinenkan/"},
 {city:"osaka", k:"sake", n:"하쿠쓰루 주조 자료관", ja:"白鶴酒造資料館", area:"고베 나다", d:"술 빚는 과정을 전시한 자료관. 둘러본 뒤 시음할 수 있고, 2026년 8월에 매장을 새로 단장했어요.",
  fee:"무료", rv:"필요 없음", h:"9:30–16:30 (입장 16:00까지)", st:"고베시 히가시나다구 스미요시미나미마치", u:"https://www.hakutsuru.co.jp/"},
 {city:"osaka", k:"beer", n:"아사히 맥주 박물관 (스이타)", ja:"アサヒビールミュージアム（吹田）", area:"오사카부 스이타", d:"아사히 맥주 공장 견학. 약 90분 투어 끝에 슈퍼드라이 등을 시음해요.",
  fee:"유료 (20세 이상 1,000엔)", rv:"완전 예약제 (인터넷·전화)", h:"투어 10:00–15:00 출발", cl:"부정기 휴무", u:"https://www.asahibeer.co.jp/brewery/"},
 {city:"fukuoka", k:"sake", n:"이시쿠라 주조 하카타 햐쿠넨구라", ja:"石蔵酒造 博多百年蔵", area:"하카타", d:"하카타에서 백 년 넘게 술을 빚어 온 양조장. 공장 견학은 없지만 직매장에서 시음하고 살 수 있어요.",
  fee:"직매장 시음", rv:"필요 없음 (10명 이상은 문의)", h:"11:00–17:00", cl:"화요일, 1월 1~3일", st:"지하철 기온역에서 걸어서 약 12분", u:"https://www.ishikura.co.jp/"},
 {city:"fukuoka", k:"beer", n:"기린 맥주 후쿠오카 공장", ja:"キリンビール福岡工場", area:"후쿠오카현 아사쿠라", d:"약 75분 공장 투어 뒤에 이치방시보리 맥주를 시음해요. 안내는 일본어로만 해요.",
  fee:"유료 (20세 이상 1,000엔)", rv:"예약 필요", h:"투어 10:00–15:00 출발", cl:"월요일 (공휴일이면 다음 평일), 연말연시", u:"https://www.kirin.co.jp/experience/factory/fukuoka/"},
 {city:"hokkaido", k:"beer", n:"삿포로 맥주 박물관", ja:"サッポロビール博物館", area:"삿포로 (히가시구)", d:"일본 맥주 역사를 볼 수 있는 붉은 벽돌 박물관. 2026년 7월 새 단장 뒤 자유 관람도 유료가 됐고, 시음이 포함된 가이드 투어는 예약제예요.",
  fee:"유료 (자유 관람 성인 1,000엔)", rv:"가이드 투어는 예약 필요", h:"11:00–18:00 (입장 17:30까지)", cl:"12월 31일", u:"https://www.sapporobeer.jp/brewery/s_museum/"},
 {city:"hokkaido", k:"whisky", n:"닛카 위스키 요이치 증류소", ja:"ニッカウヰスキー余市蒸溜所", area:"요이치 (오타루에서 열차 약 30분)", d:"닛카 위스키가 시작된 증류소. 시음이 포함된 가이드 투어는 예약제이고, 뮤지엄·매장은 예약 없이 들어갈 수 있어요(유료 테이스팅 바).",
  fee:"뮤지엄 무료 · 테이스팅 바 유료", rv:"가이드 투어는 예약 필요", cl:"12월 23일~1월 7일, 6월 11일", st:"JR 요이치역에서 걸어서 약 5분", u:"https://www.nikka.com/distilleries/yoichi/"},
 {city:"hokkaido", k:"sake", n:"다나카 주조 기코구라", ja:"田中酒造 亀甲蔵", area:"오타루", d:"오타루 유일의 사케 양조장. 유리창 너머로 술 빚는 곳을 10~15분 둘러보고 시음할 수 있어요.",
  fee:"무료", rv:"10명 미만은 필요 없음", h:"9:05–17:30", cl:"연중무휴", st:"JR 미나미오타루역에서 걸어서 약 5분", u:"https://tanakashuzo.com/"},
 {city:"hokkaido", k:"sake", n:"오토코야마 사케 자료관", ja:"男山酒造り資料舘", area:"아사히카와", d:"아사히카와의 오래된 양조장이 운영하는 자료관. 옆 매장에서 시음하고 살 수 있어요.",
  fee:"무료", rv:"필요 없음", u:"https://www.otokoyama.com/museum/"},
 {city:"okinawa", k:"beer", n:"오리온 해피 파크", ja:"オリオンハッピーパーク", area:"나고 (오키나와 북부)", d:"오리온 맥주 공장 투어. 끝에 갓 만든 맥주를 1인 2잔까지 시음해요.",
  fee:"유료", rv:"예약 필요 (인터넷·전화)", h:"9:30–17:00", cl:"월요일, 연말연시", u:"https://www.orionbeer.co.jp/happypark/"},
 {city:"okinawa", k:"awamori", n:"즈이센 주조", ja:"瑞泉酒造", area:"나하 슈리", d:"슈리성 바로 옆 아와모리 양조장. 영상 관람과 구스(古酒)·리큐어 비교 시음을 무료로 할 수 있어요.",
  fee:"무료", rv:"5명 이상만 예약", cl:"공휴일", st:"슈리성 게이세이몬에서 걸어서 약 2분", u:"https://www.zuisen.co.jp/"},
 {city:"nagoya", k:"beer", n:"기린 맥주 나고야 공장", ja:"キリンビール名古屋工場", area:"아이치현 기요스", d:"약 80분 공장 투어 뒤에 이치방시보리 맥주를 시음해요. 안내는 일본어로만 해요.",
  fee:"유료 (20세 이상 1,000엔)", rv:"예약 필요", h:"투어 10:10–15:10 출발", cl:"월요일 (공휴일이면 다음 평일), 연말연시", u:"https://www.kirin.co.jp/experience/factory/nagoya/"},
 {city:"nagoya", k:"sake", n:"하라다 주조장", ja:"原田酒造場", area:"다카야마 옛 거리", d:"다카야마 옛 거리(산마치)의 사케 양조장. 술잔을 사면 여러 가지 사케를 시음할 수 있어요.",
  fee:"시음 유료 (술잔 구매)", rv:"필요 없음", h:"9:00–17:00", cl:"연중무휴", st:"JR 다카야마역에서 걸어서 약 15분", u:"https://www.hidatakayama.or.jp/eat/detail_3131.html", o:0},
 {city:"hiroshima", k:"sake", n:"사이조 사카구라 거리", ja:"西条酒蔵通り", area:"히가시히로시마 사이조", d:"가모쓰루·후쿠비진·가모이즈미·기레이·사이조쓰루·하쿠보탄·산요쓰루 7곳 양조장이 모인 거리. 각 양조장에서 시음할 수 있고, 주말·공휴일에 문을 여는 곳이 많아요.",
  fee:"양조장마다 다름", rv:"필요 없음", st:"JR 사이조역에서 가모쓰루 주조까지 걸어서 약 5분", u:"https://hh-kanko.ne.jp/ginjyo/", o:0},
 {city:"shikoku", k:"beer", n:"도고 바쿠슈칸", ja:"道後麦酒館", area:"마쓰야마 도고온천", d:"도고온천 본관 맞은편의 지역 맥주집. '봇짱'·'마돈나' 등 나쓰메 소세키 소설에서 이름을 딴 도고 맥주 4가지를 마실 수 있어요.",
  fee:"유료 (식당)", rv:"필요 없음", h:"12:00–21:00", cl:"수요일 (공휴일이면 다음 날)", st:"노면전차 도고온천역에서 걸어서 약 4분", u:"https://www.gltjp.com/ja/directory/item/14702/", o:0},
 {city:"shikoku", k:"sake", n:"긴료노사토", ja:"金陵の郷", area:"가가와 고토히라", d:"곤피라 참배길 입구에 있는 옛 양조장 건물의 사케 박물관. 시음할 수 있어요.",
  fee:"무료", rv:"단체만 예약", h:"평일 9:00–16:30 · 주말·공휴일 9:00–17:30", cl:"연중무휴", st:"JR 고토히라역에서 걸어서 약 10분", u:"https://www.nishino-kinryo.co.jp/museum/"}
];
const DRINK_TYPES = [
 ["사케 (니혼슈)","쌀·누룩·물로 빚는 발효주. 알코올 15% 안팎이고, 차게·상온·따뜻하게 모두 마셔요."],
 ["소주 (쇼추)","고구마·보리·쌀 등으로 만든 증류주. 규슈가 본고장이고, 물이나 탄산수에 타 마시는 경우가 많아요."],
 ["아와모리","오키나와의 증류주. 타이 쌀과 검은 누룩으로 만들고, 3년 넘게 숙성한 것을 구스(古酒)라고 해요."],
 ["맥주","아사히·기린·삿포로·산토리 4대 회사 외에 지역 맥주(지비루)도 많아요."],
 ["위스키","야마자키·하쿠슈·요이치 같은 증류소 한정 위스키는 증류소에서만 살 수 있는 경우가 많아요. 일본에서는 하이볼로도 많이 마셔요."],
 ["우메슈","매실을 담가 만든 달콤한 술. 술이 약한 사람도 마시기 쉬워요."]
];
const DRINK_LABEL = ["준마이(純米): 쌀·누룩·물만으로 빚은 사케예요.",
 "긴조(吟醸)·다이긴조(大吟醸): 쌀을 많이 깎아(정미율 60%·50% 이하) 향이 화사해요.",
 "혼조조(本醸造): 양조 알코올을 조금 더해 깔끔한 맛이에요.",
 "나마자케(生酒): 가열 살균을 하지 않은 생술이라 냉장 보관해야 해요.",
 "니고리자케(にごり酒): 술지게미가 남아 뿌옇고 부드러워요.",
 "일본주도(日本酒度): 숫자가 플러스로 클수록 대체로 단맛이 적어요(카라구치)."];
const DRINK_ORDER = ["사케는 보통 1고(一合, 약 180ml) 단위로 주문해요.",
 "히야(冷や)는 차게 또는 상온, 아쓰칸(熱燗)은 따뜻하게 데운 사케예요.",
 "이자카야에서는 주문하지 않아도 작은 안주(오토시)가 나오고 자릿세처럼 요금이 붙는 경우가 많아요.",
 "노미호다이(飲み放題)는 정해진 시간 동안 마음껏 마시는 요금제예요."];
const DRINK_BUY = {
 tokyo:[
  {k:"sake", n:"사와노이", ja:"澤乃井", d:"도쿄 오메에서 빚는 도쿄 지역 사케. 깔끔한 맛이라 처음 마시는 사람에게도 무난해요.", w:"양조장 매장, 도쿄 백화점 주류 코너"},
  {k:"whisky", n:"기린 싱글 그레인 위스키 후지", ja:"キリン シングルグレーンウイスキー 富士", d:"후지산 기슭 후지고텐바 증류소의 위스키. 부드럽고 달콤한 향이에요.", w:"증류소 매장, 큰 주류점·백화점"},
  {k:"sake", n:"닷사이", ja:"獺祭", d:"야마구치현 사케지만 과일 향이 화사한 준마이 다이긴조로 인기가 많아 도쿄에서도 쉽게 살 수 있어요.", w:"백화점, 공항 면세점"}],
 osaka:[
  {k:"sake", n:"나다·후시미 사케", ja:"灘・伏見の酒", d:"하쿠쓰루·기쿠마사무네(나다), 겟케이칸(후시미) 등 간사이 대표 양조장의 사케예요.", w:"양조장 기념관 매장, 오사카·교토 백화점"},
  {k:"umeshu", n:"초야 우메슈", ja:"チョーヤ梅酒", d:"오사카 하비키노에 본사가 있는 우메슈 회사. 매실이 든 병이나 작은 병 세트가 선물하기 좋아요.", w:"슈퍼, 백화점, 공항"},
  {k:"whisky", n:"야마자키", ja:"山崎", d:"일본 첫 몰트위스키 증류소의 위스키. 인기가 많아 일반 매장에서는 구하기 어려운 경우가 많아요.", w:"증류소 매장(수량 한정), 백화점"}],
 fukuoka:[
  {k:"shochu", n:"구로키리시마", ja:"黒霧島", d:"미야자키현의 고구마 소주. 규슈에서 가장 흔히 마시는 소주 가운데 하나예요.", w:"슈퍼, 주류점, 공항"},
  {k:"shochu", n:"이이치코", ja:"いいちこ", d:"오이타현의 보리 소주. 향이 순해서 물이나 탄산수에 타 마시기 좋아요.", w:"슈퍼, 주류점, 공항"},
  {k:"sake", n:"시게마스", ja:"繁桝", d:"후쿠오카현 야메의 오래된 양조장 사케. 후쿠오카 지역 사케를 찾는다면 좋은 선택이에요.", w:"하카타역·백화점 기념품 매장"}],
 hokkaido:[
  {k:"beer", n:"삿포로 클래식", ja:"サッポロクラシック", d:"홋카이도에서만 파는 삿포로 맥주. 여행 중에 꼭 마셔 볼 만해요.", w:"홋카이도 슈퍼·편의점, 신치토세 공항"},
  {k:"whisky", n:"싱글 몰트 요이치", ja:"シングルモルト余市", d:"닛카 요이치 증류소의 몰트위스키. 증류소에서만 파는 위스키도 있어요.", w:"요이치 증류소 매장, 백화점"},
  {k:"sake", n:"오토코야마·구니마레", ja:"男山・国稀", d:"아사히카와의 오토코야마, 마시케의 구니마레 등 추운 북쪽에서 빚는 깔끔한 사케예요.", w:"양조장 매장, 삿포로 백화점"},
  {k:"wine", n:"오타루 와인", ja:"おたるワイン", d:"홋카이도산 포도로 만든 오타루의 와인. 오타루 관광 기념품으로 많이 사요.", w:"오타루 운하 근처 기념품 매장, 홋카이도 슈퍼"}],
 okinawa:[
  {k:"awamori", n:"구스(오래 숙성한 아와모리)", ja:"古酒（クース）", d:"3년 넘게 숙성한 아와모리. 양조장 매장에서 시음해 보고 고를 수 있어요.", w:"양조장 매장, 국제거리 주류점"},
  {k:"awamori", n:"잔파", ja:"残波", d:"요미탄의 아와모리. 향이 부드러워 처음 마시는 사람에게도 무난해요.", w:"슈퍼, 공항"},
  {k:"beer", n:"오리온 드래프트", ja:"オリオン ドラフト", d:"오키나와를 대표하는 맥주. 가볍고 시원한 맛이라 더운 날씨에 잘 어울려요.", w:"슈퍼·편의점, 나하 공항"}],
 nagoya:[
  {k:"sake", n:"히다 다카야마 사케", ja:"飛騨高山の酒", d:"하라다 주조의 '산샤', 히라세 주조의 '구스다마', 후나사카 주조의 '미야마기쿠' 등 옛 거리 양조장의 사케예요.", w:"다카야마 옛 거리 양조장 매장"},
  {k:"sake", n:"구니자카리", ja:"國盛", d:"아이치현 한다의 나카노 주조 사케. 나고야 근처에서 쉽게 살 수 있어요.", w:"나고야 백화점, 기념품 매장"},
  {k:"beer", n:"긴샤치 맥주", ja:"金しゃちビール", d:"아이치현의 지역 맥주. 이름은 나고야성 지붕의 황금 샤치호코 장식에서 왔어요.", w:"나고야역 기념품 매장"}],
 hiroshima:[
  {k:"sake", n:"사이조 사케", ja:"西条の酒", d:"가모쓰루·하쿠보탄·가모이즈미·기레이 등 '사케의 도시' 사이조 양조장의 사케예요.", w:"사이조 양조장 매장, 히로시마역 기념품 매장"},
  {k:"liqueur", n:"세토우치 레몬 술", ja:"瀬戸内レモンのお酒", d:"히로시마는 일본 최대 레몬 산지예요. 레몬 리큐어나 레몬 사와가 기념품으로 많아요.", w:"히로시마역 기념품 매장, 공항"}],
 shikoku:[
  {k:"sake", n:"고치 사케", ja:"土佐の酒", d:"쓰카사보탄·스이게이·도사쓰루 등 깔끔하고 쌉쌀한 맛의 고치 사케예요.", w:"고치 백화점·역 기념품 매장"},
  {k:"beer", n:"도고 맥주", ja:"道後ビール", d:"마쓰야마 도고온천의 지역 맥주. '봇짱'·'마돈나' 등 소설에서 딴 이름이 붙어 있어요.", w:"도고온천 상점가, 마쓰야마 공항"},
  {k:"sake", n:"긴료", ja:"金陵", d:"가가와 고토히라의 양조장 사케. 곤피라 참배 기념품으로 좋아요.", w:"긴료노사토, 고토히라 상점가"},
  {k:"liqueur", n:"유자 술", ja:"ゆず酒", d:"일본 최대 유자 산지 고치의 유자로 만든 리큐어. 상큼해서 술이 약한 사람도 마시기 쉬워요.", w:"고치 기념품 매장"}],
};
const DRINK_SHOP = ["백화점 지하 식품관 주류 코너에는 지역 술이 모여 있고, 시음해 보고 고를 수 있는 곳도 많아요.",
 "역·공항 기념품 가게에는 작은 병이나 맛보기 세트가 있어 선물하기 좋아요.",
 "생술(나마자케)은 냉장 보관이 필요하니 여행 마지막 날에 사세요.",
 "증류소 한정 위스키는 한 사람이 살 수 있는 수량이 정해진 경우가 많아요."];
const DRINK_VISIT = ["일본은 20세부터 술을 마실 수 있어요. 견학 시음도 20세 미만은 할 수 없어요.",
 "운전하는 사람은 시음할 수 없어요. 대신 음료나 기념품을 주는 곳이 많아요.",
 "공장 투어는 대부분 예약제이고, 안내는 일본어로만 하는 곳이 많아요.",
 "요금과 예약 방식은 자주 바뀌니 방문 전에 공식 사이트에서 확인하세요."];
const DRINK_HOME_OTHER = "집으로 가져갈 때: 면세 한도는 나라마다 달라요. 출발 전에 자기 나라 세관 안내를 확인하세요.";
const DRINK_CARRY = ["한국으로 가져올 때: 술은 2병, 합계 2L, 400달러까지 면세예요. 기본 면세 한도(800달러)와 따로 계산하고, 만 19세 미만은 면세가 안 돼요.",
 "비행기: 알코올 24% 이하는 제한이 없고, 24% 넘고 70% 이하는 1인 5L까지 실을 수 있어요. 70%가 넘는 술은 실을 수 없어요(항공사마다 다를 수 있어요).",
 "국제선 기내 반입은 액체 100ml 규정이 있어서, 시내에서 산 술은 위탁 수하물에 넣으세요. 공항 면세점에서 산 술은 봉인된 봉투째로 들고 타요.",
 "병이 깨지지 않게 옷으로 감싸거나 매장에서 파는 완충 포장을 쓰세요."];
const drinkKo = () => ((window.I18N&&window.I18N.lang)||"ko")==="ko";
const drinkCarry = () => drinkKo() ? DRINK_CARRY : [DRINK_HOME_OTHER, ...DRINK_CARRY.slice(1)];
const drinkHomeQ = () => drinkKo() ? "일본 술은 한국에 몇 병까지 가져올 수 있나요?" : "일본 술은 몇 병까지 가져갈 수 있나요?";
const drinkHref = c => ROUTED ? window.NT_BASE + LPRE + (c && c!=="all" ? `${c}/drink/` : "drink/") : "#drink";
const drinkA = (c,inner,cls) => `<a${cls?` class="${cls}"`:""} href="${drinkHref(c)}" data-drc="${c||"all"}">${inner}</a>`;
function drinkChips(cur){ return `<div class="wxmon">${DRINK_CITIES.map(k=>drinkA(k,esc(CITIES[k].ko),k===cur?"on":"")).join("")}</div>`; }
const drinkList = (h,items) => `<div class="gblk"><h4>${h}</h4><ul class="gul">${items.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`;
function drinkCard(v){
  const row=(a,b)=>b?`<dt>${a}</dt><dd>${esc(b)}</dd>`:"";
  return `<article class="dcard"><div class="dtop"><span class="dkind dk-${v.k}">${DRINK_KIND[v.k]}</span><span class="harea">${esc(v.area)}</span></div>
   <h3>${esc(v.n)}</h3>${v.ja&&v.ja!==v.n?`<p class="hja notranslate" lang="ja">${esc(v.ja)}</p>`:""}<p class="dd">${esc(v.d)}</p>
   <dl>${row("요금",v.fee)}${row("예약",v.rv)}${row("시간",v.h)}${row("휴무",v.cl)}${row("가는 길",v.st)}</dl>
   <a class="more" href="${v.u}" target="_blank" rel="noopener">${v.o===0?"안내 페이지 ↗":"공식 사이트 ↗"}</a></article>`;
}
function drinkBuyCard(v){
  return `<article class="dcard dbuy"><div class="dtop"><span class="dkind dk-${v.k}">${DRINK_KIND[v.k]}</span></div>
   <h3>${esc(v.n)}</h3><p class="hja notranslate" lang="ja">${esc(v.ja)}</p><p class="dd">${esc(v.d)}</p>
   <dl><dt>살 수 있는 곳</dt><dd>${esc(v.w)}</dd></dl></article>`;
}
V.drink = function(){
  const c = DRINK_CITIES.includes(st.city) ? st.city : "";
  const bc=(i,h)=>`<span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">${h.replace("<a ",'<a itemprop="item" ').replace(/>([^<]*)<\/a>$/,'><span itemprop="name">$1</span></a>')}<meta itemprop="position" content="${i}"></span>`;
  const qa=(q,x)=>`<div class="faqi" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><dt itemprop="name">${q}</dt><dd itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><div itemprop="text">${x}</div></dd></div>`;
  const note = `<p class="sisrc">2026년 11월 각 공식 사이트 기준이에요. 요금·시간·예약 방식은 바뀔 수 있어요. 술은 20세부터, 운전 전에는 마시지 마세요.</p>`;
  if(!c){
    return `<div class="wx">
     <div class="ghead"><h2>일본 술 여행 – 지역별 사케·맥주·위스키</h2><p>일본 술의 종류와 고르는 법, 지역별로 견학·시음할 수 있는 양조장과 증류소, 한국에 가져올 때의 규칙까지 정리했어요.</p></div>
     <nav class="wxmon stjump">${DRINK_CITIES.map(k=>`<a href="#st-${k}" data-stjump="${k}">${esc(CITIES[k].ko)}</a>`).join("")}</nav>
     <div class="dtypes">${DRINK_TYPES.map(([a,b])=>`<div class="gblk"><h4>${esc(a)}</h4><p>${esc(b)}</p></div>`).join("")}</div>
     ${drinkList("사케 라벨 읽는 법", DRINK_LABEL)}
     ${drinkList("주문할 때 알아 둘 말", DRINK_ORDER)}
     ${DRINK_CITIES.map(k=>{ const vs=DRINKS.filter(v=>v.city===k);
       return `<section class="stsec" id="st-${k}"><h3 class="sgh"><span>${esc(CITIES[k].ko)}</span></h3><p class="stsub">${esc(DRINK_INTRO[k])}</p>
        <div class="dlist">${vs.map(v=>`<div class="dmini"><span class="dkind dk-${v.k}">${DRINK_KIND[v.k]}</span><b>${esc(v.n)}</b><small>${esc(v.area)}</small></div>`).join("")}</div>
        <p class="dbuyl"><b>사 가면 좋은 술</b>${(DRINK_BUY[k]||[]).map(v=>`<span>${esc(v.n)}</span>`).join("")}</p>
        <p class="stmore">${drinkA(k,`${esc(CITIES[k].ko)} 술 여행 자세히 보기<i> →</i>`,"more")}</p></section>`; }).join("")}
     ${drinkList("술 살 때 팁", DRINK_SHOP)}
     ${drinkList("양조장·증류소 견학 팁", DRINK_VISIT)}
     <section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>
      ${qa(drinkHomeQ(), `<span>${esc(drinkCarry()[0])}</span>`)}
      ${qa("비행기에 술을 실을 수 있나요?", `<span>${esc(DRINK_CARRY[1])}</span> <span>${esc(DRINK_CARRY[2])}</span>`)}
     </dl></section>
     ${drinkList("술을 가지고 올 때", drinkCarry())}
     ${note}
    </div>`;
  }
  const vs = DRINKS.filter(v=>v.city===c), n = esc(CITIES[c].ko), free = vs.filter(v=>v.rv&&v.rv.startsWith("필요 없음"));
  return `<div class="wx">
   <nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${bc(1,drinkA("all","일본 술 여행 – 지역별 사케·맥주·위스키"))}</nav>
   <div class="ghead"><h2>${n} 술 여행</h2><p>${esc(DRINK_INTRO[c])}</p></div>
   ${drinkChips(c)}
   <h3 class="sgh"><span>견학·시음할 수 있는 곳</span></h3>
   <div class="dgrid">${vs.map(drinkCard).join("")}</div>
   <h3 class="sgh"><span>사 가면 좋은 술</span></h3>
   <div class="dgrid">${(DRINK_BUY[c]||[]).map(drinkBuyCard).join("")}</div>
   ${drinkList("술 살 때 팁", DRINK_SHOP)}
   ${note}
   <section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>
    ${free.length?qa(`${n}에서 예약 없이 들를 수 있는 곳은 어디인가요?`, free.map(v=>`<span><b>${esc(v.n)}</b> (<span>${esc(v.area)}</span>)</span>`).join(" / ")):""}
    ${(DRINK_BUY[c]||[]).length?qa(`${n}에서 사 갈 만한 술은 무엇인가요?`, DRINK_BUY[c].map(v=>`<span><b>${esc(v.n)}</b> (<span>${DRINK_KIND[v.k]}</span>)</span>`).join(" / ")):""}
    ${qa("견학할 때 시음을 못 하는 경우가 있나요?", `<span>${esc(DRINK_VISIT[0])}</span> <span>${esc(DRINK_VISIT[1])}</span>`)}
    ${qa(drinkHomeQ(), `<span>${esc(drinkCarry()[0])}</span>`)}
   </dl></section>
   <div class="wxlinks">${drinkA("all",`일본 술 종류와 라벨 읽는 법<i> →</i>`,"btn ghost")}${typeof stayA==="function"?stayA(c,`${n} 숙소 추천<i> →</i>`,"btn ghost"):""}</div>
  </div>`;
};
/*DRINK_END*/
