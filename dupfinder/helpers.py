import json
import logging
from pathlib import Path

logging.basicConfig()
log = logging.getLogger('dupfinder')
log.setLevel(logging.INFO)


def traverse(base_dir, verbose):
    '''Traverses through the base_dir returning all files contained within.

    Args:
        base_dir: The starting directory to begin scanning from.
        verbose: If verbose True will output verbose debug logs.

    Returns:
        A tuple containing the absolute file path and binary content.

        Example:

        ('/base_dir/A/B/C/file.png', <class 'bytes'>)

    '''
    for item in Path(base_dir).glob('**/*'):
        if not item.is_file():
            continue
        abs_filepath = str(item.absolute())
        if verbose:
            log.debug(abs_filepath)

        with open(abs_filepath, 'rb') as fs:
            # TODO: skip very large files?
            yield (abs_filepath, fs.read(-1))


def write_file(filename, data):
    with open(filename, 'w+') as fd:
        fd.write(json.dumps(data))
