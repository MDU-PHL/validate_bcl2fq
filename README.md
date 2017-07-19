# Validate BLC2FASTQ for use at MDU

`bcl2fastq` is the Illumina software tool to transform raw `bcl` data from
an Illumina sequencer to `fastq` data. This is the tool used on BaseSpace,
but we use it locally.

As part of our NATA accreditation, we verified the demultiplexing of raw
Illumina BCL data using `bcl2fastq` version 1.19.0.316. The goal of this
program is to automate the verification of new version of `bcl2fastq`.

## What does this program do?

The goal is to verify that FASTQ files produces by a new version of `bcl2fastq`
are compatible with FASTQ files produced under the original `bcl2fastq` version.

## How do we do it?

The approach we are taking is one based on kmer counting. In essence, we
take the following steps:

1. Count kmers in a FASTQ file from our original validation
2. Generate a new FASTQ file from the same BCL data using a
    newer version of `bcl2fastq`.
3. Count kmers on this new FASTQ file.
4. Compare the kmers from each file.
5. Compare the counts for each file.


## What should the result be?

In the ideal world, the following tests would be true between the two files:

1. Number of kmers identified is equal
2. The identified kmers are the equal
3. The count of each kmer is the same

If these three tests are true, then the data produced by the two different
versions of `bcl2fastq` are exactly the same.

## What if one or more of the tests fail?

If test 1 fails, it is very likely that test 2 will fail too. This might be due
to changes in the `bcl2fastq` code masking adapters and low quality bases. If
this is the case, then it is possible to accept the new results.

If test 3 fails, some tolerance level should be accepted. This remains to be
determined.

## What is the output?

The output is a verification report in PDF format.

# Dependencies

* kmc version 3.0.0 [available here](https://github.com/refresh-bio/KMC/releases/tag/v3.0.0)

# Installation

Not yet installable. a pip installable `setup.py` script will be available for
the first release.

# Continuous integration

Travis CI support is coming...
