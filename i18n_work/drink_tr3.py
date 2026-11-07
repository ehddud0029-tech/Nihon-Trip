# 술 페이지 '사 가면 좋은 술' 가격대·맛 번역 → tr_46.tsv, zh_47.tsv, th_47.tsv (순서: pt_miss.json)
import json, re, sys
KO = json.load(open(sys.argv[1], encoding='utf-8'))
NOTE = {
 "상위 등급은 더 비싸요": ("higher grades cost more", "上位グレードはさらに高価", "las gamas altas cuestan más", "les gammes supérieures coûtent plus", "高等级更贵", "เกรดสูงกว่าราคาแพงกว่า"),
 "정가, 실제로는 더 비싼 경우가 많아요": ("list price; often sold for more", "希望小売価格、実際はもっと高いことが多い", "precio oficial; a menudo se vende más caro", "prix conseillé ; souvent vendu plus cher", "建议零售价，实际常常更贵", "ราคาตั้ง แต่มักขายแพงกว่า"),
 "정가": ("list price", "希望小売価格", "precio oficial", "prix conseillé", "建议零售价", "ราคาตั้ง"),
 "오래 숙성할수록 비싸요": ("older is pricier", "長期熟成ほど高価", "cuanto más añejo, más caro", "plus il est vieux, plus il est cher", "陈酿越久越贵", "ยิ่งบ่มนานยิ่งแพง"),
}
UNIT = {"캔": ("can", "缶", "lata", "canette", "罐", "กระป๋อง"), "병": ("bottle", "瓶", "botella", "bouteille", "瓶", "ขวด")}
def num(x, L):
    if L == 2: return x.replace(',', '.')
    if L == 3: return x.replace(',', ' ')
    return x
def one(part, L):  # "350ml 캔 약 250엔" / "캔 약 200~300엔"
    m = re.match(r'^(?:(\d+)ml )?(?:(캔|병) )?약 ([\d,]+)(?:~([\d,]+))?엔$', part.strip()); assert m, part
    vol, u, a, b = m.groups()
    rng = num(a, L) + ('–' + num(b, L) if b else '')
    if L == 1: rng = a + ('〜' + b if b else '')
    if L == 4: rng = a + ('~' + b if b else '')
    uu = UNIT[u][L] if u else ''
    if L == 0: return ' '.join(x for x in [f'{vol} ml' if vol else '', uu, f'approx. ¥{rng}'] if x)
    if L == 1: return (f'{vol}ml' if vol else '') + uu + f' 約{rng}円'
    if L == 2: return ', '.join(x for x in [' '.join(y for y in [uu, 'de' if vol and uu else '', f'{vol} ml' if vol else ''] if y), f'aprox. {rng} ¥'] if x)
    if L == 3: return ', '.join(x for x in [' '.join(y for y in [uu, 'de' if vol and uu else '', f'{vol} ml' if vol else ''] if y), f'env. {rng} ¥'] if x)
    if L == 4: return (f'{vol}ml' if vol else '') + uu + f' 约{rng}日元'
    if L == 5: return ' '.join(x for x in [uu, f'{vol} มล.' if vol else '', f'ประมาณ {rng} เยน'] if x)
def price(k, L):
    note = ''
    m = re.match(r'^(.*?) \((.+)\)$', k)
    if m: k, note = m.group(1), NOTE[m.group(2)][L]
    sep = {0: ', ', 1: '、', 2: '; ', 3: ' ; ', 4: '，', 5: ', '}[L]
    s = sep.join(one(p, L) for p in k.split(', '))
    if note: s += {1: f'（{note}）', 4: f'（{note}）'}.get(L, f' ({note})')
    return s
