from pathlib import Path
import unittest
from unittest.mock import patch
from .dupfinder import find_duplicates, deduplicate_content

BASE_DIR = Path(__file__).parent


class TestDupfinder(unittest.TestCase):

    maxDiff = None
    @patch('dupfinder.dupfinder.traverse')
    def test_find_duplicates(self, traverse):

        traverse.return_value = [
            ('basedir/testfile.pdf', 'content-1'.encode('utf-8')),
            ('basedir/testfile2.pdf', 'content-2'.encode('utf-8')),
            ('basedir/A/testfile.pdf', 'content-1'.encode('utf-8')),
            ('basedir/A/otherfile.pdf', 'content-3'.encode('utf-8')),
            ('basedir/A/1/otherfile.pdf', 'content-4'.encode('utf-8')),
            ('basedir/B/otherfile.pdf', 'content-2'.encode('utf-8')),
            ('basedir/B/1/otherfile.pdf', 'content-1'.encode('utf-8')),
            ('basedir/B/1/2/otherfile.pdf', 'content-4'.encode('utf-8')),
            ('basedir/B/2/otherfile.pdf', 'content-1'.encode('utf-8')),
        ]

        expected_output = {
            '1ef0ae7bbe4ce6c99ab744fe8c27582178d69c660538ef6a4b201cf5a944e17a': [
                'basedir/testfile.pdf',
                'basedir/A/testfile.pdf',
                'basedir/B/1/otherfile.pdf',
                'basedir/B/2/otherfile.pdf'
            ],
            '3460ebae1c45bfd069074b365281354cfdf41b82ffb05c7eedd6775446fcd3a4': [
                'basedir/testfile2.pdf',
                'basedir/B/otherfile.pdf'
            ],
            'e0dcca0b30e52954e73320830b86f921d458d03e8f5d137fb4b5a1bfc4d3b2ab': [
                'basedir/A/1/otherfile.pdf',
                'basedir/B/1/2/otherfile.pdf'
            ]
        }

        output = find_duplicates('/test-dir')

        self.assertTrue(traverse.called)
        self.assertDictEqual(output, dict(expected_output))

    def test_find_duplicates__filetypes(self):
        test_files_path = BASE_DIR / 'test_files'
        expected_output = {
            '3a4720542e42a50cd738f6150f54efe8161c1aaed601af07ea4ad3a19d5f18c2': [
                str(BASE_DIR / 'test_files/aws.svg'),
                str(BASE_DIR / 'test_files/A/aws.svg')
            ],
            '33322f02f318cc86556bad5656b6d853d9ac5d16d34de6a6ddff694d83ed0238': [
                str(BASE_DIR / 'test_files/honeycomb.mp4'),
                str(BASE_DIR / 'test_files/A/honeycomb.mp4')
            ],
            '18b041778ebbc596441d2bfa72c91ede09a2cb2dddf4e2c52d83efe2f46595aa': [
                str(BASE_DIR / 'test_files/tesla-impact-report-2019.pdf'),
                str(BASE_DIR / 'test_files/B/tesla-impact-report-2019.pdf')
            ],
            '8f8207e9b9e8d33f0afffd5be46426291c361688ecbac3ab09001c3da1d2d28a': [
                str(BASE_DIR / 'test_files/Mapping startups.png'),
                str(BASE_DIR / 'test_files/B/Mapping startups.png')
            ],
            'b9c8d1b2809eb34f6f57b4747320da0425fe217663d2b6f4d2deb2ba86261861': [
                str(BASE_DIR / 'test_files/Ketsa_-_13_-_Mission_Ready.mp3'),
                str(BASE_DIR / 'test_files/C/Ketsa_-_13_-_Mission_Ready.mp3')
            ]
        }
        output = find_duplicates(test_files_path)

        self.assertDictEqual(output, expected_output)

    @patch('os.mkdir')
    @patch('os.remove')
    def test_deduplicate_content(self, remove, mkdir):
        duplicates = {
            '3a4720542e42a50cd738f6150f54efe8161c1aaed601af07ea4ad3a19d5f18c2': [
                str(BASE_DIR / 'test_files/aws.svg'),
                str(BASE_DIR / 'test_files/A/aws.svg')
            ],
            '18b041778ebbc596441d2bfa72c91ede09a2cb2dddf4e2c52d83efe2f46595aa': [
                str(BASE_DIR / 'test_files/tesla-impact-report-2019.pdf'),
                str(BASE_DIR / 'test_files/B/tesla-impact-report-2019.pdf')
            ]
        }
        expected_remove_invokations = [
            str(BASE_DIR / 'test_files/A/aws.svg'),
            str(BASE_DIR / 'test_files/B/tesla-impact-report-2019.pdf')
        ]

        remove_invocations = []
        remove.side_effect = lambda x: remove_invocations.append(x)

        deduplicate_content(duplicates)

        self.assertFalse(mkdir.called)
        self.assertListEqual(remove_invocations, expected_remove_invokations)

    @patch('os.mkdir')
    @patch('os.replace')
    def test_deduplicate_content__replace(self, replace, mkdir):
        duplicates = {
            '3a4720542e42a50cd738f6150f54efe8161c1aaed601af07ea4ad3a19d5f18c2': [
                str(BASE_DIR / 'test_files/aws.svg'),
                str(BASE_DIR / 'test_files/A/aws.svg')
            ],
            '18b041778ebbc596441d2bfa72c91ede09a2cb2dddf4e2c52d83efe2f46595aa': [
                str(BASE_DIR / 'test_files/tesla-impact-report-2019.pdf'),
                str(BASE_DIR / 'test_files/B/tesla-impact-report-2019.pdf')
            ]
        }
        expected_replace_invokations = [
            (
                str(BASE_DIR / 'test_files/A/aws.svg'),
                str(BASE_DIR / '.backup/dupfinder_test_files_A_aws.svg')
            ),
            (
                str(BASE_DIR / 'test_files/B/tesla-impact-report-2019.pdf'),
                str(BASE_DIR / '.backup/dupfinder_test_files_B_tesla-impact-report-2019.pdf')
            )
        ]
        replace_invocations = []
        replace.side_effect = lambda a, b: replace_invocations.append((a, b))

        deduplicate_content(duplicates, BASE_DIR / '.backup')

        self.assertTrue(mkdir.called)
        self.assertListEqual(replace_invocations, expected_replace_invokations)
