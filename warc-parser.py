#!/usr/bin/env python
import logging
from importlib import import_module
from os import listdir, makedirs
from os.path import join
from multiprocessing import Pool
from argparse import ArgumentParser
import errno

DIR_WARC = None
DIR_OUTPUT = None
PARSER = None  # the module that implements parse(filename, html_body)


def get_html(warcfile):
    with open(warcfile, 'r') as f:
        try:
            lines = f.readlines()
            idx_response_ok = None
            for idx, line in enumerate(lines):
                if line.startswith('HTTP'):
                    if '200' in line:
                        idx_response_ok = idx
                    else:
                        idx_response_ok = -1
                    break
            if idx_response_ok is None:
                logging.info('Abort %s: no HTTP status code found' % warcfile)
                return None
            elif idx_response_ok == -1:
                logging.info('Abort %s: HTTP status code not 200' % warcfile)
                return None

            idx_html = None
            for idx, line in enumerate(lines[idx_response_ok + 1:]):
                if line.startswith('<!DOCTYPE html>'):
                    idx_html = idx
                    break

            return '\n'.join(lines[idx_html:])
        except Exception as e:
            logging.error('Abort %s: error when reading file; %s' % (warcfile, str(e)))
            return None


def parse_html(filename, html_body):
    """
    Parse HTML body.
    :param filename: the name of the WARC file
    :param html_body: string of HTML from the WARC file
    :return: None, or string of parsed result
    """
    parser = import_module(PARSER)
    result = parser.parse(filename, html_body)
    if result is None:
        logging.error('Abort %s: error when parsing html' % filename)
        return None
    else:
        return result


def process_warc(warcfile):
    html = get_html(join(DIR_WARC, warcfile))
    if html:
        result = parse_html(warcfile, html)
        if result is None:
            return

        with open(join(DIR_OUTPUT, warcfile), 'w') as f:
            f.write(result)
            logging.info('Finished parsing %s' % warcfile)


def do_work(num_processes):
    """
    Parse WARC files of NY Times articles and write results.
    :param num_processes: the number of processes to use
    :return:
    """
    files = [file for file in listdir(DIR_WARC) if not file.startswith('.')]
    logging.info('Start to parse %d WARC files in total' % len(files))

    with Pool(processes=num_processes) as pool:
        pool.map(process_warc, files)
    logging.info('Finished parsing %d WARC files in total' % len(files))


def get_args():
    logging.basicConfig(format='%(asctime)s: [%(levelname)s]: %(message)s', level=logging.INFO)

    parser = ArgumentParser('WARC Parser')
    parser.add_argument('dir_warc', help='The path of directory containing WARC files')
    parser.add_argument('dir_output', help='The path of output directory')
    parser.add_argument('-p', '--processes', type=int, default=2,
                        help='Number of worker processes to use; default is 2')
    parser.add_argument('--parser', default='parser-nytimes',
                        help='The module used to parse HTML body; default is parser-nytimes')
    return parser.parse_args()


if __name__ == "__main__":
    args = get_args()
    DIR_WARC = args.dir_warc
    DIR_OUTPUT = args.dir_output
    PARSER = args.parser

    try:
        makedirs(DIR_OUTPUT)
    except OSError as e:  # Avoid race condition when creating directory
        if e.errno != errno.EEXIST:
            raise

    do_work(args.processes)
