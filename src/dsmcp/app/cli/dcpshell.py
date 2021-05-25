'''

:author: fv
:date: Created on 24 mars 2021
'''
import cmd
import datetime as DT

import dapi2

from dapi2.derror import DApiComError
from dboard.common import DBoardPreferedDapiMode, SystemModeConfig
from dapi2.common import wordToVersion, wordToDate, versionToStr
from dboard.generic import GenericBoard
from dboard.base import DBoard
from PyQt5.QtCore import QCoreApplication




def valToWord(v):
    '''convert a value in 16-bits integer (word)
    
    The value can be expressed as :
    - decimal without prefix
    - hexadecimal with prefix :code:`0x`
    - binary with prefix :code:`0b`
    - octal with prefix :code:`0o`  
    
    :param str v: The value to convert
    :return: An integer
    :rtype: int
    ''' 
    if not isinstance(v, int):
        if v[:1] == '0x':
            v = int(v[2:],16) & 0xFFFF
        elif v[:1] == '0b':
            v = int(v[2:],2) & 0xFFFF
        elif v[:1] == '0o':
            v = int(v[2:],8) & 0xFFFF
        else:
            v = int(v,10) & 0xFFFF
    return v

def valToDate(v):
    '''Convert value to date.
    
    :param str v: The value to convert
    :return: A date
    :rtype: date
    '''
    return DT.datetime.strptime(v, '%Y-%m-%d')

def valToVersion(v):
    '''Convert value to version tuple
    
    :param str v: The value to convert
    :return: An n-tuple containing version numbers
    :rtype: tuple
    '''
    v = v.split('.')
    return tuple((valToWord(x) for x in v))

def parse(arg):
    'Convert a series of zero or more numbers to an argument tuple'
    return tuple(map(int, arg.split()))


