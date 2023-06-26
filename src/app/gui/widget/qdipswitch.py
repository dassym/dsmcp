'''

:author: fv
:date: Created on 12 mai 2021
'''

from PyQt5.Qt import QFrame, QLabel, QHBoxLayout, QSizePolicy, QWidget, Qt,\
    QPainter, QBrush, QColor, QRect, QVBoxLayout, QAbstractButton, QMargins,\
    QPropertyAnimation, pyqtProperty, QSize
import logging


_logger = logging.getLogger(__name__)

class QDipSwitchUnit(QAbstractButton):
    
    def __init__(self, parent, orientation=Qt.Vertical):
        QWidget.__init__(self,parent)
        self._orientation = orientation
        self.setCheckable(True)
        self.setContentsMargins(0,0,0,0)
        self.setMinimumSize(QSize(40, 80))
        self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Preferred)
        if self._orientation == Qt.Vertical:
            u = self.rect().width()//4
            self._track_rect = QRect(self.rect()).marginsRemoved(QMargins(u,u,u,u))
            self._thumb_rect = QRect(self._track_rect)
            self._thumb_rect.setHeight(self._track_rect.height()//2)
        else:  
            u = self.rect().height()//4
            self._track_rect = QRect(self.rect()).marginsRemoved(QMargins(u,u,u,u))
            self._thumb_rect = QRect(self._track_rect)
            self._thumb_rect.setWidth(self._track_rect.width()//2)
          
                
        
            
        self._base_offset = 0
        self._end_offset = {
            True: lambda: (self._track_rect.height()//2 if self._orientation == Qt.Vertical else self._track_rect.widht()//2) - self._base_offset ,
            False: lambda: self._base_offset,
        }
        self._offset = self._base_offset            
            
        palette = self.palette()
        
        self._body_brush = QBrush(QColor('firebrick'))
        
        self._text_color = {
                True: palette.highlightedText().color(),
                False: palette.dark().color(),
            }
        self._thumb_text = {
                True: 'On',
                False: 'Off',
            }
        self._track_opacity = 1
        
            
    @pyqtProperty(int)
    def offset(self):
        return self._offset

    @offset.setter
    def offset(self, value):
        self._offset = value
        self.update()            
        
    def resizeEvent(self, event):
        if self._orientation == Qt.Vertical:
            u = self.rect().width()//3
            self._track_rect = QRect(self.rect()).marginsRemoved(QMargins(u,u,u,u))
            self._thumb_rect = QRect(self._track_rect)
            self._thumb_rect.setHeight(self._track_rect.height()//2)
        else:  
            u = self.rect().height()//3
            self._track_rect = QRect(self.rect()).marginsRemoved(QMargins(u,u,u,u))
            self._thumb_rect = QRect(self._track_rect)
            self._thumb_rect.setWidth(self._track_rect.width()//2)
            
        self._offset = self._end_offset[self.isChecked()]()
        
        return QAbstractButton.resizeEvent(self, event)
        
    def paintEvent(self, event):
        QWidget.paintEvent(self, event)
        painter = QPainter(self)
        
        track_opacity = self._track_opacity
        
        
        #if self.isEnabled():
        body_brush = self._body_brush
        text_color = self._text_color[self.isChecked()]
        # else:
        #     track_opacity *= 0.8
        #     body_brush = self.palette().shadow()
        #     text_color = self.palette().shadow().color()
            
        track_brush = QBrush(body_brush)
        thumb_brush = QBrush(body_brush)        

        thumb_brush.setColor(thumb_brush.color().lighter(200))
        track_brush.setColor(track_brush.color().darker(200))
        
        thumb_rect = QRect(self._thumb_rect)
        if self._orientation == Qt.Vertical:
            thumb_rect.translate(0,self.offset)
        else:
            thumb_rect.translate(self.offset,0)
            
            
        painter.fillRect(self.rect(), body_brush)
        painter.fillRect(self._track_rect, track_brush)
        painter.fillRect(thumb_rect, thumb_brush)
        painter.save()
        font = painter.font()
        #painter.pen().setColor(track_brush.color())
        font.setPixelSize(int(0.75 * thumb_rect.width()))
        painter.setFont(font)
        
        painter.translate(thumb_rect.center());
        painter.rotate(-90)
        painter.translate(-thumb_rect.center());
        painter.drawText(
            thumb_rect,
            Qt.AlignCenter,
            self._thumb_text[self.isChecked()],
        )
        
         
        painter.restore()
        
    
    def mouseReleaseEvent(self, event):  # pylint: disable=invalid-name
        super().mouseReleaseEvent(event)
        if event.button() == Qt.LeftButton:
            anim = QPropertyAnimation(self, b'offset', self)
            anim.setDuration(120)
            anim.setStartValue(self.offset)
            anim.setEndValue(self._end_offset[self.isChecked()]())
            anim.start()

    def enterEvent(self, event):  # pylint: disable=invalid-name
        self.setCursor(Qt.PointingHandCursor)
        super().enterEvent(event)    
    
    def setOrientation(self, orientation):
        self._orientation = orientation
        self.update()
    
        
    @property
    def orientation(self):
        return self._orientation
    


class QDipSwitch(QFrame):
    '''
    classdocs
    '''

    def __init__(self, parent, reg=None, n=8, shift=0, orientation=Qt.Vertical):
        '''
        Constructor
        '''
        QFrame.__init__(self, parent)
        self._shift = shift
        self._n = n
        self._reg = reg
        self._switches = []
        self._orientation = orientation
        self.setContentsMargins(0,0,0,0)
        
        self._layout = QVBoxLayout(self)
        
        self._labelText = QLabel(self)
        self._labelText.setObjectName('labelText')
        self._labelText.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._layout.addWidget(self._labelText)
        
        self._labelValue = QLabel(self)
        self._labelValue.setObjectName('labelValue') 
        self._labelValue.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        self._layout.addWidget(self._labelValue)
                
        if self._orientation == Qt.Vertical:
            self._layoutdip = QHBoxLayout(self)
        else:
            self._layoutdip = QVBoxLayout(self)
        self._layout.setContentsMargins(0,0,0,0)
        
        for sw in range(self._n):
            sw = QDipSwitchUnit(self, orientation=self._orientation)
            self._layoutdip.addWidget(sw)
            self._switches.append(sw)
        
        self._layout.addLayout(self._layoutdip)
        
        
        self.setLayout(self._layout)
        #self.setSizePolicy(QSizePolicy.Preferred, QSizePolicy.Fixed)
        
    def onRegisterChange(self, reg, old_value=None, new_value=None):
        if new_value is None:
            new_value = self._reg.value
        self._labelValue.setText( '{0:d} (0x{0:04x})'.format(new_value) )
        for i, sw in enumerate(self._switches):
            m = 1<<(i+self._shift)
            sw.setChecked( (new_value & m) != 0 )
        self.update()
        
    def setReg(self, reg=None, shift=0 ):
        if self._reg is not None:
            self._reg.changed.disconnect(self.onRegisterChange)
            self._labelValue.clear()
        self._reg = reg
        self._shift = shift
        if self._reg is not None:
            self._labelText.setText(self._reg.name)
            self.setToolTip(self._reg.descr)
            self._reg.changed.connect(self.onRegisterChange)
            self.onRegisterChange(self._reg, self._reg.value, self._reg.value)
        else:
            self._labelText.setText('~')
            self.setToolTip('')
        self.update()
            
    def setOrientation(self, orientation):
        self._orientation = orientation
        for sw in self._switches:
            sw.setOrientation(self._orientation)
        self.update()

    def setShift(self, shift):
        self._shift = shift
        #TODO:Update switch unit
        self.update()
        
    @property
    def reg(self):
        return self._reg
    @property
    def shift(self):
        return self._shift
    

class QDipSwitch2(QDipSwitch):
    def __init__(self, parent, reg=None, shift=0, orientation = Qt.Vertical):
        QDipSwitch.__init__(self, parent, reg=reg, n=2, shift=shift, orientation=orientation)
    
class QDipSwitch4(QDipSwitch):
    def __init__(self, parent, reg=None, shift=0, orientation = Qt.Vertical):
        QDipSwitch.__init__(self, parent, reg=reg, n=4, shift=shift, orientation=orientation)
    
class QDipSwitch8(QDipSwitch):
    def __init__(self, parent, reg=None, shift=0, orientation = Qt.Vertical):
        QDipSwitch.__init__(self, parent, reg=reg, n=8, shift=shift, orientation=orientation)

    