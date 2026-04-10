from pathlib import Path
import json

p = Path('/Users/smithd98/.openclaw/workspace/wiki/dashboard_data.json')
data = json.loads(p.read_text())

hero_tooltips = {
    'E2273': 'Neurometric: +systems-layer credibility',
    'E2272': 'ClawChief: +product maturity',
    'E2271': 'Boardy: $17M raised',
}
for h in data['hero_episodes']:
    h['audit_hardened'] = True
    h['delta_tooltip'] = hero_tooltips.get(h['episode'], h.get('headline', ''))

founder_updates = {
    "Andrew D'Souza": {
        'image': 'https://images.crunchbase.com/image/upload/c_thumb,h_256,w_256,f_auto,g_faces,z_0.7,q_auto:eco,dpr_2/v1438258327/p2i88mlyqjex79sc2x0l.jpg',
        'audit_hardened': True,
        'delta_tooltip': 'Boardy: $17M raised'
    },
    'Rob May': {
        'image': 'https://images.crunchbase.com/image/upload/c_thumb,h_256,w_256,f_auto,g_faces,z_0.7,q_auto:eco,dpr_2/v1398284534/y3cpx07uonexkivt598q.jpg',
        'audit_hardened': True,
        'delta_tooltip': 'Neurometric: +systems-layer credibility'
    },
    'Ryan Carson': {
        'image': '',
        'audit_hardened': False,
        'delta_tooltip': 'ClawChief: +product maturity'
    },
    'Victor Riparbelli': {
        'image': 'https://cdn.prod.website-files.com/61845f7929f5aa517ebab999/649195a02484a0d8e859ec1a_Victor%20Riparbelli.jpg',
        'audit_hardened': True,
        'delta_tooltip': 'Synthesia: +scale validated'
    }
}
for t in data['trajectory_delta']:
    upd = founder_updates.get(t['founder'])
    if upd:
        t.update(upd)

node_updates = {
    "Andrew D'Souza": ('/founders/andrew-d-souza.html', 'Boardy: $17M raised'),
    'Rob May': ('/founders/rob-may.html', 'Neurometric: +systems-layer credibility'),
    'Ryan Carson': ('/founders/ryan-carson.html', 'ClawChief: +product maturity'),
    'Creandum': ('/episodes/e2271.html', 'Creandum nexus: Boardy institutional validation'),
    'GV': ('/founders/victor-riparbelli.html', 'GV nexus: Synthesia $4B / $200M Series E'),
    'Synthesia': ('/founders/victor-riparbelli.html', 'Synthesia: +scale validated'),
    'Victor Riparbelli': ('/founders/victor-riparbelli.html', 'Synthesia: +scale validated')
}
for n in data['constellation_nodes']:
    if n['label'] in node_updates:
        n['url'], n['delta_tooltip'] = node_updates[n['label']]

for miss in data['the_misses']:
    if miss['company'] == 'Airbnb':
        miss['miss_delta'] = '$78.04B market cap'
        miss['logic_then'] = 'Passed on trust risk in 2009 because mainstream behavior looked too brittle for scale.'
        miss['reality_now'] = 'Software trust layers, ratings, identity, and repeat reputation loops proved to be the $78.04B unlock by 2026.'
        miss['lesson'] = 'When software absorbs trust risk, a category that looked impossible can become inevitable.'
    if miss['company'] == 'Uber':
        miss['miss_delta'] = '12,500x'
        miss['logic_then'] = 'Passed on regulatory and market-structure risk because the category looked capped by legacy transport rules.'
        miss['reality_now'] = 'Liquidity, software trust, and demand aggregation turned a constrained service into a platform-scale winner.'
        miss['lesson'] = 'When software rewrites market structure, old category ceilings break fast.'

p.write_text(json.dumps(data, indent=2))
print('upgraded dashboard data')
