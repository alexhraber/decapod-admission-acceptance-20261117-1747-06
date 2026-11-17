"""Project real private captures into allowlisted, independently inspectable witnesses.

No model narration is treated as fact. Native child calls join unique actual bash
execution intervals. Git samples are delivered after their corresponding tool
result; their original sampling times and raw-source digests are retained.
"""
import pathlib,json,hashlib,time,os
RUN=pathlib.Path(os.environ['DECAPOD_ACCEPTANCE_RUN']).resolve()
OUT=RUN/'public-witnesses';OUT.mkdir(mode=0o700,exist_ok=True)
REPO=os.environ['DECAPOD_ACCEPTANCE_REPOSITORY_SLUG']
def sha(b):return 'sha256:'+hashlib.sha256(b).hexdigest()
def records(name):return [json.loads(l) for l in (RUN/name).read_text().splitlines()]
host=records('pi.received.private.jsonl'); boundaries=records('host-boundaries.private.jsonl')
start={};end={};pending=[];docs={k:[] for k in ['host','kernel','git','github']}
rawhost=sha((RUN/'pi.received.private.jsonl').read_bytes())
def add(source,ns,value):
 i=len(docs[source]);docs[source].append(value);pending.append((ns,source,i))
for n,row in enumerate(host):
 e=row['event'];typ=e['type'];safe=None
 if typ=='message_end':
  m=e['message'];safe={'type':typ,'message':{k:m[k] for k in ['role','provider','model','stopReason'] if k in m}}
  if m['role']=='user':safe['message']['content']=m['content']
  elif m['role']=='assistant':safe['message']['content']=[{k:c[k] for k in ['type','id','name']} for c in m['content'] if c['type']=='toolCall']
  else:safe=None
 elif typ in ['tool_execution_start','tool_execution_end']:
  safe={k:e[k] for k in ['type','toolCallId','toolName','isError'] if k in e}
  (start if typ.endswith('start') else end)[e['toolCallId']]=row['received_ns']
 if safe is not None:
  safe['private_source']={'sha256':rawhost,'pointer':f'/{n}/event','redaction':'reasoning, narration, arguments and tool output omitted'}
  add('host',row['received_ns'],safe)
assert start.keys()==end.keys()
for f in sorted((RUN/'native').glob('invocation-*.json')):
 d=json.loads(f.read_text());op=d['operation']
 if op not in ['context','claim','workspace','validate','publish']:continue
 ids=[i for i in start if start[i]<=d['started_ns']<=d['ended_ns']<=end[i]]
 assert len(ids)==1,(f.name,ids)
 tool=ids[0]
 assert next(r['event']['toolName'] for r in host if r['event']['type']=='tool_execution_start' and r['event']['toolCallId']==tool)=='bash'
 o=d['output'];assert isinstance(o,dict) or op=='context'
 if op=='context':o={'status':'ok' if d['exit_code']==0 else 'error'}
 elif op=='claim':o={k:o[k] for k in ['status','id'] if k in o}|{'result':{k:o['result'][k] for k in ['lease_generation','lease_seconds','assigned_to','mode'] if k in o['result']}}
 elif op=='workspace':o={k:o[k] for k in ['status','branch','can_work'] if k in o}
 elif op=='validate':o={k:o[k] for k in ['status','publication_ready','scope'] if k in o}
 elif op=='publish':o={k:o[k] for k in ['status','branch','commit_hash','pr_url','pr_verified','remote_verified','warnings'] if k in o}
 safe={k:d[k] for k in ['operation','exit_code','binary_sha256','reason_codes']}
 safe.update(repository=REPO,host_tool_call_id=tool,output=o,
  private_source={'sha256':sha(f.read_bytes()),'file_id':f.name,'redaction':'argv, local paths, session output and arbitrary text omitted'})
 for k in ['plan','observations','receipt']:
  if k in d:safe[k]=d[k]
 add('kernel',d['ended_ns'],safe)
for row in boundaries:
 if row['phase']!='tool_result':continue
 ident=row['event']['toolCallId']
 if ident not in end:continue # prerequisite smoke test, outside the primary process
 for w in row['git']['worktrees']:
  if not w['branch'].startswith('agent/'+os.environ['DECAPOD_ACCEPTANCE_AGENT']+'/'):continue
  safe={k:w[k] for k in ['head','base','clean','branch','material_sha256']}
  safe.update(repository=REPO,tool_call_id=ident,sampled_ns=row['git']['time_ns'],
   private_source={'sha256':sha(json.dumps(row,sort_keys=True).encode()),'scope':'bounded non-atomic tool-boundary Git sample'})
  add('git',end[ident]+1,safe)
forge=json.loads((RUN/'forge-readback.private.json').read_text())
add('github',max(x[0] for x in pending)+1,{'head':forge['headRefOid'],'base':forge['actual_target'],'branch':forge['headRefName'],'base_branch':forge['baseRefName'],'url':forge['url'],'merged':forge['mergedAt'] is not None,'state':forge['state'],
 'private_source':{'sha256':sha((RUN/'forge-readback.private.json').read_bytes()),'scope':'independent gh PR readback plus live target ref'}})
if (RUN/'forge-after-controls.private.json').exists():
 current=json.loads((RUN/'forge-after-controls.private.json').read_text())
 snapshot=json.loads((RUN/'git-after-controls.private.json').read_text())
 primary=next(w for w in snapshot['worktrees'] if w['branch'].startswith('agent/'+os.environ['DECAPOD_ACCEPTANCE_AGENT']+'/'))
 assert primary['head']==forge['headRefOid'] and primary['clean']
 ns=max(x[0] for x in pending)+1
 add('git',ns,{'repository':REPO,'head':primary['head'],'base':current['actual_target'],'clean':primary['clean'],
   'private_source':{'sha256':sha((RUN/'git-after-controls.private.json').read_bytes()),'scope':'post-run unchanged primary source and independently read current GitHub target'}})
 add('github',ns+1,{'head':current['headRefOid'],'base':current['actual_target'],'branch':current['headRefName'],'base_branch':current['baseRefName'],'url':current['url'],'merged':current['mergedAt'] is not None,'state':current['state'],
   'private_source':{'sha256':sha((RUN/'forge-after-controls.private.json').read_bytes()),'scope':'post-run actual target ref and independently read primary PR; no new admission'}})
inv=json.loads((RUN/'invocation.private.json').read_text());objective=inv['objective'];artifacts={}
for name,values in docs.items():
 b=(json.dumps(values,indent=2,sort_keys=True)+'\n').encode();(OUT/(name+'.json')).write_bytes(b)
 artifacts[name]={'file':name+'.json','source':name,'sha256':sha(b),'public_uri':None}
pending.sort();begin=pending[0][0]
capture={'schema':'decapod.agent-acceptance.v1','run_id':os.environ['DECAPOD_ACCEPTANCE_RUN_ID'],'owner_issue':1758,'repository':REPO,'objective':objective,'objective_revision':1,'approved_objective_sha256':sha(objective.encode()),'harness_version':'0.73.1','kernel_version':inv['kernel_version'],'kernel_sha256':inv['kernel_binary_sha256'],'kernel_source':inv['kernel_source'],'artifacts':artifacts,'events':[{'sequence':n+1,'elapsed_ms':(ns-begin)//1000000,'artifact':s,'pointer':f'/{i}'} for n,(ns,s,i) in enumerate(pending)]}
(OUT/'capture.json').write_text(json.dumps(capture,indent=2)+'\n')
print(json.dumps({'events':len(pending),'artifacts':{k:len(v) for k,v in docs.items()},'unique_tool_intervals':len(start),'output':str(OUT)}))
