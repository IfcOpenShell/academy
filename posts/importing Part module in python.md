<!--
.. title: Importing Part module in ifcOpenShell-python
.. slug: Importing Part module in ifcOpenShell-python
.. date: 2021-11-10 12:20:00 UTC+05:30
.. tags: 
.. category: 
.. link: 
.. description: 
.. type: text
.. author: Devang Chauhan
-->

# Importing Part module from FreeCAD in python

I was looking for a way to extract BREP (Boundary representation) from IFC and I stumbled
upon [this](https://pythoncvc.net/?p=839) article. In the article, you'll see that
[Cyril](https://www.linkedin.com/in/cyril-waechter-5a5b6180/) uses the Part
module of [FreeCAD](https://www.freecadweb.org/index.php).
This post shows you how you can import the Part module in Python.
<!-- TEASER_END -->

## Step-1

Download FreeCAD from [here](https://github.com/FreeCAD/FreeCAD/releases) and
extract it to a location on your system. You are going to use the extracted directory
folder so choose such a location on your system where you can keep the extracted folder
long-term. I have saved the folder in the "D" drive of my machine.

## Step-2

Find the version of Python being used in FreeCAD. In the downloaded folder go to "bin",
and find python.exe.
![Location](/images/import_Part.png)
Double click on python.exe and observe the python version.
![version](/images/import_Part2.png)

## Step-3

Download and install the matching python version on your system.

## Step-4

Once installed, go to the folder named "site-packages" in your python installation and
create a file named "example.pth". The file name can be anything here.
![site-packages](/images/import_Part3.png)

## Step-5

Lastly, in the example.pth file, add paths to the folders "bin" and "lib" in the FreeCAD
folder you downloaded in Step-1.

After doing all the steps, you will be able to import the Part module in Python and would
be able to work with BREPs.

## Usage

```python
import FreeCAD
import Part
```