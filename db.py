'''
Backend sqlite3 db module.
'''

from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from builtins import *

__version__ = '0.1'

import sqlite3
from xlsxwriter.workbook import Workbook

class Database:

    @classmethod
    def get_queries(cls, name):
        '''
        Store all queries here
            :param name - Get the name of the query
        '''
        init = '''
                CREATE TABLE IF NOT EXISTS 
                `students` (
                    `id` INTEGER PRIMARY KEY,
                    `year` INTEGER,
                    `term` INTEGER,
                    `program` text,
                    `tot_enroll_planned` INTEGER,
                    `pland_stds` INTEGER,
                    `pattern` INTEGER
                    );
                '''
        fetch_students = "SELECT * FROM `students`"                
        fetch_student = "SELECT * FROM `students` where id = ?"

        insert_student = '''
                    INSERT INTO `students` 
                    VALUES (NULL, ?, ?, ?, ?, ?, ?)
                    '''
        
        remove_student = '''
                    DELETE FROM `students` where id = ?
                    '''
        
        modify_student = '''
                    UPDATE `students`
                    SET `year`=?,
                    `term`=?,
                    `program`=?,
                    `tot_enroll_planned`=?,
                    `pland_stds`=?,
                    `pattern`=?
                    where `id`=?
                    '''
        if name == 'init':
            return [init]
        elif name == 'fetch_students':
            return [fetch_students]
        elif name == 'fetch_student':
            return [fetch_student]            
        elif name == 'insert_student':
            return [insert_student]
        elif name == 'remove_student':
            return [remove_student]
        elif name == 'modify_student':
            return [modify_student]
    
    def execute_queries(
                    self, 
                    query, 
                    type = 'get'
                    ):
        '''
        Query executor for all the 
        non parameterized queries (without ?).
            :param - query - Query to be executed
            :param - type - ['get' or 'set]
                        get will return the values
                        set will only run the query and return nothing
        '''
        try:
            self.cur.execute(query)
        except Exception as e:
            print(f'Issue occured while running {query} : {e}')
            return False, e
        else:
            print(f'{type} type successfully executed')
            if type == 'get':
                rows = self.cur.fetchall()
                return True, rows
            elif type == 'set':
                self.conn.commit()
                return True, None

    def __init__(self, db):
        self.conn = sqlite3.connect(db)
        self.cur = self.conn.cursor()
        for query in self.get_queries('init'):
            self.execute_queries(query, 'set')
    
    def insert_student(
                    self,*columns
                    ):
        '''
        Inserts student into the db
            :param - columns arguments (all the columns values)
            ex : insert_student('2009', 2, 'Data Analytics', 2)
        '''
        query = self.get_queries('insert_student')[0]
        try:
            self.cur.execute(query,tuple(columns))
        except Exception as e:
            print(f'Unable to add the entry : {e}')
        else:
            self.conn.commit()
            print(f'Entry successfully added : {columns}')
    
    def remove_student(self, id):
        '''
        Removes the entry with the provided id
        '''
        query = self.get_queries('remove_student')[0]
        try:
            print(query, (id,))
            self.cur.execute(query, (id,))
        except Exception as e:
            print(f'Unable to remove the entry : {e}')
        else:
            self.conn.commit()
            print(f'Entry successfully removed for id : {id}')
    
    def modify_sudent(self, *columns):
        '''
        Updates the passed columns for a particular id
         :param columns : - Update columns , id column
        '''
        query = self.get_queries('modify_student')[0]
        try:
            print(query, tuple(columns))
            self.cur.execute(query, tuple(columns))
        except Exception as e:
            print(f'Unable to modify the entry : {e}')
        else:
            self.conn.commit()
            print(f'Entry successfully modified to {columns}')

    def get_student(self, id=None):
        '''
        Fetch entries(s)
            :param - id [default - None]
            returns specied or all the data from the data store.
        '''
        try:
            if id:
                query = self.get_queries('fetch_student')[0]
                self.cur.execute(query, (id,))
            else:
                query = query = self.get_queries('fetch_students')[0]
                self.cur.execute(query)
        except Exception as e:
           print(f'Unable to fetch data : {e}')
        else:
           print(f'Successfully fetched')
           return self.cur.fetchall()
    
    def __del__(self):
        '''
        Connection destroyer
        '''
        self.cur.close()
        self.conn.close()
    
    def export_data(self, path):
        '''
        Export data to the excel file
        '''
        workbook = Workbook(path)
        worksheet = workbook.add_worksheet()
        data = [tuple( [row[0] for row in self.cur.description])]
        rows = self.get_student()
        data.extend(rows)
        for i, row in enumerate(data):
            for j, _ in enumerate(row):
                worksheet.write(i, j, row[j])
        workbook.close()
        return
