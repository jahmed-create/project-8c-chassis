# Front/rear module replacement review

The supplied C18 GX100 STEP is now the actual front-module payload. `Project_8C_Chassis_01_Front.step` contains the 108 supplied C18 solids plus three explicitly named cabin-to-C18 RHS adapter members. The old proxy front frame members remain in the FreeCAD history tree as hidden comparison geometry and are excluded from the front export.

The supplied Probox cassette is now the actual rear-module payload. `Project_8C_Chassis_03_Rear.step` contains the 199 supplied Probox solids plus four named RHS cradle adapter members. The old proxy rear frame members remain hidden comparison geometry and are excluded from the rear export.

`Project_8C_Structural_Chassis_Assembly.step` contains the cabin, continuity/interface weldment, and only the adapter members. `Project_8C_Master_Chassis_Assembly.step` contains the body opening study, wheel/tyre envelopes, cabin, continuity structure, and the actual supplied C18/Probox/C11 reference payloads at their global coordinates.

The donor assemblies are still provisional design inputs. No hole pattern, bolt axis, suspension mount, drivetrain orientation, or safety claim is inferred from their visual alignment.
