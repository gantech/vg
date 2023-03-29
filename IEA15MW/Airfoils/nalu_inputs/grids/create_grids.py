#! coding: utf-8
import glob
import numpy as np
import subprocess, sys
sys.path.append('../../utilities')
from airfoil import AirfoilShape


afs =  [ af.split('/')[1] for af in glob.glob('coordinates/*') ]

for af in afs:

    print(af)

    profile = np.loadtxt('coordinates/{}'.format(af))
    af_shape = AirfoilShape(profile[:,0], profile[:,1])

    tvec = np.array( [0.2001, float(af_shape(0.2001)[2]),0]) - np.array( [0.1999, float(af_shape(0.1999)[2]), 0.0])
    nvec = np.cross( tvec, np.array([0,0,-1]))
    print('tvec = ', tvec)
    print('nvec = ', nvec/np.linalg.norm(nvec))
    
    af_cst = af_shape.cst(order=8)
    af_shape = AirfoilShape.from_cst_parameters(af_cst.cst_lower,
                                                np.minimum(af_shape.te_lower, -0.001),
                                                af_cst.cst_upper,
                                                np.maximum(af_shape.te_upper, 0.001))

    
    

    # with open('af_profile_upper.dat','w') as f:
    #     f.write('{:d} \n'.format( np.size(af_shape.xupper)))
    #     for i,x in enumerate(af_shape.xupper):
    #         f.write('{} {} 0.0000 \n'.format(x, af_shape.yupper[i]))
    # with open('af_profile_lower.dat','w') as f:
    #     f.write('{:d} \n'.format( np.size(af_shape.xlower) + 1))
    #     for i,x in enumerate(af_shape.xlower):
    #         f.write('{} {} 0.0000 \n'.format(x, af_shape.ylower[i]))
    #     f.write('0.0000 0.0000 0.0000 \n')

    # with open('tmp_grid.glf', "w") as outfile:
    #     subprocess.run(["sed", "s/AF_NAME/{}/".format(af), "create_af_grid.glf"], stdout=outfile)
    #     subprocess.call(["/projects/hfm/Fidelity/Pointwise/Pointwise2022.1.2/pointwise", "-b", "tmp_grid.glf"])
    #     subprocess.call(["rm", "tmp_grid.glf"])

    # with open('tmp_grid.glf', "w") as outfile:
    #     subprocess.run(["sed", "s/AF_NAME/{}/".format(af), "extrude_mesh.glf"], stdout=outfile)
    #     subprocess.call(["/projects/hfm/Fidelity/Pointwise/Pointwise2022.1.2/pointwise", "-b", "tmp_grid.glf"])
    #     subprocess.call(["rm", "tmp_grid.glf"])
