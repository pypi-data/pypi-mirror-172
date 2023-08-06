from jft.text_colours.success import f as success
from jft.directory.list_testables import f as list_testables
from jft.file.load import f as load
from jft.pf import f as pf
from jft.text_colours.danger import f as danger
# check_line_lengths
def f(Pi=None):
  print('Checking line lengths...', end='\r')
  Pi = list_testables() or Pi
  for pi in Pi:
    ignore_line_lengths = False
    for line_index, line in enumerate(load(pi).split('\n')):
      if 'ignore_overlength_lines' in line: ignore_line_lengths = True
      if len(line) > 80 and not ignore_line_lengths: return pf([
        f'{pi}:{line_index+1}',
        danger(line)
      ])
  print(f"{success('PASS')} Line Lengths "+' '*20)

def t(): return True # TODO: Fix this test
