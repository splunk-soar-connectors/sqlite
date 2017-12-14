# --
# File: sqlite_connector.py
#
# Copyright (c) Phantom Cyber Corporation, 2017
#
# This unpublished material is proprietary to Phantom Cyber.
# All rights reserved. The methods and
# techniques described herein are considered trade secrets
# and/or confidential. Reproduction or distribution, in whole
# or in part, is forbidden except by express written permission
# of Phantom Cyber.
#
# --

import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult

import os
import re
import csv
import json
import sqlite3
import requests


class RetVal(tuple):
    def __new__(cls, val1, val2=None):
        return tuple.__new__(RetVal, (val1, val2))


class SqliteConnector(BaseConnector):

    def __init__(self):
        super(SqliteConnector, self).__init__()
        self._state = None

    def _get_format_vars(self, param):
        format_vars = param.get('format_vars')
        if format_vars:
            format_vars = csv.reader([format_vars], quotechar='"', skipinitialspace=True, escapechar='\\').next()
        else:
            format_vars = tuple()
        return format_vars

    def _get_query_results(self, action_result):
        try:
            columns = self._cursor.description
            results = [{columns[index][0]:column for index, column in enumerate(value)} for value in self._cursor.fetchall()]
        except Exception as e:
            return RetVal(action_result.set_status(
                phantom.APP_ERROR,
                "Unable to retrieve results from query",
                e
            ))

        return RetVal(phantom.APP_SUCCESS, results)

    def _handle_test_connectivity(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        query = "pragma schema_version;"
        try:
            self._cursor.execute(query)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Test connectivity failed", e
            )

        query = "select sqlite_version();"
        try:
            self._cursor.execute(query)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Test connectivity failed", e
            )

        version = self._cursor.fetchall()[0]
        self.save_progress("Using SQLite Version {}".format(version))
        self.save_progress("Test connectivity passed")
        return action_result.set_status(phantom.APP_SUCCESS)

    def _handle_run_query(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        query = param['query']
        format_vars = self._get_format_vars(param)

        try:
            # The BEGIN starts the query as a transaction, so the changes
            #  will not autocommit (i.e. create / drop table)
            self._cursor.execute('BEGIN')
            self._cursor.execute(query, format_vars)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Error running query", e
            )

        if not param.get('no_commit', False):
            try:
                self._connection.commit()
            except Exception as e:
                return action_result.set_status(
                    phantom.APP_ERROR, "Unable to commit changes", e
                )

        ret_val, results = self._get_query_results(action_result)
        if phantom.is_fail(ret_val):
            return ret_val

        for row in results:
            action_result.add_data(row)

        summary = action_result.update_summary({})
        summary['total_rows'] = len(results)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully ran query")

    def _handle_list_columns(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))
        table_name = param['table_name']

        if not re.match(r'^[a-z0-9_$]+$', table_name, re.IGNORECASE):
            return action_result.set_status(
                phantom.APP_ERROR,
                "table_name can only contains alphanumeric characters + '_' and '$'"
            )

        query = "SELECT * FROM sqlite_master WHERE type='table' AND name=?;"
        try:
            self._cursor.execute(query, (table_name,))
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Error listing tables", e
            )

        results = self._cursor.fetchall()
        if len(results) < 1:
            return action_result.set_status(phantom.APP_ERROR, "There is no table with that name")

        query = "PRAGMA table_info({});".format(table_name)

        try:
            self._cursor.execute(query)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Error listing columns", e
            )

        ret_val, results = self._get_query_results(action_result)
        if phantom.is_fail(ret_val):
            return ret_val

        for row in results:
            action_result.add_data(row)

        summary = action_result.update_summary({})
        summary['num_columns'] = len(results)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully listed columns")

    def _handle_list_tables(self, param):
        action_result = self.add_action_result(ActionResult(dict(param)))

        query = "SELECT * FROM sqlite_master WHERE type='table';"
        try:
            self._cursor.execute(query)
        except Exception as e:
            return action_result.set_status(
                phantom.APP_ERROR, "Error listing tables", e
            )

        ret_val, results = self._get_query_results(action_result)
        if phantom.is_fail(ret_val):
            return ret_val

        for row in results:
            action_result.add_data(row)

        summary = action_result.update_summary({})
        summary['num_tables'] = len(results)

        return action_result.set_status(phantom.APP_SUCCESS, "Successfully listed tables")

    def handle_action(self, param):

        ret_val = phantom.APP_SUCCESS

        # Get the action that we are supposed to execute for this App Run
        action_id = self.get_action_identifier()

        self.debug_print("action_id", self.get_action_identifier())

        if action_id == 'test_connectivity':
            ret_val = self._handle_test_connectivity(param)

        elif action_id == 'run_query':
            ret_val = self._handle_run_query(param)

        elif action_id == 'list_columns':
            ret_val = self._handle_list_columns(param)

        elif action_id == 'list_tables':
            ret_val = self._handle_list_tables(param)

        return ret_val

    def _initialize_error(self, msg, exception=None):
        if self.get_action_identifier() == "test_connectivity":
            self.save_progress(msg)
            if exception:
                self.save_progress(str(exception))
            self.set_status(phantom.APP_ERROR, "Test Connectivity Failed")
        else:
            self.set_status(phantom.APP_ERROR, msg, exception)
        return phantom.APP_ERROR

    def initialize(self):
        config = self.get_config()
        self._state = self.load_state()
        path = config.get('database_path')
        if path is None:
            state_dir = self.get_state_dir()
            asset_id = self.get_asset_id()
            path = '{}/{}_db.db'.format(state_dir, asset_id)
        else:
            # Don't create a databse if they provided a path, throw an error if it doesn't exist
            if not os.path.isfile(path):
                return self._initialize_error("No SQLite database could be found at provided path")

        try:
            self._connection = sqlite3.connect(
                path,
                detect_types=sqlite3.PARSE_DECLTYPES | sqlite3.PARSE_COLNAMES,
                isolation_level=None
            )
            self._cursor = self._connection.cursor()
        except Exception as e:
            return self._initialize_error("error connecting to database", e)
        self.save_progress("Database connection established")
        return phantom.APP_SUCCESS

    def finalize(self):
        self.save_state(self._state)
        return phantom.APP_SUCCESS


