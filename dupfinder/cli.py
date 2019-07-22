#! /usr/local/bin/python
import hashlib
import os
import json
import logging
import argparse

logging.basicConfig()
log  = logging.getLogger('dupfinder')
log.setLevel(logging.INFO)

def deduplicate_content(duplicates, backup_dest = None):
    if backup_dest and not os.path.exists(backup_dest):
        os.mkdir(backup_dest)

    for filenames in duplicates.values():
        for filepath in filenames[1:]:
            if backup_dest:
                # filename = os.path.basename(filepath)
                relpath = os.path.relpath(filepath)
                destpath =  os.path.abspath(os.path.join(backup_dest, relpath.replace('./','').replace('/', '_') ))
                log.debug('backing up {} -> {}'.format(relpath, destpath))
                os.replace(filepath, destpath )
            else:
                os.remove(filepath)

def update_state(type_key, hash_key, filename, visited, duplicates):
    visited[type_key][hash_key] = visited[type_key][hash_key] if visited[type_key].get(hash_key) else []
    visited[type_key][hash_key].append(filename)

    if len( visited[type_key].get(hash_key) ) > 1:
        duplicates[type_key][hash_key] = visited[type_key][hash_key]

    return (visited, duplicates)

def check_duplicates(filepath, content, visited, duplicates):
    filename = os.path.basename(filepath)
    filename_hash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
    content_hash = hashlib.sha256(content).hexdigest()

    visited, duplicates = update_state('filename', filename_hash, filepath, visited, duplicates)
    visited, duplicates = update_state('content', content_hash, filepath, visited, duplicates)

    return (visited, duplicates)

def traverse(baseDir, verbose):
    for root, dirs, files in os.walk(baseDir, True):
        for filename in files:
            abs_filepath = os.path.join(root, filename)
            rel_filepath = os.path.relpath(abs_filepath, baseDir)
            with open(abs_filepath, 'rb') as fs:
                log.debug(abs_filepath if verbose else rel_filepath)
                yield (abs_filepath, fs.read(-1) )

def find_duplicates(baseDir, verbose):
    visited = dict(filename= {}, content= {})
    duplicates = dict(filename= {}, content= {})

    for filename, content in traverse(baseDir, verbose):
        visited, duplicates = check_duplicates(filename, content, visited, duplicates)

    return duplicates

def write_file(filename, data):
    with open(filename, 'w+') as fd:
        fd.write(json.dumps(data))

def main():        
    parser = argparse.ArgumentParser(
        description='Duplicate file finder and deduplicator'
    )
    parser.add_argument("directory", help="base directory to run program on")
    parser.add_argument("-d", "--dedup", help="automatically remove duplicated content. Backup is saved in './backup'", action="store_true")
    parser.add_argument("-f", "--force", help="force removal of files w/o making backup.", action="store_true")
    parser.add_argument("-v", "--verbose", help="display verbose logs", action="store_true")
    parser.add_argument("-vv", help="display logs with maximum verbosity", default=False, action="store_true")
    args = parser.parse_args()

    baseDir = os.path.abspath(args.directory)
    log.info('Checking files in {}'.format(baseDir))
    result_file_name = os.path.join(os.getcwd(), 'duplicates.json')

    if args.verbose or args.vv:
        log.setLevel(logging.DEBUG)
        log.debug('Debug mode enabled')

    if args.vv:
        log.debug('Displayed paths will be relative to {}'.format(baseDir))

    try:
        duplicates = find_duplicates(baseDir, args.vv)
        log.info('Saving results...')
        log.info('Results will be saved to {}'.format(result_file_name))

        write_file(result_file_name, duplicates)

        if args.dedup:
            backup_dir = None if args.force else './backup'

            log.info('Deduplicating files...')
            log.info('Note only files with duplicated content will be removed')
            if backup_dir :
                log.debug('removed duplicate files will be saved to `./backup` for manual removal')
            deduplicate_content(duplicates['content'], backup_dir)

        log.info('Done!')
    except Exception as exp:
        log.warn(exp)


if __name__ == "__main__":
    main()