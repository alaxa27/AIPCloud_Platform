#!/bin/bash

echo '================= 1 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/sentence

echo '================= 2 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://0.0.0.0:80/analyze/text

echo '================= 3 ==================='

curl -u text@jdc.fr:jdc -i -X GET http://0.0.0.0:80/analyze/dialogue

echo '================= 4 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/customer

echo '================= 5 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://0.0.0.0:80/analyze/text

echo '================= 6 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/extraction

echo '================= 7 ==================='

curl -u text@jdc.fr:jdc -i -X GET http://0.0.0.0:80/analyze/dialogue

echo '================= 8 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"sentence":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/sentence

echo '================= 9 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Votre service est très mauvais, aucune écoute, aucune considération. Bref, encore un SAV bien inutile."}' http://0.0.0.0:80/analyze/customer

echo '================= 10 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://0.0.0.0:80/analyze/text

echo '================= 11 ==================='

curl -u text@jdc.fr:jdc -i -X POST -H "Content-Type: application/json" -d '{"text":"Ce sont mille chemins différents qui nous ont conduits ici aujourd’hui, vous et moi, animés par le même désir de servir. Et même si ce désir n’a pas le même visage, pas la même forme, même s’il n’emporte pas les mêmes conséquences, nous en connaissons vous et moi la source : le simple amour de la patrie.[...]Notre premier devoir est tout à la fois de retrouver le sens et la force d’un projet ambitieux de transformation de notre pays et de rester arrimés au réel. De ne rien céder au principe de plaisir, aux mots faciles, aux illusions pour regarder en face la réalité de notre pays sous toutes ses formes. Ce mandat du peuple, donc, quel est-il?"}' http://0.0.0.0:80/analyze/extraction
