# Gryphon 3D Engine Library Mesh2String for Blender 2.7.x #
*It may work on Blender 2.6.x too but didn't tested!*

Latest version: **1.0**

## Description ##

This is a blender add-on to easily allow exporting object data into strings that can be used in the 3D engine for rendering.

The library for the pico-8 can be found [here](http://www.lexaloffle.com/bbs/?tid=28077).

## How to install it ##

Open `File > User preferences...` in Blender and select `Add-ons` tab.

Click `Install from File...` at the bottom and choose **EGryphon3DLibPanel.zip** file.

Under `Pico-8` category (or search `gryphon`) locate `Pico-8: Gryphon 3D Engine Library Mesh2String` and click the check-box near the name to activate it.

Click `Save User Settings` so you don't have to redo all this the next time you boot Blender.

## How to use it ##

On `Properties editor`, select `Objects` and scroll down to the very bottom, you'll find the **Gryphon 3D Engine Library** panel, if you can't find it please make sure you installed it correctly and have a supported blender version.

Click `Enable add-on` to activate the conversion, the panel will be expanded further so scroll down.

By default it will update and apply tranformations automatically so you can copy faces and vertices data right away.

## Limitations ##

Engine library importer have a limitation of 255 maximum vertices, this is due to each face index being 8-bits (2 characters).

Engine library doesn't import color information so the add-on ignores vertex colors for now.

## History ##

v1.0: Initial release.
