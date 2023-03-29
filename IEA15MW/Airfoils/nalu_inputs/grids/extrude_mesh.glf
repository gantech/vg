# Fidelity Pointwise 2022.1.2 Journal file - Wed Mar 29 13:06:16 2023

package require PWI_Glyph 6.22.1

pw::Application setUndoMaximumLevels 5
pw::Application reset
pw::Application markUndoLevel {Journal Reset}

pw::Application clearModified

pw::Application reset -keep Clipboard
set _TMP(mode_1) [pw::Application begin ProjectLoader]
  $_TMP(mode_1) initialize AF_NAME.pw
  $_TMP(mode_1) setAppendMode false
  $_TMP(mode_1) setRepairMode Defer
  $_TMP(mode_1) load
$_TMP(mode_1) end
unset _TMP(mode_1)
pw::Application resetUndoLevels
pw::Display resetView -Z
pw::Application setCAESolver {EXODUS II} 3
pw::Application markUndoLevel {Set Dimension 3D}

set _TMP(mode_1) [pw::Application begin Create]
  set _DM(1) [pw::GridEntity getByName dom-1]
  set _TMP(PW_1) [pw::FaceStructured createFromDomains [list $_DM(1)]]
  set _TMP(face_1) [lindex $_TMP(PW_1) 0]
  unset _TMP(PW_1)
  set _BL(1) [pw::BlockStructured create]
  $_BL(1) addFace $_TMP(face_1)
$_TMP(mode_1) end
unset _TMP(mode_1)
set _TMP(mode_1) [pw::Application begin ExtrusionSolver [list $_BL(1)]]
  $_TMP(mode_1) setKeepFailingStep true
  $_BL(1) setExtrusionSolverAttribute Mode Translate
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {1 0 0}
  $_BL(1) setExtrusionSolverAttribute TranslateDirection {0 0 1}
  $_BL(1) setExtrusionSolverAttribute TranslateDistance 0.02333
  $_TMP(mode_1) run 64
$_TMP(mode_1) end
unset _TMP(mode_1)
unset _TMP(face_1)
pw::Application markUndoLevel {Extrude, Translate}

set _TMP(PW_1) [pw::VolumeCondition getByName Flow]
$_TMP(PW_1) apply [list $_BL(1)]
pw::Application markUndoLevel {Set VC}

set _DM(2) [pw::GridEntity getByName dom-6]
set _DM(3) [pw::GridEntity getByName dom-2]
set _DM(4) [pw::GridEntity getByName dom-3]
set _DM(5) [pw::GridEntity getByName dom-4]
set _DM(6) [pw::GridEntity getByName dom-5]
set _DM(7) [pw::GridEntity getByName dom-7]
set _DM(8) [pw::GridEntity getByName dom-8]
set _DM(9) [pw::GridEntity getByName dom-9]
set _DM(10) [pw::GridEntity getByName dom-11]
unset _TMP(PW_1)
set _TMP(PW_1) [pw::BoundaryCondition getByName inflow]
$_TMP(PW_1) apply [list [list $_BL(1) $_DM(8)]]
pw::Application markUndoLevel {Set BC}

set _TMP(PW_2) [pw::BoundaryCondition getByName outflow]
$_TMP(PW_2) apply [list [list $_BL(1) $_DM(7)] [list $_BL(1) $_DM(9)]]
pw::Application markUndoLevel {Set BC}

set _TMP(PW_3) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

unset _TMP(PW_3)
set _TMP(PW_3) [pw::BoundaryCondition create]
pw::Application markUndoLevel {Create BC}

unset _TMP(PW_3)
set _TMP(PW_3) [pw::BoundaryCondition getByName bc-5]
$_TMP(PW_3) setName front
pw::Application markUndoLevel {Name BC}

set _TMP(PW_4) [pw::BoundaryCondition getByName bc-6]
$_TMP(PW_4) setName sides
pw::Application markUndoLevel {Name BC}

$_TMP(PW_3) setPhysicalType -usage CAE {Node Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_3) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_4) setPhysicalType -usage CAE {Side Set}
pw::Application markUndoLevel {Change BC Type}

$_TMP(PW_4) setName back
pw::Application markUndoLevel {Name BC}

$_TMP(PW_3) apply [list [list $_BL(1) $_DM(10)]]
pw::Application markUndoLevel {Set BC}

$_TMP(PW_4) apply [list [list $_BL(1) $_DM(1)]]
pw::Application markUndoLevel {Set BC}

set _TMP(PW_5) [pw::BoundaryCondition getByName airfoil]
$_TMP(PW_5) apply [list [list $_BL(1) $_DM(3)] [list $_BL(1) $_DM(4)] [list $_BL(1) $_DM(5)] [list $_BL(1) $_DM(6)]]
pw::Application markUndoLevel {Set BC}

unset _TMP(PW_1)
unset _TMP(PW_2)
unset _TMP(PW_5)
unset _TMP(PW_3)
unset _TMP(PW_4)
pw::Application save AF_NAME_3d.pw
set _TMP(mode_1) [pw::Application begin CaeExport [pw::Entity sort [list $_BL(1)]]]
  $_TMP(mode_1) initialize -strict -type CAE AF_NAME_3d.exo
  $_TMP(mode_1) verify
  $_TMP(mode_1) write
$_TMP(mode_1) end
unset _TMP(mode_1)
