# Dupfinder

An efficient way to find duplicate files.
Comparison is done via `SHA-256` hashs. Results are output to `duplicates.json` file in the current directory.

![GitHub](https://img.shields.io/github/license/yohannesHL/dupfinder)

## Setup

> - Pull the source code
> - `cd dupfinder`
> - `pip install .`

## Usage

> - Run `dupfinder <folder-name>`
> - Add `-o` or `--output` followed by a desired filename for output JSON file (defaults to `duplicates.json`)
> - Add `-d` or `--dedup` to automatically remove duplicated files inplace (duplicate files marked for deletion are backed to a `./backup` folder)
> - Add `-f` or `--force` in conjunction with `-d` to remove files without backup
> - Add `-v` or `--verbose` to see verbose logs




## Example

`$ dedup basedir`

The output `duplicates.json` file containes a mapping of content hash keys to a list of filepaths (duplicates):
```
{
    "1ef0ae7bbe4ce6c99ab744fe8c27582178d69c660538ef6a4b201cf5a944e17a": [
        "basedir/testfile.pdf",
        "basedir/A/testfile.pdf",
        "basedir/B/1/otherfile.pdf",
        "basedir/B/2/otherfile.pdf"
    ],
    "3460ebae1c45bfd069074b365281354cfdf41b82ffb05c7eedd6775446fcd3a4": [
        "basedir/testfile2.pdf",
        "basedir/B/otherfile.pdf"
    ],
    "e0dcca0b30e52954e73320830b86f921d458d03e8f5d137fb4b5a1bfc4d3b2ab": [
        "basedir/A/1/otherfile.pdf",
        "basedir/B/1/2/otherfile.pdf"
    ]
}
```

##  Deduplication

The `--dedup` flag can be used to optionally get rid of duplicate files.

For a directory structure like:
```
test_files
├── A
│   ├── aws.svg
│   └── honeycomb.mp4
├── aws.svg
├── B
│   ├── Mapping startups.png
│   └── tesla-impact-report-2019.pdf
├── C
│   └── Ketsa_-_13_-_Mission_Ready.mp3
├── cloud-init.cfg
├── Faulhaber.doc
├── honeycomb.mp4
├── Ketsa_-_13_-_Mission_Ready.mp3
├── Mapping startups.png
└── tesla-impact-report-2019.pdf

```

Running `$ dupfinder test_files --dedup` results in:
```
test_files
├── A
├── aws.svg
├── B
├── C
├── cloud-init.cfg
├── Faulhaber.doc
├── honeycomb.mp4
├── Ketsa_-_13_-_Mission_Ready.mp3
├── Mapping startups.png
└── tesla-impact-report-2019.pdf
```

Comparing with `duplicate.json` output, we can see that the files furthest away from the base dir are removed:
```
{
    "3a4720542e42a50cd738f6150f54efe8161c1aaed601af07ea4ad3a19d5f18c2": [
        "/home/coder/project/dupfinder/dupfinder/test_files/aws.svg",
        "/home/coder/project/dupfinder/dupfinder/test_files/A/aws.svg"
    ],
    "33322f02f318cc86556bad5656b6d853d9ac5d16d34de6a6ddff694d83ed0238": [
        "/home/coder/project/dupfinder/dupfinder/test_files/honeycomb.mp4",
        "/home/coder/project/dupfinder/dupfinder/test_files/A/honeycomb.mp4"
    ],
    "18b041778ebbc596441d2bfa72c91ede09a2cb2dddf4e2c52d83efe2f46595aa": [
        "/home/coder/project/dupfinder/dupfinder/test_files/tesla-impact-report-2019.pdf",
        "/home/coder/project/dupfinder/dupfinder/test_files/B/tesla-impact-report-2019.pdf"
    ],
    "8f8207e9b9e8d33f0afffd5be46426291c361688ecbac3ab09001c3da1d2d28a": [
        "/home/coder/project/dupfinder/dupfinder/test_files/Mapping startups.png",
        "/home/coder/project/dupfinder/dupfinder/test_files/B/Mapping startups.png"
    ],
    "b9c8d1b2809eb34f6f57b4747320da0425fe217663d2b6f4d2deb2ba86261861": [
        "/home/coder/project/dupfinder/dupfinder/test_files/Ketsa_-_13_-_Mission_Ready.mp3",
        "/home/coder/project/dupfinder/dupfinder/test_files/C/Ketsa_-_13_-_Mission_Ready.mp3"
    ]
}
```

## Backup
By default removed files are also backed up to `./backup`:
```
backup
├── dupfinder_test_files_A_aws.svg
├── dupfinder_test_files_A_honeycomb.mp4
├── dupfinder_test_files_B_Mapping startups.png
├── dupfinder_test_files_B_tesla-impact-report-2019.pdf
└── dupfinder_test_files_C_Ketsa_-_13_-_Mission_Ready.mp3
```





## Auther
Yohannes Libanos

