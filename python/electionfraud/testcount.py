# -*- python -*-

import collections
import unittest

import electionfraud.testdata as eftd

import electionfraud.countmethod.borda as borda
import electionfraud.countmethod.bucklin as bucklin
import electionfraud.countmethod.contingent as cv
import electionfraud.countmethod.coombs as coombs
import electionfraud.countmethod.exception as cmx
import electionfraud.countmethod.fptp as fptp
import electionfraud.countmethod.irv as irv


class CountMethodTest(unittest.TestCase):
    pass

class TestFPTP(CountMethodTest):
    
    def setUp(self):
        self.cm = fptp.FirstPastThePost()
        pass

    def test_premature(self):
        self.assertRaises(cmx.IncompleteCount, self.cm.leader)

    def test_fptp(self):
        self.cm.count(eftd.TN_FPTP_100)
        self.assertEqual(self.cm.residue, len(eftd.TN_FPTP_100))
        for choice in eftd.TENNESSEE.keys():
            self.assertEqual(self.cm.results[choice], eftd.TENNESSEE[choice])

class TestIRV(CountMethodTest):
    
    def setUp(self):
        self.cm = irv.InstantRunoffVoting()

    def test_premature(self):
        self.assertRaises(cmx.IncompleteCount, self.cm.leader)
    
    def test_irv_tennessee(self):
        self.cm.count(eftd.TN_IRV_100)
        # invariant
        self.assertEqual(self.cm.results, self.cm.residue[-1])
        # initial round 0
        self.assertEqual(self.cm.residue[0][eftd.chattanooga], 15)
        self.assertEqual(self.cm.residue[0][eftd.knoxville], 17)
        self.assertEqual(self.cm.residue[0][eftd.nashville], 26)
        self.assertEqual(self.cm.residue[0][eftd.memphis], 42)
        # round 1
        self.assertEqual(self.cm.residue[1][eftd.nashville], 26)
        self.assertEqual(self.cm.residue[1][eftd.knoxville], 32)
        self.assertEqual(self.cm.residue[1][eftd.memphis], 42)
        # final round 2
        self.assertEqual(self.cm.residue[2][eftd.memphis], 42)
        self.assertEqual(self.cm.residue[2][eftd.knoxville], 58)


class TestCoombs(CountMethodTest):

    def setUp(self):
        self.cm = coombs.CoombsMethod()

    def test_premature(self):
        self.assertRaises(cmx.IncompleteCount, self.cm.leader)

    def test_coombs_tennessee(self):
        self.cm.count(eftd.TN_IRV_100)
        # invariant
        self.assertEqual(self.cm.results, self.cm.residue[-1])
        # initial round 0
        leaders, trailers = self.cm.residue[0]
        self.assertEqual(leaders[eftd.memphis], 42)
        self.assertEqual(leaders[eftd.nashville], 26)
        self.assertEqual(leaders[eftd.knoxville], 17)
        self.assertEqual(leaders[eftd.chattanooga], 15)
        self.assertEqual(trailers[eftd.memphis], 58)
        self.assertEqual(trailers[eftd.knoxville], 42)
        # final round 1
        leaders, trailers = self.cm.results
        self.assertEqual(leaders[eftd.nashville], 68)
        self.assertEqual(leaders[eftd.knoxville], 17)
        self.assertEqual(leaders[eftd.chattanooga], 15)
        self.assertEqual(trailers[eftd.knoxville], 68)
        self.assertEqual(trailers[eftd.nashville], 32)

