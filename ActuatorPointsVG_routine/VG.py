# Coding: utf-8
import pandas as pd
import numpy as np
from scipy.spatial.transform import Rotation as R
#from mpi4py import MPI
import yaml


class VG:
    def __init__(self, beta=0, l=1.0, h=1.0, x0=0.0, y0=0.0, z0=0.0, normal_vec=[0,0,1.0]):
        """Initialize a VG with parameters

        Args:

            beta (double): Angle of VG w.r.t +x. Positive angle indicates
            positive rotation about +z axis. (degreees)
            l (double): Length of VG (m)
            h (double): Height of VG (m)
            x0 (double): X-Location of forward tip of VG (m)
            y0 (double): X-Location of forward tip of VG (m)
            z0 (double): Z-Location of forward tip of VG (m)

        Return:
            VG object

        """

        #Read a template of VG discretization into triangles. Template VG is a
        #right triangle with height and length of 1.0 in the z=0 plane, then
        #scaled to match length 'l' and height 'h'

        nodes = pd.read_csv('vg_template_coarse.dat',sep='\s+',skiprows=1,header=None,
                            nrows=10) * np.array([l,h,0.0])
        nodes = np.loadtxt('vg_template_coarse.dat',skiprows=1,max_rows=10) * np.array([l,h,0.0])

        cell_ids = pd.read_csv('vg_template_coarse.dat',sep='\s+',skiprows=12
                               ,header=None) - 1
        cell_ids = np.loadtxt('vg_template_coarse.dat',skiprows=12,dtype=int)-1
        cell_centers = (nodes[cell_ids[:,0]] +
                        nodes[cell_ids[:,1]] +
                        nodes[cell_ids[:,2]])/3.0

        self.beta = np.radians(beta)
        self.l = l
        self.h = h
        self.origin = np.array([x0,y0,z0])

        #Coordinate directions for template VG
        bvec = np.array([0,1,0])
        tvec = np.array([1,0,0])
        nvec = np.array([0,0,1])

        r1 = self.get_rotation(bvec, normal_vec)
        self.bvec = r1.apply(bvec)

        r2 = R.from_rotvec( self.beta * self.bvec)

        self.nvec = r2.apply(r1.apply(nvec))
        self.tvec = r2.apply(r1.apply(tvec))


        x1 = (nodes[cell_ids[:,1]] -
               nodes[cell_ids[:,0]])
        x2 = (nodes[cell_ids[:,2]] -
               nodes[cell_ids[:,0]])

        nodes = r2.apply(r1.apply(nodes))
        self.centers = r2.apply(r1.apply(cell_centers)) + np.array([x0,y0,z0])
        self.areas = np.linalg.norm(0.5 * np.cross( (nodes[cell_ids[:,1]] -
                                      nodes[cell_ids[:,0]]),
                                     (nodes[cell_ids[:,2]] -
                                      nodes[cell_ids[:,0]])), axis=1)

    def get_rotation(self, vec1, vec2):
        """Create a quaternion that rotates vec1 to vec2

           Args:
               vec1 (np.ndarray):
               vec2 (np.ndarray):
           Return:
               r: Rotation object that rotates vec1 to vec2

        """
        v1Cv2 = np.cross(vec1, vec2)
        return R.from_rotvec( np.arccos(np.dot(vec1, vec2)) * v1Cv2)
        # q = np.r_[ np.dot(vec1, vec2), v1Cv2]
        # q /= np.linalg.norm(q)
        # q[0] += 1.0 #Change angle from theta to theta/2
        # q /= np.linalg.norm(q)
        # return R.from_quat(q)


delta1 = 4.267e-3
delta2 = 1.067e-2
angle = 19.5
height = 2.133e-3
xdisp = 6.40e-2
length = 6.4e-3

ydisp = -0.5 * delta2 -0.5 * delta1

vg_l = VG(beta=angle, l=length, h=height,x0=xdisp,y0=ydisp+0.5*delta1)
vg_yaml =  {
    'ncells': np.size(vg_l.centers,0),
    'centers': vg_l.centers.tolist(),
    'areas': vg_l.areas.tolist(),
    'bvec': vg_l.bvec.tolist(),
    'tvec': vg_l.tvec.tolist(),
    'nvec': vg_l.nvec.tolist(),
}
yaml.dump(vg_yaml, open('vg_l.yaml','w'))
