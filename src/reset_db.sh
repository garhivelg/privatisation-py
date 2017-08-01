#! /bin/bash
rm ../db/privatisation.db && alembic upgrade head
