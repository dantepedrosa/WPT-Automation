import femm
import os

dir_path = os.path.dirname(os.path.realpath(__file__))
femm.openfemm()
femm.opendocument(dir_path + '\\Untitled.FEM')


for j in range(1, 26):
    
    femm.mi_addmaterial(('Copper Wire '+ str(j/10)) , 1, 1, 0, 0, 58, 0, 0, 1, 3, 0, 0, 1, j/10)
    femm.mi_selectlabel(-3.4, 0)
    femm.mi_setblockprop(('Copper Wire '+ str(j/10)), 1, 0, 'Primary', 0, 0, 2)
    femm.mi_clearselected()
    