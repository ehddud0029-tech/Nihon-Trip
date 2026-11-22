# 검색에 내놓을 페이지 규칙 (2026-11-19, 사용자 결정: 저품질 판정 대응 1·2번 정리)
# - 간체 중국어(zh) 전체 검색 제외
# - 같은 틀이 반복되거나 다른 페이지와 겹치는 하위 페이지는 noindex + 사이트맵·hreflang에서 뺌 (페이지는 그대로 볼 수 있음)
# - 예외: 하락 전(2026-11-01~09) 서치콘솔 노출이 있던 주소는 남김 (site/index_keep.json, 노출 있던 모든 주소)
# - 2단계(2026-11-22): 장소 상세는 추천 일정 장소·영업시간 있는 쇼핑 시설(site/place_keep.json)이나 노출 있던 주소만,
#   지역 관광지·맛집·교통 목록은 노출 있던 주소만 남김
import json, os
_KEEP = None
def _keep():
    global _KEEP
    if _KEEP is None:
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'index_keep.json')
        _KEEP = set(tuple(x) for x in json.load(open(f, encoding='utf-8'))) if os.path.exists(f) else set()
    return _KEEP
_PK = None
def _pkeep():
    global _PK
    if _PK is None:
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'place_keep.json')
        _PK = set(json.load(open(f, encoding='utf-8'))) if os.path.exists(f) else set()
    return _PK
NOINDEX_LANGS = {'zh'}
JP_TOPIC_DROP = {'transport', 'shopping', 'map', 'spots', 'food'}   # 일본 전체 주제 화면(축제 월별은 남김)

def rule_ok(path):
    p = [x for x in path.strip('/').split('/') if x]
    if not p: return True
    a = p[0]
    if a in JP_TOPIC_DROP: return False
    if a in ('stay', 'drink'): return len(p) == 1
    if a == 'airport': return len(p) <= 2
    if a == 'place': return len(p) > 1 and p[1] in _pkeep()   # 2단계
    if a in ('itinerary', 'weather', 'guide', 'festivals', 'about', 'contact', 'privacy', 'saved'): return True
    if len(p) == 1: return True
    if p[1] in ('weather', 'stay', 'drink', 'festivals'):
        if len(p) == 2: return True
        if p[1] == 'weather': return p[2].isdigit()
        if p[1] == 'drink': return p[2] in ('buy', 'shops')
        return False   # 숙소 탭·동네
    if len(p) == 2: return True
    if len(p) == 3: return False   # 지역 목록: 노출 있던 주소만 (index_keep.json, 2단계)
    return False   # 지역 교통 탭 등

def idx_ok(lang, path):
    if lang in NOINDEX_LANGS: return False
    if (lang, path) in _keep(): return True
    return rule_ok(path)
