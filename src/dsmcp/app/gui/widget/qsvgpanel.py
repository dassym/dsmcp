'''

:author: fv
:date: Created on 28 mars 2021
'''
import lxml.etree as ET
from PyQt5.QtCore import QObject, pyqtSignal
from PyQt5.Qt import  Qt, QGraphicsSvgItem, QGraphicsView, QGraphicsScene, QSvgRenderer,\
    QTimer, QPointF, QRectF, QByteArray
import logging

KEY_REPEAT_PERIOD = 200 #ms

KEY_FIRST_REPEAT_COUNT = 2

KEY_LONG_COUNT = 3 # nb repeates


def drawText(painter, p, flags, text):
    size = 32767.0
    corner = QPointF(p.x(), p.y() - size)
    if flags & Qt.AlignHCenter:
        corner.setX(corner.x() - size/2.0)
    elif flags & Qt.AlignRight:
        corner.setX(corner.x() - size)
    if flags & Qt.AlignVCenter:
        corner.setY(corner.y() +size/2.0)
    elif flags & Qt.AlignTop:
        corner.setY(corner.y() + size)
    else:
        flags |= Qt.AlignBottom
    rect = QRectF(corner.x(), corner.y(), size, size)
    return painter.drawText(rect, flags, text)
    



class SvgItem(QGraphicsSvgItem):
    '''Base class for SVG item
    
    :param str oid: The item ID
    :param QSvgPanel owner: The item's owner panel
    :param QWidget parent: optionally the parent widget
    '''
    def __init__(self, svg, owner, renderer, parent=None):
        super().__init__(parent)
        self.svg = svg
        xStyle = svg.get('style')
        if xStyle is not None :
            try:
                self.style = dict( ( kv.split(':') for kv in xStyle.split(';') ) )
            except KeyError:
                self.style = None
        else:
            self.style = None
        self._owner = owner
        self.setSharedRenderer(renderer)
        self.setElementId(svg.get('id'))
        self._bounds = renderer.boundsOnElement(self.elementId())
        self.setPos(self._bounds.topLeft())
        self._owner.log.debug(self.__class__.__name__+":"+self.elementId()+":Initialized")
        #self.setFlag(QGraphicsItem.ItemIsSelectable, True) #horrible selection-box
        
    def initialize(self):
        pass
        
    def _update(self):
        self.update()
    
    def changeAttribute(self, name, value):
        pass
    
    @property
    def owner(self):
        return self._owner
    
    @property
    def board(self):
        return self._owner._board
    
    @property
    def id(self):
        return self.elementId()
    @property
    def bounds(self):
        return self._bounds
    
class SvgLayout(SvgItem):
    '''Class for the layout (draw) of panel.'''
    pass    

class SvgSensitiveItem(SvgItem):
    '''Base class for sensitive items'''
    
    mousePressed = pyqtSignal(QObject, name='mousePressed')
    '''Signal for *mouse pressed* event'''
     
    mouseReleased = pyqtSignal(QObject, name='mouseReleased')
    '''Signal for *mouse released* event'''
    
    
    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        '''Rewrite of the handler for the "mouse pressed" event'''
        self.mousePressed.emit(self)
        super().mousePressEvent(event)
        event.accept()

    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        '''Rewrite of the handler for the "mouse released" event'''
        self.mouseReleased.emit(self)
        super().mouseReleaseEvent(event)

