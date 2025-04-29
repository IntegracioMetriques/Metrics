# MetricsApp

## Taula de continguts
- [Configuració per a una organització](#configuracio-per-a-una-organitzacio)
- [Configuració per a un repositori](#configuracio-per-a-un-repositori)

Aquesta eina serveix per a recollir mètriques dels repositoris de una organització o de un repositori concret. A continuació s'expliquen els pasos per a configurar-la, tan pe a una organització com per a un repositori concret.

## Configuració per a una organització

Aquests pasos cal que els faci el propietari de l'organització de github
El primer que cal fer és crear un repositori public nou a l'organització a partir d'aquest repositori, amb el botó Use this template a dalt a la dreta d'aquest repositori:

(Afegir foto)

Un cop creat, cal anar a la branca **gh-pages**, obrir docs/config.json i posar a excluded_repos el nom del repo que acabeu de crear. És molt important fer-ho a la branca  **gh-pages**, si ho feu a **main** o **master** no funcionarà. També si teniu com a membres de la organització professors i bots, heu de posar els seus noms d'usuari a excluded_members. Després us heu d'asegurar que metrics_scope i members posi org (ja hauria d'estar configurat així per defecte).

Després heu d'anar a configuració, i dintre de la categoria Code and automation, anar a Pages.
(Inserir foto aqui)

Un cop a Pages, deixeu Source a Deploy from a branch, i a branch poseu la branca **gh-pages** i canvieu la carpeta de /(root) a /docs.

(Inserir imatge)

Un cop fet això podeu tornar a la pagina de Code i a la seccio about, si cliqueu per cofigurar, hi ha un apartat que es website, i una checkbox *Use your GitHub Pages website*, marqueu-la i feu Save Changes. Podeu copiar aquest link i posarlo al about de tots els repositoris de la vostra organització.

(Inserir imatge de on es about i de la pantalla de editarlo)

L'últim pas es anar a la configuració del usuari que es el propietari de la organització, anar a developer setting, personal access tokens i Fine-graiend tokens, i donarli a generate new token. Pose-li el nom que vulgueu (metrics, p ex). heu de canviar el Resource Owner del token a la organització, i això només ho pot fer el propietari de la organització, per això és important que ho faci aquest. 

També poseu una Expiration date que duri fins al final del projecte, si es un projecte que entregueu el 31 de maig, poseu una setmana més per exemple.

(imatges de developer setting, fine-grained,)

A repository acces poseu all repositories.

A Repository permissions heu de seleccionar: 

-Actions: read and write

-Contents: read-only

-Issues: read-only

-Pull requests: read-only

A organization permissions:

-Members: read-only

Si ho heu seleccionat tot bé, quan li doneu a generate token, us sortiran els permissos seguents:

(imatge)

Un cop generat, copie el token temporalment a algun lloc, com a un arxiu de text, perquè un cop sortiu de la pagina ja no podreu veure'l més. 

Ara heu d'anar al repositori que he creat, configuració i a l'apartat Security, aneu a Secrets and variables, i seleccioneu Actions, i veure-u una pestanya que es secrets.

(Imatge)

Heu de crear un nou Secret amb el botó verd *New repository secret*. Es molt important que sigui a secret i no variables, perque no funcionarà i a més a més tothom podria veure el token, que per seguretat ha de ser privat. A name, en aquest cas cal que li poseu de nom **ORG_TOKEN** per aque funcioni, i enganxeu el token que heu copiat abans a l'apartat Secret, i feu Add secret. Encara no borreu el arxiu amb el token copiat.

Ara el repositori de metriques ja està configurat del tot, però per a que reculli metriques quan feu push a altres repositoris, cal que configure-ho a cada repositori una última cosa.

Per a cada repositori que volgueu recollir les metriques, cal seguir els pasos per afegir el token a cadascun d'ells, amb el mateix nom, i per últim, heu de copiar els arxius trigger_workflow.yml i remote_repo.json que són a al carpeta docs del repositori que acabeu de crear, poseu el nom del repositori amb el format **owner/name**, on owner és la organització i name es el nom del repositori, i a cada un dels repositoris, important que sigui a la branca **main** o **master**, crear ua carpeta .github, amb una altre a dins que es digui workflows, i a dins posar els dos arxius. Un cop fet això, ja esta configurat tot el repositori.



