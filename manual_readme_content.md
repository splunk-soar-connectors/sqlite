If you create an asset without specifying a path to the SQLite database, then a new SQLite database
will be created which is unique to the asset (located at
`     /opt/phantom/local_data/app_states/6eba2c65-cac0-4a5f-9e5d-3c79d2d90aeb/<asset_id>_db.db    `
). It is possible to import existing SQLite databases as well. Copy it over to the Phantom OVA, and
set the "Path to the SQLite database" to the path of this file. Ensure that the user phantom-worker
has read and write access to this file. It is recommended that you place any imported database into
the app's state directory.
