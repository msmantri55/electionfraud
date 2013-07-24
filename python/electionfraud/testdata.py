# -*- python -*-

from electionfraud.fraud import Choice

memphis = Choice('Memphis')
nashville = Choice('Nashville')
chattanooga = Choice('Chattanooga')
knoxville = Choice('Knoxville')

a = Choice('Andrew')
b = Choice('Brian')
c = Choice('Catherine')
d = Choice('David')

A = Choice('Andrea')
B = Choice('Brad')
C = Choice('Carter')
D = Choice('Delilah')

TENNESSEE = {
    memphis: 42,
    nashville: 26,
    chattanooga: 15,
    knoxville: 17
    }

# http://en.wikipedia.org/wiki/Instant-runoff_voting

TN_FPTP_100 = list()
for choice in TENNESSEE.keys():
    TN_FPTP_100.extend([[choice]] * TENNESSEE[choice])

TN_IRV_100 = [[memphis, nashville, chattanooga, knoxville]] * 42
TN_IRV_100 = TN_IRV_100 + [[nashville, chattanooga, knoxville, memphis]] * 26
TN_IRV_100 = TN_IRV_100 + [[chattanooga, knoxville, nashville, memphis]] * 15
TN_IRV_100 = TN_IRV_100 + [[knoxville, chattanooga, nashville, memphis]] * 17

ABC_CV_2 = [[a, b]] * 30
ABC_CV_2 = ABC_CV_2 + [[a, c]] * 6
ABC_CV_2 = ABC_CV_2 + [[b, a]] * 9
ABC_CV_2 = ABC_CV_2 + [[b, c]] * 7
ABC_CV_2 = ABC_CV_2 + [[c, b]] * 28
ABC_CV_2 = ABC_CV_2 + [[c, a]] * 20

ABCD_CV_3 = [[A, B, C]] * 34
ABCD_CV_3 = ABCD_CV_3 + [[B, C, A]] * 17
ABCD_CV_3 = ABCD_CV_3 + [[C, B, A]] * 22
ABCD_CV_3 = ABCD_CV_3 + [[C, D, B]] * 10
ABCD_CV_3 = ABCD_CV_3 + [[D, C, B]] * 37

ABCD_CV_4 = [[a, c, b, d]] * 51
ABCD_CV_4 = ABCD_CV_4 + [[c, b, d, a]] * 5
ABCD_CV_4 = ABCD_CV_4 + [[b, c, d, a]] * 23
ABCD_CV_4 = ABCD_CV_4 + [[d, c, b, a]] * 21

# http://en.wikipedia.org/wiki/Borda_count

