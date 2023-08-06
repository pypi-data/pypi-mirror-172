# vcfvalidator

This package checks the metadata of VCF files with respect to the following paper: https://f1000research.com/articles/11-231


### Installing the package:

```
pip install vcfvalidator
```

### How to use the validator:

The package installs a CLI tool that can be used to check the VCF metdata with the following command:
```
$ vcfvalidator validate-metadata PATH_TO_VCF_FILE
```

The VCF file under PATH_TO_VCF_FILE can be either compressed with GZIP (*.vcf.gz) or uncompressed (*.vcf).