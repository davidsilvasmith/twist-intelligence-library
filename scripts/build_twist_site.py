from pathlib import Path
import json, re, html as htmlmod

root = Path('/Users/smithd98/.openclaw/workspace')
wiki = root / 'wiki'
templates = root / 'templates'
data = json.loads((wiki / 'dashboard_data.json').read_text())
base_template = (templates / 'base.html').read_text()

hero_vids = {'E2273':'1ORdeSPOy2k','E2272':'1ORdeSPOy2k','E2271':'g5LxEPGLDsc'}
for h in data['hero_episodes']:
    vid = hero_vids.get(h['episode'])
    if vid:
        h['thumbnail'] = f'https://img.youtube.com/vi/{vid}/maxresdefault.jpg'

for n in data['constellation_nodes']:
    if n['label'] == 'Creandum':
        n['delta_tooltip'] = 'Lead investors in Boardy, focused on Applied AI and European breakout founders.'
    if n['label'] == 'GV':
        n['delta_tooltip'] = "Synthesia's Series E lead, the strategic anchor for generative video at scale."

(wiki / 'dashboard_data.json').write_text(json.dumps(data, indent=2))

(root/'episodes').mkdir(exist_ok=True)
(root/'founders').mkdir(exist_ok=True)

def slug(s):
    return re.sub(r'[^a-z0-9]+','-',s.lower()).strip('-')

def episode_url(ep):
    return f'/episodes/{ep.lower()}/'

def founder_url(name):
    return f'/founders/{slug(name)}/'

def write_route(dirpath: Path, body: str):
    dirpath.mkdir(parents=True, exist_ok=True)
    (dirpath / 'index.html').write_text(body)

def render_page(title, body, description, back='/'):
    return (base_template
        .replace('__TITLE__', htmlmod.escape(title))
        .replace('__DESCRIPTION__', htmlmod.escape(description))
        .replace('__BACK__', back)
        .replace('__BODY__', body))

def markdown_to_html(text, ep=None):
    lines = text.splitlines()
    parts = []
    in_list = False
    for raw in lines:
        line = raw.strip()
        if not line:
            if in_list:
                parts.append('</ul>')
                in_list = False
            continue
        if line.startswith('# '):
            if in_list:
                parts.append('</ul>')
                in_list = False
            parts.append(f'<h1 class="headline text-4xl italic mb-4">{htmlmod.escape(line[2:])}</h1>')
            continue
        if line.startswith('## '):
            if in_list:
                parts.append('</ul>')
                in_list = False
            parts.append(f'<h2 class="headline text-2xl italic mb-4 mt-8">{htmlmod.escape(line[3:])}</h2>')
            continue
        if line.startswith(('- ', '* ')):
            if not in_list:
                parts.append('<ul class="list-disc pl-6 mb-6 space-y-2">')
                in_list = True
            content = htmlmod.escape(line[2:])
            content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
            parts.append(f'<li>{content}</li>')
            continue
        if in_list:
            parts.append('</ul>')
            in_list = False
        content = htmlmod.escape(line)
        content = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', content)
        if ep == 'E2271' and 'rows and columns' in line.lower():
            parts.append('<blockquote class="executive-axiom">“If we have data, let’s look at data. If all we have are opinions, let’s go with mine.”<span class="axiom-signature">Jim Barksdale</span></blockquote>')
        parts.append(f'<p class="mb-4 leading-7">{content}</p>')
    if in_list:
        parts.append('</ul>')
    return ''.join(parts)

appearance_map = {
    "Andrew D'Souza": ["E2271"],
    "Rob May": ["E2273"],
    "Ryan Carson": ["E2272"],
    "Victor Riparbelli": []
}

episode_index_cards = []
founder_index_cards = []

