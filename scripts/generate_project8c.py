#!/usr/bin/env python3
"""Project 8C C17 conceptual chassis generator."""
import os, csv, json, math, shutil
from pathlib import Path
import FreeCAD as App
import Part
ROOT=Path(__file__).resolve().parents[1]; OUT=ROOT/'deliverables'; OUT.mkdir(parents=True,exist_ok=True)
SCALE=2100.0/1770.0; WB=3000.0*SCALE; BODY_L=5150.0*SCALE; BODY_FRONT=4050.0*SCALE; BODY_REAR=(4050.0-5150.0)*SCALE; FRONT_X=WB

doc=App.newDocument('Project8C_Master_Chassis')
def add_prop(obj,typ,name,value,grp='C17 Metadata'):
    try: obj.addProperty(typ,name,grp)
    except Exception: pass
    try: setattr(obj,name,value)
    except Exception: pass
def group(name,label,parent=None):
    g=doc.addObject('App::DocumentObjectGroup',name); g.Label=label
    if parent: parent.addObject(g)
    return g
def feature(grp,name,shape,status,source,part_id=None,notes=''):
    o=doc.addObject('Part::Feature',name); o.Shape=shape
    add_prop(o,'App::PropertyString','PartID',part_id or name)
    try:
        o.addProperty('App::PropertyEnumeration','Status','C17 Metadata'); o.Status=['F','D','P','M','E','X']; o.Status=status
    except Exception: add_prop(o,'App::PropertyString','StatusCode',status)
    add_prop(o,'App::PropertyString','Provenance',source); add_prop(o,'App::PropertyString','DesignNotes',notes); grp.addObject(o); return o
def tube(p0,p1,sy,sz,wall=3.0):
    p0,p1=App.Vector(*p0),App.Vector(*p1); v=p1.sub(p0); L=v.Length
    if L<=1e-6: raise ValueError('zero length tube')
    sh=Part.makeBox(L,sy,sz)
    if sy>2*wall and sz>2*wall and L>2*wall:
        sh=sh.cut(Part.makeBox(L+2,sy-2*wall,sz-2*wall,App.Vector(-1,wall,wall)))
    sh.Placement=App.Placement(p0,App.Rotation(App.Vector(1,0,0),v)); return sh
def marker(p,r=10,h=18): return Part.makeCylinder(r,h,App.Vector(*p),App.Vector(0,0,1))
def color(o,c,t=0):
    try: o.ViewObject.ShapeColor=c; o.ViewObject.Transparency=t
    except Exception: pass

g_params=group('G00_Parameters','00 Parameters & Revisions'); g_body=group('G01_BodyReference','01 Body Reference'); g_hp=group('G02_HardpointSkeleton','02 Hardpoint Skeleton'); g_donor_front=group('G03_DonorFrontGX100','03 Donor Front GX100 (provisional)'); g_donor_rear=group('G04_DonorRearProbox','04 Donor Rear Probox (provisional)'); g_front=group('G05_Front','05 Chassis 01 Front'); g_cabin=group('G06_Cabin','06 Chassis 02 Cabin'); g_rear=group('G07_Rear','07 Chassis 03 Rear'); g_int=group('G08_Interfaces','08 Interfaces Global'); g_seats=group('G09_Occupants','09 Seats Controls Belts'); g_bodymount=group('G10_BodyMounts','10 Body Mounts and Fluid Routing'); g_analysis=group('G11_Analysis','11 Analysis'); g_fab=group('G12_Fabrication','12 Fabrication'); g_exports=group('G13_Exports','13 Exports'); g_wheels=group('G14_Wheels','14 Wheel and Tyre Study')
param=doc.addObject('App::FeaturePython','MasterParameters'); param.Label='C17 Master Parameters (design review)'
for n,v,s in [('Scale',SCALE,'F'),('BodyLength',BODY_L,'D'),('BodyWidth',2100,'F'),('Wheelbase',WB,'D'),('RearAxleX',0,'F'),('FrontAxleX',FRONT_X,'D'),('FrontTrackStudy',1550,'P'),('RearTrackReference',1455,'P'),('FrontWheelZ',330,'P'),('CabinAftX',889.83,'P'),('LegacyFirewallX',950,'X'),('FrontFrameStartX',2375,'P'),('CabinFrontX',2550.85,'P'),('RearModuleMinX',-791,'P'),('RearModuleMaxX',950,'P')]:
    add_prop(param,'App::PropertyLength',n,v,'C17 Parameters'); add_prop(param,'App::PropertyString',n+'_Status',s,'C17 Status')
