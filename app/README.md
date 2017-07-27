
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

Using his credentials, the user can analyze a:

> sentence

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://127.0.0.1:8080/analyze/sentence

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

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://127.0.0.1:8080/analyze/text

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

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"C’est incroyable à quel point vous êtes des incapables ! Que des incompétents, odieux et irrespectueux."}' http://127.0.0.1:8080/analyze/customer

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

> image:

    curl -u image@jdc.fr:junior -i -X POST -H "Content-Type: application/json" -d '{"image-url": "https://media1.britannica.com/eb-media/95/156695-131-FF89C9FA.jpg" }' http://127.0.0.1:8080/image

Using the wrong credentials the request is refused:

    $ curl -u text@jdc.fr:amazon -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://127.0.0.1:8080/analyze/sentence

    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: text/html; charset=utf-8
    Content-Length: 19
    WWW-Authenticate: Basic realm="Authentication Required"
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Sun, 23 Jul 2017 12:11:25 GMT

    Unauthorized Access


[Read more about the Text Sentiment Analyzer.](http://juniordataconsulting.com/aipcloud/text/sentiment/)