for mc in (root/'wiki/masterclasses').glob('*.md'):
    text = mc.read_text()
    ep = re.search(r'episode:\s*(E\d+)', text).group(1)
    title = re.search(r'title:\s*"([^"]+)"', text).group(1)
    yt = re.search(r'youtube_url:\s*"([^"]*)"', text)
    ytu = yt.group(1) if yt else ''
    body_md = re.sub(r'^---.*?---\n','',text, flags=re.S)
    paragraphs = markdown_to_html(body_md, ep=ep)
    guests = [t for t in data['trajectory_delta'] if t.get('episode') == ep]
    guest_links = ''.join(f'<a class="px-3 py-2 bg-white rounded-lg border border-stone-200 hover:border-green-500" href="{founder_url(g["founder"])}">{htmlmod.escape(g["founder"])} · {htmlmod.escape(g["company"])} </a>' for g in guests)
    entities = []
    for g in guests:
        entities.append(f'<a class="px-3 py-2 bg-white rounded-lg border border-stone-200 hover:border-green-500" href="{founder_url(g["founder"])}">{htmlmod.escape(g["founder"])} </a>')
        entities.append(f'<a class="px-3 py-2 bg-stone-50 rounded-lg border border-stone-200 hover:border-green-500" href="{founder_url(g["founder"])}">{htmlmod.escape(g["company"])} </a>')
    thumb = next((h['thumbnail'] for h in data['hero_episodes'] if h['episode']==ep), '')
    rigor_note = ''
    if ep == 'E2271':
        rigor_note = '<section class="mb-10 bg-green-50 border border-green-200 rounded-2xl p-6"><h2 class="headline text-2xl italic mb-4">Jim Barksdale Pivot</h2><p class="leading-7">Jason\'s stance hardens here: away from AI vibes, toward tabular data rigor. The real point is that 70 to 80 percent of enterprise data lives in rows and columns, so the serious operator advantage comes from measurable structured outcomes, not demo heat.</p></section>'
    if ep == 'E2269':
        rigor_note = '<section class="mb-10 bg-stone-100 border border-stone-200 rounded-2xl p-6"><h2 class="headline text-2xl italic mb-4">Why this masterclass matters</h2><p class="leading-7">This is the tactical counterweight to the lore-heavy episodes. It shows founders how to operationalize agents with onboarding, memory, scheduling, self-review, and continuous optimization.</p></section>'
    body = f'''<h1 class="headline text-5xl italic mb-4">{htmlmod.escape(ep)}: {htmlmod.escape(title)}</h1>{('<img class="w-full rounded-2xl mb-8 border border-stone-200" src="'+thumb+'">') if thumb else ''}<div class="flex gap-3 mb-8">{('<a class="inline-block px-4 py-2 bg-green-600 text-white rounded-lg font-semibold" href="'+ytu+'" target="_blank">Open Episode</a>') if ytu else ''}</div>{rigor_note}<section class="mb-10">{paragraphs}</section><section class="mb-10"><h2 class="headline text-2xl italic mb-4">Featured Entities</h2><div class="flex flex-wrap gap-3">{''.join(entities) or '<p class="text-stone-500">No linked entities yet.</p>'}</div></section><section><h2 class="headline text-2xl italic mb-4">Guests</h2><div class="flex flex-wrap gap-3">{guest_links or '<p class="text-stone-500">No linked guest yet.</p>'}</div></section>'''
    write_route(root/'episodes'/ep.lower(), render_page(f'Masterclass: {ep} - {title} | TWiST Wiki', body, f'{ep} masterclass page with linked founders, entities, and audited TWiST context.'))
    episode_index_cards.append(f'<a href="{episode_url(ep)}" class="block bg-white rounded-2xl border border-stone-200 p-6 hover:border-green-500"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">{htmlmod.escape(ep)}</div><h2 class="headline text-2xl italic mb-2">{htmlmod.escape(title)}</h2></a>')

