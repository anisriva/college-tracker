'''
Use this module for fetching the 
system configurations.
Class object can be used as a iterable,.
ex: 
obj = PropsLoader()
obj['themes']
'''
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

__version__ = '0.1'

import logging
from os.path import expandvars
from yaml import safe_load, YAMLError

class PropsLoader(object):

    '''
    Configuration access provider
    '''
    def __init__(self,file='resources\settings.yaml'):
        self.config = self.__get_file(file)
    
    def __getitem__(self,key):
        if isinstance(self.config[key], int):
            return self.config[key]
        else:
            return expandvars(self.config[key])

    @classmethod
    def __get_file(cls,file):
        '''
        Retrieve connections from connections.yml file
        '''
        with open(file, 'r') as stream:
            try:
                return safe_load(stream)
            except YAMLError as e:
                logging.error('Issue with connections file -> {} : {}'.format(file,e))
                return None