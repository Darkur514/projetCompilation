from utils.utils import est_non_terminal

#!!!!!!!!!!! check

def verifier_Greibach(axiome, regles):
  """
  — X → aA1A2...An avec n ≥ 1
  — X → a
  — S → ε seulement si ε appartient au langage.
  """
  for md, mgs in regles.items():
    for mg in mgs:
      for i in range(mg):
        if mg[i] == 'eps' and md != axiome:
            raise Exception("epsilon que dans l'axiome")
        if i == 0 and est_non_terminal(mg[i]):
          raise Exception("premier symbol doit etre terminal")
        if i != 0 and not est_non_terminal(mg[i]):
          raise Exception("le symbole doit etre non terminal")
        

def verifier_Chomsky(axiome, regles):
  """
  — X → Y Z
  — X → a
  — S → ε seulement si ε appartient au langage.
  """
  for md, mgs in regles.items():
    for mg in mgs:
        if mg[0] == 'eps' and md != axiome:
           raise Exception("epsilon que dans l'axiome")
        if not est_non_terminal(mg[0]) and len(mg)>1:
          raise Exception("len regles avec les terminaux doit etre egale a 1")
        if len(mg) > 2:
          raise Exception("len maximal d'une regle doit etre 2 ")
        if len(mg) == 2 and not est_non_terminal(mg[0]) or est_non_terminal(mg[1]):
          raise Exception("toutes les regles de len 2 doit etre composee de nt")