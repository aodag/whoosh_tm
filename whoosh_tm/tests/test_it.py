import unittest
from testfixtures import TempDirectory
from whoosh.fields import Schema, TEXT, ID

dummy_schema = Schema(title=TEXT(stored=True),
                      path=ID(stored=True),
                      content=TEXT)


class TestIt(unittest.TestCase):

    def test_it(self):
        import transaction
        from whoosh_tm.datamanager import WhooshDataManager
        from whoosh.qparser import QueryParser
        from whoosh.index import create_in, open_dir
        with TempDirectory() as d:
            ix = create_in(d.path, dummy_schema)
            dm = WhooshDataManager(ix)
            t = transaction.get()
            t.join(dm)

            dm.add_document(
                title=u"First document", path=u"/a",
                content=u"This is the first document we've added!")
            dm.add_document(
                title=u"Second document", path=u"/b",
                content=u"The second one is even more interesting!")
            transaction.commit()

            ix2 = open_dir(d.path)
            with ix2.searcher() as searcher:
                parser = QueryParser("content", ix2.schema)
                results = searcher.search(parser.parse('second'))
                self.assertEqual(len(results), 1)

                self.assertEqual(results[0]["title"], "Second document")

    def test_multi(self):
        import transaction
        from whoosh_tm.datamanager import WhooshDataManager
        from whoosh.qparser import QueryParser
        from whoosh.index import create_in, open_dir
        import threading

        with TempDirectory() as d:
            ix1 = create_in(d.path, dummy_schema)
            ix2 = open_dir(d.path)

            def add_document1():
                dm1 = WhooshDataManager(ix1)
                t = transaction.get()
                t.join(dm1)
                dm1.add_document(
                    title=u"First document", path=u"/a",
                    content=u"This is the first document we've added!")
                transaction.commit()

            def add_document2():
                dm2 = WhooshDataManager(ix2)
                t = transaction.get()
                t.join(dm2)

                dm2.add_document(
                    title=u"Second document", path=u"/b",
                    content=u"The second one is even more interesting!")
                transaction.commit()

            th1 = threading.Thread(target=add_document1)
            th2 = threading.Thread(target=add_document2)
            th1.start()
            th2.start()
            th1.join()
            th2.join()

            ix3 = open_dir(d.path)
            with ix3.searcher() as searcher:
                parser = QueryParser("content", ix3.schema)
                results = searcher.search(parser.parse('second'))
                self.assertEqual(len(results), 1)

                self.assertEqual(results[0]["title"], "Second document")

    def test_abort(self):
        import transaction
        from whoosh_tm.datamanager import WhooshDataManager
        from whoosh.qparser import QueryParser
        from whoosh.index import create_in, open_dir
        with TempDirectory() as d:
            ix = create_in(d.path, dummy_schema)
            dm = WhooshDataManager(ix)
            t = transaction.get()
            t.join(dm)

            dm.add_document(
                title=u"First document", path=u"/a",
                content=u"This is the first document we've added!")
            dm.add_document(
                title=u"Second document", path=u"/b",
                content=u"The second one is even more interesting!")
            transaction.abort()

            ix2 = open_dir(d.path)
            with ix2.searcher() as searcher:
                parser = QueryParser("content", ix2.schema)
                results = searcher.search(parser.parse('second'))
                self.assertEqual(len(results), 0)

    def test_multi_with_abort(self):
        import transaction
        from whoosh_tm.datamanager import WhooshDataManager
        from whoosh.qparser import QueryParser
        from whoosh.index import create_in, open_dir
        import threading

        with TempDirectory() as d:
            ix1 = create_in(d.path, dummy_schema)
            ix2 = open_dir(d.path)

            def add_document1():
                dm1 = WhooshDataManager(ix1)
                t = transaction.get()
                t.join(dm1)
                dm1.add_document(
                    title=u"First document", path=u"/a",
                    content=u"This is the first document we've added!")
                transaction.abort()

            def add_document2():
                dm2 = WhooshDataManager(ix2)
                t = transaction.get()
                t.join(dm2)

                dm2.add_document(
                    title=u"Second document", path=u"/b",
                    content=u"The second one is even more interesting!")
                transaction.abort()

            th1 = threading.Thread(target=add_document1)
            th2 = threading.Thread(target=add_document2)
            th1.start()
            th2.start()
            th1.join()
            th2.join()

            ix3 = open_dir(d.path)
            with ix3.searcher() as searcher:
                parser = QueryParser("content", ix3.schema)
                results = searcher.search(parser.parse('second'))
                self.assertEqual(len(results), 0)
