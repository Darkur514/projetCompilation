import sys
import os
from utils.formes import tous_mots, print_mots_tries
from utils.read_write import lire

if __name__ == "__main__":
    
    len_mots = int(sys.argv[1])
    filename = sys.argv[2]

    f_name, f_extension = os.path.splitext(filename)
    assert f_extension in ['.chomsky', '.greibach'] , "La grammaire doit etre soit la forme normale"

    axiome, regles = lire(filename)

    mots = tous_mots(len_mots, axiome, regles)
    print_mots_tries(mots)