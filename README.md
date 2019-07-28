# API
API gateway to handle the requests

---
By Marco Spanhaak - uploaded 2019-05-31
---

---
Now the API part is build on Python. I assume that you have build up your own Python environment.
---
## Install a virtual environment for Python
Create a new dir and work from there.
```
$ virtualenv venv
$ source venv/bin/activate
$ pip install flask flask-jsonpify flask-sqlalchemy flask-restful
$ pip freeze
```
That is basically all, now you can run the API just as any other Python script.
---
The API needs to go in the scripts folder of the virtual environment.
