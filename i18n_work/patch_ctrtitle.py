# 검색 클릭률용 제목 다듬기 (2026-11)
# - 한국어 월 축제 제목 '1월월' 오류 고침
# - 맛집 페이지 제목: 'TOP 5'와 메뉴 이름 (8개 언어)
# - 관광지 제목에 입장료 금액(어른 한 가지 요금일 때) 또는 '입장 무료'
# - 큰 쇼핑 시설(층별 안내·면세 있는 곳) 제목: 영업시간·층별 안내·면세
# html과 backup pre에 같이 적용, 여러 번 돌려도 안전
import re

def block(s, begin, end, new, anchor):
    if begin in s:
        i = s.index(begin); j = s.index(end, i) + len(end)
        return s[:i] + new.strip() + s[j:]
    assert s.count(anchor) == 1, anchor[:50]
    return s.replace(anchor, new.strip() + '\n' + anchor)

FILES = ['/home/claude/tabishiori.html', '/home/claude/i18n_work/backup/tabishiori.pre.html']

CTR = r'''/*CTRT_BEGIN*/
/* 검색 제목: 관광지는 입장료 금액·무료, 큰 쇼핑 시설은 층별 안내·면세 */
const CTR_T = {
 ko:{paid:"{n} 입장료 {f} – 운영 시간·가는 길 ({a})",free:"{n} – 입장 무료·운영 시간·가는 길 ({a})",mall:"{n} – 영업시간·층별 안내·면세 ({a})"},
 en:{paid:"{n} – Admission {f}, Hours & Access ({a})",free:"{n} – Free Entry, Hours & Access ({a})",mall:"{n} – Hours, Floor Guide & Tax-Free ({a})"},
 ja:{paid:"{n} – 入場料{f}・営業時間・アクセス（{a}）",free:"{n}（入場無料）– 営業時間・アクセス（{a}）",mall:"{n} – 営業時間・フロアガイド・免税（{a}）"},
 es:{paid:"{n} – Entrada {f}, horario y cómo llegar ({a})",free:"{n} – Entrada gratis, horario y cómo llegar ({a})",mall:"{n} – Horario, plantas y tax-free ({a})"},
 fr:{paid:"{n} – Entrée {f}, horaires et accès ({a})",free:"{n} – Entrée gratuite, horaires et accès ({a})",mall:"{n} – Horaires, étages et détaxe ({a})"},
 zh:{paid:"{n} – 门票{f}·营业时间·交通（{a}）",free:"{n}（免费入场）– 营业时间·交通（{a}）",mall:"{n} – 营业时间·楼层指南·免税（{a}）"},
 tw:{paid:"{n} – 門票{f}·營業時間·交通（{a}）",free:"{n}（免費入場）– 營業時間·交通（{a}）",mall:"{n} – 營業時間·樓層指南·免稅（{a}）"},
 th:{paid:"{n} – ค่าเข้าชม {f} เวลาเปิด และการเดินทาง ({a})",free:"{n} – เข้าชมฟรี เวลาเปิด และการเดินทาง ({a})",mall:"{n} – เวลาเปิด ชั้นต่าง ๆ และปลอดภาษี ({a})"}
};
function ctrTitle(it, L, shi){
  const M = CTR_T[L] || CTR_T.ko;
  if(it.type==="shop") return (shi && shi.h && shi.f && shi.tf) ? M.mall : "";
  if(it.type!=="spot") return "";
  const si = (typeof SPOT_INFO!=="undefined" && SPOT_INFO[it.id]) || null; if(!si || si.closed) return "";
  if(si.f==="F" && !(si.fx||[]).length) return M.free;
  const f = si.f;
  if(Array.isArray(f) && f.length===1 && f[0][0]==="adult" && f[0][1]!=null && !f[0][2]){
    const r = SIV.rows(it.id), fee = r && r.rows.find(x=>x[0]==="fee"), st0 = r && r.rows.find(x=>x[0]==="status");
    if(st0 || !fee || !fee[1][0]) return "";
    return M.paid.replace("{f}", fee[1][0]);
  }
  return "";
}
/*CTRT_END*/'''

RULES = [
  # 1월월 오류
  ('all_festivals:"일본 {m}월 축제·행사 – 지역별 축제 달력"', 'all_festivals:"일본 {m} 축제·행사 – 지역별 축제 달력"'),
  ('all_festivals:"일본 {m}월에 열리는 축제와 계절 행사{L}. 날짜와 장소, 즐기는 법."', 'all_festivals:"일본 {m}에 열리는 축제와 계절 행사{L}. 날짜와 장소, 즐기는 법."'),
  # 맛집 제목
  ('food:"{a} 맛집 추천 · {c} 여행"', 'food:"{a} 맛집 추천 TOP 5 – 라멘·스시·야키니쿠 메뉴별"'),
  ('food:"Where to Eat in {a}, {c} – Top Restaurants"', 'food:"Best Restaurants in {a}, {c} – Top 5 Ramen, Sushi & More"'),
  ('food:"{a}のグルメ・おすすめ店"', 'food:"{a}のグルメ おすすめ店TOP5 – ラーメン・寿司・焼肉"'),
  ('food:"Dónde comer en {a} ({c}) – Mejores restaurantes"', 'food:"Mejores restaurantes en {a} ({c}) – Top 5 de ramen, sushi y más"'),
  ('food:"Où manger à {a} ({c}) – Meilleurs restaurants"', 'food:"Meilleurs restaurants à {a} ({c}) – Top 5 ramen, sushi et plus"'),
  ('"food":"{a}美食推荐 · {c}旅游"', '"food":"{a}美食推荐TOP5 – 拉面·寿司·烤肉"'),
  ('"food":"{a}美食推薦 · {c}旅遊"', '"food":"{a}美食推薦TOP5 – 拉麵·壽司·燒肉"'),
  ('"food":"ร้านอาหารแนะนำใน{a} · เที่ยว{c}"', '"food":"ร้านอาหารแนะนำใน{a} TOP 5 – ราเมง ซูชิ ยากินิกุ"'),
  # 영어 제목 줄이기
  ('shop:"{n} – What to Buy & How to Get There ({a})"', 'shop:"{n} – What to Buy & Access ({a})"'),
  ('en:"{n} – Opening Hours, What to Buy & Access ({a})"', 'en:"{n} – Hours, What to Buy & Access ({a})"'),
  # 제목 고르기
  ('return {title:((it.type==="shop"&&shi&&shi.h&&PTH[L])||(PT[L]||PT.ko)[it.type]).replace("{n}",n)',
   'return {title:(ctrTitle(it,L,shi)||(it.type==="shop"&&shi&&shi.h&&PTH[L])||(PT[L]||PT.ko)[it.type]).replace("{n}",n)'),
]

for fn in FILES:
    s = open(fn, encoding='utf-8').read()
    for old, new in RULES:
        if new in s: continue
        if old not in s: print('!! not found', fn, old[:60]); continue
        s = s.replace(old, new)
    s = block(s, '/*CTRT_BEGIN*/', '/*CTRT_END*/', CTR, 'function pageMeta(){')
    open(fn, 'w', encoding='utf-8').write(s)
    print('ok', fn)
