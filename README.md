# Project 8C C17 chassis design review package

This checkout contains the generated FreeCAD master model, a structural-only STEP assembly, a full review assembly with donor references, and donor reference geometry, constraint audit, and validation records for Project 8C C17.

The package is **CONCEPT / DESIGN REVIEW / ENGINEERING HOLD**. It is not released for fabrication or road use. Toyota donor dimensions and all safety-critical mounts remain provisional or measured-item placeholders until C17 gates G01–G11 are closed.

To regenerate the CAD outputs in the cloud environment:

```bash
cd /workspace/project-8c-chassis
MPLCONFIGDIR=/tmp/mpl \
PYTHONPATH=/usr/lib/freecad-python3/lib:/usr/lib/freecad-python3/Ext \
PYTHONHOME=/usr \
/usr/bin/python3 scripts/generate_project8c.py
```

The script requires the supplied STEP references under `references/` and writes all generated files to `deliverables/`. The master FCStd tree is organized into parameters, body reference, hardpoints, donor references, front/cabin/rear weldments, global interfaces, occupants, body mounts, analysis, fabrication, and exports.


`Project_8C_Chassis_01_Front.step` now carries the supplied C18 front module plus named cabin adapters. `Project_8C_Chassis_03_Rear.step` carries the supplied Probox rear module plus named cradle adapters. `Project_8C_Structural_Chassis_Assembly.step` is the weldment/interface-only export. `Project_8C_Master_Chassis_Assembly.step` is the full review assembly with the supplied C11, C18, Probox, body, and wheel reference geometry.
