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

```
@article{doi:10.1080/27660400.2022.2153633,
  author = {Luca Foppiano and Pedro Baptista Castro and Pedro Ortiz Suarez and Kensei Terashima and Yoshihiko Takano and Masashi Ishii},
  title = {Automatic extraction of materials and properties from superconductors scientific literature},
  journal = {Science and Technology of Advanced Materials: Methods},
  volume = {3},
  number = {1},
  pages = {2153633},
  year  = {2023},
  publisher = {Taylor & Francis},
  doi = {10.1080/27660400.2022.2153633},
  URL = { 
        https://doi.org/10.1080/27660400.2022.2153633
  },
  eprint = { 
        https://doi.org/10.1080/27660400.2022.2153633
  }
}
```
