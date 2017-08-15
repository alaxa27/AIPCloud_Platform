
## Introduction

Ce document montre comment utiliser cette API pour bénéficier de la puissance des services d'[AIPCloud.](http://juniordataconsulting.com/aipcloud/).


## Utilisation

### Comptes d'utilisateurs:

Cinq comptes d'utilisateurs sont déjà créés dans la base de données implémentée sur Google Cloud SQL:
Deux administrateurs: 'admin@jdc.fr' et 'text@jdc.fr', qui ont accés à tous les points de l'API.
Un compte test ('test@jdc.fr') qui a le droit à 9 requêtes avec la même adresse IP.
Un compte ayant seulement l'accés aux méthodes d'analyse de texte ('client@jdc.fr') et un autre ayant seulement l'accés à la méthode d'analyse d'image ('image@jdc.fr').

    +----+---------------+---------------+-------+-------------+------+
    | id | email         | password_hash | admin | queries_max | test |
    +----+---------------+---------------+-------+-------------+------+
    |  1 | text@jdc.fr   | jdc           |     1 |          -1 |    0 |
    |  2 | image@jdc.fr  | jdc           |     0 |          30 |    0 |
    |  3 | admin@jdc.fr  | jdc           |     1 |          -1 |    0 |
    |  4 | client@jdc.fr | jdc           |     0 |          20 |    0 |
    |  5 | test@jdc.fr   | jdc           |     0 |           9 |    1 |
    +----+---------------+---------------+-------+-------------+------+

Le champ queries_max contient le nombre maximal de requêtes que l'utilisateur peut effectuer. Il est à -1 pour les utilisateurs ayant le droit à un nombre illimité de requêtes.


### Exemples de requêtes:

En utilisant son email et mot de passe, et en fonction de ses droits d'accés, L'utilisateur peut faire appel au différents points de l'API pour analyser un texte ou une image.

#### Analyse de phrase:

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/sentence

    HTTP/1.0 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Content-Length: 62
    Server: Werkzeug/0.12.2 Python/3.5.3
    Date: Sat, 12 Aug 2017 20:54:28 GMT

    {
      "negatif": 95.52,
      "neutre": 4.34,
      "positif": 0.13
    }

#### Analyse de texte:

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://0.0.0.0:80/analyze/text

    HTTP/1.0 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Content-Length: 280
    Server: Werkzeug/0.12.2 Python/3.5.3
    Date: Sat, 12 Aug 2017 20:41:00 GMT

    {
      "lerp": 0.4175,
      "negativity": 9.43,
      "neutrality": 39.38,
      "positivity": 51.18,
      "relevance": 74.74,
      "slope": -0.2857,
      "summary": "Le texte est plut\u00f4t neutre positif. Le texte est neutre au d\u00e9but et n\u00e9gatif vers la fin.",
      "variance": 0.0729
    }

#### Analyse du texte pour le Service Client:

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/customer

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

#### Extraction des mots-clés dans un texte:

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/extraction

    HTTP/1.0 200 OK
    Content-Type: application/json
    Access-Control-Allow-Origin: *
    Content-Length: 407
    Server: Werkzeug/0.12.2 Python/3.5.3
    Date: Sat, 12 Aug 2017 22:39:27 GMT

    [
      {
        "keyword": "mauvais",
        "score": 0.1684
      },
      {
        "keyword": "SAV",
        "score": 0.1684
      },
      {
        "keyword": "\u00e9coute",
        "score": 0.1599
      },
      {
        "keyword": "Bref",
        "score": 0.1599
      },
      {
        "keyword": "consid\u00e9ration",
        "score": 0.1573
      },
      {
        "keyword": "service",
        "score": 0.093
      },
      {
        "keyword": "inutile",
        "score": 0.093
      }
    ]

#### Analyse de dialogue:

    $ curl -u text@jdc.fr:jdc -i -X GET http://0.0.0.0:80/analyze/dialogue


#### Traitement d'une image:

    $ curl -u image@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"image_url": "https://media1.britannica.com/eb-media/95/156695-131-FF89C9FA.jpg" }' http://0.0.0.0:80/analyze/image


En utilsant un email/mot de passe érroné(s), l'accés au point demandé est refusé:

    $ curl -u text@jdc.fr:amazon -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://127.0.0.1:8080/analyze/sentence

    HTTP/1.0 401 UNAUTHORIZED
    Content-Type: text/html; charset=utf-8
    Content-Length: 19
    WWW-Authenticate: Basic realm="Authentication Required"
    Server: Werkzeug/0.12.2 Python/2.7.12
    Date: Sun, 23 Jul 2017 12:11:25 GMT

    Unauthorized Access


Quand un utilisateur essaye d'appeler une méthode à laquelle il n'a pas accés, une réponse 403 FORBIDDEN est renvoyée:

    $ curl -u image@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentee":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/sentence

    HTTP/1.0 403 FORBIDDEN
    Content-Type: text/html
    Content-Length: 234
    Access-Control-Allow-Origin: *
    Server: Werkzeug/0.12.2 Python/3.5.3
    Date: Sat, 12 Aug 2017 22:46:45 GMT

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>403 Forbidden</title>
    <h1>Forbidden</h1>
    <p>You don't have the permission to access the requested resource. It is either read-protected or not readable by the server.</p>


Le format JSON de chaque méthode doit être respecté dans le message des requêtes envoyées. Par exemple, l'utilisation du mot 'sntence' au lieu de 'sentence' lors de l'appel au point '/analyze/sentence' va générer une réponse 400 BAD REQUEST:

    $ curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sntence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/sentence

    HTTP/1.0 400 BAD REQUEST
    Content-Type: text/html
    Content-Length: 192
    Access-Control-Allow-Origin: *
    Server: Werkzeug/0.12.2 Python/3.5.3
    Date: Sat, 12 Aug 2017 22:48:32 GMT

    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 3.2 Final//EN">
    <title>400 Bad Request</title>
    <h1>Bad Request</h1>
    <p>The browser (or proxy) sent a request that this server could not understand.</p>


[Savoir plus sur Junior Data Consulting.](http://juniordataconsulting.com/)
