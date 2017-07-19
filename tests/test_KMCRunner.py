'''
Test KMC runner
'''

import unittest
import tempfile
import os
import shutil
from validate_bcl2fq import KMCRunner

test_seq_r1 = '''@071112_SLXA-EAS1_s_7:5:1:817:345
GGGTGATGGCCGCTGCCGATGGCGTCAAATCCCACC
+071112_SLXA-EAS1_s_7:5:1:817:345
IIIIIIIIIIIIIIIIIIIIIIIIIIIIII9IG9IC
@071112_SLXA-EAS1_s_7:5:1:801:338
GTTCAGGGATACGACGTTTGTATTTTAAGAATCTGA
+071112_SLXA-EAS1_s_7:5:1:801:338
IIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII6IBI\n'''

test_seq_r2 = '''@071112_SLXA-EAS1_s_7:5:1:817:345
AAGTTACCCTTAACAACTTAAGGGTTTTCAAATAGA
+071112_SLXA-EAS1_s_7:5:1:817:345
IIIIIIIIIIIIIIIIIIIIDIIIIIII>IIIIII/
@071112_SLXA-EAS1_s_7:5:1:801:338
AGCAGAAGTCGATGATAATACGCGTCGTTTTATCAT
+071112_SLXA-EAS1_s_7:5:1:801:338
IIIIIIIIIIIIIIIIIIIIIIGII>IIIII-I)8I\n'''


class TestKMCRunner(unittest.TestCase):
    def setUp(self):
        self.workdir = tempfile.mkdtemp()
        self.outname = os.path.join(self.workdir, 'res')
        self.obj = KMCRunner.KMC()
        fastq_tmp = tempfile.NamedTemporaryFile(mode='r+t',
                                                delete=False,
                                                dir=self.workdir)
        fastq_tmp.write(test_seq_r1)
        fastq_tmp.close()
        self.fastq = fastq_tmp.name
        self.obj.count_kmers(self.fastq,
                             outname=self.outname,
                             workdir=self.workdir,
                             ks=3,
                             threads=24)

    def test_total_kmers(self):
        '''
        A function to test count kmers method of KMC class returns the right
        number of total kmers
        '''
        self.assertEqual(68, self.obj.total_kmers)

    def test_total_kmers_below_threshold(self):
        '''
        A function to test count kmers method of KMC class returns the right
        number of total kmers found below the default threshold of 2
        '''
        self.assertEqual(5, self.obj.total_kmers_below_threshold)

    def test_total_kmers_above_threshold(self):
        '''
        A function to test count kmers method of KMC class returns the right
        number of total kmers found above the default threshold of 1e9
        '''
        self.assertEqual(0, self.obj.total_kmers_above_threshold)

    def test_total_unique_kmers(self):
        '''
        A function to test count kmers method of KMC class returns the right
        number of total of unique kmers
        '''
        self.assertEqual(29, self.obj.total_unique_kmers)

    def tearDown(self):
        '''Do some cleanup'''
        shutil.rmtree(self.workdir)
