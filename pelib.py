'''This is a helper module that defines the PE object and the PEobj class 
responsible for loading and parsing PE data'''

import pefile
import os
import logging

from hashlib import sha1
from sys import exit, stderr
from textwrap import dedent

log = logging.getLogger(__name__)

class Executable:
    '''Class for the analysed PEs
    'size' and 'data' have no default value as the object is initiated when the
    file is loaded after basic integrity checks, so we'll always have the
    name and the data, which is just the file dump. Other vars are filled in 
    in parse_data().
    '''

    def __init__(self, name, data, size=None, type=None, sha1=None, imp=None):
        self.file_name = name
        self.data = data
        self.file_size = size
        self.file_type = type
        self.sha1_hash = sha1
        self.imp_hash = imp

    def display_info(self):
        ''''''
        print(dedent(
        f'''
        PE details:
        Name:      {self.file_name}
        Size:      {self.file_size}
        Type:      {','.join(self.file_type)}
        SHA1 hash: {self.sha1_hash}
        Imp hash:  {self.imp_hash}
        '''
        ))

    def dump_info(self):
        pass

class PEobj:

    def load_file(filename):
        '''Loads the file to memory and creates the object'''

        # Ugly way to handle exception handling for file loads, I know
        try:
            f = open(filename, 'rb')
        except IOError as error:
            log.error('Error loading file: ' + error)
        else:
            with f:
                data = f.read()
                result = Executable(filename, data)
                return result

    def parse_data(object):
        '''Parses the PE, gathers information and updates the object'''

        try:
            file = pefile.PE(data=object.data)
        except pefile.PEFormatError as error:
            log.error('Error parsing file: ' + str(error) + " " + object.file_name)
            return

        object.file_size = len(object.data)
        object.sha1_hash = sha1(object.data).hexdigest()
        object.imp_hash = file.get_imphash()

        file_characteristics = file.FILE_HEADER.Characteristics
        object.file_type = PEobj.characteristics(file_characteristics)

    def characteristics(value):
        '''Tester for the FILE_HEADER.Characteristics to determine the PE type
        Takes in'''

        flags = {
            'DLL': 0x2000,
            'SYS': 0x1000,
            'EXE': 0x0002
        }

        result = []

        for i in flags.keys():
            if bool(value & flags[i]):
                result.append(i)
        
        return result

if __name__ == "__main__":
    log.error('\'tis but a helper script!')