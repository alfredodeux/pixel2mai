from matplotlib.patches import Polygon
from matplotlib.patches import Rectangle
import matplotlib.pyplot as plt
import matplotlib.path as mplPath
import numpy as np

# target pixel size (size of the square play area)
target = 1080

# base pixel square width (must be divisible by screen size)
# higher = more resolution, lower = more lenient
# 100 seems a reasonable minimum
divs = 180

fileName = "%dto%d.h" % (divs,target)

# check that sizes are valid
if(target % divs != 0):
   print("ERROR: %d NOT divisible by %d" % (target, divs))
   quit()
else:
   print("Writing %s" % fileName)

factor = int(target/divs)
# show pixel lines
showDivs = False

# show chart
showChart = True

# copied enum from MychIO/Runtime/Device/TouchPanel/TouchPanelZone.cs
# A1=0, A2=1 ... E8=33, XX=34 (no zone)
XX=34 # no zone
zoneNames = ["A1","A2","A3","A4","A5","A6","A7","A8",
             "B1","B2","B3","B4","B5","B6","B7","B8",
             "C1","C2",
             "D1","D2","D3","D4","D5","D6","D7","D8",
             "E1","E2","E3","E4","E5","E6","E7","E8",
             "XX"]

# drawing is based on 1000x1000 pixel image
offset = np.array([1000,1000])

# export the zoneMatrix to file
def exportMatrix(M):
   # first expand matrix to target size
   Mtemp = M.repeat(factor,axis=0) # repeat along x
   zoneMatrix = Mtemp.repeat(factor,axis=1) # repeat along y

   # write matrix to file
   with open(fileName, 'w') as f:
      f.write("uint8_t zoneMatrix[%d][%d] = {" % (target, target))
      for y in range(0,target):
         f.write("{")
         for x in range(0,target):
            f.write("%d" % zoneMatrix[x][y])
            if(x != target-1): f.write(",")
         if(y != target-1): f.write("},\n")
         else: f.write("}};")
   print("DONE WRITING")

# rotate and scale from the first polygon
def createPts(pts):
   for x in range(1, len(pts)):
      angle = 2*np.pi*x/len(pts)
      pts[x] = rotatePts(pts[0],angle)
      # scale
      pts[x] = (pts[x]+offset)/(2.0*offset[0]/divs)
      if(x == len(pts)-1):
         pts[0] = (pts[0]+offset)/(2.0*offset[0]/divs)

# all polygons are simply rotated about center
def rotatePts(pts, th):
   M = np.array([[np.cos(th),-np.sin(th)],
                 [np.sin(th), np.cos(th)]])
   return np.dot(M,pts.T).T

fig, ax = plt.subplots(1,1)

# create zone arrays
Apts = np.zeros((8,7,2)) # 8 zones + 7pt polygon
Bpts = np.zeros((8,7,2)) # 8 zones + 7pt polygon
Cpts = np.zeros((2,6,2)) # 2 zones + 6pt polygon
Dpts = np.zeros((8,6,2)) # 8 zones + 6pt polygon
Epts = np.zeros((8,4,2)) # 8 zones + 4pt polygon

# draw each polygon point by point (doesn't need to be X1)
Apts[3] = np.array([(97,644), (149,986), (389,910), (595,800), (390,523), (290,523), (169,572)]) # A4
Apts[0] = rotatePts(Apts[3], -135*np.pi/180.0) # A1

Bpts[2] = np.array([(303,287), (454,287), (520,115), (418,12), (348,12), (257,103), (257,239)]) # B3
Bpts[0] = rotatePts(Bpts[2], -90*np.pi/180.0) # B1

Cpts[0] = np.array([(11,188), (80, 188), (190, 75), (190, -75), (80, -188), (11,-188)]) # C1

Dpts[2] = np.array([(742,0), (660, 80), (992, 121), (1000, 0), (992, -121), (660,-80)]) # D3
Dpts[0] = rotatePts(Dpts[2], -90*np.pi/180.0) # D1

Epts[3] = np.array([(308, 308), (506, 308), (506, 506), (308, 506)]) # E4
Epts[0] = rotatePts(Epts[3], -135*np.pi/180.0) # E1

# create polygons
createPts(Apts)
createPts(Bpts)
createPts(Cpts)
createPts(Dpts)
createPts(Epts)

# add polygons to graph in enum order
polygons = []
for x in range(0,len(Apts)): polygons.append(Apts[x])
for x in range(0,len(Bpts)): polygons.append(Bpts[x])
for x in range(0,len(Cpts)): polygons.append(Cpts[x])
for x in range(0,len(Dpts)): polygons.append(Dpts[x])
for x in range(0,len(Epts)): polygons.append(Epts[x])
for x in range(0,len(polygons)): ax.add_patch(Polygon(polygons[x]))

# zones stored as mplPath to perform polygon-inside-point calculation
zones = []
for x in range(0,len(polygons)): zones.append(mplPath.Path(polygons[x]))

# set the graph origin to top-left corner (standard)
plt.xlim(0,divs)
plt.ylim(divs,0)
ax.set_aspect('equal', adjustable='box')
plt.title("MOUSE OVER ZONES")

# draw divisor lines
if(showDivs):
   for x in range(0,divs):
      ax.add_patch(Rectangle([0,divs*x/divs],divs,0.001,angle=0,color="k"))
      ax.add_patch(Rectangle([divs*x/divs,0],divs,0.001,angle=90,color="k"))

# test by capturing mouse position and printing zone
def onMove(event):
    ix, iy = event.xdata, event.ydata
    if(ix != None and iy != None):
       idx1 = int(ix)
       idx2 = int(iy)
       plt.title(zoneNames[int(M[idx1][idx2])])
       plt.draw()

# perform zone.contains_points on each division and store the enum
pt = np.array([(0,0)])
M = np.zeros((divs,divs))
for x in range(0,divs):
   for y in range(0,divs):
      pt[0] = (x,y)
      # for each point, check if in a zone and record the zone number (A1=0, A2=1, etc)
      for z in range(0,len(zones)):
         if(zones[z].contains_points(pt)):
            M[x][y] = z
            break
         else: # set as 34 if not a valid zone
            M[x][y] = XX

# write the file
exportMatrix(M)

# setup the mouse test
cid = fig.canvas.mpl_connect('motion_notify_event', onMove)

if(showChart):
   plt.show()
