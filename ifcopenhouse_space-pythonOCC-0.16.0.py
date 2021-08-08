import OCC.gp
import OCC.Geom

import OCC.Bnd
import OCC.BRepBndLib

import OCC.BRep
import OCC.BRepPrimAPI
import OCC.BRepAlgoAPI
import OCC.BRepBuilderAPI

import OCC.GProp
import OCC.BRepGProp

import OCC.TopoDS
import OCC.TopExp
import OCC.TopAbs

import ifcopenshell
import ifcopenshell.geom

# Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

# Initialize a graphical display window
occ_display = ifcopenshell.geom.utils.initialize_display()

# Open the IFC file using IfcOpenShell
ifc_file = ifcopenshell.open("IfcOpenHouse.ifc")

# Display the geometrical contents of the file using Python OpenCascade
products = ifc_file.by_type("IfcProduct")
for product in products:
    if product.is_a("IfcOpeningElement"): continue
    if product.Representation:
        shape = ifcopenshell.geom.create_shape(settings, product).geometry
        display_shape = ifcopenshell.geom.utils.display_shape(shape)
        if product.is_a("IfcPlate"):
            # Plates are the transparent parts of the window assembly
            # in the IfcOpenHouse model
            ifcopenshell.geom.utils.set_shape_transparency(display_shape, 0.8)
    
# Wait for user input and erase the display
raw_input()
occ_display.EraseAll()

# Get a list of all walls in the file
walls = ifc_file.by_type("IfcWall")

# Create a list of wall representation shapes
# and compute the bounding box of these shapes
wall_shapes = []
bbox = OCC.Bnd.Bnd_Box()
for wall in walls:
    shape = ifcopenshell.geom.create_shape(settings, wall).geometry
    
    wall_shapes.append((wall, shape))
    OCC.BRepBndLib.brepbndlib_Add(shape, bbox)    
    
    ifcopenshell.geom.utils.display_shape(shape)
    
# Calculate the center/average of the bounding box
bounding_box_center = ifcopenshell.geom.utils.get_bounding_box_center(bbox)
print "Bounding box center: %.2f %.2f %.2f" % (
    bounding_box_center.X(), 
    bounding_box_center.Y(),
    bounding_box_center.Z())

occ_display.DisplayMessage(bounding_box_center, "Center", update=True)

raw_input()
occ_display.EraseAll()

occ_display.DisplayMessage(bounding_box_center, "Center", update=True)

# Now create halfspace solids from the inner faces of the wall
halfspaces = []
for wall, shape in wall_shapes:
    exp = OCC.TopExp.TopExp_Explorer(shape, OCC.TopAbs.TopAbs_FACE)
    while exp.More():
        face = OCC.TopoDS.topods.Face(exp.Current())
        exp.Next()
        surf = OCC.BRep.BRep_Tool.Surface(face)
        obj = surf.GetObject()
        assert obj.DynamicType().GetObject().Name() == "Geom_Plane"
        
        plane = OCC.Geom.Handle_Geom_Plane.DownCast(surf).GetObject()
        
        if plane.Axis().Direction().Z() == 0:
            face_bbox = OCC.Bnd.Bnd_Box()
            OCC.BRepBndLib.brepbndlib_Add(face, face_bbox)
            face_center = ifcopenshell.geom.utils.get_bounding_box_center(face_bbox).XYZ()
            
            face_normal = plane.Axis().Direction().XYZ()
            face_towards_center = bounding_box_center.XYZ() - face_center
            face_towards_center.Normalize()
            
            dot = face_towards_center.Dot(face_normal)
            
            if dot < -0.8:
                
                ifcopenshell.geom.utils.display_shape(face)
                
                face_plane = plane.Pln()
                new_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(face_plane).Face()
                halfspace = OCC.BRepPrimAPI.BRepPrimAPI_MakeHalfSpace(new_face, bounding_box_center).Solid()
                halfspaces.append(halfspace)

raw_input()
occ_display.EraseAll()

# Create halfspace solids from the bottom faces of the roofs
roofs = ifc_file.by_type("IfcRoof")
for roof in roofs:
    shape = ifcopenshell.geom.create_shape(settings, roof).geometry
    
    exp = OCC.TopExp.TopExp_Explorer(shape, OCC.TopAbs.TopAbs_FACE)
    while exp.More():
        face = OCC.TopoDS.topods.Face(exp.Current())
        exp.Next()
        surf = OCC.BRep.BRep_Tool.Surface(face)
        plane = OCC.Geom.Handle_Geom_Plane.DownCast(surf).GetObject()
        
        assert obj.DynamicType().GetObject().Name() == "Geom_Plane"
        if plane.Axis().Direction().Z() > 0.7:
            face_plane = plane.Pln()
            new_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(face_plane).Face()
            halfspace = OCC.BRepPrimAPI.BRepPrimAPI_MakeHalfSpace(new_face, bounding_box_center).Solid()
            halfspaces.append(halfspace)
            
# Create an initial box from which to cut the halfspaces
common_shape = OCC.BRepPrimAPI.BRepPrimAPI_MakeBox(OCC.gp.gp_Pnt(-10, -10, 0), OCC.gp.gp_Pnt(10, 10, 10)).Solid()
for halfspace in halfspaces:
    common_shape = OCC.BRepAlgoAPI.BRepAlgoAPI_Common(common_shape, halfspace).Shape()

ifcopenshell.geom.utils.display_shape(common_shape)

# Calculate the volume properties of the resulting space shape
props = OCC.GProp.GProp_GProps()
OCC.BRepGProp.brepgprop_VolumeProperties(shape, props)
print "Space volume: %.3f cubic meter" % props.Mass()

# Enter the main loop so that the user can navigate
ifcopenshell.geom.utils.main_loop()
