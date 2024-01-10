[comment]: # "Auto-generated SOAR connector documentation"
# SQLite

Publisher: Splunk  
Connector Version: 2.1.1  
Product Vendor: SQLite  
Product Name: SQLite  
Product Version Supported (regex): ".\*"  
Minimum Product Version: 5.5.0  

This app supports investigative actions against a local SQLite database

[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2017-2024 Splunk Inc."
[comment]: # ""
[comment]: # "Licensed under the Apache License, Version 2.0 (the 'License');"
[comment]: # "you may not use this file except in compliance with the License."
[comment]: # "You may obtain a copy of the License at"
[comment]: # ""
[comment]: # "    http://www.apache.org/licenses/LICENSE-2.0"
[comment]: # ""
[comment]: # "Unless required by applicable law or agreed to in writing, software distributed under"
[comment]: # "the License is distributed on an 'AS IS' BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND,"
[comment]: # "either express or implied. See the License for the specific language governing permissions"
[comment]: # "and limitations under the License."
[comment]: # ""
If you create an asset without specifying a path to the SQLite database, then a new SQLite database
will be created which is unique to the asset (located at
`     /opt/phantom/local_data/app_states/6eba2c65-cac0-4a5f-9e5d-3c79d2d90aeb/<asset_id>_db.db    `
). It is possible to import existing SQLite databases as well. Copy it over to the Phantom OVA, and
set the "Path to the SQLite database" to the path of this file. Ensure that the user phantom-worker
has read and write access to this file. It is recommended that you place any imported database into
the app's state directory.


### Configuration Variables
The below configuration variables are required for this Connector to operate.  These variables are specified when configuring a SQLite asset in SOAR.

VARIABLE | REQUIRED | TYPE | DESCRIPTION
-------- | -------- | ---- | -----------
**database_path** |  optional  | string | Path to default SQLite database

### Supported Actions  
[test connectivity](#action-test-connectivity) - Validate the asset configuration for connectivity using supplied configuration  
[run query](#action-run-query) - Run a query against a table or tables in the database  
[list columns](#action-list-columns) - List the columns of a table  
[list tables](#action-list-tables) - List the tables in the database  

## action: 'test connectivity'
Validate the asset configuration for connectivity using supplied configuration

Type: **test**  
Read only: **True**

#### Action Parameters
No parameters are required for this action

#### Action Output
No Output  

## action: 'run query'
Run a query against a table or tables in the database

Type: **investigate**  
Read only: **False**

It is recommended to use the <b>format_vars</b> parameter when applicable. For example, if you wanted to find a specific IP, you could set <b>query</b> to a formatted string, like "select \* from my_hosts where ip = ?" (note the use of <b>?</b>), and set <b>format_vars</b> to the IP address. This will ensure the inputs are safely sanitized and avoid SQL injection attacks.<br><br>The <b>format_vars</b> parameter accepts a comma seperated list. You can escape commas by surrounding them in double quotes, and escape double quotes with a backslash. Assuming you have a list of values for the format vars, you can employ this code in your playbooks to properly format it into a string:<br> <code>format_vars_str = ','.join(['"{}"'.format(str(x).replace('\\\\', '\\\\\\\\').replace('"', '\\\\"')) for x in format_vars_list])</code><br><br>Setting <b>no_commit</b> will make it so the App does not commit any changes made to the database (so you can ensure it's a read only query).

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault_id** |  optional  | Vault ID of SQLite database to use | string |  `vault id` 
**query** |  required  | Query string | string |  `sql query` 
**format_vars** |  optional  | Comma separated list of variables | string | 
**no_commit** |  optional  | Do not commit changes to database | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.vault_id | string |  `vault id`  |   da39a3ee5e6b4b0d3255bfef95601890afd80709 
action_result.parameter.format_vars | string |  |   a 
action_result.parameter.no_commit | boolean |  |  
action_result.parameter.query | string |  `sql query`  |   SELECT \* FROM foo WHERE bar = ?; 
action_result.data.\* | string |  |  
action_result.summary.total_rows | numeric |  |  
action_result.message | string |  |   Successfully ran query 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list columns'
List the columns of a table

Type: **investigate**  
Read only: **True**

The <b>table_name</b> parameter must be composed of only alphanumeric characters plus '_' and '$'.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault_id** |  optional  | Vault ID of SQLite database to use | string |  `vault id` 
**table_name** |  required  | Name of table | string |  `sqlite table name` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.vault_id | string |  `vault id`  |   da39a3ee5e6b4b0d3255bfef95601890afd80709 
action_result.parameter.table_name | string |  `sqlite table name`  |   foo 
action_result.data.\*.cid | numeric |  |   0 
action_result.data.\*.dflt_value | string |  |  
action_result.data.\*.name | string |  |   bar 
action_result.data.\*.notnull | numeric |  |   1 
action_result.data.\*.pk | numeric |  |   0 
action_result.data.\*.type | string |  |   text 
action_result.summary.num_columns | numeric |  |  
action_result.message | string |  |   Successfully listed columns 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1   

## action: 'list tables'
List the tables in the database

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault_id** |  optional  | Vault ID of SQLite database to use | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS | EXAMPLE VALUES
--------- | ---- | -------- | --------------
action_result.status | string |  |   success  failed 
action_result.parameter.vault_id | string |  `vault id`  |   da39a3ee5e6b4b0d3255bfef95601890afd80709 
action_result.data.\*.name | string |  `sqlite table name`  |   foo 
action_result.data.\*.rootpage | numeric |  |   2 
action_result.data.\*.sql | string |  |   CREATE TABLE foo (bar text NOT NULL) 
action_result.data.\*.tbl_name | string |  `sqlite table name`  |   foo 
action_result.data.\*.type | string |  |   table 
action_result.summary.num_tables | numeric |  |  
action_result.message | string |  |   Successfully listed tables 
summary.total_objects | numeric |  |   1 
summary.total_objects_successful | numeric |  |   1 