class SvgKey(SvgSensitiveItem):
    '''Base class for key item'''    

    pressShort = pyqtSignal()
    '''Signal for a short press of the key'''
    
    pressLong = pyqtSignal()
    '''Signal for a long press of the key'''
    
    pressRepeat =  pyqtSignal(int)
    '''signal for repetitions of key presses'''
    
    
    
    @classmethod
    def factory(cls, svg, owner, renderer, parent=None):
        '''class method for constructing an object according to its name
        
        :param str oid: The item ID
        :param QSvgPanel owner: The item's owner panel
        :param QWidget parent: optionally the parent widget
        
        :return: The new descendant object of the "SvgItem" class.
        :rtype: SvgItem
        '''
        k = svg.get('id').split('_')
        name = k[1]
        try:
            ext = k[2:]
        except KeyError:
            ext = None
               
        if name == 'dassym':
            return DassymKey(svg, owner, renderer, parent=parent)
        elif name == 'inc':
            return IncrementKey(svg, owner, renderer, parent=parent)
        elif name == 'dec':
            return DecrementKey(svg, owner, renderer, parent=parent)
        elif name == 'parameters':
            return ParametersKey(svg, owner, renderer, parent=parent)
        elif name == 'reverse':
            return ReverseKey(svg, owner, renderer, parent=parent)
        elif name == 'light':
            return LightKey(svg, owner, renderer, parent=parent)
        elif name == 'memory':
            return MemoryKey(svg, owner, num=int(ext[0]),  renderer=renderer, parent=parent)
        elif name == 'workspace':
            if len(ext) > 1 and ext[1].lower() == 'toggle':
                return WorkspaceToggleKey(svg, owner, num=int(ext[0]),  renderer=renderer, parent=parent)
            else:
                return WorkspaceKey(svg, owner, num=int(ext[0]),  renderer=renderer, parent=parent)
        elif name == 'gear':
            return GearKey(svg, owner, numerator=int(ext[0]), denominator=int(ext[1]), renderer=renderer,  parent=parent)
        else:
            return SvgKey(svg, owner, renderer=renderer, parent=parent)
        
    
    def __init__(self, svg, owner,  renderer, parent=None):
        '''Constructor'''
        SvgSensitiveItem.__init__(self, svg, owner, renderer, parent=parent)

    def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        self._repeat_count = 0
        self.owner._key_timer.timeout.connect(self.onTimer)
        self.owner._key_timer.start()
        self.owner.log.debug(self.__class__.__name__+":" + self.id + ' - mousePressEvent()')
        super().mousePressEvent(event)
        event.accept()


    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        self.owner.log.debug(self.__class__.__name__+":" + self.id + ' - mouseReleaseEvent()')
        self.owner._key_timer.timeout.disconnect(self.onTimer)
        self.owner._key_timer.stop()
        if self._repeat_count == 0:
            self.pressShort.emit()
        super().mouseReleaseEvent(event)
        
    def onTimer(self):
        self.owner.log.debug(self.__class__.__name__+":" + self.id + ' - onTimer()')
        self._repeat_count += 1
        if self._repeat_count >= KEY_FIRST_REPEAT_COUNT:
            self.pressRepeat.emit(self._repeat_count)
        if self._repeat_count == KEY_LONG_COUNT:
            self.pressLong.emit()

        
class DassymKey(SvgKey):
    '''Class for *Dassym* key'''
    pass
    
class ReverseKey(SvgKey):
    '''Class for *reverse* key'''
    pass

class LightKey(SvgKey):
    '''Class for *light* key'''
    pass

class MemoryKey(SvgKey):
    '''Class for *memory* key'''
    
    def __init__(self, svg, owner, num, renderer, parent=None):
        SvgKey.__init__(self, svg, owner, renderer, parent=parent)
        self.num = num
        

class WorkspaceKey(SvgKey):
    '''Class for *Workspace* key'''
    
    def __init__(self, svg, owner, num, renderer, parent=None):
        SvgKey.__init__(self, svg, owner, renderer, parent=parent)
        self.num = num

class WorkspaceToggleKey(WorkspaceKey):
    '''Class for *Workspace* key'''
    pass
    

class GearKey(SvgKey):
    '''Class for *gear* key'''
    
    def __init__(self, svg, owner, numerator, denominator, renderer, parent=None):
        SvgKey.__init__(self, svg, owner, renderer, parent=parent)
        self.numerator = numerator
        self.denominator = denominator


class IncrementKey(SvgKey):
    '''Class for *increment* key'''
    pass

class DecrementKey(SvgKey):
    '''Class for *decrement* key'''
    pass

class ParametersKey(SvgKey):
    '''Class for *parameters* key'''
    pass


