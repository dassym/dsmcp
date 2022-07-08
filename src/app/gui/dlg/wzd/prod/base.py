'''

:author:  F. Voillat
:date: 2022-06-15 Creation
:copyright: Dassym SA 2021
'''
from PyQt5.Qt import QCoreApplication

from ..common import BaseDialog, BaseWizardPage  # @UnusedImport


class WizardProdStartup(BaseDialog): 

    @classmethod
    def tr(cls, text, disambiguation=None, n=-1):
        return QCoreApplication.translate('WizardProdStartup', text, disambiguation, n)       