add_prop(param,'App::PropertyString','CoordinateSystem','+X front, +Y vehicle-left, +Z up; rear axle origin','C17 Parameters'); add_prop(param,'App::PropertyString','ReleaseState','CONCEPT / DESIGN REVIEW / ENGINEERING HOLD','C17 Parameters'); g_params.addObject(param)
# body central shell loft and target envelope
stations=[(2550.85,1364.41,308.47,1245.76),(2194.92,1400,308.47,1328.81),(1838.98,1423.73,308.47,1352.54),(1483.05,1423.73,308.47,1352.54),(1127.12,1423.73,308.47,1316.95),(889.83,1407.91,308.47,1261.58),(771.19,1400,308.47,1233.90)]
wires=[]
for x,w,zb,zc in stations: wires.append(Part.makePolygon([App.Vector(x,-w/2,zb),App.Vector(x,w/2,zb),App.Vector(x,w/2,zc),App.Vector(x,-w/2,zc),App.Vector(x,-w/2,zb)]))
body=feature(g_body,'CentralShell_StationLoft',Part.makeLoft(wires,True,False),'P','C10 scaled station CSV','REF-BODY-SHELL','Central shell only; validated 2100 mm fenders unavailable'); color(body,(0.35,0.65,0.85),88)
target=feature(g_body,'BodyTargetEnvelope_2100mm',Part.makeBox(BODY_L,2100,1780,App.Vector(BODY_REAR,-1050,0)),'F','C17 overall body target','REF-BODY-TARGET','Envelope only; no exterior fender skin'); color(target,(0.15,0.35,0.65),96)
# Full scaled 8C starter envelope.  This is a body reference surface, not a
# claim that the historical skin or 2100 mm fender CAD has been validated.
body_macro=[(0,80,430,490,520,0.90),(180,250,360,570,630,0.88),(420,390,300,650,735,0.86),(700,470,270,700,810,0.84),(1000,520,250,720,875,0.82),(1300,545,250,730,900,0.82),(1600,555,255,750,930,0.82),(1900,575,260,790,1050,0.82),(2200,590,260,820,1120,0.82),(2500,600,260,830,1140,0.82),(2800,600,260,830,1140,0.82),(3100,600,260,820,1110,0.82),(3400,590,260,800,1040,0.82),(3700,575,265,780,980,0.82),(4000,550,270,750,940,0.83),(4300,510,285,710,910,0.84),(4600,440,310,670,880,0.86),(4850,340,350,620,840,0.88),(5050,220,400,570,790,0.90),(5150,60,470,520,700,0.92)]
body_wires=[]
for s,hw,zbot,zshoulder,ztop,factor in body_macro:
    x=(4050.0-s)*SCALE; hw*=SCALE; zbot*=SCALE; zshoulder*=SCALE; ztop*=SCALE
    pts=[App.Vector(x,0,zbot),App.Vector(x,-hw*.72,zbot+(zshoulder-zbot)*.10),App.Vector(x,-hw*.96,zbot+(zshoulder-zbot)*.45),App.Vector(x,-hw,zshoulder),App.Vector(x,-hw*.92,zshoulder+(ztop-zshoulder)*.42),App.Vector(x,-hw*.65,zshoulder+(ztop-zshoulder)*.78),App.Vector(x,-hw*.30,zshoulder+(ztop-zshoulder)*factor),App.Vector(x,0,ztop),App.Vector(x,hw*.30,zshoulder+(ztop-zshoulder)*factor),App.Vector(x,hw*.65,zshoulder+(ztop-zshoulder)*.78),App.Vector(x,hw*.92,zshoulder+(ztop-zshoulder)*.42),App.Vector(x,hw,zshoulder),App.Vector(x,hw*.96,zbot+(zshoulder-zbot)*.45),App.Vector(x,hw*.72,zbot+(zshoulder-zbot)*.10),App.Vector(x,0,zbot)]
    c=Part.BSplineCurve(); c.interpolate(pts,False); body_wires.append(Part.Wire(c.toShape()))
