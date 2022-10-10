from time import perf_counter

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QTimer


# 描绘静态数据
class BasicArrayPlot:
    def __init__(self, widget):
        self.plot = None
        self.app = pg.mkQApp("Plotting Example")

        # Enable antialiasing for prettier plots
        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'b')
        pg.setConfigOption('foreground', 'k')

        self.win = pg.GraphicsLayoutWidget(widget, show=True, title="Basic plotting examples")
        self.win.resize(1000, 600)
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        self.win.setBackground('w')

        if widget is not None:
            widget.layout().addWidget(self.win)

        # np.random.normal(size=100)
        self.setData([1, 2, 3, 4])
        self.setData([1, 1, 13, 1])

    def setData(self, ylist):
        self.win.clear()
        self.plot = self.win.addPlot(title="Basic array plotting", y=ylist, pen=(0, 0, 0))


class dynamicArrayPlot:
    def __init__(self, widget):
        self.win = pg.GraphicsLayoutWidget(widget, show=True, title="Basic plotting examples")
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        self.win.setBackground('w')

        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'b')
        pg.setConfigOption('foreground', 'k')
        if widget is not None:
            widget.layout().addWidget(self.win)

        # 3) Plot in chunks, adding one new plot curve for every 100 samples
        self.chunkSize = 100
        # Remove chunks after we have 10
        self.maxChunks = 20
        self.startTime = perf_counter()
        # win.nextRow()
        self.p5 = self.win.addPlot(colspan=2, pen=(0, 0, 0))
        self.p5.setLabel('bottom', 'Time', 's')
        self.p5.setXRange(-10, 0)

        self.curves = []
        self.data5 = np.empty((self.chunkSize + 1, 2))
        self.ptr5 = 0

    def update_plot(self, point=None):
        if point is None:
            point = np.random.normal()

        now = perf_counter()
        for c in self.curves:
            c.setPos(-(now - self.startTime), 0)

        i = self.ptr5 % self.chunkSize
        if i == 0:
            curve = self.p5.plot()
            self.curves.append(curve)
            last = self.data5[-1]
            self.data5 = np.empty((self.chunkSize + 1, 2))
            self.data5[0] = last
            while len(self.curves) > self.maxChunks:
                c = self.curves.pop(0)
                self.p5.removeItem(c)
        else:
            curve = self.curves[-1]
        self.data5[i + 1, 0] = now - self.startTime
        self.data5[i + 1, 1] = point  # np.random.normal()
        curve.setData(x=self.data5[:i + 2, 0], y=self.data5[:i + 2, 1], pen=(0, 0, 0))
        self.ptr5 += 1


if __name__ == '__main__':
    # pyqtgraph.examples.run()

    app = pg.mkQApp("Plotting Example")
    plot = dynamicArrayPlot(None)
    timer = QTimer()
    timer.timeout.connect(plot.update_plot)
    timer.start(50)
    pg.exec()



