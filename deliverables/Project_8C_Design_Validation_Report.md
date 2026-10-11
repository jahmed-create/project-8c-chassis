# Project 8C rebuilt design validation report

**Revision:** C17 rebuilt review pass  
**Status:** CONCEPT / DESIGN REVIEW / ENGINEERING HOLD

The first proxy-only assembly was rejected as insufficient. This rebuilt package keeps the supplied donor geometry in the review assembly and separates the structural-only export from the full review assembly.

- FreeCAD master: 126 objects, including the C11, C18, and Probox supplied references, 62 named RHS members, wheel/tyre envelopes, body station envelopes, and status metadata. All generated shapes reloaded valid.
- Structural STEP: 77 valid solids after re-import; this is the weldment-only assembly.
- Full review STEP: 410 valid solids after re-import; this contains the 108-solid C18 front reference, 199-solid Probox reference, 21-solid C11 reference, scaled body opening study, wheel/tyre envelopes, and structural members at their global positions.
- Donor review STEP: 328 valid solids after re-import.
- Units and axes: millimetres; +X front, +Y vehicle-left, +Z up; rear axle origin.
- Body-only scale: `2100/1770` passes. The full scaled body starter envelope spans X=-1305.08…4805.08; the 2100 mm fender target remains a separate reference constraint.
- Geometry: all generated and re-imported STEP files are non-null and valid. Structural contacts, body references, and unresolved conflict planes are separately tagged.

The rebuilt architecture adds continuous rear-to-front rails, rear cradle diagonals, front tower ties, a provisional cabin shear panel, door-opening diagonals, a candidate firewall hoop, explicit wheel/tyre envelopes, and a rear service opening. These are design-review geometry, not released cut or weld data.

No suspension kinematics approval, donor interface measurement, drivetrain orientation approval, clearance signoff, FEA, fatigue assessment, brake proof, restraint proof, crash proof, or legal approval has been performed. Gates G01–G11 remain open.
