# pecheck

A simple script I wrote for a job interview that loads a PE file, pulls some basic data from it and displays or dumps into a json file.

```
$ python3 pecheck.py -h
usage: pecheck.py [-h] [-r] [-d | -p] [-o O] [-q] file

Parses PE files and prints out some basic data. Can also dump data to a json
file instead of printing the results

positional arguments:
  file        file or directory to check

optional arguments:
  -h, --help  show this help message and exit
  -r          recursive directory checking
  -d          dump the results to a json file
  -p          by default output is presented after all jobs in the queue are
              processed. This switch allows overriding this setting and
              printing the results as they are parsed
  -o O        set where to save your dumped output
  -q          suppress error output aka the silent mode
  ```
