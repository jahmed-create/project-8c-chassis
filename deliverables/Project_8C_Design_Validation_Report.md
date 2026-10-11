# Project 8C front/rear replacement validation report

**Status:** CONCEPT / DESIGN REVIEW / ENGINEERING HOLD

The supplied C18 GX100 STEP is the front-module payload, and the supplied Probox STEP is the rear-module payload. The old proxy frame members are hidden in the FreeCAD history tree and excluded from those module exports.

- FreeCAD master: 135 objects; all generated shapes valid on reload.
- Front module STEP: 111 valid solids — 108 supplied C18 solids plus 3 named RHS adapters.
- Rear module STEP: 203 valid solids — 199 supplied Probox solids plus 4 named RHS adapters.
- Cabin module STEP: 22 valid solids.
- Structural-only assembly: 46 valid solids.
- Full review assembly: 379 valid solids, including C11, C18, Probox, body opening and wheel/tyre study geometry.
- Donor review STEP: 328 valid solids.
- Units and axes: millimetres; +X front, +Y vehicle-left, +Z up; rear axle origin.
- Body-only scale `2100/1770`: PASS.

The adapters are integration study members without invented donor holes or bolt coordinates. Donor interfaces, suspension geometry, drivetrain orientation, clearance, kinematics, FEA, fatigue, restraint, crash, weld, and legal approval remain open under C17 gates G01–G11.
