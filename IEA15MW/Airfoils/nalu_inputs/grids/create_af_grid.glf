# Pointwise V18.4R2 Journal file - Tue Sep 21 20:17:02 2021

package require PWI_Glyph 4.18.4

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified

set _TMP(mode_1) [pw::Application begin GridImport]
  $_TMP(mode_1) initialize -strict -type Segment af_profile_lower.dat
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Import Grid}

pw::Application undo
set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Segment af_profile_lower.dat
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Import Database}

set _TMP(mode_1) [pw::Application begin DatabaseImport]
  $_TMP(mode_1) initialize -strict -type Segment af_profile_upper.dat
  $_TMP(mode_1) read
  $_TMP(mode_1) convert
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Import Database}

set _DB(1) [pw::DatabaseEntity getByName curve-2]
set _DB(2) [pw::DatabaseEntity getByName curve-1]
set _TMP(PW_1) [pw::Connector createOnDatabase -parametricConnectors Aligned -merge 0 -reject _TMP(unused) [list $_DB(1) $_DB(2)]]
unset _TMP(unused)
unset _TMP(PW_1)
pw::Application markUndoLevel {Connectors On DB Entities}

set _CN(1) [pw::GridEntity getByName con-2]
set _CN(2) [pw::GridEntity getByName con-1]
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(1) $_CN(2)]
$_TMP(PW_1) do setDimension 200
$_TMP(PW_1) delete
unset _TMP(PW_1)
pw::CutPlane refresh
pw::Application markUndoLevel Dimension

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin Modify [list $_CN(1) $_CN(2)]]
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(2) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setBeginSpacing 0.001
  unset _TMP(PW_1)
  set _TMP(PW_1) [$_CN(1) getDistribution 1]
  $_TMP(PW_1) setEndSpacing 0.001
  unset _TMP(PW_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Change Spacings}

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint [$_CN(1) getPosition -arc 1]
  $_TMP(PW_1) addPoint {1 0 0}
  set _CN(3) [pw::Connector create]
  $_CN(3) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(3) calculateDimension
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Create 2 Point Connector}

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) addPoint [$_CN(2) getPosition -arc 0]
  $_TMP(PW_1) addPoint {1 0 0}
  set _CN(4) [pw::Connector create]
  $_CN(4) addSegment $_TMP(PW_1)
  unset _TMP(PW_1)
  $_CN(4) calculateDimension
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application markUndoLevel {Create 2 Point Connector}

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(PW_1) [pw::Collection create]
$_TMP(PW_1) set [list $_CN(4) $_CN(3)]
$_TMP(PW_1) do setDimensionFromSpacing 0.001
$_TMP(PW_1) delete
unset _TMP(PW_1)
pw::CutPlane refresh
pw::Application markUndoLevel Dimension

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::Edge createFromConnectors [list $_CN(1) $_CN(2) $_CN(4) $_CN(3)]]
  set _TMP(edge_1) [lindex $_TMP(PW_1) 0]
  unset _TMP(PW_1)
  set _DM(1) [pw::DomainStructured create]
  $_DM(1) addEdge $_TMP(edge_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin ExtrusionSolver [list $_DM(1)]]
  $_TMP(mode_1) setKeepFailingStep true
  $_DM(1) setExtrusionSolverAttribute NormalInitialStepSize 1e-05
  $_DM(1) setExtrusionSolverAttribute SpacingGrowthFactor 1.15
  $_TMP(mode_1) run 98
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(edge_1)
pw::Application markUndoLevel {Extrude, Normal}

set _TMP(mode_1) [pw::Application begin Create]
  set _TMP(PW_1) [pw::SegmentSpline create]
  set _CN(5) [pw::GridEntity getByName con-5]
  set _CN(6) [pw::GridEntity getByName con-6]
  $_TMP(PW_1) delete
  unset _TMP(PW_1)
$_TMP(mode_1) abort
unset _TMP(mode_1)
set _TMP(split_params) [list]
lappend _TMP(split_params) 48
lappend _TMP(split_params) 370
set _TMP(PW_1) [$_CN(6) split -I $_TMP(split_params)]
unset _TMP(PW_1)
unset _TMP(split_params)
pw::Application markUndoLevel Split

pw::Application setCAESolver CGNS 2
pw::Application markUndoLevel {Set Dimension 2D}

set _TMP(PW_1) [pw::VolumeCondition create]
pw::Application markUndoLevel {Create VC}

$_TMP(PW_1) apply [list $_DM(1)]
pw::Application markUndoLevel {Set VC}

$_TMP(PW_1) setName Flow
pw::Application markUndoLevel {Name VC}

unset _TMP(PW_1)
set ents [list $_DM(1)]
set _TMP(mode_1) [pw::Application begin Modify $ents]
$_TMP(mode_1) abort
unset _TMP(mode_1)

pw::Display resetView -Z
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_DM(1)]]]
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application setCAESolver {EXODUS II} 2
pw::Application markUndoLevel {Select Solver}

set _CN(7) [pw::GridEntity getByName con-6-split-1]
set _CN(8) [pw::GridEntity getByName con-6-split-2]
set _CN(9) [pw::GridEntity getByName con-6-split-3]
set _TMP(PW_1) [pw::BoundaryCondition getByName Unspecified]
set _TMP(PW_2) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_3) [pw::BoundaryCondition getByName bc-2]
unset _TMP(PW_2)
set _TMP(PW_4) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_5) [pw::BoundaryCondition getByName bc-3]
unset _TMP(PW_4)
set _TMP(PW_6) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

set _TMP(PW_7) [pw::BoundaryCondition getByName bc-4]
unset _TMP(PW_6)
$_TMP(PW_3) apply [list [list $_DM(1) $_CN(8)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_3) setName inflow
pw::Application markUndoLevel {Name BC}
unset _TMP(PW_3)
set _TMP(PW_3) [pw::BoundaryCondition getByName inflow]
$_TMP(PW_3) setPhysicalType -usage CAE {Side Set}

$_TMP(PW_5) apply [list [list $_DM(1) $_CN(9)] [list $_DM(1) $_CN(7)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_5) setName outflow
pw::Application markUndoLevel {Name BC}
unset _TMP(PW_5)
set _TMP(PW_5) [pw::BoundaryCondition getByName outflow]
$_TMP(PW_5) setPhysicalType -usage CAE {Side Set}

$_TMP(PW_7) setName airfoil
pw::Application markUndoLevel {Name BC}

$_TMP(PW_7) apply [list [list $_DM(1) $_CN(2)] [list $_DM(1) $_CN(3)] [list $_DM(1) $_CN(4)] [list $_DM(1) $_CN(1)]]
pw::Application markUndoLevel {Set BC}
unset _TMP(PW_7)
set _TMP(PW_7) [pw::BoundaryCondition getByName airfoil]
$_TMP(PW_7) setPhysicalType -usage CAE {Side Set}

unset _TMP(PW_1)
unset _TMP(PW_3)
unset _TMP(PW_5)
unset _TMP(PW_7)


set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_DM(1)]]]
  $_TMP(mode_1) initialize -strict -type CAE AF_NAME.exo
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application save AF_NAME.pw
