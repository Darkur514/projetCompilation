import os
import sys
from copy import deepcopy
from utils.read_write import lire, ecrire
from utils.formes import greibach, chomsky
from utils.utils import set_new_next_nt
from utils.check_form import *

if __name__ == "__main__":
    
    filename = sys.argv[1]
    debug = False
    try: 
        debug = int(sys.argv[2])
        if debug: print('Debug mode on')
    except: pass

    f_name, f_extension = os.path.splitext(filename)
    assert f_extension == '.general' , "L'extention doit etre .general"

    axiome, regles = lire(filename)
    regles_c = deepcopy(regles)


    new_axiome, new_regles = greibach(axiome, regles)
    ecrire(new_axiome, new_regles, f_name+'.greibach')
    if debug: verifier_Greibach(axiome, regles)

    set_new_next_nt(regles_c)
    new_axiome, new_regles = chomsky(axiome, regles_c)
    ecrire(new_axiome, new_regles, f_name+'.chomsky')
    if debug: verifier_Chomsky(axiome, regles)

    print('Execution du grammaire.py est terminee')