"""Read-only, private host observation carrier. It never returns tool overrides."""
import pathlib,subprocess,json,hashlib,time,os
RUN=pathlib.Path(os.environ['DECAPOD_ACCEPTANCE_RUN']).resolve()
REPO=pathlib.Path(os.environ['DECAPOD_ACCEPTANCE_REPO']).resolve()
OWNER='https://github.com/DecapodLabs/decapod/issues/1758'
def sha(b):return 'sha256:'+hashlib.sha256(b).hexdigest()
def private_json(path,value):
    fd=os.open(path,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
    with os.fdopen(fd,'w') as f:json.dump(value,f,sort_keys=True)
def append(path,value):
    fd=os.open(path,os.O_WRONLY|os.O_APPEND|os.O_CREAT,0o600)
    with os.fdopen(fd,'w') as f:f.write(json.dumps(value,sort_keys=True)+'\n')
def snapshot():
    reads=[]
    def git(path,*args):
        r=subprocess.run(['/usr/bin/git','-c','core.fsmonitor=false','-C',str(path),*args],capture_output=True,timeout=10)
        reads.append({'args':list(args),'exit_code':r.returncode,'stdout_sha256':sha(r.stdout)})
        return r.stdout.decode(errors='replace').strip() if r.returncode==0 else None
    result={'owner_issue':OWNER,'time_ns':time.time_ns(),'consistency':'bounded non-atomic tool-boundary sample','refs':git(REPO,'for-each-ref','--format=%(refname) %(objectname)'),'worktrees':[]}
    base=git(REPO,'rev-parse','refs/remotes/origin/'+os.environ['DECAPOD_ACCEPTANCE_BASE'])
    for line in (git(REPO,'worktree','list','--porcelain') or '').splitlines():
        if not line.startswith('worktree '):continue
        root=pathlib.Path(line[9:]);untracked={}
        for name in (git(root,'ls-files','--others','--exclude-standard') or '').splitlines():
            p=root/name
            if p.is_symlink():untracked[name]='symlink'
            elif p.is_file() and p.stat().st_size<=1024*1024:untracked[name]=sha(p.read_bytes())
            else:untracked[name]='unmeasured'
        diff=git(root,'diff','--binary','--no-ext-diff','--no-textconv','HEAD') or ''
        result['worktrees'].append({'path':str(root),'id':sha(str(root).encode()),'head':git(root,'rev-parse','HEAD'),
            'branch':git(root,'symbolic-ref','--short','HEAD'),'base':base,'clean':git(root,'status','--porcelain')=='',
            'material_sha256':sha(json.dumps({'diff':diff,'untracked':untracked},sort_keys=True).encode())})
    result['git_reads']=reads
    return result
if __name__=='__main__':
    import sys
    record=json.load(sys.stdin)
    record.update(owner_issue=OWNER,time_ns=time.time_ns())
    try:record['git']=snapshot()
    except Exception as error:record['capture_error']=type(error).__name__
    append(RUN/'host-boundaries.private.jsonl',record)
