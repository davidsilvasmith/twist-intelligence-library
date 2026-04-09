from pathlib import Path
import json, re, html as htmlmod

root = Path('/Users/smithd98/.openclaw/workspace')
wiki = root / 'wiki'
data = json.loads((wiki / 'dashboard_data.json').read_text())

hero_vids = {'E2273':'1ORdeSPOy2k','E2272':'1ORdeSPOy2k','E2271':'g5LxEPGLDsc'}
founder_images = {
  "Andrew D'Souza": "",
  "Victor Riparbelli": "",
  "Ryan Carson": "",
  "Rob May": ""
}
for h in data['hero_episodes']:
    vid = hero_vids.get(h['episode'])
    if vid:
        h['thumbnail'] = f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg'
    if h['episode'] == 'E2271':
        h['delta_now'] = '$17M raised'
        h['delta_percent'] = '+1,420%'
        h['topics'] = ['YC','AI','Tabular Data Rigor','Fundraising']
    if h['episode'] == 'E2272':
        h['delta_now'] = '$2,000/month cost test'
        h['delta_percent'] = '+pricing reset'
    if h['episode'] == 'E2273':
        h['delta_now'] = 'Project Glasswing / inference moat'
        h['delta_percent'] = '+strategic threat'
for t in data['trajectory_delta']:
    t['image'] = founder_images.get(t['founder'],'')
    if t['company'] == 'Boardy':
        t['now_label'] = '$17M raised, audited in E2271'
    if t['company'] == 'Synthesia':
        t['now_label'] = '$4B valuation, $200M Series E led by GV'
    if t['company'] == 'Neurometric':
        t['now_label'] = 'Project Glasswing context, inference-time compute moat'
for m in data['the_misses']:
    if m['company'] == 'Airbnb':
        m['miss_delta'] = '$78.62B market cap'
        m['reality_now'] = 'The software trust layer, ratings, identity, and repeat reputation loops turned stranger risk into a scalable lodging marketplace now worth $78.62B.'

(wiki / 'dashboard_data.json').write_text(json.dumps(data, indent=2))

(root/'episodes').mkdir(exist_ok=True)
(root/'founders').mkdir(exist_ok=True)

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def base_page(title, body, back='/index.html'):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{htmlmod.escape(title)}</title><script src="https://cdn.tailwindcss.com"></script><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet"><style>body{{font-family:Inter,sans-serif}} .headline{{font-family:'Noto Serif',serif}}</style></head><body class="bg-stone-50 text-stone-900"><main class="max-w-5xl mx-auto px-6 py-12"><div class="flex items-center justify-between mb-8"><a href="{back}" class="text-green-700 font-semibold">← Back to dashboard</a><nav class="flex gap-4 text-sm"><a href="/index.html">Home</a><a href="/founders/andrew-d-souza.html">Founders</a><a href="/episodes/e2273.html">Episodes</a><a href="https://x.com/TWiStartups" target="_blank">Twitter</a><a href="https://www.linkedin.com/company/this-week-in-startups/" target="_blank">LinkedIn</a></nav></div>{body}</main></body></html>'''

appearance_map = {
    "Andrew D'Souza": ["E2271"],
    "Rob May": ["E2273"],
    "Ryan Carson": ["E2272"],
    "Victor Riparbelli": []
}

