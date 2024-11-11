# pixel2mai
This project takes the screen pixel and directly indexes a matrix to return a maimai zone (A1->E8). Made for [MajdataPlay](https://github.com/LingFeng-bbben/MajdataPlay) 
and [MychIO](https://github.com/istareatscreens/MychIO/issues/2) as a way to provide maimai zones from a mouse or touch screen device without any runtime calculations. 


Simply set the target size (usually the screen width in portrait mode) and the divs (resolution). Larger divs means it will take longer to calculate without much benefit 
since the finger is much larger than a single pixel. 


Notes:
- One zone per letter is hand-traced using images from [maipico](https://github.com/whowechina/mai_pico/blob/main/cad/maimai_touch%20v2.png)
- That one zone is rotated about the origin to generate all the zones (A1-A8, B1-B8, C1-C2, D1-D8, E1-E8)
- Uses matplotlib [contains_points](https://matplotlib.org/stable/api/path_api.html#matplotlib.path.Path.contains_points) to determine if point is inside polygon
- Exports the zoneMatrix for direct use in other applications (see 180to1080.h) with origin (0,0) in the top left corner


The app simulates a screen. You can mouse over the zones and the title of the graph will reflect the zone the mouse is hovered over (see testing.mp4)
