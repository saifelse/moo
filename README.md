moo
===

A scavenger hunt!

Cloning and setting up
---------------
```
git clone git@github.com:saifelse/moo.git
cd moo
pip install -r requirements.txt
python manage.py compile
python manage.py scss
```

Start a shell to initialize the DB:
```
python manage.py shell
```

Then run the following:
```
import moo
moo.reset_db()
```

Running locally
---------------
`python manage.py runserver`

Deploying
---------
`fab deploy`

