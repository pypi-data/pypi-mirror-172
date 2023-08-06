import os
from followeraudit.FauditAPIclient import FauditAPIclient
import unittest

class test_bytesviwapi(unittest.TestCase):

    def setUp(self):
        # your private API key.
        key = os.environ.get("AUDIT_API_TOKEN")
        self.api = FauditAPIclient(key)

    def test_newaudit_api(self):
        response = self.api.newaudit(username='iampiyushkhatri')
        self.assertEqual(response['status'], 'success')

    def test_bulkaudit_api(self):
        response = self.api.bulkaudit(username=['arjun077','iampiyushkhatri','RobertDowneyJr'])
        self.assertEqual(response['status'], 'success')

    
    def test_getaudit_api(self):
        response = self.api.auditstatus(audit_id='daa69a4e0a5dc4b4c0ddb3218fd479a2')
        self.assertEqual(response['status'], 'success')
