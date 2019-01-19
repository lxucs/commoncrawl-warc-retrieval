#!/usr/bin/env python
from os import listdir, makedirs
from os.path import join
import json
import zlib
import errno
import logging
import requests
from multiprocessing import Pool
from argparse import ArgumentParser

URL_PREFIX = 'http://commoncrawl.s3.amazonaws.com/'
DIR_OUTPUT = None
URL_STRIP = '.com/'


def retrieve_indexed_text(index):
    try:
        byte_start = int(index['offset'])
        byte_end = byte_start + int(index['length']) - 1
        r = requests.get(URL_PREFIX + index['filename'],
                         headers={'Range': 'bytes=%d-%d' % (byte_start, byte_end)})

        name_output = index['url'][(index['url'].find(URL_STRIP) + len(URL_STRIP)):].replace('/', '-')
        with open(join(DIR_OUTPUT, name_output), 'wb') as f:
            f.write(zlib.decompress(r.content, 32 + zlib.MAX_WBITS))
        logging.info('Finished retrieving indexed text ' + name_output)
    except Exception as e:
        logging.info('Abort %s: error when retrieving file; %s' % (name_output, str(e)))


def do_work(dir_index, num_processes):
    """
    :param dir_index: path of directory containing index files from cdx-index-filter
    :param num_processes: the number of processes to use
    :return:
    """
    dict_indices = {}  # Use dict to remove duplicates caused by http/https
    for idx_file in listdir(dir_index):
        if not idx_file.startswith('.'):
            with open(join(dir_index, idx_file), 'r') as f:
                for index in json.load(f):
                    key = index['url'][index['url'].find('://'):]
                    dict_indices[key] = index

    indices = dict_indices.values()
    logging.info('Start to retrieve %d indexed text in total' % len(indices))
    with Pool(processes=num_processes) as pool:
        pool.map(retrieve_indexed_text, indices)
    logging.info('Finished retrieving all %d indexed text' % len(indices))


def get_args():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s]: %(message)s', level=logging.INFO)

    parser = ArgumentParser('CDX Index Text Retrieval')
    parser.add_argument('dir_index', help='The path of directory containing index files')
    parser.add_argument('dir_output', help='The path of output directory')
    parser.add_argument('-p', '--processes', type=int, default=2,
                        help='Number of worker processes to use; default is 2')
    parser.add_argument('--strip', default='.com/',
                        help='Use stripped url as file name of retrieved text; ' +
                             'default is to strip everything before .com/')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    DIR_INDEX = args.dir_index
    DIR_OUTPUT = args.dir_output
    URL_STRIP = args.strip

    try:
        makedirs(DIR_OUTPUT)
    except OSError as e:  # Avoid race condition when creating directory
        if e.errno != errno.EEXIST:
            raise

    do_work(DIR_INDEX, args.processes)
