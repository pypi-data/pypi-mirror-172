## README assignment1 gruppo CMST

#### URL REPOSITORY
https://gitlab.com/d_c_monti/assignment_1

#### COMPONENTI GRUPPO:
* Davide Monti
* Samuele Campanella
* Lorenzo Titta
* Davide Soldati

#### DESCRIZIONE APP:
L'applicazione permette ad un utente di gestire un elenco di attività.
Collegandosi all'applicazione l'utente può visualizzare le attività ancora da svolgere, cancellarla se svolta oppure modificarla.
###### Tecnologie utilizzate:
TaskMaster è stata realizzata con Python utilizzando il framework Flask per quanto riguarda la gestione del front-end e della logica applicativa.\
Il database invece è stato realizzato con SQLAlchemy, una libreria Python che permette di astrarre il codice sql necessario per la realizzazione del database

#### PIPELINE (WIP):
Abbiamo pensato di organizzare il repository secondo il modello git flow.\
Di conseguenza il repository avrà diversi branch per lo sviluppo e l'implementazione di singole feature, un branch develop su cui avverrà la merge delle varie feature una volta concluso il loro sviluppo e infine un branch main che coinciderà con la versione di release.
Per questo motivo utilizzeremo tre pipelines diverse: \
\
<img src="https://www.bitbull.it/blog/git-flow-come-funziona/gitflow-1.png" alt="drawing" style="width:500px;"/>

###### Pipeline feature:
Viene eseguita in tutti i rami feature. Di conseguenza abbiamo deciso che la pipeline si occuperà di eseguire le fasi di build e unit-test.

###### Pipeline develop:
Viene eseguita solo sul ramo develop al momento del merge con una nuova feature che è stata sviluppata. \
In questa pipeline oltre alle fasi eseguite nella pipeline feature vengono eseguiti anche gli integration test.

###### Pipeline master:
Si occupa della fase di release e deployment e viene esguita alla fine di un ciclo di sviluppo.
Per questo motivo in questa pipeline vengono eseguite le fasi di:
* Build
* Package
* Release
* Deployment


