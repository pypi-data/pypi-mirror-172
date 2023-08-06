## 2.0.11 (2022-10-22)

### Fix

- fix correct name for moss_emscli

## 2.0.10 (2022-10-22)

### Fix

- better status code check when testing urls
- does not stop if GDAL ist not present

## 2.0.9 (2022-10-05)

### Fix

- show variant id in tree

## 2.0.8 (2022-10-05)

### Fix

- show variant tree in workflow output

## 2.0.7 (2022-10-04)

### Fix

- some parameters can be empty

## 2.0.6 (2022-10-04)

### Fix

- better handling of ems_dump without variant

## 2.0.5 (2022-09-29)

### Fix

- multiple fix for emscli
- remove compare from subcommands

## 2.0.4 (2022-09-29)

### Fix

- add optional file name for the dump output

## 2.0.3 (2022-09-28)

### Fix

- emscli_dump for nF Export

## 2.0.2 (2022-09-26)

### Fix

- Remove not needed file
- better handling of GDAL Exception

### Refactor

- set version 2.0.1
- fix name for ems_cli
- set version 2.0.1

## 2.0.1 (2022-09-26)

### BREAKING CHANGE

- Since version 2.0.0 Python 2 is no more supported

### Feat

- **ems_cli_dump**: Add export for Variants
- add emscli_dump for dumping layers

### Fix

- remove not needed files
- small correction in script
- add vscode config
- type error
- type error
- Append a / at the end if not present
- Fix problems with jsonid in login

### Refactor

- rename ems_cli to moss_ems_cli to avoid conflict
- Add missing dependencies
- Add missing dependencies
- Add missing dependencies
- fix mkdocs and flake8 conflict
- remove python2 files
- Remove support for Python2

## v1.2.4 (2021-11-22)

## v.1.2.1 (2021-05-17)

### Fix

- restore missing Class needed for QGIS Plugin

## v1.2.0 (2021-05-12)

### BREAKING CHANGE

- the geometry parameter in query, accept an ESRI Geometry and it's used for spatial filter. Every other parameter for standard EMS can be added.

### Feat

- Add filter option for master: better handling of exception.
- Add asUrl for attachment info
- **28405**: WEGA EMSPY - CLI um ein Projekt zu exportieren/importieren
- add updateAttachment to layer
- add deleteAttachment to layer
- add registerAttachment to layer
- add registerAttachment to layer
- add method to download an attachment
- add files to use Jenkins
- remove configuration file for gitlab ci
- add configuration file for gitlab ci
- add configuration file for gitlab ci
- update postgresql version to 11-2.5

### Fix

- check if variants tree has a root node
- handle not existing preferred variant
- Fix typing in python2
- Fix python2 logging syntax
- Fix python2 logging syntax
- add support for old geometry boolean
- Add scripts to the package build
- add_attachment fix file name to avoid including the path
- Fix returning id only from EmsLayer Query
- Fix returning id only from EmsLayer Query
- remove formatter for logging
- remove linting errors
- correct name for gitlab CI
- correct name for gitlab CI
- remove temp Directory after tests
- Add Database password for PostgreSQL to avoid error on starting
- wrong spelling in pyproject.toml

### Refactor

- We check if ems is running, before tests This avoids to use sleep or random wait.
- Move code frm SVN to GIT
- Move code frm SVN to GIT
- Move code frm SVN to GIT
- Move code frm SVN to GIT
- Move code frm SVN to GIT
