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
    if not t.get('image'):
        t['image'] = founder_images.get(t['founder'],'')
    if t['company'] == 'Boardy':
        t['now_label'] = '$17M raised, audited in E2271'
    if t['company'] == 'Synthesia':
        t['now_label'] = '$4B valuation, $200M Series E led by GV'
    if t['company'] == 'Neurometric':
        t['now_label'] = 'Project Glasswing context, inference-time compute moat'
for m in data['the_misses']:
    if m['company'] == 'Airbnb':
        m['miss_delta'] = '$78.04B market cap'
        m['reality_now'] = 'Software trust layers, ratings, identity, and repeat reputation loops proved to be the $78.04B unlock by 2026.'

(wiki / 'dashboard_data.json').write_text(json.dumps(data, indent=2))

(root/'episodes').mkdir(exist_ok=True)
(root/'founders').mkdir(exist_ok=True)

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def base_page(title, body, back='/index.html', description='Structured TWiST intelligence page.'):
    return f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>{htmlmod.escape(title)}</title><meta name="description" content="{htmlmod.escape(description)}"><script src="https://cdn.tailwindcss.com"></script><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet"><style>body{{font-family:Inter,sans-serif}} .headline{{font-family:'Noto Serif',serif}}</style></head><body class="bg-stone-50 text-stone-900"><main class="max-w-5xl mx-auto px-6 py-12"><div class="flex items-center justify-between mb-8"><a href="{back}" class="text-green-700 font-semibold">← Back to dashboard</a><nav class="flex gap-4 text-sm"><a href="/index.html">Home</a><a href="/founders/andrew-d-souza.html">Founders</a><a href="/episodes/e2273.html">Episodes</a><a href="https://x.com/TWiStartups" target="_blank">Twitter</a><a href="https://www.linkedin.com/company/this-week-in-startups/" target="_blank">LinkedIn</a></nav></div>{body}</main></body></html>'''

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
    entities = []
    for g in guests:
        entities.append(f'<a class="px-3 py-2 bg-white rounded-lg border border-stone-200 hover:border-green-500" href="/founders/{slug(g["founder"])}.html">{htmlmod.escape(g["founder"])} </a>')
        entities.append(f'<a class="px-3 py-2 bg-stone-50 rounded-lg border border-stone-200 hover:border-green-500" href="/founders/{slug(g["founder"])}.html">{htmlmod.escape(g["company"])} </a>')
    thumb = next((h['thumbnail'] for h in data['hero_episodes'] if h['episode']==ep), '')
    body = f'''<h1 class="headline text-5xl italic mb-4">{htmlmod.escape(ep)}: {htmlmod.escape(title)}</h1>{('<img class="w-full rounded-2xl mb-8 border border-stone-200" src="'+thumb+'">') if thumb else ''}<div class="flex gap-3 mb-8">{('<a class="inline-block px-4 py-2 bg-green-600 text-white rounded-lg font-semibold" href="'+ytu+'" target="_blank">Open Episode</a>') if ytu else ''}</div><section class="mb-10"><h2 class="headline text-2xl italic mb-4">Masterclass</h2>{paragraphs}</section><section class="mb-10"><h2 class="headline text-2xl italic mb-4">Featured Entities</h2><div class="flex flex-wrap gap-3">{''.join(entities) or '<p class="text-stone-500">No linked entities yet.</p>'}</div></section><section><h2 class="headline text-2xl italic mb-4">Guests</h2><div class="flex flex-wrap gap-3">{guest_links or '<p class="text-stone-500">No linked guest yet.</p>'}</div></section>'''
    (root/'episodes'/f'{ep.lower()}.html').write_text(base_page(f'Masterclass: {ep} - {title} | TWiST Wiki', body, description=f'{ep} masterclass page with linked founders, entities, and audited TWiST context.'))