class SvgLed(SvgItem):
    @classmethod
    def factory(cls, svg, owner, renderer, parent=None):
        '''class method for constructing an Led object according to its name
        
        :param str oid: The item ID
        :param QSvgPanel owner: The item's owner panel
        :param QWidget parent: optionally the parent widget
        
        :return: The new descendant object of the :class:`Display` class.
        '''
    
        k = svg.get('id').split('_')
        name = k[1]
        try:
            ext = k[2:]
        except KeyError:
            ext = None

        if name == 'reverse':
            return ReverseLed(svg, owner, renderer, parent=parent)
        elif name == 'light':
            if ext[0] == 'blue':
                return LightBlueLed(svg, owner, renderer, parent=parent)
            else:
                return LightLed(svg, owner, renderer, parent=parent)
        elif name == 'mem':
                return MemoryLed(svg, owner, num=int(ext[0]), renderer=renderer, parent=parent)
            
    def __init__(self, svg, owner, renderer, parent=None):
        SvgItem.__init__(self, svg, owner, renderer, parent=parent)
        self.on = False
        try:
            self._fillOn = self.style['fill']
        except:
            self._fillOn = '#ccff00'
            
        self._fillOff = '#808080'  
            
    def _update(self):
        if self.on:
            self.style['fill'] = self._fillOn
        else: 
            self.style['fill'] = self._fillOff
        
        self.svg.set('style', ';'.join( k+':'+v for k,v in self.style.items() ) ) 
        #self.owner.log.debug('style='+self.svg.get('style'))
        super()._update()
        
        
class ReverseLed(SvgLed):

    def _update(self):
        self.on = self.owner.board.isMotorReverse()
        super()._update()

class LightLed(SvgLed):
    def _update(self):
        self.on = self.owner.board.isLightEnabled()
        SvgLed._update(self)

class LightBlueLed(LightLed):
    
    def initialize(self):
        self.setVisible(self.owner.board.hasBlueLight())
        
    
    def _update(self):
        self.on = self.owner.board.isLightAlternate()
        SvgLed._update(self)

class MemoryLed(SvgLed):
    
    def __init__(self, svg, owner, num, renderer, parent=None):
        SvgLed.__init__(self, svg, owner, renderer, parent=parent)
        self.num = num
        

