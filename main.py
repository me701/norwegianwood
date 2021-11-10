import sys
from PyQt5.QtWidgets import QApplication
from widgetgallery import WidgetGallery

if __name__ == '__main__':
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())


