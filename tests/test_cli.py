import json,subprocess,sys,tempfile,unittest
from pathlib import Path
class InterfaceTests(unittest.TestCase):
 def test_three_languages(self):
  for lang in ('fr','en','es'):
   r=subprocess.run([sys.executable,'-m','import_order_lab','examples/demo.json','--lang',lang],capture_output=True,text=True)
   self.assertEqual(r.returncode,0,r.stderr); d=json.loads(r.stdout);self.assertEqual(d['language'],lang);self.assertTrue(d['summary'])
 def test_invalid_input_localized(self):
  with tempfile.TemporaryDirectory() as tmp:
   p=Path(tmp)/'bad.json';p.write_text('{"x":NaN}')
   messages=[]
   for lang in ('fr','en','es'):
    r=subprocess.run([sys.executable,'-m','import_order_lab',str(p),'--lang',lang],capture_output=True,text=True)
    self.assertEqual(r.returncode,2);self.assertEqual(r.stdout,'');d=json.loads(r.stderr);self.assertEqual(d['code'],'invalid_input');messages.append(d['message'])
   self.assertEqual(len(set(messages)),3)

 def test_missing_language_value_is_structured(self):
  r=subprocess.run([sys.executable,'-m','import_order_lab','examples/demo.json','--lang'],capture_output=True,text=True)
  self.assertEqual(r.returncode,2);self.assertEqual(json.loads(r.stderr)['code'],'invalid_input')
 def test_duplicate_json_keys_rejected(self):
  with tempfile.TemporaryDirectory() as tmp:
   path=Path(tmp)/'duplicate.json';path.write_text('{"x":1,"x":2}')
   r=subprocess.run([sys.executable,'-m','import_order_lab',str(path)],capture_output=True,text=True)
   self.assertEqual(r.returncode,2);self.assertEqual(json.loads(r.stderr)['code'],'invalid_input')
