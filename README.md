# Dupfinder

An efficient way to find duplicate files.
Comparison is done via `SHA-256` hashs. Results are output to `duplicates.json` file in the current directory.

## Setup
> Pull the source code
> `cd dupfinder`
> `pip install .` or `python setup.py install`

## Usage

> - Run `dupfinder <folder-name>`
> - Add `-d` or `--dedup` to automatically remove duplicated files (files are moved to a `./backup` folder unless `-f` is also supplied)
> - Add `-f` or `--force` in conjunction with `-d` to remove files without backup
> - Add `-v` or `--verbose` to see verbose logs



## Licence
MIT

## Auther
Yohannes Libanos

