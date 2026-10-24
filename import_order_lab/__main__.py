import argparse
import json
from pathlib import Path
import sys
from .core import run
from .metadata import DESCRIPTION

ERROR={'fr':'Entrée invalide : vérifier les champs et les limites documentés.','en':'Invalid input: check documented fields and bounds.','es':'Entrada no válida: compruebe los campos y límites documentados.'}
class Parser(argparse.ArgumentParser):
    def error(self,message):raise ValueError('arguments')
def reject_constant(value):raise ValueError('nonfinite_json')
def unique_object(pairs):
    out={}
    for key,value in pairs:
        if key in out:raise ValueError('duplicate_json_key')
        out[key]=value
    return out
def main():
    lang='en'
    for i,arg in enumerate(sys.argv[:-1]):
        if arg=='--lang' and sys.argv[i+1] in ERROR:lang=sys.argv[i+1]
    try:
        parser=Parser(add_help=False)
        parser.add_argument('input',nargs='?');parser.add_argument('--lang',default='en')
        args,unknown=parser.parse_known_args()
        if unknown or not args.input or args.lang not in ERROR:raise ValueError('arguments')
        lang=args.lang
        with Path(args.input).open('rb') as stream: raw=stream.read(8*1024*1024+1)
        if len(raw)>8*1024*1024:raise ValueError('input_size')
        data=json.loads(raw,parse_constant=reject_constant,object_pairs_hook=unique_object)
        if not isinstance(data,dict):raise ValueError('object_required')
        if 'assets_root' in data:data['assets_root']=str((Path(args.input).absolute().parent/Path(data['assets_root'])).resolve())
        result=run(data)
        print(json.dumps({'language':lang,'summary':DESCRIPTION[lang],'result':result},ensure_ascii=False,allow_nan=False,sort_keys=True))
    except (ValueError,KeyError,TypeError,OSError,OverflowError,ZeroDivisionError,AttributeError):
        print(json.dumps({'code':'invalid_input','message':ERROR[lang]},ensure_ascii=False),file=sys.stderr)
        return 2
    return 0
if __name__=='__main__':sys.exit(main())
