# Project 8C C17 input acceptance and design assessment

**Revision:** C17 Rev 0, design review package generated 11 October 2026  
**Release state:** CONCEPT / DESIGN REVIEW / ENGINEERING HOLD — NOT FOR FABRICATION

## Source authority and status

The C17 dossier is treated as the primary design specification. The companion constraint JSON, hardpoint registry, open-gate CSV, C10/C11 cabin references, C18 GX100 frame STEP, and Probox cassette STEP are retained under `references/`. The PDFs and STEP models are design inputs and visual/packaging studies. They do not establish measured donor interfaces, structural adequacy, roadworthiness, or fabrication approval.

The master coordinate system is rear wheel station origin, +X toward the front, +Y toward vehicle left, +Z up, with ground Z=0 provisional. The body-only scale is `S = 2100/1770 = 1.18644068`; Toyota donor hardware remains 1:1.

## Normalized master constraints

| Item | Value | Status | Interpretation |
|---|---:|:---:|---|
| Body overall length | 6110.17 mm | D | 5150 × S; exterior surface still incomplete |
| Body overall width | 2100 mm | F | approved body/fender target |
| Body overall height | 1779.66 mm | D | silhouette datum requires validation |
| Wheelbase | 3559.32 mm | D | nominal wheel stations |
| Rear axle | X=0 mm | F | global datum |
| Front axle | X=3559.32 mm | D | public drawings may round to 3559 |
| Front track study | 1550 mm | P | GX100 packaging target |
| Rear track reference | 1455 mm | P | Probox study target |
| Front trial wheel | Y=±775, Z=330; tyre OD 660 | P | wheel/WMS/tyre still unverified |
| Cabin opening | X=889.83…2550.85 | P | C11 spatial template |
| Front frame study | X=2375…4545 | P | C16 span; shared splice required |
| Rear module study | X=-791…950 | P | C09/C08 envelope; donor mounts unmeasured |

## Hardpoint assessment

The complete incoming registry is retained in `Project_8C_C17_Hardpoint_Registry.csv`. The generated model shows status-tagged markers for fixed/derived wheel stations, provisional GX100 links and coilover proxies, provisional Probox hub stations, and the two conflicting firewall/cockpit planes. Missing GX100 upper pivots, ball joints, tie rods, wheel mounting surfaces and rack points remain named M items. Probox strut tops, four subframe mounts, engine/transaxle mounts and output/CV axes remain M items. Seat H-points and belts remain M/E items.

No provisional marker is a drilling datum. The generated bracket schedule is explicitly HOLD.

## Previous concept assessment

- **C11 cabin:** 21 valid solids and a useful spatial ladder. It lacks seats, doors, floor sheet, rollover system, belt anchors and a structural firewall. The new model retains the C11 station intent, then adds continuous overlap rails and diagonal splice paths.
- **C18/C16 front:** supplied STEP imports as 108 valid solids with a 2350…4553.65 mm X range. It is retained as a separate donor/reference group. The new front weldment uses continuous rails, four crossmembers, wheel outriggers, and proxy tower paths; supplied bracket geometry is not treated as measured.
- **Probox cassette:** supplied STEP imports as 199 valid solids with a -816…975 mm X range. It is retained as a separate donor/reference group and review STEP. The structural rear cradle uses a simpler replaceable RHS load path plus clearly named mount placeholders.

## Conflict resolution log

- **X-01 firewall/cockpit (950 vs 889.83):** shown as two red planes and left quarantined. The final bulkhead must follow seat-back, heat/fire, engine, service and occupant review.
- **X-02 front/cabin overlap (2375…2551):** converted to a deliberate 176 mm co-design lap with shared 60×80×4 rails and diagonal splice members. Joint weld access and loads remain to be checked.
- **X-03 wheel/arch mismatch:** front wheel and tyre are kept as provisional study markers; scaled arch and actual fender CAD are absent. No clearance approval is claimed.
- **X-04 body width mismatch:** the C10 loft is central shell only (about 1424 mm maximum) while the approved exterior target is 2100 mm. The 2100 mm reference is represented as a separate envelope until validated fenders arrive.

## Architecture alternatives and selection

**Alternative A — continuous deep-sill frame with cross-braced floor (selected):** paired 100×50×3 cabin sills, upper door rails, transverse floor members, continuous 60×80×4 overlap rails, and triangulated front/rear cradles. It gives the clearest torsion and suspension load paths while keeping tubes straight and jig-accessible.

**Alternative B — detached three-cassette ladder:** independent front, cabin and rear boxes joined by short plates. It is easier to model but creates discontinuous load paths at both interfaces and makes open-roof torsion and firewall loads dependent on local splice plates. It is rejected for the primary study, though the rear donor cassette remains removable inside the selected continuous frame.

## Required release gates

G01–G11 remain open: donor identity and drivetrain; Probox mounts/strut tops; GX100 link and steering survey; wheel/brake/rack/wing package; damper specification; final fender CAD; seats/belts/rollover; firewall and transaxle go/no-go; mass/material/load data; FEA/fatigue/weld/jig/inspection; BRTA classification and approval path.

The correct next physical actions are a donor survey fixture, a measured GX100 suspension skeleton, the exact Probox drivetrain orientation check, validated exterior fender/tyre CAD, and a qualified occupant/restraint strategy. Only after those inputs should holes, weld details, final section sizes, cut lengths or safety conclusions be released.
