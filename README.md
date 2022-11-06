# Simulation du Trafic Routier
TIPE Option PC | Palmero Pierre-Antoine & Hachet Alexandre

## Méthode de récupération des données
Les données récupéré pour l'analyse sont issues de bison-fute, un raspberry-pi fait une requête sur le document xml
correspondant toutes les 30 min, le fichier xml est parser par un script python et les données sont stockées sous forme
de document cvs.
<br>
Un dataset de test est disponible dans "Analyse/Test_Dataset/"

## ToDo List
 - ### Etude théorique
   - [ ] Modélisation de la fem d'une bobine

 - ### Outils de traitement
   - [x] Convertisseur XML vers CSV
   
 - ### Modélisation
   - [ ] Simulation SOL2
   - [ ] Modèle python
   
 - ### Analyse
   - [ ] Analyse des résultats
