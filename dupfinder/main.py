#! /usr/local/bin/python
import hashlib
import os
import json
import logging
import argparse

logging.basicConfig()
log  = logging.getLogger('dupfinder')
log.setLevel(logging.INFO)

def update_state(type_key, hash_key, filename, seen, duplicates):
    seen[type_key][hash_key] = seen[type_key][hash_key] if seen[type_key].get(hash_key) else []
    seen[type_key][hash_key].append(filename)

    if len( seen[type_key].get(hash_key) ) > 1:
        duplicates[type_key][hash_key] = duplicates[type_key][hash_key] if duplicates[type_key].get(hash_key) else []
        duplicates[type_key][hash_key].append(filename)

    return (seen, duplicates)

def check_duplicates(filepath, content, seen, duplicates):
    filename = os.path.basename(filepath)
    filename_hash = hashlib.sha256(filename.encode('utf-8')).hexdigest()
    content_hash = hashlib.sha256(content).hexdigest()

    seen, duplicates = update_state('filename', filename_hash, filepath, seen, duplicates)
    seen, duplicates = update_state('content', content_hash, filepath, seen, duplicates)

    return (seen, duplicates)

def traverse(baseDir, verbose):
    for root, dirs, files in os.walk(baseDir, True):
        for filename in files:
            abs_filepath = os.path.join(root, filename)
            rel_filepath = os.path.relpath(abs_filepath, baseDir)
            with open(abs_filepath, 'rb') as fs:
                log.debug(abs_filepath if verbose else rel_filepath)
                yield (abs_filepath, fs.read(-1) )

def find_duplicates(baseDir, verbose):
    seen = dict( filename= {}, content= {})
    duplicates = dict(filename= {}, content= {})

    for filename, content in traverse(baseDir, verbose):
        seen, duplicates = check_duplicates(filename, content, seen, duplicates)

    return duplicates

def main():        
    parser = argparse.ArgumentParser(
        description='Duplicate file finder'
    )
    parser.add_argument("directory", default=os.getcwd())
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

    duplicates = find_duplicates(baseDir, args.vv)

    log.info('Saving results...')
    log.info('Results will be saved to {}'.format(result_file_name))

    with open(result_file_name, 'w+') as fd:
        fd.write(json.dumps(duplicates))
    log.info('Done!')

if __name__ == "__main__":
    main()