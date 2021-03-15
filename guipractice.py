import sys
from PyQt5.QtWidgets import *
from PyQt5 import uic

from matplotlib.backends.backend_qt5agg import (NavigationToolbar2QT as NavigationToolbar)
import matplotlib.animation as animation
import numpy as np
import pandas as pd

# UI파일 연결
# 단, UI파일은 Python 코드 파일과 같은 디렉토리에 위치해야한다.
form_class = uic.loadUiType("guipractice.ui")[0]


# 화면을 띄우는데 사용되는 Class 선언
class WindowClass(QMainWindow, form_class):
    def __init__(self):
        super().__init__()  # for using all class, especially using setupui method
        self.setupUi(self)
        self.addToolBar(NavigationToolbar(self.plotting.canvas, self))  # Generate Plotting frame
        print('line(20)', type(self.plotting))  # Mplwiget is figure class in matplotlib
        print('line(21)',type(self.plotting.canvas))
        self.button.clicked.connect(self.update_animation)  # Click Signal

        self.modify.clicked.connect(self.methodname)

    def methodname(self):
        self.lineedit.setText(self.lineedit.text())
        print(self.lineedit.text())
        print(type(self.lineedit.text()))

    def update_animation(self):
        self.ani = animation.FuncAnimation(fig=self.plotting, func=self.update_axes, frames=self.update_data)
        # FunAnimation(fig, func, frames=None, init_func=None, fargs=None, save_count=None, *, cache_frame_data=True, **kwargs)
        self.plotting.canvas.draw()

    def update_data(self):
        data = pd.read_csv('data.csv')
        data = data.dropna(how="any")  # Prevent N/A

        x = data['x_value']
        y = data['total_1']
        x = np.array(x.tolist())
        y = np.array(y.tolist())

        yield x, y  # Pass values outside of function

    def update_axes(self, update):
        x, y = update[0], update[1]
        self.plotting.canvas.axes.clear()
        self.plotting.canvas.axes.set_title('plotting')
        self.plotting.canvas.axes.plot(x, y)


if __name__ == "__main__":
    # QApplication : Class of excuting ui class
    app = QApplication(sys.argv)  # sys.argv is automatically get argument values
    # WindowClass의 인스턴스 생성
    myWindow = WindowClass()
    # 프로그램 화면을 보여주는 코드
    myWindow.show()

    # 프로그램을 이벤트루프로 진입시키는(프로그램을 작동시키는) 코드
    app.exec_()
