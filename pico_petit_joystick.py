from machine import Pin, ADC
from time import sleep
import time

# Configuration de la LED intégrée
led = Pin("LED", Pin.OUT)

# Configuration du joystick
vrx = ADC(Pin(26))  # Axe X sur GP26 (ADC0)
vry = ADC(Pin(27))  # Axe Y sur GP27 (ADC1)
sw = Pin(16, Pin.IN, Pin.PULL_UP)  # Bouton sur GP16 avec pull-up

print("Bonjour depuis la Pico")
print("Programme de lecture du mini joystick")
print("VRx -> GP26, VRy -> GP27, SW -> GP16")
print("Bougez le joystick et appuyez sur le bouton...")
print("-" * 50)

# Variables pour détecter les changements
last_button_state = True

# Variables de calibration (seront ajustées automatiquement)
min_x, max_x = 65535, 0
min_y, max_y = 65535, 0
center_x, center_y = 32768, 32768
dead_zone_x = 1000  # Zone morte pour l'axe X
dead_zone_y = 1000  # Zone morte pour l'axe Y

# Mode calibration guidée
calibration_mode = True
calibration_collecting = False  # Nouvel état pour savoir si on collecte
calibration_step = 0  # 0=centre, 1=gauche, 2=droite, 3=haut, 4=bas
calibration_samples = 0
samples_per_step = 20
_instruction_shown = False # Variable interne pour gérer l'affichage
calibration_instructions = [
    "LAISSEZ le joystick au CENTRE",
    "POUSSEZ le joystick vers la GAUCHE",
    "POUSSEZ le joystick vers la DROITE", 
    "POUSSEZ le joystick vers le HAUT",
    "POUSSEZ le joystick vers le BAS"
]

def get_direction(x, y):
    """Détermine la direction basée sur les valeurs X et Y"""
    dx = x - center_x
    dy = y - center_y
    
    # Utiliser des zones mortes dynamiques pour chaque axe
    if abs(dx) < dead_zone_x and abs(dy) < dead_zone_y:
        return "CENTRE"
    
    # Déterminer la direction principale
    if abs(dx) > abs(dy):
        return "DROITE" if dx > 0 else "GAUCHE"
    else:
        return "HAUT" if dy > 0 else "BAS"

def map_value(value, val_min, val_max, new_min=-100, new_max=100):
    """Convertit une valeur vers -100 à +100 en utilisant min/max réels"""
    if val_max == val_min:
        return 0
    return int((value - val_min) * (new_max - new_min) / (val_max - val_min) + new_min)

while True:
    # Lecture des valeurs analogiques (0-65535)
    x_raw = vrx.read_u16()
    y_raw = vry.read_u16()
    
    # Mode calibration au démarrage
    if calibration_mode:
        button_state = sw.value()
        # Détecter un front descendant (appui)
        button_pressed = not button_state and last_button_state

        if not calibration_collecting:
            # Afficher l'instruction une seule fois par étape
            if not _instruction_shown:
                print(f"\nÉtape {calibration_step + 1}/5: {calibration_instructions[calibration_step]}")
                print("Appuyez sur le bouton pour COMMENCER la capture...")
                _instruction_shown = True

            # Un appui démarre la collecte
            if button_pressed:
                print("Capture en cours... Maintenez la position.")
                print("Appuyez à nouveau pour TERMINER cette étape.")
                calibration_collecting = True
                sleep(0.2)  # Anti-rebond
        
        else:  # Mode collecte en cours
            # Un deuxième appui termine la collecte pour cette étape
            if button_pressed:
                print("Position enregistrée !")
                
                if calibration_step == 3:  # Fin de calibration HAUT
                    print(f"Calibration HAUT terminée. max_y = {max_y}")
                elif calibration_step == 4:  # Fin de calibration BAS
                    print(f"Calibration BAS terminée. min_y = {min_y}")
                    # Vérifier si les valeurs sont logiques
                    if min_y >= max_y:
                        print("ATTENTION: min_y >= max_y, inversion des valeurs...")
                        min_y, max_y = max_y, min_y
                
                calibration_step += 1
                calibration_samples = 0
                calibration_collecting = False
                _instruction_shown = False  # Pour réafficher à la prochaine étape
                
                # Calibration terminée ?
                if calibration_step >= len(calibration_instructions):
                    calibration_mode = False
                    # Calculer les zones mortes dynamiques (15% de la plage)
                    dead_zone_x = (max_x - min_x) * 0.15
                    dead_zone_y = (max_y - min_y) * 0.15
                    
                    print(f"\nCalibration terminée!")
                    print(f"Centre: X={center_x}, Y={center_y}")
                    print(f"Plages: X[{min_x}-{max_x}], Y[{min_y}-{max_y}]")
                    print(f"Zone morte calculée: X={dead_zone_x:.0f}, Y={dead_zone_y:.0f}")
                    print("Maintenant, testez toutes les directions du joystick...")
                    print("-" * 60)
                
                sleep(0.2)  # Anti-rebond
                last_button_state = button_state
                continue

            # Pendant la collecte, on met à jour les valeurs
            # Traitement selon l'étape
            if calibration_step == 0:  # Centre
                if calibration_samples == 0:
                    center_x = x_raw
                    center_y = y_raw
                else:
                    center_x = (center_x * calibration_samples + x_raw) // (calibration_samples + 1)
                    center_y = (center_y * calibration_samples + y_raw) // (calibration_samples + 1)
            elif calibration_step == 1:  # Gauche
                min_x = min(min_x, x_raw)
            elif calibration_step == 2:  # Droite
                max_x = max(max_x, x_raw)
            elif calibration_step == 3:  # Haut
                max_y = max(max_y, y_raw)
            elif calibration_step == 4:  # Bas
                min_y = min(min_y, y_raw)
            
            calibration_samples += 1
            if calibration_samples % 5 == 0: # Afficher toutes les 5 mesures
                print(f"Échantillon {calibration_samples}: X={x_raw}, Y={y_raw}")
        
        last_button_state = button_state
        led.toggle()
        sleep(0.05)
        continue
    
    # Lecture du bouton (False = pressé, True = relâché)
    button_state = sw.value()
    
    # Conversion en pourcentage (-100 à +100) avec les vraies valeurs
    x_percent = map_value(x_raw, min_x, max_x)
    y_percent = map_value(y_raw, min_y, max_y)
    
    # Détection de la direction
    direction = get_direction(x_raw, y_raw)
    
    # Affichage des valeurs avec les valeurs brutes pour debug
    print(f"X: {x_percent:+4d}% ({x_raw:5d}) | Y: {y_percent:+4d}% ({y_raw:5d}) | Direction: {direction:8s} | Bouton: {'PRESSE' if not button_state else 'RELACHE'}")
    
    # Détection du changement d'état du bouton
    if button_state != last_button_state:
        if not button_state:
            print("*** BOUTON PRESSE ! ***")
        else:
            print("*** BOUTON RELACHE ! ***")
        last_button_state = button_state
    
    # Faire clignoter la LED pour montrer que le programme est actif
    led.toggle()
    
    sleep(0.1)  # Lecture 10 fois par seconde


