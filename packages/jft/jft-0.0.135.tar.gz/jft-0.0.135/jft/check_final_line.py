from jft.text_colours.success import f as success
from jft.directory.list_testables import f as list_testables
from jft.file.load import f as load
from jft.text_colours.danger import f as danger
from jft.pf import f as pf
# check_final_line
def f(Pi=None):
  print('Checking final lines...', end='\r')
  Pi = list_testables() or Pi
  for pi in Pi:
    _lines = load(pi).split('\n')
    _last_line_index = len(_lines)-1
    _line = _lines[_last_line_index]
    if _line != '': return pf([
      f'{pi}:{_last_line_index}',
      danger([_line])
    ])
  print(f"{success('PASS')} Final lines "+' '*20)

def t(): return True # TODO: Fix this test
