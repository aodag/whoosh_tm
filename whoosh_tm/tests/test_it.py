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

            dm.add_document(
                title=u"First document", path=u"/a",
                content=u"This is the first document we've added!")
            dm.add_document(
                title=u"Second document", path=u"/b",
                content=u"The second one is even more interesting!")
            t.join(dm)
            transaction.commit()

            ix2 = open_dir(d.path)
            with ix2.searcher() as searcher:
                parser = QueryParser("content", ix2.schema)
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

            dm.add_document(
                title=u"First document", path=u"/a",
                content=u"This is the first document we've added!")
            dm.add_document(
                title=u"Second document", path=u"/b",
                content=u"The second one is even more interesting!")
            t.join(dm)
            transaction.abort()

            ix2 = open_dir(d.path)
            with ix2.searcher() as searcher:
                parser = QueryParser("content", ix2.schema)
                results = searcher.search(parser.parse('second'))
                self.assertEqual(len(results), 0)
