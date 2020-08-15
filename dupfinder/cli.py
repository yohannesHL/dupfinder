import os
import logging
import argparse
from .helpers import log, write_file, traverse
from .dupfinder import find_duplicates, deduplicate_content


def main():
    parser = argparse.ArgumentParser(
        description=(
            'Finds duplicate files based on there content hash.'
            'Outputs the results in a'
        )
    )
    parser.add_argument('directory', help='Base directory run search on')
    parser.add_argument(
        '-o', '--output',
        default='duplicates.json', action='store_true',
        help='Output results to a specified JSON file; default=duplicates.json'
    )
    parser.add_argument(
        '-d', '--dedup',
        action='store_true',
        help='Automatically deduplicate content. Backup is saved in "./backup"'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Force removal of files w/o making backup.'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Display verbose logs'
    )
    args = parser.parse_args()

    if args.verbose:
        log.setLevel(logging.DEBUG)
        log.debug('Debug mode enabled')

    try:
        base_dir = os.path.abspath(args.directory)
        log.info('Checking files in {}'.format(base_dir))
    
        duplicates = find_duplicates(base_dir, args.verbose)

        if args.output:
            result_file_name = os.path.join(os.getcwd(), args.output)

            log.info('Saving results to "{}"'.format(result_file_name))

            write_file(result_file_name, duplicates)

        if args.dedup:
            log.info('Deduplicating files...')
            backup_dir = None if args.force else './backup'

            if backup_dir:
                log.debug('removed duplicates will be backed up to "./backup"')
            deduplicate_content(duplicates['content'], backup_dir)

        log.info('Done!')
    except Exception as exp:
        log.warn(exp)


if __name__ == '__main__':
    main()
