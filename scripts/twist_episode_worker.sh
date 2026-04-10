#!/bin/zsh
set -euo pipefail
ROOT="/Users/smithd98/.openclaw/workspace"
EP_JSON="$ROOT/wiki/raw/twist_latest_20.json"
STATE="$ROOT/wiki/raw/twist_ingest_state.json"
LOG="$ROOT/wiki/raw/twist_worker.log"
PIDFILE="$ROOT/wiki/raw/twist_worker.pid"
mkdir -p "$ROOT/wiki/raw" "$ROOT/wiki/masterclasses" "$ROOT/wiki/founders" "$ROOT/wiki/companies"
echo $$ > "$PIDFILE"
if [ ! -f "$STATE" ]; then
  cat > "$STATE" <<'JSON'
{"nextIndex":0,"targetCount":10,"completed":[],"errors":[]}
JSON
fi
log(){ printf '%s %s\n' "$(date -u +'%Y-%m-%dT%H:%M:%SZ')" "$*" | tee -a "$LOG"; }
cleanup(){ rm -f "$PIDFILE"; }
trap cleanup EXIT
log "worker_start"
python3 - <<'PY'
import json, re, subprocess, time, sys, traceback
from pathlib import Path
root = Path('/Users/smithd98/.openclaw/workspace')
episodes = json.loads((root/'wiki/raw/twist_latest_20.json').read_text())
state_path = root/'wiki/raw/twist_ingest_state.json'
log_path = root/'wiki/raw/twist_worker.log'
def log(msg):
    with log_path.open('a') as f:
        f.write(time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()) + ' ' + msg + '\n')
while True:
    state = json.loads(state_path.read_text())
    i = state.get('nextIndex',0)
    target = min(state.get('targetCount',10), len(episodes))
    if i >= target:
        log('worker_done')
        break
    item = episodes[i]
    prompt = f"Return plain JSON only with keys episode,title,topics,core_question,thesis,axioms,decision_rules,proof_points,contrarian_take,operator_playbook,watchouts,one_line_formula. This is not a summary. Extract a doctrine-first operator playbook from the episode. Rules: 3-5 axioms max, 2-4 decision rules max, proof points must be concrete, operator_playbook must be actionable next-week steps, keep every field concise and high-signal. Episode {item['episode']}: {item['title']}"
    cmd = ['npx','@google/gemini-cli','-p',prompt,'--output-format','json']
    log(f"start {item['episode']}")
    try:
        res = subprocess.run(cmd, cwd=str(root), text=True, capture_output=True, timeout=None)
        if res.returncode != 0:
            err = (res.stderr or res.stdout or '').strip()[:1200]
            state.setdefault('errors', []).append({'episode': item['episode'], 'error': err})
            state['nextIndex'] = i + 1
            state_path.write_text(json.dumps(state, indent=2))
            log(f"error {item['episode']} {err[:200]}")
            time.sleep(30)
            continue
        outer = json.loads(res.stdout)
        resp = outer.get('response','').strip()
        resp = re.sub(r'^```(?:json)?\s*','',resp)
        resp = re.sub(r'\s*```$','',resp)
        try:
            data = json.loads(resp)
        except Exception:
            data = {
                'episode': item['episode'],
                'title': item['title'],
                'topics': [],
                'core_question': '',
                'thesis': resp[:300],
                'axioms': [],
                'decision_rules': [],
                'proof_points': [],
                'contrarian_take': '',
                'operator_playbook': [],
                'watchouts': [],
                'one_line_formula': ''
            }
        (root/'wiki/raw'/f"{item['episode']}_gemini_min.json").write_text(json.dumps(data, indent=2))
        safe = re.sub(r'[^A-Za-z0-9]+','_', item['title']).strip('_')
        mc_path = root/'wiki/masterclasses'/f"{item['episode']}_{safe}.md"
        mc_path.write_text(
            f"---\nepisode: {item['episode']}\ntitle: \"{item['title']}\"\nyoutube_url: \"{item.get('youtube_url','')}\"\nthumbnail: \"{item.get('thumbnail','')}\"\ntopics: {json.dumps(data.get('topics', []))}\nstatus: doctrine_v1\nsource_method: gemini_worker\n---\n\n# {item['episode']} - {item['title']}\n\n## Core Question\n{data.get('core_question','')}\n\n## Thesis\n{data.get('thesis','')}\n\n## Axioms\n" + '\n'.join(f"- {x}" for x in data.get('axioms', [])) + "\n\n## Decision Rules\n" + '\n'.join(f"- {x}" for x in data.get('decision_rules', [])) + "\n\n## Proof Points\n" + '\n'.join(f"- {x}" for x in data.get('proof_points', [])) + f"\n\n## Contrarian Take\n{data.get('contrarian_take','')}\n\n## Operator Playbook\n" + '\n'.join(f"- {x}" for x in data.get('operator_playbook', [])) + "\n\n## Watchouts\n" + '\n'.join(f"- {x}" for x in data.get('watchouts', [])) + f"\n\n## One-Line Formula\n{data.get('one_line_formula','')}\n"
        )
        state.setdefault('completed', []).append(item['episode'])
        state['nextIndex'] = i + 1
        state_path.write_text(json.dumps(state, indent=2))
        log(f"done {item['episode']}")
        time.sleep(15)
    except Exception as e:
        state.setdefault('errors', []).append({'episode': item['episode'], 'error': str(e)[:1200]})
        state['nextIndex'] = i + 1
        state_path.write_text(json.dumps(state, indent=2))
        log(f"exception {item['episode']} {str(e)[:200]}")
        time.sleep(30)
PY