class TestContingent(CountMethodTest):
    
    def setUp(self):
        self.cm = cv.ContingentVote()

    def test_supplementary(self):
        self.cm.count(eftd.ABC_CV_2)
        # invariant
        self.assertEqual(self.cm.results, self.cm.residue[-1])
        # round 1
        self.assertEqual(self.cm.residue[0][eftd.a], 36)
        self.assertEqual(self.cm.residue[0][eftd.b], 16)
        self.assertEqual(self.cm.residue[0][eftd.c], 48)
        # round 2
        self.assertEqual(self.cm.residue[1][eftd.a], 45)
        self.assertEqual(self.cm.residue[1][eftd.c], 55)

    def test_sri_lankan(self):
        self.cm.count(eftd.ABCD_CV_3)
        # invariant
        self.assertEqual(self.cm.results, self.cm.residue[-1])
        # round 1
        self.assertEqual(self.cm.residue[0][eftd.A], 34)
        self.assertEqual(self.cm.residue[0][eftd.B], 17)
        self.assertEqual(self.cm.residue[0][eftd.C], 32)
        self.assertEqual(self.cm.residue[0][eftd.D], 37)
        # round 2
        self.assertEqual(self.cm.residue[1][eftd.A], 73)
        self.assertEqual(self.cm.residue[1][eftd.D], 47)

class TestTraditionalBorda(CountMethodTest):

    def setUp(self):
        self.cm = None
    
    def test_premature(self):
        self.cm = borda.ModifiedBorda()
        self.assertRaises(cmx.IncompleteCount, self.cm.leader)

    def test_tennessee(self):
        self.cm = borda.TraditionalBorda(len(eftd.TENNESSEE.keys()))
        self.cm.count(eftd.TN_IRV_100)
        self.assertEqual(self.cm.result[eftd.memphis], 126)
        self.assertEqual(self.cm.result[eftd.nashville], 194)
        self.assertEqual(self.cm.result[eftd.chattanooga], 173)
        self.assertEqual(self.cm.result[eftd.knoxville], 107)

    def test_abcd(self):
        self.cm = borda.TraditionalBorda(4)
        self.cm.count(eftd.ABCD_CV_4)
        self.assertEqual(self.cm.result[eftd.a], 153)
        self.assertEqual(self.cm.result[eftd.b], 151)
        self.assertEqual(self.cm.result[eftd.c], 205)
        self.assertEqual(self.cm.result[eftd.d], 91)

class TestBucklin(CountMethodTest):

    def setUp(self):
        self.cm = bucklin.Bucklin()

    def test_bucklin_tennessee(self):
        self.cm.count(eftd.TN_IRV_100)
        #
        self.assertEqual(self.cm.result[eftd.memphis], 42)
        self.assertEqual(self.cm.result[eftd.nashville], 68)
        self.assertEqual(self.cm.result[eftd.chattanooga], 58)
        self.assertEqual(self.cm.result[eftd.knoxville], 32)
        # 
        self.assertEqual(self.cm.residue[0][eftd.memphis], 42)
        self.assertEqual(self.cm.residue[0][eftd.nashville], 26)
        self.assertEqual(self.cm.residue[0][eftd.chattanooga], 15)
        self.assertEqual(self.cm.residue[0][eftd.knoxville], 17)

class TestSTV(CountMethodTest):

    def setUp(self):
        pass

    def test_party_foods(self):
        self.skipTest('results and residue formats not determined')
        self.cm = stv.SingleTransferableVote(5, 3)
        self.cm.count(eftd.FOOD_STV_20)

    def test_abcd(self):
        self.skipTest('results and residue formats not determined')
        self.cm = stv.SingleTransferableVote(4, 3)
        self.cm.count(eftd.ABCD_STV_57)

class TestNauruBorda(CountMethodTest):

    def setUp(self):
        self.cm = borda.NauruBorda()

    def test_nauru(self):
        self.skipTest('no test case found yet')

class TestKiribatiBorda(CountMethodTest):
    
    def setUp(self):
        self.cm = borda.KiribatiBorda(0)

    def test_kiribati(self):
        self.skipTest('no test case found yet')
        
class TestModifiedBorda(CountMethodTest):

    def setUp(self):
        self.cm = borda.ModifiedBorda()

    def test_modified(self):
        self.skipTest('no test case found yet')

class TestBaldwin(CountMethodTest):

    def setUp(self):
        pass

    def test_baldwin_placeholder(self):
        self.skipTest('poor description of method, no test case found yet')

class TestNanson(CountMethodTest):

    def setUp(self):
        pass

    def test_nanson_placeholder(self):
        self.skipTest('poor description of method, no test case found yet')

if __name__ == '__main__':
    unittest.main()
