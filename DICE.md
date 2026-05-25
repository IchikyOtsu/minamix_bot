# Dés — Guide `/roll`

## Syntaxe de base

| Commande | Résultat |
|---|---|
| `/roll 2d6` | Lance 2 dés à 6 faces |
| `/roll 1d20+5` | Lance 1d20, ajoute 5 |
| `/roll 3d8-2` | Lance 3d8, soustrait 2 |
| `/roll 4d6*2` | Lance 4d6, multiplie par 2 |
| `/roll 10d4/2` | Lance 10d4, divise par 2 |

## Séries

| Commande | Résultat |
|---|---|
| `/roll 6 4d6` | Lance 4d6 six fois (séries numérotées) |
| `/roll 2d6 ; 1d20 ; 3d8` | Jusqu'à 4 lancers séparés par `;` |

## Modificateurs

### Garder / Supprimer
| Commande | Résultat |
|---|---|
| `/roll 4d6 k3` | Garde les 3 **plus hauts** dés |
| `/roll 4d6 kl2` | Garde les 2 **plus bas** dés |
| `/roll 4d6 d1` | Supprime le **plus bas** dé |

### Exploser
Un dé explose = il est relancé et ajouté au total quand il atteint la valeur cible.

| Commande | Résultat |
|---|---|
| `/roll 4d6 e6` | Explose une fois si résultat = 6 |
| `/roll 4d6 e` | Explose une fois sur valeur max |
| `/roll 4d6 ie6` | Explose en chaîne sur 6 (max 100) |
| `/roll 4d6 ie` | Explose en chaîne sur valeur max |

### Relancer
| Commande | Résultat |
|---|---|
| `/roll 4d6 r2` | Relance une fois chaque dé ≤ 2 |
| `/roll 4d6 ir2` | Relance en boucle chaque dé ≤ 2 (max 100) |

### Succès / Échecs
Au lieu d'additionner, compte les dés qui atteignent un seuil.

| Commande | Résultat |
|---|---|
| `/roll 5d10 t7` | Compte les dés ≥ 7 (succès) |
| `/roll 5d10 t7 f1` | Succès ≥ 7, soustrait les dés ≤ 1 |
| `/roll 5d10 t7 b1` | Idem mais les dés ≤ 1 = botch |

## Flags d'affichage

| Flag | Effet |
|---|---|
| `s` | Résultat simplifié — total uniquement |
| `nr` | Masque les dés individuels |
| `ul` | Affiche les dés dans l'ordre de lancer (non trié) |
| `p` | Lancer privé — réponse visible uniquement par toi |
| `! texte` | Ajoute un commentaire affiché au-dessus |

Exemples :
```
/roll 4d6 s
/roll p 1d20
/roll 2d6 ! Mon attaque principale
```

## Combinaisons

Les modificateurs se cumulent :
```
/roll 4d6 ie6 k3 +2
/roll 5d10 t8 f1 ul
/roll p 2d20 k1 ! Avantage discret
```

---

## Alias D&D 5e

| Commande | Équivalent |
|---|---|
| `/roll dndstats` | 6× `4d6 d1` pour générer des stats |
| `/roll attack +5` | `1d20+5` |
| `/roll skill -2` | `1d20-2` |
| `/roll save +3` | `1d20+3` |
| `/roll +d20` | `2d20 k1` — avantage |
| `/roll -d20` | `2d20 kl1` — désavantage |

---

## Alias systèmes de jeu

### Chronicles of Darkness — `NcodX`
N dés d10, succès sur ≥ 8, les 10 explosent.
```
/roll 5cod
```

### World of Darkness — `NwodX`
N dés d10, succès sur ≥ X (défaut 8).
```
/roll 5wod7
```

### Fate / Fudge — `Ndf`
N dés Fate (−1 / 0 / +1), total entre −N et +N.
```
/roll 4df
```

### Warhammer Fantasy — `NwhX`
N dés d100, succès si résultat ≤ X.
```
/roll 3wh45
```

### Shadowrun — `srN`
N dés d6, compte les succès sur ≥ 5.
```
/roll sr8
```

### Earthdawn — `edN`
Lancer du pas N (1–50), utilise la table officielle de pas.
```
/roll ed7
/roll ed20
```

### AGE System — `age`
Lance 3d6, le deuxième est le "dé du dragon" (affecte les cascades).
```
/roll age
```

---

## Systèmes avancés

### Warhammer 40k : Wrath & Glory — `wng N`
Lance N dés d6. Le premier est le dé de Colère. Succès sur ≥ 4.
- Dé de Colère = 1 → Complication du Destin
- Dé de Colère = 6 → Gloire
```
/roll wng 6
```

### Dark Heresy 2e — `dh N`
Lance 1d100 contre un seuil de compétence N. Détecte la Fureur du Juste (double chiffres = succès) et le Désastre (double chiffres = échec).
```
/roll dh 45
```

### Godbound — `gb N`
Lance N dés d6, convertit le total en dégâts via la table officielle (1–3 → 1, 4–5 → 2, 6–9 → 4, 10–11 → 6, 12+ → 8).
```
/roll gb 3
```

---

## Aide in-game

```
/roll help
```