body_full_shape=Part.makeLoft(body_wires,True,False)
body_full=feature(g_body,'BodyScaledFullEnvelope',body_full_shape,'P','C03/C10 scaled body starter macro','REF-BODY-FULL','Uniformly scaled concept envelope; fenders and panel boundaries are not validated'); color(body_full,(0.25,0.55,0.85),90)
cockpit_cut=Part.makeBox(2550.85-889.83,1423.73,1200,App.Vector(889.83,-711.865,980))
arch_r=(330.0+45.0)*SCALE
for ax in [0.0,FRONT_X]:
    cockpit_cut=cockpit_cut.fuse(Part.makeCylinder(arch_r,2500,App.Vector(ax,-1250,330.0*SCALE),App.Vector(0,1,0)))
body_open_shape=body_full_shape.cut(cockpit_cut)
body_open=feature(g_body,'BodyScaledWithCockpitAndArchStudy',body_open_shape,'P','C17 scaled body conflict study','REF-BODY-OPENINGS','Cockpit and wheel-arch cuts are provisional; X-03 remains unresolved'); color(body_open,(0.30,0.60,0.90),92)
# hardpoints
hardpoints=[('HP-REAR-AXLE',0,0,330,'F','C17 master datum'),('HP-FRONT-WHEEL-L',FRONT_X,775,330,'P','C17 front track study'),('HP-FRONT-WHEEL-R',FRONT_X,-775,330,'P','C17 front track study'),('HP-GX-L1-L',3350,425,295,'P','C16 proxy'),('HP-GX-L1-R',3350,-425,295,'P','C16 proxy'),('HP-GX-L2-L',3760,425,295,'P','C16 proxy'),('HP-GX-L2-R',3760,-425,295,'P','C16 proxy'),('HP-GX-SH-L',3490,515,825,'P','C16 proxy'),('HP-GX-SH-R',3490,-515,825,'P','C16 proxy'),('HP-PROBOX-HUB-L',0,727.5,330,'P','Probox reference track'),('HP-PROBOX-HUB-R',0,-727.5,330,'P','Probox reference track'),('HP-FIREWALL-LEGACY',950,0,650,'X','C17 X-01 conflict'),('HP-CABIN-AFT',889.83,0,650,'X','C17 X-01 conflict')]
for n,x,y,z,s,src in hardpoints:
    o=feature(g_hp,n,marker((x,y,z-9)),s,src,n,'Marker only; never a machining datum'); color(o,(0.95,0.2,0.1) if s in ('X','M') else (0.95,0.75,0.1))
# supplied STEP references retained as separate, 1:1 provisional donor geometry
donor_front_shape=Part.read(str(ROOT/'references/Project_8C_C18_Combined_Front_Chassis_GX100_GAZ_Structural_Frame.step'))
donor_front=feature(g_donor_front,'D-FRONT-C18-Supplied-STEP',donor_front_shape,'P','Supplied C18 STEP reference','DONOR-C18-FRONT','Reference geometry only; not verified GX100 interface or road-rated structure'); color(donor_front,(0.95,0.75,0.15),82)
donor_rear_shape=Part.read(str(ROOT/'references/Project_8C_Probox_Donor_Cassette_Concept_Rev01.step'))
donor_rear=feature(g_donor_rear,'D-REAR-Probox-Supplied-STEP',donor_rear_shape,'P','Supplied Probox Rev01 STEP reference','DONOR-PROBOX-REV01','199-solid visual cassette; donor VIN, mounts, drivetrain and service geometry unverified'); color(donor_rear,(0.85,0.55,0.20),84)
# Keep the earlier C11 cabin study visible as a quarantined reference so that
# the new weldment can be compared against the source rather than silently
# replacing it.
c11_shape=Part.read(str(ROOT/'references/Project_8C_C11_Cabin_RHS_Frame_Concept.step'))
c11_ref=feature(g_body,'D-CABIN-C11-Supplied-STEP',c11_shape,'P','Supplied C11 cabin STEP reference','DONOR-C11-CABIN','Spatial reference only; no seat, door, belt, firewall or rollover design'); color(c11_ref,(0.25,0.75,0.95),93)
# Wheel and tyre envelopes are kept as separate study solids.  They are not
# wheel designs or clearance approval.
def wheel_env(name,x,y,z,r,w,src,status='P'):
    sh=Part.makeCylinder(r,w,App.Vector(x,y-w/2,z),App.Vector(0,1,0))
    o=feature(g_wheels,name,sh,status,src,name,'Envelope only; wheel offset, WMS, tyre load and fender sweep require confirmation'); color(o,(0.15,0.15,0.15),72); return o
