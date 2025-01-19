from utils.utils import est_non_terminal, get_next_nt, get_all_term, get_curr_nt

######### regles supplementaires necessaires au changement de la forme #############
def elliminer_rec_gauche_immediate(axiome, regles):
  new_regles = {}
  for mg, mds in regles.items():
    #new_regles[mg] = []
    with_recursion = []
    without_recursion = []

    for md in mds:
      if md[0] == mg:
        with_recursion.append(md)
      else:
        without_recursion.append(md)
    
    if len(with_recursion) == 0:
      new_regles[mg] = mds
    else:
      new_regles[mg] = md
      new_mg = get_next_nt(axiome, regles)
      for i in range(len(without_recursion)):
        without_recursion[i].append(new_mg)
        print('bb', without_recursion)
      new_regles[mg] = without_recursion

      for i in range(len(with_recursion)):
        with_recursion[i].pop(0)
        with_recursion[i].append(new_mg)
      new_regles[new_mg] = with_recursion
  return axiome, new_regles
  

######### regles de changement de forme fondamentales #############


# 1. Supprime les règles 𝑋 → 𝜀 sauf si 𝑋 est l’axiome
def change_regles_with_eps(m_with_eps, regles):
  for mg, mds in regles.items():
    for md in mds:
      occurences = md.count(m_with_eps)
      if occurences > 0:
        m_eps_idx = [i for i, x in enumerate(md) if x == m_with_eps]
        num_subsets = 2 ** len(m_eps_idx)
        for i in range(num_subsets):
            for j in range(num_subsets):
                if (i & (2**j)) != 0:
                  if m_eps_idx[j]+1 <= len(md):
                    to_append = md[:m_eps_idx[j]]+md[m_eps_idx[j]+1:]
                  else:
                    to_append = md[:m_eps_idx[j]]
                  if len(to_append) == 0:
                    to_append = ['eps']
                  if to_append not in regles[mg]:
                    regles[mg].append(to_append)
  return regles

def supprimer_eps(axiome, regles):
  """Supprime les règles 𝑋 → 𝜀 sauf si 𝑋 est l’axiome """
  has_eps = True
  while has_eps:
    has_eps = False
    for mg, mds in regles.items():
      if mg != axiome:
        for md in mds:
          if len(md) == 1 and md[0] == 'eps':
            has_eps = True
            regles[mg].remove(['eps'])
            regles = change_regles_with_eps(mg, regles)

  return regles



# 2. Supprime les non-terminaux en tête des règles
def supp_nt_en_tete(regles):
  """Supprime les non-terminaux en tête des règles """
  has_nt_en_tete = True
  while has_nt_en_tete:
    has_nt_en_tete = False
    for mg, mds in regles.items():
      for md in mds:
        if est_non_terminal(md[0]):
          has_nt_en_tete = True
          nt = md[0]
          suite = md[1:]
          regles[mg].remove(md)
          for membre in regles[nt]:
            if membre+suite not in regles[mg]:
              regles[mg].append(membre+suite)
  return regles




# 3. Supprimer les terminaux dans le membre droit des règles de longueur au moins deux

def t_to_nt(axiome, regles): #terminaux2NonTerminaux
  t_dict = {}
  for mg, mds in regles.items():
    for md in mds:
      for m in md:
        if not est_non_terminal(m) and m not in t_dict:
          t_dict[m] = [get_next_nt(axiome, regles), False]
  return t_dict

def add_new_nt(regles, t_dict):
  for key, value in t_dict.items():
    if value[1] == True:
      regles[value[0]] = [[key]]
  return regles

def supp_term_mb2(axiome, regles):
  """
  Supprime les terminaux dans le membre droit 
  des règles de longueur au moins deux
  """
  t_dict = t_to_nt(axiome, regles)

  for mg, mds in regles.items():
      for i in range(len(mds)):
        if len(mds[i])>1:
          for j in range(len(mds[i])):
            if mds[i][j] in t_dict:
              terminal = mds[i][j]
              regles[mg][i][j] = t_dict[terminal][0]
              t_dict[terminal][1] = True
  add_new_nt(regles, t_dict)
  return regles


#4. supprimer les règles avec plus de deux non-terminaux
def supp_2nt(axiome, regles):
  """Supprime les règles avec plus de deux non-terminaux"""
  new_regles = {}

  for mg, mds in regles.items():
      for i in range(len(mds)):
        if len(mds[i])>2: #on applique cette fontion apres supp_term_mb2 donc on est sure que len(md)>2 => md a plus de 2 nt
          md = mds[i]

          for j in range(len(md)-1):
            if j == 0:
              regles[mg][i] = [md[j], get_next_nt(axiome, regles)]
            elif j == len(md)-2:
              new_regles[get_curr_nt()] = [[md[j], md[j+1]]]
            else:
              nt_key = get_curr_nt()
              nt_value = get_next_nt(axiome, regles)
              new_regles[nt_key] = [[md[j], nt_value]]


  regles.update(new_regles)
  return regles



# 5. retirer l’axiome des membres droits des règles

