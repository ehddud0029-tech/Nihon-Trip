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
  {k:"sake", n:"사와노이", ja:"澤乃井", d:"도쿄 오메에서 빚는 도쿄 지역 사케. 깔끔한 맛이라 처음 마시는 사람에게도 무난해요.", w:"양조장 매장, 도쿄 백화점 주류 코너", p:"720ml 약 1,500~2,500엔", t:"맛: 물처럼 맑고 깔끔하며 끝맛이 가벼워요."},
  {k:"whisky", n:"기린 싱글 그레인 위스키 후지", ja:"キリン シングルグレーンウイスキー 富士", d:"후지산 기슭 후지고텐바 증류소의 위스키. 부드럽고 달콤한 향이에요.", w:"증류소 매장, 큰 주류점·백화점", p:"700ml 약 5,000~6,000엔", t:"맛: 바닐라와 꿀 같은 달콤한 향에 부드러운 목 넘김이에요."},
  {k:"sake", n:"닷사이", ja:"獺祭", d:"야마구치현 사케지만 과일 향이 화사한 준마이 다이긴조로 인기가 많아 도쿄에서도 쉽게 살 수 있어요.", w:"백화점, 공항 면세점", p:"720ml 약 2,000~3,000엔 (상위 등급은 더 비싸요)", t:"맛: 멜론·사과 같은 과일 향이 화사하고 단맛이 은은해요."}],
 osaka:[
  {k:"sake", n:"나다·후시미 사케", ja:"灘・伏見の酒", d:"하쿠쓰루·기쿠마사무네(나다), 겟케이칸(후시미) 등 간사이 대표 양조장의 사케예요.", w:"양조장 기념관 매장, 오사카·교토 백화점", p:"720ml 약 1,000~3,000엔", t:"맛: 나다는 쌉쌀하고 힘 있는 맛, 후시미는 부드럽고 순한 맛이에요."},
  {k:"umeshu", n:"초야 우메슈", ja:"チョーヤ梅酒", d:"오사카 하비키노에 본사가 있는 우메슈 회사. 매실이 든 병이나 작은 병 세트가 선물하기 좋아요.", w:"슈퍼, 백화점, 공항", p:"720ml 약 1,000~1,500엔", t:"맛: 매실 향이 진하고 새콤달콤해요. 얼음에 타 마시기 좋아요."},
  {k:"whisky", n:"야마자키", ja:"山崎", d:"일본 첫 몰트위스키 증류소의 위스키. 인기가 많아 일반 매장에서는 구하기 어려운 경우가 많아요.", w:"증류소 매장(수량 한정), 백화점", p:"700ml 약 7,000엔 (정가, 실제로는 더 비싼 경우가 많아요)", t:"맛: 딸기·체리 같은 과일 향과 일본 오크(미즈나라)의 은은한 향이에요."}],
 fukuoka:[
  {k:"shochu", n:"구로키리시마", ja:"黒霧島", d:"미야자키현의 고구마 소주. 규슈에서 가장 흔히 마시는 소주 가운데 하나예요.", w:"슈퍼, 주류점, 공항", p:"900ml 약 1,000~1,500엔", t:"맛: 고구마 향이 은은하고 단맛이 돌며 뒷맛이 깔끔해요."},
  {k:"shochu", n:"이이치코", ja:"いいちこ", d:"오이타현의 보리 소주. 향이 순해서 물이나 탄산수에 타 마시기 좋아요.", w:"슈퍼, 주류점, 공항", p:"720ml 약 1,000엔", t:"맛: 보리의 고소한 향이 가볍고 순해서 부담이 없어요."},
  {k:"sake", n:"시게마스", ja:"繁桝", d:"후쿠오카현 야메의 오래된 양조장 사케. 후쿠오카 지역 사케를 찾는다면 좋은 선택이에요.", w:"하카타역·백화점 기념품 매장", p:"720ml 약 1,500~3,000엔", t:"맛: 쌀의 감칠맛이 살아 있는 부드럽고 균형 잡힌 맛이에요."}],
 hokkaido:[
  {k:"beer", n:"삿포로 클래식", ja:"サッポロクラシック", d:"홋카이도에서만 파는 삿포로 맥주. 여행 중에 꼭 마셔 볼 만해요.", w:"홋카이도 슈퍼·편의점, 신치토세 공항", p:"350ml 캔 약 250엔", t:"맛: 보리 맛이 진하면서도 깔끔하고 시원해요."},
  {k:"whisky", n:"싱글 몰트 요이치", ja:"シングルモルト余市", d:"닛카 요이치 증류소의 몰트위스키. 증류소에서만 파는 위스키도 있어요.", w:"요이치 증류소 매장, 백화점", p:"700ml 약 7,700엔 (정가)", t:"맛: 석탄 직화 증류에서 오는 스모키한 향과 묵직한 맛이에요."},
  {k:"sake", n:"오토코야마·구니마레", ja:"男山・国稀", d:"아사히카와의 오토코야마, 마시케의 구니마레 등 추운 북쪽에서 빚는 깔끔한 사케예요.", w:"양조장 매장, 삿포로 백화점", p:"720ml 약 1,500~3,000엔", t:"맛: 쌉쌀하고 깔끔한 가라쿠치(드라이)가 많아요."},
  {k:"wine", n:"오타루 와인", ja:"おたるワイン", d:"홋카이도산 포도로 만든 오타루의 와인. 오타루 관광 기념품으로 많이 사요.", w:"오타루 운하 근처 기념품 매장, 홋카이도 슈퍼", p:"720ml 약 1,500~2,500엔", t:"맛: 산뜻한 산미의 가벼운 화이트 와인이 많아요."}],
 okinawa:[
  {k:"awamori", n:"구스(오래 숙성한 아와모리)", ja:"古酒（クース）", d:"3년 넘게 숙성한 아와모리. 양조장 매장에서 시음해 보고 고를 수 있어요.", w:"양조장 매장, 국제거리 주류점", p:"720ml 약 2,000~5,000엔 (오래 숙성할수록 비싸요)", t:"맛: 바닐라 같은 단 향이 나고 숙성될수록 부드러워요."},
  {k:"awamori", n:"잔파", ja:"残波", d:"요미탄의 아와모리. 향이 부드러워 처음 마시는 사람에게도 무난해요.", w:"슈퍼, 공항", p:"720ml 약 1,500엔", t:"맛: 과일 같은 향이 나고 아와모리치고 순해요."},
  {k:"beer", n:"오리온 드래프트", ja:"オリオン ドラフト", d:"오키나와를 대표하는 맥주. 가볍고 시원한 맛이라 더운 날씨에 잘 어울려요.", w:"슈퍼·편의점, 나하 공항", p:"350ml 캔 약 250엔", t:"맛: 가볍고 상쾌해서 더운 날 벌컥 마시기 좋아요."}],
 nagoya:[
  {k:"sake", n:"히다 다카야마 사케", ja:"飛騨高山の酒", d:"하라다 주조의 '산샤', 히라세 주조의 '구스다마', 후나사카 주조의 '미야마기쿠' 등 옛 거리 양조장의 사케예요.", w:"다카야마 옛 거리 양조장 매장", p:"720ml 약 1,500~3,000엔", t:"맛: 쌀 맛이 풍부하고 단단한 맛이 많아요."},
  {k:"sake", n:"구니자카리", ja:"國盛", d:"아이치현 한다의 나카노 주조 사케. 나고야 근처에서 쉽게 살 수 있어요.", w:"나고야 백화점, 기념품 매장", p:"720ml 약 1,000~2,000엔", t:"맛: 순하고 부드러워 식사와 함께 마시기 편해요."},
  {k:"beer", n:"긴샤치 맥주", ja:"金しゃちビール", d:"아이치현의 지역 맥주. 이름은 나고야성 지붕의 황금 샤치호코 장식에서 왔어요.", w:"나고야역 기념품 매장", p:"330ml 병 약 400~600엔", t:"맛: 종류가 여러 가지이고, 진하고 향이 풍부한 수제 맥주예요."}],
 hiroshima:[
  {k:"sake", n:"사이조 사케", ja:"西条の酒", d:"가모쓰루·하쿠보탄·가모이즈미·기레이 등 '사케의 도시' 사이조 양조장의 사케예요.", w:"사이조 양조장 매장, 히로시마역 기념품 매장", p:"720ml 약 1,500~3,000엔", t:"맛: 연수로 빚어 부드럽고 은은한 단맛이 있어요."},
  {k:"liqueur", n:"세토우치 레몬 술", ja:"瀬戸内レモンのお酒", d:"히로시마는 일본 최대 레몬 산지예요. 레몬 리큐어나 레몬 사와가 기념품으로 많아요.", w:"히로시마역 기념품 매장, 공항", p:"캔 약 200~300엔, 병 약 1,000~2,000엔", t:"맛: 레몬 껍질 향이 상큼하고 새콤해요."}],
 shikoku:[
  {k:"sake", n:"고치 사케", ja:"土佐の酒", d:"쓰카사보탄·스이게이·도사쓰루 등 깔끔하고 쌉쌀한 맛의 고치 사케예요.", w:"고치 백화점·역 기념품 매장", p:"720ml 약 1,500~3,000엔", t:"맛: 단맛이 적고 쌉쌀해서 생선 요리와 잘 어울려요."},
  {k:"beer", n:"도고 맥주", ja:"道後ビール", d:"마쓰야마 도고온천의 지역 맥주. '봇짱'·'마돈나' 등 소설에서 딴 이름이 붙어 있어요.", w:"도고온천 상점가, 마쓰야마 공항", p:"330ml 병 약 500~600엔", t:"맛: 종류마다 달라요. 쾰시·에일 등 향이 좋은 수제 맥주예요."},
  {k:"sake", n:"긴료", ja:"金陵", d:"가가와 고토히라의 양조장 사케. 곤피라 참배 기념품으로 좋아요.", w:"긴료노사토, 고토히라 상점가", p:"720ml 약 1,500~3,000엔", t:"맛: 쌀의 단맛이 은은하고 부드러워요."},
  {k:"liqueur", n:"유자 술", ja:"ゆず酒", d:"일본 최대 유자 산지 고치의 유자로 만든 리큐어. 상큼해서 술이 약한 사람도 마시기 쉬워요.", w:"고치 기념품 매장", p:"720ml 약 1,500~2,500엔", t:"맛: 유자 향이 상큼하고 달콤해서 디저트처럼 마셔요."}],
};
/*DRPHOTO*/const DRINK_PHOTO = {"사와노이":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/0/00/Ozawa_shuzo_211009.jpg/960px-Ozawa_shuzo_211009.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Ozawa shuzo 211009.jpg","artist":"江戸村のとくぞう","license":"CC BY-SA 4.0"},"기린 싱글 그레인 위스키 후지":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c5/Fuji_Gotemba_distillery05.jpg/960px-Fuji_Gotemba_distillery05.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Fuji Gotemba distillery05.jpg","artist":"Keeezawa","license":"CC0"},"닷사이":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/7/7f/%E7%8D%BA%E7%A5%AD_%E9%8C%A6%E5%B8%AF%E6%A9%8B.jpg/960px-%E7%8D%BA%E7%A5%AD_%E9%8C%A6%E5%B8%AF%E6%A9%8B.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"獺祭 錦帯橋.jpg","artist":"Breizhiz75","license":"CC BY-SA 4.0"},"나다·후시미 사케":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/5/5e/Gekkeikanbottle.JPG/960px-Gekkeikanbottle.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Gekkeikanbottle.JPG","artist":"Fotonovela","license":"CC BY-SA 3.0"},"야마자키":{"src":"https://upload.wikimedia.org/wikipedia/commons/e/e4/The_Yamazaki_Single_Malt_Whisky_Aged_12_years.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled","file":"The Yamazaki Single Malt Whisky Aged 12 years.JPG","artist":"Look Sharp!","license":"CC BY-SA 3.0"},"구로키리시마":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/2/21/%E9%BB%92%E9%9C%A7%E5%B3%B6_20%E5%BA%A6900ML%E7%93%B6%E8%A1%A8%E9%9D%A2.jpg/960px-%E9%BB%92%E9%9C%A7%E5%B3%B6_20%E5%BA%A6900ML%E7%93%B6%E8%A1%A8%E9%9D%A2.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"黒霧島 20度900ML瓶表面.jpg","artist":"A-sonoda","license":"CC BY-SA 4.0"},"이이치코":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f1/Iichiko_%E3%81%84%E3%81%84%E3%81%A1%E3%81%93_%2830726907326%29.jpg/960px-Iichiko_%E3%81%84%E3%81%84%E3%81%A1%E3%81%93_%2830726907326%29.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Iichiko いいちこ (30726907326).jpg","artist":"ayustety","license":"CC BY-SA 2.0"},"삿포로 클래식":{"src":"https://upload.wikimedia.org/wikipedia/commons/d/d5/%E3%82%B5%E3%83%83%E3%83%9D%E3%83%AD%E3%82%AF%E3%83%A9%E3%82%B7%E3%83%83%E3%82%AF.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled","file":"サッポロクラシック.JPG","artist":"Mininomo","license":"CC BY-SA 3.0"},"싱글 몰트 요이치":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/c/ce/JapaneseNikkaWhiskyYoichiWoodyVanillic.jpg/960px-JapaneseNikkaWhiskyYoichiWoodyVanillic.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"JapaneseNikkaWhiskyYoichiWoodyVanillic.jpg","artist":"サフィル","license":"CC BY-SA 4.0"},"오토코야마·구니마레":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/0/00/Otokoyama%2C_Asahikawa.jpg/960px-Otokoyama%2C_Asahikawa.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Otokoyama, Asahikawa.jpg","artist":"K. Takeda","license":"CC BY-SA 3.0"},"오타루 와인":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/5/52/Hokkaido_wine.JPG/960px-Hokkaido_wine.JPG?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Hokkaido wine.JPG","artist":"星組背番号10","license":"CC BY-SA 3.0"},"구스(오래 숙성한 아와모리)":{"src":"https://upload.wikimedia.org/wikipedia/commons/6/66/Various_Awamori_bottles_by_jetalone_in_Ginza%2C_Tokyo.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail_unscaled","file":"Various Awamori bottles by jetalone in Ginza, Tokyo.jpg","artist":"jetalone from Ginza, Tokyo","license":"CC BY 2.0"},"오리온 드래프트":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/f/f3/Orion_beer_350ml_can_01.jpg/960px-Orion_beer_350ml_can_01.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Orion beer 350ml can 01.jpg","artist":"妖精書士","license":"CC0"},"히다 다카야마 사케":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/2/25/Sake_shop_-Takayama.jpg/960px-Sake_shop_-Takayama.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Sake shop -Takayama.jpg","artist":"Kat Clay from Sydney, Australia","license":"CC BY 2.0"},"구니자카리":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/6/64/Kunizakari_Sake_no_Bunkakan_Museum_ac.jpg/960px-Kunizakari_Sake_no_Bunkakan_Museum_ac.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Kunizakari Sake no Bunkakan Museum ac.jpg","artist":"Asturio Cantabrio","license":"CC BY-SA 4.0"},"사이조 사케":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/6/69/%E9%85%92%E8%94%B5%E9%80%9A%E3%82%8A_%E8%B3%80%E8%8C%82%E9%B6%B4_Sake_brewery_%22Kamotsuru%22_-_panoramio.jpg/960px-%E9%85%92%E8%94%B5%E9%80%9A%E3%82%8A_%E8%B3%80%E8%8C%82%E9%B6%B4_Sake_brewery_%22Kamotsuru%22_-_panoramio.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"酒蔵通り 賀茂鶴 Sake brewery \"Kamotsuru\" - panoramio.jpg","artist":"OS6","license":"CC BY-SA 3.0"},"세토우치 레몬 술":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/2/25/NGO_Kita_s20260303_192954_%E7%84%A1%E7%B3%96%E3%83%AC%E3%83%A2%E3%83%B3%E3%82%B5%E3%83%AF%E3%83%BC.jpg/960px-NGO_Kita_s20260303_192954_%E7%84%A1%E7%B3%96%E3%83%AC%E3%83%A2%E3%83%B3%E3%82%B5%E3%83%AF%E3%83%BC.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"NGO Kita s20260303 192954 無糖レモンサワー.jpg","artist":"円周率３パーセント","license":"CC BY-SA 4.0"},"고치 사케":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/6/6b/%E7%B4%94%E7%B1%B3%E5%90%9F%E9%86%B8_%E9%85%94%E9%AF%A8.jpg/960px-%E7%B4%94%E7%B1%B3%E5%90%9F%E9%86%B8_%E9%85%94%E9%AF%A8.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"純米吟醸 酔鯨.jpg","artist":"Kozakura154","license":"CC BY 4.0"},"도고 맥주":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/0/09/Dogo_Beer.jpg/960px-Dogo_Beer.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Dogo Beer.jpg","artist":"Kanatam...","license":"CC BY-SA 3.0"},"긴료":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/b/bb/Kotohira_Nishino-Kinryo_2021-08_ac.jpg/960px-Kotohira_Nishino-Kinryo_2021-08_ac.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Kotohira Nishino-Kinryo 2021-08 ac.jpg","artist":"Asturio Cantabrio","license":"CC BY-SA 4.0"},"유자 술":{"src":"https://thumb.wikimedia.org/wikipedia/commons/thumb/c/c0/Yuzufruit.jpg/960px-Yuzufruit.jpg?utm_source=commons.wikimedia.org&utm_campaign=imageinfo&utm_content=thumbnail","file":"Yuzufruit.jpg","artist":"Nagarazoku from TOKYO, Japan","license":"CC BY-SA 2.0"}};/*DRPHOTO_END*/
const DRINK_STORES = [
 ["백화점 지하 식품관 (데파치카)","지역 사케·와인·위스키가 모여 있고, 시음 코너가 있는 곳도 많아요. 선물 포장도 해 줘요."],
 ["주류 전문점·할인점","야마야·카쿠야스·리커 마운틴 같은 체인은 종류가 많고 값이 싼 편이에요."],
 ["슈퍼·편의점","맥주·추하이·작은 병 사케를 쉽게 살 수 있어요. 그 지역에서만 파는 맥주도 있어요."],
 ["돈키호테·대형 가전 매장","위스키 코너가 큰 곳이 많고 늦게까지 열어요."],
 ["공항 면세점","출국 심사를 마친 뒤 사면 기내에 들고 탈 수 있어요. 시내보다 종류가 적을 수 있어요."],
 ["양조장·증류소 직매장","그곳에서만 파는 술이나 생술을 살 수 있고, 시음해 보고 고를 수 있어요."]];
