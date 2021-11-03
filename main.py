

import sys
from PyQt5.QtWidgets import QApplication

from widgetgallery import WidgetGallery

def main():
    app = QApplication(sys.argv)
    gallery = WidgetGallery()
    gallery.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main()