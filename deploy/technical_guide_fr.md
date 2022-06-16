# Deploiement

## Debian 

### Construction du .deb AMD64

1. Faire une copie du dossier de base `dsm-cp/deploy/debian/dsmcp_v.v-v_amd64`, et le renommer en choississant la nouvelle version
	- Premier chiffre : version majeure (exemple : 2)
	- Deuxième chiffre : version mineure (exemple : 14)
	- Troisième chiffre : version de release Debian (exemple : 3)
	- Résultat : `2.14-3`
2. Copier tous les fichiers et dossiers de `dsm-cp/src` dans le dossier **renommé** `dsm-cp/deploy/debian/dsmcp_x.x-x_amd64/opt/dassym/dsmcp` du projet **(où x correspond à la version que vous avez paramétrée à l'étape 1)**
3. Ouvrir un terminal au dossier `dsm-cp/deploy/deb`
4. Executer `dpkg-deb --build --root-owner-group dsmcp_x.x-x_amd64` (changez la version dans le nom du dossier) : créer l'installeur .deb  
5. Récupérer le fichier créé (*dsmcp_x.x-x_amd64.deb*)

[tutoriel debian](https://wiki.debian.org/Packaging/Intro)

#### Construction d'un .deb ARM64

Après avoir généré votre *.deb* amd64 :

1. Dupliquer le dossier d'installeur amd64 et le renommer en `arm64`
2. Modifier le fichier `dsm-cp/deploy/debian/dsmcp_x.x-x_amd64/DEBIAN/control` 
3. Modifier `Architecture: amd64` en `Architecture: arm64`
4. Executer `dpkg-deb --build --root-owner-group dsmcp_x.x-x_arm64` (changez la version dans le nom du dossier) : créer l'installeur .deb  
5. Récupérer le fichier créé (*dsmcp_x.x-x_arm64.deb*)

### Installation du .deb 

1. Récupérer le fichier d'installation .deb 
2. Executer le fichier à l'aide de dpkg (`sudo dpkg -i <package_name>`)

### Supprimer le package 

1. `sudo dpkg --purge dsmcp` : supprime le paquet dsmcp

#### Problèmes rencontrés :

##### Erreur qt 

En démarrant une application *dcpbasic*, j'avais une erreur qt.

Détail de l'erreur : *qt.qpa.plugin: Could not load the Qt platform plugin "xcb" in "" even though it was found.*

**Résolution : **

1. `sudo python3 -m pip uninstall pyqt5` : désinstaller pyqt5
2. `sudo pip install pyqt5` : réinstaller pyqt5

##### Lock dans */var/lib/dpkg/lock*

L'installation de mon .deb a échoué (erreur dans le script de post installation). 

Détail de l'erreur : *Waiting for cache lock: Could not get lock /var/lib/dpkg/lock-frontend. It's held by process 1000 (dpkg)...*

**Résolution : **

1. `sudo kill -9 1000` (changer le PID *1000* suivant votre PID) : arrêter de force le processus dpkg qui est en erreur
2. `sudo rm /var/lib/dpkg/lock-frontend` : supprimer le premier lock
3. `sudo rm /var/lib/dpkg/lock` : supprimer le deuxième lock
4. `sudo dpkg --configure -a` : reconfigurer dpkg 
5. `sudo dpkg --purge dsmcp` : supprimer le paquet qui a échoué son installation
6. Régler les problèmes de l'installeur (le plus souvent dans le script *postinst*)

Conseil : Si l'erreur est juste `Errors were encountered while processing: dsmcp`, il suffit de commencer l'étape 5.

[source](https://itsfoss.com/could-not-get-lock-error/)

##### Version de Dapi2 trop ancienne

La version pypi de dapi2 n'était plus compatible avec *dsmcp*.

**Résolution : **

1. `sudo dpkg --purge pydapi2` : supprimer l'ancienne version de *pydapi2*
2. Récupérer la dernière version de *pydapi2* sur git
3. Compresser la dernière version téléchargée de dsm-cp en *tar.gz*
4. Copier le tarball (fichier *tar.gz*) dans la machine cible
5. Décompresser l'archive dans `~/git`
6. `sudo pip3 install -e /home/USER/git/PyDapi2/ --upgrade` **(Ne pas oublier de changer USER par votre nom d'utilisateur)** : ajoute le package pydapi au bibliothèques pip 

##### Pas d'accès aux ports série  

Mon utilisateur n'a pas accès aux ports série.

Détail de l'erreur : *serial.serialutil.SerialException: [Errno 13] could not open port /dev/ttyS0: [Errno 13] Permission denied: '/dev/ttyS0'*

**Résolution : **

1. `sudo usermod -aG dialout $USER` : ajoute l'utilisateur actuel au groupe dialout (communication ports série), effectif après déconnexion de l'utilisateur
2. `reboot` : redémarrage pour rendre le changement de groupe effectif 

##### Erreur lancement dcpdev

Détail de l'erreur : *TypeError: prepareCfg() takes 2 positional arguments but 3 were given*

**Résolution : **

1. La version dev de dsmcp n'a qu'une version graphique, il faut donc la lancer : `python 3 dcpdev.py -S --gui=qt5`

##### Erreur QGraphicsSVG

Détail de l'erreur *ImportError: cannot import name 'QGraphicsSvgItem' from 'PyQt5.Qt'*

**Résolution:**

1. Installer le package : `sudo apt-get install libqt5svg5*`


## Windows

### Construction de l'executable 

1. Avoir un ordinateur Windows 10 (?avec python >3.8 installé)
2. Installer Inno Setup [ici](https://jrsoftware.org/isinfo.php)
3. Cloner les fichiers du projet dsmcp dans le disque *G:* (ou changer les variables de chemin de fichiers dans le script iss)
4. Ouvrir le script `deploy/windows/InstallDsmcp.iss` avec Inno setup
5. Compiler le script iss (Barre des menus > *Build* > *Compile*)
6. Récupérer l'installeur exécutable créé dans `deploy/windows/dsmcp-setup.exe`

### Installation

1. Avoir un ordinateur Windows 10, avec python >3.8 installé 
2. Télécharger l'installeur Windows *.exe*
3. Executer l'installateur *.exe*
4. Suivre les instruction d'installation
5. Ouvrir un cmd et taper `dcpbasic -S` (démarre 'app basic sans gui)


## Démarrer les applications

Commandes bash / cmd pour démarrer les applications :

* dcpbasic sans gui : `dcpbasic -S`
* dcpbasic avec gui qt5 : `dcpbasic -S --gui=qt5`
* dcpdev avec gui qt5 : `dcpdev -S --gui=qt5`  (attention à ne pas oublier `--gui=qt5`)