class Display(SvgItem):
    
    @classmethod
    def factory(cls, svg, owner, renderer, parent=None):
        '''class method for constructing an Display object according to its name
        
        :param str oid: The item ID
        :param QSvgPanel owner: The item's owner panel
        :param QWidget parent: optionally the parent widget
        
        :return: The new descendant object of the :class:`Display` class.
        '''
    
        k = svg.get('id').split('_')
        kind = k[1].lower()

        try:
            ndigits = int(k[2])
        except KeyError:
            ndigits = 3
        
        if kind == '7seg':
            return Display7seg(svg, owner, ndigits=ndigits, renderer=renderer, parent=parent)
        else:
            return Display(svg, owner, ndigits=ndigits, renderer=renderer, parent=parent)
                
    def __init__(self, svg, owner, ndigits=3, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.ndigits = ndigits
        self._text = ''
        
        
    def paint(self, painter, option, widget):
        '''
        
        :param QPainter painter:
        :param QStyleOptionGraphicsItem option:
        :param QWidget widget:
        ''' 
        
        ret = super().paint(painter, option, widget)
        
        rect = QRectF(self.boundingRect())
        #rect = rect.marginsRemoved(QMarginsF(1,2,2,1))
        
        #txt = QStaticText() 
        #txt.setText( "{0:5d}".format(self._speed) )
        #txt.setTextWidth(rect.width())
        txt = self._text
        painter.setPen(Qt.white);
        painter.setBrush(Qt.white);
        
        fm = painter.fontMetrics()
        f = painter.font()
        rectTxt = fm.boundingRect('00000')
        scale = rect.width() / rectTxt.width()
        f.setPointSizeF(f.pointSizeF() * scale)
        painter.setFont(f)
        painter.drawText(rect, Qt.AlignCenter, txt)
        
        return ret
        
        
    def setText(self, text):
        self._text = text
        

class Display7seg(Display):
    pass

class Gauge(SvgItem):
    
    @classmethod
    def factory(cls, svg, owner, renderer, parent=None):
        '''class method for constructing an Gauge object according to its name
        
        :param str oid: The item ID
        :param QSvgPanel owner: The item's owner panel
        :param QWidget parent: optionally the parent widget
        
        :return: The new descendant object of the :class:`Gauge` class.
        '''
    
        k = svg.get('id').split('_')
        kind = k[1].lower()

        if kind == 'torque':
            return GaugeTorque(svg, owner, renderer=renderer, parent=parent)
        elif kind == 'speed':
            return GaugeSpeed(svg, owner, renderer=renderer, parent=parent)
        elif kind == 'speedref':
            return GaugeSpeedReference(svg, owner, renderer=renderer, parent=parent)
        elif kind == 'pressure':
            return GaugePressure(svg, owner, renderer=renderer, parent=parent)
        elif kind == 'analoginput':
            return GaugeAnalogInput(svg, owner, int(k[2]), renderer=renderer, parent=parent)
        elif kind == 'temp':
            return GaugeTemperature(svg, owner, int(k[2]), renderer=renderer, parent=parent)
        elif kind == 'psvoltage':
            return GaugePSVoltage(svg, owner, renderer=renderer, parent=parent)
        else:
            raise KeyError('Unknow gauge kind ({0!s})'.format(kind))
                
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.caption = 'Gauge' 
        self.minValue = 0.0
        self.maxValue = 1.0
        self._value = self.minValue
        
        
    def paint(self, painter, option, widget):
        '''
        
        :param QPainter painter:
        :param QStyleOptionGraphicsItem option:
        :param QWidget widget:
        ''' 
        
        ret = super().paint(painter, option, widget)
        
        rect = QRectF(self.boundingRect())
        scale = (self.value-self.minValue) / (self.maxValue-self.minValue)
        if rect.width()>rect.height():
            rect.setWidth(rect.width() * scale)
        else: 
            h = rect.height() * scale
            rect.setY(rect.height() -h)
            rect.setHeight(h)

        painter.setPen(Qt.NoPen);
        painter.setBrush(Qt.blue);


        painter.drawRect(rect)
        
        return ret
    
    def setValue(self, value):
        if value > self.maxValue:
            self._value = self.maxValue
        elif value < self.minValue:
            self._value = self.minValue
        else:
            self._value = value
        
    
    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, value):
        self.setValue(value)

class BaseGaugeAnalogInput(Gauge):
    '''Gauge to display actual torque (load)'''
    
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
    
    def initialize(self):
        Gauge.initialize(self)
        self.minValue = 0
        self.maxValue = 10000
        self.value = self.minValue

    