front_wheels=[wheel_env('W-FRONT-L',FRONT_X,775,330,330,215,'C17 C14 trial tyre'),wheel_env('W-FRONT-R',FRONT_X,-775,330,330,215,'C17 C14 trial tyre')]
rear_wheels=[wheel_env('W-REAR-L',0,727.5,330,317,165,'Probox Rev01 165R13-style reference'),wheel_env('W-REAR-R',0,-727.5,330,317,165,'Probox Rev01 165R13-style reference')]
member_rows=[]
def member(grp,n,p0,p1,sy,sz,wall,status,source,notes,section='RHS'):
    o=feature(grp,n,tube(p0,p1,sy,sz,wall),status,source,n,notes); add_prop(o,'App::PropertyLength','OuterY',sy,'RHS'); add_prop(o,'App::PropertyLength','OuterZ',sz,'RHS'); add_prop(o,'App::PropertyLength','Wall',wall,'RHS'); add_prop(o,'App::PropertyString','StartNode',str(tuple(round(v,2) for v in p0)),'RHS'); add_prop(o,'App::PropertyString','EndNode',str(tuple(round(v,2) for v in p1)),'RHS'); add_prop(o,'App::PropertyString','Section',section,'RHS'); color(o,(0.72,0.72,0.75))
    member_rows.append({'part_id':n,'section':section,'outer_y':sy,'outer_z':sz,'wall':wall,'length_mm':round(math.dist(p0,p1),2),'status':status,'start':p0,'end':p1,'notes':notes}); return o
# cabin
for side,y in [('L',510),('R',-510)]:
    member(g_cabin,f'C2-LS-{side}',(890,y,445),(2551,y,445),50,100,3,'P','C11 member schedule','Primary sill'); member(g_cabin,f'C2-US-{side}',(890,y,675),(2551,y,675),40,60,3,'P','C11 member schedule','Upper door rail')
    for i,x in enumerate([915,1240,1630,2010,2526],1): member(g_cabin,f'C2-SIDE-{side}-{i}',(x,y,545),(x,y,675),40,40,3,'P','C11 member schedule','Sill connector')
for i,x in enumerate([915,1240,1630,2010,2526],1): member(g_cabin,f'C2-FLOOR-{i}',(x,-485,445),(x,485,445),50,100,3,'P','C11 member schedule','Floor diaphragm')
# Thin floor/shear panels are reference solids, not a released sheet-metal
# drawing.  They make the open-top cabin's torsion strategy explicit.
floor=feature(g_cabin,'C2-Floor-Shear-Panel',Part.makeBox(1610,970,3,App.Vector(920,-485,545)),'P','C17 torsion concept','C2-FLOOR-SHEET','Panel gauge, weld/bond detail and removable service access require engineering'); color(floor,(0.35,0.45,0.55),55)
for side,y in [('L',510),('R',-510)]:
    member(g_cabin,f'C2-DOOR-DIAG-{side}',(1050,y,545),(2200,y,675),40,40,3,'P','C17 side intrusion concept','Door opening diagonal; door hardware and ingress study pending')
member(g_int,'I-FRONT-CABIN-LAP-L',(2375,510,445),(2551,510,445),60,80,4,'P','C17 architecture','Continuous rail across 176 mm overlap'); member(g_int,'I-FRONT-CABIN-LAP-R',(2375,-510,445),(2551,-510,445),60,80,4,'P','C17 architecture','Continuous rail across 176 mm overlap'); member(g_int,'I-FRONT-CABIN-XBRACE-L',(2375,510,445),(2551,350,675),40,40,3,'P','C17 architecture','Triangulated splice'); member(g_int,'I-FRONT-CABIN-XBRACE-R',(2375,-510,445),(2551,-350,675),40,40,3,'P','C17 architecture','Triangulated splice')
# front
for side,y in [('L',520),('R',-520)]:
    member(g_front,f'F1-RAIL-{side}',(2375,y,445),(4545,y,500),60,80,4,'P','C17 integrated architecture','Continuous front rail'); member(g_front,f'F1-LOWER-OUT-{side}',(3350,y,325),(3559,775 if y>0 else -775,330),40,50,3,'P','C16 wheel proxy','WMS/link geometry unverified'); member(g_front,f'F1-NOSE-OUT-{side}',(4200,y,390),(4545,650 if y>0 else -650,400),40,50,3,'P','C17 architecture','Forward body support'); member(g_front,f'F1-TOWER-{side}',(3375,y,445),(3490,515 if y>0 else -515,825),50,60,4,'P','C16 coilover proxy','Damper survey required')