for founder in data['trajectory_delta']:
    name = founder['founder']
    photo = founder.get('image','')
    appearances = appearance_map.get(name, [])
    app_links = ''.join(f'<li><a class="text-green-700 underline" href="/episodes/{ep.lower()}.html">{ep}</a></li>' for ep in appearances) or '<li class="text-stone-500">No TWiST appearance linked yet.</li>'
    body = f'''<div class="grid md:grid-cols-[180px,1fr] gap-8 items-start mb-8">{('<img class="w-44 h-44 rounded-2xl object-cover border border-stone-200" src="'+photo+'" alt="'+htmlmod.escape(name)+'">') if photo else '<div class="w-44 h-44 rounded-2xl bg-stone-200 border border-stone-200"></div>'}<div><h1 class="headline text-5xl italic mb-2">{htmlmod.escape(name)}</h1><p class="text-lg text-stone-600 mb-6">{htmlmod.escape(founder.get('role',''))}, {htmlmod.escape(founder.get('company',''))}</p><div class="grid md:grid-cols-2 gap-4"><div class="bg-white rounded-2xl p-6 border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Then</div><div class="text-lg font-semibold">{htmlmod.escape(founder.get('then_label',''))}</div></div><div class="bg-white rounded-2xl p-6 border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Now</div><div class="text-lg font-semibold">{htmlmod.escape(founder.get('now_label',''))}</div></div></div></div></div><section class="bg-white rounded-2xl p-6 border border-stone-200 mb-8"><h2 class="headline text-2xl italic mb-4">Intervention Note</h2><p class="leading-7">{htmlmod.escape(founder.get('intervention_note',''))}</p><p class="mt-4 text-sm text-stone-500">Verification: {htmlmod.escape(founder.get('verification',''))}</p></section><section><h2 class="headline text-2xl italic mb-4">TWiST Appearance History</h2><ul class="list-disc pl-6 space-y-2">{app_links}</ul></section>'''
    (root/'founders'/f'{slug(name)}.html').write_text(base_page(f'Founder Trajectory: {name} | TWiST Wiki', body, description=f'{name} trajectory page with audited company context and TWiST appearance history.'))

hero_cards = []
for h in data['hero_episodes']:
    tags = ' '.join(h.get('topics', []))
    audit = 'true' if h.get('audit_hardened') else 'false'
    glow = 'ring-2 ring-green-300/70' if h.get('audit_hardened') else ''
    hero_cards.append(f'''<a href="/episodes/{h['episode'].lower()}.html" data-audit-hardened="{audit}" data-tags="{htmlmod.escape(tags)}" class="hero-card group block {glow}"><div class="relative aspect-[16/9] rounded-2xl overflow-hidden mb-3 bg-stone-200"><img class="w-full h-full object-cover" src="{h['thumbnail']}" onerror="this.src='{h['thumbnail'].replace('maxresdefault','hqdefault')}'"></div><div class="flex items-center justify-between px-1 py-2 bg-white rounded-lg mb-4"><p class="text-[11px] font-bold text-stone-600 truncate mr-4">{htmlmod.escape(h['delta_label'])}: <span class="text-stone-400">{htmlmod.escape(h['delta_then'])}</span> <span class="text-green-500">→</span> {htmlmod.escape(h['delta_now'])} <span class="text-green-500 ml-1">({htmlmod.escape(h['delta_percent'])})</span></p><svg class="w-16 h-4 stroke-[#39ff14] fill-none stroke-2" viewBox="0 0 100 40"><path d="{h.get('sparkline_path','M0,35 L100,5')}"></path></svg></div><h3 class="headline text-xl font-bold leading-tight">{htmlmod.escape(h['headline'])}</h3></a>''')

traj_cards = []
for t in data['trajectory_delta']:
    img = f'<img class="w-20 h-20 rounded-full object-cover border border-stone-200" src="{t.get("image","")}" alt="{htmlmod.escape(t["founder"])}">' if t.get('image') else '<div class="w-20 h-20 rounded-full bg-stone-200 border border-stone-200"></div>'
    audit = 'true' if t.get('audit_hardened') else 'false'
    glow = 'ring-2 ring-green-300/70' if t.get('audit_hardened') else ''
    traj_cards.append(f'''<a href="/founders/{slug(t['founder'])}.html" data-audit-hardened="{audit}" class="founder-card bg-white rounded-xl p-6 shadow-sm flex flex-col justify-between border border-stone-200 hover:border-green-500 transition-colors {glow}"><div class="flex justify-between items-start mb-8">{img}<div class="text-right"><span class="text-[#39ff14] font-bold text-2xl headline">{htmlmod.escape(t['delta_percent'])}</span><p class="text-[10px] text-stone-500 uppercase font-bold tracking-widest">Velocity Delta</p></div></div><div class="mb-8"><h4 class="headline text-lg font-bold mb-1">{htmlmod.escape(t['founder'])}</h4><p class="text-xs text-stone-500 mb-4">{htmlmod.escape(t['role'])}, {htmlmod.escape(t['company'])}</p><div class="flex justify-between font-semibold text-sm gap-4"><span class="text-stone-400">{htmlmod.escape(t['then_label'])}</span><span>{htmlmod.escape(t['now_label'])}</span></div></div><span class="w-full py-3 text-[10px] font-bold uppercase tracking-widest text-[#106e00] border border-green-200 rounded-lg text-center">View Intervention</span></a>''')

