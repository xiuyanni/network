#!/usr/bin/env python

from BaseHTTPServer import BaseHTTPRequestHandler
import cgi
import sqlite3
from abc import ABCMeta

HTDATASTORE_DBNAME = 'HiThere.db'


class HiThereDataStore:
    """
        HiThere DataStore (Abstract class)
        Store/Retrieve Data
    """
    __metaclass__ = ABCMeta

    def store(self, username, nickname, password):
        return NotImplemented

    def query(self, username):
        return NotImplemented

    def update_location(self, username, latitude, longtitude):
        return NotImplemented

    def tell_friends(self, username):
        return NotImplemented

    def add_friend(self, username_1, username_2):
        return NotImplemented

import os

class HiThereDataStoreSqlite(HiThereDataStore):
    """
        HiThere DataStore Implementation using Sqlite3
        Refer: https://docs.python.org/2/library/sqlite3.html

        Use Sqlite to store or retrieve data
    """

    def __init__(self):
        """
            Initialize database
        """
        self.dbname = HTDATASTORE_DBNAME

        try:
            os.remove(self.dbname)
        except:
            pass

        _conn = sqlite3.connect(self.dbname)
        _conn.execute("CREATE TABLE users(id integer primary key, username varchar unique, \
            nickname, password, latitude, longtitude)")
        _conn.execute("CREATE TABLE friends(username_1, username_2, share)")
        #_conn.execute("CREATE TABLE locations(username, latitude, longtitude, share)")

    # _conn.execute("CREATE TABLE groups(groupname, crealt, share)")

    def store(self, username, nickname, password):
        """
            create a new user
        """
        try:
            _conn = sqlite3.connect(self.dbname)
            c = _conn.cursor()
            c.execute("INSERT INTO users(username, nickname, password) VALUES (?, ?, ?)", \
                      [username, nickname, password])
            _conn.commit()
        except:
            print "Store: fail to create new User [", username, "]"
            return False

        return True

    def query(self, username):
        """
            return {'username' : <username>, 'password' : <password>}
        """
        try:
            c = sqlite3.connect(self.dbname).cursor()
            c.execute("SELECT * FROM users WHERE username=?", [username])
            row = c.fetchone()
            return {'username': row[1], 'password': row[3]}
        except:
            print "Query: fail to get user [", username, "]"
        return None


    def update_location(self, username, latitude, longtitude):

        try:
            _conn = sqlite3.connect(self.dbname)
            c = _conn.cursor()
            c.execute("UPDATE users SET latitude=?, longtitude=? WHERE username=?", [latitude, longtitude, username])
            _conn.commit()
        except:
            print "Update location: fail to update the location of user [", username, "]"
            return False
        return True


    def tell_friends(self, username):

        try:
            c = sqlite3.connect(self.dbname).cursor()
            c.execute("SELECT users.username, users.latitude, users.longtitude  FROM users JOIN (SELECT username_2 FROM friends WHERE username_1=?) AS temp ON temp.username_2=users.username",[username])
            
            rows = c.fetchall()
            print rows
            return rows

           # print  [(u'bob@gmail.com', u'976', u'787'), (u'cherry@gmail.com', u'1276', u'689')]


        except:
            print "Tell friends: fail to get user [", username, "]'s friends."
        return None


    def add_friend(self, username_1, username_2):

        try:
            _conn = sqlite3.connect(self.dbname)
            c = _conn.cursor()
            c.execute("INSERT INTO friends(username_1, username_2) VALUES (?, ?)", [username_1, username_2])
            _conn.commit()
        except:
            print "add friend: fail to add friend [", username_2, "] to the user [", username_1, "]"
            return False
        return True


    # create a new instance for DataStore (here, we use Sqlite implementation)


HTDataStore = HiThereDataStoreSqlite()

# constant
INVALID_CMDJSON = '{"Status" : "Fail", "Reason" : "Invalid Request"}'


class HiThereProtocol:
    """
        HiThere Communication Protocol (Abstract Class)
    """
    __metaclass__ = ABCMeta

    @staticmethod
    def process(dict):
        """
            Ultrimate Interface to HiThereProtocol
        """
        if 'command' not in dict.keys():
            return INVALID_CMDJSON
        try:
            cmd = dict['command'].lower()
            # find the right function
            cmd_method = getattr(HiThereProtocolJSON, cmd)  # FIXME
            return cmd_method(dict)
        except:
            print "Process: No Command Found! (", cmd, ")."
            pass
        return INVALID_CMDJSON

    @staticmethod
    def register(d):
        """
            Register new user
        """
        return NotImplemented

    @staticmethod
    def login(d):
        """
            User Login
        """
        return NotImplemented

    # TODO
    # you need support from DataStore which stores the location data
    @staticmethod
    def checkin(d):
        """
            Check-in user's location
            INPUT:
                {"username" : "alice@gmail.com", "latitude" : -128.00, "longtitude" : 20.00"}
        """
        return NotImplemented


    # TODO
    # Note: You need DataStore provides interface to access persistent data, e.g. db
    # so as to get the friend list
    @staticmethod
    def getfriendlist(d, b):
        """
            Get Friend list
            Input:
                d - dictionary of parameters
                b - whether include locations
        """
        return NotImplemented


    @staticmethod
    def addfriend(d):
        """
                    Get Friend list
                    Input:
                    d - dictionary of parameters
        """
        return NotImplemented


