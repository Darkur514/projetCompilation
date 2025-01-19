def est_non_terminal(X): 
    """Renvoie True si X est non terminal False sinon"""
    if len(X) == 2 and ord(X[0]) in range(65, 91) and ord(X[1]) in range(48, 58): #epsilon = 'eps'
        return True
    return False

def get_all_term(regles):
    terminaux = []
    for mb_droits in regles.values():
        for i in mb_droits:
            for symb in i:
                if not est_non_terminal(symb) and symb not in terminaux:
                    terminaux.append(symb)
    return terminaux

################### Gestion et affichage des membres ######################

def get_all_memebres_droits_nt(regles):
    membre_droit = [] 
    for membres in regles.values():
      for membre in membres:
        for m in membre:
          if est_non_terminal(m):
            membre_droit.append(m)
    membre_droit = list(set(membre_droit))
    return membre_droit

def get_all_memebres_gauches_nt(regles):
    return list(regles.keys())

def get_all_nt(regles):
  """Renvoies tous les non terminaux utilses"""
  nt = get_all_memebres_droits_nt(regles)
  nt += get_all_memebres_gauches_nt(regles)
  return list(set(nt))

#################### Creation de nouveaux non terminaux #################################

nt_curr_letter = 65
nt_curr_number = 0
curr_nt = 'A0'

class LimitException(Exception):
    def __init__(self):
        self.message = 'La limit des non terminaux est atteinte'

    def __str__(self):
        return self.message
  

def get_next_nt():
    """Creation d'un nouveau non terminal pas encore utilise"""
    global nt_curr_letter
    global nt_curr_number
    global curr_nt
    if nt_curr_letter == 90 and nt_curr_number == 9: #Z = 90
      raise LimitException()
    
    nt_curr_number = (nt_curr_number+1)%10
    if nt_curr_number == 0:
        nt_curr_letter += 1
        if nt_curr_letter == 69: #E
           nt_curr_letter += 1
    next_nt =  chr(nt_curr_letter) + str(nt_curr_number)
    curr_nt = next_nt
    return next_nt

def get_curr_nt():
  """Renvoie le nom du dernier non terminal cree"""
  global curr_nt
  return curr_nt

def set_new_next_nt(regles):
  """
  Effectue le update du dernier non ternimal utilise 
  apres la lecture du fichier contenant la grammaire
  afin de pouvoir affecter de bons noms aux nouveaux non terminaux
  """
  global nt_curr_letter
  global nt_curr_number

  max_letter = 'A'
  max_number = 0
  all_nt = get_all_nt(regles)
  for nt in all_nt:
    if nt[0] > max_letter:
      max_letter = nt[0]
    if int(nt[1]) > max_number:
      max_number = int(nt[1]) 
  max_letter = ord(max_letter)
  nt_curr_letter = max_letter
  nt_curr_number = max_number


#################### Collecte des non terminaux non utilises ################


def gc_nt(axiome, regles): 
    """
    supprimer les non terminaux s'ils
        1.ne sont pas accessibles depuis l'axiome
        2.ont les membre droits identiques

    renommer tous les non terminaux en commensant par A0
    """

    global nt_curr_letter
    global nt_curr_number

    nt_curr_letter = 64
    nt_curr_number = -1


    new_regles = {}
    old_regles = {}
    for mg, mds in regles.items():
       if mds not in new_regles.values():
        new_regles[mg] = mds
       else:
        old_regles[mg] = list(new_regles.keys())[list(new_regles.values()).index(mds)]
    regles = new_regles

    for mg, mds in regles.items():
      for i in range(len(mds)):
         for j in range(len(mds[i])):
            if mds[i][j] in old_regles:
               regles[mg][i][j] = old_regles[mds[i][j]]


    new_nt = get_next_nt()
    new_regles = {new_nt: []}

    nom_changes = {axiome: new_nt}
    to_threat = regles[axiome]
    x_to_threat = [[axiome, len(to_threat)]]
 
    for membre_droits in to_threat:
        new_membre_droits = []
        for membre_droit in membre_droits:
            
            if est_non_terminal(membre_droit):
                if membre_droit not in nom_changes:
                    to_threat += regles[membre_droit]
                    x_to_threat.append([membre_droit, len(regles[membre_droit])])
                    nom_changes[membre_droit] = get_next_nt()
                new_membre_droits.append(nom_changes[membre_droit])
            else:
                new_membre_droits.append(membre_droit)

        new_regles[nom_changes[x_to_threat[0][0]]].append(new_membre_droits)

        x_to_threat[0][1] -= 1
        if x_to_threat[0][1] == 0 and len(x_to_threat)>1:
          x_to_threat.pop(0)
          new_regles[nom_changes[x_to_threat[0][0]]] = []

    return new_nt, new_regles