for founder in data['trajectory_delta']:
    name = founder['founder']
    photo = founder.get('image','')
    appearances = appearance_map.get(name, [])
    app_links = ''.join(f'<li><a class="text-green-700 underline" href="{episode_url(ep)}">{ep}</a></li>' for ep in appearances) or '<li class="text-stone-500">No TWiST appearance linked yet.</li>'
    visual = ('<img class="w-44 h-44 rounded-2xl object-cover border border-stone-200" src="'+photo+'" alt="'+htmlmod.escape(name)+'">') if photo else '<div class="w-44 h-44 rounded-2xl neural-placeholder border border-stone-200 flex items-center justify-center text-sm font-bold tracking-[0.25em] text-stone-600">NEURAL</div>'
    vc_jump = ''
    if name == "Andrew D'Souza":
        vc_jump = '<a class="inline-block mt-4 text-green-700 underline" href="/">Jump to Creandum on the Venture Constellation</a>'
    elif name == 'Victor Riparbelli':
        vc_jump = '<a class="inline-block mt-4 text-green-700 underline" href="/">Jump to GV and NEA on the Venture Constellation</a>'
    elif name == 'Rob May':
        vc_jump = '<a class="inline-block mt-4 text-green-700 underline" href="/">Jump to HalfCourt Ventures on the Venture Constellation</a>'
    elif name == 'Ryan Carson':
        vc_jump = '<a class="inline-block mt-4 text-green-700 underline" href="/">Jump to the OpenClaw ecosystem node on the Venture Constellation</a>'
    body = f'''<div class="grid md:grid-cols-[180px,1fr] gap-8 items-start mb-8">{visual}<div><h1 class="headline text-5xl italic mb-2">{htmlmod.escape(name)}</h1><p class="text-lg text-stone-600 mb-6">{htmlmod.escape(founder.get('role',''))}, {htmlmod.escape(founder.get('company',''))}</p><div class="grid md:grid-cols-2 gap-4"><div class="bg-white rounded-2xl p-6 border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Then</div><div class="text-lg font-semibold">{htmlmod.escape(founder.get('then_label',''))}</div></div><div class="bg-white rounded-2xl p-6 border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Now</div><div class="text-lg font-semibold">{htmlmod.escape(founder.get('now_label',''))}</div></div></div>{vc_jump}</div></div><section class="bg-white rounded-2xl p-6 border border-stone-200 mb-8"><h2 class="headline text-2xl italic mb-4">Intervention Note</h2><p class="leading-7">{htmlmod.escape(founder.get('intervention_note',''))}</p><p class="mt-4 text-sm text-stone-500">Verification: {htmlmod.escape(founder.get('verification',''))}</p></section><section><h2 class="headline text-2xl italic mb-4">TWiST Appearance History</h2><ul class="list-disc pl-6 space-y-2">{app_links}</ul></section>'''
    write_route(root/'founders'/slug(name), render_page(f'Founder Trajectory: {name} | TWiST Wiki', body, f'{name} trajectory page with audited company context and TWiST appearance history.'))
    founder_index_cards.append(f'<a href="{founder_url(name)}" class="block bg-white rounded-2xl border border-stone-200 p-6 hover:border-green-500"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">Founder</div><h2 class="headline text-2xl italic mb-2">{htmlmod.escape(name)}</h2><p class="text-stone-600">{htmlmod.escape(founder.get("role",""))}, {htmlmod.escape(founder.get("company",""))}</p></a>')

hero_cards = []
for h in data['hero_episodes']:
    tags = ' '.join(h.get('topics', []))
    audit = 'true' if h.get('audit_hardened') else 'false'
    glow = 'ring-2 ring-green-300/70' if h.get('audit_hardened') else ''
    hero_cards.append(f'''<a href="{episode_url(h['episode'])}" data-audit-hardened="{audit}" data-tags="{htmlmod.escape(tags)}" class="hero-card group block {glow}"><div class="relative aspect-[16/9] rounded-2xl overflow-hidden mb-3 bg-stone-200"><img class="w-full h-full object-cover" src="{h['thumbnail']}" onerror="this.src='{h['thumbnail'].replace('maxresdefault','hqdefault')}'"></div><div class="flex items-center justify-between px-1 py-2 bg-white rounded-lg mb-4"><p class="text-[11px] font-bold text-stone-600 truncate mr-4">{htmlmod.escape(h['delta_label'])}: <span class="text-stone-400">{htmlmod.escape(h['delta_then'])}</span> <span class="text-green-500">→</span> {htmlmod.escape(h['delta_now'])} <span class="text-green-500 ml-1">({htmlmod.escape(h['delta_percent'])})</span></p><svg class="w-16 h-4 stroke-[#39ff14] fill-none stroke-2" viewBox="0 0 100 40"><path d="{h.get('sparkline_path','M0,35 L100,5')}"></path></svg></div><h3 class="headline text-xl font-bold leading-tight">{htmlmod.escape(h['headline'])}</h3></a>''')

