# Spaceframe rebuild review

The architecture now follows the supplied reference image as a triangulated spaceframe rather than a ladder frame with a few braces.

- 78 dedicated `SF-*` members form paired lower and upper rails, repeated side-bay triangles, lower/upper crossmembers, front and rear pyramids, cockpit hoops, roof X-bracing, side intrusion bars, and cowl diagonals.
- The supplied C18 GX100 assembly remains the actual front-module payload: 108 donor solids plus three cabin adapters.
- The supplied Probox cassette remains the actual rear-module payload: 199 donor solids plus four cradle adapters.
- The C11 cabin reference, scaled body opening study, and wheel/tyre envelopes remain separately tagged reference geometry.
- `Project_8C_Spaceframe_Architecture.step` isolates the image-led tubular frame. `Project_8C_Structural_Chassis_Assembly.step` contains the spaceframe, cabin continuity members, and donor adapters. `Project_8C_Master_Chassis_Assembly.step` contains the full review assembly.

The triangulation is a packaging and load-path study. It does not establish tube grade, weld detail, suspension pickup strength, rollover compliance, or fabrication release.
