# Collection of utilities to generate nalu-wind input files for airfoil
# simulations

import yaml, json, glob, sys
from pathlib import Path
import numpy as np
import pandas as pd
from scipy.spatial.transform import Rotation
sys.path.append('utilities/')
import VG
from airfoil import AirfoilShape

def gen_static_case(af_name, mesh_file, aoa, rey, run_folder="nalu_runs", template="nalu_inputs/template/airfoil_static.yaml"):
    """Generate a nalu input file for simulation of flow past an airfoil
    using k-w-SST turbulence model

    Args:
        af_name (string):
        mesh_file (string):
        aoa (double): Angle of attack in degrees
        rey (double): Reynolds number
        template (string): Path to template nalu input file in yaml format

    Returns:
        None

    """

    if ( not Path(template).exists() ):
        print("Template file ", template, " doesn't exist. Please check your inputs")
        sys.exit()

    tfile = yaml.load(open(template),Loader=yaml.UnsafeLoader)

    if ( not Path(mesh_file).exists() ):
        print("Mesh file ", mesh_file, " doesn't exist. Please check your inputs")
        sys.exit()

    Path(run_folder+'/{}/static/rey_{:08d}/aoa_{}'.format(af_name, int(rey), aoa )).mkdir(
        parents=True, exist_ok=True)

    tfile['realms'][0]['mesh_transformation'][0]['motion'][0]['angle'] = float(aoa)
    tfile['realms'][0]['mesh'] = str(Path(mesh_file).absolute())

    visc = float(15.0 * 1.225/ rey)
    tfile['realms'][0]['material_properties']['specifications'][1]['value'] = visc

    tfile['realms'][0]['output']['output_data_base_name'] = 'results/{}.e'.format(af_name)

    tfile['linear_solvers'][1]['muelu_xml_file_name'] = str(
        Path('nalu_inputs/template/milestone_aspect_ratio_gs.xml').absolute() )

    yaml.dump(tfile, open(run_folder+'/{}/static/rey_{:08d}/aoa_{}/{}_static_aoa_{}.yaml'.format(
        af_name, int(rey), aoa, af_name, aoa),'w'), default_flow_style=False)