if __name__ == '__main__':

    import sys
    import pudb
    import argparse

    pudb.set_trace()

    argparser = argparse.ArgumentParser()

    argparser.add_argument('input_test_json', help='Input Test JSON file')
    argparser.add_argument('-u', '--username', help='username', required=False)
    argparser.add_argument('-p', '--password', help='password', required=False)

    args = argparser.parse_args()
    session_id = None

    username = args.username
    password = args.password

    if (username is not None and password is None):

        # User specified a username but not a password, so ask
        import getpass
        password = getpass.getpass("Password: ")

    if (username and password):
        try:
            print ("Accessing the Login page")
            r = requests.get("https://127.0.0.1/login", verify=False)
            csrftoken = r.cookies['csrftoken']

            data = dict()
            data['username'] = username
            data['password'] = password
            data['csrfmiddlewaretoken'] = csrftoken

            headers = dict()
            headers['Cookie'] = 'csrftoken=' + csrftoken
            headers['Referer'] = 'https://127.0.0.1/login'

            print ("Logging into Platform to get the session id")
            r2 = requests.post("https://127.0.0.1/login", verify=False, data=data, headers=headers)
            session_id = r2.cookies['sessionid']
        except Exception as e:
            print ("Unable to get session id from the platfrom. Error: " + str(e))
            exit(1)

    if (len(sys.argv) < 2):
        print "No test json specified as input"
        exit(0)

    with open(sys.argv[1]) as f:
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=4))

        connector = SqliteConnector()
        connector.print_progress_message = True

        if (session_id is not None):
            in_json['user_session_token'] = session_id

        ret_val = connector._handle_action(json.dumps(in_json), None)
        print (json.dumps(json.loads(ret_val), indent=4))

    exit(0)
