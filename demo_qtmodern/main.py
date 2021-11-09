"""
Separate driver to show the widget gallery using the 
qmodern style

  pip install qmodern
"""


import sys
from PyQt5.QtWidgets import QApplication
from widgetgallery import WidgetGallery

import qtmodern.styles
import qtmodern.windows

if __name__ == '__main__':
    app = QApplication(sys.argv)
    qtmodern.styles.dark(app)
    gallery = WidgetGallery()
    # comment the next line to see the subtle difference
    # made by adding "frameless" windows.
    #gallery = qtmodern.windows.ModernWindow(gallery)

    gallery.show()
    sys.exit(app.exec_())



