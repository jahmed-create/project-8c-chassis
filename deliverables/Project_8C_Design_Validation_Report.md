# Project 8C spaceframe validation report

**Status:** CONCEPT / DESIGN REVIEW / ENGINEERING HOLD

- FreeCAD master: 214 objects; all generated shapes valid on reload.
- Front module: 111 valid solids — supplied C18 assembly plus three adapters.
- Rear module: 203 valid solids — supplied Probox cassette plus four adapters.
- Dedicated spaceframe STEP: 78 valid triangulated RHS members.
- Structural assembly: 124 valid solids after re-import.
- Full review assembly: 457 valid solids after re-import.
- Donor review STEP: 328 valid solids after re-import.
- Units and axes: millimetres; +X front, +Y vehicle-left, +Z up; rear axle origin.
- Body-only scale `2100/1770`: PASS.

The spaceframe includes paired lower/upper rails, side-bay X bracing, crossmembers, front/rear pyramids, cockpit hoops, roof X-bracing, intrusion bars, and cowl diagonals to match the requested reference style. These members are design-review geometry; no tube grade, weld detail, FEA, kinematics, restraint, crash, or legal approval is claimed. Gates G01–G11 remain open.
