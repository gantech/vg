The directories IEA-15-240-RWT-Monopile and IEA-15-240-RWT were directly copied from v1.1.3 of the IEA-15-240-RWT repository, in the OpenFAST directory. Only "Airfoils", within the IEA-15-240-RWT folder, should be modified, and nothing else within these imported folders.

"Airfoils" is a symbolic link to another directory, which contains the airfoil polars in a format for OpenFAST to use. To modify which airfoils are considered, the symbolic link should be modified to point to a different folder. The repository contains "Unchanged_Airfoils", which refers to the nalu results without the VGs, and "Modified_Airfoils", which refers to the nalu results with VGs.

https://github.com/IEAWindTask37/IEA-15-240-RWT/tree/v1.1.3/OpenFAST