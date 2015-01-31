from transaction.interfaces import IDataManager
from zope.interface import implementer
from whoosh.writing import BufferedWriter


@implementer(IDataManager)
class WhooshDataManager(object):

    transaction_manager = None

    def __init__(self, index):
        self.index = index
        self.writer = None
        self.documents = []

    def abort(self, transaction):
        pass

    def tpc_abort(self, transaction):
        self.documents = []
        if self.writer is not None:
            self.writer.cancel()
            self.writer = None

    def tpc_begin(self, transaction):
        self.writer = BufferedWriter(self.index)

    def commit(self, transaction):
        for document in self.documents:
            self.writer.add_document(**document)

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        self.writer.commit()
        self.writer.close()

    def sortKey(self):
        return self.__class__.__name__
