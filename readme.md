# Closest Word Service

This is a service to find similar words using the provided API or a web interface.
It is based on Glove: https://nlp.stanford.edu/projects/glove/


## Installation

### Requirements

* Python 3
* virtualenv
* docker
* docker-compose

### Running the Service

```
$ git clone <URL>:closest_word_service && cd closest_word_service
$ sudo docker-compose up -d
```


## API

Send a JSON object the the endpoint ``/ClosestWord`` with the following form:

```
{
   "word": "coffee",
   "N": 2
}
```

where the field ``word`` contains the word to find similar expressions for. ``N``
is the number of similar words to  be received.

The response will be a JSON object of the  following form:

```
{
  "message": "success",
  "words": ["tea", "cake"]
}
```

Where ``words`` contains the most similar words in descending order.

If the given ``N`` is smaller than 1 or ``word`` is not part of the dictionary,
the ``words`` field will be an empty array. The ``message`` field contains a
status message.

Example of how to use the service from the command line:

```
$ curl --header "Content-Type: application/json" \
       --request POST \
       --data '{"word":"tea", "N":2}' \
       http://localhost:5050/ClosestWord
```

Or just execute the example script:

```
$ ./query.sh
```


## Web Interface

Similar words can also be found through a web interface. Enter the URL where the
service is hosted and enter a word in the search field.
In case you run the docker service on your local machine, type http://localhost in your browser.


## Configuration

The default port for the API is ``5050`` and for the web interface it is ``80``. Changes can be made by modifying the appropriate environmental variables in the docker-compose.yml file.


## Development

In case you would not like to use docker or debug the API / web interface change into the directory ``api`` or ``frontend`` respectively and run:

```
$ cd api/
$ virtualenv env -p python3
$ env/bin/pip install -r requirements.txt
$ source ../envvars
$ env/bin/python api.py
```

Default environmental variables are set in the envvars file.