class GaugeAnalogInput(BaseGaugeAnalogInput):
    '''Gauge to display actual torque (load)'''
    
    def __init__(self, svg, owner, index, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.index = index
        self.caption = 'Analog #'+str(index)
        
    def _update(self):
        self.value = self.owner.board.getAnalogInput(self.index)
        self.setToolTip("{0:s}: {1:.0f}".format(self.caption, self.value))        
        #self.owner.log.debug('GaugeAnalogInput.value = '+str(self.owner.board.getAnalogInput(self.index)))
        Gauge._update(self)
    

class GaugeTemperature(GaugeAnalogInput):
    '''Gauge to display actual torque (load)'''
    
    def __init__(self, svg, owner, index, renderer=None, parent=None):
        super().__init__(svg, owner, index, renderer, parent)
        self.caption = 'Temp. on An#'+str(index)
        
    def _update(self):
        self.value = self.owner.board.getAnalogInput(self.index)
        self.setToolTip("{0:s}: {1:.1f}°C".format(self.caption, self.value/100))        
        #self.owner.log.debug('GaugeAnalogInput.value = '+str(self.owner.board.getAnalogInput(self.index)))
        Gauge._update(self)

        
class GaugeSpeedReference(BaseGaugeAnalogInput):
    '''Gauge to display actual speed reference'''
    
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.caption = 'Speed ref'
        
    def _update(self):
        try:
            self.value = 10000 * self.owner.board.getSpeedReference() / self.owner.board.motorSpeed() 
        except ZeroDivisionError:
            self.value = 0 
        self.setToolTip("{0:s}: {1:.1f}%".format(self.caption, self.value/100))
        Gauge._update(self)
    

class GaugePressure(BaseGaugeAnalogInput):
    '''Gauge to display actual pressure on sensor'''
    
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.caption = 'Pressure ref'
        
    def _update(self):
        self.value = self.owner.board.getPressure()
        self.setToolTip("{0:s}: {1:.1f}%".format(self.caption, self.value/100))
        Gauge._update(self)
        


class GaugeTorque(Gauge):
    '''Gauge to display actual torque (load)'''
    
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.caption = 'Torque'
        
    def _update(self):
        self.value = self.owner.board.motorRealCurrent()
        self.setToolTip("{0:s}: {1:.0f}mA".format(self.caption, self.value))
        Gauge._update(self)
        
    
    def initialize(self):
        Gauge.initialize(self)
        self.maxValue = self.owner.board.torque_range.upper
        
        
class GaugeSpeed(Gauge):
    '''Gauge to display proportion between actual and set point speed'''
    
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.caption = 'Speed'
        
    def _update(self):
        if self.owner.board.motorSpeed() != 0:
            self.value = self.owner.board.motorRealSpeed() / self.owner.board.motorSpeed()
            self.setToolTip("{0:s}: {1:.1f}% {2:d}".format(self.caption, self.value*100, self.owner.board.motorSpeed()))
        else:
            self.setToolTip("{0:s}: N/A".format(self.caption,))
        Gauge._update(self)
    
class GaugePSVoltage(Gauge):
    '''Gauge to display the power supply voltage'''
    
    def __init__(self, svg, owner, renderer=None, parent=None):
        super().__init__(svg, owner, renderer, parent)
        self.caption = 'PS voltage'
        
    def _update(self):
        self.value = self.owner.board.getPowerSupply()
        self.setToolTip("{0:s}: {1:.1f}V".format(self.caption, self.value))
        Gauge._update(self)
        
    def initialize(self):
        Gauge.initialize(self)
        self.maxValue = self.owner.board.powersupply_range.upper
    

class QSvgPanel(QGraphicsView):
    '''Class for panel with SVG layout
    
    :param QWidget parent: The parent widget.
    :parem list flags: Arguments are passed to the QWidget constructor.    
    '''


    def __init__(self, parent=None):
        '''Constructor'''
        QGraphicsView.__init__(self, parent=parent)
        self.log = logging.getLogger(self.__class__.__name__) 
        self._scene = QGraphicsScene(self)
        self._layout_renderer = QSvgRenderer()
        self._sensitive_renderer = QSvgRenderer()
        self._display_renderer = QSvgRenderer()
        self._key_timer = QTimer()
        self._key_timer.setInterval(KEY_REPEAT_PERIOD)
        self.keys = []
        self.leds = []
        self.gauges = []
        self.setScene(self._scene)
        self._board = None
        self._display = None
        
    def setSvg(self, fname):
        '''Sets the SVG layout and initialize sensitive regions and keys
        
        :param str fname: The SVG file name
        '''

        namespaces={
            #'dc':"http://purl.org/dc/elements/1.1/",
            #'cc':"http://creativecommons.org/ns#",
            #'rdf':"http://www.w3.org/1999/02/22-rdf-syntax-ns#",
            'svg':"http://www.w3.org/2000/svg",
            #'sodipodi':"http://sodipodi.sourceforge.net/DTD/sodipodi-0.dtd",
            'inkscape':"http://www.inkscape.org/namespaces/inkscape",    
            }

        xSvgTree = ET.parse(fname)
        xSvgRoot = xSvgTree.getroot()
        
        xLayout = xSvgRoot.xpath("//svg:g[@id='layout']", namespaces=namespaces)[0]
        
         
        self._layout_renderer.load(QByteArray(b'<svg:svg>'+ET.tostring(xLayout)+b'</svg:svg>'))
        self._layout_renderer.setAspectRatioMode(Qt.KeepAspectRatio)
        self._layout_renderer.setViewBox(self.rect())
        
        layout = SvgLayout(xLayout, self, self._layout_renderer)
        self._scene.addItem(layout)
        
        xSensitive = xSvgRoot.xpath("//svg:g[@id='sensitive']", namespaces=namespaces)[0]
        self._sensitive_renderer.load(QByteArray(b'<svg:svg>'+ET.tostring(xSensitive)+b'</svg:svg>'))
        self._sensitive_renderer.setAspectRatioMode(Qt.KeepAspectRatio)
        self._sensitive_renderer.setViewBox(self.rect())

        xKeys = xSensitive.xpath(".//*[starts-with(@id,'key_')]", namespaces=namespaces) 
        
        for xKey in xKeys:
            key =  SvgKey.factory(xKey, self, self._sensitive_renderer)
            # key.pressRepeat.connect(partial(self.onKeyPressRepeat, key))
            # key.pressShort.connect(partial(self.onKeyPressShort, key))
            # key.pressLong.connect(partial(self.onKeyPressLong,key))
            self._scene.addItem(key)
            self.keys.append(key)
            
        self.xDisplay = xSvgRoot.xpath("//svg:g[@id='display']", namespaces=namespaces)[0]
        self._display_renderer.load(QByteArray(b'<svg:svg>'+ET.tostring(self.xDisplay)+b'</svg:svg>'))
        self._display_renderer.setAspectRatioMode(Qt.KeepAspectRatio)
        self._display_renderer.setViewBox(self.rect())
        try:
            xDisplayDisplay = self.xDisplay.xpath(".//*[starts-with(@id,'display_')]", namespaces=namespaces)[0]
            self._display = Display.factory(xDisplayDisplay, self, self._display_renderer)
            self._scene.addItem(self._display)
        except IndexError:
            self._display = None
            
        for xLed in self.xDisplay.xpath(".//*[starts-with(@id,'led_')]", namespaces=namespaces):
            led =  SvgLed.factory(xLed, self, self._display_renderer)
            self._scene.addItem(led)
            self.leds.append(led)
            
        for xGauge in self.xDisplay.xpath(".//*[starts-with(@id,'gauge_')]", namespaces=namespaces):
            gauge =  Gauge.factory(xGauge, self, self._display_renderer)
            self._scene.addItem(gauge)
            self.gauges.append(gauge)
            
    def setBoard(self, board):
        self._board = board
        self.initialize()
            
    def initialize(self):
        if self._board is None: return
        for led in self.leds:
            led.initialize()
        for gauge in self.gauges:
            gauge.initialize()        
        
        
    def refresh(self):
        if self._board is not None:
            self._display._update()
            self._display_renderer.load(QByteArray(b'<svg:svg>'+ET.tostring(self.xDisplay)+b'</svg:svg>'))
            for led in self.leds:
                led._update()
            for gauge in self.gauges:
                gauge._update()
            
        
    def update(self, *args, **kwargs):
        self.refresh()        
        ret = QGraphicsView.update(self, *args, **kwargs)
        return ret
          
            
    #===========================================================================
    # def onKeyPressShort(self, key):
    #     self.log.debug('onKeyPressShort('+str(key.id)+")")
    #     
    # def onKeyPressRepeat(self, key, count):
    #     self.log.debug( 'onKeyPressRepeat('+str(key.id)+", "+str(count)+")" )
    #     
    # def onKeyPressLong(self, key):
    #     self.log.debug( 'onKeyPressLong('+str(key.id)+")" )
    #===========================================================================

        
    def resizeEvent(self, *args, **kwargs):
        '''Rewrite the resize event handler'''
        self.fitInView(self._scene.sceneRect(), Qt.KeepAspectRatio)
        return QGraphicsView.resizeEvent(self, *args, **kwargs)

    # def mousePressEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        # #self.log.debug('SvgViewer - mousePressEvent() - X:'+str(event.x())+";Y:"+str(event.y()) )
        # super().mousePressEvent(event)
        
        
    def mouseReleaseEvent(self, event: 'QtWidgets.QGraphicsSceneMouseEvent'):
        '''Rewrite the mouse release event handler'''
        self.log.debug('SvgViewer - mouseReleaseEvent()')
        super().mouseReleaseEvent(event)
        
        
    def setDisplayText(self, txt):
        if self._display:
            self._display.setText(txt)
            
        
    @property
    def scene(self):
        return self._scene
    @property
    def renderer(self):
        self._renderer
        
    @property
    def board(self):
        return self._board
        
        
        