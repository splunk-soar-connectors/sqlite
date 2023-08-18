[comment]: # " File: README.md"
[comment]: # "  Copyright (c) 2017-2023 Splunk Inc."
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
