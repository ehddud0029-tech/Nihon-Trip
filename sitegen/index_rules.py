# 검색에 내놓을 페이지 규칙 (2026-11-19, 사용자 결정: 저품질 판정 대응 1·2번 정리)
# - 간체 중국어(zh) 전체 검색 제외
# - 같은 틀이 반복되거나 다른 페이지와 겹치는 하위 페이지는 noindex + 사이트맵·hreflang에서 뺌 (페이지는 그대로 볼 수 있음)
# - 예외: 하락 전(2026-11-01~09) 서치콘솔 노출이 있던 주소는 남김 (site/index_keep.json)
import json, os
_KEEP = None
def _keep():
    global _KEEP
    if _KEEP is None:
        f = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'site', 'index_keep.json')
        _KEEP = set(tuple(x) for x in json.load(open(f, encoding='utf-8'))) if os.path.exists(f) else set()
    return _KEEP
NOINDEX_LANGS = {'zh'}
JP_TOPIC_DROP = {'transport', 'shopping', 'map', 'spots', 'food'}   # 일본 전체 주제 화면(축제 월별은 남김)

def rule_ok(path):
    p = [x for x in path.strip('/').split('/') if x]
    if not p: return True
    a = p[0]
    if a in JP_TOPIC_DROP: return False
    if a in ('stay', 'drink'): return len(p) == 1
    if a == 'airport': return len(p) <= 2
    if a in ('place', 'itinerary', 'weather', 'guide', 'festivals', 'about', 'contact', 'privacy', 'saved'): return True
    if len(p) == 1: return True
    if p[1] in ('weather', 'stay', 'drink', 'festivals'):
        if len(p) == 2: return True
        if p[1] == 'weather': return p[2].isdigit()
        if p[1] == 'drink': return p[2] in ('buy', 'shops')
        return False   # 숙소 탭·동네
    if len(p) == 2: return True
    if len(p) == 3: return p[2] in ('spots', 'food', 'transport')
    return False   # 지역 교통 탭 등

def idx_ok(lang, path):
    if lang in NOINDEX_LANGS: return False
    if (lang, path) in _keep(): return True
    return rule_ok(path)
