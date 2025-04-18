#!/bin/bash

# Run script.py with arguments to delete all data from the database
python scripts.py database delete_all

# Run schema.py to set up the PostgreSQL schema
python schema.py postgres

# Run seed.py to seed the PostgreSQL database
python seed.py postgres