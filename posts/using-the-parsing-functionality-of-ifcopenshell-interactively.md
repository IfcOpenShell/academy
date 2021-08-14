<!--
.. title: Using the parsing functionality of IfcOpenShell interactively
.. slug: using-the-parsing-functionality-of-ifcopenshell-interactively
.. date: 2015-02-26 12:17:00 UTC+02:00
.. tags: IfcOpenShell, python
.. category: 
.. link: 
.. description: 
.. type: text
.. author: Thomas Krijnen
-->

In this recipe we are going to look at an interactive way of working with Python and IfcOpenShell that allows to quickly explore the possibilities offered by the tools. When the python interpreter (python.exe) is executed without arguments it will function as a REPL (a Read Evaluate Print Loop). It enables the user to type a single line of code and immediately see the evaluated result. An example of such a session is provided below. It outlines the procedure of starting with an IfcProject and descending down to the unit for angular measures. In this particular file it seems that angles are specified as degrees, a constant factor of 0.0174533 away from radians.

```python
Python 2.7.8 (default, Jun 30 2014, 16:03:49) [MSC v.1500 32 bit (Intel)] on win32
Type "help", "copyright", "credits" or "license" for more information.
>>> import ifcopenshell
>>> file = ifcopenshell.open("IfcOpenHouse.ifc")
>>> project = file.by_type("IfcProject")[0]
>>> project
#18=IfcProject('2f0veX5Vj59AhEg6WqGnhO',#5,'IfcOpenHouse',$,$,$,$,(#11),#17)
>>> project.is_a()
'IfcProject'
>>> project.is_a("IfcRoot")
True
>>> project.is_a("IfcWall")
False
>>> project.id()
18
>>> project.attribute_name(0)
'GlobalId'
>>> project.attribute_type(0)
'STRING'
>>> project.GlobalId
'2f0veX5Vj59AhEg6WqGnhO'
>>> project.Bier
Traceback (most recent call last):
  File "", line 1, in 
  File "ifcopenshell\\ifcopenshell.py", line 28, in __getattr__
    except: raise AttributeError("entity instance of type '%s' has no attribute '%s'"%(self.wrapped_data.is_a(), name))
AttributeError: entity instance of type 'IfcProject' has no attribute 'Bier'
>>> project.UnitsInContext
#17=IfcUnitAssignment((#13,#16))
>>> units = project.UnitsInContext.Units
>>> angle_unit = filter(lambda u: u.UnitType == "PLANEANGLEUNIT", units)[0]
>>> angle_unit
#16=IfcConversionBasedUnit(#12,.PLANEANGLEUNIT.,'Degrees',#15)
>>> angle_unit.ConversionFactor
#15=IfcMeasureWithUnit(IfcPlaneAngleMeasure(0.0174533),#14)
>>> angle_unit.ConversionFactor.ValueComponent
IfcPlaneAngleMeasure(0.0174533)
>>> angle_unit.ConversionFactor.ValueComponent.is_a()
'IfcPlaneAngleMeasure'
>>> angle_unit.ConversionFactor.ValueComponent.wrappedValue
0.0174533
```