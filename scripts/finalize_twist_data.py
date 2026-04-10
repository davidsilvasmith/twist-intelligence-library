from pathlib import Path
import json

p = Path('/Users/smithd98/.openclaw/workspace/wiki/dashboard_data.json')
data = json.loads(p.read_text())

# Truth-audited metrics
for t in data['trajectory_delta']:
    if t['company'] == 'Boardy':
        t['now_label'] = '$17M raised, audited in E2271'
        t['audit_hardened'] = True
        t['delta_tooltip'] = 'Boardy: $17M raised'
    if t['company'] == 'Synthesia':
        t['now_label'] = '$4B valuation, $200M Series E led by GV'
        t['audit_hardened'] = True
        t['delta_tooltip'] = 'Synthesia: +scale validated'

existing = {n['label'] for n in data['constellation_nodes']}
def add_node(label, type_, company, connected_to, url, tooltip, active=True):
    if label not in existing:
        data['constellation_nodes'].append({
            'label': label,
            'type': type_,
            'company': company,
            'connected_to': connected_to,
            'url': url,
            'delta_tooltip': tooltip,
            'active': active
        })
        existing.add(label)

add_node('HalfCourt Ventures', 'vc', 'HalfCourt Ventures', ['Rob May', 'Neurometric'], '/episodes/e2273.html', 'HalfCourt Ventures: Neurometric systems-layer signal')
add_node('Boardy', 'company', 'Boardy', ["Andrew D'Souza", 'Creandum'], '/founders/andrew-d-souza.html', 'Boardy: $17M raised')
add_node('Applied AI', 'concept', 'Applied AI', ['Creandum', 'GV'], '/index.html', 'Applied AI: audited operator layer')
add_node('Victor Riparbelli', 'guest', 'Synthesia', ['NEA', 'GV', 'Synthesia'], '/founders/victor-riparbelli.html', 'Synthesia: +scale validated')
add_node('Neurometric', 'company', 'Neurometric', ['Rob May', 'HalfCourt Ventures'], '/founders/rob-may.html', 'Neurometric: Project Glasswing context')
add_node('OpenClaw ecosystem', 'concept', 'OpenClaw', ['Ryan Carson'], '/episodes/e2272.html', 'OpenClaw ecosystem: workflow economics')

# Ensure canonical URLs/tooltips exist on audited nodes
for n in data['constellation_nodes']:
    if n['label'] == 'Creandum':
        n['url'] = '/episodes/e2271.html'
        n['delta_tooltip'] = 'Creandum nexus: Boardy institutional validation'
    if n['label'] == 'GV':
        n['url'] = '/founders/victor-riparbelli.html'
        n['delta_tooltip'] = 'GV nexus: Synthesia $4B / $200M Series E'
    if n['label'] == 'Synthesia':
        n['url'] = '/founders/victor-riparbelli.html'
        n['delta_tooltip'] = 'Synthesia: +scale validated'

# JSON lint by roundtrip
p.write_text(json.dumps(data, indent=2))
json.loads(p.read_text())
print('finalized dashboard data and validated JSON')