def gen_static_case_vg(af_name, mesh_file, aoa, rey,
                       run_folder="nalu_runs",
                       template="nalu_inputs/template/airfoil_static_vg.yaml",
                       vg_template='nalu_inputs/template/vg_template_coarse.dat',
                       vg_loc=0.2):
    """Generate a nalu input file for simulation of flow past an airfoil with a VG
    using k-w-SST turbulence model

    Args:
        af_name (string):
        mesh_file (string):
        aoa (double): Angle of attack in degrees
        rey (double): Reynolds number
        template (string): Path to template nalu input file in yaml format
        template_vg (string): Path to template VG file
        vg_loc (double): Non-dimensional location of VG along the airfoil

    Returns:
        None

    """

    print("Few parameters of the VG are hard-coded for now. Needs to be converted to function inputs later")

    if ( not Path(template).exists() ):
        print("Template file ", template, " doesn't exist. Please check your inputs")
        sys.exit()
    if ( not Path(vg_template).exists() ):
        print("VG Template file ", vg_template, " doesn't exist. Please check your inputs")
        sys.exit()

    tfile = yaml.load(open(template),Loader=yaml.UnsafeLoader)

    if ( not Path(mesh_file).exists() ):
        print("Mesh file ", mesh_file, " doesn't exist. Please check your inputs")
        sys.exit()

    Path(run_folder+'/{}/static/rey_{:08d}/aoa_{}'.format(af_name, int(rey), aoa )).mkdir(
        parents=True, exist_ok=True)

    tfile['realms'][0]['mesh_transformation'][0]['motion'][0]['angle'] = float(aoa)
    tfile['realms'][0]['mesh'] = str(Path(mesh_file).absolute())

    visc = float(15.0 * 1.225/ rey)
    tfile['realms'][0]['material_properties']['specifications'][1]['value'] = visc

    tfile['realms'][0]['output']['output_data_base_name'] = 'results/{}.e'.format(af_name)

    tfile['linear_solvers'][1]['muelu_xml_file_name'] = str(
        Path('nalu_inputs/template/milestone_aspect_ratio_gs.xml').absolute() )

    yaml.dump(tfile, open(run_folder+'/{}/static/rey_{:08d}/aoa_{}/{}_static_aoa_{}.yaml'.format(
        af_name, int(rey), aoa, af_name, aoa),'w'), default_flow_style=False)

    angle = 19.5
    height = 6.667E-03
    length = 2.000E-02
    delta2 = 3.333E-02
    delta1 = 1.333E-02
    
    profile = np.loadtxt('nalu_inputs/grids/coordinates/{}'.format(af_name))
    af_shape = AirfoilShape(profile[:,0], profile[:,1])

    
    tvec = np.array( [vg_loc+0.0001, float(af_shape(vg_loc+0.0001)[2]),0]) - np.array( [vg_loc-0.0001, float(af_shape(vg_loc-0.0001)[2]), 0.0])
    nvec = np.cross( tvec, np.array([0,0,-1]))
    nvec = nvec/np.linalg.norm(nvec)

    x_vg = np.array([vg_loc, float(af_shape(vg_loc)[2]), 0.5*delta2])
    rot_vec = Rotation.from_rotvec(np.radians(aoa) * np.array([0, 0, -1]))
    x_vg_rot = rot_vec.apply(x_vg-np.array([0.25,0.0,0.0])) + np.array([0.25,0.0,0.0])
    nvec_rot = rot_vec.apply(nvec)
    print('Airfoil = ', af_name, ' AoA = ', aoa, ' degrees')
    print('nvec_rot = ', nvec_rot)
    print('x_vg_rot = ', x_vg_rot)
    
    vg_l = VG.VG(template_file=vg_template,
              beta=angle, l=length, h=height,
              x0=x_vg_rot[0], y0=x_vg_rot[1], z0=x_vg_rot[2],
              normal_vec=nvec_rot)
    
    vg_yaml =  {
        'ncells': np.size(vg_l.centers,0),
        'centers': vg_l.centers.tolist(),
        'areas': vg_l.areas.tolist(),
        'bvec': vg_l.bvec.tolist(),
        'tvec': vg_l.tvec.tolist(),
        'nvec': vg_l.nvec.tolist(),
    }
    yaml.dump(vg_yaml, open( run_folder+'/{}/static/rey_{:08d}/aoa_{}/vg.yaml'.format(
        af_name, int(rey), aoa),'w'))
    
    

def write_xfoil_input_file(dir_name,af_name,re):
    with open(dir_name+'/'+af_name+'.in','w') as f:
      f.write('load ../../nalu_inputs/grids/coordinates/{} \n'.format(af_name))
      f.write('{} \n'.format(af_name))
      f.write('pane \n')
      f.write('oper \n')
      f.write('v {} \n'.format(re))
      f.write('p \n')
      f.write('{}.polar \n'.format(af_name))
      f.write('\n')
      f.write('aseq -10 14 1 \n')
      f.write('aseq 14.1 25.0 0.1 \n')
      f.write('\n')
      f.write('quit\n')

def gen_static_cases(aoa_range = np.linspace(-10,25,36), rey=[10e6]):
    """Generate static cases for the airfoils in the database

    Args:
        rey (list): List of Reynolds numbers
        aoa_range (np.array): Angle of attack range

    Return:
       None

    """

    airfoils = [ af.split('/')[-1] for af in glob.glob('nalu_inputs/grids/coordinates/*') ]
    
    for af in airfoils:
        print(af)
        for re in rey:
            # xfoil_dir = 'xfoil_runs/rey_{:08d}/'.format(int(re))
            # Path(xfoil_dir).mkdir(parents=True, exist_ok=True)
            # write_xfoil_input_file(xfoil_dir, af, re)
            for aoa in aoa_range:
                gen_static_case_vg(af, 'nalu_inputs/grids/{}_3d.exo'.format(af), aoa, re)

    # with open('xfoil_runs/run_xfoil.sh','w') as f:
    #     f.write('/projects/integrate/ganeshv/Xfoil/bin/xfoil < $1 \n')
        
    # with open('xfoil_runs/run_allxfoilcases.sh','w') as f:
    #     f.write('for i in rey*'+'\n')
    #     f.write('do'+'\n')
    #     f.write('  cd $i'+'\n')
    #     f.write('  ls *in | xargs -n 1 -P 36 bash ../run_xfoil.sh \n')
    #     f.write('  cd ../'+'\n')
    #     f.write('done'+'\n')
    

if __name__=="__main__":

    gen_static_cases()
