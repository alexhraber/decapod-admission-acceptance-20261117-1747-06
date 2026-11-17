#!/usr/bin/env python3
"""Transparent CLI capture: identical argv, original stdout/stderr and exit code."""
import pathlib,subprocess,sys,os,time,json,re,uuid
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parent))
from capture_support import RUN,OWNER,sha,private_json,append
BINARY=RUN/'kernel/decapod'
args=sys.argv[1:];started=time.time_ns();identity=uuid.uuid4().hex
cwd=pathlib.Path.cwd()
r=subprocess.run([str(BINARY),*args],stdout=subprocess.PIPE,stderr=subprocess.PIPE)
ended=time.time_ns()
def parse(data):
    try:return json.loads(data)
    except (ValueError,UnicodeError):return None
raw=parse(r.stdout)
operation='other'
if '--help' not in args and '-h' not in args and args:
    if args[0] in ['docs','constitution','infer']:operation='context'
    if args[:2]==['todo','claim']:operation='claim'
    if args[:2]==['workspace','ensure']:operation='workspace'
    if args[0]=='validate':operation='validate'
    if args[:2]==['workspace','publish']:operation='publish'
    if args[0]=='rpc' and any(v in args for v in ['agent.init','context.resolve']):operation='context'
record={'schema':'decapod.native-invocation-capture.v1','owner_issue':OWNER,'id':identity,'started_ns':started,'ended_ns':ended,
    'argv':args,'cwd':str(cwd),'binary_sha256':sha(BINARY.read_bytes()),'exit_code':r.returncode,'operation':operation,
    'stdout_sha256':sha(r.stdout),'stderr_sha256':sha(r.stderr),'output':raw,
    'reason_codes':sorted(set(x for x in re.findall(r'\b[A-Z][A-Z0-9]+(?:_[A-Z0-9]+)+\b',(r.stdout+r.stderr).decode(errors='replace')) if not x.startswith('DECAPOD_')))}
if isinstance(raw,dict):
    readiness=raw.get('readiness',raw)
    path=readiness.get('evidence_path') if isinstance(readiness,dict) else None
    if isinstance(path,str):
        for name,file in [('plan','expected-plan.json'),('observations','observations.json'),('receipt','completion/native-readiness-receipt.json')]:
            p=pathlib.Path(path)/file
            if p.is_file() and not p.is_symlink() and p.stat().st_size<16*1024*1024:
                value=p.read_bytes();record[name]=parse(value);record[name+'_file_sha256']=sha(value)
private_json(RUN/'native'/('invocation-'+identity+'.json'),record)
(RUN/'native'/('invocation-'+identity+'.stdout.private')).write_bytes(r.stdout)
(RUN/'native'/('invocation-'+identity+'.stderr.private')).write_bytes(r.stderr)
sys.stdout.buffer.write(r.stdout);sys.stdout.buffer.flush()
sys.stderr.buffer.write(r.stderr);sys.stderr.buffer.flush()
sys.exit(r.returncode)
