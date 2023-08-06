# capatsv

Cellranger ATAC peak annotation, for use with BED peak input files. Functionality sourced from Cellranger ATAC version 2.1.0, with minor tweaks to respect the input sorting when creating the output.

## Installation

```
pip3 install capatsv
```

The script depends on a recent version of bedtools, was tested with 2.30.0 matching the one distributed within Cellranger ATAC 2.1.0.

## Usage

Once installed, the peak annotation script becomes callable via the command line

```
capatsv --bed /path/to/peaks.bed --ref /path/to/cellranger/arc/reference --tsv /path/to/annotated/output.tsv
```

Where `--bed` is your BED file of peaks to annotate, `--ref` is the path to the Cellranger reference that was used when creating the peaks, and `--tsv` is the path to the `atac_peak_annotation.tsv` equivalent the script will generate.

It's also possible to import the package within a python session:

```
import capatsv

capatsv.capatsv(bed, ref, tsv)
```
