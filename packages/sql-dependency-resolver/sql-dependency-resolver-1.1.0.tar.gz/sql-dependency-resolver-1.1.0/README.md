# sql-dependency-resolution
A dependency resolution library that performs conflict resolution to create a topological ordering for creating and destroying SQL objects such as views, functions and indexes.

## Installation
Install using `pip install sql-dependency-resolver`

## Usage
* import using `from resolver import ViewDependencyResolver`
* use `create_order` and `drop_order` to retrieve dependency ordering.(currently only views are supported).

## Caveats
* assumes name of file is the name of view.
* views must be pre-fixed with `vw_` or `mvw_`.
* dependecies are collected from join conditions.

## Tests
Run tests with `pytest`
## TODO
* implement functions, procedures and indexes.
* auto detect name from header using regex.
