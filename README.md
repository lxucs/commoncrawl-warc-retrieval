All tools can be used directly to retrieve and parse NYTimes US Politics articles. Support for more data source will be added later.

Install dependencies: `pip install -r requirements.txt`

### Pipeline
cdx index files -> filtering -> retrieval -> parsing.

# CommonCrawl Index Filter
A simple python command line tool for filtering url index from retrieved index files.

## Examples
```./cdx-index-filter.py /Users/abc/input /Users/abc/output```

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
usage: CDX Index Text Retrieval [-h] [-p PROCESSES] dir_index dir_output

positional arguments:
  dir_index             The path of directory containing index files
  dir_output            The path of output directory

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        Number of worker processes to use; default is 2
```

# WARC Parser

A simple python command line tool to parse WARC files.

## Examples
```./warc-parser.py /Users/abc/input /Users/abc/output```

```./warc-parser.py /Users/abc/input /Users/abc/output -p 4``` (using 4 parallel processes)

## Usage
Below is the current list of options, also available by running `./warc-parser.py -h`
```
usage: WARC-Parser [-h] [-p PROCESSES] dir_warc dir_output

positional arguments:
  dir_warc              The path of directory containing WARC files
  dir_output            The path of output directory

optional arguments:
  -h, --help            show this help message and exit
  -p PROCESSES, --processes PROCESSES
                        Number of worker processes to use; default is 2
```