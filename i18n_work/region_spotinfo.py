"""새 지역(나고야·히로시마·시코쿠) 관광지 입장료·운영 시간 (2026년 10월 조사, spot_info_notes.txt 참고)"""
W = lambda ko, en, ja, es, fr: {"ko": ko, "en": en, "ja": ja, "es": es, "fr": fr}
F = "F"
F24 = {"f": "F", "h": [["24h"]]}
FS = {"f": "F", "h": [["shops"]]}
NY = lambda a, b: {"d": [a, b]}
RT = W("왕복", "Round trip", "往復", "Ida y vuelta", "Aller-retour")
OW = W("편도", "One way", "片道", "Solo ida", "Aller simple")
RES = W("온라인 예약 필수", "Online reservation required", "オンライン予約制", "Reserva en línea obligatoria", "Réservation en ligne obligatoire")
IRR = "irr"

INFO = {
 # 나고야
 "n_castle": {"f": [["adult", 500]], "h": [["9:00", "16:30", "16:00"]], "c": [NY([12, 29], [1, 1])],
              "x": W("천수각 내부는 2018년부터 들어갈 수 없어요. 혼마루 어전과 성터는 볼 수 있어요.", "The keep has been closed to visitors since 2018; the Honmaru Palace and grounds are open.", "天守閣は2018年から入場できません。本丸御殿と城内は見学できます。", "La torre está cerrada al público desde 2018; el Palacio Honmaru y el recinto se pueden visitar.", "Le donjon est fermé depuis 2018 ; le palais Honmaru et l'enceinte restent ouverts.")},
 "n_atsuta": F24, "n_osu": FS,
 "n_mirai": {"f": [["deck", 1300]], "h": [["10:00", "21:00", "20:40"]], "hx": [W("토요일은 21:40 입장까지 연장", "Saturdays: last entry 21:40", "土曜は最終入場21:40", "Sábados: última entrada 21:40", "Samedi : dernière entrée 21 h 40")], "c": ["none"]},
 "n_scmaglev": {"f": [["adult", 1200]], "h": [["10:00", "17:30", "17:00"]], "c": ["tue+", NY([12, 28], [1, 1])]},
 "n_toyota": {"f": [["adult", 1000]], "h": [["9:30", "17:00", "16:30"]], "c": ["mon+", "ny"]},
 "n_tokugawa": {"f": [["adult", 2000]], "fx": [W("전시 교체 기간엔 1,600엔", "¥1,600 during exhibition changeovers", "展示替え期間は1,600円", "1.600 ¥ durante los cambios de exposición", "1 600 ¥ pendant les changements d'exposition")], "h": [["10:00", "17:00", "16:30"]], "c": ["mon+", {"t": W("12월 중순~연초", "Mid-December to New Year", "12月中旬〜年始", "De mediados de diciembre a Año Nuevo", "De mi-décembre au Nouvel An")}]},
 "n_ghibli": {"f": [[W("대산책 프리미엄 (평일/주말)", "O-sanpo Premium (weekday/weekend)", "大さんぽプレミアム（平日/土日祝）", "O-sanpo Premium (laborable/fin de semana)", "O-sanpo Premium (semaine/week-end)"), "7,300~"], [W("대산책 (평일/주말)", "O-sanpo (weekday/weekend)", "大さんぽ（平日/土日祝）", "O-sanpo (laborable/fin de semana)", "O-sanpo (semaine/week-end)"), "3,300~"]],
              "fx": [RES], "h": [["10:00", "17:00", 0, "wd"], ["9:00", "17:00", 0, "we"]], "c": ["tue+"]},
 "n_inuyamajo": {"f": [["adult", 1000]], "h": [["9:00", "17:00", "16:30"]], "c": [NY([12, 29], [12, 31])]},
 "n_jokamachi": FS,
 "n_meijimura": {"f": [["adult", 2500]], "h": [["9:30", "17:00", 0, [3, 11]], ["10:00", "16:00", 0, [12, 2]]], "hx": [W("11월 평일은 16:00까지", "Weekdays in November until 16:00", "11月の平日は16:00まで", "Laborables de noviembre hasta las 16:00", "En semaine en novembre jusqu'à 16 h")], "c": [IRR]},
 "n_sanmachi": FS,
 "n_asaichi": {"f": "F", "h": [["7:00", "12:00"]], "hx": ["seas"], "c": ["none"]},
 "n_jinya": {"f": [["adult", 440]], "h": [["8:45", "17:00", 0, [3, 10]], ["8:45", "16:30", 0, [11, 2]]], "c": [NY([12, 29], [1, 3])]},
 "n_hidanosato": {"f": [["adult", 700]], "h": [["8:30", "17:00"]], "c": ["none"]},
 "n_shinhotaka": {"f": [[RT, 3800]], "h": [["8:30", "16:00", 0, [4, 11]], ["9:00", "15:30", 0, [12, 3]]], "c": ["maint"]},
 "n_shirakawa": {"f": [["street_free"]], "h": [["24h"]], "x": W("주민이 사는 마을이에요. 밤에는 조용히 해 주세요.", "People live in the village, so keep quiet at night.", "住民が暮らす集落です。夜は静かに。", "Es un pueblo habitado: guarda silencio por la noche.", "Des habitants y vivent : restez discret la nuit.")},
 "n_shiroyama": {"f": [[W("셔틀버스 편도", "Shuttle bus, one way", "シャトルバス片道", "Lanzadera, solo ida", "Navette, aller simple"), 300]], "fx": [W("걸어서 오르면 무료", "Free if you walk up", "徒歩なら無料", "Gratis si subes a pie", "Gratuit à pied")], "h": [["9:00", "16:00"]], "hx": ["seas"]},
 "n_wada": {"f": [["adult", 400]], "h": [["9:00", "17:00"]], "c": [IRR]},
 # 히로시마
 "h_peacepark": F24, "h_dome": {"f": "F", "h": [["24h"]], "x": W("건물 안에는 들어갈 수 없어요.", "You can't enter the building.", "建物の中には入れません。", "No se puede entrar en el edificio.", "On ne peut pas entrer dans le bâtiment.")},
 "h_museum": {"f": [["adult", 200]], "fx": [W("시간 지정권은 온라인 판매", "Timed tickets sold online", "時間指定券はオンライン販売", "Entradas con hora en línea", "Billets horaires en ligne")], "h": [["7:30", "18:00", 0, [3, 7]], ["7:30", "19:00", 0, [8, 8]], ["7:30", "18:00", 0, [9, 11]], ["7:30", "17:00", 0, [12, 2]]], "hx": ["l30"], "c": [NY([12, 30], [12, 31])]},
 "h_shukkeien": {"f": [["adult", 350]], "h": [["9:00", "18:00", "17:30", [[3, 16], [9, 15]]], ["9:00", "17:00", "16:30", [[9, 16], [3, 15]]]], "c": [NY([12, 29], [12, 31])]},
 "h_castle": {"f": [["park_free"]], "h": [["24h", 0, 0, 0, "grounds"]], "x": W("천수각 내부 관람은 2026년 3월 22일로 끝났어요.", "Visits inside the keep ended on March 22, 2026.", "天守閣内部の観覧は2026年3月22日で終了しました。", "Las visitas al interior de la torre terminaron el 22 de marzo de 2026.", "Les visites du donjon ont pris fin le 22 mars 2026.")},
 "h_orizuru": {"f": [["deck", "2,200~"]], "h": [["10:00", "18:00", "17:30"]], "c": [NY([12, 31], [12, 31])]},
 "h_itsukushima": {"f": [["adult", 300]], "h": [["6:30", "18:00"]], "hx": ["seas"], "c": ["none"],
                   "x": W("미야지마에 들어갈 때 1인 100엔의 방문세를 내요.", "A ¥100 visitor tax applies when you enter Miyajima.", "宮島に入る際、1人100円の宮島訪問税がかかります。", "Al entrar en Miyajima se paga una tasa de 100 ¥ por persona.", "Une taxe de visite de 100 ¥ par personne s'applique à Miyajima.")},
 "h_misen": {"f": [[RT, 2000]], "h": [["9:00", "16:00"]], "hx": [W("마지막 하행은 16:30", "Last ride down 16:30", "下り最終16:30", "Último descenso 16:30", "Dernière descente 16 h 30")], "c": ["maint"]},
 "h_daishoin": {"f": "F", "h": [["8:00", "17:00"]], "c": ["none"]},
 "h_senkoji": {"f": [["grounds_free"], [W("로프웨이 왕복", "Ropeway round trip", "ロープウェイ往復", "Teleférico i/v", "Téléphérique A/R"), 700]], "h": [["9:00", "17:15", 0, 0, W("로프웨이", "Ropeway", "ロープウェイ", "Teleférico", "Téléphérique")]], "c": ["none"]},
 "h_nekonohosomichi": F24,
 "h_shimanami": {"f": [["street_free"]], "fx": [W("자전거 대여는 따로", "Bike rental extra", "レンタサイクルは別料金", "Alquiler de bici aparte", "Location de vélo en plus")]},
 "h_bikan": FS,
 "h_ohara": {"f": [["adult", 2000]], "h": [["9:00", "17:00", "16:30", [3, 11]], ["9:00", "15:00", 0, [12, 2]]], "c": ["mon+", {"t": W("겨울 휴관 (7월 하순~8월은 무휴)", "Winter break (open daily late July–August)", "冬季休館（7月下旬〜8月は無休）", "Cierre de invierno (abierto a diario de finales de julio a agosto)", "Fermeture hivernale (ouvert tous les jours fin juillet–août)")}]},
 "h_ivy": FS,
 # 시코쿠
 "k_dogo": {"f": [[W("가미노유 1층", "Kami-no-Yu (1F)", "神の湯（1階）", "Kami-no-Yu (1.ª planta)", "Kami-no-Yu (RdC)"), 700]], "h": [["6:00", "23:00", "22:30"]], "c": [{"t": W("12월 중 하루 (청소)", "One day in December (cleaning)", "12月に1日（大掃除）", "Un día de diciembre (limpieza)", "Un jour en décembre (nettoyage)")}]},
 "k_matsuyamajo": {"f": [["keep", 520], [W("로프웨이·리프트 왕복", "Ropeway or lift, round trip", "ロープウェイ・リフト往復", "Teleférico o telesilla, i/v", "Téléphérique ou télésiège, A/R"), 520]], "h": [["9:00", "17:00", 0, 0, "keep"]], "hx": ["seas"], "c": [{"t": W("12월 셋째 수요일 (천수각)", "3rd Wednesday of December (keep)", "12月第3水曜（天守）", "Tercer miércoles de diciembre (torre)", "3e mercredi de décembre (donjon)")}]},
 "k_ishiteji": {"f": "F", "h": [["24h", 0, 0, 0, "grounds"]], "c": ["none"]},
 "k_ritsurin": {"f": [["adult", 500]], "h": [["sun"]], "hx": ["month"], "c": ["none"]},
 "k_tamamo": {"f": [["adult", 300]], "h": [["sun"]], "hx": ["seas"], "c": [NY([12, 29], [12, 31])]},
 "k_yashima": {"f": "F", "h": [["24h"]], "c": ["none"]},
 "k_chichu": {"f": [["adult", 2100]], "fx": [RES], "h": [["10:00", "18:00", "17:00", [3, 9]], ["10:00", "17:00", "16:00", [10, 2]]], "c": ["mon+"]},
 "k_benesse": {"f": [["adult", 1300]], "h": [["8:00", "21:00"]], "c": ["none"]},
 "k_iepro": {"f": [[W("공통권 (6곳)", "Combined ticket (6 houses)", "共通チケット（6軒）", "Entrada combinada (6 casas)", "Billet combiné (6 maisons)"), 1050], [W("1곳", "Single house", "1軒", "Una casa", "Une maison"), 420]], "h": [["10:00", "16:30"]], "c": ["mon+"]},
 "k_iloveyu": {"f": [["adult", 660]], "h": [["13:00", "21:00"]], "c": ["mon+"]},
 "k_konpira": {"f": "F", "h": [["6:00", "17:00", 0, 0, W("본궁", "Main shrine", "御本宮", "Santuario principal", "Sanctuaire principal")]], "hx": ["seas"], "c": ["none"]},
 "k_kanamaruza": {"f": [["adult", 500]], "h": [["9:00", "17:00"]], "c": [{"t": W("공연·준비 기간", "Performance and preparation periods", "公演・準備期間", "Durante funciones y preparativos", "Pendant les représentations et préparatifs")}]},
}
