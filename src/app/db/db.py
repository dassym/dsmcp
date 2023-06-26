'''

:author:  F. Voillat
:date: 2022-03-07 Creation
:copyright: Dassym SA 2021
'''

import logging
from pathlib import Path

from app.db.partner import DbStandardCustomer
import lxml.etree as ET
import re as RE

from ..common import USR_DATA_DIR
from .board import DbBoard
from .firmware import DbFirmwares, DbFirmware
from .partner import DbCustomer
from .configuration import DbConfiguration
from .production import DbBoardProduction
import dapi2


DB_DATA_FILE = 'data.xml'


class PrefixResolver(ET.Resolver):
    def __init__(self, prefix):
        if prefix[-1] != ':':
            prefix += ':'
        self.log = logging.getLogger('PrefixResolver[{0!s}]'.format(prefix))
        self.prefix = prefix

    def resolve(self, url, pubid, context):
        if url.startswith(self.prefix):
            path = Path(USR_DATA_DIR).joinpath(url[len(self.prefix):])
            self.log.debug(url + "->" + str(path))
            return self.resolve_filename(str(path),context)


class Database(object):

    R_FIRM = RE.compile(r".*_firm\.bin",)
    R_CFG = RE.compile(r".*_firm\.cfg",)

    def __init__(self, app, lang='en'):
        self._scanned_paths = []
        self._current_loading_path = None
        self.app = app
        self.board_class = None
        self.log = logging.getLogger('Database')
        self.log.debug('Construct')
        self.lang = lang
        self.boards = {}
        self.customers = {}
        self.productions = {}
        self.firmwares = DbFirmwares(self)
        self.firm_paths = []
        self.standard_cust = None
        self.configurations = []

    def clear(self):
        self.boards = {}
        self.customers = {}
        self.firmwares.clear()


    def _scanDir(self, path):


        def processFirmare(item):
            #self.log.debug(' > fpath = '+fpath)
            firmware = DbFirmware.fromBinary(self.firmwares, str(item))

            if firmware.type == 'full':
                return False
            if firmware.customer is None and not self.app.config.dev_mode:
                self.log.warning('Firmware without customer:'+item.name)
                #return False

            if self.board_class is not None and firmware.target != self.board_class.getName():
                return False
            self.firmwares.add(firmware)
            return True


        def processConfiguration(item):
            cfg = DbConfiguration.fromFile(str(item))
            self.configurations.append(cfg)


            return True

        if not path.exists():
            self.app.sayWarning(f'The path `{path}` does not exist!')
            return False
        if self._alreadySacanned(path):
            self.app.sayWarning(f'The path `{path}` has already been scanned!')
            return False

        fdata = Path(path).joinpath(DB_DATA_FILE)
        if fdata.exists():
            self.loadFile(fdata)

        for item in path.iterdir():
            if item.is_file():
                if self.R_FIRM.match(str(item)) is not None:
                    processFirmare(item)
                elif self.R_CFG.match(str(item)) is not None:
                    processConfiguration(item)

            elif item.is_dir():
                self._scanDir(item)

        self._scanned_paths.append(path)


    def _alreadySacanned(self, path):
        for p in self._scanned_paths:
            if p in path.parents:
                return True
        return False

    def discover(self, paths, board_class=None, clear=True):
        '''Discovers DSMCP data in the mentioned directories

        Args:
            paths (str, list, tuple): list of directories to scan
            board_class (class): If defined : filter data according the board class
            clear (bool): If `True` : clear all data before scan.
        '''
        if clear:
            self.clear()

        if isinstance(paths, str):
            opaths = [Path(paths)]
        else:
            paths = list(set(paths))
            paths.sort()
            opaths = [ Path(p).resolve() for p in paths ]

        self.board_class = board_class

        self.log.info('Discovers data in {:s}'.format(str(opaths)))

        for opath in opaths:
            self._scanDir(opath)




    def loadFile(self, path):
        self.log.debug('loadFile({0!s}).'.format(path))

        self._current_loading_path = path

        xparser = ET.XMLParser()
        xparser.resolvers.add( PrefixResolver('user') )

        with path.open() as f:
            self.app.sayMedium(f"Load data from XML file `{path!s}`")
            xtree = ET.parse(f, xparser)
            xtree.xinclude()
            xroot = xtree.getroot()

            for xboard in xroot.findall('board'):
                bid = xboard.get('id')
                oboard = DbBoard.fromXml(self, xboard, oid=bid)
                self.boards[oboard.id] = oboard


            for xcustomer in xroot.findall("standardcustomer"):
                ocustomer = DbStandardCustomer.fromXml(self, xcustomer)
                self.customers[ocustomer.id] = ocustomer
                self.standard_cust = ocustomer

            for xcustomer in xroot.findall("customer"):
                ocustomer = DbCustomer.fromXml(self, xcustomer)
                self.log.debug('loadFile:New customer `{1!s}`  ({0!s})'.format(path,ocustomer))
                self.customers[ocustomer.id] = ocustomer


            for xproduction in xroot.findall("production"):
                oproduction = DbBoardProduction.fromXml(self, xproduction)
                self.log.debug('loadFile:Production `{0!s}`'.format(oproduction.id))
                self.productions[oproduction.id] = oproduction

        self._current_loading_path = None

    def getCurrentLoadingPath(self):
        return self._current_loading_path

    def getCustomers(self, standard=False):
        return [ x for x in self.customers.values() if (standard or not x.standard)]

    def getCustomer(self, cid, insensitive=False):
        if cid is None or cid == '*':
            return None
        try:
            if insensitive:
                CID = cid.upper()
                for k,v in self.customers.items():
                    if k.upper() == CID:
                        return v
                raise KeyError()
            else:
                return self.customers[cid]
        except KeyError:
            self.log.warning(f"getCustomer:unknown customer `{cid}` creation !")
            cust = DbCustomer(self, oid=cid, name=cid)
            self.customers[cust.id] = cust
            return cust


    def getBoard(self, bid_or_board, insensitive=False):

        def getById(bid):
            try:
                if insensitive:
                    BID = bid.upper()
                    for k,v in self.boards.items():
                        if k.upper() == BID:
                            return v
                    raise KeyError()
                else:
                    return self.boards[bid]
            except KeyError:
                raise KeyError(f"Board `{bid!s}` not found in database!")

        def getByClass(board_class):
            if not isinstance(board_class,str):
                board_class = board_class.__name__
            for b in self.boards.values():
                if board_class == b.board_class.__name__:
                    return b
            raise KeyError(f"Board class`{board_class!s}` not found in database!")


        def getByOject(board):
            for b in self.boards.values():
                if isinstance(board,b.board_class):
                    return b
            raise KeyError(f"Board `{board.__class__!s}` not found in database!")

        if bid_or_board is None:
            return None
        if isinstance(bid_or_board, dapi2.DBoard):
            return getByOject(bid_or_board)
        try:
            return getByClass(bid_or_board)
        except KeyError:
            return getById(bid_or_board)





    def findBoards(self, customer=None):
        if customer is None or not customer.boards:
            return (self.boards.values(), [])
        else:
            custboards = list(x.board for x in customer.boards)
            r = ([],[])
            for b in self.boards.values():
                r[int(not b in custboards)].append(b)
        return r

    def getBoardVariant(self, vid, board=None, insensitive=False):
        if board is not None:
            return board.getVariant(vid,insensitive=insensitive)
        else:
            for b in self.boards.values():
                try:
                    return b.getVariant(vid,insensitive=insensitive)
                except KeyError:
                    pass
        raise KeyError(f'Variant `{vid!s}` not found in database!')

    def findBoardVariants(self, board, customer=None):
        return board.findVariants(customer)

    def isEmpty(self):
        return len(self.boards) == 0 and len(self.customers) == 0


    @property
    def db(self):
        return self



