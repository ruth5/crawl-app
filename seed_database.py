"""Seeds the database with users."""

import os
# from random import choice, randint
# from datetime import datetime
import crud, model, server

os.system('dropdb crawl')
os.system('createdb crawl')

model.connect_to_db(server.app)
model.db.create_all()

for n in range(10):
    email = f'user{n}@test.com' 
    password = 'test'

    user = crud.create_user(email, password)
