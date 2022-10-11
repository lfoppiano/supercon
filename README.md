# SuperCon2: Automatic extraction of materials and properties from superconductor scientific literature

- [Introduction](#introduction)
- [Releases](#releases)
- [Field list](#field-list)

## Introduction 

SuperCon 2 is the quantitative database of superconductors materials and properties, created automatically using [grobid-superconductors](https://github.com/lfoppiano/grobid-superconductors) on a set of 37000 from arXiv. 

## Releasees 

The latest version was extracted on the 2022/12/03 and contains about 40000 records.  
- `supercon2_v22.12.03.csv` contains the superconductors records. For more information, see the [field list](#field-list), below.
- `supercon2_1203_papers.csv` contains the list of doi, title, authors for each paper. The data was automatically extracted with [Grobid](https://github.com/kermitt2/grobid) and consolidated using [biblio-glutton](https://github.com/kermitt2/biblio-glutton)

## Field list

The fields are explained 
```
id
rawMaterial
materialId
name
formula
doping
shape
materialClass
fabrication
substrate
variables
criticalTemperature
criticalTemperatureMeasurementMethod
appliedPressure
section
subsection
hash
title
doi
authors
publisher
journal
year
```

## How to cite

If you use this work please cite our preprint (currently under review): 

```
@unpublished{foppiano:hal-03776658,
  TITLE = {{Automatic Extraction of Materials and Properties from Superconductors Scientific Literature}},
  AUTHOR = {Foppiano, Luca and Baptista de Castro, Pedro and Ortiz Suarez, Pedro and Terashima, Kensei and Takano, Yoshihiko and Ishii, Masashi},
  URL = {https://hal.inria.fr/hal-03776658},
  NOTE = {working paper or preprint},
  YEAR = {2022},
  MONTH = Sep,
  PDF = {https://hal.inria.fr/hal-03776658/file/main.pdf},
  HAL_ID = {hal-03776658},
  HAL_VERSION = {v1},
}
```