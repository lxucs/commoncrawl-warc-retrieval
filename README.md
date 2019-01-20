Install dependencies: `pip install -r requirements.txt`

### Pipeline
cdx index files -> filtering -> retrieval -> parsing.

For a detailed walkthrough of how to retrieve web pages of specific domain using CommonCrawl index, please see this [article](https://liyanxu.blog/2019/01/19/retrieve-web-pages-using-commoncrawl-index/).

# CommonCrawl Index Filter
A simple python command line tool for filtering url index from retrieved index files.

## Examples
```./cdx-index-filter.py /Users/abc/input /Users/abc/output```

```./cdx-index-filter.py /Users/abc/input /Users/abc/output --pattern .*www.nytimes.com/20[\\d/]+/us/politics/.+\\.html$```

```./cdx-index-filter.py /Users/abc/input /Users/abc/output -p 4``` (using 4 parallel processes)

## Usage
Below is the current list of options, also available by running `./cdx-index-filter.py -h`
```
usage: CDX Index Filter [-h] [-p PROCESSES] [--pattern PATTERN]
                        dir_input dir_output

positional arguments:
  dir_input             The path of input directory to be filtered
  dir_output            The path of output directory

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        Number of worker processes to use; default is 2
  --pattern PATTERN     Custom url filtering pattern; default is NYTimes US
                        Politics article
```

# CommonCrawl Index Text Retrieval

A simple python command line tool to retrieve indexed text from WARC file.

## Examples
```./cdx-index-retrieval.py /Users/abc/input /Users/abc/output```

```./cdx-index-retrieval.py /Users/abc/input /Users/abc/output -p 4``` (using 4 parallel processes)

## Usage
Below is the current list of options, also available by running `./cdx-index-retrieval.py -h`
```
usage: CDX Index Text Retrieval [-h] [-p PROCESSES] [--strip STRIP]
                                dir_index dir_output

positional arguments:
  dir_index             The path of directory containing index files
  dir_output            The path of output directory

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        Number of worker processes to use; default is 2
  --strip STRIP         Use stripped url as file name of retrieved text;
                        default is to strip everything before .com/
```

# WARC Parser

A simple python command line tool to parse WARC files.

Custom HTML parser can be passed in using the option `--parser`; it should be a module that implements `parse(filename, html_body)`.

## Examples
```./warc-parser.py /Users/abc/input /Users/abc/output --parser parser-nytimes```

```./warc-parser.py /Users/abc/input /Users/abc/output -p 4``` (using 4 parallel processes)

## Usage
Below is the current list of options, also available by running `./warc-parser.py -h`
```
usage: WARC Parser [-h] [-p PROCESSES] [--parser PARSER] dir_warc dir_output

positional arguments:
  dir_warc              The path of directory containing WARC files
  dir_output            The path of output directory

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        Number of worker processes to use; default is 2
  --parser PARSER       The module used to parse HTML body; default is parser-
                        nytimes
```
