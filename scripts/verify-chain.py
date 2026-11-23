import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
events=json.loads((root/'evidence/events-live.json').read_text());state=json.loads((root/'evidence/verified-live.json').read_text())['state'];previous='0'*64
for i,e in enumerate(events,1):
 e=dict(e);actual=e.pop('event_hash');assert e['sequence']==i and e['previous_hash']==previous
 expected=hashlib.sha256(json.dumps(e,sort_keys=True,separators=(',',':'),ensure_ascii=True).encode()).hexdigest();assert actual==expected
 previous=actual
assert previous==state['head'] and len(events)==state['events']
print(f'{len(events)} event hashes and final head verified')
