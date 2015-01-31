import threading
from transaction.interfaces import IDataManager
from zope.interface import implementer
# from whoosh.writing import BufferedWriter


lock = threading.Lock()


@implementer(IDataManager)
class WhooshDataManager(object):

    transaction_manager = None

    def __init__(self, index):
        self.index = index
        self.writer = None
        self.documents = []

    def reset(self):
        self.documents = []
        if self.writer is not None:
            self.writer.cancel()
            self.writer = None
        lock.release()

    def add_document(self, **fields):
        self.documents.append(fields)

    def abort(self, transaction):
        pass

    def tpc_abort(self, transaction):
        self.reset()

    def tpc_begin(self, transaction):
        lock.acquire()
        self.writer = self.index.writer()

    def commit(self, transaction):
        for document in self.documents:
            self.writer.add_document(**document)

    def tpc_vote(self, transaction):
        pass

    def tpc_finish(self, transaction):
        self.writer.commit()
        self.writer = None
        self.reset()

    def sortKey(self):
        return self.__class__.__name__
