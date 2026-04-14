# 🧩 Calendar Puzzle Solver

Ce projet propose un solveur automatisé pour le "Calendar Puzzle" (casse-tête du calendrier quotidien). Il utilise la programmation par contraintes pour trouver l'agencement exact des 8 pièces géométriques permettant de laisser visibles uniquement le mois et le jour sélectionnés.

Le projet inclut un script en ligne de commande ainsi qu'une interface web interactive et visuelle.

**Testez l'application en direct : [https://calendar-puzzle.onrender.com/](https://calendar-puzzle.onrender.com/)**

---

## ✨ Fonctionnalités

* **Résolution exacte :** Calcule l'une des solutions valides pour n'importe quelle date de l'année (ex: `OCT 18`).
* **Moteur performant :** Modélisation mathématique via la bibliothèque `pycsp3` et résolution par contraintes (Exact Cover).
* **Interface Web :** Application Flask légère avec un affichage visuel coloré généré via Tailwind CSS.
* **Prêt pour la production :** Configuration Docker incluse (Java + Python).

---

## 📁 Structure du projet

```text
calendar_puzzle/
│
├── solver.py               # Script CLI pour la résolution dans le terminal
├── app.py                  # Serveur web Flask contenant le moteur de résolution
├── requirements.txt        # Dépendances Python du projet
├── Dockerfile              # Configuration pour le déploiement cloud
└── templates/
    └── index.html          # Interface utilisateur web (HTML + Tailwind CSS)
