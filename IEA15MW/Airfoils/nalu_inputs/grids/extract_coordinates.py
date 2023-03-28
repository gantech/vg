# coding: utf-8
from  turbine_perturb import TurbineData
import numpy as np
t = TurbineData("IEA-15-240-RWT.yaml")
for af in t.airfoil_labels:
    x,y = t.get_airfoil(af)
    np.savetxt('coordinates/'+af, np.c_[x,y], delimiter=' ')
