import os

import OCC.gp
import OCC.Geom
import OCC.Utils
import OCC.Bnd
import OCC.BRepBndLib
import OCC.BRep
import OCC.BRepPrimAPI
import OCC.BRepAlgoAPI
import OCC.BRepBuilderAPI
import OCC.BRepAlgo
import OCC.TopOpeBRepTool
import OCC.ShapeExtend
import OCC.GProp
import OCC.BRepGProp
import OCC.GC
import OCC.ShapeAnalysis
import OCC.TopTools

from OCC.TopoDS import TopoDS

import ifcopenshell
import ifcopenshell.geom


# Specify to return pythonOCC shapes from ifcopenshell.geom.create_shape()
settings = ifcopenshell.geom.settings()
settings.set(settings.USE_PYTHON_OPENCASCADE, True)

# Initialize a graphical display window
occ_display = ifcopenshell.geom.utils.initialize_display()
occ_display.View.SetBackgroundImage("white_bg.bmp")

# Open the IFC file using IfcOpenShell
ifc_file = ifcopenshell.open(os.path.join(os.path.dirname(__file__), "IfcOpenHouse.ifc"))

# The geometric elements in an IFC file are the IfcProduct elements. So these are 
# opened and displayed.
products = ifc_file.by_type("IfcProduct")
product_shapes = []

# For every product a shape is created if the shape has a Representation.
for product in products:
    if product.is_a("IfcOpeningElement") or product.is_a("IfcSite"): continue
    if product.Representation is not None:
        shape = ifcopenshell.geom.create_shape(settings, product).geometry
        product_shapes.append((product, shape))


# Two list are initialized to calculate the surface area to be printed.
surface_areas_per_section = []
surface_areas_per_building = []

# In this part the sections are created. You can enter the starting height, the 
# maximum height and the height difference between each section.
starting_height = 0
maximum_height = 1.5
height_step = 0.5

section_height = starting_height
while section_height <= maximum_height:
    print "Section height          =", section_height
    
    # A horizontal plane is created from which a face is constructed to intersect with 
    # the building. The face is transparently displayed along with the building.    
    section_plane = OCC.gp.gp_Pln(
        OCC.gp.gp_Pnt(0, 0, section_height),
        OCC.gp.gp_Dir(0, 0, 1)
    )
    section_face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(section_plane, -10, 10, -10, 10).Face()
    
    section_face_display = ifcopenshell.geom.utils.display_shape(section_face)
    ifcopenshell.geom.utils.set_shape_transparency(section_face_display, 0.5)
    for shape in product_shapes: ifcopenshell.geom.utils.display_shape(shape[1])
    
    raw_input()
    occ_display.EraseAll()
    
    # The surface area per section list is emptied every iteration
    surface_areas_per_section = []
    
    # Each product of the building is intersected with the horizontal face
    for product, shape in product_shapes:
        section = OCC.BRepAlgoAPI.BRepAlgoAPI_Section(section_face, shape).Shape()
        
        # The edges of the intersection are stored in a list
        section_edges = list(OCC.Utils.Topo(section).edges())    
        
        # If the length of the section_edges list is greater than 0 there is an 
        # intersection between the plane (at current height) and the product. Only in that 
        # case the product needs to be printed. 
        if len(section_edges) > 0:
            print "    {:<20}: {}".format(product.is_a(), product.Name)
            
            # Open Cascade has a function to turn loose unconnected edges into a list of 
            # connected wires. This function takes handles (pointers) to Open Cascade's native 
            # sequence type. Hence, two sequences and handles, one for the input, one for the 
            # output, are created. 
            edges = OCC.TopTools.TopTools_HSequenceOfShape()
            edges_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(edges)
            
            wires = OCC.TopTools.TopTools_HSequenceOfShape()
            wires_handle = OCC.TopTools.Handle_TopTools_HSequenceOfShape(wires)
            
            # The edges are copied to the sequence
            for edge in section_edges: edges.Append(edge)
                        
            # A wire is formed by connecting the edges
            OCC.ShapeAnalysis.ShapeAnalysis_FreeBounds.ConnectEdgesToWires(edges_handle, 1e-5, True, wires_handle)
            wires = wires_handle.GetObject()
                
            # From each wire a face is created
            print "        number of faces = %d" % wires.Length()
            for i in range(wires.Length()):
                wire_shape = wires.Value(i+1)
                wire = TopoDS.wire(wire_shape)
                face = OCC.BRepBuilderAPI.BRepBuilderAPI_MakeFace(wire).Face()
                
                # The wires and the faces are displayed
                ifcopenshell.geom.utils.display_shape(wire)
                face_display = ifcopenshell.geom.utils.display_shape(face)
                ifcopenshell.geom.utils.set_shape_transparency(face_display, 0.5)
                
                # Data about the wire is created to calculate the area
                wire_data = OCC.ShapeExtend.ShapeExtend_WireData(wire, True, True)
                wire_data_handle = OCC.ShapeExtend.Handle_ShapeExtend_WireData(wire_data)
                
                # The surface area of the face is calculated and appended to the list
                surface_area = abs(OCC.ShapeAnalysis.ShapeAnalysis_TotCross2D(wire_data_handle, face))
                print "        surface area    =", surface_area
                surface_areas_per_section.append(surface_area)
    
    # the sum of this list is the area that needs to be printed for the current section
    print "    Total section area  =", sum(surface_areas_per_section)
    print
    
    raw_input()
    occ_display.EraseAll()
    
    # The sections surface area is added to the list and the value of height_step is 
    # added to section_height to continue to the next section 
    surface_areas_per_building.append(sum(surface_areas_per_section))
    section_height += height_step
    
# After completing all the sections the total area that needs to be printed is calculated
print "Total building section areas =", sum(surface_areas_per_building)
