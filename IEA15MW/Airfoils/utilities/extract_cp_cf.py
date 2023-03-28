# state file generated using paraview version 5.9.0

#### import the simple module from the paraview
from paraview.simple import *
import glob, sys
#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

try: 
    print(sys.argv[1])
    aoa = float(sys.argv[1])
    # ----------------------------------------------------------------
    # setup the data processing pipelines
    # ----------------------------------------------------------------
    
    # create a new 'ExodusIIReader'
    
    output_file = glob.glob('results/*.e')[0]
    output_f = ExodusIIReader(registrationName='output_f', FileName=[output_file])
    output_f.PointVariables = ['pressure', 'tau_wall', 'viscous_force_', 'pressure_force_']
    output_f.SideSetArrayStatus = ['airfoil']
    output_f.ElementBlocks = []
    UpdatePipeline(time=output_f.TimestepValues[-1], proxy=output_f)
    
    # create a new 'Extract Block'
    extractBlock1 = ExtractBlock(registrationName='ExtractBlock1', Input=output_f)
    extractBlock1.BlockIndices = [9]
    
    # create a new 'Transform'
    transform0 = Transform(registrationName='Transform0', Input=extractBlock1)
    transform0.Transform = 'Transform'
    # init the 'Transform' selected for 'Transform'
    transform0.Transform.Translate = [-0.25, 0.0, 0.0]
    
    # create a new 'Transform'
    transform1 = Transform(registrationName='Transform1', Input=transform0)
    transform1.Transform = 'Transform'
    # init the 'Transform' selected for 'Transform'
    transform1.Transform.Rotate = [0.0, 0.0, aoa]
    
    # create a new 'Transform'
    transform2 = Transform(registrationName='Transform2', Input=transform1)
    transform2.Transform = 'Transform'
    transform2.Transform.Translate = [+0.25, 0.0, 0.0]
    
    # create a new 'Calculator'
    calculator1 = Calculator(registrationName='Calculator1', Input=transform2)
    calculator1.ResultArrayName = 'cf'
    calculator1.Function = 'viscous_force_ / (0.5 * 1.225 * 15.0 * 15.0) * abs(pressure) / mag(pressure_force_)'
    
    # create a new 'Calculator'
    calculator2 = Calculator(registrationName='Calculator2', Input=calculator1)
    calculator2.ResultArrayName = 'cp'
    calculator2.Function = 'pressure / (0.5 * 1.225 * 15.0 * 15.0)'
    
    calculator3 = Calculator(registrationName='Calculator3', Input=calculator2)
    calculator3.ResultArrayName = 'top'
    calculator3.Function = '(cross(pressure_force_, kHat) . iHat) / pressure'
    
    # get animation scene
    #animationScene1 = GetAnimationScene()
    #animationScene1.AnimationTime = output_f.TimestepValues[-1]
    #animationScene1.GoToLast()
    
    
    #--------------------------------------------
    # uncomment the following to render all views
    #RenderAllViews()
    # alternatively, if you want to write images, you can use SaveScreenshot(...).
    # save data
    SaveData('cp_cf.csv', proxy=calculator3, ChooseArraysToWrite=1,  PointDataArrays=['cp', 'cf', 'top'],  Precision=12)
    
    sys.exit()

except:
    
    pass