for mc in (root/'wiki/masterclasses').glob('*.md'):
    text = mc.read_text()
    ep = re.search(r'episode:\s*(E\d+)', text).group(1)
    title = re.search(r'title:\s*"([^"]+)"', text).group(1)
    yt = re.search(r'youtube_url:\s*"([^"]*)"', text)
    ytu = yt.group(1) if yt else ''
    body_md = re.sub(r'^---.*?---\n','',text, flags=re.S)
    paragraphs = ''.join(f'<p class="mb-4 leading-7">{htmlmod.escape(p.strip())}</p>' for p in body_md.split('\n\n') if p.strip())
    guests = [t for t in data['trajectory_delta'] if t.get('episode') == ep]
    guest_links = ''.join(f'<a class="px-3 py-2 bg-white rounded-lg border border-stone-200 hover:border-green-500" href="/founders/{slug(g["founder"])}.html">{htmlmod.escape(g["founder"])} · {htmlmod.escape(g["company"])} </a>' for g in guests)
    thumb = next((h['thumbnail'] for h in data['hero_episodes'] if h['episode']==ep), '')
    entities = []
    for g in guests:
        entities.append(f'<a class="px-3 py-2 bg-white rounded-lg border border-stone-200 hover:border-green-500" href="/founders/{slug(g["founder"])}.html">{htmlmod.escape(g["founder"])} </a>')
        entities.append(f'<a class="px-3 py-2 bg-stone-50 rounded-lg border border-stone-200 hover:border-green-500" href="/founders/{slug(g["founder"])}.html">{htmlmod.escape(g["company"])} </a>')
    body = f'''<h1 class="headline text-5xl italic mb-4">{htmlmod.escape(ep)}: {htmlmod.escape(title)}</h1>{('<img class="w-full rounded-2xl mb-8 border border-stone-200" src="'+thumb+'">') if thumb else ''}<div class="flex gap-3 mb-8">{('<a class="inline-block px-4 py-2 bg-green-600 text-white rounded-lg font-semibold" href="'+ytu+'" target="_blank">Open Episode</a>') if ytu else ''}</div><section class="mb-10"><h2 class="headline text-2xl italic mb-4">Masterclass</h2>{paragraphs}</section><section class="mb-10"><h2 class="headline text-2xl italic mb-4">Featured Entities</h2><div class="flex flex-wrap gap-3">{''.join(entities) or '<p class="text-stone-500">No linked entities yet.</p>'}</div></section><section><h2 class="headline text-2xl italic mb-4">Guests</h2><div class="flex flex-wrap gap-3">{guest_links or '<p class="text-stone-500">No linked guest yet.</p>'}</div></section>'''
    (root/'episodes'/f'{ep.lower()}.html').write_text(base_page(f'Masterclass: {ep} - {title} | TWiST Wiki', body))

for founder in data['trajectory_delta']:
    name = founder['founder']
    photo = founder.get('image','')
    appearances = appearance_map.get(name, [])
    app_links = ''.join(f'<li><a class="text-green-700 underline" href="/episodes/{ep.lower()}.html">{ep}</a></li>' for ep in appearances) or '<li class="text-stone-500">No TWiST appearance linked yet.</li>'
    body = f'''<div class="grid md:grid-cols-[180px,1fr] gap-8 items-start mb-8">{('<img class="w-44 h-44 rounded-2xl object-cover border border-stone-200" src="'+photo+'" alt="'+htmlmod.escape(name)+'">') if photo else '<div class="w-44 h-44 rounded-2xl bg-stone-200 border border-stone-200"></div>'}<div><h1 class="headline text-5xl italic mb-2">{htmlmod.escape(name)}</h1><p class="text-lg text-stone-600 mb-6">{htmlmod.escape(founder.get('role',''))}, {htmlmod.escape(founder.get('company',''))}</p><div class="grid md:grid-cols-2 gap-4"><div class="bg-white rounded-2xl p-6 border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Then</div><div class="text-lg font-semibold">{htmlmod.escape(founder.get('then_label',''))}</div></div><div class="bg-white rounded-2xl p-6 border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Now</div><div class="text-lg font-semibold">{htmlmod.escape(founder.get('now_label',''))}</div></div></div></div></div><section class="bg-white rounded-2xl p-6 border border-stone-200 mb-8"><h2 class="headline text-2xl italic mb-4">Intervention Note</h2><p class="leading-7">{htmlmod.escape(founder.get('intervention_note',''))}</p><p class="mt-4 text-sm text-stone-500">Verification: {htmlmod.escape(founder.get('verification',''))}</p></section><section><h2 class="headline text-2xl italic mb-4">TWiST Appearance History</h2><ul class="list-disc pl-6 space-y-2">{app_links}</ul></section>'''
    (root/'founders'/f'{slug(name)}.html').write_text(base_page(f'Founder Trajectory: {name} | TWiST Wiki', body))

