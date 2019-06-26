#matplotlib inline
import matplotlib.pyplot as plt
import tilemapbase

tilemapbase.init(create=True)
my_office = (-1.554934, 53.804198)

degree_range = 0.003
extent = tilemapbase.Extent.from_lonlat(my_office[0] - degree_range, my_office[0] + degree_range,
                  my_office[1] - degree_range, my_office[1] + degree_range)
extent = extent.to_aspect(1.0)


#The path to plot

longs = [-1.554934, -1.555, -1.5552, -1.554]
lats = [53.804198, 53.80416, 53.8041, 53.8042]

# Convert to web mercator
path = [tilemapbase.project(x,y) for x,y in zip(longs, lats)]
for x,y in zip(longs, lats):
    print(x,y)
x, y = zip(*path)

fig, ax = plt.subplots(figsize=(10,10))

plotter = tilemapbase.Plotter(extent, tilemapbase.tiles.build_OSM(), width=600)
plotter.plot(ax)
ax.plot(x, y, "ro-")
fig.show()
input()

plotter.plot(plt.axes())
plt.plot(x,y, "ro-")
