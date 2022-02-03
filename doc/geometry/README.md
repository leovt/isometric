# Geometry of the isometric map

## Orientation in assets and tiles on the map

The map grid axis align are west to east and south to north. The map can be viewed in four orientations, each view is named after the location of the camera.
The base view is `View_SW` where the camera is located in the south west. 
Therefore in this view North is in the top left, east in the top right, west in the bottom left and south in the bottom right of the screen.
The top line of the following graphics shows the naming convention for each orientation of the map grid.

![Orientations of views and assets](TileAndMapOrientation.png)

The assets (image files) are named after their orientation in the `View_SW`. The lower part of the image above shows a sloped tile. If it is oriented toward 
the west in the map coordinate system (top row `Slope_W`) and viewed from the north east (third column `View_NE`) the same asset is used as for a tile sloped 
east (third row `Slope_E`) and viewed from the south west (first column `View_SW`), namely the image `asset_E`.

## Alignment of Tile borders with Pixels

The theoretical tile borders (blue lines in the picture) are aligned with the corners of the pixels. In order to have a seamless joining of tiles, 
the pixels on both sides of the border need to be chosen consistently. Here the arrangement is demonstrated for 16x8 pixel base tiles and also for sloped tiles.
Note that the lines along the axis on the bottom form consistent 2:1 Pixel steps. Note also that the base tile is only 14 pixels wide, even though the theoretical 
tile is 16 pixels wide.

![Pixel Alignment](PixelAlignment.png)

This concept probably will have to be refined in oder to allow a smoother transition between different tiles (e.g. grass to dirt) or between tiles of
different slopes, and thus different lighting.

## Coordinate Systems

There are three coordinate systems used:

*  **The map (or world) coordinate system (e,n,z)** The origin of this coordinate system is in the south west corner (A) of the map, at the edge of the tile. 
   Coordinate e counts tiles to the east and coordinate n counts tiles to the north. The z coordinate is the height.
       
*  **The view (or camera) coordinate system (u,v,z)** The origin of this coordinate system is always at the corner of the map, which appears topmost on the screen (B).
   It is thus always the opposite corner from the camera position. In `View_SW` it is the NE corner.
   The u axis always extends towards the bottom left on the screen and the v axis towards the bottom right. The z axis is identical to the map coordinate system.
   
*  **The screen coordinate system (x,y)** The unit is pixels. As usual the x coordinate runs from the left to the right and y runs from top to bottom. 
   The value 0 corresponds to the left or top edge of the screen (or window). The center of the top left pixel thus has the coordinates (0.5px, 0.5px).

The image below illustrates the relationship of the coordinate systems in two different view orientations.

!(Coordinate Systems)[CoordinateSystems.png]

