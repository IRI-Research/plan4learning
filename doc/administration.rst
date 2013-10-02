**************
administration
**************

Django et ses modules d'extensions propose de nombreuses commande d'administration. Le but est ici d'en lister les plus utiles pour l'administration de l'application.
L`accès à ces commandes se fait par le script ``manage.py`` situee dans le répertoire ``src`` de l'application.
Il est bien sur indispensable d'activer l'environement virtuel de l'application (cf. :ref:`deployment-virtualenv`) avant de lancer ce script.
Le reste des commandes est documenté soit à l'adresse suivante : https://docs.djangoproject.com/en/1.5/ref/django-admin/, soit directement en invoquant la commande avec l'option ``--help`` i.e.::

    cd src
    python manage.py <commande> --help
     

Commandes à passer lors d'un upgrade de version
===============================================

Lors d'une mise à jour de l'application les commandes suivantes sont systématiquement à lancer :
::

    python manage.py syncdb --migrate
    python manage.py collectstatic

La première permet la mise à jour du schéma de la base de donnée et de lancer les éventuelles migration de données.
La deuxième sert à mettre à jour les resources statiques.


Commande d'administration
=========================

Voici une liste des commandes ser vant à gérer l'import et l'export des notices (``Record``). 

``import_record``
-----------------

.. code-block:: bash

    $ python manage.py import_record --help     
    Usage: manage.py import_record [options] record_url ...

    Import p4l record rdf format
    
    Options:
      -v VERBOSITY, --verbosity=VERBOSITY
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --settings=SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this is not provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --pythonpath=PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --traceback           Print traceback on exception
      -b BATCH_SIZE, --batch-size=BATCH_SIZE
                            number of object to import in bulk operations
      -p, --preserve        preserve existing record
      -i, --index           index while importing
      --version             show program version number and exit
      -h, --help            show this help message and exit


Cette commande importe des notices en format rdf speecifique au projet dans l'application. Elle prend comme argument une liste de chemin vers les fichiers à importer.
Les options suivantes sont disponibles:

  * ``-b BATCH_SIZE`` : contrôle la taille des lots lors de l'import.
    Augmenter la taille des lots peut améliorer les performances lors de l'import mais augmente la consomation mémoire.
    (valeur par défaut: 50)
    
  * ``-p`` : ne tente pas d'effacer les notices lors de l'import.
    L'import d'une notice existante (même identifiant) proviquera une erreur et l'arrêt de l'import
    
  * ``-i`` : met à jour l'index des notices lors de l'import.

Les points suivants sont à noter:

  #. Toute erreur interrompt l'import des notices.
  
  #. L'import d'un fichier n'estr pas transactionnel: i.e. un fichier peut être partiellement importé.
  
  #. À un lot (option `b`) correspond une transaction de base de donnée.
     Donc en cas d'erreur lors d'un l'import, le lot courant complet est annulé.
  
  #. L'indexation n'est pas transactionnelle.
     Donc en cas d'erreur d'import il est possible que certaine notice ait été indexée mais ne se retrouve pas finalement en base.
     Il est à noté que dans ce cas, ces notices apparaîtrons dans la page de liste des notices.


``dump_record``
---------------

.. code-block:: bash

    $ python manage.py dump_record --help
    Usage: manage.py dump_record [options] file_path...

    Export p4l record rdf format
    
    Options:
      -v VERBOSITY, --verbosity=VERBOSITY
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --settings=SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this is not provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --pythonpath=PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --traceback           Print traceback on exception
      -l LIMIT, --limit=LIMIT
                            number of record to export. -1 is all (default)
      -s SKIP, --skip=SKIP  number of record to skip before export. default 0.
      -b BATCH, --batch=BATCH
                            query batch default 100.
      -j, --bzip2           bz2 compress
      -z, --gzip            gzip compress
      --version             show program version number and exit
      -h, --help            show this help message and exit
    

Cette commande exporte des notices en format rdf.  Elle prend comme argument le chemin d'un fichier. Si le fichier existe, celui-ci sera écrasé sans aucune confirmation.
Lors de l'export les notices sont classées par leur identifiant (tri syntaxique ascendant). 

Les options suivantes sont disponibles:

  * ``-b BATCH`` : tailles des lots de notices par requête de base de données. La valeur de ce paramêtre dépend des performances et capacité du serveur de base de données et de la machine d'export.
  * ``-l LIMIT`` : nombre maximum de notices à exporter. -1 (le défaut) exporte toute les notices.
  * ``-s SKIP`` : nombre de notice à ignorer avant de commencer l'export. O par défaut. Rappel: Lors de l'export les notices sont classées par leur identifiant (tri syntaxique ascendant).
    Avec l'option ``-l``, cette option permet l'export des notices en lots.
  * ``-j``, ``-z`` : permet la compression à la volée des données. La compression se fait au fur et à mesure de l'export.
  
Les points suivants sont à noter:

  #. Toute erreur interompt immédiatement l'export.
  #. En cas d'erreur, l'export est immédiatement interrompu et le fichier produit ne sera pas valide.
     En particulier, dans le cas où une option de compression a été activé, l'archive partielle crée peut s'avérer illisible.


``rebuild_index``
-----------------

.. code-block:: bash

    $ python manage.py rebuild_index  --help
    Usage: manage.py rebuild_index [options] 
    
    Completely rebuilds the search index by removing the old data and then updating.
    
    Options:
      -v VERBOSITY, --verbosity=VERBOSITY
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --settings=SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --pythonpath=PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --traceback           Print traceback on exception
      -a AGE, --age=AGE     Number of hours back to consider objects new.
      -s START_DATE, --start=START_DATE
                            The start date for indexing within. Can be any
                            dateutil-parsable string, recommended to be YYYY-MM-
                            DDTHH:MM:SS.
      -e END_DATE, --end=END_DATE
                            The end date for indexing within. Can be any dateutil-
                            parsable string, recommended to be YYYY-MM-
                            DDTHH:MM:SS.
      -b BATCHSIZE, --batch-size=BATCHSIZE
                            Number of items to index at once.
      -r, --remove          Remove objects from the index that are no longer
                            present in the database.
      -u USING, --using=USING
                            Update only the named backend (can be used multiple
                            times). By default all backends will be updated.
      -k WORKERS, --workers=WORKERS
                            Allows for the use multiple workers to parallelize
                            indexing. Requires multiprocessing.
      --noinput             If provided, no prompts will be issued to the user and
                            the data will be wiped out.
      --version             show program's version number and exit
      -h, --help            show this help message and exit

Commande utilisée pour reconstruire l'index Elasticsearch. L'age d'une notice est calculé à partir de sa date de mise à jour.
Cette date est la date d'import de la notice si elle n'a pas été mise à jour dans l'application, et sa date de création si elle a été créée dans l'application. 
Cette commande est fournie par le module Django ``Haystack``. Sa documentation se trouve à l'adresse suivante : http://django-haystack.readthedocs.org/en/v2.1.0/management_commands.html

``update_index``
----------------

.. code-block:: bash

    $ python manage.py update_index  --help
    Usage: manage.py update_index [options] <label label ...>
    
    Freshens the index for the given app(s).
    
    Options:
      -v VERBOSITY, --verbosity=VERBOSITY
                            Verbosity level; 0=minimal output, 1=normal output,
                            2=verbose output, 3=very verbose output
      --settings=SETTINGS   The Python path to a settings module, e.g.
                            "myproject.settings.main". If this isn't provided, the
                            DJANGO_SETTINGS_MODULE environment variable will be
                            used.
      --pythonpath=PYTHONPATH
                            A directory to add to the Python path, e.g.
                            "/home/djangoprojects/myproject".
      --traceback           Print traceback on exception
      -a AGE, --age=AGE     Number of hours back to consider objects new.
      -s START_DATE, --start=START_DATE
                            The start date for indexing within. Can be any
                            dateutil-parsable string, recommended to be YYYY-MM-
                            DDTHH:MM:SS.
      -e END_DATE, --end=END_DATE
                            The end date for indexing within. Can be any dateutil-
                            parsable string, recommended to be YYYY-MM-
                            DDTHH:MM:SS.
      -b BATCHSIZE, --batch-size=BATCHSIZE
                            Number of items to index at once.
      -r, --remove          Remove objects from the index that are no longer
                            present in the database.
      -u USING, --using=USING
                            Update only the named backend (can be used multiple
                            times). By default all backends will be updated.
      -k WORKERS, --workers=WORKERS
                            Allows for the use multiple workers to parallelize
                            indexing. Requires multiprocessing.
      --version             show program's version number and exit
      -h, --help            show this help message and exit

Commande utilisée pour mettre à jour l'index Elasticsearch. L'age d'une notice est calculé à partir de sa date de mise à jour.
Cette date est la date d'import de la notice si elle n'a pas été mise à jour dans l'application, et sa date de création si elle a été créée dans l'application. 
Cette commande est fournie par le module Django ``Haystack``. Sa documentation se trouve à l'adresse suivante : http://django-haystack.readthedocs.org/en/v2.1.0/management_commands.html


console d'administration / gestion des utilisateurs
===================================================

Le back-office offre une console d'administration donnant accès en particulier à la gestion des utilisateurs.
On y accède par le lien ``admin`` dans l'en-tête des pages si on est connecté en tant qu'administrateur ou bien en allant directement à l'adresse ``<racine du site>/p4l/admin/``.


L'administration des utilisateurs se fait à l'adresse suivante : ``<racine du site>/p4l/admin/p4l/user/``.

L'administration des groupes d'utilisateurs se fait à l'adresse suivante: ``<racine du site>/p4l/admin/auth/group/``.


L'interface de gestion est assez classique et ne présente pas de difficulté particulière.


Pour qu'un utilisateur puisse créer et mettre à jour des enregistrements (``Records``), il faut qu'il ait les permissions d'ajout, de modification et d'effacement de tous les objets de l'application ``p4l``.
Le champ ``Permission de l'utilisateur`` doit donc comporter toutes les entrées de la forme ``p4l | <object> | <permission>``.


Pour faciliter la gestion de ces permissions, le plus simple est de créer un groupe ``utilisateurs``. On affectera à ce groupe toutes les permissions sur les objects de l'application ``p4l``.
il suffira ensuite de mettre les utilisateurs dans ce groupe (champ ``Groupes`` dans l'interface d'édition des utilisateurs). L'utilisateur héritera alors des parmissions du groupe.
 
