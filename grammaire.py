import os
import sys
from utils.read_write import lire, ecrire
from utils.formes import greibach, chomsky

if __name__ == "__main__":
    
    filename = sys.argv[1]
    f_name, f_extension = os.path.splitext(filename)
    assert f_extension == '.general' , "L'extention doit etre .general"

    axiome, regles = lire(filename)
    #ecrire(axiome, regles, f_name+'.chomsky')

    new_axiome, new_regles = greibach(axiome, regles)
    ecrire(new_axiome, new_regles, f_name+'.greibach')

    #new_axiome, new_regles = chomsky(axiome, regles)
    #ecrire(new_axiome, new_regles, f_name+'.chomsky')

    print('Execution du grammaire.py est terminee')