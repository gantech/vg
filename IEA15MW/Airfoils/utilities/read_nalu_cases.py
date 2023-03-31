# Collection of utilities to read and process nalu-wind output data for airfoil
# simulations

import yaml, json, glob, sys
from pathlib import Path
import numpy as np
import pandas as pd


def read_static_case(
    af_name,
    aoa,
    rey,
    u_infty=15.0,
    rho=1.225):
    """Read the airfoil performance data for simulation of flow past an airfoil
    using k-w-SST turbulence model

    Args:
        af_name (string):
        aoa (double): Angle of attack in degrees
        rey (double): Reynolds number
        u_infty (double): Free-stream velocity (in m/s)
        rho (double): Free-stream density of air (in kg/m^3)

    Returns:
        [cl, cd, cm]: Array of lift, drag and moment coefficient

    """

    results_file = "nalu_runs/{}/static/rey_{:08d}/aoa_{}/results/forces.dat".format(
        af_name, int(rey), aoa
    )

    if not Path(results_file).exists():
        print(
            "Results file ", results_file, " doesn't exist. Please check this directory"
        )
        return [-1, -1, -1]

    try:
        data = pd.read_csv(
            results_file,
            sep="\s+",
            skiprows=1,
            header=None,
            names=[
                "Time",
                "Fpx",
                "Fpy",
                "Fpz",
                "Fvx",
                "Fvy",
                "Fvz",
                "Mtx",
                "Mty",
                "Mtz",
                "Y+min",
                "Y+max",
            ],
        ).iloc[-1]
        dyn_pres = 0.5 * rho * (u_infty ** 2) * 2.333E-02
        cl = (data["Fpy"] + data["Fvy"]) / dyn_pres
        cd = (data["Fpx"] + data["Fvx"]) / dyn_pres
        cm = data["Mtz"] / dyn_pres
    except:
        cl = 0.0
        cd = 0.0
        cm = 0.0

    return [cl, cd, cm]

def collect_xfoil_polar(dir_name, yaml_filename, af_name=None):
    if (af_name is None):
        af_list = glob.glob(dir_name+'/*polar')
    else:
        af_list = glob.glob(dir_name+'/'+af_name+'*polar')
    af_polar = {}
    for af in af_list:
        af_name = Path(af).with_suffix('').name
        try:
            p_data = pd.read_csv(af,skiprows=12,sep='\s+',usecols=[0,1,2,4],header=None,names=['aoa','cl','cd','cm'])
            af_polar[af_name] = {
                'aoa': p_data['aoa'].to_list(),
                'cl': p_data['cl'].to_list(),
                'cd': p_data['cd'].to_list(),
                'cm': p_data['cm'].to_list()
            }
        except:
            af_polar[af_name] = {
                'aoa': [-10,25],
                'cl': [0,0],
                'cd': [0,0],
                'cm': [0,0]
            }
            
    yaml.dump(af_polar, open(yaml_filename,'w'), default_flow_style=False)
    
def read_static_cases(aoa_range=np.linspace(-10, 25, 36), rey=[10e6]):
    """Read aerodynamic performance data for static cases in airfoil.

    """

    airfoils = [ af.split('/')[-1] for af in glob.glob('nalu_inputs/grids/coordinates/*') ]
    
    Path("xfoil_results/").mkdir(parents=True, exist_ok=True)
    Path("nalu_results/static_vg/").mkdir(parents=True, exist_ok=True)

    #for re in rey:
        #collect_xfoil_polar('xfoil_runs/rey_{:08d}/'.format(int(re)), 'xfoil_results/airfoils_rey{:08d}.yaml'.format(int(re)))
        
    for af in airfoils:
        for re in rey:
            polar_data = np.array(
                [read_static_case(af, aoa, re) for aoa in aoa_range]
            )
            
            p_data = { af: {
                "aoa": aoa_range.tolist(),
                "cl": polar_data[:, 0].tolist(),
                "cd": polar_data[:, 1].tolist(),
                "cm": polar_data[:, 2].tolist(),
            } }
            print(p_data)
            yaml.dump(
                p_data,
                open("nalu_results/static_vg/{}_rey{:08d}.yaml".format(af, int(re)), "w"),
            )
            

if __name__ == "__main__":

    read_static_cases()
