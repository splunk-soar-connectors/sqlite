[comment]: # "Auto-generated SOAR connector documentation"
# SQLite

Publisher: Phantom  
Connector Version: 2\.0\.3  
Product Vendor: SQLite  
Product Name: SQLite  
Product Version Supported (regex): "\.\*"  
Minimum Product Version: 4\.9\.39220  

This app supports investigative actions against a local SQLite database

[comment]: # " File: readme.md"
[comment]: # "  Copyright (c) 2017-2022 Splunk Inc."
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
**database\_path** |  optional  | string | Path to default SQLite database

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

It is recommended to use the <b>format\_vars</b> parameter when applicable\. For example, if you wanted to find a specific IP, you could set <b>query</b> to a formatted string, like "select \* from my\_hosts where ip = ?" \(note the use of <b>?</b>\), and set <b>format\_vars</b> to the IP address\. This will ensure the inputs are safely sanitized and avoid SQL injection attacks\.<br><br>The <b>format\_vars</b> parameter accepts a comma seperated list\. You can escape commas by surrounding them in double quotes, and escape double quotes with a backslash\. Assuming you have a list of values for the format vars, you can employ this code in your playbooks to properly format it into a string\:<br> <code>format\_vars\_str = ','\.join\(\['"\{\}"'\.format\(str\(x\)\.replace\('\\\\', '\\\\\\\\'\)\.replace\('"', '\\\\"'\)\) for x in format\_vars\_list\]\)</code><br><br>Setting <b>no\_commit</b> will make it so the App does not commit any changes made to the database \(so you can ensure it's a read only query\)\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault\_id** |  optional  | Vault ID of SQLite database to use | string |  `vault id` 
**query** |  required  | Query string | string |  `sql query` 
**format\_vars** |  optional  | Comma separated list of variables | string | 
**no\_commit** |  optional  | Do not commit changes to database | boolean | 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.format\_vars | string | 
action\_result\.parameter\.no\_commit | boolean | 
action\_result\.parameter\.query | string |  `sql query` 
action\_result\.data\.\* | string | 
action\_result\.summary\.total\_rows | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list columns'
List the columns of a table

Type: **investigate**  
Read only: **True**

The <b>table\_name</b> parameter must be composed of only alphanumeric characters plus '\_' and '$'\.

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault\_id** |  optional  | Vault ID of SQLite database to use | string |  `vault id` 
**table\_name** |  required  | Name of table | string |  `sqlite table name` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.parameter\.table\_name | string |  `sqlite table name` 
action\_result\.data\.\*\.cid | numeric | 
action\_result\.data\.\*\.dflt\_value | string | 
action\_result\.data\.\*\.name | string | 
action\_result\.data\.\*\.notnull | numeric | 
action\_result\.data\.\*\.pk | numeric | 
action\_result\.data\.\*\.type | string | 
action\_result\.summary\.num\_columns | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric |   

## action: 'list tables'
List the tables in the database

Type: **investigate**  
Read only: **True**

#### Action Parameters
PARAMETER | REQUIRED | DESCRIPTION | TYPE | CONTAINS
--------- | -------- | ----------- | ---- | --------
**vault\_id** |  optional  | Vault ID of SQLite database to use | string |  `vault id` 

#### Action Output
DATA PATH | TYPE | CONTAINS
--------- | ---- | --------
action\_result\.status | string | 
action\_result\.parameter\.vault\_id | string |  `vault id` 
action\_result\.data\.\*\.name | string |  `sqlite table name` 
action\_result\.data\.\*\.rootpage | numeric | 
action\_result\.data\.\*\.sql | string | 
action\_result\.data\.\*\.tbl\_name | string |  `sqlite table name` 
action\_result\.data\.\*\.type | string | 
action\_result\.summary\.num\_tables | numeric | 
action\_result\.message | string | 
summary\.total\_objects | numeric | 
summary\.total\_objects\_successful | numeric | 