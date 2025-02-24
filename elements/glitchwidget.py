#--------------------------------

# Imports
from PyQt5 import QtWidgets, QtCore, QtGui
import random
#--------------------------------

# Glitch QPainter widget class
class GlitchWidget(QtWidgets.QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setAttribute(QtCore.Qt.WA_TransparentForMouseEvents)
        self.glitch_active = False

        self.glitch_timer = QtCore.QTimer()
        self.glitch_timer.timeout.connect(self.trigger_glitch)
        self.glitch_duration = 100
        self.glitch_timer.start(2000)
    #--------------------------------

    # Functions
    def trigger_glitch(self):
        """
        enable and disable glitches
        """
        self.glitch_active = True
        self.update() # enable and prepair disable
        QtCore.QTimer.singleShot(self.glitch_duration, self.disable_glitch)
    # sub-function ^
    def disable_glitch(self):
        self.glitch_active = False
        self.update() # disable
    #--------------------------------

    def paintEvent(self, event):
        """
        paint the glitches
        """
        if not self.glitch_active:
            return
        
        painter = QtGui.QPainter(self)
        pen = QtGui.QPen(QtGui.QColor(255, 105, 180), 2, QtCore.Qt.DashLine)
        painter.setPen(pen)

        for _ in range(10):
            x_start = random.randint(0, self.width())
            y_start = random.randint(0, self.height())
            x_end = x_start + random.randint(-25, 25)
            painter.drawLine(x_start, y_start, x_end, y_start)
        painter.end()
#--------------------------------