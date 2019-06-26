import pyqtgraph as pg
import numpy as np
x = np.random.normal(size=1000)
y = np.random.normal(size=1000)
graph=pg.plot(x, y, pen=None, symbol='o') ## setting pen=None disables line drawing
