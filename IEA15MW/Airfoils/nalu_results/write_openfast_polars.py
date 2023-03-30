from turbine_perturb import TurbineData
from scipy.interpolate import PchipInterpolator
import numpy as np
import sys
sys.path.append('../utilities')
from airfoil import *
from wisdem.airfoilprep import Polar
from pathlib import Path


nalu_polars = AirfoilTableDB('static/airfoils_rey10000000.yaml')

#Get the thickness profile along the blade first
t = TurbineData("../yaml_data/IEA-15-240-RWT.yaml")
tbyc = np.array( [ np.minimum(1.0, t.get_tbycmax(t.create_af_cst(af)[:-2])) for af in t.airfoil_labels] )
tbyc_interp = PchipInterpolator( t.airfoil_grid, tbyc)

of_ad15_blade = np.loadtxt('../../OpenFAST_NaluPolars/IEA-15-240-RWT/IEA-15-240-RWT_AeroDyn15_blade.dat',skiprows=6)
of_ad15_blade[:,0] = of_ad15_blade[:,0]/of_ad15_blade[-1,0]

Path('../../OpenFAST_NaluPolars/Unchanged_Airfoils').mkdir(exist_ok=True)
for i,s in enumerate(of_ad15_blade[:,0]):
    ui = np.argmin( tbyc > tbyc_interp(s)) #Upper station index
    li = ui-1 #Lower station index
    interp_fac = (tbyc_interp(s) - tbyc[ui])/(tbyc[li] - tbyc[ui])

    ui_afp = nalu_polars.get_airfoil_data(t.airfoil_labels[ui])
    li_afp = nalu_polars.get_airfoil_data(t.airfoil_labels[li])

    interp_afp = li_afp * interp_fac + ui_afp * (1.0 - interp_fac)
    
    #Extrapolate polars to -180 to +180 degrees using WISDEM tool
    afp_extrap = Polar(10e6,
                       interp_afp['aoa'],
                       interp_afp['cl'],
                       interp_afp['cd'],
                       -interp_afp['cm']).extrapolate(cdmax=1.3)
    
    afp_data = AirfoilTable(afp_extrap.alpha, cl=afp_extrap.cl, cd=afp_extrap.cd, cm=afp_extrap.cm)
    afp_data.write_openfast_polar('../../OpenFAST_NaluPolars/Unchanged_Airfoils/IEA-15-240-RWT_AeroDyn15_Polar_{:02d}.dat'.format(i))


