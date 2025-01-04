from utils.utils import set_new_next_nt

############### Lecture ##########################
def lire_mg(md):
  """Ramene les membres droits a la bonne forme"""
  new_md = []
  i = 0
  while i<len(md):
    if ord(md[i]) in range(97, 122):
      new_md.append(md[i])
      i += 1
    elif md[i] == 'E':
      new_md.append('eps')
      i += 1
    else:
      new_md.append(md[i:i+2])
      i += 2
  return new_md


def lire(file_name):
  """
  Lecture des fichiers avec les grammaires.
  Les ramenes vers la forme convenable aux traitement
  """
  
  i = 0
  regles = {}
  with open(file_name, 'r') as f:
    line = f.readline()
    while line != '':
      line = line.split('\n')[0]
      md, mg = line.split(':')
      md, mg = md.strip(), mg.strip()

      if i == 0:
        axiome = md
        print(axiome, i)
        i = 1

      if md in regles:
        regles[md].append(lire_mg(mg))
      else:
        regles[md] = [lire_mg(mg)]

      line =f.readline()

  set_new_next_nt(regles)
  return axiome, regles


################ Ecriture ###############

def ecrire(axiome, regles, filename):
  with open(filename, 'w') as f:
    for md in regles[axiome]:
      f.write(f"{axiome} : {''.join(md)} \n")
    regles.pop(axiome)
    for mg, mds in regles.items():
      for md in mds:
        f.write(f"{mg} : {''.join(md)} \n")
  print('Ecriture finie')