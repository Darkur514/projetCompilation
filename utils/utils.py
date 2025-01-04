def est_non_terminal(X): ### redo voir est_terminal
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
    md = [] 
    for membres in regles.values():
      for membre in membres:
        for m in membre:
          if est_non_terminal(m):
            md.append(m)
    md = list(set(md))
    return md

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

def get_next_nt(axiome, regles):
    """Creation d'un nouveau non terminal pas encore utilise"""
    global nt_curr_letter
    global nt_curr_number
    global curr_nt
    if nt_curr_letter == 90 and nt_curr_number == 9: #Z = 90
      gc_nt(axiome, regles)
      if nt_curr_letter == 90 and nt_curr_number == 9: 
        raise Exception("La limit des non terminaux est atteinte")
    else:
        nt_curr_number = (nt_curr_number+1)%10
        if nt_curr_number == 0:
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

#todo memmbre droits identiques
def gc_nt(axiome, regles): 
    """
    supprimer les non terminaux s'ils
        1.ne sont pas accessibles depuis l'axiome
        2.ont les membre droits identiques

    renommer tous les non terminaux en commensant par A0
    """

    global nt_curr_letter
    global nt_curr_number

    nt_curr_letter = 65
    nt_curr_number = 0

    new_nt = get_next_nt()
    new_regles = {new_nt: []}

    nom_changes = {axiome: new_nt}
    to_threat = regles[axiome]
    x_to_threat = [[axiome, len(to_threat)]]
 
    for mds in to_threat:
        new_mds = []
        for md in mds:
            if est_non_terminal(md):
                if md not in nom_changes:
                    to_threat += regles[md]
                    x_to_threat.append([md, len(regles[md])])
                    nom_changes[md] = get_next_nt()
                new_mds.append(nom_changes[md])
            else:
                new_mds.append(md)

        new_regles[nom_changes[x_to_threat[0][0]]].append(new_mds)

        x_to_threat[0][1] -= 1
        if x_to_threat[0][1] == 0 and len(x_to_threat)>1:
          x_to_threat.pop(0)
          new_regles[nom_changes[x_to_threat[0][0]]] = []

        
    return(new_regles)