class HiThereProtocolJSON(HiThereProtocol):
    """
        HiThere Communication Protocol Implementation in JSON (Response)

        Input: dictionary of request, e.g.
            { "command" : "register", "username" : "alice@gmail.com", "password" : "123"}

        Output: (JSON) e.g.
            { "Status" : "OK"} (if sucess)
            { "Status" : "Fail", "Reason" : "Invalid Parameter"} (If fail)
    """

    @staticmethod
    def register(dict):
        """
            Register a user
            INPUT:
            { "command" : "register", "username" : "alice@gmail.com", "password" : "123"}
            OUTPUT:
            { "Status" : "OK"} (if sucess)
            { "Status" : "Fail", "Reason" : "Invalid Parameter"} (If fail)
        """
        assert 'command' in dict.keys()
        assert dict['command'] == 'register'

        try:
            username = dict['username']
            password = dict['password']
            nickname = ''
            if 'nickname' in dict.keys():
                nickname = dict['nickname'].value
            # save to data store
            success = HTDataStore.store(username, nickname, password)
            if success:
                print "Register: user [", username, "] registered"
                return '{"Status" : "OK"}'
        except:
            print "Register: fail to parse"

        return INVALID_CMDJSON

    @staticmethod

    def login(dict):
        """
                User login
                INPUT:
                { "command" : "login", "username" : "alice@gmail.com", "password" : "123"}
                OUTPUT:
                { "Status" : "OK"} (if sucess)
                { "Status" : "Fail", "Reason" : "Invalid Parameter"} (If fail)
                """
        assert 'command' in dict.keys()
        assert dict['command'] == 'login'
        try:
            username = dict['username']

            # request to data store for credentials
            cred = HTDataStore.query(username)

            # validate the password
            if cred['password'] == dict['password']:
                print "Login: user [", username, "] authenticated."
                return '{"Status" : "OK"}'
        except:
            print "Login: user [", username, "](", dict['password'], ") failed."
            print cred

        return '{"Status" : "Fail"}'


    @staticmethod
    def checkin(dict):
        """
                    User login
                    INPUT:
                    { "command" : "checkin", "username" : "alice@gmail.com", "latitude" : "876",
                    "longtitude" : "987"}
                    OUTPUT:
                    { "Status" : "OK"} (if sucess)
                    { "Status" : "Fail", "Reason" : "Invalid Parameter"} (If fail)
                """

        assert 'command' in dict.keys()
        assert dict['command'] == 'checkin'

        try:
            username = dict['username']
            latitude = dict['latitude']
            longtitude = dict['longtitude']
            success = HTDataStore.update_location(username, latitude, longtitude)
         #   print "success:", success

            if success:
                print "Checkin: user [", username, "] updated location."
                return '{"Status" : "OK"}'

        except:
            print "Checkin: user [", username, "] location update failed."
            return '{"Status" : "Fail"}'


    @staticmethod
    def getfriendlist(dict):
        """
                    Get Friend List
                    INPUT:
                    { "command" : "getfriendlist", "username" : "alice@gmail.com"}
                    OUTPUT:
                    { "Status" : "OK"} (if sucess)
                    { "Status" : "Fail", "Reason" : "Invalid Parameter"} (If fail)
                """
        assert 'command' in dict.keys()
        assert dict['command'] == 'getfriendlist'

        try:
            username = dict['username']
            row = HTDataStore.tell_friends(username)
            print row
            return row

        except:
            print "Get Friend List: friend list for user [", username, "] cannot be returned."
            return '{"Status" : "Fail"}'



    @staticmethod
    def addfriend(dict):
        """
                    Get Friend List
                    INPUT:
                    { "command" : "addfriend", "username1" : "alice@gmail.com", "username2" : "bob@gmail.com"}
                    OUTPUT:
                    { "Status" : "OK"} (if sucess)
                    { "Status" : "Fail", "Reason" : "Invalid Parameter"} (If fail)
                """
        assert 'command' in dict.keys()
        assert dict['command'] == 'addfriend'

        try:
            username1 = dict['username1']
            username2 = dict['username2']
            success = HTDataStore.add_friend(username1, username2)

            if success:
                print "Addfriend: user [", username1, "] added [", username2, "] as friend."
                return '{"Status" : "OK"}'

        except:
            print "addFriend: user [", username1, "] add friend failed."
            return '{"Status" : "Fail"}'


class PostHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        # Parse the form data posted
        form = cgi.FieldStorage(fp=self.rfile,
                                headers=self.headers,
                                environ={'REQUEST_METHOD': 'POST',
                                         'CONTENT_TYPE': self.headers['Content-Type'],
                                })

        # Begin the response
        self.send_response(200)
        self.end_headers()
        values = [form[k].value for k in form.keys()]
        dict = {k.lower(): v for k, v in zip(form.keys(), values)}
        print dict

        response = HiThereProtocolJSON.process(dict)
        assert response is not None
        print response
        self.wfile.write(response + '\n')


if __name__ == '__main__':
    from BaseHTTPServer import HTTPServer

    server = HTTPServer(('127.0.0.1', 8080), PostHandler)
    print 'Starting server, use <Ctrl-C> to stop'

    server.serve_forever()
