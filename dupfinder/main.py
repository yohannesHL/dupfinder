import hashlib
import os
import json
import logging
import argparse


logging.basicConfig()

log  = logging.getLogger('dupfinder')
log.setLevel(logging.INFO)
duplicates = {}
seen = {}

def check_content(filename, content):
    hash = hashlib.sha256(content).hexdigest()

    seen[hash] = seen[hash] if seen.get(hash) else []
    seen[hash].append(filename)
    duplicate = True if len(seen[hash]) > 1 else False

    if duplicate:
        duplicates[hash] = duplicates[hash] if duplicates.get(hash) else []
        duplicates[hash].append(filename)

    return duplicate

def traverse(baseDir):
    for root,dirs, files in os.walk(baseDir, True):
        for filename in files:
            with open(os.path.join(root, filename), 'r') as fs:
                log.debug(os.path.join(root,filename).replace(baseDir,'.'))
                yield (os.path.join(root,filename), fs.read(-1) )
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description='Duplicate file finder'
    )
    parser.add_argument("file")
    parser.add_argument("-v", "--verbose", help="dispay verbose logs", action="store_true")
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug('Debug mode enabled')
    
    baseDir = args.file or os.getcwd() 
    log.info('Checking files in {}'.format(baseDir))
    result_file_name = os.path.join(os.getcwd(), 'duplicates.json')
    log.debug('Paths displayed will be relative to {}'.format(baseDir))

    for filename, content in traverse(baseDir):
        check_content(filename, content)

    log.info('Saving results...')
    log.info('Result file will be saved to {}'.format(result_file_name))

    with open(result_file_name, 'w+') as fd:
        fd.write(json.dumps(duplicates))
    log.info('Done!')