hero_cards = []
for h in data['hero_episodes']:
    hero_cards.append(f'''<a href="/episodes/{h['episode'].lower()}.html" class="group block"><div class="relative aspect-[16/9] rounded-2xl overflow-hidden mb-3 bg-stone-200"><img class="w-full h-full object-cover" src="{h['thumbnail']}" onerror="this.src='{h['thumbnail'].replace('maxresdefault','hqdefault')}'"></div><div class="flex items-center justify-between px-1 py-2 bg-white rounded-lg mb-4"><p class="text-[11px] font-bold text-stone-600 truncate mr-4">{htmlmod.escape(h['delta_label'])}: <span class="text-stone-400">{htmlmod.escape(h['delta_then'])}</span> <span class="text-green-500">→</span> {htmlmod.escape(h['delta_now'])} <span class="text-green-500 ml-1">({htmlmod.escape(h['delta_percent'])})</span></p><svg class="w-16 h-4 stroke-[#39ff14] fill-none stroke-2" viewBox="0 0 100 40"><path d="{h.get('sparkline_path','M0,35 L100,5')}"></path></svg></div><h3 class="headline text-xl font-bold leading-tight">{htmlmod.escape(h['headline'])}</h3></a>''')

traj_cards = []
for t in data['trajectory_delta']:
    img = f'<img class="w-20 h-20 rounded-full object-cover border border-stone-200" src="{t.get("image","")}" alt="{htmlmod.escape(t["founder"])}">' if t.get('image') else '<div class="w-20 h-20 rounded-full bg-stone-200 border border-stone-200"></div>'
    traj_cards.append(f'''<a href="/founders/{slug(t['founder'])}.html" class="bg-white rounded-xl p-6 shadow-sm flex flex-col justify-between border border-stone-200 hover:border-green-500 transition-colors"><div class="flex justify-between items-start mb-8">{img}<div class="text-right"><span class="text-[#39ff14] font-bold text-2xl headline">{htmlmod.escape(t['delta_percent'])}</span><p class="text-[10px] text-stone-500 uppercase font-bold tracking-widest">Velocity Delta</p></div></div><div class="mb-8"><h4 class="headline text-lg font-bold mb-1">{htmlmod.escape(t['founder'])}</h4><p class="text-xs text-stone-500 mb-4">{htmlmod.escape(t['role'])}, {htmlmod.escape(t['company'])}</p><div class="flex justify-between font-semibold text-sm gap-4"><span class="text-stone-400">{htmlmod.escape(t['then_label'])}</span><span>{htmlmod.escape(t['now_label'])}</span></div></div><span class="w-full py-3 text-[10px] font-bold uppercase tracking-widest text-[#106e00] border border-green-200 rounded-lg text-center">View Intervention</span></a>''')

miss_cards = []
for m in data['the_misses']:
    miss_cards.append(f'''<article class="bg-white rounded-2xl p-8 border border-stone-200"><div class="flex justify-between items-start mb-6"><div><h3 class="headline text-3xl mb-2">{htmlmod.escape(m['company'])}</h3><p class="text-sm text-stone-500">Vintage: {htmlmod.escape(m['vintage'])}</p></div><div class="text-right"><div class="text-4xl headline font-black text-orange-600">{htmlmod.escape(m['miss_delta'])}</div><div class="text-xs uppercase text-stone-500">Miss Delta</div></div></div><div class="grid md:grid-cols-2 gap-4 mb-4"><div class="bg-stone-50 p-4 rounded-xl"><div class="text-xs uppercase text-stone-500 mb-2">Then</div><p class="text-sm leading-6">{htmlmod.escape(m['logic_then'])}</p></div><div class="bg-orange-50 p-4 rounded-xl"><div class="text-xs uppercase text-stone-500 mb-2">Market Reality</div><p class="text-sm leading-6">{htmlmod.escape(m['reality_now'])}</p></div></div><div class="border-l-4 border-orange-500 pl-4"><div class="text-xs uppercase text-orange-700 mb-2">Lesson</div><p class="text-sm leading-6">{htmlmod.escape(m['lesson'])}</p></div></article>''')

