***********
Déploiement
***********

La documentation de déploiement suivante est sur la base d'une Debian 7.0 (Wheezy).


options de déployement
======================

De nombreuses options de déploiement existe. Les plus populaires sont décrite sur le site Django à l'adresse suivante : https://docs.djangoproject.com/en/1.5/howto/deployment/.

Nous décrivons ici l'installation de l'option apache + modwsgi : https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/


installation des prérequis
==========================

Liste des prérequis
- python 2.7
- apache
- modwsgi
- postgresql
- elasticsearch
- build tools

Le reste des dépendances est fourni dans les sources.
Toute les commandes ci dessous doivent se faire entant que ``root``, typiquement en prefixant toute les commandes avec ``sudo``.


Python 2.7
----------

C'est la version par défaut de la distribution debian 7. Si python n'est pas déjà installé::

    apt-get install python 


Apache et mod-wsgi
------------------

On utilise les versions distribuée avec la debian 7.
::

    apt-get install apache2
    apt-get install libapache2-mod-wsgi


Postgresql
----------

La aussi nous utilisons la version distribuée avec la debian 7, c'est à dire la 9.1.
::

    apt-get install postgresql


Elasticsearch
-------------

Elasticsearh a Java pour prérequis. Cette étape n'est pas décrite ici.
Télécharger le paquet debian (deb) à l'adresse suivante : https://download.elasticsearch.org/elasticsearch/elasticsearch/elasticsearch-0.90.5.deb .
::

    dpkg -i elasticsearch-0.90.5.deb


Build tools
----------- 

La création de l'environement virtuel nécessite l'installation des outils de base de compilation. ::

    apt-get install build-essential


Etapes de déploiement
=====================

L'ensemble des commandes suivantes ne nécessite pas d'être exécutées comme utilisateur prilivégié.

Organisation des sources / commandes Django
-------------------------------------------

Les fichiers du projets peuvent être organisés en 4 groupes correspondant à des sous-répertoires 
  - ``src`` : contient l'ensemble du code, template et resources statiques
  - ``virtualenv`` : script de création de l'environement virtuel et dépendances python
  - ``web`` : répertoire de publication des resources statiques 
  - ``run`` : répertoire contenant les logs de l'application

Django fournit un utilitaire en ligne de commande permettant l'execution de tâche d'administration. La documentation se trouve à l'adresse suivante : https://docs.djangoproject.com/en/1.5/ref/django-admin/ .
cet


Virtualenv
----------

L'environement d'execution python est isolé de l'environement du système par l'utilisation d'un environement virtuel ou ``virtualenv``.
Une documentation d'utilisation se trouve à l'adresse suivante : http://www.virtualenv.org/en/latest/ .
Il faut en particulier noter la procédure d'activation de l'environement virtuel. Dans la suite, les commandes d'administration django devront être lancées après cette activation. 

Un script permettant la création de l'environement virtuel et de l'installation de toutes les dépendances "python" est fourni dans le répertoire ``virtualenv``.

.. code-block :: sh

    cd virtualenv/web/
    python create_python_env.py
    python project-boot.py <chemin de l'environement virtuel>


Au cours de l'exploitation du serveur et en particulier lors des mise à jour du système d'exploitation, il faut être attentif aux mise à jour de la distribution python ayant servie à la création de l'environement virtuel.
Si la version de python est mise à jour, l'environement virtuel devra lui aussi être mis à jour.

Configuration
-------------

La configuration du système se fait dans le fichier ``src/config.py``. Ce fichier doit être créé à partir du fichier ``src/config.py.tmpl``.
La plupart des configurations sont soit documentées directement dans le fichier, soit documentés à l'adresse suivante : https://docs.djangoproject.com/en/1.5/ref/settings/


Création de la base
-------------------

La base est crée en plusieurs étapes. D'abord il faut créer la base de donnée vide. On pourra par exemple utiliser la commande suivante.

.. code-block :: postgresql

    CREATE DATABASE p4l
      WITH ENCODING='UTF8'
           OWNER=iri
           TEMPLATE=template0
           LC_COLLATE='en_US.UTF-8'
           LC_CTYPE='en_US.UTF-8'
           CONNECTION LIMIT=-1;

Tout autre méthode est correcte. Attention cependant d'utiliser un encoding "utf-8". 

Le schema de la base est créé avec la commande django suivante (penser à préalablement activer l'environement virtuel)::

    python manage.py syncdb --migrate

Enfin on crée un "super" utilisateur pouvant accéder à l'admininistration du site.:: 

    python manage.py createsuperuser


deployement des resources statiques
-----------------------------------

Le déploiement des resources statiques du site se font à l'aide de la commande suivante:
::

    python manage.py collecststatic


configuration web
-----------------

La configuration web (apache) est documentée à l'adresse suivante : https://docs.djangoproject.com/en/1.5/howto/deployment/wsgi/modwsgi/ .
Comme cette configuration dépend de l'environement propre au serveur, nous n'en détaillerons pas les étapes. 

Cependant, voici une liste des points notables:

- Bien faire la séparation entre la partie dynamique servie par modwsgi, et la partie statique servie par apache.
- le système utilise un environement virtuel. Pensez bien à renseigner le chemin du répertoire ``site-packages`` dans la directive ``WSGIPythonPath``
- L'utilisation de ``mod_wsgi`` en mode démon (``daemon mode``) est fortement recommandée.
  