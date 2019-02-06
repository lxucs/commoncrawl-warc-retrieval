#!/usr/bin/env python
from os import listdir, makedirs
from os.path import join
import errno
import json
import re
import logging
from multiprocessing import Pool
from argparse import ArgumentParser


def filter_entry(entry: json, url_pattern):
    """
    :param entry: json object of one cdx index
    :param url_pattern: regex pattern to filter url
    :return: None if doesn't meet up criteria, or dict of simplified entry
    """
    return None if url_pattern.match(entry['url']) is None else {
        'url': entry['url'],
        'length': entry['length'],
        'filename': entry['filename'],
        'offset': entry['offset']
    }


def filter_file(path_input, url_pattern: str, path_output):
    url_pattern = re.compile(url_pattern)
    with open(path_input, 'r') as fin:
        with open(path_output, 'wb') as fout:
            for line in fin:
                entry = json.loads(line)
                filtered = filter_entry(entry, url_pattern)
                if filtered:
                    json.dump(filtered, fout)
                    fout.write('\n')
    logging.info('Done filtering file: %s' % path_input)


def do_work(dir_input, dir_output, url_pattern, num_processes):
    """
    Filter files in input directory using multiprocessing.
    :param dir_input: path of input directory
    :param dir_output: path of output directory; create one if not exists
    :param url_pattern: url pattern string
    :param num_processes: the number of processes to use
    :return:
    """
    with Pool(processes=num_processes) as pool:
        try:
            makedirs(dir_output)
        except OSError as e:  # Avoid race condition when creating directory
            if e.errno != errno.EEXIST:
                raise
        pool_input = [[join(dir_input, f), url_pattern, join(dir_output, f)]
                      for f in listdir(dir_input) if not f.startswith('.')]
        pool.starmap(filter_file, pool_input)


def get_args():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s]: %(message)s', level=logging.INFO)

    parser = ArgumentParser('CDX Index Filter')
    parser.add_argument('dir_input', help='The path of input directory to be filtered')
    parser.add_argument('dir_output', help='The path of output directory')
    parser.add_argument('-p', '--processes', type=int, default=2,
                        help='Number of worker processes to use; default is 2')
    parser.add_argument('--pattern',
                        help='Custom url filtering pattern; default is NYTimes US Politics article')
    return parser.parse_args()


if __name__ == "__main__":
    pattern = '.*www.nytimes.com/20[\\d/]+/us/politics/.+\\.html$'  # Only take url without query parameters

    args = get_args()
    if args.pattern:
        pattern = args.pattern

    do_work(args.dir_input, args.dir_output, pattern, args.processes)
