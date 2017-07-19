'''
Some classes to run KMC
'''

import subprocess
import os
import re
import shutil
import logging

# a constant indicating the name of the environmental
# variable indicating the version of bcl2fastq
KMC_VAR = 'KMC_VERSION'


class Error(Exception):
    '''A base error class'''
    pass


class VersionError(Error):
    '''An error class for when there is a version error'''
    def __init__(self, program, exp_version):
        self.message = f'Expected {program} version {exp_version} but \
                        did not find it'


class EnvError(Error):
    '''An error class for when an environmental variable is not found'''
    def __init__(self, var):
        self.message = f'Could not find the environmental variable {var}.'


class KMC:
    '''
    Run KMC to count kmers
    '''
    def __init__(self, version=None, path=None):
        if version is None:
            try:
                version = re.escape(os.environ[KMC_VAR])
            except:
                raise EnvError(KMC_VAR)
        self.version = re.compile(version)
        if path is None:
            self.cmd = shutil.which('kmc')
        else:
            self.cmd = path
        self.__check_version()

    def __check_version(self):
        p = subprocess.run([self.cmd],
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf8')
        local_version = self.version.findall(p.stdout)
        if len(local_version) == 0:
            raise VersionError(self.cmd, self.version)
        else:
            logging.info(f'Found appropriate version of {self.cmd}')

    def __kmc_parser(self, output):
        '''Parse the stdout of KMC'''
        self.kmc_output = {}
        output = output.split("\n")
        for l in output:
            tmp = l.strip()
            try:
                key, value = tmp.split(':')
                self.kmc_output[key.strip()] = value.strip()
            except:
                logging.info(f'Skipping line {l}')

    def count_kmers(self, fastq, outname, workdir,
                    ks=25, threads=24):
        '''Run KMC to count kmers on a FASTQ file'''
        cmd = [self.cmd, f'-k{ks}', '-t{threads}', fastq, outname, workdir]
        p = subprocess.run(cmd,
                           stdout=subprocess.PIPE,
                           stderr=subprocess.PIPE,
                           encoding='utf8')
        self.__kmc_parser(p.stdout)
        self.total_kmers = int(self.kmc_output['Total no. of k-mers'])
        self.total_unique_kmers = int(self.kmc_output['No. of unique k-mers'])
        self.total_reads = int(self.kmc_output['Total no. of reads'])
        self.total_kmers_below_threshold = int(self.kmc_output[
                                        'No. of k-mers below min. threshold'])
        self.total_kmers_above_threshold = int(self.kmc_output[
                                        'No. of k-mers above max. threshold'])

        pass