const DRINK_SHOP = ["가격대는 2026년 11월 일본 매장 기준 대략적인 값이에요. 매장과 시기에 따라 달라요.","백화점 지하 식품관 주류 코너에는 지역 술이 모여 있고, 시음해 보고 고를 수 있는 곳도 많아요.",
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
const DRINK_TABS = ["","buy","tips","shops"];
const DRINK_TAB_LABEL = {"":"견학·시음할 수 있는 곳", buy:"사 가면 좋은 술", tips:"술 살 때 팁", shops:"술을 사는 매장"};
const drinkHref = (c,t) => ROUTED ? window.NT_BASE + LPRE + (c && c!=="all" ? `${c}/drink/${t?t+"/":""}` : "drink/") : "#drink";
const drinkA = (c,inner,cls,t) => `<a${cls?` class="${cls}"`:""} href="${drinkHref(c,t)}" data-drc="${c||"all"}" data-drt="${t||""}">${inner}</a>`;
function drinkChips(cur,t){ return `<div class="wxmon">${DRINK_CITIES.map(k=>drinkA(k,esc(CITIES[k].ko),k===cur?"on":"",t)).join("")}</div>`; }
function drinkTabs(c,t){ return `<nav class="dtabs" aria-label="술 여행">${DRINK_TABS.map(k=>drinkA(c,esc(DRINK_TAB_LABEL[k]),k===t?"on":"",k).replace("<a ",k===t?'<a aria-current="page" ':"<a ")).join("")}</nav>`; }
const drinkList = (h,items) => `<div class="gblk"><h4>${h}</h4><ul class="gul">${items.map(x=>`<li>${esc(x)}</li>`).join("")}</ul></div>`;
function drinkCard(v){
  const row=(a,b)=>b?`<dt>${a}</dt><dd>${esc(b)}</dd>`:"";
  return `<article class="dcard"><div class="dtop"><span class="dkind dk-${v.k}">${DRINK_KIND[v.k]}</span><span class="harea">${esc(v.area)}</span></div>
   <h3>${esc(v.n)}</h3>${v.ja&&v.ja!==v.n?`<p class="hja notranslate" lang="ja">${esc(v.ja)}</p>`:""}<p class="dd">${esc(v.d)}</p>
   <dl>${row("요금",v.fee)}${row("예약",v.rv)}${row("시간",v.h)}${row("휴무",v.cl)}${row("가는 길",v.st)}</dl>
   <a class="more" href="${v.u}" target="_blank" rel="noopener">${v.o===0?"안내 페이지 ↗":"공식 사이트 ↗"}</a></article>`;
}
const DRINK_ART = {
 sake:   ["#3d6f8e","#e8f0f5",'<path d="M44 14h12v14c0 4 10 8 10 22v46c0 4-3 6-6 6H40c-3 0-6-2-6-6V50c0-14 10-18 10-22z" fill="#fff" opacity=".95"/><rect x="38" y="58" width="24" height="26" rx="2" fill="#fffdf8"/><path d="M50 62v18M45 67h10M45 74h10" stroke="#3d6f8e" stroke-width="2.2"/>'],
 shochu: ["#6b5b95","#eeebf4",'<path d="M45 12h10v16c0 3 9 6 9 18v50c0 4-3 6-6 6H42c-3 0-6-2-6-6V46c0-12 9-15 9-18z" fill="#fff" opacity=".95"/><rect x="40" y="56" width="20" height="30" rx="2" fill="#fffdf8"/><circle cx="50" cy="71" r="6" fill="none" stroke="#6b5b95" stroke-width="2.2"/>'],
 awamori:["#2f7d6b","#e6f2ef",'<path d="M38 40c0-8 6-12 6-18h12c0 6 6 10 6 18v52c0 5-4 8-8 8H46c-4 0-8-3-8-8z" fill="#fff" opacity=".95"/><rect x="44" y="14" width="12" height="9" rx="2" fill="#fff"/><path d="M38 64h24" stroke="#2f7d6b" stroke-width="10"/><path d="M42 64h16" stroke="#2f7d6b" stroke-width="2" stroke-dasharray="3 3"/>'],
 beer:   ["#c08a1e","#faf1de",'<path d="M46 12h8v14c0 3 7 6 7 15v53c0 4-3 6-6 6H45c-3 0-6-2-6-6V41c0-9 7-12 7-15z" fill="#fff" opacity=".95"/><ellipse cx="50" cy="66" rx="9" ry="12" fill="#fffdf8"/><path d="M50 58v16" stroke="#c08a1e" stroke-width="2.2"/><circle cx="50" cy="12" r="5" fill="#fff"/>'],
 whisky: ["#8a4b2a","#f5ece6",'<rect x="45" y="10" width="10" height="16" rx="2" fill="#fff"/><path d="M36 34c0-5 4-8 9-8h10c5 0 9 3 9 8v58c0 4-3 7-7 7H43c-4 0-7-3-7-7z" fill="#fff" opacity=".95"/><rect x="40" y="52" width="20" height="24" rx="2" fill="#fffdf8"/><path d="M44 60h12M44 66h12" stroke="#8a4b2a" stroke-width="2"/>'],
 umeshu: ["#b5536b","#f8e9ed",'<rect x="44" y="12" width="12" height="10" rx="2" fill="#fff"/><path d="M36 30c0-5 4-8 8-8h12c4 0 8 3 8 8v62c0 4-3 7-7 7H43c-4 0-7-3-7-7z" fill="#fff" opacity=".95"/><circle cx="45" cy="80" r="6" fill="#d9a441"/><circle cx="55" cy="84" r="6" fill="#c9922f"/><circle cx="50" cy="72" r="6" fill="#e0b04a"/>'],
 wine:   ["#7a2e45","#f4e7eb",'<path d="M46 10h8v22c0 4 8 7 8 18v44c0 4-3 6-6 6H44c-3 0-6-2-6-6V50c0-11 8-14 8-18z" fill="#fff" opacity=".95"/><rect x="41" y="60" width="18" height="20" rx="2" fill="#fffdf8"/>'],
 liqueur:["#c2701a","#fbefe2",'<path d="M44 12h12v12c0 3 10 8 10 20v50c0 4-3 6-6 6H40c-3 0-6-2-6-6V44c0-12 10-17 10-20z" fill="#fff" opacity=".95"/><circle cx="50" cy="70" r="10" fill="#e7c23a"/><path d="M50 60v-6" stroke="#5b8a3a" stroke-width="3"/>'],
};
const drinkArt = k => { const [c,bg,body]=DRINK_ART[k]||DRINK_ART.sake; return `<figure class="dph dart" aria-hidden="true" style="background:${bg}"><svg viewBox="0 0 100 110" width="150" height="165"><rect x="0" y="100" width="100" height="10" fill="${c}" opacity=".18"/><g style="filter:drop-shadow(0 2px 3px rgba(0,0,0,.18))">${body.replace(/<path d="M(\d)/,`<path fill="${c}" d="M$1`)}</g></svg></figure>`; };
const drinkMap = q => `https://www.google.com/maps/search/?api=1&query=${encodeURIComponent(q)}`;
const DRINK_STORE_Q = ["デパ地下 酒売り場","酒 ディスカウント","スーパー","ドン・キホーテ","空港 免税店","酒蔵 直売所"];
function drinkBuyCard(v,c){
  const ph = DRINK_PHOTO[v.n];
  const art = ph ? "" : drinkArt(v.k);
  const fig = ph ? `<figure class="dph"><img src="${esc(ph.src)}" alt="${esc((window.__tr||(x=>x))(v.n))}" decoding="async"><figcaption><a href="https://commons.wikimedia.org/wiki/File:${encodeURIComponent(ph.file.replace(/ /g,"_"))}" target="_blank" rel="noopener">사진</a> <span class="notranslate">${esc(ph.artist)} · ${esc(ph.license)}</span></figcaption></figure>` : "";
  return `<article class="dcard dbuy">${fig||art}<div class="dtop"><span class="dkind dk-${v.k}">${DRINK_KIND[v.k]}</span></div>
   <h3>${esc(v.n)}</h3><p class="hja notranslate" lang="ja">${esc(v.ja)}</p><p class="dd">${esc(v.d)}</p>${v.t?`<p class="dtaste">${esc(v.t)}</p>`:""}
   <dl>${v.p?`<dt>가격대</dt><dd>${esc(v.p)}</dd>`:""}<dt>살 수 있는 곳</dt><dd>${esc(v.w)}</dd></dl>
   ${c&&CITIES[c]?`<a class="more dmap" href="${drinkMap(`${v.ja.split("（")[0]} ${CITIES[c].jp}`)}" target="_blank" rel="noopener">구글 지도에서 파는 곳 찾기 ↗</a>`:""}</article>`;
}
V.drink = function(){
  const c = DRINK_CITIES.includes(st.city) ? st.city : "";
  const bc=(i,h)=>`<span itemprop="itemListElement" itemscope itemtype="https://schema.org/ListItem">${h.replace("<a ",'<a itemprop="item" ').replace(/>([^<]*)<\/a>$/,'><span itemprop="name">$1</span></a>')}<meta itemprop="position" content="${i}"></span>`;
  const qa=(q,x)=>`<div class="faqi" itemscope itemprop="mainEntity" itemtype="https://schema.org/Question"><dt itemprop="name">${q}</dt><dd itemscope itemprop="acceptedAnswer" itemtype="https://schema.org/Answer"><div itemprop="text">${x}</div></dd></div>`;
  const note = `<p class="sisrc">2026년 11월 각 공식 사이트 기준이에요. 요금·시간·예약 방식은 바뀔 수 있어요. 술은 20세부터, 운전 전에는 마시지 마세요.</p>`;
  if(!c){
    const tabs = [["","지역별 견학·시음"],["types","술 종류와 라벨"],["visit","견학 팁"],["carry","가지고 올 때"]], t = tabs.some(x=>x[0]===st.sub)?st.sub:"";
    let body;
    if(t==="types") body = `<div class="dtypes">${DRINK_TYPES.map(([a,b])=>`<div class="gblk"><h4>${esc(a)}</h4><p>${esc(b)}</p></div>`).join("")}</div>
     ${drinkList("사케 라벨 읽는 법", DRINK_LABEL)}
     ${drinkList("주문할 때 알아 둘 말", DRINK_ORDER)}`;
    else if(t==="visit") body = `${drinkList("양조장·증류소 견학 팁", DRINK_VISIT)}
     <section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>${qa("견학할 때 시음을 못 하는 경우가 있나요?", `<span>${esc(DRINK_VISIT[0])}</span> <span>${esc(DRINK_VISIT[1])}</span>`)}</dl></section>`;
    else if(t==="carry") body = `${drinkList("술을 가지고 올 때", drinkCarry())}
     <section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>
      ${qa(drinkHomeQ(), `<span>${esc(drinkCarry()[0])}</span>`)}
      ${qa("비행기에 술을 실을 수 있나요?", `<span>${esc(DRINK_CARRY[1])}</span> <span>${esc(DRINK_CARRY[2])}</span>`)}
     </dl></section>`;
    else body = `<nav class="wxmon stjump">${DRINK_CITIES.map(k=>drinkA(k,esc(CITIES[k].ko))).join("")}</nav>
     ${DRINK_CITIES.map(k=>{ const vs=DRINKS.filter(v=>v.city===k);
       return `<section class="stsec" id="st-${k}"><h3 class="sgh"><span>${esc(CITIES[k].ko)}</span></h3><p class="stsub">${esc(DRINK_INTRO[k])}</p>
        <div class="dlist">${vs.map(v=>`<div class="dmini"><span class="dkind dk-${v.k}">${DRINK_KIND[v.k]}</span><b>${esc(v.n)}</b><small>${esc(v.area)}</small></div>`).join("")}</div>
        <p class="dbuyl"><b>사 가면 좋은 술</b>${(DRINK_BUY[k]||[]).map(v=>`<span>${esc(v.n)}</span>`).join("")}</p>
        <div class="wxlinks dsub" style="margin-top:12px">${DRINK_TABS.map(t2=>drinkA(k,`${esc(DRINK_TAB_LABEL[t2])}<i> →</i>`,"btn ghost",t2)).join("")}</div></section>`; }).join("")}`;
    return `<div class="wx">
     <div class="ghead"><h2>일본 술 여행 – 지역별 사케·맥주·위스키</h2><p>일본 술의 종류와 고르는 법, 지역별로 견학·시음할 수 있는 양조장과 증류소, 한국에 가져올 때의 규칙까지 정리했어요.</p></div>
     ${subTabs(tabs,t)}
     ${body}
     ${note}
    </div>`;
  }
  const vs = DRINKS.filter(v=>v.city===c), n = esc(CITIES[c].ko), free = vs.filter(v=>v.rv&&v.rv.startsWith("필요 없음")), t = DRINK_TABS.includes(st.dtab)?st.dtab:"", buy = DRINK_BUY[c]||[];
  let body = "", faq = [];
  if(t===""){
    body = `<div class="dgrid">${vs.map(drinkCard).join("")}</div>${drinkList("양조장·증류소 견학 팁", DRINK_VISIT)}`;
    if(free.length) faq.push(qa(`${n}에서 예약 없이 들를 수 있는 곳은 어디인가요?`, free.map(v=>`<span><b>${esc(v.n)}</b> (<span>${esc(v.area)}</span>)</span>`).join(" / ")));
    faq.push(qa("견학할 때 시음을 못 하는 경우가 있나요?", `<span>${esc(DRINK_VISIT[0])}</span> <span>${esc(DRINK_VISIT[1])}</span>`));
  } else if(t==="buy"){
    body = `<div class="dgrid">${buy.map(v=>drinkBuyCard(v,c)).join("")}</div><p class="sisrc">${esc(DRINK_SHOP[0])}</p>`;
    if(buy.length) faq.push(qa(`${n}에서 사 갈 만한 술은 무엇인가요?`, buy.map(v=>`<span><b>${esc(v.n)}</b> (<span>${DRINK_KIND[v.k]}</span>)</span>`).join(" / ")));
  } else if(t==="tips"){
    body = `${drinkList("술 살 때 팁", DRINK_SHOP.slice(1))}${drinkList("사케 라벨 읽는 법", DRINK_LABEL)}${drinkList("술을 가지고 올 때", drinkCarry())}`;
    faq.push(qa(drinkHomeQ(), `<span>${esc(drinkCarry()[0])}</span>`));
    faq.push(qa("비행기에 술을 실을 수 있나요?", `<span>${esc(DRINK_CARRY[1])}</span> <span>${esc(DRINK_CARRY[2])}</span>`));
  } else {
    const shops = vs.filter(v=>["sake","whisky","awamori"].includes(v.k)&&v.n!=="일본 술 정보관");
    body = `<div class="dtypes">${DRINK_STORES.map(([a,b],i)=>`<div class="gblk"><h4>${esc(a)}</h4><p>${esc(b)}</p><p><a class="more" href="${drinkMap(`${DRINK_STORE_Q[i]} ${CITIES[c].jp}`)}" target="_blank" rel="noopener">구글 지도에서 ${esc(CITIES[c].ko)} 매장 찾기 ↗</a></p></div>`).join("")}</div>
     ${buy.length?`<div class="gblk"><h4>추천 술을 살 수 있는 곳</h4><dl class="dwhere">${buy.map(v=>`<dt>${esc(v.n)}</dt><dd>${esc(v.w)} · <a href="${drinkMap(`${v.ja.split("（")[0]} ${CITIES[c].jp}`)}" target="_blank" rel="noopener">지도 ↗</a></dd>`).join("")}</dl></div>`:""}
     ${shops.length?`<div class="gblk"><h4>직매장에서 살 수 있는 양조장·증류소</h4><ul class="gul">${shops.map(v=>`<li><b>${esc(v.n)}</b> (<span>${esc(v.area)}</span>)</li>`).join("")}</ul></div>`:""}`;
  }
  return `<div class="wx">
   <nav class="wxcrumb" itemscope itemtype="https://schema.org/BreadcrumbList">${bc(1,drinkA("all","일본 술 여행 – 지역별 사케·맥주·위스키"))}${t?` › ${bc(2,drinkA(c,`${n} 술 여행`))}`:""}</nav>
   <div class="ghead"><h2>${n} 술 여행</h2><p>${esc(DRINK_INTRO[c])}</p></div>
   ${drinkChips(c,t)}
   ${drinkTabs(c,t)}
   <h3 class="sgh"><span>${esc(DRINK_TAB_LABEL[t])}</span></h3>
   ${body}
   ${note}
   ${faq.length?`<section class="gblk faq" itemscope itemtype="https://schema.org/FAQPage"><h4>자주 묻는 질문</h4><dl>${faq.join("")}</dl></section>`:""}
   <div class="wxlinks">${DRINK_TABS.filter(k=>k!==t).map(k=>drinkA(c,`${esc(DRINK_TAB_LABEL[k])}<i> →</i>`,"btn ghost",k)).join("")}${typeof stayA==="function"?stayA(c,`${n} 숙소 추천<i> →</i>`,"btn ghost"):""}</div>
  </div>`;
};
/*DRINK_END*/
