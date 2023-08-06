# Lord Of The Rings SDK

Description: An SDK that makes it easy for developers to consume information about the Lord of The Rings trilogy.

SDK builds on an existing [Lord of The Rings API](https://the-one-api.dev/)


### Tech Stack
Built using Python 3.10.5 (see `.python-version` file). External libraries are kept as minimal as possible 
(see `requirements.in` file)

## Installation
```commandline
pip install lord-aubrey-of-the-rings
```


## Run
Register and login [here](https://the-one-api.dev/sign-up) to get your _access token_. 

Import the class `LordOfTheRings` and call the available methods, passing params where necessary. Example:

```python
from lord_of_the_rings.endpoints import LordOfTheRings

client = LordOfTheRings(access_token='your_access_token')

client.get_books()
client.get_movies('5cd95395de30eff6ebccde5b')
client.get_characters('5cd99d4bde30eff6ebccfe2e', 'quote')
```

There are also the options of 

Pagination:
```python
client.get_characters(limit=2)
client.get_characters(page=3)
client.get_characters(offset=11)
```

Sorting:
```python
client.get_books(sort='name:asc')
client.get_quotes(sort='dialog:desc')
```

and Filtering:
```python
client.get_characters(name='Gandalf')
client.get_characters(race='Hobbit,Human')
```

Consult the [API docs](https://the-one-api.dev/documentation) for more information

Exposed methods:
```json lines
METHOD          : PARAMETER(S)
get_books       : identifier (optional), 'chapter' (optional, requires identifier)
get_movies      : identifier (optional), 'quote' (optional, requires identifier)
get_characters  : identifier (optional), 'quote' (optional, requires identifier)
get_quotes      : identifier (optional)
get_chapters    : identifier (optional)
```


## Install (to run SDK locally)
Clone github repo and run the following code. It creates a fresh virtual environment (called .venv) and 
installs requirements
```commandline
make setup
```

Install pip requirements / Sync requirements.in with requirements.txt
```commandline
make pip_sync
```


### Run tests
```commandline
make runtest
```