class DcpShell(cmd.Cmd):
    prompt = '>'
    file = None
    use_rawinput = False
    
    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return QCoreApplication.translate('DcpShell',text, disambiguation, n)    

    def __init__(self, app, completekey='tab', stdin=None, stdout=None):
        super().__init__(completekey, stdin, stdout)
        
        self.app = app
        
    def onecmd(self, line):
        try:
            return super().onecmd(line)
        except DApiComError as e:
            print(self.tr("*ERROR 0x{0:02X} ({0:d}): {1:s}").format(e.errorno[0], e.label))
        except (KeyError, ValueError) as e:
            print(self.tr("*ERROR: ")+str(e))
            return False # don't stop



    def _show_cfg(self):
        '''Shows application's configuration.'''
        print("""\033[0mConfiguration:
  Communication: \033[1m{com!s}\033[0m
  DAPI preferred mode: \033[1m{board.dmode.name:s}\033[0m             
            """.format(com=self.app.dcom, dapi=self.app.dapi, board=self.app.board))
    
    def _show_board(self):
        '''Shows board's information and status.'''
        self.app.board.getRegisters('system')
        self.app.board.getRegisters('psvr','wer', refresh=True)
        #self.app.dapi.readRegs(self.app.board.getRegisters('system'))
        print("""\033[0mBoard {board!s}:
  Factory data: SN:\033[1m{snr:05d}\033[0m ; Date:\033[1m{fdr:s}\033[0m ; Hardware:\033[1m{hvr:s}\033[0m
  Firmware: \033[1m{svr:s}\033[0m ; Date:\033[1m{fbdr:s}\033[0m  
  BIOS: \033[1m{bvr:s}\033[0m ; Date:\033[1m{bbdr:s}\033[0m  
        """.format(
                board=self.app.board,
                snr=self.app.board.regs.snr.value,
                fdr=wordToDate(self.app.board.regs.fdr.value).isoformat(),
                hvr=versionToStr(wordToVersion(self.app.board.regs.hvr.value)),
                svr=versionToStr(self.app.board.getFirmwareVersion()),
                fbdr=self.app.board.getFirmwareDate().isoformat(),
                bvr=versionToStr(wordToVersion(self.app.board.regs.bvr.value)),
                bbdr=wordToDate(self.app.board.regs.bbdr.value).isoformat(), 
                )
        )
        
        firm = self.app.firmwares.get(
                        self.app.board,
                        self.app.board.getFirmwareTag()
                        #self.app.board.getFirmwareVersion(),
                        #self.app.board.getFirmwareDate()
                        )
        if firm is not None:
            print("  Firmware : " + str(firm))
        else:
            print("  Firmware : undefined (0x{0:04x})".format(self.app.board.getFirmwareTag()) )
            
        if self.app.board.getError():
            print("  Error status: \033[1m0x{0:04X}\033[0m".format(self.app.board.getError()))
        print("  Reset type: "+self.app.board.getLastReset().name )
        print("  Connection access level: "+self.app.board.getAccessLevel().name )
        print("  Power supply: \033[1m{0:.02f}\033[0mV".format(self.app.board.getPowerSupply()))
        if self.app.board.isOnStandby(): 
            print("  On standby")
        else:
            print("  Workspace : {0!s}".format( self.app.board.getWorkspace()))
        if len(self.app.board.workspaces) == 1:
            print("  \033[31mWARNING: No workspace found!\033[0m")
            
    def _show_ws(self):
        '''Shows workspaces's information and status.'''
        pass

    def _show_motor(self):
        '''Shows motor's status.'''
        if self.app.board.isOnStandby():
            print('Standby.')
        else:
            self.app.board.getRegisters('scr','acr','smr','msr','a256dcr','a256dvr', 'lsr','rsr', refresh=True)
            mode = self.app.board.getSystemModeConfiguration()
            print("""\033[0mMotor:
  Set points: speed = \033[1m{r.scr.value:d}\033[0mrpm ; acceleration = \033[1m{r.acr.value:d}\033[0mkrpm/s
  Mode: \033[1m0x{r.smr.value:04x}\033[0m = {m!s} 
  Requested speed = \033[1m{r.rsr.value:d}\033[0mrpm ; Logical speed = \033[1m{r.lsr.value:d}\033[0mrpm
  Real speed = \033[1m{r.msr.value:d}\033[0mrpm ; current = \033[1m{r.a256dcr.value:d}\033[0mmA ; voltage = \033[1m{r.a256dvr.value:d}\033[0mmV
""".format(r=self.app.dapi.regs, m=mode))
            
            
    
    def do_cfg(self, arg):
        '''Modify or show the application configuration.
        Usage: cfg [dmode {c,r}] [show]
        dmode c : set the preferred DAPI mode to `command`. 
        dmode r : set the preferred DAPI mode to `register`.
        show : display the appication configuration
        '''
        args = arg.lower().split()
        
        if args[0] == 'dmode':
            if args[1] == 'c':
                self.app.board.dmode = DBoardPreferedDapiMode.COMMAND
            elif args[1] == 'r':
                self.app.board.dmode = DBoardPreferedDapiMode.REGISTER
            else:
                raise ValueError('Invalid DAPI2 mode!')
        elif args[0] == 'show':
            self._show_cfg()
    
    def do_sb(self, arg):
        '''Shows information about the board.
        Usage: sb'''
        self._show_board()

    def do_sm(self, arg):
        '''Shows information about the motor.
        Usage: sm'''
        self._show_motor()
    
    def do_sc(self, arg):
        '''Shows information about the application configuration.
        Usage: sc'''
        self._show_cfg()
    
    def do_show(self, arg):
        '''Shows information about an item.
        Usage: show {cfg, board, ws, motor}
        '''
        args = arg.lower().split()
        if args[0] == 'cfg':
            self._show_cfg()
        elif args[0] == 'board':
            self._show_board()
        elif args[0] == 'ws':
            self._show_ws()
        elif args[0] == 'motor':
            self._show_motor()
        else:
            raise ValueError('Invalid item to show!')
        
    def do_connect(self, arg):
        '''Connect to board.
        Usage: connect {no, user, service, factory}
        '''
        level = dapi2.DApiAccessLevel[arg.upper()]
        self.app.board.connect(level, level.passwd )
        self.prompt = level.name[0]+'>'
        
    def do_cu(self, arg):
        '''Connect to board with `user` level.
        Usage: cu
        '''
        self.do_connect('user')

    def do_cs(self, arg):
        '''Connect to board with `service` level.
        Usage: cs
        '''
        self.do_connect('service')

    def do_cf(self, arg):
        '''Connect to board with `factory` level.
        Usage: cf
        '''
        self.do_connect('factory')

    def do_disconnect(self, arg):
        '''Disconnect board.
        Usage: disconnect'''
        self.app.board.disconnect()
        self.prompt = '>'
        
    def do_start(self, arg):
        '''Starts the motor.
        Usage: start [<speed>]
        
        <speed> : optional argument to fix new speed set point.'''
        args = parse(arg)
        try:
            speed = args[0]
        except:
            speed = None
        self.app.board.motorStart(speed)
        
    def do_mode(self, arg):
        '''Change system mode 
        Usage: mode {set,clear} <flag> [<flag> ...]
        
        <flag> : is the configuration flag : {START, HOLDING, ROCKING, AUTOBOOST, AUTOSTOP, AUTOREVERSE, REVERSE, QUADRATIC, LIGHT, FREEWHEEL, INDIRECT, LIGHTAUTO}        
        '''
        
        flags = self.app.board.getSystemModeConfiguration()
        print('Actual system mode: \033[1m0x{f.value:04x}\033[0m = {f!s} '.format(f=flags) )
        to_set = True
        
        args = list(a.upper() for a in arg.split())
        if len(args) > 0:
            try:
                for arg in args:
                    if arg == 'SET':
                        to_set = True 
                    elif arg == 'CLEAR':
                        to_set = False
                    else:
                        if to_set:
                            flags |= SystemModeConfig[arg]
                        else:
                            flags &= ~SystemModeConfig[arg]
                self.app.board.setSystemModeConfiguration(flags)
                print('New system mode: \033[1m0x{f.value:04x}\033[0m = {f!s} '.format(f=flags) )
            except Exception:
                print("""
Malformed command line. Usage: mode {set,clear} <flag> [<flag> ...]
Example: mode set indirect clear light""")
                return False                    
        
    def do_stop(self, arg):
        '''Stops the motor.
        Usage: stop'''
        self.app.board.motorStop()
        
    def do_light(self, arg):
        '''Sets light
        Usage: light <cmd>
        
        <cmd> : is light command.   
        '''
        args = (a.lower() for a in arg.split())
        for a in args:
            if a == 'on':
                self.app.board.lightOn() 
            elif a == 'off':
                self.app.board.lightOff()
            if a == 'auto':
                self.app.board.lightAuto(True)
            elif a == 'manu':
                self.app.board.lightAuto(False)
            if a.isdigit():
                self.app.board.lightIntensity(int(a))
    
    def do_ws0(self, arg):    
        '''Go to standby mode
        Usage: ws0
        ''' 
        self.app.board.setWorkspace(0)

    def do_ws1(self, arg):    
        '''Go to workspace #1
        Usage: ws1
        ''' 
        self.app.board.setWorkspace(1)

    def do_ws2(self, arg):    
        '''Go to workspace #2
        Usage: ws2
        ''' 
        self.app.board.setWorkspace(2)
    
    def do_ws(self, arg):
        '''Change the active workspace
        Usage: ws <workspace>
        
        <workspace> is the Workspace number (=PAR)
        ''' 
        self.app.board.setWorkspace(int(arg))
        
    def do_get(self, arg):
        '''Gets the value of one or more registers.
        Usage: get <reg> [;<reg> ...]
        
        <reg> is the register name
        '''
        args = (a.lower() for a in arg.split())
        regs = self.app.board.getRegisters(*args)
        print("=> "+' ; '.join( r.toString() for r in regs) )
        #print("=> "+' ; '.join( "{0:s}=0x{1:04x}({1:d})".format(r.name, r.value) for r in regs) )
        
    def do_set(self, arg):
        '''Sets the value of one or more registers.
        Usage: set <reg>=<val> [;<reg>=<val> ...]
        
        <reg> is the register name
        <val> is the new value to set
        ''' 
        arg = arg.replace(' ', '').lower()
        try:
            args = dict([ (k,v) for k,v in [ tuple(a.split('=')) for a in arg.split(';') ]])
            
            for k, v in args.items():
                if isinstance(v, str):
                    if v[:2] == '0x':
                        args[k] = int(v[2:],16) & 0xFFFF
                    elif v[:2] == '0b':
                        args[k] = int(v[2:],2) & 0xFFFF
                    else:
                        args[k] = int(v,10) & 0xFFFF
            
        except Exception:
            print("""
Malformed command line. Usage: set reg <reg> = <value> [; <reg> = <value>  ... ]
Where:
  <reg> is the register name
  <value> is the register the value expressed in decimal (12), hexadecimal (0xC) or binary (0b1100).""")
            return False
        self.app.board.setRegisters(**args, synchronous=True)
        # r = []
        # for k,v in args.items():
            # r.append("{0:s} = 0x{1:04x} ({1:d})".format(k, self.app.board.regs(k).value ))
        # print("  "+" ; ".join(r))
        regs = self.app.board.getRegisters(*args.keys())
        print("=> "+' ; '.join( "{0:s}=0x{1:04x}({1:d})".format(r.name, r.value) for r in regs) )
        
        
    def _flashCallback(self, i, n):
        p = i/n
        print('\033[2K\r{0!s} [{1:50s}] {2:6.2f}% ({3:d}/{4:d})'.format('Writing in progress', '#'*int(round(50*p)), 100*p, i, n), end='')
        
    def do_firm(self, arg):
        '''Rewrites the firmware into the board ROM.
        Usage: firm
        '''
        
        if isinstance(self.app.board, GenericBoard):  
            print("Choice the board family target:")
            board_classes = list(DBoard.getBoardClasses().values())
            for i, board_class in enumerate(board_classes):
                print("{0:3d} - {1:s}".format(i+1, board_class.getName()))
            print("Enter 1 to {0:d} to choice board family or 0 to abort. [0]".format(i))
            s = input()
            if s == '' or s == '0':
                return False    
            board_class = board_classes[int(s,10)-1]    
        else:
            board_class = self.app.board.__class__
        
        print("Choice the firmware to write into {0:s} ROM:".format(board_class.getName()))
        firmwares = list(self.app.firmwares.find(board_class))
        for i, firm in enumerate(firmwares):
            print("{0:4d} - {1!s} ".format(i+1, firm)) 
        print("Enter 1 to {0:d} to choice the firmware or 0 to abort. [0]".format(i+1))
        s = input()
        if s == '' or s == '0':
            return False
        i = int(s,10)
        firm = firmwares[i-1]
        print("Are your sure to overwrite the {0:s} board firmware with this {1!s} (Yes / No)? y[n]".format(board_class.getName(), firm))
        s = input()
        if s.lower() == 'y' :
            self.app.tracer.stop = True
            try:
                self.app.board.flashFirm(firm, self._flashCallback)
            finally:
                self.app.tracer.stop = False
            print('\033[2K\rFirmware update operation completed successfully.')
        else:
            return False
        
    def do_factory(self, arg):
        '''Rewrites factory data into the board E²PROM.
        Usage: factory [sn=<sn>][;fd=<fd>][;hv=<hv>]
        
        Where:
          <sn> is the serial number
          <fd> is the date in ISO format (YYYY-MM-DD)
          <hv> is the major and minor hardware version separated by a dot (.)      
        '''
        
        data = list(self.app.board.getFactoryData())
        arg = arg.replace(' ', '').lower()
        print('Actual factory data: SN:\033[1m{sn:05d}\033[0m ; Date:\033[1m{fd:s}\033[0m ; Hardware:\033[1m{hv[0]:d}.{hv[1]:02d}\033[0m'.format(sn=data[0], fd=data[1].isoformat(), hv=data[2] ) )
        if len(arg) > 0:  
            try:
                args = dict([ (k,v) for k,v in [ tuple(a.split('=')) for a in arg.split(';') ]])
                for k, v in args.items():
                    if k == 'sn':
                        data[0] = valToWord(v)
                    elif k == 'fd':
                        data[1] = valToDate(v)
                    elif k == 'hv':
                        data[2] = valToVersion(v)
                self.app.board.setFactoryData(*data)
            except Exception:
                print("""
    Malformed command line. Usage: factory [sn=<sn>][;fd=<fd>][;hv=<hv>]
    Example: factory sn=01234 ; fd=2021-05-1 ; hv=5.01""")
                return False
        
        
        
    def do_bye(self, arg):
        '''Terminates the shell'''
        return self.do_exit(arg)

    def do_exit(self, arg):
        '''Terminates the shell'''
        self.close()
        return True
    
    def close(self):
        if self.file:
            self.file.close()
            self.file = None    