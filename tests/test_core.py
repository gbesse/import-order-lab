import unittest,json,tempfile
from pathlib import Path
from import_order_lab import run
class Tests(unittest.TestCase):
 def data(self):
  d=json.loads(Path('examples/demo.json').read_text());d['assets_root']=str(Path('examples/fixtures').resolve());return d
 def test_actual_installed_wheel_produces_import_order_counterexample(self):
  r=run(self.data());self.assertTrue(r['order_sensitive']);self.assertEqual({x['exit_code']for x in r['runs']},{0,1});self.assertTrue(all(x['status']=='completed'for x in r['runs']))
 def test_wrong_hash_refused_before_execution(self):
  d=self.data();d['wheels'][0]['sha256']='0'*64
  with self.assertRaises(ValueError):run(d)
 def test_module_injection_and_fixture_escape_rejected(self):
  d=self.data();d['modules']=['os; print(1)']
  with self.assertRaises(ValueError):run(d)
  d=self.data();d['wheels'][0]['file']='../../elsewhere.whl'
  with self.assertRaises(ValueError):run(d)
