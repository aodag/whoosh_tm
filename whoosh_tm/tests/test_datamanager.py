import unittest
from unittest import mock
from zope.interface.verify import verifyObject


class TestWhooshDataManager(unittest.TestCase):

    def _get_target(self):
        from whoosh_tm.datamanager import WhooshDataManager
        return WhooshDataManager

    def _make_one(self, *args, **kwargs):
        return self._get_target()(*args, **kwargs)

    def test_it(self):
        from transaction.interfaces import IDataManager
        index = mock.Mock()
        target = self._make_one(index)
        self.assertIsNotNone(target)
        verifyObject(IDataManager, target)
