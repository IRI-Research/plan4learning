:tocdepth: 4
:tocmaxdepth: 3

*********
Évolution
*********

Internationalisation
====================

Le système d'internationalisation (i18n) utilise le mécanisme fourni par Django.

Il est documenté aux adresses suivantes :
  * https://docs.djangoproject.com/en/1.5/topics/i18n/ et
  * https://docs.djangoproject.com/en/1.5/topics/i18n/translation/

Ce mécanisme est basé sur l'utilitaire `gettext <http://www.gnu.org/software/gettext/manual/gettext.html#Concepts>`_.

En particulier, dans l'arborescence des sources de l'application, les fichiers ``src/p4l/locale/*/LC_MESSAGES/django.[po,mo]`` sont les fichiers de resources de langues.
Les fichier éditable sont les fichiesr ``.po``.

Deux commandes d'administration sont fournies par Django pour gérer les fichiers de resources de traduction:


  * ``makemessages`` : https://docs.djangoproject.com/en/1.5/ref/django-admin/#django-admin-makemessages.
    C'est la commande permettant la création et la mis ā jour des fichiers ``.po``.
    Cette commande extrait des fichier sources de l'application les chaîne de caractères à traduire et les places dans les fichier ``.po``.
    Typiquement, on ne lancera cette commande que si de nouvelle chaînes à trduire sont ajoutées dans l'application.
     
  * ``compilemessages`` : Compile les fichiers ``.po`` contitués par la commande précédente afin que les traduction soit prise en compte.
    cette commande produit les fichier ``.mo``. 

Ces commandes peuvent être lancées de plusieurs façon. Le plus simple est de les lancer depuis le répertoire ``src/p4l`` et avec l'utilitaire ``django-admin.py``.
Ce dernier est installé lors de l'installation de Django.
Dans le cas de l'utilisation d'un environement virtuel, il se trouve dans le répertoire ``bin``, et de fait dans le "PATH" lorsque l'environement virtuel est activé.
La suite des commandes pour 

.. code-block:: bash

    $ cd src/p4l
    $ django-admin.py makemessages -a
    <edition des fichiers .po>
    $ django-admin.py compilemessages 


modification des champs
=======================

La modification de la liste des champs traitée par le back-office nécessite des changements a plusieurs niveaux.
Voici une liste des points à modifier.

  * Dans la :ref:`configuration <evol-config>` (``settings.py``) : les propriétés ``SPARQL_REF_QUERIES`` et ``RDF_SCHEMES``
  * :ref:`Évolution du schéma <evol-schema>` de la base de données
  * :ref:`Modification du parser <evol-parser>` pour l'import.
  * :ref:`Modification du sérialiseur <evol-serializer>` pour l'export 
    + modification de la constante ``p4l.mapping.constants.GRAPH_NAMESPACES``
  * :ref:`Modification du serialiseur rest <evol-rest-serializer>`.
  * 
  * modification de l'écran d'affichage du :ref:`détail <evol-detail>` d'une notice.
  * modification de l'écran d':ref:`édition <evol-edition>` d'une notice.
  
La description de ces modifications se base sur la condition que le type de champ ajouté est le même qu'un champ déjà existant.
La création d'un nouveau type de champ est hors du scope de cette documentation, 
mais l'examen attentif des points suivants pourront être un point de dépard pour le développement. 


.. _evol-config:

Modification de la configuration
--------------------------------

Cette modification concerne seulement les champs dont la(es) valeur(s) est(sont) contrôlé(s) par un référentiel.
Les deux propriétés concernées sont ``SPARQL_REF_QUERIES`` et ``RDF_SCHEMES``. ce sont deux dictionnaires ayant les mêmes valeurs de clef.
Chaque clef correspond à un référentiel.

.. _evol-config-SPARQL-REF-QUERIES:

``SPARQL_REF_QUERIES``
^^^^^^^^^^^^^^^^^^^^^^

les valeurs de ce dictionnaire sont elle même un dictionnaire qui contient les requêtes SPARQL d'exploration des reeférentiels.
les clés suivantes sont à renseigner:

    * ``url`` : url du endpoint pour ce référentiel. On n'y mettra ``SPARQL_QUERY_ENDPOINT`` la plupart du temps.
    * ``filter`` : requête filtrant les entrées du référentiel selon une partie de terme.
      Cette requète est utiliser pour faire de l'autocomplétion.
    * ``root`` : Requête qui donne les racines des référentiels en arbre et l'ensemble des termes pour les autres
    * ``childs`` : Requ6ete donnant les enfants d'un noeud particulier pour les référentiel "arbre".
      Cette clé n'a pas besoin d'être renseigné pour les autres.
    * ``child-count`` : Nombre denfant pour 1 noeud d'un référentiel arbre. N'a pas besoin d'être renseignee pour les autres.
 
 
``RDF_SCHEMES``
^^^^^^^^^^^^^^^

Ce dictionnaire donne les uri des ``scheme`` des référentiels. 


.. _evol-schema:

Modification du schema de la base de donnée
-------------------------------------------

Modification du modèle Django
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

La première étape consiste à modifier le modèle Django.
La documentation Django sur les modèle se trouve à l'url suivante https://docs.djangoproject.com/en/1.5/topics/db/models/

le modèle du projet se trouve dans ``src/p4l/models`` et en particulier la définition d'une notice (objet ``Record``) dans ``src/p4l/models/data.py``.
ce fichier contient toute les définitions des champs actuellement utilisés et pourra servir de base d'exemple pour les évolutions envisagées.
 
Attention, contrairement à la documentation Django, il ne faut pas appliquer pas la commande ``syncdb`` pour mettre à jour le schema de la base de donnée.


Utilisation de South
^^^^^^^^^^^^^^^^^^^^

Pour assurer la gestion des migration de modèle de donnée sur des base en production nous utilison le module Django South : http://south.aeracode.org/.

L'utilisation de ce module passe par la création de migrations.

En particulier nous suivons l'exemple donné à l'url suivante:
http://south.readthedocs.org/en/latest/tutorial/part1.html#changing-the-model

Les commandes ajoutées par South sont documentées à l'adresse suivante :
http://south.readthedocs.org/en/latest/commands.html


.. _evol-parser:

Modification du parser pour l'import
------------------------------------

L'import des notice au format rdf se fait avec la commande ``import_record`` (cf :ref:`admin-import-record`).
Cette commande sépare le fichier rdf en sous graphes rdf, un par objet ``Record``.
Ces graphes sont alors pris en présent à un parser qui se charge de leur transformation en objets ``Record``.

Le parser est définit dans le fichier ``src/p4l/mapping/parsers.py``, plus particulièrement dans la classe ``RecordParser``.
La définition des champs et des sous-objets se fait dans la méthode ``build_record``.

Le parsing des données du graphe se fait en fait à l'aide de deux méthodes principales défines sur la classe ``RecordParser``:

  * ``extract_single_value_form_graph`` : permet d'extraire une valeur simple du graphe. elle est utilisée pour les champs simples monovalués.
  * ``extract_multiple_values_from_graph`` : Gère l'ajout d'objet à un gestionnaire d'objets liés ("related object manager" : https://docs.djangoproject.com/en/1.5/ref/models/relations/).
    Les données nécessaire pour la création des objets sont extraites du graphe. 


Points à noter:

  #. les champs simples doivent être positionnés avant la sauvegarde de la notice (appel à la méthode save du modèle ``Record``).
     Par contre les champs complexes (sous objets, champs multivalués,...) doivent être traités après l'appel à ``.save()``
  #. Lorsqu'une notice est mise à jour, l'objet ``Record`` et ces dépendances sont effacés et recréés
  #. Sauf pour les champs gérés par un référentiel, ll y a une relation d'aggregation entre l'objet ``Record`` et ses sous objets.
     Dans le cas des champs complexes avec référentiel, c'est une relation multiple (many to many).
     Dans ce cas lors de l'effacement d'un object ``Record``, seul les entrées dans les tables de liason sont effacées. Les entrée dans les tables de référentiel se sont pas affectées.
  #. Sur les champs avec référentiel, il n'y a pas de validation. Les entrées dans les tables de référentiels sont crées à la demande, sans validation par rapport au repository Sésame.      
  #. L'ensemble de la création (ou de l'effacement) d'un objet ``Record`` et de ces dépendances est fait dans une transaction.
 

.. _evol-serializer:

Modification du serialiseur pour l'export
-----------------------------------------

l'export des notices au format rdf se fait avec la commande ``dump_record`` (cf :ref:`admin-dump-record`).
Chaque objet ``Record`` concerné par l'export est transformé en graphe rdf par un serialiseur. Le graphe rdf est ensuite sérialisé en xml.

Le serializer est défini dans le fichier ``src/p4l/mapping/__init__.py`` et fait appel à des resources se trouvant dans ``src/p4l/mapping/serializers.py``. 

Les interfaces définies dans ce modules sont inspirées de celle proposée par le module ``Rest framework`` que nous utilisons par ailleurs (cf. :ref:`evol-rest-serializer`).
En particulier on pourra lire la documentation des ``serializer``: http://django-rest-framework.org/api-guide/serializers.html .


.. _evol-rest-serializer:

Modification du serialiseur REST
--------------------------------

Une partie de l'application (l'édition des notices) dépend d'interface REST proposant du JSON.
Pour cela nous utilisons le module "Django REST Framework".
La documentation de ce module se trouve à l'adresse suivante : http://django-rest-framework.org/ .

La classe à modifier est ``RecordSerializer`` qui se trouve dans le fichier ``src/p4l/api/serializers.py``.
La documentation sur les ``serializer`` du Rest Framework est à l'adresses suivante : http://django-rest-framework.org/tutorial/1-serialization.html.
La documentation de l'api des serializer se trouve aux url suivantes : http://django-rest-framework.org/api-guide/serializers.html, http://django-rest-framework.org/api-guide/fields.html, http://django-rest-framework.org/api-guide/relations.html.

Nous utilisons les mécanismes standarts de sérialisation du ``REST Framework``. Nous avons juste adaptee les points suivants:

  * Pour les champs contrôlés par un référentiel, le mécanisme standart du ``REST Framework`` est d'accepter les valeurs que si elle sont déjà présente dans la base.
    Nous avons changé ce comportement pour accepter toute les valeurs et de créer les nouvelles à la demande. Ceci a été fait pour simplifier la gestion des référentiels et la centraliser en amont du back office.
    Ceci est implémenté dans la classe ``p4l.api.serializers.ThesaurusSerializer``.
  * Pour les champs multiples et les sous-objets, l'ID de l'objet en base n'est pas sérialisée. Ceci se trouve dans la classe ``p4l.api.serializers.P4lModelSerializer``.
  * Lors d'un update, les sous-objets sont effacés puis recréés. cela a pour conséquence qu'un update partiel n'est pas possible. A chaque requête de mise à jour, l'ensemble de l'objet ``Record`` et de tous ses sous-objets doit être envoyé à l'API REST d'update. 
  * Une modification du seerializer REST n'est nécessaire que si le nouveau champ est contrôlé par un référentiel (bien sur si ce nouveau champs est d'un type déjà supporté par l'application).


.. _evol-ref-labels:

Modification de la récupération des labels des champs contrôlés par référentiel
-------------------------------------------------------------------------------

L'application ne gère pas les labels des valeurs des champs contrôlés par référentiel.
Pour l'affichage dews notices il est donc nécessaire de préalablement requêter tous ces labels.

Ce requêtage se fait dans la méthode ``p4l.views.fill_label_for_model`` (dans le fichier ``src/p4l/views.py``).
Cette méthode retourne un dictionnaire où les clefs sont les uri des termes, et les valeurs les labels correspondants dans la langue demandées.

Bien sur aucune modification est nécessaire si le champ ajouté ou modifié n'introduit pas un nouveau référentiel.


.. _evol-detail:

Modification de l'écran de détail
---------------------------------

L'écran de détail d'une notice (c.f. :ref:`interface-detail`) utilise le couple classique vue/template Django.

La documentation Django sur les vues est à l'url suivante : https://docs.djangoproject.com/en/1.5/topics/class-based-views/.
La documentation Django sur les template est ici : https://docs.djangoproject.com/en/1.5/topics/templates/.

La vue d'affichage du détail d'une notice est générée par la classe suivante : ``p4l.views.RecordDetailView`` (dans le fichier ``src/p4l/views.py``).
Le template d'affichage du détail est le suivant : ``src/templates/p4l/record_view.html``.

Normalement seul le template a besoin d'être modifié. Les champs déjà présents pourront être pris comme exemple pour introduire le nouveau champ.


.. _evol-edition:

Modification de l'écran d'édition
---------------------------------

Comme pour l'écran de détail, l'écran d'édition d'une notice (c.f. :ref:`interface-edit`) utilise un couple vue/template Django. (c.f. :ref:`evol-detail` pour les url de documentation Django)
Par contre les fonctionnalités de cette page sont nettement plus complexes dans leur mise en oeuvre.

La vue d'édition d'une notice est générée par la classe suivante : ``p4l.views.RecordEditView`` (dans le fichier ``src/p4l/views.py``).
Le template d'affichage du détail est le suivant : ``src/templates/p4l/record_update_form.html``.
Par ailleurs la vue d'édition est en fait une véritable application web ("webapp") basée sur la librairie Angularjs (http://angularjs.org/).
Elle est implémentée dans le fichier ``src/p4l/static/p4l/js/p4l.js``.
La page fait aussi appel à des resources (des templates) dans le reepertoire ``src/p4l/static/p4l/template``.

Normalement, seul les fichiers template Django ``src/templates/p4l/record_update_form.html`` ou bien angular ``src/p4l/static/p4l/templates`` auront besoin d'être modifiés pour ajouter ou modifier un champs d'un type déjà existant.

Lors du chargement de la page d'édition, les données de la notice sont chargée à partir de la couche d'API REST sous forme d'objets sérialisés en JSON.
Ces données viennent remplir le "modèle" de l'appli web.
Ce modèle est ensuite exploité dans une série de directives Angularjs (c.f. http://docs.angularjs.org/guide/directive) qui permettent l'éditions des différents champs et sous-objets de la notice.
Lors de la sauvegarde, ce modèle est sérialisé en JSON et soumis par requête http à la couche d'API REST de l'application.
 
Le formulaire d'édition utilise 4 types d'éléments pour gérer les différents champs et sous-objets de l'objet notice.

  * Pour les champs simples: des contôles html (``input``, ``textarea``...) liés au modèle dans un formulaire Angularjs (http://docs.angularjs.org/guide/forms)
  * Pour les champs simples liés à un référentiel : la directive :ref:`simple-sem-uri <evol-edition-simple-sem-uri>`.
  * Pour les champs complexes liés à un référentiel : la directive :ref:`add-sem-uri <evol-edition-add-sem-uri>`.
  * Pour les champs complexes autres (sous-objets) : la directive :ref:`object-list <evol-edition-object-list>`.
 
Les contrôles html et l'usage qu'Angularjs en fait sont documentés dans la référence d'API : http://docs.angularjs.org/api/.
Le reste des directives est documenté ci-après et on pourra se basé sur les champs existant pour aveoir des exemple d'utilisation.

.. _evol-edition-simple-sem-uri:

Directive ``simple-sem-uri``
^^^^^^^^^^^^^^^^^^^^^^^^^^^^

  * ``val`` : le champ du modèle lié à cette directive.
  * ``listname`` : Une des clefs du paramètre de configuration ``SPARQL_REF_QUERIES`` (c.f. :ref:`evol-config-SPARQL-REF-QUERIES`)
  * ``placeholder`` : texte d'aide du champs de saisie pour le référentiel.


.. _evol-edition-add-sem-uri:

Directive ``add-sem-uri``
^^^^^^^^^^^^^^^^^^^^^^^^^

  * ``list`` : le champ du modèle lié à cette directive, ce doit être une liste (champ multivalué).
  * ``listname`` : Une des clefs du paramètre de configuration ``SPARQL_REF_QUERIES`` (c.f. :ref:`evol-config-SPARQL-REF-QUERIES`)
  * ``placeholder`` : texte d'aide du champs de saisie pour le référentiel.


.. _evol-edition-object-list:

Directive ``object-list``
^^^^^^^^^^^^^^^^^^^^^^^^^

  * ``form-template`` : nom d'un template pour l'édition des sous-objets.
  * ``disp-template`` : nom d'un template pour gérer l'affichage des sous-objets. Ce paramêtre est optionnel en mode table.
    Si ce paramêtre est vide, un template est automatiquement généré.
  * ``object-list`` : le champ du modèle lié à cette directive, ce doit être une liste (champ multivalué).
  * ``object-fields`` : Liste des champs du sous-objet à afficher en mode table.
  * ``table`` : Affiche les sous objets en table ou pas.
  * ``size-fields`` : Largeur des colonnes pour le mode table. L'ordre des colonnes est le même que pour ``object-fields``.
    L'unité est une colonne définie par le système de grille Bootstrap : http://getbootstrap.com/css/#grid.
  * ``label-fields`` : Label des colonnes pour le mode table. Ces labels sont traduits. L'ordre des colonnes est le même que pour ``object-fields``.

Les templates définis par les paramêtres ``form-template`` et ``disp-template`` se trouvent dans le répertoire ``src/p4l/static/p4l/templates``.
Ce sont des templates Angularjs (c.f. http://docs.angularjs.org/guide/dev_guide.templates).
Pour les template ``form-template``, l'objet édité est dans la variable ``editedObj``.
Pour les template ``disp-template``, l'objet édité est dans la variable ``obj``. 
Les templates existant donneront des exemples d'utilisation et pourront servir de base pour l'ajout d'un nouveau champ.
Attention, ce sont des ressources statiques pour l'application.
Si ils sont modifiés, la commande ``collectstatic`` doit être lancée afin qu'ils soient correctement déployés et pris en compte par Angular.