def retirer_axiome(axiome, regles):
    nv_axiome = get_next_nt(axiome, regles)
    nv_regles = {axiome: [[nv_axiome]]}

    for non_terminal, membres_droit in regles.items():
        nv_membres_droit = []
        for i in membres_droit:
            nv_prods = []
            for j in i:
                if j == axiome:
                    nv_prods.append(nv_axiome)
                else:
                    nv_prods.append(j)
            nv_membres_droit.append(nv_prods)

        if non_terminal == axiome:
            nv_regles[nv_axiome] = nv_membres_droit
        else:
            nv_regles[non_terminal] = nv_membres_droit

    return nv_axiome, nv_regles

# 6. supprimer les règles unité 𝑋 → 𝑌 ;

def supp_regles_unite(regles):
    """Supprime les règles unité 𝑋 → 𝑌"""
    nv_regles = {}

    for gauche in regles:
        nv_regles[gauche] = []

    for gauche, droit in regles.items():
        a_traiter = droit
        while a_traiter:
            regle = a_traiter.pop(0)
            if len(regle) == 1 and est_non_terminal(regle[0]):
                a_traiter.extend(regles[regle[0]])
            else:
                if regle not in nv_regles[gauche]:
                    nv_regles[gauche].append(regle)

    return nv_regles


# 7. supprimer les symboles terminaux qui ne sont pas en tête des règles
def ajout_regle(regles, nterm, prod) :
  if nterm in regles:
    regles[nterm].append(prod)
  else :
    regles[nterm] = [[prod]]
  return regles

def supp_symb_term(axiome, regles) :
  """Supprime les symboles terminaux qui ne sont pas en tête des règles"""
  term_pris = get_all_term(regles)
  term = []
  non_term = []
  for gauche, droite in regles.items() :
        for i in droite :
          for j in range(1, len(i)) :
            if i[j] in term_pris :
              term.append(i[j])
              i.pop(j)
              k = get_next_nt(axiome, regles)
              i.insert(j, k)
              non_term.append(k)

  for i in range(len(term)):
     ajout_regle(regles, non_term[i], term[i])
  return regles

################# Formes normaux ##########################
def greibach(axiome, regles, debug):
  """
  Retourne la grammaire sous la forme de Greibach.
  Applique:
    1. retirer l’axiome des membres droits des règles ;
    2. supprimer les règles 𝑋 → 𝜀 sauf si 𝑋 est l’axiome ;
    3. supprimer les règles unité 𝑋 → 𝑌 ;
    4. supprimer les non-terminaux en tête des règles ;
    5. supprimer les symboles terminaux qui ne sont pas en tête des règles.

  """
  #+ delete recursion gauche
  if debug: print(regles)
  elliminer_rec_gauche_immediate(axiome, regles)
  if debug: print('0', regles)
  axiome, regles = retirer_axiome(axiome, regles)
  if debug: print('1', regles)
  regles = supprimer_eps(axiome, regles)
  if debug: print('2', regles)
  regles = supp_regles_unite(regles)
  if debug: print('3', regles)
  regles = supp_nt_en_tete(regles)
  if debug: print('4', regles)
  regles = supp_symb_term(axiome, regles)
  if debug: print('5', regles)

  return axiome, regles

def chomsky(axiome, regles, debug):
  """
  Retourne la grammaire sous la forme de Chomsky.
  Applique:
  1. retirer l’axiome des membres droits des règles ;
  2. supprimer les terminaux dans le membre droit des règles de longueur au moins deux ;
  3. supprimer les règles avec plus de deux non-terminaux ;
  4. supprimer les règles 𝑋 → 𝜀 sauf si 𝑋 est l’axiome ;
  5. supprimer les règles unité 𝑋 → �
  """
  if debug: print(regles)
  elliminer_rec_gauche_immediate(axiome, regles)
  if debug: print('0', regles)
  axiome, regles = retirer_axiome(axiome, regles)
  if debug: print('1', regles)
  regles = supp_term_mb2(axiome, regles)
  if debug: print('2', regles)
  regles = supp_2nt(axiome, regles)
  if debug: print('3', regles)
  regles = supprimer_eps(axiome, regles)
  if debug: print('4', regles)
  regles = supp_regles_unite(regles)
  if debug: print('5', regles)

  return axiome, regles



############ Creation de mots #########################

def print_mots_tries(mots):
  for i in range(len(mots)):
    mots[i]  = ''.join(mots[i])
  mots = list(set(mots))
  mots.sort()
  for mot in mots:
    print(mot)

def tous_mots(len_mot, axiome, regles):
  mots_possibles = []
  mots_retenus = []
  for md in regles[axiome]:
    if len(md) <= len_mot:
      mots_possibles.append(md)

  has_nt = True
  while has_nt:
    #print('aaaa')
    has_nt = False
    for i in range(len(mots_possibles)):
      j = 0
      while j < len(mots_possibles[i]):
        if est_non_terminal(mots_possibles[i][j]):
          has_nt = True
          for md in regles[mots_possibles[i][j]]:
            if len(mots_possibles[i]) + len(md) <= len_mot:
              nouveau_mot = mots_possibles[i][:j] + md + mots_possibles[i][(j+1):]
              mots_retenus.append(nouveau_mot)
        j += 1
   
    if mots_retenus != []:
      print(type(mots_retenus))
      mots_possibles = mots_retenus
    #print(mots_possibles, has_nt)
    mots_retenus = []
  #print( regles, mots_retenus, has_nt)
  print(mots_possibles)
  return mots_possibles