# 🎛️ CASCADE ARCHITECT CONTROL CENTER

> **Usage :** Copie-colle le bloc correspondant dans le chat Cascade selon ton besoin.

---

### 🧠 GESTION DE LA MÉMOIRE & SYNC
**Utilité :** Charger les derniers skills depuis GitHub ou sauvegarder l'état actuel du cerveau.

**Prompt Sync-Load :**
> "Exécute le protocole Sentinel : lance './windsurf/scripts/sync.sh load' puis lis 'windsurf/memory/skills.md' pour rafraîchir ton contexte expert."

**Prompt Sync-Save :**
> "Archive ma progression : mets à jour 'windsurf/memory/skills.md' avec les nouveaux acquis de cette session, puis exécute './windsurf/scripts/sentinel.py' pour pousser vers GitHub."

---

### ⚡ PERFORMANCE & RENDU M1 (METAL)
**Utilité :** Lancer les calculs lourds sur le GPU ou optimiser les scripts NumPy.

**Prompt Launch-Shader :**
> "Passe en mode GPU-Acceleration : compile 'fractal.metal' et lance 'metal_streamer.py'. Assure-toi que le buffer de rendu est optimisé pour l'architecture de mémoire unifiée du M1."

**Prompt Optimize-Math :**
> "Analyse ce script : remplace toutes les boucles Python par des opérations vectorisées NumPy (Broadcasting) compatibles avec le framework Accelerate d'Apple."

---

### 🖥️ MONITORING & DASHBOARD
**Utilité :** Visualiser l'état du système et de la mémoire en temps réel.

**Prompt Launch-Dash :**
> "Lance le 'windsurf_monitor.py' dans un terminal séparé. Surveille spécifiquement mes services FastAPI (port 8000) et Next.js (port 3000)."

---

### 🧹 COMPRESSION DE CONTEXTE (ANTI-LAG)
**Utilité :** Résumer l'échange quand la discussion devient trop longue pour éviter que Cascade ne perde le fil.

**Prompt Compress :**
> "Le contexte devient saturé. Analyse notre historique, extrais les décisions d'architecture critiques dans 'windsurf/memory/context_snapshot.md', puis vide ta mémoire active pour repartir sur une base propre."

---

### 🛠️ MAINTENANCE & SETUP
**Utilité :** Nettoyer l'environnement ou vérifier l'intégrité du système.

**Prompt Cleanup :**
> "Exécute 'just cleanup' pour purger les fichiers temporaires, les logs et les processus zombies sur les ports actifs."

**Prompt Check-Integrity :**
> "Lance 'python3 scripts/validate_memory.py' pour vérifier que nos fichiers de skills sur GitHub respectent les standards du CI."

---

### 🏗️ ARCHITECTURE & UI/UX
**Utilité :** Générer des composants ou des schémas techniques.

**Prompt Design-UI :**
> "Crée un composant UI en Braille Unicode haute-fidélité pour [NOM_DU_MODULE]. Utilise des dégradés TrueColor (24-bit) et intègre une physique d'easing pour les transitions."

---

### 📊 COMMANDES RAPIDES (Terminal)

#### **Sync & Memory**
```bash
# Charger depuis GitHub
python3 windsurf/scripts/sentinel.py

# Forcer le sync
python3 windsurf/scripts/sentinel.py --force

# Valider la mémoire
python3 windsurf/scripts/sentinel.py --validate
```

#### **Performance & GPU**
```bash
# Lancer le rendu GPU Metal
python3 metal_streamer.py

# Démonstration GPU
python3 skills/metal-gpu-rendering/metal_demo.py

# Optimiser les performances
python3 -c "import numpy as np; print('NumPy version:', np.__version__)"
```

#### **Monitoring**
```bash
# Dashboard temps réel
python3 windsurf_monitor.py

# Monitoring des services
python3 windsurf_monitor.py --services-only

# Logs système
tail -f logs/evolution.log
```

#### **Maintenance**
```bash
# Nettoyage complet
find . -name "*.pyc" -delete
find . -name "__pycache__" -type d -exec rm -rf {} +

# Vérifier l'intégrité
python3 -m py_compile windsurf/scripts/sentinel.py

# Status Git
git status --porcelain
```

---

### 🎯 ALIASES TERMINAL (À ajouter à ~/.zshrc)

