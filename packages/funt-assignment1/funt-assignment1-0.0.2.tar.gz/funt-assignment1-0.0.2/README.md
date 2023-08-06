# Assignment 1

Il progetto presentato consiste nell'implementazione di due Pipeline CI/CD, in adozione dei principi DevOps. 
Il metodo di sviluppo software continuo (CI/CD) permette di eseguire in modo continuativo le fasi di build, test e deploy a cambiamenti iterativi di codice.

L'obiettivo è quello di automatizzare e rendere più efficiente l'intero processo di sviluppo di una semplice applicazione.

L'infrastruttura utilizzata per lo sviluppo delle Pipeline è Gitlab CI/CD. 

## Applicazione

Una semplice applicazione web verrà implementata appositamente per lo svolgimento del progetto così da poter osservare il corretto funzionamento e l'efficacia delle Pipeline CI/CD. 

L'applicazione proposta si presenterà all'utente con un minimale form in cui inserire il nome del corso universitario ed il relativo voto conseguito.
Tali dati verranno inseriti all'interno di un database e sarà dunque possibile all'utente, tramite appositi comandi, visualizzare lo storico degli esami e calcolare la media dei voti.

Tecnologie utilizzate:
- Python 3.x
- Flask 2.2.2, framework Web 
- SQLAlchemy, toolkit SQL e mappatore relazionale di oggetti
- Gunicorn, server HTTP Python Web Server Gateway Interface

## Modello di Sviluppo

Il modello di sviluppo di riferimento è il modello Multi-Branch, nel quale si assegnano ruoli molto specifici ai diversi branch e si definiscono i modi e i tempi delle loro interazioni. 
La scelta dello sviluppo Multi-Branch permette di adottare il principio DevOps di Continuous Delivery.

Il branch main memorizza la cronologia di rilascio ufficiale e il branch develop funge da branch di integrazione per le funzioni.
Ogni nuova funzione deve risiedere nel proprio branch; i branch feature usano il branch develop come branch principale.
Quando una funzione è completa, ne viene eseguito nuovamente il merge nel branch develop. Le funzioni non devono mai interagire direttamente con il branch main.

Una volta che develop ha acquisito un numero sufficiente di funzioni per effettuare un rilascio, si esegue un fork di un branch release da develop. 
La creazione di questo branch avvia il ciclo di rilascio successivo, pertanto non è possibile aggiungere nuove funzioni dopo questo punto.
Quando è tutto pronto per il rilascio, viene eseguito il merge del branch release in main e il branch viene contrassegnato con un numero di versione.
Inoltre, dovrebbe esserne eseguito nuovamente il merge in develop, che nel frattempo potrebbe essere avanzato dall'inizio del rilascio.

I branch di manutenzione, o "hotfix", vengono utilizzati per applicare rapidamente patch ai rilasci di produzione.

![img_1.png](img_1.png)

## Pipeline

La Pipeline si articola nei seguenti stage, approfonditi nelle relative sezioni:
- build: risolve le dipendenze e compila il codice
- verify: esegue l'analisi statica e/o dinamica
- unit-test: esegue i test di unità
- integration-test: esegue i test di integrazione fra le varie componenti
- package: genera il package da utilizzare per il rilascio
- release: rende il package disponibile per il download
- deploy: distribuisce il software per l'utilizzo esterno

Tecnologie utilizzate:
- Wheel, libreria di packaging standard
- Setuptools,  libreria di processi di sviluppo pacchetti
- Twine, utility per pubblicare pacchetti su PyPI
- Heroku, platform as a service (PaaS) sul cloud per distribuzione software

### Build

### Verify 

### Unit-Test

### Integration-Test

### Package 

### Release

### Deploy

## Membri del Gruppo

* Napoli Mattia _852239_
* Urbani Nicolò _856213_
* Tremolada Giulia _861144_
* Frigerio Riccardo _852226_

## Repository Link

La pipeline è accessibile alla repository GitLab al link:
https://gitlab.com/nicolo.urbani/2022_assignment1_title/

## License
This project is licensed under the MIT License.
