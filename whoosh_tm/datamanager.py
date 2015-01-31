from transaction.interfaces import IDataManager
from zope.interface import implementer


@implementer(IDataManager)
class WhooshDataManager(object):
    def __init__(self):
        pass