```bash
# Cascade Brain aliases
alias brain='cd /Users/bp/Documents/cascade-brain && python3 windsurf_monitor.py'
alias sync='cd /Users/bp/Documents/cascade-brain && python3 windsurf/scripts/sentinel.py'
alias gpu='cd /Users/bp/Documents/cascade-brain && python3 metal_streamer.py'
alias skills='cd /Users/bp/Documents/cascade-brain && cat windsurf/memory/skills.md'
alias context='cd /Users/bp/Documents/cascade-brain && cat windsurf/memory/context_snapshot.md'

# Maintenance aliases
alias cleanup='find . -name "*.pyc" -delete && find . -name "__pycache__" -type d -exec rm -rf {} +'
alias cascade-status='cd /Users/bp/Documents/cascade-brain && git status && python3 windsurf/scripts/sentinel.py --status'
```

---

### 🔧 CONFIGURATION RAPIDE

#### **Initialisation Rapide**
```bash
# Clone et setup
git clone https://github.com/thra8/my-cascade-brain.git cascade-brain
cd cascade-brain
./setup_cascade_pro.sh

# Configuration Git
git remote set-url origin git@github.com:thra8/my-cascade-brain.git
git push -u origin main

# Lancer le monitor
python3 windsurf_monitor.py
```

#### **Vérification Santé**
```bash
# Vérifier Metal
python3 -c "import Metal; print('Metal OK:', Metal.MTLCreateSystemDefaultDevice())"

# Vérifier NumPy
python3 -c "import numpy as np; print('NumPy OK:', np.__version__)"

# Vérifier les dépendances
python3 -c "import psutil; print('PSUtil OK:', psutil.cpu_percent())"
```

---

### 📈 PERFORMANCE TARGETS

#### **M1 Optimization**
- **CPU Usage** : < 50% pour les opérations normales
- **Memory Usage** : < 4GB pour le stack complet
- **GPU Rendering** : 60+ FPS pour fractales 120x60
- **Response Time** : < 100ms pour les commandes

#### **Memory Management**
- **Skills File** : < 50KB avec compression
- **Context Snapshot** : < 20KB
- **Evolution Log** : < 100KB avec rotation
- **Git History** : Nettoyage après 100 commits

---

### 🚨 DÉPANNAGE RAPIDE

#### **Problèmes Communs**
```bash
# Metal non disponible
python3 -c "import Metal; print(Metal.MTLCreateSystemDefaultDevice())"

# Permissions refusées
chmod +x windsurf/scripts/sentinel.py
chmod +x setup_cascade_pro.sh

# Git SSH error
ssh -T git@github.com
git remote set-url origin https://github.com/thra8/my-cascade-brain.git

# Memory corruption
python3 windsurf/scripts/sentinel.py --validate
git checkout windsurf/memory/
```

#### **Recovery Commands**
```bash
# Restaurer depuis GitHub
git fetch origin
git reset --hard origin/main

# Recréer l'environnement
./setup_cascade_pro.sh --force

# Nettoyer et réinitialiser
cleanup
python3 windsurf/scripts/sentinel.py --force
```

---

### 📚 RÉFÉRENCES RAPIDES

#### **Skills Disponibles**
- **3D Graphics** : Braille Unicode 2x8, 68.8 FPS
- **Color Design** : TrueColor 24-bit, WCAG compliance
- **DevOps** : Stack health, port management
- **AI Assistant** : Devin-like planning
- **Memory** : Cipher integration, MCP support
- **Spec-Driven** : GitHub workflow, multi-agent
- **Metal GPU** : Fractales, fluid simulation

#### **Architecture M1**
- **CPU** : 8 cores (4 P-cores + 4 E-cores)
- **GPU** : 8 cores, 2.6 TFLOPS
- **Memory** : 8GB unified, 68.25 GB/s bandwidth
- **Neural Engine** : 16 cores, 11 TOPS

---

### 🎮 MODES AVANCÉS

#### **GPU-Accelerated Mode**
```bash
# Activer le mode GPU
export CASCADE_GPU_MODE=1
python3 metal_streamer.py

# Mode haute performance
export CASCADE_PERFORMANCE=high
python3 metal_streamer.py --resolution 240x120
```

#### **Development Mode**
```bash
# Mode développement avec logs
export CASCADE_DEBUG=1
python3 windsurf/scripts/sentinel.py --verbose

# Mode test
export CASCADE_TEST_MODE=1
python3 -m pytest skills/
```

---

### 📝 NOTES PERSONNELLES

#### **Workflow Quotidien**
1. **Morning** : `brain` → Charger contexte
2. **Development** : Utiliser skills selon besoin
3. **Sync** : `sync` → Sauvegarder progression
4. **Evening** : `cleanup` → Nettoyer environnement

#### **Best Practices**
- Toujours sync avant les changements majeurs
- Utiliser le GPU pour les calculs intensifs
- Monitorer les performances M1
- Compresser le contexte régulièrement

---

**Dernière mise à jour** : 2025-03-15  
**Version** : 1.0.0  
**Platform** : macOS M1 (ARM64)  
**Repository** : https://github.com/thra8/my-cascade-brain
