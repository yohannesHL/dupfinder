import hashlib
import os
from .helpers import log, traverse


def find_duplicates(base_dir, verbose=None):
    '''Finds duplicates files in a given base_dir.

    Args:
        base_dir: The starting absolute directory to start search on.
        verbose: Optional; If verbose True will output verbose debug logs.

    Returns:
        A dict mapping content hashes to a list of files with identical hashes.

        Example:

        {
            "a23b34e8c9248d783a3f33849114c386": [
                "/basedir/A/file.pdf",
                "/basedir/A/B/samefile.pdf",
                "/basedir/A/B/C/alsosamefile.pdf"
            ]
        }
    '''
    visited = dict()
    duplicates = dict()

    for filename, content in traverse(base_dir, verbose):
        filehash = hashlib.sha256(content).hexdigest()
        visited[filehash] = visited[filehash] if visited.get(filehash) else []
        visited[filehash].append(filename)

        if len(visited.get(filehash)) > 1:
            duplicates[filehash] = visited[filehash]

    return duplicates


def deduplicate_content(duplicates, backup_dest=None):
    '''Deduplicates files: Removes duplicate files only keeping a single copy.

    Args:
        duplicates: dict mapping with key hash and value array.
        backup_dest: Optional; If backup_dest is defined files will be backedup
            to the specified destination before deletion. There will be no
            nested folders in this directory and all files will be hoisted
            up to the base with their original paths included in their
            filenames (separated by _).

            Example:

            basedir/A/B/testfile.pdf -> .backup/basedir_A_B_testfile.pdf     
    '''
    if backup_dest is not None and not os.path.exists(backup_dest):
        os.mkdir(backup_dest)

    for filenames in duplicates.values():
        for filepath in filenames[1:]:
            if backup_dest:
                newpath = os.path.join(backup_dest, (os.path.relpath(filepath)
                                                     .replace('./', '')
                                                     .replace('/', '_')))
                destpath = os.path.abspath(newpath)
                log.debug('backing up {} -> {}'.format(filepath, destpath))
                os.replace(filepath, destpath)
            else:
                os.remove(filepath)