miss_cards = []
for m in data['the_misses']:
    miss_cards.append(f'''<article class="bg-white rounded-2xl p-8 border border-stone-200"><div class="flex justify-between items-start mb-6"><div><h3 class="headline text-3xl mb-2">{htmlmod.escape(m['company'])}</h3><p class="text-sm text-stone-500">Vintage: {htmlmod.escape(m['vintage'])}</p></div><div class="text-right"><div class="text-4xl headline font-black text-orange-600">{htmlmod.escape(m['miss_delta'])}</div><div class="text-xs uppercase text-stone-500">Miss Delta</div></div></div><div class="grid md:grid-cols-2 gap-4 mb-4"><div class="bg-stone-50 p-4 rounded-xl"><div class="text-xs uppercase text-stone-500 mb-2">Then</div><p class="text-sm leading-6">{htmlmod.escape(m['logic_then'])}</p></div><div class="bg-orange-50 p-4 rounded-xl"><div class="text-xs uppercase text-stone-500 mb-2">Market Reality</div><p class="text-sm leading-6">{htmlmod.escape(m['reality_now'])}</p></div></div><div class="border-l-4 border-orange-500 pl-4"><div class="text-xs uppercase text-orange-700 mb-2">Lesson</div><p class="text-sm leading-6">{htmlmod.escape(m['lesson'])}</p></div></article>''')

graph_nodes = []
for n in data['constellation_nodes']:
    href = n.get('url') or ('/founders/' + slug(n['label']) + '.html' if n['type'] == 'guest' else '/index.html')
    graph_nodes.append({
        'id': n['label'],
        'group': n['type'],
        'company': n.get('company',''),
        'url': href,
        'tooltip': n.get('delta_tooltip',''),
        'audit_hardened': n.get('active', False)
    })

graph_links = []
drawn = set()
for n in data['constellation_nodes']:
    for target in n.get('connected_to',[]):
        key = '::'.join(sorted([n['label'], target]))
        if key in drawn:
            continue
        drawn.add(key)
        graph_links.append({'source': n['label'], 'target': target})

