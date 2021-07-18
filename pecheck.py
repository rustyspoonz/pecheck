#!/usr/bin/env python3

import argparse
import os
import json
import time
import logging
import sys

from pelib import PEobj

def setup_parsing():
    '''Sets up command line arguments parsing'''
    parser = argparse.ArgumentParser(description="Parses PE files and prints \
                                     out some basic data. Can also dump data \
                                     to a json file instead of printing the \
                                     results")
    parser.add_argument("file", help="file or directory to check")
    parser.add_argument("-r", help="recursive directory checking", 
                        action="store_true") 
    group = parser.add_mutually_exclusive_group()
    group.add_argument("-d", help="dump the results to a json file", 
                        action="store_true")
    group.add_argument("-p", help="by default output is presented after all \
                        jobs in the queue are processed. This switch allows \
                        overriding this setting and printing the results as \
                        they are parsed", action="store_true")
    parser.add_argument("-o", help="set where to save your dumped output", 
                        default='./output')
    parser.add_argument("-q", help="suppress error output aka the silent mode", 
                        action="store_true")
    args = parser.parse_args()

    return args

def job_queue(filename, recursive, dump, progress, outfile):
    '''Main function that handles file queue and output, takes in arguments 
    from the command line and determines if it's working on a directory or a 
    file'''

    queue = []
    results = []

    # Determine if we're handling a file or a directory
    if recursive:
        queue = [os.path.join(path, name) 
                  for path, subdirs, files in os.walk(filename) 
                  for name in files]
    else:
        if os.path.isdir(filename):
            queue = [i for i in os.listdir(filename)]
        elif os.path.isfile(filename):
            queue.append(filename)
        else:
            logging.error("This seems like a special or nonexistent file. \
                I'm not designed for this! Beep boop beep")
    
    if len(queue) > 0:
        for i in queue:
            result = PEobj.load_file(i)
            PEobj.parse_data(result)
            results.append(result)
            if progress:
                if result.file_type:
                    result.display_info()
    else:
        logging.error('No files to process.')
        return

    if not progress:
        if not dump:
            for i in results:
                # Outputs only relevant files, dump option is more complete
                if i.file_type:
                    i.display_info()
        else:
            # Creating a dictionary to convert to json and save to file
            output = {}         
            counter = 0
            for i in results:
                output[counter] = {}
                output[counter]['file_name'] = i.file_name
                output[counter]['file_size'] = i.file_size
                output[counter]['file_type'] = i.file_type
                output[counter]['sha1_hash'] = i.sha1_hash
                output[counter]['imp_hash'] = i.imp_hash
                counter += 1
            
            out_file_name = outfile+"_"+str(round(time.time()))
            with open(out_file_name, 'w') as out:
                logging.info('Dumping output to file: ' + out_file_name)
                json.dump(output, out)

if __name__ == "__main__":
    args = setup_parsing()
    logFormat = '%(message)s'
    if args.q:
        logging.basicConfig(format=logFormat, stream=sys.stdout, 
                            level=logging.CRITICAL)
    else:
        logging.basicConfig(format=logFormat, stream=sys.stdout, 
                            level=logging.INFO)    
    job_queue(args.file, args.r, args.d, args.p, args.o)