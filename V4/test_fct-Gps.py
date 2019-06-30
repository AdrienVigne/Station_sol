import tilemapbase
import numpy as np
import matplotlib.pyplot as plt



tilemapbase.init(create=True)



centre0  = (-1.7545,48.045)
marge = 0.0005

theta = np.linspace(np.pi/2,3*np.pi/2,20)
#theta = - theta
angle_aller = (20/180)*np.pi
rayon = 20

rayon_terre = 6378137

x_t = rayon * np.cos(theta)
y_t = rayon * np.sin(theta) * np.sin(angle_aller)
z_t = rayon * np.sin(theta) * np.cos(angle_aller)

print (x_t,y_t,z_t)

centre = (centre0[0]*np.pi/180,centre0[1]*np.pi/180)

x0 = rayon_terre * np.cos(centre[0]) * np.cos(centre[1])
y0 = rayon_terre * np.cos(centre[0]) * np.sin(centre[1])
z0 = rayon_terre * np.sin(centre[0])
print("home")
print(x0,y0,z0)

rho0 = np.sqrt((x0**2)+(y0**2)+(z0**2))

phi0 = np.arccos(z0/rho0)*180/np.pi
theta0 = np.arctan(y0/x0)*180/np.pi

if phi0 > 90:
    phi0=90-phi0


print(rho0,phi0,theta0)

X = [x0+X for X in x_t]
Y = [y0+Y for Y in y_t]
Z = [z0+Z for Z in z_t]
phi=[]
theta=[]
print(len(X))
for i in range(len(X)):
    rho =np.sqrt( (X[i]**2)+(Y[i]**2)+(Z[i]**2))
    phi_temp = np.arccos(Z[i]/rho)*180/np.pi
    if phi_temp > 90 :
        phi_temp = 90 -phi_temp
    phi.append(phi_temp)

    theta.append(np.arctan(Y[i]/X[i])*180/np.pi)
print(theta,phi)

path = [tilemapbase.project(x,y) for x,y in zip(phi,theta)]
x, y = zip(*path)
#print(np.mean(x))
centre=(np.mean(phi),np.mean(theta))
extent = tilemapbase.Extent.from_lonlat(centre[0] - marge, centre[0] + marge,centre[1] - marge, centre[1] + marge)
extent = extent.to_aspect(1.0)
fig, ax = plt.subplots(figsize=(8, 8), dpi=100)
ax.xaxis.set_visible(False)
ax.yaxis.set_visible(False)

plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)
plotter.plot(ax, tilemapbase.tiles.build_OSM())

x0,y0 = tilemapbase.project(*centre0)

print(x,y)
ax.plot(x,y,'ro-')
ax.plot(x0,y0,'b>')

#plt.plot([0.495108],[0.347409],'ro')


ax.axis("off")


fig.show()
input()
