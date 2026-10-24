import tempfile,subprocess,sys,os,itertools,json,re,hashlib
from pathlib import Path

def module(x):
 if not isinstance(x,str)or not re.fullmatch(r'[A-Za-z_]\w*(?:\.[A-Za-z_]\w*)*',x):raise ValueError('module')
 return x
def run(data):
 modules=data['modules'];target=module(data['target']);root=Path(data['assets_root']).resolve();wheels=data['wheels']
 if not isinstance(modules,list)or not 1<=len(modules)<=4 or len(modules)!=len(set(modules))or not isinstance(wheels,list)or not 1<=len(wheels)<=5:raise ValueError('bounds')
 for x in modules:module(x)
 paths=[]
 for wheel in wheels:
  p=(root/wheel['file']).resolve()
  if not p.is_relative_to(root)or p.suffix!='.whl'or p.stat().st_size>5_000_000 or hashlib.sha256(p.read_bytes()).hexdigest()!=wheel['sha256']:raise ValueError('wheel_receipt')
  paths.append(str(p))
 with tempfile.TemporaryDirectory(prefix='owned-import-order-')as tmp:
  home=Path(tmp);venv=home/'venv';env={k:os.environ[k]for k in ('PATH','SYSTEMROOT','WINDIR','LANG')if k in os.environ};env.update(HOME=tmp,TMPDIR=tmp,PIP_CONFIG_FILE=os.devnull,PIP_DISABLE_PIP_VERSION_CHECK='1',PIP_NO_INDEX='1',PYTHONHASHSEED='0')
  completed=subprocess.run([sys.executable,'-I','-m','venv',str(venv)],capture_output=True,env=env,timeout=60)
  if completed.returncode:raise ValueError('venv')
  executable=venv/('Scripts/python.exe'if os.name=='nt'else'bin/python');installed=subprocess.run([str(executable),'-I','-m','pip','install','--no-index','--no-deps',*paths],capture_output=True,env=env,timeout=60)
  if installed.returncode:raise ValueError('trusted_wheel_install')
  code='import importlib,runpy,json,sys;[importlib.import_module(name)for name in json.loads(sys.argv[1])];runpy.run_module(sys.argv[2],run_name="__main__")';runs=[]
  for order in itertools.permutations(modules):
   try:
    process=subprocess.run([str(executable),'-I','-c',code,json.dumps(order),target],cwd=tmp,env=env,capture_output=True,timeout=15);status='completed';stdout=process.stdout;stderr=process.stderr;exit_code=process.returncode
   except subprocess.TimeoutExpired:status='timed_out';stdout=b'';stderr=b'';exit_code=None
   runs.append({'order':list(order),'status':status,'exit_code':exit_code,'stdout_sha256':hashlib.sha256(stdout).hexdigest(),'stderr_sha256':hashlib.sha256(stderr).hexdigest()})
  signatures={(r['status'],r['exit_code'],r['stdout_sha256'],r['stderr_sha256'])for r in runs}
 return {'runs':runs,'distinct_outcome_signatures':len(signatures),'order_sensitive':len(signatures)>1,'model':'actual_trusted_local_wheels_fresh_venv_fresh_process_per_import_permutation_not_security_sandbox'}
