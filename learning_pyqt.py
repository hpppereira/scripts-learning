# Learning PyQt
# Henrique Pereira
# 2019/03/14

import sys
from PyQt5 import QtGui
from PyQt5 import QtWidgets

app = QtWidgets.QApplication(sys.argv)

window = QtWidgets.QWidget()
window.setGeometry(0, 0, 500, 300)
window.setWindowTitle("PyQT Tuts")

window.show()