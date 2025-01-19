from utils.utils import set_new_next_nt

############### Lecture ##########################
def lire_membre_droit(membre_droit):
  """Ramene les membres droits a la bonne forme"""
  new_membre_droit = []
  i = 0
  while i<len(membre_droit):
    if ord(membre_droit[i]) in range(97, 122):
      new_membre_droit.append(membre_droit[i])
      i += 1
    elif membre_droit[i] == 'E':
      new_membre_droit.append('E')
      i += 1
    else:
      new_membre_droit.append(membre_droit[i:i+2])
      i += 2
  return new_membre_droit


def lire(file_name):
  """
  Lecture des fichiers avec les grammaires.
  Les ramenes vers la forme convenable au traitement
  """
  
  i = 0
  regles = {}
  with open(file_name, 'r') as f:
    line = f.readline()
    while line != '':
      line = line.split('\n')[0]
      membre_gauche, membre_droit = line.split(':')
      membre_gauche, membre_droit = membre_gauche.strip(), membre_droit.strip()

      if i == 0:
        axiome = membre_gauche
        print(axiome, i)
        i = 1

      if membre_gauche in regles:
        regles[membre_gauche].append(lire_membre_droit(membre_droit))
      else:
        regles[membre_gauche] = [lire_membre_droit(membre_droit)]

      line =f.readline()

  set_new_next_nt(regles)
  #print('aaa', regles)
  return axiome, regles


################ Ecriture ###############

def ecrire(axiome, regles, filename):
  with open(filename, 'w') as f:
    for membre_droit in regles[axiome]:
      f.write(f"{axiome} : {''.join(membre_droit)} \n")
    regles.pop(axiome)
    for membre_gauche, membre_droits in regles.items():
      for membre_droit in membre_droits:
        f.write(f"{membre_gauche} : {''.join(membre_droit)} \n")
  print('Ecriture finie')