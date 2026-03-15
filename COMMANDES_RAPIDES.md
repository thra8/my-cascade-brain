# 🕹️ COMMANDES RAPIDES CASCADE

> Copie-colle simplement la commande suivie de tes infos.

| Commande | Action | Usage |
| :--- | :--- | :--- |
| `/réparateur` | Fixe les bugs & dossiers | `/réparateur` |
| `/ingest` | Apprend un nouveau skill | `/ingest [Coller lien ou texte ici]` |
| `/santé` | Diagnostic complet | `/santé` |
| `/sync` | Sauvegarde GitHub | `/sync` |
| `/dash` | Dashboard Temps Réel | `/dash` |
| `/clean` | Purge logs & cache | `/clean` |

---

## 📋 Détail des Commandes

### 🔧 `/réparateur`
Exécute le système de réparation automatique pour restaurer l'intégrité du système Cascade.

**Usage** : `/réparateur`

**Actions** :
- Lance `self_repair.py`
- Répare les permissions
- Valide la structure des dossiers
- Corrige les fichiers corrompus

### 📥 `/ingest`
Mode ingestion de compétences pour apprendre de nouveaux patterns et optimisations.

**Usage** : `/ingest [texte ou lien]`

**Exemples** :
```
/ingest https://github.com/user/repo
/ingest Nouvelle technique NumPy pour M1 avec vectorisation
```

**Actions** :
- Analyse le contenu fourni
- Extrait les patterns clés
- Formate en standard Architect
- Intègre dans `skills.md`

### 🩺 `/santé`
Diagnostic complet du système Cascade avec rapport de performance.

**Usage** : `/santé`

**Actions** :
- Lance `check_system.py`
- Teste les performances NumPy/Metal
- Valide la structure des fichiers
- Affiche le rapport de santé

### 🔄 `/sync`
Synchronisation complète avec GitHub pour sauvegarder la mémoire.

**Usage** : `/sync`

**Actions** :
- Lance `sentinel.py`
- Valide la mémoire
- Commit et push automatiques
- Vérifie l'intégrité

### 📊 `/dash`
Lancement ou rafraîchissement du dashboard de monitoring temps réel.

**Usage** : `/dash`

**Actions** :
- Lance `windsurf_monitor.py`
- Affiche les métriques système
- Surveille les services actifs
- Monitoring en continu

### 🧹 `/clean`
Nettoyage complet des fichiers temporaires, logs et cache.

**Usage** : `/clean`

**Actions** :
- Supprime les fichiers `.pyc`
- Nettoie les dossiers `__pycache__`
- Purge les logs temporaires
- Libère l'espace disque

---

## 🚀 Workflow Rapide

### Installation Initiale
```bash
git clone https://github.com/thra8/my-cascade-brain.git
cd cascade-brain
just install
```

### Vérification Santé
```bash
/santé
```

### Développement Quotidien
```bash
/dash          # Monitor en continu
/ingest [skill] # Apprendre nouvelle compétence
/sync          # Sauvegarder progression
```

### Maintenance
```bash
/clean         # Nettoyer
/réparateur    # Réparer si nécessaire
/santé         # Vérifier après réparation
```

---

## 🎯 Tips d'Utilisation

### ⚡ Performance
- Utilise `/santé` pour vérifier les performances après modifications
- Lance `/clean` avant les benchmarks
- Utilise `/dash` pour surveiller en temps réel

### 📚 Apprentissage
- `/ingest` accepte les liens GitHub et les blocs de texte
- Les compétences sont automatiquement formatées et catégorisées
- Vérifie avec `/skills` après ingestion

### 🔧 Maintenance
- `/réparateur` résout la plupart des problèmes courants
- `/sync` assure la sauvegarde automatique
- `/clean` libère l'espace et améliore les performances

---

## 📞 Aide Rapide

Pour obtenir de l'aide sur une commande spécifique :
```bash
/help [commande]
```

Pour voir toutes les commandes disponibles :
```bash
/help
```

Pour le statut complet du système :
```bash
/status
```

---

*Ce document est mis à jour automatiquement avec l'évolution du système Cascade.*