svg_parts = []
by = {n['label']: n for n in data['constellation_nodes']}
drawn = set()
for n in data['constellation_nodes']:
    for target in n.get('connected_to',[]):
        if target not in by:
            continue
        key = '::'.join(sorted([n['label'], target]))
        if key in drawn:
            continue
        drawn.add(key)
        svg_parts.append(f'<line x1="{n["x"]}" y1="{n["y"]}" x2="{by[target]["x"]}" y2="{by[target]["y"]}" stroke="#d1d5db" stroke-width="1" stroke-dasharray="4" />')
for n in data['constellation_nodes']:
    href = '/founders/' + slug(n['label']) + '.html' if n['type'] == 'guest' else '/index.html'
    guest_suffix = f" ({n['company']})" if n['type'] == 'guest' else ''
    svg_parts.append(f'<a href="{href}"><circle cx="{n["x"]}" cy="{n["y"]}" r="{6 if n["type"]=="vc" else 5}" fill="{"#39ff14" if n.get("active") else "#1b1c19"}" /><text x="{n["x"]+10}" y="{n["y"]+4}" font-size="10" fill="#3c4b35">{htmlmod.escape(n["label"] + guest_suffix)}</text></a>')

index = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>TWiST Intelligence Library | This Week in Startups Knowledge Graph</title><script src="https://cdn.tailwindcss.com"></script><script src="https://cdn.jsdelivr.net/npm/d3@7"></script><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet"><style>body{{font-family:Inter,sans-serif}} .headline{{font-family:'Noto Serif',serif}}</style></head><body class="bg-[#f9f7f2] text-stone-900"><div class="min-h-screen"><nav class="sticky top-0 z-20 bg-[#f9f7f2]/95 backdrop-blur border-b border-stone-200"><div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"><div class="headline text-2xl italic font-bold">TWiST Intelligence</div><div class="flex gap-6 text-sm font-semibold"><a href="/index.html">Library</a><a href="/founders/andrew-d-souza.html">Founder Delta</a><a href="/episodes/e2273.html">Masterclass</a><a href="https://x.com/TWiStartups" target="_blank">Twitter</a><a href="https://www.linkedin.com/company/this-week-in-startups/" target="_blank">LinkedIn</a></div></div></nav><main class="max-w-7xl mx-auto px-6 py-10 space-y-20"><header class="bg-white rounded-3xl border border-stone-200 p-8"><div class="flex items-center justify-between mb-6"><h1 class="headline text-5xl italic">Jason's Take</h1><button id="compare-toggle" class="px-4 py-2 rounded-full bg-green-600 text-white font-semibold">Compare Stance ON</button></div><div id="stance-panel" class="grid md:grid-cols-2 gap-4"><div id="stance-left" class="bg-stone-50 p-6 rounded-2xl"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">AI Vibes frame</div><p class="headline italic text-xl">General LLM excitement, broad automation optimism, and loose narrative-driven bullishness.</p></div><div id="stance-right" class="bg-green-50 p-6 rounded-2xl"><div class="text-xs uppercase tracking-widest text-green-700 mb-2">Tabular Data Rigor frame</div><p class="headline italic text-xl">E2271 and E2272 sharpen the standard: operating metrics, pricing reality, and proof over vibes.</p></div></div></header><section><div class="flex justify-between items-end mb-10"><h2 class="headline italic text-4xl">High-Fidelity Intelligence</h2><a href="/episodes/e2273.html" class="text-green-700 font-semibold">Open featured masterclass</a></div><div class="grid md:grid-cols-3 gap-8">{''.join(hero_cards)}</div></section><section><div class="grid md:grid-cols-12 gap-12 items-center"><div class="md:col-span-4"><h2 class="headline italic text-4xl mb-6">Relationship Constellation</h2><p class="text-stone-600 text-lg leading-relaxed mb-8">Interactive connective tissue between guests, investors, and applied AI operators.</p></div><div class="md:col-span-8 aspect-video bg-white rounded-3xl border border-stone-200 shadow-inner overflow-hidden"><svg id="constellation" class="w-full h-full p-6" viewBox="0 0 800 450">{''.join(svg_parts)}</svg></div></div></section><section><div class="mb-16"><h2 class="headline italic text-4xl mb-4">Founder Delta</h2><p class="text-stone-600 max-w-xl">Living trajectory pages with then-vs-now proof points.</p></div><div class="grid md:grid-cols-4 gap-6">{''.join(traj_cards)}</div></section><section><div class="max-w-4xl mx-auto text-center space-y-8"><h2 class="headline italic text-4xl leading-relaxed">{htmlmod.escape(data['masterclass_featured']['title'])}</h2><p class="text-[11px] uppercase tracking-[0.2em] text-stone-500 font-bold">{' • '.join(data['masterclass_featured']['topics'])}</p><a class="inline-block px-4 py-2 bg-green-600 text-white rounded-lg font-semibold" href="/episodes/e2273.html">Open Masterclass</a></div></section><section><div class="mb-8"><h2 class="headline italic text-4xl">The Misses</h2></div><div class="grid md:grid-cols-2 gap-8">{''.join(miss_cards)}</div></section></main><footer class="border-t border-stone-200 bg-[#f5f3ee] py-10"><div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between gap-6"><div><p class="headline text-sm font-black mb-2">TWiST Intelligence</p><p class="text-[10px] tracking-widest uppercase text-stone-500">© 2026 TWiST Intelligence. All Rights Reserved.</p></div><div class="flex gap-8 text-xs tracking-widest uppercase text-stone-500"><a href="/index.html">Library</a><a href="/founders/andrew-d-souza.html">Founder Delta</a><a href="/episodes/e2273.html">Masterclass</a><a href="https://x.com/TWiStartups" target="_blank">Twitter</a><a href="https://www.linkedin.com/company/this-week-in-startups/" target="_blank">LinkedIn</a></div></div></footer></div><script>const stateModes={{off:{{leftTitle:'2022 AI Hype frame',leftBody:'General LLM excitement, broad automation optimism, and loose narrative-driven bullishness.',rightTitle:'2026 General AI frame',rightBody:'Broad enthusiasm for autonomous agents before the pricing and rigor filters tighten.'}},on:{{leftTitle:'AI Vibes frame',leftBody:'Narrative-first excitement: demos, clone pressure, and generalized LLM optimism.',rightTitle:'Tabular Data Rigor frame',rightBody:'E2271 and E2272 sharpen the standard: Boardy\'s $17M raise, the $2,000/month cost test, and proof over vibes.'}}}};let stanceOn=true;document.getElementById('compare-toggle').addEventListener('click',()=>{{stanceOn=!stanceOn;const mode=stanceOn?stateModes.on:stateModes.off;document.getElementById('compare-toggle').textContent=stanceOn?'Compare Stance ON':'Compare Stance OFF';document.querySelector('#stance-left div').textContent=mode.leftTitle;document.querySelector('#stance-left p').textContent=mode.leftBody;document.querySelector('#stance-right div').textContent=mode.rightTitle;document.querySelector('#stance-right p').textContent=mode.rightBody;}});</script></body></html>'''
(root/'index.html').write_text(index)
print('regenerated audited multi-page site')
