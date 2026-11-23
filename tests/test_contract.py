import json,hashlib,copy
from pathlib import Path
from datetime import datetime,timezone
import pytest
ROOT=Path(__file__).resolve().parents[1]
SRC=str(ROOT/'contracts/permit_scope.py')
NOW=1795410000

def fixture(name):return json.loads((ROOT/'fixtures'/f'{name}.json').read_text())
def canonical(x):return json.dumps(x,sort_keys=True,separators=(',',':'),ensure_ascii=True)
def digest(x):return hashlib.sha256(canonical(x).encode()).hexdigest()
def warp(vm,t):
 vm.warp(datetime.fromtimestamp(t,timezone.utc).isoformat())
 from genlayer import gl
 gl.message_raw['datetime']=datetime.fromtimestamp(t,timezone.utc).isoformat()
@pytest.fixture
def setup(direct_vm,direct_deploy,direct_owner):
 direct_vm.warp(datetime.fromtimestamp(NOW,timezone.utc).isoformat());direct_vm.check_pickling=True
 c=direct_deploy(SRC,sdk_version='v0.2.16')
 p=fixture('permit');p['organizer']='0x'+direct_owner.hex()
 s=fixture('plan');r=fixture('review.mock')
 direct_vm.mock_llm('^PERMITSCOPE_REVIEW:',json.dumps(r))
 direct_vm.mock_llm('^PERMITSCOPE_GROUNDING:','{"grounded":true}')
 return direct_vm,c,p,s,r

def lock(setup):
 vm,c,p,s,r=setup
 c.register_permit(json.dumps(p));c.submit_plan(json.dumps(s))
def assess(setup):
 lock(setup);return json.loads(setup[1].assess(setup[3]['id']))
def test_compliant_and_validator(setup):
 e=assess(setup)
 assert e['data']['result']['outcome']=='COMPLIANT'
 assert setup[0].run_validator() is True
 assert e.pop('event_hash')==digest(e)
 assert json.loads(setup[1].effective_status(setup[3]['id']))['status']=='COMPLIANT'
@pytest.mark.parametrize('field,value,issue',[('attendance',201,'capacity_exceeded'),('venue','Other Hall','venue_mismatch'),('start',1798649999,'outside_permitted_dates'),('end',1798664401,'outside_permitted_dates')])
def test_deterministic_violation(setup,field,value,issue):
 setup[3][field]=value
 result=assess(setup)['data']['result']
 assert result['outcome']=='VIOLATION' and issue in result['violations']
@pytest.mark.parametrize('integrity',['UNKNOWN','CONFLICT'])
def test_document_conflict_never_compliant(setup,integrity):
 vm,c,p,s,r=setup;r['integrity']=integrity;vm.clear_mocks();vm.mock_llm('^PERMITSCOPE_REVIEW:',json.dumps(r))
 assert assess(setup)['data']['result']['outcome']=='INCONCLUSIVE'
@pytest.mark.parametrize('state,critical,outcome',[('UNKNOWN',True,'INCONCLUSIVE'),('VIOLATED',True,'VIOLATION'),('VIOLATED',False,'CONDITIONAL')])
def test_semantic_outcomes(setup,state,critical,outcome):
 vm,c,p,s,r=setup;p['conditions'][0]['critical']=critical;r['findings']['music']['status']=state
 if state=='UNKNOWN':r['findings']['music'].update(permit_quote='',plan_quote='')
 vm.clear_mocks();vm.mock_llm('^PERMITSCOPE_REVIEW:',json.dumps(r))
 assert assess(setup)['data']['result']['outcome']==outcome
@pytest.mark.parametrize('mutation',['sha','bytes','unicode','zero','bool','dates','organizer','duplicate','condition_count','extra','url','long','empty'])
def test_bad_permit(setup,mutation):
 vm,c,p,s,r=setup
 if mutation=='sha':p['document']['sha256']='0'*64
 if mutation=='bytes':p['document']['bytes']+=1
 if mutation=='unicode':
  p['document']['text']+='é';p['document']['sha256']=hashlib.sha256(p['document']['text'].encode()).hexdigest();p['document']['bytes']=len(p['document']['text'])
 if mutation=='zero':p['capacity']=0
 if mutation=='bool':p['capacity']=True
 if mutation=='dates':p['valid_until']=NOW-1
 if mutation=='organizer':p['organizer']='0x'+'0'*40
 if mutation=='duplicate':p['conditions'].append(p['conditions'][0])
 if mutation=='condition_count':p['conditions']=[]
 if mutation=='extra':p['arbitrary']=True
 if mutation=='url':p['document']['source']='file:///etc/passwd'
 if mutation=='long':p['document']['text']='x'*14001
 if mutation=='empty':p['title']=' '
 with pytest.raises(Exception):c.register_permit(json.dumps(p))
