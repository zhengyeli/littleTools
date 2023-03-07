import matplotlib.pyplot as plt
from mpl_toolkits.axes_grid1 import host_subplot


class matplot:
    def __init__(self):
        # 鼠标左键拖拽事件
        self.lastx = 0  # 获取鼠标按下时的坐标X
        self.lasty = 0  # 获取鼠标按下时的坐标Y
        self.press = False

        self.figure = plt.figure()
        self.host = host_subplot(111)
        self.figure.canvas.mpl_connect("button_press_event", self.on_press)
        self.figure.canvas.mpl_connect("button_release_event", self.on_release)
        self.figure.canvas.mpl_connect("motion_notify_event", self.on_move)
        # 鼠标滚轮事件
        self.figure.canvas.mpl_connect('scroll_event', self.call_back)

    def example(self):
        par = self.host.twinx()

        self.host.set_xlabel("Distance")
        self.host.set_ylabel("Density")
        par.set_ylabel("Temperature")

        p1, = self.host.plot([0, 1, 2], [0, 1, 2], label="Density")
        p2, = par.plot([0, 1, 2], [0, 3, 2], label="Temperature")

        self.host.legend(labelcolor="linecolor")

        self.host.yaxis.get_label().set_color(p1.get_color())
        par.yaxis.get_label().set_color(p2.get_color())

        plt.show()
        plt

    # ================ 鼠标左键拖拽坐标 ================ #
    def on_press(self, event):
        if event.inaxes:  # 判断鼠标是否在axes内
            if event.button == 1:  # 判断按下的是否为鼠标左键1（右键是3）
                self.press = True
                self.lastx = event.xdata  # 获取鼠标按下时的坐标X
                self.lasty = event.ydata  # 获取鼠标按下时的坐标Y

    def on_move(self, event):
        axtemp = event.inaxes
        if axtemp:
            if self.press:  # 按下状态
                # 计算新的坐标原点并移动
                # 获取当前最新鼠标坐标与按下时坐标的差值
                x = event.xdata - self.lastx
                y = event.ydata - self.lasty
                # 获取当前原点和最大点的4个位置
                x_min, x_max = axtemp.get_xlim()
                y_min, y_max = axtemp.get_ylim()

                x_min = x_min - x
                x_max = x_max - x
                y_min = y_min - y
                y_max = y_max - y

                axtemp.set_xlim(x_min, x_max)
                axtemp.set_ylim(y_min, y_max)
                self.figure.canvas.draw_idle()  # 绘图动作实时反映在图像上

    def on_release(self, event):
        if self.press:
            self.press = False  # 鼠标松开，结束移动

    # ================ 鼠标滚轮放大缩小坐标 ================ #
    def call_back(self, event):
        axtemp = event.inaxes
        x_min, x_max = axtemp.get_xlim()
        y_min, y_max = axtemp.get_ylim()
        xfanwei = (x_max - x_min) / 10
        yfanwei = (y_max - y_min) / 10
        if event.button == 'up':
            axtemp.set(xlim=(x_min + xfanwei, x_max - xfanwei))
            # axtemp.set(ylim=(y_min + yfanwei, y_max - yfanwei))
        elif event.button == 'down':
            axtemp.set(xlim=(x_min - xfanwei, x_max + xfanwei))
            # axtemp.set(ylim=(y_min - yfanwei, y_max + yfanwei))
        self.figure.canvas.draw_idle()  # 绘图动作实时反映在图像上

    def plot(self, x, y):
        if len(x) == 0 or len(y) == 0:
            return
        if len(x) != len(y):
            print("len is not pair")
        else:
            self.host.set_xlabel("time")
            self.host.set_ylabel("Temperature")

            p1, = self.host.plot(x, y, label="Temperature")

            self.host.legend(labelcolor="linecolor")

            self.host.yaxis.get_label().set_color(p1.get_color())

            plt.show()


if __name__ == '__main__':
    m = matplot()
    m.example()

