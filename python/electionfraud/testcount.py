# -*- python -*-

import unittest

import electionfraud.countmethod as efcm
import electionfraud.testdata as eftd

class CountMethodTest(unittest.TestCase):
    pass

class TestFPTP(CountMethodTest):
    
    def setUp(self):
        self.cm = efcm.FirstPastThePost()
        pass

    def test_fptp(self):
        self.cm.count(eftd.TN_FPTP_100)
        self.assertEqual(self.cm.residue, len(eftd.TN_FPTP_100))
        for choice in eftd.TENNESSEE.keys():
            self.assertEqual(self.cm.results[choice], eftd.TENNESSEE[choice])

class TestIRV(CountMethodTest):
    
    def setUp(self):
        self.cm = efcm.InstantRunoffVoting()

    def test_irv_tennessee(self):
        self.cm.count(eftd.TN_IRV_100)
        # round 0
        self.assertEqual(self.cm.residue[0][eftd.chattanooga], 15)
        self.assertEqual(self.cm.residue[0][eftd.knoxville], 17)
        self.assertEqual(self.cm.residue[0][eftd.nashville], 26)
        self.assertEqual(self.cm.residue[0][eftd.memphis], 42)
        # round 1
        self.assertEqual(self.cm.residue[1][eftd.nashville], 26)
        self.assertEqual(self.cm.residue[1][eftd.knoxville], 32)
        self.assertEqual(self.cm.residue[1][eftd.memphis], 42)
        # round 2
        self.assertEqual(self.cm.residue[2][eftd.memphis], 42)
        self.assertEqual(self.cm.residue[2][eftd.knoxville], 58)
        # final
        self.assertEqual(self.cm.results[eftd.memphis], 42)
        self.assertEqual(self.cm.results[eftd.knoxville], 58)
        # stupid sanity
        self.assertEqual(self.cm.results, self.cm.residue[-1])
        

if __name__ == '__main__':
    unittest.main()
