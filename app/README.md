
Installation
------------

create a virtual environment and install the requirements:

    $ virtualenv env
    $ source env/bin/activate
    (env) $ pip install -r requirements.txt
    (env) $ sudo apt-get install python-tk

Running
-------

To run the server use the following command:

    (env) $ python main.py
     * Running on http://127.0.0.1:8080/

Then from a different terminal window you can send requests.

Examples
-------

The following `curl` command registers a new user with email `client@jdc.fr` and password `jdc` (Uncomment the new_user method first in main.py):

    $ curl -i -X POST -H "Content-Type: application/json" -d '{"email":"client@jdc.fr","password":"jdc"}' http://127.0.0.1:8080/users

    HTTP/1.0 201 CREATED
  	Content-Type: application/json
  	Content-Length: 31
  	Server: Werkzeug/0.12.2 Python/2.7.12
  	Date: Sun, 23 Jul 2017 11:12:34 GMT

  	{
  	  "email": "client@jdc.fr"
  	}


These credentials can now be used to analyze a:
> sentence

    $ curl -u client@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://127.0.0.1:8080/analyze/sentence

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 62
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Sun, 23 Jul 2017 12:39:29 GMT

    {
      "Negatif": 95.52,
      "Neutre": 4.34,
      "Positif": 0.13
    }

> text

    $ curl -u client@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://127.0.0.1:8080/analyze/text

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 87
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Mon, 24 Jul 2017 18:58:02 GMT

    {
      "Negatif": 9.43,
      "Neutre": 39.38,
      "Pertinence": 100.0,
      "Positif": 51.18
    }

> customer service sentence

    $ curl -u client@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"C’est incroyable à quel point vous êtes des incapables ! Que des incompétents, odieux et irrespectueux."}' http://127.0.0.1:8080/analyze/customer

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 78
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Mon, 24 Jul 2017 19:08:36 GMT

    {
      "Agressivite": 99.78,
      "Remboursement": 99.23,
      "Sentiment": -96.22
    }

Using the wrong credentials the request is refused:

    $ curl -u client@jdc.fr:amazon -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://127.0.0.1:8080/analyze/sentence

    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: text/html; charset=utf-8
    Content-Length: 19
    WWW-Authenticate: Basic realm="Authentication Required"
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Sun, 23 Jul 2017 12:11:25 GMT

    Unauthorized Access


Finally, to avoid sending email and password with every request an authentication token can be requested:

    $ curl -u client@jdc.fr:jdc -i -X GET http://127.0.0.1:8080/token

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 174
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Sun, 23 Jul 2017 12:27:18 GMT

    {
      "expires-in": "23h 36min 41s",
      "token": "eyJhbGciOiJIUzI1NiIsImV4cCI6MTUwMDg5NzgzOSwiaWF0IjoxNTAwODEyODM4fQ.eyJpZCI6MX0.eLCg4c8FSIrpOCY-1oI4xl3KjRpTUp8pEW5tjfI17fQ"
    }


And now during the token validity period there is no need to send email and password to authenticate anymore:

    $ curl -u eyJhbGciOiJIUzI1NiIsImV4cCI6MTUwMDg5NzgzOSwiaWF0IjoxNTAwODEyODM4fQ.eyJpZCI6MX0.eLCg4c8FSIrpOCY-1oI4xl3KjRpTUp8pEW5tjfI17fQ:a -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://127.0.0.1:8080/analyze/sentence

    HTTP/1.0 200 OK
    Content-Type: application/json
    Content-Length: 62
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Sun, 23 Jul 2017 12:40:38 GMT

    {
      "Negatif": 95.52,
      "Neutre": 4.34,
      "Positif": 0.13
    }


Once the token expires it cannot be used anymore. Note that in this last example the password is arbitrarily set to `a`, since the password isn't used for token authentication.

[Read more about the Text Sentiment Analyzer.](http://juniordataconsulting.com/aipcloud/text/sentiment/)