traj_cards = []
for t in data['trajectory_delta']:
    img = f'<img class="w-20 h-20 rounded-full object-cover border border-stone-200" src="{t.get("image","")}" alt="{htmlmod.escape(t["founder"])}">' if t.get('image') else '<div class="w-20 h-20 rounded-full neural-placeholder border border-stone-200 flex items-center justify-center text-[10px] font-bold tracking-widest text-stone-600">NEURAL</div>'
    audit = 'true' if t.get('audit_hardened') else 'false'
    glow = 'ring-2 ring-green-300/70' if t.get('audit_hardened') else ''
    traj_cards.append(f'''<a href="{founder_url(t['founder'])}" data-audit-hardened="{audit}" class="founder-card bg-white rounded-xl p-6 shadow-sm flex flex-col justify-between border border-stone-200 hover:border-green-500 transition-colors {glow}"><div class="flex justify-between items-start mb-8">{img}<div class="text-right"><span class="text-[#39ff14] font-bold text-2xl headline">{htmlmod.escape(t['delta_percent'])}</span><p class="text-[10px] text-stone-500 uppercase font-bold tracking-widest">Velocity Delta</p></div></div><div class="mb-8"><h4 class="headline text-lg font-bold mb-1">{htmlmod.escape(t['founder'])}</h4><p class="text-xs text-stone-500 mb-4">{htmlmod.escape(t['role'])}, {htmlmod.escape(t['company'])}</p><div class="flex justify-between font-semibold text-sm gap-4"><span class="text-stone-400">{htmlmod.escape(t['then_label'])}</span><span>{htmlmod.escape(t['now_label'])}</span></div></div><span class="w-full py-3 text-[10px] font-bold uppercase tracking-widest text-[#106e00] border border-green-200 rounded-lg text-center">View Intervention</span></a>''')

miss_cards = []
for m in data['the_misses']:
    miss_cards.append(f'''<article class="bg-white rounded-2xl p-8 border border-stone-200"><div class="flex justify-between items-start mb-6"><div><h3 class="headline text-3xl mb-2">{htmlmod.escape(m['company'])}</h3><p class="text-sm text-stone-500">Vintage: {htmlmod.escape(m['vintage'])}</p></div><div class="text-right"><div class="text-4xl headline font-black text-orange-600">{htmlmod.escape(m['miss_delta'])}</div><div class="text-xs uppercase text-stone-500">Miss Delta</div></div></div><div class="grid md:grid-cols-2 gap-4 mb-4"><div class="bg-stone-50 p-4 rounded-xl"><div class="text-xs uppercase text-stone-500 mb-2">Then</div><p class="text-sm leading-6">{htmlmod.escape(m['logic_then'])}</p></div><div class="bg-orange-50 p-4 rounded-xl"><div class="text-xs uppercase text-stone-500 mb-2">Market Reality</div><p class="text-sm leading-6">{htmlmod.escape(m['reality_now'])}</p></div></div><div class="border-l-4 border-orange-500 pl-4"><div class="text-xs uppercase text-orange-700 mb-2">Lesson</div><p class="text-sm leading-6">{htmlmod.escape(m['lesson'])}</p></div></article>''')