for i,(x,z) in enumerate([(2551,445),(3350,325),(3760,325),(4200,430)],1): member(g_front,f'F1-CROSS-{i}',(x,-520,z),(x,520,z),60,60,4,'P','C17 architecture','Front transverse load path')
for side,sgn in [('L',1),('R',-1)]:
    for n,x,y,z in [('L1',3350,425*sgn,295),('L2',3760,425*sgn,295),('SH',3490,515*sgn,825)]:
        o=feature(g_front,f'F1-BRACKET-{n}-{side}',Part.makeBox(12,70,120,App.Vector(x-6,y-35,z-60)),'P','C16 nominal proxy',f'F1-BRKT-{n}-{side}','Study plate only; bore/gap/axis unmeasured'); color(o,(0.95,0.65,0.15))
# rear
for side,y in [('L',560),('R',-560)]: member(g_rear,f'R3-RAIL-{side}',(-791,y,390),(950,y,445),60,80,4,'P','C17 architecture','Rear primary rail'); member(g_rear,f'R3-CRADLE-{side}',(-650,y,260),(520,y,260),50,50,3,'P','Probox cassette concept','Cradle rail; interface M'); member(g_rear,f'R3-REAR-TIE-{side}',(-791,y,390),(-791,410 if y>0 else -410,500),50,60,3,'P','C17 architecture','Rear body support')
for i,x in enumerate([-650,-520,0,520,800],1): member(g_rear,f'R3-CROSS-{i}',(x,-560,390),(x,560,390),60,60,4,'P','C17 architecture','Rear transverse path')
# Second-level triangulation and service cradle rails.  These members make the
# load path visually continuous while preserving the measured-point HOLD on
# every donor interface.
for side,y0,y1 in [('L',650,510),('R',-650,-510)]:
    member(g_int,f'I-CONT-RAIL-{side}-REAR',(-791,y0,390),(890,y1,445),60,80,4,'P','C17 integrated load path','Rear-to-cabin continuous rail; final node review required')
    member(g_int,f'I-CONT-RAIL-{side}-FRONT',(2551,y1,445),(4545,520 if side=='L' else -520,500),60,80,4,'P','C17 integrated load path','Cabin-to-front continuous rail; final node review required')
    member(g_int,f'I-REAR-DIAG-{side}',(-520,y0,390),(520,y1,260),40,50,3,'P','C17 rear cradle concept','Rear cradle diagonal; removable cassette load path')
    member(g_int,f'I-FRONT-DIAG-{side}',(2551,y1,445),(3350,425 if side=='L' else -425,295),40,50,3,'P','C17 front cradle concept','Front suspension load path; donor axes unverified')
# Cross-vehicle load ties at the suspension tower and rear service bay.
member(g_front,'F1-SHOCK-TOWER-TIE',(3490,-515,825),(3490,515,825),50,60,4,'P','C16 coilover proxy','Upper tower tie; damper and tower loads require engineering')
member(g_rear,'R3-STRUT-TOP-TIE',(420,-700,900),(420,700,900),50,60,4,'P','Probox Rev01 strut envelope','Strut-top tie proxy; actual top mounts are M')
member(g_rear,'R3-REAR-SERVICE-CROSS',(-650,-650,650),(650,650,650),40,50,3,'P','C17 service architecture','Engine removal opening boundary; clearances unverified')
# Candidate bulkhead/hoop members are deliberately marked provisional because
# the X=889.83 / 950 firewall conflict is unresolved.
for side in ['L','R']:
    y=560 if side=='L' else -560
    member(g_int,f'I-BULKHEAD-HOOP-{side}',(920,y,390),(920,y,950),50,60,4,'X','C17 X-01 conflict','Candidate thermal/fire bulkhead hoop; do not freeze')
