"""One bounded real Pi invocation. No semantic steering or controller repair."""
import pathlib,subprocess,os,json,time,selectors,signal,hashlib,shutil,sys
from capture_support import RUN,REPO,OWNER,sha,private_json,append,snapshot
OBJECTIVE=os.environ.get('DECAPOD_ACCEPTANCE_OBJECTIVE','Implement the repository-scoped read authorization described in README.md and publish a verified pull request.')
PI=os.environ['DECAPOD_ACCEPTANCE_PI']
TOOLS=pathlib.Path(__file__).resolve().parent
RUN.mkdir(mode=0o700,exist_ok=False)
os.umask(0o077)
for name in ['bin','kernel','native']:(RUN/name).mkdir(mode=0o700)
shutil.copyfile(os.environ['DECAPOD_ACCEPTANCE_KERNEL'],RUN/'kernel/decapod')
(RUN/'kernel/decapod').chmod(0o555)
shim=RUN/'bin/decapod'
shim.write_text('#!'+sys.executable+'\nimport runpy;runpy.run_path('+repr(str(TOOLS/'decapod-carrier.py'))+",run_name='__main__')\n")
shim.chmod(0o700)

observed_pi_version=subprocess.check_output([PI,'--version'],text=True,timeout=30).strip()
assert observed_pi_version=='0.73.1', 'review the new Pi version before an acceptance run'
capabilities=subprocess.check_output([str(RUN/'kernel/decapod'),'capabilities'],text=True,timeout=60)
kernel_version=capabilities.splitlines()[0].removeprefix('Decapod ').strip()
assert kernel_version==os.environ['DECAPOD_ACCEPTANCE_KERNEL_VERSION'], 'kernel version differs from the reviewed pin'
env=os.environ.copy()
env.update(PI_TELEMETRY='0',PI_OFFLINE='1',DECAPOD_AGENT_ID=os.environ['DECAPOD_ACCEPTANCE_AGENT'],DECAPOD_CLAIM_AUTORUN='0',DECAPOD_ACCEPTANCE_PYTHON=sys.executable,DECAPOD_ACCEPTANCE_SNAPSHOT_HELPER=str(TOOLS/'capture_support.py'))
env['PATH']=str(RUN/'bin')+os.pathsep+env['PATH']
argv=[PI,'--mode','json','--print','--provider',os.environ['DECAPOD_ACCEPTANCE_PROVIDER'],'--model',os.environ['DECAPOD_ACCEPTANCE_MODEL'],'--thinking','medium','--no-session','--no-extensions','--extension',str(TOOLS/'capture.ts'),'--no-skills','--no-prompt-templates',OBJECTIVE]
limits={'wall_seconds':3600,'tool_calls':120,'observed_total_tokens':2000000,'observed_uncached_tokens':200000,'token_threshold_granularity':'completed provider response; any overshoot is recorded'}
private_json(RUN/'invocation.private.json',{'schema':'decapod.real-pi-invocation.v1','owner_issue':OWNER,'objective':OBJECTIVE,'objective_revision':1,
    'argv':argv,'limits':limits,'kernel_version':kernel_version,'kernel_source':os.environ['DECAPOD_ACCEPTANCE_KERNEL_SOURCE'],'kernel_binary_sha256':sha((RUN/'kernel/decapod').read_bytes()),'harness_version':observed_pi_version,'provider':os.environ['DECAPOD_ACCEPTANCE_PROVIDER'],'model':os.environ['DECAPOD_ACCEPTANCE_MODEL'],'initial_git':snapshot(),
    'adapter_digests':{n:sha((TOOLS/n).read_bytes()) for n in ['capture_support.py','capture.ts','decapod-carrier.py','run_pi.py']},'human_interventions_after_objective':0})
started=time.monotonic();tools=0;tokens=0;uncached=0;turns=0;reason=None;stopped_at=None
stderr=open(RUN/'pi.stderr.private','xb')
p=subprocess.Popen(argv,cwd=REPO,env=env,stdout=subprocess.PIPE,stderr=stderr,start_new_session=True)
selector=selectors.DefaultSelector();selector.register(p.stdout,selectors.EVENT_READ);buffer=b''
raw=open(RUN/'pi.raw.private.jsonl','xb')
def stop(why):
    global reason,stopped_at
    if stopped_at is None:
        reason=why;stopped_at=time.monotonic()
        try:os.killpg(p.pid,signal.SIGTERM)
        except ProcessLookupError:pass
while p.poll() is None or selector.get_map():
    if time.monotonic()-started>limits['wall_seconds'] or tools>=limits['tool_calls'] or tokens>=limits['observed_total_tokens'] or uncached>=limits['observed_uncached_tokens']:
        stop('experiment_budget_exhausted')
    if stopped_at is not None and time.monotonic()-stopped_at>15:
        try:os.killpg(p.pid,signal.SIGKILL)
        except ProcessLookupError:pass
    events=selector.select(timeout=1)
    if not events:
        continue
    for key,_ in events:
        chunk=os.read(key.fd,65536)
        if not chunk:selector.unregister(key.fileobj);continue
        buffer+=chunk
        if len(buffer)>16*1024*1024:stop('protocol_record_bound_exceeded')
        while b'\n' in buffer:
            line,buffer=buffer.split(b'\n',1);raw.write(line+b'\n');raw.flush()
            try:event=json.loads(line)
            except ValueError:stop('invalid_pi_json_record');continue
            append(RUN/'pi.received.private.jsonl',{'received_ns':time.time_ns(),'event':event})
            if event.get('type')=='tool_execution_start':tools+=1
            if event.get('type')=='message_end' and event.get('message',{}).get('role')=='assistant':
                usage=event['message'].get('usage',{})
                turns+=1;tokens+=usage.get('totalTokens',0);uncached+=sum(usage.get(k,0) for k in ['input','output','cacheWrite'])
                print(json.dumps({'turn':turns,'tool_calls':tools,'observed_tokens':tokens,'observed_uncached_tokens':uncached,'stop_reason':event['message'].get('stopReason')}),flush=True)
raw.close();stderr.close();code=p.wait(timeout=15)
private_json(RUN/'process-result.private.json',{'exit_code':code,'stop_reason':reason,'elapsed_seconds':round(time.monotonic()-started,3),'tool_calls':tools,'assistant_messages':turns,'observed_tokens':tokens,'observed_uncached_tokens':uncached,'final_git':snapshot()})
print(json.dumps({'exit_code':code,'stop_reason':reason,'tool_calls':tools,'observed_tokens':tokens}),flush=True)
