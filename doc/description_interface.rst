**************************
Description de l'interface
**************************

L'application est constituée de 4 écrans.
Ces écrans sont des pages html5.
Ces pages utilisent le framework css Bootstrap (http://getbootstrap.com/).


Connexion
=========

.. image:: _static/p4l_connect.png
    :width: 600pt

Toutes les pages de l'application sont protégées par un système de login/mot de passe.
Ce dialogue de connexion s'affiche lorsque l'utilisateur essaye d'accéder à une des pages de l'application et qu'il n'est pas connecté.



Liste des notices
=================

.. image:: _static/p4l_list.png
    :width: 600pt

Cet écran donne la liste des notices et permet la recherche.
La recherche se fait sur l'identifiant d'une notice, le(s) titre(s) d'une notice et les auteurs (personnes ou institutions).

Les notices sont affichées dans l'ordre de leur identifiant (tri lexicographique ascendant) lorsque qu'aucune recherche n'est faite. Elles sont triées par tri de pertinence lorsqu'une recherche a été effectuée.

En haut de la liste un bouton permet l'ouverture du dialogue de création d'une nouvelle notice.
Pour chaque notice de la liste 2 boutons sont proposés : vue de du détail de la liste ou bien édition. 


En haut de la page se trouve un champ de recherche permettant le filtrage des notices.
C'est une recherche de type full-text qui porte sur les champs suivants des notices :
  
    * identifiant
    * titres (dans toutes les langues)
    * auteurs (personnes et entités)

Le champ de recherche permet l'utilisation d'un mini langage de requête décrit à l'adresse suivante : http://pythonhosted.org/Whoosh/querylang.html
Les points à noter à ce sujet sont :
  
    * La recherche ne tient pas compte des accents
    * L'opérateur par défaut est le ``OR``.
    * la valeur du spécifieur ``field`` doit être dans la liste suivante : ``identifier``, ``titles``, ``years``, ``authors``.

Opérateurs de recherche : AND, OR, NOT
--------------------------------------

    * Les opérateurs de recherche AND, OR et NOT doivent s'écrire en majuscules.
    * ``032221`` cherche ``032221`` dans les titres et les auteurs et les identifiants.
    * ``032221 021099`` trouvera les deux notices avec ces deux identifiants.
    * ``language education`` cherche les mots ``language`` OU ``education`` dans les titres et les auteurs et les identifiants.
    * ``language AND education`` cherche les mots ``language`` ET ``education`` dans les titres et les auteurs et les identifiants.
    * ``language NOT education`` cherche le mot ``language`` SANS le mot ``education`` dans les titres et les auteurs et les identifiants.

Guillemets
----------

    * On peut mettre entre guillemets deux ou plusieurs termes pour chercher exactement sur cette expression
    * ``"school factors"`` cherche exactement l'expression "school factors" (et non pas "school OR factor", ni "school AND factor")

Parenthèses
-----------
 
    * ``(language AND education) OR maternelle`` cherche les notices contenant soit les mots ``language`` ET ``education``, soit le mot ``maternelle``

Troncature et joker ('*' et '?')
--------------------------------

    * le caractère ``*`` remplace n'importe quel nombre de lettres à la fin d'un terme. Le caractère ``?`` remplace un caractère et un seul, à la fin ou au milieu d'un terme de recherche.
    * ``lang*`` cherche tous les mots qui commencent par "lang" (language, langage, langagier, etc.)
    * ``l?ng`` trouvera à la fois "lang" et "long"

Champs de recherche
-------------------

    * ``titles:education`` cherche ``education`` uniquement dans les titres
    * ``authors:caillods`` cherche ``caillods`` uniquement dans les auteurs
    * ``years:2005`` cherche toutes les notices dont l'année est 2005 (ne cherche pas 2005 dans le titre)
    * ``education AND years:2005`` cherche ``education`` pour toutes les notices dont la date est 2005

.. _interface-detail:

Visionnage d'une notice
=======================

.. image:: _static/p4l_detail.png
    :width: 600pt

Cet écran donne accès à l'affichage du détail d'une notice. Deux boutons permettent soit de passer à l'écran d'édition de la notice, soit de pouvoir l'effacer.
Un dialogue de confirmation de l'effacement sera affiché préalablement à l'utilisateur.
Par contre, tout effacement d'une notice est définitif.


.. _interface-edit:

Édition d'une notice
====================

.. image:: _static/p4l_edit.png
    :width: 600pt

Cet écran permet l'édition d'une notice (nouvelle ou bien existante).
Un bouton d'annulation permet d'interrompre l'édition d'une fiche à tout moment.
Les modifications d'une fiche (ou bien sa création) ne seront sauvegardées seulement après avoir appuyer sur le bouton de sauvegarde.

Toute navigation hors de cet écran que ce soit en cliquant sur l'un des lien ou un des boutons de l'interface ou que ce soit en utilisant les fonctionnalités du navigateur annulera sans prévenir l'édition en cours.
Tous les changements non sauvegardés seront perdus.

Tous les champs sont éditables, a part les champs "identifiant" et "URI" qui sont en lecture seule.

Deux boutons sont disponibles pour accéder au détail de la notice ou bien à son effacement. Dans ce dernier cas un dialogue de confirmation sera affiché avant l'effacement définitif de la notice.