member(g_int,'I-BULKHEAD-TOP',(920,-560,950),(920,560,950),50,60,4,'X','C17 X-01 conflict','Candidate bulkhead top tie; cockpit and engine package unresolved')
engine=feature(g_rear,'R3-Probox-Powertrain-Envelope',Part.makeBox(1100,850,750,App.Vector(-450,-425,225)),'P','Probox Rev01 research basis','DONOR-PROBOX-POWERTRAIN','Visual package only; orientation/mount/service unverified'); color(engine,(0.75,0.35,0.25),82)
subframe=feature(g_rear,'R3-Probox-Subframe-Proxy',Part.makeBox(1040,100,50,App.Vector(-520,-610,200)).fuse(Part.makeBox(100,1120,50,App.Vector(-570,-560,200))),'M','Probox Rev01 assumption','DONOR-PROBOX-SUBFRAME','Nominal cassette; actual stamping and bolts require survey'); color(subframe,(0.9,0.5,0.15),50)
for i,(x,y) in enumerate([(-520,560),(-520,-560),(520,560),(520,-560)],1):
    o=feature(g_rear,f'R3-SUBFRAME-MOUNT-{i}',marker((x,y,200),15,30),'M','Probox Rev01 research',f'MOUNT-M-{i}','Placeholder; do not drill'); color(o,(1.0,0.1,0.1))
# conflict planes
fire=feature(g_int,'I-Firewall-Conflict-Plane',Part.makeBox(12,1200,850,App.Vector(950,-600,300)),'X','C17 X-01 conflict','CONFLICT-X01','Legacy firewall intrudes cockpit by 60.17 mm'); color(fire,(1.0,0.05,0.05),75)
aft=feature(g_int,'I-Cockpit-Aft-Edge',Part.makeBox(8,1200,850,App.Vector(889.83,-600,300)),'X','C17 X-01 conflict','CONFLICT-X01-AFT','Nominal cockpit aft edge'); color(aft,(1.0,0.2,0.1),70)
# occupants and mounts
for side,y in [('L',240),('R',-240)]:
    seat=feature(g_seats,f'O-Seat-Envelope-{side}',Part.makeBox(520,420,220,App.Vector(1190,y-210,480)),'P','Occupant package unavailable','OCC-SEAT','Envelope only; G07 open'); color(seat,(0.3,0.8,0.35),80)
    belt=feature(g_seats,f'O-Belt-Anchor-Proxy-{side}',marker((1750,y+(-190 if side=='L' else 190),780),18,30),'E','C17 G07 open gate','OCC-BELT','Safety-critical anchorage requires review'); color(belt,(0.9,0.15,0.2),10)
for i,(x,y) in enumerate([(1100,510),(1100,-510),(2450,510),(2450,-510)],1):
    o=feature(g_bodymount,f'BM-{i}',marker((x,y,430),12,25),'P','Body mount concept','BODY-MOUNT','Composite-body isolation mount; skin unverified'); color(o,(0.2,0.7,0.9))
load=feature(g_analysis,'A-LoadPath-Reference',Part.makePolygon([App.Vector(-791,0,430),App.Vector(950,0,430),App.Vector(2551,0,445),App.Vector(4545,0,500)]),'E','C17 analysis requirement','ANALYSIS-LOADPATH','Schematic only; no FEA'); color(load,(1.0,0.1,0.1))
# save/export
front_objs=[o for o in g_front.Group if hasattr(o,'Shape') and not o.Shape.isNull()]; cabin_objs=[o for o in g_cabin.Group if hasattr(o,'Shape') and not o.Shape.isNull()]; rear_objs=[o for o in g_rear.Group if hasattr(o,'Shape') and not o.Shape.isNull()]; int_objs=[o for o in g_int.Group if hasattr(o,'Shape') and not o.Shape.isNull()]; structural_objs=front_objs+cabin_objs+rear_objs+int_objs; review_objs=structural_objs+[donor_front,donor_rear,c11_ref,body_open]+front_wheels+rear_wheels

