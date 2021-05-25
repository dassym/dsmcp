'''

:author: fv
:date: Created on 19 mars 2021
'''
import re as RE

import chardet
import os.path
from PyQt5.QtCore import QCoreApplication




MAX_RANGE_SIZE = 2000
SN_LASTNUM_RE = RE.compile(r'(?:[^\d]*(\d+)[^\d]*)+')

def tr(text, disambiguation=None, n=-1):
    return QCoreApplication.translate('@default',text, disambiguation, n)


def configStr(config, sep='\n\t'):
    l = [ str(x) +" = "+ ( str(config.__dict__[x]) if config.__dict__[x] != None else '<None>' ) + ' ('+type(config.__dict__[x]).__name__+')'   for x in sorted(config.__dict__.keys())  ]
    return sep.join( l )

def getXmlName(xelement, lang='en'):
    xdescr = xelement.find( "name[@lang='{}']".format(lang)  )
    if xdescr is None:
        xdescr = xelement.find( "name[1]"  )
    if xdescr is not None:
        return xdescr.text
    return None


def getXmlDescr(xelement, lang='en'):
    xdescr = xelement.find( "descr[@lang='{}']".format(lang)  )
    if xdescr is None:
        xdescr = xelement.find( "descr[1]"  )
    if xdescr is not None:
        return xdescr.text
    return None

def str2version(text):
    if text is not None and len(text)>0:
        m = RE.search(r'\D*(\d+)\.(\d{2,})', text)
        if m==None:
            raise Exception("Invalid version : {0!s}".format(text))  
        return  ( int(m.group(1)) , int(m.group(2)) )
    else:
        return None
    
def version2str(version):
    try:
        return "{0:d}.{1:02d}".format(version[0],version[1])
    except TypeError:
        return None

def str2bool(text):
    return text is not None and len(text)>0 and text.lower()[0] in ('y', 't', '1', 'o')


def increment(s, inc=1):
    '''Recherche la dernière séquence de digits d'une chaîne est l'incrémente.
    :param str s: Chaîne de caractères à incrémenter de inc.
    :praam int inc: Valeur de l'incrément. Par défaut = 1.
    '''
    m = SN_LASTNUM_RE.search(s)
    if m:
        n = str(int(m.group(1))+inc)
        start, end = m.span(1)
        s = s[:max(end-len(n), start)] + n + s[end:]
    return s


def genrateSnList( start, n, inc=1):
    ret = set()
    for i in range(int(n)): #@UnusedVariable
        ret.add( start )
        start = increment(start, inc)
    return ret

def snFromRange(r, inc=1):
    '''
    Retourne une liste de numéros de série depuis une chaîne de caractères au format A-B ou A:C. Où A et B sont les bornes de la plage, C le nombre de SN à produire.
    :param str r: Plage de SN au format A-B ou A:C. A=SN de début, B=SN de fin, C=nombre de SN.
    :param int inc:  Valeur de l'incréement. Par défaut = 1.
    :return: Une liste de SN [A, A+inc, A+2*inc, ..., B]
    '''
    ret = set()
    if ':' in r:
        (start,count)=r.split(':',2)
        for i in range(int(count)):
            ret.add( start )
            start = increment(start, inc)
    elif '-' in r:
        (start,end)=r.split('-',2)
        ret.add( start.strip() )
        i = 0
        end = end.strip()            
        if end < start :
            end, start = start, end
        
        last = start
        while True:
            n = increment( last, inc )
            last = n
            if n <= end :
                ret.add(n)
                i += 1
                if i > MAX_RANGE_SIZE:
                    raise Exception('La plage de SN {} comporte plus de {} numéros!'.format(r,MAX_RANGE_SIZE))
            else:
                break
    else:
        ret.add(r)
    return ret

def snFromArg(arg, inc=1, exclude=[]):
    '''
    :param str arg: Argument de la ligne de commande au format A-B ou A:C. Où A et B sont les bornes de la plage, C le nombre de SN à produire.
    :param int inc: Valeur de l'incréement. Par défaut = 1. 
    :return: Une liste de SN [A, A+inc, A+2*inc, ..., B]
    '''

    ret = set()
    
    for r0 in arg:
        for r1 in r0.split(';'):
            ret |= snFromRange(r1, inc)
            
    
    for r0 in exclude:
        for r1 in r0.split(';'):
            ret -= snFromRange(r1, inc)
    
    return ret


def snFromFile(fpath, inc=1):
    global LOG
    ret = set()
    raw = open(fpath, 'rb').read(min(32, os.path.getsize(fpath)))
    result = chardet.detect(raw)
    encoding = result['encoding']
    if encoding in ('UTF-16BE', 'UTF-16LE') :
        raise Exception( 'Encodage UTF-16 non supporté !' ) 
    with open(fpath, 'r', encoding=encoding) as f:
        for sn in f:
            sn = sn.strip()            
            sn = snFromRange(sn, inc)
            ret |= sn
    return ret

def compactSnList( sn_list ):
    '''
    Générateur d'une liste de tuples représentant toutes les plages d'une liste de numéros de série.
    @param sn_list Liste des numéros de série [a, b, c, ...].
    @return Liste de tuples [ (<from> ,<to>), ... ] 
    '''
    sn_list = sorted(sn_list)
    i = 0
    for j in range(1,len(sn_list)):
        if sn_list[j] > increment(sn_list[j-1]):
            yield (sn_list[i],sn_list[j-1])
            i = j
    yield (sn_list[i], sn_list[-1])
    
    
def compactSnListToStr(sn_list):
    s = []
    for x in sn_list:
        if x[0] == x[1]:
            s.append( x[0] )
        elif increment(x[0]) == x[1]:
            s.append( x[0] + ',' + x[1] )
        else:
            s.append( x[0] + '-' + x[1] )
    return ';'.join( s )

