'''

:author: fv
:date: Created on 19 mars 2021
'''

import dapi2



TRACE_INGOING_DAPI_FMT    = '{time:9.3f} | <-- | {buf:30s} | {msg.code!s}:{regs:s}'
TRACE_OUTGOING_DAPI_FMT   = '{time:9.3f} | --> | {buf:30s} | {msg.code!s}:{regs:s}'


class Tracer(object):
    def __init__(self, app, dapi=None):
        self.app = app
        self.dapi = dapi
        self.stop = False
        
    def traceRaw(self, time, direction, buf, msg):
        if self.stop:return
        if direction == dapi2.DComTracingDirection.INGOING:
            print(dapi2.TRACE_INGOING_COLOR, end='')
            print(dapi2.TRACE_INGOING_RAW_FMT.format(time=time, buf=dapi2.buffer2str(buf), msg=msg)) #@UndefinedVariable
        else:
            print(dapi2.TRACE_OUTGOING_COLOR, end='')
            print(dapi2.TRACE_OUTGOING_RAW_FMT.format(time=time, buf=dapi2.buffer2str(buf), msg=msg)) #@UndefinedVariable
            
    def traceNormal(self, time, direction, buf, msg):
        if self.stop:return
        if direction == dapi2.DComTracingDirection.INGOING:
            if msg.isError():
                print(dapi2.TRACE_INERROR_COLOR, end='')
            else:
                print(dapi2.TRACE_INGOING_COLOR, end='')
            print(dapi2.TRACE_INGOING_NORMAL_FMT.format(time=time, buf=dapi2.buffer2str(buf), msg=msg)) #@UndefinedVariable
        else:
            if msg.isError():
                print(dapi2.TRACE_OUTERROR_COLOR, end='')
            else:
                print(dapi2.TRACE_OUTGOING_COLOR, end='')
            print(dapi2.TRACE_OUTGOING_NORMAL_FMT.format(time=time, buf=dapi2.buffer2str(buf), msg=msg)) #@UndefinedVariable
            
    def traceDapi(self, time, direction, buf, msg):
        if self.stop:return
        if msg.type() in (dapi2.MsgType.READ, dapi2.MsgType.WRITE):
            regs =  self.dapi.regs[msg.getAddr():msg.getAddr()+msg.getLength()//dapi2.REG_SIZE]
        elif msg.type() == dapi2.MsgType.COMMAND:
            return self.traceNormal(time, direction, buf, msg)
        else:
            return #self.traceNormal(time, direction, buf, msg)
        
        if direction == dapi2.DComTracingDirection.INGOING:
            if msg.isError():
                print(dapi2.TRACE_INERROR_COLOR, end='')
                regs = str(msg)
            else:
                print(dapi2.TRACE_INGOING_COLOR, end='')
                if isinstance(msg, (dapi2.WrittenRegMessage, dapi2.ValueRegMessage)) :
                    regs = ', '.join('{reg.name:s}=0x{v:04x} ({v:d})'.format(reg=r, v=msg.getRegValue(i), i=i) for i, r in enumerate(regs))
                else:
                    regs = '???'
            print(TRACE_INGOING_DAPI_FMT.format(time=time, buf=dapi2.buffer2str(buf), msg=msg, regs=regs), end='')
        else:
            if msg.isError():
                print(dapi2.TRACE_OUTERROR_COLOR, end='')
                regs = str(msg)
            else:
                print(dapi2.TRACE_OUTGOING_COLOR, end='')
                if isinstance(msg, dapi2.WriteRegMessage) :
                    regs = ', '.join('0x{v:04x}({v:d})=>{reg.name:s}'.format(reg=r, v=msg.getRegValue(i), i=i) for i, r in enumerate(regs))
                elif isinstance(msg, dapi2.ReadRegMessage):
                    regs = ', '.join('{reg.name:s}?'.format(reg=r) for r in regs)
                else:
                    regs = '???'
            print(TRACE_OUTGOING_DAPI_FMT.format(time=time, buf=dapi2.buffer2str(buf), msg=msg, regs=regs), end='')
        
        print(dapi2.TRACE_RESET_COLOR)
        