@pytest.mark.parametrize('field,value',[('attendance',True),('attendance',0),('attendance',1.2),('end',0),('start',0),('id','bad id')])
def test_bad_plan(setup,field,value):
 vm,c,p,s,r=setup;c.register_permit(json.dumps(p));s[field]=value
 with pytest.raises(Exception):c.submit_plan(json.dumps(s))
def test_duplicate_json_keys(setup):
 p=canonical(setup[2]);p=p[:-1]+',"id":"replaced"}'
 with pytest.raises(Exception):setup[1].register_permit(p)
def test_immutability(setup):
 lock(setup);c=setup[1]
 with pytest.raises(Exception):c.register_permit(json.dumps(setup[2]))
 with pytest.raises(Exception):c.submit_plan(json.dumps(setup[3]))
def test_unauthorized_submit(setup):
 setup[2]['organizer']='0x'+'1'*40
 setup[1].register_permit(json.dumps(setup[2]))
 with pytest.raises(Exception):setup[1].submit_plan(json.dumps(setup[3]))
def test_challenge_lifecycle_limit(setup):
 assess(setup);vm,c,p,s,r=setup
 with pytest.raises(Exception):c.assess(s['id'])
 for attempt in [2,3]:
  c.challenge(s['id'],'Review the acoustic music exception in the locked documents.')
  assert json.loads(c.effective_status(s['id']))['status']=='OFFICIAL_REVIEW_REQUIRED'
  with pytest.raises(Exception):c.challenge(s['id'],'duplicate')
  assert json.loads(c.assess(s['id']))['data']['attempt']==attempt
 with pytest.raises(Exception):c.challenge(s['id'],'Attempt four')
 assert json.loads(c.get_status())['events']==7

def test_revocation_overrides_old_receipt(setup):
 assess(setup);vm,c,p,s,r=setup
 c.revoke_permit(p['id'],'Withdrawn by the registered issuer.')
 assert json.loads(c.effective_status(s['id']))['status']=='REVOKED'
 assert json.loads(c.get_assessment(s['id']))['data']['result']['outcome']=='COMPLIANT'
 with pytest.raises(Exception):c.revoke_permit(p['id'],'again')
def test_revoked_no_new_plan(setup):
 vm,c,p,s,r=setup;c.register_permit(json.dumps(p));c.revoke_permit(p['id'],'withdrawn')
 with pytest.raises(Exception):c.submit_plan(json.dumps(s))
@pytest.mark.parametrize('mutation',['quote','extra','unknown_quote','invalid','malformed'])
def test_invalid_model_fails_closed(setup,mutation):
 vm,c,p,s,r=setup
 if mutation=='quote':r['findings']['music']['plan_quote']='invented quote'
 if mutation=='extra':r['extra']=True
 if mutation=='unknown_quote':r['findings']['music']['status']='UNKNOWN'
 if mutation=='invalid':r['integrity']='APPROVED'
 vm.clear_mocks();vm.mock_llm('^PERMITSCOPE_REVIEW:','bad JSON' if mutation=='malformed' else json.dumps(r))
 assert assess(setup)['data']['result']['outcome']=='INCONCLUSIVE'
def test_validator_rejects_disagreement(setup):
 assess(setup);vm,c,p,s,r=setup;r['integrity']='UNKNOWN'
 vm.clear_mocks();vm.mock_llm('^PERMITSCOPE_REVIEW:',json.dumps(r));vm.mock_llm('^PERMITSCOPE_GROUNDING:','{"grounded":true}')
 assert vm.run_validator() is False
def test_validator_rejects_misleading_quotes(setup):
 assess(setup);vm=setup[0];vm.clear_mocks();vm.mock_llm('^PERMITSCOPE_REVIEW:',json.dumps(setup[4]));vm.mock_llm('^PERMITSCOPE_GROUNDING:','{"grounded":false}')
 assert vm.run_validator() is False
def test_event_started_overrides(setup):
 assess(setup);warp(setup[0],setup[3]['start'])
 assert json.loads(setup[1].effective_status(setup[3]['id']))['status']=='EVENT_STARTED'
 with pytest.raises(Exception):setup[1].challenge(setup[3]['id'],'too late')
def test_hash_chain(setup):
 assess(setup);c=setup[1];previous='0'*64
 for i in range(1,4):
  e=json.loads(c.get_event(i));assert e['sequence']==i and e['previous_hash']==previous
  previous=e.pop('event_hash');assert previous==digest(e)
 assert json.loads(c.get_status())['head']==previous
 with pytest.raises(Exception):c.get_event(0)