TASTE = {
"맛: 물처럼 맑고 깔끔하며 끝맛이 가벼워요.":("Taste: clear and clean like water, with a light finish.","味：水のように澄んですっきり、後味が軽やかです。","Sabor: limpio y claro como el agua, con un final ligero.","Goût : clair et net comme de l'eau, avec une finale légère.","口味：清澈如水，干净利落，余味轻盈。","รสชาติ: ใสสะอาดเหมือนน้ำ จบเบา ๆ"),
"맛: 바닐라와 꿀 같은 달콤한 향에 부드러운 목 넘김이에요.":("Taste: sweet vanilla and honey aromas with a smooth finish.","味：バニラや蜂蜜のような甘い香りで、喉ごしがまろやかです。","Sabor: aromas dulces de vainilla y miel, con un paso suave.","Goût : arômes sucrés de vanille et de miel, et une texture douce.","口味：香草和蜂蜜般的甜香，入喉顺滑。","รสชาติ: กลิ่นหวานแบบวานิลลาและน้ำผึ้ง ดื่มลื่นคอ"),
"맛: 멜론·사과 같은 과일 향이 화사하고 단맛이 은은해요.":("Taste: bright melon and apple aromas with gentle sweetness.","味：メロンやりんごのような華やかな果実香で、甘みはほのかです。","Sabor: aromas vivos de melón y manzana, con un dulzor suave.","Goût : arômes vifs de melon et de pomme, avec une douceur légère.","口味：哈密瓜、苹果般的果香华丽，甜味柔和。","รสชาติ: กลิ่นผลไม้อย่างเมลอนและแอปเปิลชัดเจน หวานอ่อน ๆ"),
"맛: 나다는 쌉쌀하고 힘 있는 맛, 후시미는 부드럽고 순한 맛이에요.":("Taste: Nada sake is dry and robust; Fushimi sake is soft and mellow.","味：灘は辛口で力強く、伏見はやわらかくまろやかです。","Sabor: el de Nada es seco y con cuerpo; el de Fushimi, suave y redondo.","Goût : le saké de Nada est sec et puissant, celui de Fushimi doux et rond.","口味：滩的酒辛口有力，伏见的酒柔和顺口。","รสชาติ: สาเกนาดะแห้งและเข้ม สาเกฟุชิมินุ่มละมุน"),
"맛: 매실 향이 진하고 새콤달콤해요. 얼음에 타 마시기 좋아요.":("Taste: rich plum aroma, sweet and tart. Great on the rocks.","味：梅の香りが豊かで甘酸っぱく、ロックで飲むのがおすすめです。","Sabor: intenso aroma a ciruela, agridulce. Muy bueno con hielo.","Goût : arôme de prune intense, sucré et acidulé. Parfait sur glace.","口味：梅香浓郁，酸甜可口，适合加冰喝。","รสชาติ: กลิ่นบ๊วยเข้ม เปรี้ยวอมหวาน ดื่มกับน้ำแข็งอร่อย"),
"맛: 딸기·체리 같은 과일 향과 일본 오크(미즈나라)의 은은한 향이에요.":("Taste: strawberry and cherry fruit with subtle Japanese oak (mizunara).","味：いちごやチェリーのような果実香と、ミズナラ樽のほのかな香りです。","Sabor: fruta como fresa y cereza, con un toque de roble japonés (mizunara).","Goût : fruits comme la fraise et la cerise, avec une touche de chêne japonais (mizunara).","口味：草莓、樱桃般的果香，带有日本水楢桶的淡淡香气。","รสชาติ: กลิ่นผลไม้อย่างสตรอว์เบอร์รีและเชอร์รี และกลิ่นโอ๊กญี่ปุ่น (มิซุนาระ) อ่อน ๆ"),
"맛: 고구마 향이 은은하고 단맛이 돌며 뒷맛이 깔끔해요.":("Taste: gentle sweet-potato aroma, a touch of sweetness and a clean finish.","味：芋の香りがほのかで甘みがあり、後味はすっきりしています。","Sabor: suave aroma a boniato, algo dulce y con final limpio.","Goût : léger arôme de patate douce, une pointe de douceur et une finale nette.","口味：淡淡的红薯香，略带甜味，余味干净。","รสชาติ: กลิ่นมันเทศอ่อน ๆ หวานนิด ๆ จบสะอาด"),
"맛: 보리의 고소한 향이 가볍고 순해서 부담이 없어요.":("Taste: light, nutty barley aroma; mild and easy.","味：麦の香ばしい香りが軽く、やさしい飲み口です。","Sabor: aroma ligero y tostado de cebada; suave y fácil.","Goût : léger arôme grillé d'orge ; doux et facile.","口味：大麦香气轻盈，温和不刺激。","รสชาติ: กลิ่นข้าวบาร์เลย์หอมเบา ๆ นุ่ม ดื่มง่าย"),
"맛: 쌀의 감칠맛이 살아 있는 부드럽고 균형 잡힌 맛이에요.":("Taste: soft and balanced, with lively rice umami.","味：米の旨みが生きた、やわらかくバランスのよい味です。","Sabor: suave y equilibrado, con el umami del arroz.","Goût : doux et équilibré, avec l'umami du riz.","口味：米的鲜味鲜明，柔和而均衡。","รสชาติ: นุ่มและกลมกล่อม มีอูมามิของข้าวชัดเจน"),
"맛: 보리 맛이 진하면서도 깔끔하고 시원해요.":("Taste: full malt flavour yet clean and crisp.","味：麦の味がしっかりしながら、すっきり爽快です。","Sabor: con mucho sabor a malta, pero limpia y refrescante.","Goût : riche en malt mais nette et rafraîchissante.","口味：麦香浓郁又清爽畅快。","รสชาติ: รสมอลต์เข้มแต่สะอาดและสดชื่น"),
"맛: 석탄 직화 증류에서 오는 스모키한 향과 묵직한 맛이에요.":("Taste: smoky and full-bodied, from coal-fired direct distillation.","味：石炭直火蒸溜によるスモーキーな香りと重厚な味わいです。","Sabor: ahumado y con cuerpo, por la destilación a fuego directo de carbón.","Goût : fumé et corsé, grâce à la distillation à feu direct au charbon.","口味：煤炭直火蒸馏带来的烟熏香气和厚重口感。","รสชาติ: กลิ่นควันและรสเข้มข้นจากการกลั่นด้วยไฟถ่านหินโดยตรง"),
"맛: 쌉쌀하고 깔끔한 가라쿠치(드라이)가 많아요.":("Taste: mostly dry, crisp karakuchi styles.","味：すっきりした辛口が多いです。","Sabor: sobre todo secos y nítidos (karakuchi).","Goût : surtout des sakés secs et nets (karakuchi).","口味：多为清爽的辛口。","รสชาติ: ส่วนใหญ่เป็นแบบแห้ง (คาราคุจิ) สะอาด"),
"맛: 산뜻한 산미의 가벼운 화이트 와인이 많아요.":("Taste: mostly light white wines with fresh acidity.","味：さわやかな酸味の軽い白ワインが多いです。","Sabor: sobre todo blancos ligeros de acidez fresca.","Goût : surtout des blancs légers à l'acidité fraîche.","口味：多为酸度清爽的轻盈白葡萄酒。","รสชาติ: ส่วนใหญ่เป็นไวน์ขาวเบา ๆ เปรี้ยวสดชื่น"),
"맛: 바닐라 같은 단 향이 나고 숙성될수록 부드러워요.":("Taste: sweet, vanilla-like aroma that grows smoother with age.","味：バニラのような甘い香りがあり、熟成するほどまろやかになります。","Sabor: aroma dulce como a vainilla, más suave cuanto más añejo.","Goût : arôme sucré rappelant la vanille, plus doux avec l'âge.","口味：有香草般的甜香，越陈越柔和。","รสชาติ: กลิ่นหวานคล้ายวานิลลา ยิ่งบ่มยิ่งนุ่ม"),
"맛: 과일 같은 향이 나고 아와모리치고 순해요.":("Taste: fruity aroma and mild for an awamori.","味：果実のような香りがあり、泡盛の中ではやわらかい味です。","Sabor: aroma afrutado y suave para ser un awamori.","Goût : arôme fruité, doux pour un awamori.","口味：带果香，在泡盛中算是温和的。","รสชาติ: กลิ่นผลไม้ และนุ่มกว่าอาวาโมริทั่วไป"),
"맛: 가볍고 상쾌해서 더운 날 벌컥 마시기 좋아요.":("Taste: light and refreshing, easy to gulp on a hot day.","味：軽くて爽やかで、暑い日にごくごく飲めます。","Sabor: ligera y refrescante, ideal para un día caluroso.","Goût : légère et rafraîchissante, idéale par temps chaud.","口味：清爽轻盈，热天大口喝很过瘾。","รสชาติ: เบาและสดชื่น ดื่มอึก ๆ ในวันร้อนได้สบาย"),
"맛: 쌀 맛이 풍부하고 단단한 맛이 많아요.":("Taste: mostly rich in rice flavour, with a firm structure.","味：米の味が豊かで、しっかりした味わいが多いです。","Sabor: sobre todo con mucho sabor a arroz y buena estructura.","Goût : surtout riches en riz, avec une belle structure.","口味：多为米味丰富、口感扎实的酒。","รสชาติ: ส่วนใหญ่รสข้าวเข้มข้นและหนักแน่น"),
"맛: 순하고 부드러워 식사와 함께 마시기 편해요.":("Taste: mild and smooth, easy to drink with meals.","味：やさしくまろやかで、食事と合わせやすいです。","Sabor: suave y redondo, fácil de beber con la comida.","Goût : doux et rond, facile à boire au repas.","口味：温和柔顺，适合配餐。","รสชาติ: นุ่มนวล ดื่มคู่กับอาหารได้ง่าย"),
"맛: 종류가 여러 가지이고, 진하고 향이 풍부한 수제 맥주예요.":("Taste: several styles of rich, aromatic craft beer.","味：種類がいくつかあり、濃厚で香り豊かなクラフトビールです。","Sabor: varios estilos de cerveza artesana intensa y aromática.","Goût : plusieurs styles de bière artisanale riche et aromatique.","口味：有多种口味，是浓郁芳香的精酿啤酒。","รสชาติ: มีหลายแบบ เป็นคราฟต์เบียร์รสเข้มกลิ่นหอม"),
"맛: 연수로 빚어 부드럽고 은은한 단맛이 있어요.":("Taste: brewed with soft water, smooth with a gentle sweetness.","味：軟水で仕込むため、やわらかくほのかな甘みがあります。","Sabor: elaborado con agua blanda, suave y ligeramente dulce.","Goût : brassé à l'eau douce, rond avec une légère douceur.","口味：用软水酿造，柔和带淡淡甜味。","รสชาติ: หมักด้วยน้ำอ่อน นุ่มและหวานอ่อน ๆ"),
"맛: 레몬 껍질 향이 상큼하고 새콤해요.":("Taste: zesty lemon-peel aroma, fresh and tart.","味：レモンの皮の香りが爽やかで、酸味があります。","Sabor: aroma fresco a piel de limón, ácido y vivo.","Goût : arôme frais de zeste de citron, acidulé.","口味：柠檬皮香气清新，酸爽。","รสชาติ: กลิ่นเปลือกเลมอนสดชื่น เปรี้ยว"),
"맛: 단맛이 적고 쌉쌀해서 생선 요리와 잘 어울려요.":("Taste: low in sweetness and dry, great with seafood.","味：甘みが少なく辛口で、魚料理によく合います。","Sabor: poco dulce y seco, ideal con pescado.","Goût : peu sucré et sec, parfait avec le poisson.","口味：甜度低、偏辛口，和鱼类料理很搭。","รสชาติ: หวานน้อยและแห้ง เข้ากับอาหารทะเล"),
"맛: 종류마다 달라요. 쾰시·에일 등 향이 좋은 수제 맥주예요.":("Taste: varies by style; aromatic craft beers such as Kölsch and ale.","味：種類ごとに違います。ケルシュやエールなど香りのよいクラフトビールです。","Sabor: depende del estilo; cervezas artesanas aromáticas como Kölsch y ale.","Goût : selon le style ; bières artisanales aromatiques comme la Kölsch et l'ale.","口味：因款式而异，有科隆啤酒、艾尔等香气好的精酿啤酒。","รสชาติ: ต่างกันตามชนิด เป็นคราฟต์เบียร์กลิ่นหอม เช่น เคิลช์และเอล"),
"맛: 쌀의 단맛이 은은하고 부드러워요.":("Taste: soft, with a gentle rice sweetness.","味：米のほのかな甘みがあり、やわらかいです。","Sabor: suave, con un ligero dulzor de arroz.","Goût : doux, avec une légère douceur de riz.","口味：带有淡淡的米甜味，口感柔和。","รสชาติ: นุ่ม มีความหวานของข้าวอ่อน ๆ"),
"맛: 유자 향이 상큼하고 달콤해서 디저트처럼 마셔요.":("Taste: fresh, sweet yuzu, enjoyed almost like a dessert.","味：ゆずの香りが爽やかで甘く、デザート感覚で飲めます。","Sabor: yuzu fresco y dulce, casi como un postre.","Goût : yuzu frais et sucré, presque comme un dessert.","口味：柚子香清新甜美，像甜点一样喝。","รสชาติ: กลิ่นยูซุสดชื่นและหวาน ดื่มเหมือนของหวาน"),
"가격대":("Price range","価格帯","Precio aprox.","Prix indicatif","价格区间","ช่วงราคา"),
"가격대는 2026년 11월 일본 매장 기준 대략적인 값이에요. 매장과 시기에 따라 달라요.":("Price ranges are rough Japanese retail prices as of November 2026 and vary by shop and season.","価格帯は2026年11月の日本の店頭価格の目安で、店や時期によって変わります。","Los precios son orientativos según tiendas de Japón en noviembre de 2026 y varían según la tienda y la época.","Les prix sont indicatifs (magasins au Japon, novembre 2026) et varient selon le magasin et la période.","价格区间为2026年11月日本门店的大致价格，因店铺和时期而异。","ช่วงราคาเป็นราคาโดยประมาณในร้านญี่ปุ่น ณ พฤศจิกายน 2026 และแตกต่างตามร้านและช่วงเวลา"),
}
rows = []
for k in KO:
    rows.append((k, TASTE[k]) if k in TASTE else (k, tuple(price(k, L) for L in range(6))))
W = '/home/claude/i18n_work/'
with open(W + 'tr_46.tsv', 'w', encoding='utf-8') as f:
    for k, t in rows: f.write('\t'.join([k, *t[:4]]) + '\n')
with open(W + 'zh_47.tsv', 'w', encoding='utf-8') as f:
    for k, t in rows: f.write(k + '\t' + t[4] + '\n')
with open(W + 'th_47.tsv', 'w', encoding='utf-8') as f:
    for k, t in rows: f.write(k + '\t' + t[5] + '\n')
print('wrote', len(rows))
