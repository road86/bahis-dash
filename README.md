## Installation
First [install pipenv](https://pipenv.pypa.io/en/latest/install/), or run the command below to confirm it works. If you installed pipenv using `sudo apt install pipenv` and [getting this error](https://github.com/pypa/pipenv/issues/5133) install using `pip` instaed.
```
pipenv install
```
and copy data to `exported_data`.

If you get an error when running install
```
Resolving dependencies...
✘ Locking Failed!
```
remove the `Pipfile.lock` file and run again.
## Running
```
pipenv shell
python prep_data.py
python prepgeojson.py
python prepquickdata.py
python index.py
```
