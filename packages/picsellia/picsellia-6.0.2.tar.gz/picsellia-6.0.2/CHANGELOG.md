
# Changelog

Picsellia SDK Python is a library that allows users to connect to Picsellia backend.

All notable changes to this project will be documented in this file.

## UNREALEASED [6.0.2] - 2022-10-?
### Added
- Logging File for an Experiment

### Changed
- A lot of typos, variable naming, minor formatting
- String .format() into f-strings
- Old package dependencies
- train_test_split() return MultiAsset instead of List[Asset]

### Fixed
- Regeneration of JWT when expired
- When downloading file, open file only if response is ok

## [6.0.1] - 2022-10-04
### Added
- CHANGELOG file.

### Changed
- Fixed test_train_split with breaking changes of query language in list assets.
- Documentation of core functions, minor typos fixes.
- Workflow for testing on staging when push on development and main.

## [6.0.0] - 2022-10-03
### Added
- Annotation are now objects storing Rectangle, Polygon, Classification, Point and Line for an Asset
- Artifact are now Experiment files stored
- DatasetVersion are now used as versions of Dataset
- Datalake objects
- Datasource objects
- Job objects, to wait for tasks to end
- ModelVersion are now used as versions of Model
- ScanFiles are now Scan files stored

### Changed
- Pictures renamed to Asset that are Data objects in a DatasetVersion
- Multithreading usage
- Tags
- Annotations with objects 
