from PyQt5.QtWidgets import (QProxyStyle, QStyleFactory, QPushButton,
                             QComboBox,QStyleOptionButton)
from PyQt5.QtGui import (QPalette, QColor, QImage, QPainter, QBrush, 
                         QPen, QPolygon, QPainterPath, QRegion)
from PyQt5.QtCore import Qt, QPoint, QRectF

class NorwegianWoodStyle(QProxyStyle):

    def __init__(self):
        super().__init__(QStyleFactory.create("windows"))
        self.setObjectName("NorwegianWood")
        self.m_standardPalette = QPalette()

    def standardPalette(self):

        if not self.m_standardPalette.isBrushSet(QPalette.Disabled, QPalette.Mid):

            brown = QColor (212, 140, 95)
            beige = QColor(236, 182, 120)
            slightlyOpaqueBlack = QColor(0, 0, 0, 63)

            backgroundImage = QImage("./images/woodbackground.png")
            buttonImage = QImage("./images/woodbutton.png")
            midImage = buttonImage.convertToFormat(QImage.Format_RGB32)

            painter = QPainter()
            painter.begin(midImage)
            painter.setPen(Qt.NoPen)
            painter.fillRect(midImage.rect(), slightlyOpaqueBlack)
            painter.end()

            palette = QPalette(brown)
            palette.setBrush(QPalette.BrightText, Qt.white)
            palette.setBrush(QPalette.Base, beige)
            palette.setBrush(QPalette.Highlight, Qt.darkGreen)
            self.setTexture(palette, QPalette.Button, buttonImage)
            self.setTexture(palette, QPalette.Mid, midImage)
            self.setTexture(palette, QPalette.Window, backgroundImage)

            brush = palette.window()
            brush.setColor(brush.color().darker())

            palette.setBrush(QPalette.Disabled, QPalette.WindowText, brush)
            palette.setBrush(QPalette.Disabled, QPalette.Text, brush)
            palette.setBrush(QPalette.Disabled, QPalette.ButtonText, brush)
            palette.setBrush(QPalette.Disabled, QPalette.Base, brush)
            palette.setBrush(QPalette.Disabled, QPalette.Button, brush)
            palette.setBrush(QPalette.Disabled, QPalette.Mid, brush)

            m_standardPalette = palette
        return m_standardPalette

    def polish(self, widget):
        if (isinstance(widget, (QPushButton, QComboBox))):
            widget.setAttribute(Qt.WA_Hover, True)
        return super().polish(widget)
         

    def unpolish(self, widget):
        if (isinstance(widget, (QPushButton, QComboBox))):
            widget.setAttribute(Qt.WA_Hover, False)
        return super().unpolish(widget)
         
    def pixelMetric(self, metric, option, widget):
        if metric == self.PM_ComboBoxFrameWidth:
            return 8
        elif metric == self.PM_ScrollBarExtent:
            return self.baseStyle().pixelMetric(metric, option, widget) + 4
        else:
            return self.baseStyle().pixelMetric(metric, option, widget)

    def styleHint(self, hint, option, widget, returnData):
        if hint == self.SH_DitherDisabledText:
            return 0
        elif hint == self.SH_EtchDisabledText:
            return 1
        else:
            return self.baseStyle().styleHint(hint, option, widget, returnData)

    def drawPrimitive(self, element, option, painter, widget):

        if element == self.PE_PanelButtonCommand:

            delta = 64 if option.state and self.State_MouseOver else 0

            slightlyOpaqueBlack = QColor(0, 0, 0, 63)
            semiTransparentWhite = QColor(255, 255, 255, 127 + delta)
            semiTransparentBlack = QColor(0, 0, 0, 127 - delta)

            x, y, width, height = option.rect.getRect()

            roundRect = self.roundRectPath(option.rect)

            radius = min(width, height) // 2

            buttonOption = QStyleOptionButton(option)
            if (buttonOption and (buttonOption.features & QStyleOptionButton.Flat)):
                brush = option.palette.window()
                darker = (option.state & (self.State_Sunken | self.State_On))
            else:
                if (option.state & (self.State_Sunken | self.State_On)):
                    brush = option.palette.mid()
                    darker = not (option.state & self.State_Sunken)
                else:
                    brush = option.palette.button()
                    darker = False

            painter.save()
            painter.setRenderHint(QPainter.Antialiasing, True)
            painter.fillPath(roundRect, brush)
            if darker:
                painter.fillPath(roundRect, slightlyOpaqueBlack)
            if (radius < 10):
                penWidth = 3
            elif (radius < 20):
                penWidth = 5
            else:
                penWidth = 7
            topPen = QPen(semiTransparentWhite, penWidth)
            bottomPen = QPen(semiTransparentBlack, penWidth)
            if (option.state & (self.State_Sunken | self.State_On)):
                topPen, bottomPen = bottomPen, topPen
            x1 = int(x)
            x2 = int(x + radius)
            x3 = int(x + width - radius)
            x4 = int(x + width)

            if (option.direction == Qt.RightToLeft):
                x1, x4 = x4, x1 
                x2, x3 = x3, x2

            points = [QPoint(x1, y), QPoint(x4, y), QPoint(x3, y + radius),
                      QPoint(x2, y + height - radius), QPoint(x1, y + height)]
            topHalf = QPolygon(points)
            topHalfReg = QRegion(topHalf)
            painter.setClipPath(roundRect)
            painter.setClipRegion(topHalfReg, Qt.IntersectClip)
            painter.setPen(topPen)
            painter.drawPath(roundRect)
            bottomHalf = QPolygon(points)
            bottomHalf[0] = QPoint(x4, y + height)
            painter.setClipPath(roundRect)
            bottomHalfReg = QRegion(bottomHalf)
            painter.setClipRegion(bottomHalfReg, Qt.IntersectClip)
            painter.setPen(bottomPen)
            painter.drawPath(roundRect)

            painter.setPen(option.palette.windowText().color())
            painter.setClipping(False)
            painter.drawPath(roundRect)

            painter.restore()
        else:
            self.baseStyle().drawPrimitive(element, option, painter, widget)

    def drawControl(self, element, option, painter, widget):
        if element == self.CE_PushButtonLabel:
            buttonOption = QStyleOptionButton(option)
            if (buttonOption):
                myButtonOption = buttonOption
                if (myButtonOption.palette.currentColorGroup()!= QPalette.Disabled):
                    if (myButtonOption.state & (self.State_Sunken | self.State_On)):
                        myButtonOption.palette.setBrush(QPalette.ButtonText,
                                myButtonOption.palette.brightText())
            self.baseStyle().drawControl(element, myButtonOption, painter, widget)
        else:
            self.baseStyle().drawControl(element, option, painter, widget)

    def setTexture(self, palette, role, image):
        for i in range(0, QPalette.NColorGroups): 
            brush = QBrush(image)
            brush.setColor(palette.brush(QPalette.ColorGroup(i), role).color())
            palette.setBrush(QPalette.ColorGroup(i), role, brush)

    def roundRectPath(self, rect):

        radius = int(min(rect.width(), rect.height()) / 2)
        diam = 2 * radius

        x1, y1, x2, y2 = rect.getCoords()
        x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

        path = QPainterPath()
        path.moveTo(x2, y1 + radius)
        path.arcTo(QRectF(x2 - diam, y1, diam, diam), 0.0, 90.0)
        path.lineTo(x1 + radius, y1)
        path.arcTo(QRectF(x1, y1, diam, diam), 90.0, 90.0)
        path.lineTo(x1, y2 - radius)
        path.arcTo(QRectF(x1, y2 - diam, diam, diam), 180.0, 90.0)
        path.lineTo(x1 + radius, y2)
        path.arcTo(QRectF(x2 - diam, y2 - diam, diam, diam), 270.0, 90.0)
        path.closeSubpath()
        return path
