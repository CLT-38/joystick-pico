# Pico Joystick - Lecteur et Calibrateur

URL du repository : https://github.com/CLT-38/joystick-pico/

Ce projet transforme un Raspberry Pi Pico en une interface de lecture avancée pour un module joystick analogique. Il intègre un processus de calibration guidé au démarrage pour s'adapter précisément aux caractéristiques de votre matériel. Une fois calibré, il affiche en temps réel la position du joystick, la direction interprétée et l'état du bouton.

## Matériel requis
- Un Raspberry Pi Pico (n'importe quel modèle)
- Un module joystick analogique (2 axes + bouton-poussoir)
- Des câbles de connexion (jumper wires)
- Un PC
- Un câble USB (micro-B vers type A)

## Logiciel requis
- Le [firmware MicroPython pour Pico](https://micropython.org/download/RPI_PICO/) installé sur le Raspberry Pico.
- Le logiciel [Thonny](https://thonny.org/) installé sur le PC.
- Le code de ce projet : [pico_petit_joystick.py](pico_petit_joystick.py).

## Câblage
Connectez le module joystick au Raspberry Pi Pico en suivant les broches définies dans le script :

- **GND** du joystick -> une broche **GND** du Pico
- **+5V** (ou VCC) du joystick -> la broche **3V3(OUT)** du Pico
- **VRx** (axe X) du joystick -> la broche **GP26** (ADC0) du Pico
- **VRy** (axe Y) du joystick -> la broche **GP27** (ADC1) du Pico
- **SW** (bouton) du joystick -> la broche **GP16** du Pico

## Préparation dans Thonny
1.  Ouvrez Thonny.
2.  Allez dans le menu "Outils" -> "Options...".
3.  Dans l'onglet "Interpréteur", sélectionnez `MicroPython (Raspberry Pi Pico)` comme interpréteur.
4.  Juste en dessous, sélectionnez le port série correspondant à votre Pico (par ex. `COM3` sur Windows, `/dev/ttyACM0` sur Linux).
5.  Cliquez sur "OK". La console en bas devrait afficher une invite MicroPython (`>>>`).

## Télécharger et exécuter le code
1.  Ouvrez le fichier [pico_petit_joystick.py](pico_petit_joystick.py) dans l'éditeur de Thonny.
2.  Cliquez sur le bouton vert avec une flèche (ou appuyez sur F5) pour envoyer et exécuter le programme sur le Pico.

## Vérifier la bonne exécution
1.  Regardez la LED embarquée sur le Pico : elle doit se mettre à clignoter, indiquant que le script est actif.
2.  Observez la console dans Thonny. Le programme démarre en mode **calibration**. Suivez les instructions affichées.

### Étape 1 : Calibration
Le programme vous guidera à travers 5 étapes pour calibrer le centre, et les positions extrêmes (gauche, droite, haut, bas).

- Pour chaque étape, maintenez le joystick dans la position demandée.
- **Appuyez une fois** sur le bouton du joystick pour **démarrer** la capture.
- **Appuyez une seconde fois** pour **terminer** la capture de cette position.


A la fin de la calibration, vous pourrez tester le joystick et vérifier sur la sortie de Thonny que les directions indiquées sont correctes. De même, un clic sur le joystick doit afficher un message sur la console.

Exemple de sortie : `X:   -1% (32295) | Y:   -2% (31975) | Direction: CENTRE   | Bouton: RELACHE`


