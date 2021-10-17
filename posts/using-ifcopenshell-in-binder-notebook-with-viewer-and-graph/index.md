<!--
.. title: Using IfcOpenshell in Binder Notebooks with web-viewer and graph visualization
.. slug: using-ifcopenshell-in-binder-notebook-with-viewer-and-graph
.. date: 2021-10-17 13:45:29 UTC+02:00
.. tags: Jupyter, binder, university
.. category: 
.. link: 
.. description: 
.. type: text
.. author: Jakob Beetz 
-->


As an early release (still a little rough around the edges), [this repo](https://github.com/jakob-beetz/ifcopenshell-notebooks) has been created to allow students to get familiar with ifcopenshell without any knowledge. Its zero-setup running Jupyter-notebooks on binder.

to launch now click this: [![Binder](https://mybinder.org/badge_logo.svg)](https://mybinder.org/v2/gh/jakob-beetz/ifcopenshell-binder/main?urlpath=git-pull%3Frepo%3Dhttps%253A%252F%252Fgithub.com%252Fjakob-beetz%252Fifcopenshell-notebooks%26urlpath%3Dlab%252Ftree%252Fifcopenshell-notebooks%252F00_introduction.ipynb%26branch%3Dmain)

Some of the **features** are:
![Interactive viewer](/images/screenshot-ifc-notebook.png) 

- a viewer adapted from OCCJupyterViewer added with 

  - two-directional-selection viewer <-> model
  - section sliders for sections
  - attribute value lister
  - set and get colors
		
- graph visualization of the scene graph
![Graph viewer](/images/ifc-graph-plot.png)

- integrated IFC documentation 
![Doc in help](/images/ifchelp-example-ifcdoor.png)


There are many more examples, quizzes and task in the German version that is part of a mandatory 4th term class for 250 architecture students at the [RWTH Aachen](https://dc.rwth-aachen.de/de) that will be migrated over time. 
We are very open and happy about suggestions, issues, PRs and feedback!

TODOs:

- more explantory text
- English verion of slides with [RISE](https://rise.readthedocs.io/en/stable/index.html) to be used in lectures
- move viewer to SideCar (was not possible in the RWTH-Jupyter-Cluster yet)

I will be applying for some more funding to extend this into a good Open Educational Resource (OER) book from provincial sources in NRW/Germany, very open for collaboration ... 