graph_nodes = []
for n in data['constellation_nodes']:
    href = n.get('url') or (founder_url(n['label']) if n['type'] == 'guest' else '/')
    if href.endswith('.html'):
        if '/episodes/' in href:
            href = href.replace('/episodes/', '/episodes/').replace('.html', '/')
        elif '/founders/' in href:
            href = href.replace('/founders/', '/founders/').replace('.html', '/')
        elif href == '/index.html':
            href = '/'
    graph_nodes.append({
        'id': n['label'],
        'group': n['type'],
        'company': n.get('company',''),
        'url': href,
        'tooltip': n.get('delta_tooltip',''),
        'audit_hardened': n.get('active', False) and n.get('type') != 'concept'
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

search_index = []
for h in data['hero_episodes']:
    search_index.append({'type':'episode','label':h['episode'] + ' ' + h['title'],'url':episode_url(h['episode'])})
for t in data['trajectory_delta']:
    search_index.append({'type':'founder','label':t['founder'] + ' ' + t['company'],'url':founder_url(t['founder'])})

index_html = f'''<!DOCTYPE html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width, initial-scale=1"><title>TWiST Intelligence Library | This Week in Startups Knowledge Graph</title><meta name="description" content="Structured This Week in Startups intelligence library with audited founder trajectories, masterclass episodes, and relational venture context."><script src="https://cdn.tailwindcss.com"></script><script src="https://cdn.jsdelivr.net/npm/d3@7"></script><script src="https://cdn.jsdelivr.net/npm/fuse.js@7.0.0"></script><link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=Noto+Serif:ital,wght@0,400;0,700;1,400;1,700&display=swap" rel="stylesheet"><style>body{{font-family:Inter,sans-serif}}.headline{{font-family:'Noto Serif',serif}}.tooltip{{position:absolute;pointer-events:none;background:#0f172a;color:#f8fafc;padding:8px 10px;border-radius:8px;font-size:12px;opacity:0;transition:opacity .15s ease;box-shadow:0 10px 25px rgba(15,23,42,.25)}}.rigor-hidden{{display:none}}.graph-muted{{opacity:.18}}.neural-placeholder{{background:radial-gradient(circle at top left, rgba(255,255,255,0.7), rgba(212,212,216,0.9) 45%, rgba(161,161,170,0.95));backdrop-filter:blur(8px);box-shadow:inset 0 1px 10px rgba(255,255,255,0.4),0 10px 30px rgba(0,0,0,0.08)}}.search-result{{display:block;padding:.5rem .75rem;border-radius:.75rem}}.search-result:hover{{background:#f5f5f4}}</style></head><body class="bg-[#f9f7f2] text-stone-900"><div id="tooltip" class="tooltip"></div><div class="min-h-screen"><nav class="sticky top-0 z-20 bg-[#f9f7f2]/95 backdrop-blur border-b border-stone-200"><div class="max-w-7xl mx-auto px-6 py-4 flex items-center justify-between"><div class="headline text-2xl italic font-bold">TWiST Intelligence</div><div class="flex gap-6 text-sm font-semibold"><a href="/">Library</a><a href="/founders/">Founder Delta</a><a href="/episodes/">Masterclass</a><a href="https://x.com/TWiStartups" target="_blank">Twitter</a><a href="https://www.linkedin.com/company/this-week-in-startups/" target="_blank">LinkedIn</a></div></div></nav><main class="max-w-7xl mx-auto px-6 py-10 space-y-20"><header class="bg-white rounded-3xl border border-stone-200 p-8"><div class="flex items-center justify-between mb-6"><h1 class="headline text-5xl italic">Jason's Take</h1><button id="compare-toggle" class="px-4 py-2 rounded-full bg-green-600 text-white font-semibold">Rigor Mode ON</button></div><div class="mb-6"><input id="dashboard-search" type="search" placeholder="Search founders, episodes, frameworks" class="w-full rounded-2xl border border-stone-300 px-4 py-3"><div id="search-results" class="mt-3 grid gap-2"></div></div><div id="stance-panel" class="grid md:grid-cols-2 gap-4"><div id="stance-left" class="bg-stone-50 p-6 rounded-2xl border border-stone-200"><div class="text-xs uppercase tracking-widest text-stone-500 mb-2">AI Vibes frame</div><p class="headline italic text-xl">Narrative-first excitement: demos, clone pressure, and generalized LLM optimism.</p></div><div id="stance-right" class="bg-green-50 p-6 rounded-2xl border border-green-300"><div class="text-xs uppercase tracking-widest text-green-700 mb-2">Tabular Data Rigor frame</div><p class="headline italic text-xl">E2271 and E2272 sharpen the standard: Boardy's $17M raise, the $2,000/month cost test, and proof over vibes.</p></div></div></header><section><div class="flex justify-between items-end mb-10"><h2 class="headline italic text-4xl">High-Fidelity Intelligence</h2><a href="/episodes/" class="text-green-700 font-semibold">Open masterclasses</a></div><div class="mb-6 bg-green-50 border border-green-200 rounded-2xl p-6"><h3 class="headline text-2xl italic mb-3">Jim Barksdale Pivot</h3><p class="leading-7 text-stone-700">Rigor Mode is not cosmetic. It encodes Jason's shift from AI vibes to tabular data rigor, grounded in the reality that 70 to 80 percent of enterprise data lives in rows and columns. That is where intelligence becomes auditable.</p></div><div class="grid md:grid-cols-3 gap-8">{''.join(hero_cards)}</div></section><section><div class="flex items-end justify-between mb-8"><div><h2 class="headline italic text-4xl">Tactical Frameworks</h2><p class="text-stone-600 mt-2">Practical operator playbooks, not just market lore.</p></div><a href="{episode_url('E2269')}" class="text-green-700 font-semibold">Open E2269 framework</a></div><a href="{episode_url('E2269')}" class="block bg-white rounded-2xl border border-stone-200 p-8 hover:border-green-500"><div class="text-xs uppercase tracking-widest text-stone-500 mb-3">Masterclass Framework</div><h3 class="headline text-3xl italic mb-3">E2269, the 5-step framework for AI agents that improve while you sleep</h3><p class="text-stone-700 leading-7">Onboard agents like hires, give them shared memory, schedule reviews, let them self-troubleshoot, and rewrite instructions from evidence. This makes the library useful to founders today.</p></a></section><section><div class="grid md:grid-cols-12 gap-12 items-center"><div class="md:col-span-4"><h2 class="headline italic text-4xl mb-6">Relationship Constellation</h2><p class="text-stone-600 text-lg leading-relaxed mb-8">Interactive connective tissue between guests, companies, and venture nodes.</p></div><div class="md:col-span-8 aspect-video bg-white rounded-3xl border border-stone-200 shadow-inner overflow-hidden"><svg id="constellation" class="w-full h-full"></svg></div></div></section><section><div class="mb-16"><h2 class="headline italic text-4xl mb-4">Founder Delta</h2><p class="text-stone-600 max-w-xl">Living trajectory pages with then-vs-now proof points.</p></div><div class="grid md:grid-cols-4 gap-6">{''.join(traj_cards)}</div></section><section><div class="max-w-4xl mx-auto text-center space-y-8"><h2 class="headline italic text-4xl leading-relaxed">{htmlmod.escape(data['masterclass_featured']['title'])}</h2><p class="text-[11px] uppercase tracking-[0.2em] text-stone-500 font-bold">{' • '.join(data['masterclass_featured']['topics'])}</p><a class="inline-block px-4 py-2 bg-green-600 text-white rounded-lg font-semibold" href="/episodes/">Open Masterclass</a></div></section><section><div class="mb-8"><h2 class="headline italic text-4xl">The Misses</h2></div><div class="grid md:grid-cols-2 gap-8">{''.join(miss_cards)}</div></section></main><footer class="border-t border-stone-200 bg-[#f5f3ee] py-10"><div class="max-w-7xl mx-auto px-6 flex flex-col md:flex-row justify-between gap-6"><div><p class="headline text-sm font-black mb-2">TWiST Intelligence</p><p class="text-[10px] tracking-widest uppercase text-stone-500">© 2026 TWiST Intelligence. All Rights Reserved.</p></div><div class="flex gap-8 text-xs tracking-widest uppercase text-stone-500"><a href="/">Library</a><a href="/founders/">Founder Delta</a><a href="/episodes/">Masterclass</a><a href="https://x.com/TWiStartups" target="_blank">Twitter</a><a href="https://www.linkedin.com/company/this-week-in-startups/" target="_blank">LinkedIn</a></div></div></footer></div><script>const graphData={json.dumps({'nodes': graph_nodes, 'links': graph_links})};const searchIndex={json.dumps(search_index)};const fuse=new Fuse(searchIndex,{{keys:['label'],threshold:0.32}});const searchInput=document.getElementById('dashboard-search');const searchResults=document.getElementById('search-results');searchInput.addEventListener('input',()=>{{const q=searchInput.value.trim();searchResults.innerHTML='';if(!q)return;fuse.search(q).slice(0,6).forEach(r=>{{const a=document.createElement('a');a.href=r.item.url;a.className='search-result border border-stone-200 bg-white';a.textContent=r.item.label;searchResults.appendChild(a);}});}});const svg=d3.select('#constellation');const width=svg.node().parentElement.clientWidth||800;const height=svg.node().parentElement.clientHeight||450;svg.attr('viewBox','0 0 '+width+' '+height);const tooltip=document.getElementById('tooltip');const color=(g)=>g==='vc'?'#166534':g==='company'?'#1d4ed8':g==='guest'?'#39ff14':g==='concept'?'#7c3aed':'#111827';const simulation=d3.forceSimulation(graphData.nodes).force('link',d3.forceLink(graphData.links).id(d=>d.id).distance(110)).force('charge',d3.forceManyBody().strength(-260)).force('center',d3.forceCenter(width/2,height/2));const link=svg.append('g').selectAll('line').data(graphData.links).join('line').attr('stroke','#d1d5db').attr('stroke-width',1.5);const node=svg.append('g').selectAll('circle').data(graphData.nodes).join('circle').attr('r',d=>d.group==='vc'?10:d.group==='concept'?7:8).attr('fill',d=>color(d.group)).style('cursor','pointer').call(d3.drag().on('start',(event,d)=>{{if(!event.active)simulation.alphaTarget(0.3).restart();d.fx=d.x;d.fy=d.y;}}).on('drag',(event,d)=>{{d.fx=event.x;d.fy=event.y;}}).on('end',(event,d)=>{{if(!event.active)simulation.alphaTarget(0);d.fx=null;d.fy=null;}}));const label=svg.append('g').selectAll('text').data(graphData.nodes).join('text').text(d=>d.id).attr('font-size',11).attr('fill','#334155');node.on('mousemove',(event,d)=>{{tooltip.style.opacity=1;tooltip.textContent=d.tooltip||d.company||d.id;tooltip.style.left=(event.pageX+12)+'px';tooltip.style.top=(event.pageY+12)+'px';}}).on('mouseleave',()=>{{tooltip.style.opacity=0;}}).on('click',(event,d)=>{{if(d.url)window.location.href=d.url;}});simulation.on('tick',()=>{{link.attr('x1',d=>d.source.x).attr('y1',d=>d.source.y).attr('x2',d=>d.target.x).attr('y2',d=>d.target.y);node.attr('cx',d=>d.x).attr('cy',d=>d.y);label.attr('x',d=>d.x+12).attr('y',d=>d.y+4);}});const stateModes={{off:{{leftTitle:'2022 AI Hype frame',leftBody:'General LLM excitement, broad automation optimism, and loose narrative-driven bullishness.',rightTitle:'2026 General AI frame',rightBody:'Broad enthusiasm for autonomous agents before the pricing and rigor filters tighten.'}},on:{{leftTitle:'Jim Barksdale Pivot',leftBody:'AI vibes break when the operator cannot trace outcomes back to structured evidence.',rightTitle:'Tabular Data Rigor',rightBody:'Jason\'s pivot is earned: 70 to 80 percent of enterprise data lives in rows and columns, so rigor means measurable tabular truth, not hype.'}}}};let rigorOn=true;function applyRigor(){{document.querySelectorAll('.hero-card,.founder-card').forEach(el=>{{const keep=el.dataset.auditHardened==='true';el.classList.toggle('rigor-hidden',rigorOn && !keep);el.classList.toggle('ring-2',keep && rigorOn);el.classList.toggle('ring-green-300',keep && rigorOn);}});node.classed('graph-muted',d=>rigorOn && !d.audit_hardened);label.classed('graph-muted',d=>rigorOn && !d.audit_hardened);link.classed('graph-muted',d=>rigorOn && (!(d.source.audit_hardened)&&!(d.target.audit_hardened)));const mode=rigorOn?stateModes.on:stateModes.off;document.getElementById('compare-toggle').textContent=rigorOn?'Rigor Mode ON':'Rigor Mode OFF';document.querySelector('#stance-left div').textContent=mode.leftTitle;document.querySelector('#stance-left p').textContent=mode.leftBody;document.querySelector('#stance-right div').textContent=mode.rightTitle;document.querySelector('#stance-right p').textContent=mode.rightBody;}}setTimeout(()=>{{applyRigor();}},1000);document.getElementById('compare-toggle').addEventListener('click',()=>{{rigorOn=!rigorOn;applyRigor();}});applyRigor();</script></body></html>'''
(root/'index.html').write_text(index_html)

founders_index = render_page(
    'Founders | TWiST Wiki',
    '<h1 class="headline text-5xl italic mb-8">Founders</h1><div class="grid md:grid-cols-2 gap-6">' + ''.join(founder_index_cards) + '</div>',
    'Founder trajectories and living histories from the TWiST intelligence library.',
    back='/'
)
write_route(root/'founders', founders_index)

episodes_index = render_page(
    'Episodes | TWiST Wiki',
    '<h1 class="headline text-5xl italic mb-8">Episodes</h1><div class="grid md:grid-cols-2 gap-6">' + ''.join(episode_index_cards) + '</div>',
    'Masterclass episodes from the TWiST intelligence library.',
    back='/'
)
write_route(root/'episodes', episodes_index)

print('regenerated audited multi-page site')
