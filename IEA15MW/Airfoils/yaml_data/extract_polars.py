#coding: utf-8
from  turbine_perturb import TurbineData
import numpy as np
t = TurbineData("IEA-15-240-RWT.yaml")
t.dump_all_af_polar_cst('IEA15MW_polars.yaml')
