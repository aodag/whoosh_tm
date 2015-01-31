import unittest


class TestWhooshDataManager(unittest.TestCase):

    def _get_target(self):
        from whoosh_tm.datamanager import WhooshDataManager
        return WhooshDataManager

    def _make_one(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        target = self._make_one()
        self.assertIsNotNone(target)
