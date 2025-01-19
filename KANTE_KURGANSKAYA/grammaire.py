import os
import sys
from copy import deepcopy
from utils.read_write import lire, ecrire
from utils.formes import greibach, chomsky
from utils.utils import set_new_next_nt, gc_nt
from utils.check_form import *

if __name__ == "__main__":
    
    filename = sys.argv[1]
    debug = False
    collect = False
    try: 
        debug = int(sys.argv[2]) 
        if debug: print('Debug mode on')
    except: pass
    try: 
        collect = int(sys.argv[3]) 
        if collect: print('Collect unused non terminals')
    except: pass

    f_name, f_extension = os.path.splitext(filename)
    assert f_extension == '.general' , "L'extention doit etre .general"

    axiome, regles = lire(filename)
    regles_c = deepcopy(regles)


    new_axiome, new_regles = greibach(axiome, regles, debug)
    if debug: verifier_Greibach(new_axiome, new_regles)
    if collect : new_axiome, new_regles = gc_nt(new_axiome, new_regles)
    ecrire(new_axiome, new_regles, f_name+'.greibach')
    
    set_new_next_nt(regles_c)
    new_axiome, new_regles = chomsky(axiome, regles_c, debug)
    if debug: verifier_Chomsky(new_axiome, new_regles)
    if collect : new_axiome, new_regles = gc_nt(new_axiome, new_regles)
    ecrire(new_axiome, new_regles, f_name+'.chomsky')
    

    print('Execution du grammaire.py est terminee')