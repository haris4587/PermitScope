import json,hashlib
from pathlib import Path
root=Path(__file__).resolve().parents[1]
account='0x67da51fd9ac1d52f34f5d01d06da8548979fc514'
def doc(s):
 return {'text':s,'sha256':hashlib.sha256(s.encode()).hexdigest(),'bytes':len(s.encode()),'source':'https://github.com/haris4587/PermitScope'}
p={'id':'DEMO-PERMIT-002','organizer':account,'title':'Riverside community arts evening','venue':'Riverside Hall','valid_from':1798650000,'valid_until':1798664400,'capacity':200,'conditions':[{'id':'music','rule':'Only unamplified acoustic music is permitted. No loudspeakers or electronic amplification.','critical':True},{'id':'alcohol','rule':'No alcohol sale or service is permitted.','critical':True}], 'document':doc('SYNTHETIC DEMONSTRATION PERMIT. Permit DEMO-PERMIT-002 for Riverside Hall. Valid 2026-12-30 17:00:00 UTC to 2026-12-30 21:00:00 UTC. Maximum capacity 200 people. Only unamplified acoustic music is permitted. No loudspeakers or electronic amplification. No alcohol sale or service is permitted. Issuer: demonstration account; no government authorization is implied.')}
s={'id':'DEMO-PLAN-001','permit_id':p['id'],'venue':p['venue'],'start':1798651800,'end':1798660800,'attendance':150,'activities':'Unamplified acoustic guitar performance, water and soft drinks; no alcohol, loudspeakers or electronic amplification.', 'document':doc('SYNTHETIC DEMONSTRATION EVENT PLAN. Plan DEMO-PLAN-001 under permit DEMO-PERMIT-002. Venue Riverside Hall. Event 2026-12-30 17:30:00 UTC to 2026-12-30 20:00:00 UTC. Attendance 150 people. Unamplified acoustic guitar performance only. No loudspeakers or electronic amplification will be used. Water and soft drinks only. No alcohol will be sold or served.')}
r={'integrity':'CONSISTENT','findings':{'music':{'status':'SATISFIED','permit_quote':'Only unamplified acoustic music is permitted.','plan_quote':'Unamplified acoustic guitar performance only.'},'alcohol':{'status':'SATISFIED','permit_quote':'No alcohol sale or service is permitted.','plan_quote':'No alcohol will be sold or served.'}}}
for name,data in [('permit',p),('plan',s),('review.mock',r)]:
 (root/'fixtures'/f'{name}.json').write_text(json.dumps(data,indent=2)+'\n')
print('Synthetic fixtures generated')
