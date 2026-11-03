# 도쿄 영상 참고 보완 (2026-11): 도청 전망실 운영 시간·휴무·프로젝션 매핑, 센소지 팁(아사쿠사 문화관광센터 전망 테라스), 휴무 요일에 화요일 추가
# html·backup pre·sitegen 원본에 같이 적용
W = '/home/claude'
TOCHO_TIP_OLD = '"맑은 겨울 아침엔 서쪽으로 후지산이 보여요."]'
TOCHO_TIP_NEW = '"밤 7시부터 9시 30분까지 30분마다 청사 외벽에서 무료 프로젝션 매핑 쇼가 열려요. 맑은 겨울 아침엔 서쪽으로 후지산이 보여요."]'
SENSO_OLD = '"아사쿠사역","이른 아침이나 저녁 라이트업 시간대가 한산해요."]'
SENSO_NEW = '"아사쿠사역","이른 아침이나 저녁 라이트업 시간대가 한산해요. 가미나리몬 맞은편 아사쿠사 문화관광센터 8층 전망 테라스(무료)에서 나카미세와 센소지를 내려다볼 수 있어요."]'
SI_OLD = 's_tocho:{f:"F",h:[["9:30","21:30",0,0,"south"]],c:["irr"]}'
SI_NEW = ('s_tocho:{f:"F",h:[["9:30","22:00","21:30",0,"south"]],c:[{n:1,w:"tue"},{n:3,w:"tue"}],'
          'x:{ko:"남쪽 전망실 기준이에요. 북쪽 전망실은 둘째·넷째 월요일에 쉬어요.",en:"Hours shown are for the South Observatory; the North Observatory closes on the 2nd and 4th Mondays.",'
          'ja:"南展望室の情報です。北展望室は第2・第4月曜休室です。",es:"Datos del mirador sur; el mirador norte cierra el 2.º y 4.º lunes.",'
          'fr:"Informations de l\'observatoire sud ; l\'observatoire nord ferme les 2e et 4e lundis."}}')
WD_OLD = 'WD1 = {mon:W("월요일","Monday","月曜","lunes","lundi"),'
WD_NEW = 'WD1 = {mon:W("월요일","Monday","月曜","lunes","lundi"),tue:W("화요일","Tuesday","火曜","martes","mardi"),'
JOBS = {
 f'{W}/tabishiori.html': [(TOCHO_TIP_OLD, TOCHO_TIP_NEW), (SENSO_OLD, SENSO_NEW), (SI_OLD, SI_NEW), (WD_OLD, WD_NEW)],
 f'{W}/i18n_work/backup/tabishiori.pre.html': [(TOCHO_TIP_OLD, TOCHO_TIP_NEW), (SENSO_OLD, SENSO_NEW), (SI_OLD, SI_NEW), (WD_OLD, WD_NEW)],
 f'{W}/sitegen/spot_info.js': [(SI_OLD, SI_NEW)],
 f'{W}/sitegen/spot_info_view.js': [(WD_OLD, WD_NEW)],
 f'{W}/i18n_work/backup/spot_info_view.pre.js': [(WD_OLD, WD_NEW)],
}
for f, R in JOBS.items():
    s = open(f, encoding='utf-8').read()
    for a, b in R:
        if b in s: continue
        n = s.count(a); 
        if n == 0: print('  skip (not found)', f.split('/')[-1], a[:40]); continue
        s = s.replace(a, b)
    open(f, 'w', encoding='utf-8').write(s); print('patched', f)