index_template = """<!DOCTYPE html><html lang=\"en\"><head><meta charset=\"utf-8\"><meta name=\"viewport\" content=\"width=device-width, initial-scale=1\"><title>TWiST Intelligence Library | This Week in Startups Knowledge Graph</title><meta name=\"description\" content=\"__DESCRIPTION__\"><script src=\"https://cdn.tailwindcss.com\"></script><script src=\"https://cdn.jsdelivr.net/npm/d3@7\"></script><link href=\"https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap\" rel=\"stylesheet\"><style>body{font-family:Inter,sans-serif}.headline{font-family:'Noto Serif',serif}.tooltip{position:absolute;pointer-events:none;background:#111827;color:#fff;padding:8px 10px;border-radius:8px;font-size:12px;opacity:0;transition:opacity .15s ease}.rigor-hidden{display:none}</style></head><body class=\"bg-[#f9f7f2] text-stone-900\"><div id=\"tooltip\" class=\"tooltip\"></div><div class=\"min-h-screen\"><nav class=\"sticky top-0 z-20 bg-[#f9f7f2]/95 backdrop-blur border-b border-stone-200\"><div class=\"max-w-7xl mx-auto px-6 py-4 flex items-center justify-between\"><div class=\"headline text-2xl italic font-bold\">TWiST Intelligence</div><div class=\"flex gap-6 text-sm font-semibold\"><a href=\"/index.html\">Library</a><a href=\"/founders/andrew-d-souza.html\">Founder Delta</a><a href=\"/episodes/e2273.html\">Masterclass</a><a href=\"https://x.com/TWiStartups\" target=\"_blank\">Twitter</a><a href=\"https://www.linkedin.com/company/this-week-in-startups/\" target=\"_blank\">LinkedIn</a></div></div></nav><main class=\"max-w-7xl mx-auto px-6 py-10 space-y-20\"><header class=\"bg-white rounded-3xl border border-stone-200 p-8\"><div class=\"flex items-center justify-between mb-6\"><h1 class=\"headline text-5xl italic\">Jason's Take</h1><button id=\"compare-toggle\" class=\"px-4 py-2 rounded-full bg-green-600 text-white font-semibold\">Rigor Mode ON</button></div><div id=\"stance-panel\" class=\"grid md:grid-cols-2 gap-4\"><div id=\"stance-left\" class=\"bg-stone-50 p-6 rounded-2xl border border-stone-200\"><div class=\"text-xs uppercase tracking-widest text-stone-500 mb-2\">AI Vibes frame</div><p class=\"headline italic text-xl\">Narrative-first excitement: demos, clone pressure, and generalized LLM optimism.</p></div><div id=\"stance-right\" class=\"bg-green-50 p-6 rounded-2xl border border-green-300\"><div class=\"text-xs uppercase tracking-widest text-green-700 mb-2\">Tabular Data Rigor frame</div><p class=\"headline italic text-xl\">E2271 and E2272 sharpen the standard: Boardy's $17M raise, the $2,000/month cost test, and proof over vibes.</p></div></div></header><section><div class=\"flex justify-between items-end mb-10\"><h2 class=\"headline italic text-4xl\">High-Fidelity Intelligence</h2><a href=\"/episodes/e2273.html\" class=\"text-green-700 font-semibold\">Open featured masterclass</a></div><div class=\"grid md:grid-cols-3 gap-8\">__HERO_CARDS__</div></section><section><div class=\"grid md:grid-cols-12 gap-12 items-center\"><div class=\"md:col-span-4\"><h2 class=\"headline italic text-4xl mb-6\">Relationship Constellation</h2><p class=\"text-stone-600 text-lg leading-relaxed mb-8\">Interactive connective tissue between guests, companies, and venture nodes.</p></div><div class=\"md:col-span-8 aspect-video bg-white rounded-3xl border border-stone-200 shadow-inner overflow-hidden\"><svg id=\"constellation\" class=\"w-full h-full\"></svg></div></div></section><section><div class=\"mb-16\"><h2 class=\"headline italic text-4xl mb-4\">Founder Delta</h2><p class=\"text-stone-600 max-w-xl\">Living trajectory pages with then-vs-now proof points.</p></div><div class=\"grid md:grid-cols-4 gap-6\">__TRAJ_CARDS__</div></section><section><div class=\"max-w-4xl mx-auto text-center space-y-8\"><h2 class=\"headline italic text-4xl leading-relaxed\">__FEATURED_TITLE__</h2><p class=\"text-[11px] uppercase tracking-[0.2em] text-stone-500 font-bold\">__FEATURED_TOPICS__</p><a class=\"inline-block px-4 py-2 bg-green-600 text-white rounded-lg font-semibold\" href=\"/episodes/e2273.html\">Open Masterclass</a></div></section><section><div class=\"mb-8\"><h2 class=\"headline italic text-4xl\">The Misses</h2></div><div class=\"grid md:grid-cols-2 gap-8\">__MISS_CARDS__</div></section></main><footer class=\"border-t border-stone-200 bg-[#f5f3ee] py-10\"><div class=\"max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between gap-6\"><div><p class=\"headline text-sm font-black mb-2\">TWiST Intelligence</p><p class=\"text-[10px] tracking-widest uppercase text-stone-500\">© 2026 TWiST Intelligence. All Rights Reserved.</p></div><div class=\"flex gap-8 text-xs tracking-widest uppercase text-stone-500\"><a href=\"/index.html\">Library</a><a href=\"/founders/andrew-d-souza.html\">Founder Delta</a><a href=\"/episodes/e2273.html\">Masterclass</a><a href=\"https://x.com/TWiStartups\" target=\"_blank\">Twitter</a><a href=\"https://www.linkedin.com/company/this-week-in-startups/\" target=\"_blank\">LinkedIn</a></div></div></footer></div><script>const graphData=__GRAPH_DATA__;const svg=d3.select('#constellation');const width=svg.node().parentElement.clientWidth||800;const height=svg.node().parentElement.clientHeight||450;svg.attr('viewBox','0 0 '+width+' '+height);const tooltip=document.getElementById('tooltip');const color=(g)=>g==='vc'?'#166534':g==='company'?'#1d4ed8':g==='guest'?'#39ff14':'#111827';const simulation=d3.forceSimulation(graphData.nodes).force('link',d3.forceLink(graphData.links).id(d=>d.id).distance(110)).force('charge',d3.forceManyBody().strength(-260)).force('center',d3.forceCenter(width/2,height/2));const link=svg.append('g').selectAll('line').data(graphData.links).join('line').attr('stroke','#d1d5db').attr('stroke-width',1.5);const node=svg.append('g').selectAll('circle').data(graphData.nodes).join('circle').attr('r',d=>d.group==='vc'?10:8).attr('fill',d=>color(d.group)).style('cursor','pointer').call(d3.drag().on('start',(event,d)=>{if(!event.active)simulation.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}).on('drag',(event,d)=>{d.fx=event.x;d.fy=event.y;}).on('end',(event,d)=>{if(!event.active)simulation.alphaTarget(0);d.fx=null;d.fy=null;}));const label=svg.append('g').selectAll('text').data(graphData.nodes).join('text').text(d=>d.id).attr('font-size',11).attr('fill','#334155');node.on('mousemove',(event,d)=>{tooltip.style.opacity=1;tooltip.textContent=d.tooltip||d.company||d.id;tooltip.style.left=(event.pageX+12)+'px';tooltip.style.top=(event.pageY+12)+'px';}).on('mouseleave',()=>{tooltip.style.opacity=0;}).on('click',(event,d)=>{if(d.url)window.location.href=d.url;});simulation.on('tick',()=>{link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);node.attr('cx',d=>d.x).attr('cy',d=>d.y);label.attr('x',d=>d.x+12).attr('y',d=>d.y+4);});const stateModes={off:{leftTitle:'2022 AI Hype frame',leftBody:'General LLM excitement, broad automation optimism, and loose narrative-driven bullishness.',rightTitle:'2026 General AI frame',rightBody:'Broad enthusiasm for autonomous agents before the pricing and rigor filters tighten.'},on:{leftTitle:'AI Vibes frame',leftBody:'Narrative-first excitement: demos, clone pressure, and generalized LLM optimism.',rightTitle:'Tabular Data Rigor frame',rightBody:'E2271 and E2272 sharpen the standard: Boardy\'s $17M raise, the $2,000/month cost test, and proof over vibes.'}};let rigorOn=true;function applyRigor(){document.querySelectorAll('.hero-card,.founder-card').forEach(el=>{const keep=el.dataset.auditHardened==='true';el.classList.toggle('rigor-hidden',rigorOn && !keep);el.classList.toggle('ring-2',keep && rigorOn);el.classList.toggle('ring-green-300',keep && rigorOn);});const mode=rigorOn?stateModes.on:stateModes.off;document.getElementById('compare-toggle').textContent=rigorOn?'Rigor Mode ON':'Rigor Mode OFF';document.querySelector('#stance-left div').textContent=mode.leftTitle;document.querySelector('#stance-left p').textContent=mode.leftBody;document.querySelector('#stance-right div').textContent=mode.rightTitle;document.querySelector('#stance-right p').textContent=mode.rightBody;}document.getElementById('compare-toggle').addEventListener('click',()=>{rigorOn=!rigorOn;applyRigor();});applyRigor();</script></body></html>"""

index = index_template.replace('__DESCRIPTION__', 'Structured This Week in Startups intelligence library with audited founder trajectories, masterclass episodes, and relational venture context.').replace('__HERO_CARDS__', ''.join(hero_cards)).replace('__TRAJ_CARDS__', ''.join(traj_cards)).replace('__FEATURED_TITLE__', htmlmod.escape(data['masterclass_featured']['title'])).replace('__FEATURED_TOPICS__', ' • '.join(data['masterclass_featured']['topics'])).replace('__MISS_CARDS__', ''.join(miss_cards)).replace('__GRAPH_DATA__', json.dumps({'nodes': graph_nodes, 'links': graph_links}))
(root/'index.html').write_text(index)
print('regenerated audited multi-page site')
