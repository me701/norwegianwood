
#include "widgetgallery.h"
#include "norwegianwoodstyle.h"

from PyQt5.QtWidgets import QApplication, QCheckBox, QComboBox , QDateTimeEdit, QDial, QGridLayout, \
    QGroupBox, QDialog, QLabel, QLineEdit, QProgressBar, QPushButton, QRadioButton, QSlider, \
        QScrollBar, QSpinBox, QStyle, QStyleFactory, QTableWidget, \
        QTextEdit, QVBoxLayout, QHBoxLayout, QSizePolicy, QTabWidget, QWidget
from PyQt5.QtCore import Qt, QEvent, QDateTime, QTimer
from PyQt5.QtGui import QPalette

class WidgetGallery(QDialog):

    def __init__(self, parent=None):
        super().__init__(parent)

        self.styleComboBox = QComboBox()
        defaultStyleName = QApplication.style().objectName()
        styleNames = QStyleFactory.keys()
        styleNames.append("NorwegianWood")
        for i in range(1, len(styleNames)):
            if (defaultStyleName == styleNames[i]):
                styleNames.swapItemsAt(0, i)
                break
  
        self.styleComboBox.addItems(styleNames)

        styleLabel = QLabel(self.tr("&Style:")) # check this tr use
        styleLabel.setBuddy(self.styleComboBox)


        self.useStylePaletteCheckBox = QCheckBox(self.tr("&Use style's standard palette"))
        self.useStylePaletteCheckBox.setChecked(True)

        self.disableWidgetsCheckBox = QCheckBox(self.tr("&Disable widgets"))

        self.createTopLeftGroupBox()
        self.createTopRightGroupBox()
        self.createBottomLeftTabWidget()
        self.createBottomRightGroupBox()
        self.createProgressBar()

        self.styleComboBox.textActivated.connect(self.changeStyle)
        self.useStylePaletteCheckBox.toggled.connect(self.changePalette)
        self.disableWidgetsCheckBox.toggled.connect(self.topLeftGroupBox.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.topRightGroupBox.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.bottomLeftTabWidget.setDisabled)
        self.disableWidgetsCheckBox.toggled.connect(self.bottomRightGroupBox.setDisabled)

        topLayout = QHBoxLayout()
        topLayout.addWidget(styleLabel)
        topLayout.addWidget(self.styleComboBox)
        topLayout.addStretch(1)
        topLayout.addWidget(self.useStylePaletteCheckBox)
        topLayout.addWidget(self.disableWidgetsCheckBox)

        mainLayout = QGridLayout()
        mainLayout.addLayout(topLayout, 0, 0, 1, 2)
        mainLayout.addWidget(self.topLeftGroupBox, 1, 0)
        mainLayout.addWidget(self.topRightGroupBox, 1, 1)
        mainLayout.addWidget(self.bottomLeftTabWidget, 2, 0)
        mainLayout.addWidget(self.bottomRightGroupBox, 2, 1)
        mainLayout.addWidget(self.progressBar, 3, 0, 1, 2)
        mainLayout.setRowStretch(1, 1)
        mainLayout.setRowStretch(2, 1)
        mainLayout.setColumnStretch(0, 1)
        mainLayout.setColumnStretch(1, 1)
        self.setLayout(mainLayout)

        self.setWindowTitle(self.tr("Styles"))
        self.styleChanged()
 
    def changeStyle(self, styleName):
        #if (styleName == "NorwegianWood"):
        #    QApplication.setStyle(NorwegianWoodStyle())
        #else:
        #    pass    
        QApplication.setStyle(QStyleFactory.create(styleName))


    def changePalette(self):
        QApplication.setPalette(
           QApplication.style().standardPalette() if self.useStylePaletteCheckBox.isChecked() else QPalette())


    def changeEvent(self, event):
        if event.type() == QEvent.StyleChange:
            self.styleChanged()

    def styleChanged(self):
        styleName = QApplication.style().objectName()
        for i in range(0, self.styleComboBox.count()): 
            if (self.styleComboBox.itemText(i) == styleName):
                self.styleComboBox.setCurrentIndex(i)
                break
        self.changePalette()


    def advanceProgressBar(self):

        curVal = self.progressBar.value()
        maxVal = self.progressBar.maximum()
        self.progressBar.setValue(curVal + (maxVal - curVal) / 100)
        


    def createTopLeftGroupBox(self):

        self.topLeftGroupBox = QGroupBox(self.tr("Group 1"))

        radioButton1 = QRadioButton(self.tr("Radio button 1"))
        radioButton2 = QRadioButton(self.tr("Radio button 2"))
        radioButton3 = QRadioButton(self.tr("Radio button 3"))
        radioButton1.setChecked(True)

        checkBox = QCheckBox(self.tr("Tri-state check box"))
        checkBox.setTristate(True)
        checkBox.setCheckState(Qt.PartiallyChecked)

        layout = QVBoxLayout()
        layout.addWidget(radioButton1)
        layout.addWidget(radioButton2)
        layout.addWidget(radioButton3)
        layout.addWidget(checkBox)
        layout.addStretch(1)
        self.topLeftGroupBox.setLayout(layout)



    def createTopRightGroupBox(self):

        self.topRightGroupBox = QGroupBox(self.tr("Group 2"))

        defaultPushButton = QPushButton(self.tr("Default Push Button"))
        defaultPushButton.setDefault(True)

        togglePushButton = QPushButton(self.tr("Toggle Push Button"))
        togglePushButton.setCheckable(True)
        togglePushButton.setChecked(True)

        flatPushButton = QPushButton(self.tr("Flat Push Button"))
        flatPushButton.setFlat(True)

        layout = QVBoxLayout()
        layout.addWidget(defaultPushButton)
        layout.addWidget(togglePushButton)
        layout.addWidget(flatPushButton)
        layout.addStretch(1)
        self.topRightGroupBox.setLayout(layout)


    def createBottomLeftTabWidget(self):

        self.bottomLeftTabWidget = QTabWidget()
        self.bottomLeftTabWidget.setSizePolicy(QSizePolicy.Preferred,
                                        QSizePolicy.Ignored)

        tab1 = QWidget()
        tableWidget = QTableWidget(10, 10)

        tab1hbox = QHBoxLayout()
        tab1hbox.setContentsMargins(5,5, 5, 5)
        tab1hbox.addWidget(tableWidget)
        tab1.setLayout(tab1hbox)

        tab2 = QWidget()
        textEdit = QTextEdit()

        textEdit.setPlainText("Twinkle, twinkle, little star,\n"
                                "How I wonder what you are.\n"
                                "Up above the world so high,\n"
                                "Like a diamond in the sky.\n"
                                "Twinkle, twinkle, little star,\n"
                                "How I wonder what you are!\n")

        tab2hbox = QHBoxLayout()
        tab2hbox.setContentsMargins(5, 5, 5, 5)
        tab2hbox.addWidget(textEdit)
        tab2.setLayout(tab2hbox)

        self.bottomLeftTabWidget.addTab(tab1, self.tr("&Table"))
        self.bottomLeftTabWidget.addTab(tab2, self.tr("Text &Edit"))


    def createBottomRightGroupBox(self):

        self.bottomRightGroupBox = QGroupBox(self.tr("Group 3"))
        self.bottomRightGroupBox.setCheckable(True)
        self.bottomRightGroupBox.setChecked(True)

        lineEdit = QLineEdit("s3cRe7")
        lineEdit.setEchoMode(QLineEdit.Password)

        spinBox = QSpinBox(self.bottomRightGroupBox)
        spinBox.setValue(50)

        dateTimeEdit = QDateTimeEdit(self.bottomRightGroupBox)
        dateTimeEdit.setDateTime(QDateTime.currentDateTime())

        slider = QSlider(Qt.Horizontal, self.bottomRightGroupBox)
        slider.setValue(40)

        scrollBar = QScrollBar(Qt.Horizontal, self.bottomRightGroupBox)
        scrollBar.setValue(60)

        dial = QDial(self.bottomRightGroupBox)
        dial.setValue(30)
        dial.setNotchesVisible(True)

        layout = QGridLayout()
        layout.addWidget(lineEdit, 0, 0, 1, 2)
        layout.addWidget(spinBox, 1, 0, 1, 2)
        layout.addWidget(dateTimeEdit, 2, 0, 1, 2)
        layout.addWidget(slider, 3, 0)
        layout.addWidget(scrollBar, 4, 0)
        layout.addWidget(dial, 3, 1, 2, 1)
        layout.setRowStretch(5, 1)
        self.bottomRightGroupBox.setLayout(layout)

    def createProgressBar(self):
        self.progressBar = QProgressBar()
        self.progressBar.setRange(0, 10000)
        self.progressBar.setValue(0)

        timer = QTimer(self)
        timer.timeout.connect(self.advanceProgressBar)
        timer.start(1000)