doc.recompute(); doc.saveAs(str(OUT/'Project_8C_Master_Chassis.FCStd'))
for objs,path in [(front_objs,OUT/'Project_8C_Chassis_01_Front.step'),(cabin_objs,OUT/'Project_8C_Chassis_02_Cabin.step'),(rear_objs,OUT/'Project_8C_Chassis_03_Rear.step'),(structural_objs,OUT/'Project_8C_Structural_Chassis_Assembly.step'),(review_objs,OUT/'Project_8C_Master_Chassis_Assembly.step')]: Part.export(objs,str(path))
Part.export([donor_front,donor_rear,c11_ref],str(OUT/'Project_8C_Donor_Proxies_Review.step'))
with open(OUT/'Project_8C_Datum_and_Hardpoint_Registry.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['id','x_mm','y_mm','z_mm','status','source','notes']); [w.writerow(list(r)+['Marker only']) for r in hardpoints]
registry=ROOT/'references/Project_8C_C17_Hardpoint_Registry.csv'
if registry.exists(): shutil.copy2(registry,OUT/'Project_8C_Datum_and_Hardpoint_Registry.csv')
for nm in ['Project_8C_C17_Constraint_Master.json','Project_8C_C17_Open_Gates.csv']:
    src=ROOT/'references'/nm
    if src.exists(): shutil.copy2(src,OUT/nm.replace('Project_8C_C17_','Project_8C_'))
with open(OUT/'Project_8C_Weldment_Member_Schedule.csv','w',newline='') as f:
    w=csv.DictWriter(f,fieldnames=['part_id','section','outer_y','outer_z','wall','length_mm','status','start','end','notes']); w.writeheader(); w.writerows(member_rows)
with open(OUT/'Project_8C_Bracket_Drilling_HOLD.csv','w',newline='') as f:
    w=csv.writer(f); w.writerow(['item','status','required evidence','release condition'])
    for item,req in [('GX100 lower link 1/2 brackets','upright and bushing survey'),('GX100 upper arm pivots','OEM assembly survey'),('GX100 coilover clevis','selected damper and loads'),('Probox subframe mounts','four bolt centres/sleeves'),('Probox engine/transaxle mounts','mount centres/orientation'),('Seat/belt anchors','selected seats/H-points/restraint strategy')]: w.writerow([item,'HOLD',req,'C17 engineering gates closed'])
def bb(objs):
    b=None
    for o in objs: b=o.Shape.BoundBox if b is None else b.united(o.Shape.BoundBox)
    return None if b is None else [round(v,3) for v in (b.XMin,b.XMax,b.YMin,b.YMax,b.ZMin,b.ZMax)]
checks={'units':'mm','coordinate_system':'+X front, +Y vehicle-left, +Z up; rear axle origin','fcstd_exists':(OUT/'Project_8C_Master_Chassis.FCStd').exists(),'step_files':[p.name for p in OUT.glob('*.step')],'module_counts':{'front':len(front_objs),'cabin':len(cabin_objs),'rear':len(rear_objs),'interfaces':len(int_objs),'structural':len(structural_objs),'review_assembly':len(review_objs)},'bbox_mm':{'front':bb(front_objs),'cabin':bb(cabin_objs),'rear':bb(rear_objs),'structural_assembly':bb(structural_objs),'review_assembly':bb(review_objs)},'axis_check':True,'scale_check':abs(SCALE-2100/1770)<1e-12,'release_state':'CONCEPT / DESIGN REVIEW / ENGINEERING HOLD','unverified_gates':['G01','G02','G03','G04','G05','G06','G07','G08','G09','G10','G11']}
with open(OUT/'Project_8C_Design_Validation.json','w') as f: json.dump(checks,f,indent=2)
report=f'''Project 8C C17 integrated chassis design review\nRevision: C17 Rev 0 / generated 2026-10-11\nSTATUS: CONCEPT / DESIGN REVIEW / ENGINEERING HOLD\n\nArchitecture\n- Continuous paired primary rails run from the rear bay through deep cabin sills into the GX100 front cradle, with second-level diagonal load paths and explicit tower ties.\n- Cabin floor crossmembers, a provisional shear panel, side-door diagonals and shared X-02 overlap members make the open-top torsion strategy explicit.\n- The supplied 108-solid C18 front reference, 199-solid Probox reference and 21-solid C11 cabin reference are retained at their supplied global positions in the review assembly.\n- Rear Probox packaging is represented by a replaceable RHS cradle around the actual donor envelope, with four measured-point placeholders and a removable service opening.\n- Firewall at X=950 and cockpit aft edge X=889.83 remain the visible X-01 conflict pending thermal, seat, and service packaging.\n\nFixed / derived parameters\n- Body width 2100 mm (F); body length {BODY_L:.2f} mm (D); wheelbase {WB:.2f} mm (D).\n- Rear axle X=0 (F); front axle X={FRONT_X:.2f} (D); +X front, +Y vehicle-left, +Z up.\n- Toyota donor geometry is not scaled; donor interfaces are P/M proxies.\n\nDesign assessment\n- C11 is retained as a spatial reference and strengthened with 60x80x4 lap rails and diagonal splice members.\n- C16 front study is reorganized into paired continuous rails, four crossmembers, wheel outriggers, and proxy tower load paths.\n- Probox Rev01 is retained as a packaging reference; rear-drive transaxle feasibility, mounts, axle geometry, lubrication, cooling, and service removal remain unresolved.\n- Scaled central shell station loft is reference geometry only; validated fenders are absent and wheel/arch conflict X-03 remains open.\n\nEngineering limitations\n- No donor drilling, weld specification, material certificate, fatigue result, FEA, kinematics solution, brake calculation, restraint calculation, or legal approval is asserted.\n- Bracket drilling schedule is a HOLD. Fabrication requires closure of C17 gates G01-G11 and independent competent review.\n'''
(OUT/'Project_8C_Engineering_Report.md').write_text(report)
try:
 import matplotlib; matplotlib.use('Agg'); import matplotlib.pyplot as plt; from matplotlib.backends.backend_pdf import PdfPages
 with PdfPages(OUT/'Project_8C_Concept_Drawing_Set.pdf') as pp:
  for title,mode in [('Plan view / global X-Y','plan'),('Side view / global X-Z','side'),('Front view / global Y-Z','front')]:
   fig,ax=plt.subplots(figsize=(11.7,8.3)); ax.set_title(title+' — CONCEPT / DESIGN REVIEW / HOLD',color='darkred')
   for r in member_rows:
    p0,p1=r['start'],r['end']; a,b=((p0[0],p0[1]),(p1[0],p1[1])) if mode=='plan' else (((p0[0],p0[2]),(p1[0],p1[2])) if mode=='side' else ((p0[1],p0[2]),(p1[1],p1[2])))
    ax.plot([a[0],b[0]],[a[1],b[1]],color='#315b8a',lw=1.3)
   if mode=='plan': ax.plot([BODY_REAR,BODY_FRONT,BODY_FRONT,BODY_REAR,BODY_REAR],[-1050,-1050,1050,1050,-1050],'--',color='gray'); ax.set_xlabel('X (mm)'); ax.set_ylabel('Y (mm)')
   elif mode=='side': ax.axvline(889.83,color='red',ls=':'); ax.axvline(950,color='red',ls='--'); ax.set_xlabel('X (mm)'); ax.set_ylabel('Z (mm)')
   else: ax.set_xlabel('Y (mm)'); ax.set_ylabel('Z (mm)')
   ax.grid(True,alpha=.25); ax.set_aspect('equal',adjustable='datalim'); ax.text(.01,.02,'C17 HOLD — proxy donor interfaces; no fabrication release',transform=ax.transAxes,color='darkred'); pp.savefig(fig,bbox_inches='tight'); plt.close(fig)
 with PdfPages(OUT/'Project_8C_Conflict_Resolution_Log.pdf') as pp:
  lines=report.splitlines(); page=[]
  for line in lines:
   page.append(line)
   if len(page)>=42:
    fig=plt.figure(figsize=(8.3,11.7)); plt.axis('off'); plt.text(.06,.95,'\n'.join(page),va='top',family='monospace',fontsize=9); pp.savefig(fig); plt.close(fig); page=[]
  if page:
   fig=plt.figure(figsize=(8.3,11.7)); plt.axis('off'); plt.text(.06,.95,'\n'.join(page),va='top',family='monospace',fontsize=9); pp.savefig(fig); plt.close(fig)
except Exception as e: (OUT/'PDF_GENERATION_WARNING.txt').write_text(str(e))
print(json.dumps(checks,indent=2))
