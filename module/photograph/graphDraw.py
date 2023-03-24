from time import perf_counter

import numpy as np
import pyqtgraph as pg
from PyQt6.QtCore import QTimer


# 描绘静态数据
from PyQt6.QtWidgets import QWidget, QGridLayout


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
        self.setData([0.00, 0.86, 1.59, 2.10, 2.35, 2.35, 2.18, 1.94, 1.76, 1.73, 1.90, 2.26, 2.75,
                      3.24, 3.63, 3.80, 3.70, 3.30, 2.68, 1.93, 1.18, 0.54, 0.11, -0.10, -0.11,
                      0.00, 0.11, 0.10, -0.11, -0.54, -1.18, -1.93, -2.68, -3.30, -3.70, -3.80,
                      -3.63, -3.24, -2.75, -2.26, -1.90, -1.73, -1.76, -1.94, -2.18, -2.35, -2.35,
                      -2.10, -1.59, -0.86, 0.00, 0.86, 1.59, 2.10, 2.35, 2.35, 2.18, 1.94, 1.76,
                      1.73, 1.90, 2.26, 2.75, 3.24, 3.63, 3.80, 3.70, 3.30, 2.68, 1.93, 1.18,
                      0.54, 0.11, -0.10, -0.11, 0.00, 0.11, 0.10, -0.11, -0.54, -1.18, -1.93,
                      -2.68, -3.30, -3.70, -3.80, -3.63, -3.24, -2.75, -2.26, -1.90, -1.73,
                      -1.76, -1.94, -2.18, -2.35, -2.35, -2.10, -1.59, -0.86, 0.00, 0.86, 1.59,
                      2.10, 2.35, 2.35, 2.18, 1.94, 1.76, 1.73, 1.90, 2.26, 2.75, 3.24, 3.63,
                      3.80, 3.70, 3.30, 2.68, 1.93, 1.18, 0.54, 0.11, -0.10, -0.11, 0.00, 0.11,
                      0.10, -0.11, -0.54, -1.18, -1.93, -2.68, -3.30, -3.70, -3.80, -3.63, -3.24,
                      -2.75, -2.26, -1.90, -1.73, -1.76, -1.94, -2.18, -2.35, -2.35, -2.10, -1.59,
                      -0.86, 0.00, 0.86, 1.59, 2.10, 2.35, 2.35, 2.18, 1.94, 1.76, 1.73, 1.90, 2.26,
                      2.75, 3.24, 3.63, 3.80, 3.70, 3.30, 2.68, 1.93, 1.18, 0.54, 0.11, -0.10, -0.11,
                      0.00, 0.11, 0.10, -0.11, -0.54, -1.18, -1.93, -2.68, -3.30, -3.70, -3.80, -3.63,
                      -3.24, -2.75, -2.26, -1.90, -1.73, -1.76, -1.94, -2.18, -2.35, -2.35, -2.10, -1.59,
                      -0.86, 0.00, 0.86, 1.59, 2.10, 2.35, 2.35, 2.18, 1.94, 1.76, 1.73, 1.90, 2.26, 2.75,
                      3.24, 3.63, 3.80, 3.70, 3.30, 2.68, 1.93, 1.18, 0.54, 0.11, -0.10, -0.11, 0.00, 0.11,
                      0.10, -0.11, -0.54, -1.18, -1.93, -2.68, -3.30, -3.70, -3.80, -3.63, -3.24, -2.75,
                      -2.26, -1.90, -1.73, -1.76, -1.94, -2.18, -2.35, -2.35, -2.10, -1.59, -0.86, 0.00])
        self.addData(
            [0.000000, 0.172730, 0.457387, 0.787303, 1.101169, 1.351995, 1.518298, 1.602997, 1.634530, 1.653705,
             1.703173, 1.815011, 2.002803, 2.251292, 2.528203, 2.783642, 2.967691, 3.034435, 2.963247, 2.755721,
             2.439240, 2.057780, 1.666571, 1.311757, 1.026199, 0.820089, 0.677468, 0.561485, 0.426618, 0.232474,
             -0.051219, -0.428570, -0.880767, -1.366666, -1.835313, -2.229918, -2.511123, -2.657516, -2.676092,
             -2.592520, -2.453428, -2.308129, -2.198038, -2.146211, -2.152998, -2.192565, -2.224186, -2.199243,
             -2.076878, -1.832469, -1.464420, -0.997564, -0.477855, 0.039904, 0.503883, 0.874673, 1.136846, 1.298159,
             1.390919, 1.459023, 1.547593, 1.690679, 1.903442, 2.171888, 2.464748, 2.732931, 2.927166, 3.002049,
             2.937366, 2.735038, 2.422711, 2.044571, 1.656015, 1.303322, 1.019458, 0.814701, 0.673163, 0.558044,
             0.423868, 0.230277, -0.052976, -0.429973, -0.881888, -1.367563, -1.836029, -2.230490, -2.511580, -2.657882,
             -2.676384, -2.592754, -2.453615, -2.308278, -2.198157, -2.146307, -2.153074, -2.192626, -2.224235,
             -2.199282, -2.076909, -1.832494, -1.464440, -0.997580, -0.477868, 0.039894, 0.503875, 0.874667, 1.136841,
             1.298155, 1.390916, 1.459020, 1.547590, 1.690677, 1.903440, 2.171886, 2.464746, 2.732930, 2.927165,
             3.002048, 2.937365, 2.735037, 2.422710, 2.044570, 1.656015, 1.303321, 1.019458, 0.814701, 0.673163,
             0.558044, 0.423868, 0.230277, -0.052976, -0.429973, -0.881888, -1.367563, -1.836029, -2.230490, -2.511580,
             -2.657882, -2.676384, -2.592754, -2.453615, -2.308278, -2.198157, -2.146307, -2.153074, -2.192626,
             -2.224235, -2.199282, -2.076909, -1.832494, -1.464440, -0.997580, -0.477868, 0.039894, 0.503875, 0.874667,
             1.136841, 1.298155, 1.390916, 1.459020, 1.547590, 1.690677, 1.903440, 2.171886, 2.464746, 2.732930,
             2.927165, 3.002048, 2.937365, 2.735037, 2.422710, 2.044570, 1.656015, 1.303321, 1.019458, 0.814701,
             0.673163, 0.558044, 0.423868, 0.230277, -0.052976, -0.429973, -0.881888, -1.367563, -1.836029, -2.230490,
             -2.511580, -2.657882, -2.676384, -2.592754, -2.453615, -2.308278, -2.198157, -2.146307, -2.153074,
             -2.192626, -2.224235, -2.199282, -2.076909, -1.832494, -1.464440, -0.997580, -0.477868, 0.039894, 0.503875,
             0.874667, 1.136841, 1.298155, 1.390916, 1.459020, 1.547590, 1.690677, 1.903440, 2.171886, 2.464746,
             2.732930, 2.927165, 3.002048, 2.937365, 2.735037, 2.422710, 2.044570, 1.656015, 1.303321, 1.019458,
             0.814701, 0.673163, 0.558044, 0.423868, 0.230277, -0.052976, -0.429973, -0.881888, -1.367563, -1.836029,
             -2.230490, -2.511580, -2.657882, -2.676384, -2.592754, -2.453615, -2.308278, -2.198157, -2.146307,
             -2.153074, -2.192626, -2.224235, -2.1],
            0, 0, 255)

    def setData(self, ylist):
        self.win.clear()
        self.plot = self.win.addPlot(title="Basic array plotting", y=ylist, pen=(255, 0, 0))

    def addData(self, ylist, r, g, b):
        # self.win.clear()
        self.plot.plot(y=ylist, pen=(r, g, b))


class dynamicArrayPlot:
    def __init__(self, widget):

        self.win = pg.GraphicsLayoutWidget(widget, show=True, title="Basic plotting examples")
        self.win.setWindowTitle('pyqtgraph example: Plotting')
        self.win.setBackground('w')

        pg.setConfigOptions(antialias=True)
        pg.setConfigOption('background', 'b')
        pg.setConfigOption('foreground', 'k')
        if widget.layout() is not None:
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

    def update_point_plot(self, point=None):
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
        # curve.setData(x=self.data5[:i + 2, 0], y=self.data5[:i + 2, 1], pen=pg.mkPen(None), symbol='o', symbolSize=5)
        self.ptr5 += 1


if __name__ == '__main__':
    # pyqtgraph.examples.run()

    app = pg.mkQApp("Plotting Example")
    plot = dynamicArrayPlot(None)
    timer = QTimer()
    timer.timeout.connect(plot.update_plot)
    timer.start(50)
    pg.exec()
