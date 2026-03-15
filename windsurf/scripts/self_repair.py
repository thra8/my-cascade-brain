#!/usr/bin/env python3
"""
Cascade Self-Repair System
Diagnostic et réparation automatique des problèmes système
"""

import os
import subprocess
import sys
import shutil
from pathlib import Path
from datetime import datetime

class CascadeRepair:
    """Système de réparation automatique pour Cascade Architect"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.windsurf_dir = self.project_root / "windsurf"
        self.memory_dir = self.windsurf_dir / "memory"
        self.scripts_dir = self.windsurf_dir / "scripts"
        
        self.repairs_done = []
        self.errors_found = []
        
    def log_repair(self, action: str, success: bool, details: str = ""):
        """Enregistrer une action de réparation"""
        status = "✅" if success else "❌"
        print(f"{status} {action}")
        if details:
            print(f"   {details}")
        
        if success:
            self.repairs_done.append(action)
        else:
            self.errors_found.append(f"{action}: {details}")
    
    def check_and_create_directories(self):
        """Vérifier et créer les répertoires essentiels"""
        print("--- 📁 Vérification des répertoires ---")
        
        essential_dirs = [
            self.windsurf_dir,
            self.memory_dir,
            self.scripts_dir,
            self.memory_dir / "backups",
        ]
        
        for dir_path in essential_dirs:
            if not dir_path.exists():
                try:
                    dir_path.mkdir(parents=True, exist_ok=True)
                    self.log_repair(f"Création répertoire {dir_path.name}", True)
                except Exception as e:
                    self.log_repair(f"Création répertoire {dir_path.name}", False, str(e))
            else:
                print(f"✅ Répertoire {dir_path.name} existe")
        
        print()
    
    def check_and_create_files(self):
        """Vérifier et créer les fichiers essentiels"""
        print("--- 📄 Vérification des fichiers ---")
        
        essential_files = {
            self.windsurf_dir / ".windsurfrules": self._create_windsurf_rules,
            self.memory_dir / "identity.md": self._create_identity_file,
            self.memory_dir / "skills.md": self._create_skills_file,
            self.memory_dir / "context_snapshot.md": self._create_context_file,
            self.project_root / "requirements.txt": self._create_requirements_file,
            self.project_root / ".python-version": self._create_python_version_file,
            self.project_root / "justfile": self._create_justfile,
        }
        
        for file_path, create_func in essential_files.items():
            if not file_path.exists():
                try:
                    create_func(file_path)
                    self.log_repair(f"Création fichier {file_path.name}", True)
                except Exception as e:
                    self.log_repair(f"Création fichier {file_path.name}", False, str(e))
            else:
                print(f"✅ Fichier {file_path.name} existe")
        
        print()
    
    def fix_permissions(self):
        """Corriger les permissions des scripts"""
        print("--- 🔧 Correction des permissions ---")
        
        executable_files = [
            self.scripts_dir / "skill_ingest.py",
            self.scripts_dir / "sentinel.py",
            self.scripts_dir / "check_system.py",
            self.project_root / "windsurf_monitor.py",
            self.project_root / "setup_cascade_pro.sh",
        ]
        
        for file_path in executable_files:
            if file_path.exists():
                try:
                    current_perms = oct(file_path.stat().st_mode)[-3:]
                    if current_perms != "755":
                        file_path.chmod(0o755)
                        self.log_repair(f"Permissions {file_path.name}", True, f"Changé de {current_perms} à 755")
                    else:
                        print(f"✅ Permissions {file_path.name} OK")
                except Exception as e:
                    self.log_repair(f"Permissions {file_path.name}", False, str(e))
            else:
                print(f"⚠️ Fichier {file_path.name} manquant")
        
        print()
    
    def fix_git_repository(self):
        """Vérifier et réparer le repository Git"""
        print("--- 🔄 Vérification Git ---")
        
        git_dir = self.project_root / ".git"
        if not git_dir.exists():
            try:
                subprocess.run(["git", "init"], check=True, capture_output=True)
                self.log_repair("Initialisation Git", True)
            except subprocess.CalledProcessError as e:
                self.log_repair("Initialisation Git", False, str(e))
        else:
            print("✅ Repository Git initialisé")
        
        # Vérifier le remote
        try:
            result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
            if "github.com" not in result.stdout:
                # Ajouter le remote GitHub
                remote_url = "https://github.com/thra8/my-cascade-brain.git"
                subprocess.run(["git", "remote", "add", "origin", remote_url], check=True)
                self.log_repair("Configuration remote GitHub", True)
            else:
                print("✅ Remote GitHub configuré")
        except subprocess.CalledProcessError as e:
            self.log_repair("Configuration remote GitHub", False, str(e))
        
        print()
    
    def fix_virtual_environment(self):
        """Vérifier et réparer l'environnement virtuel"""
        print("--- 🐍 Vérification environnement virtuel ---")
        
        venv_dir = self.project_root / "venv"
        python_cmd = "python3.12"
        
        if not venv_dir.exists():
            try:
                subprocess.run([python_cmd, "-m", "venv", "venv"], check=True)
                self.log_repair("Création environnement virtuel", True)
            except subprocess.CalledProcessError as e:
                self.log_repair("Création environnement virtuel", False, str(e))
        else:
            print("✅ Environnement virtuel existe")
        
        # Vérifier les dépendances
        requirements_file = self.project_root / "requirements.txt"
        if requirements_file.exists():
            try:
                activate_script = venv_dir / "bin" / "activate"
                if activate_script.exists():
                    # Installer les dépendances
                    pip_cmd = f"source {activate_script} && pip install -r {requirements_file}"
                    result = subprocess.run(pip_cmd, shell=True, capture_output=True, text=True)
                    if result.returncode == 0:
                        self.log_repair("Installation dépendances", True)
                    else:
                        self.log_repair("Installation dépendances", False, result.stderr)
                else:
                    self.log_repair("Installation dépendances", False, "Script d'activation non trouvé")
            except Exception as e:
                self.log_repair("Installation dépendances", False, str(e))
        
        print()
    
    def clean_temporary_files(self):
        """Nettoyer les fichiers temporaires"""
        print("--- 🧹 Nettoyage des fichiers temporaires ---")
        
        temp_patterns = [
            "*.pyc",
            "__pycache__",
            ".DS_Store",
            "*.log",
            "*.tmp",
        ]
        
        cleaned_count = 0
        for pattern in temp_patterns:
            try:
                if pattern.endswith("/"):
                    # Directory pattern
                    for dir_path in self.project_root.rglob(pattern.rstrip("/")):
                        if dir_path.is_dir():
                            shutil.rmtree(dir_path)
                            cleaned_count += 1
                else:
                    # File pattern
                    for file_path in self.project_root.rglob(pattern):
                        if file_path.is_file():
                            file_path.unlink()
                            cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Erreur nettoyage {pattern}: {e}")
        
        if cleaned_count > 0:
            self.log_repair("Nettoyage fichiers temporaires", True, f"{cleaned_count} fichiers supprimés")
        else:
            print("✅ Aucun fichier temporaire à nettoyer")
        
        print()
    
    def validate_system_integrity(self):
        """Valider l'intégrité du système"""
        print("--- 🔍 Validation intégrité système ---")
        
        # Vérifier Python
        try:
            result = subprocess.run(["python3.12", "--version"], capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Python 3.12 disponible: {result.stdout.strip()}")
            else:
                self.log_repair("Vérification Python 3.12", False, "Python 3.12 non trouvé")
        except FileNotFoundError:
            self.log_repair("Vérification Python 3.12", False, "Python 3.12 non installé")
        
        # Vérifier les packages critiques
        critical_packages = ["numpy", "psutil", "rich"]
        for package in critical_packages:
            try:
                result = subprocess.run(["python3.12", "-c", f"import {package}"], capture_output=True)
                if result.returncode == 0:
                    print(f"✅ Package {package} disponible")
                else:
                    self.log_repair(f"Vérification package {package}", False, f"Import failed")
            except Exception as e:
                self.log_repair(f"Vérification package {package}", False, str(e))
        
        print()
    
    def generate_repair_report(self):
        """Générer le rapport de réparation"""
        print("--- 📋 RAPPORT DE RÉPARATION ---")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Répertoire: {self.project_root}")
        print()
        
        print(f"✅ Réparations effectuées: {len(self.repairs_done)}")
        for repair in self.repairs_done:
            print(f"   • {repair}")
        
        if self.errors_found:
            print(f"❌ Erreurs rencontrées: {len(self.errors_found)}")
            for error in self.errors_found:
                print(f"   • {error}")
        else:
            print("🎉 Aucune erreur rencontrée!")
        
        print()
        
        # Recommandations
        if len(self.errors_found) == 0:
            print("🚀 Système entièrement réparé!")
            print("💡 Prochaines étapes recommandées:")
            print("   • just health - Vérifier l'état de santé")
            print("   • just sync - Synchroniser avec GitHub")
            print("   • just benchmark - Tester les performances")
        else:
            print("⚠️ Actions manuelles requises:")
            print("   • Consulter les erreurs ci-dessus")
            print("   • Exécuter les corrections manuellement")
            print("   • Relancer la réparation si nécessaire")
    
    # Méthodes de création de fichiers
    def _create_windsurf_rules(self, file_path):
        """Créer le fichier .windsurfrules par défaut"""
        content = '''# ⚡ SLASH COMMAND DISPATCHER
commands:
  - trigger: "/réparateur"
    action: "Exécuter 'just fix' (lance self_repair.py) pour restaurer l'intégrité du système."
  
  - trigger: "/ingest"
    action: "Passer en mode Ingestion de compétences : analyser le texte/lien fourni, catégoriser, et lancer skill_ingest.py."
  
  - trigger: "/santé"
    action: "Exécuter 'just health' (lance check_system.py) et afficher le rapport de diagnostic."
  
  - trigger: "/sync"
    action: "Lancer le protocole de sauvegarde totale vers GitHub (sentinel.py)."
  
  - trigger: "/dash"
    action: "Lancer ou rafraîchir le dashboard 'windsurf_monitor.py'."
  
  - trigger: "/clean"
    action: "Exécuter 'just cleanup' pour purger les fichiers temporaires, logs et cache."

# Force Cascade à ne PAS discuter quand un / est utilisé : Exécution directe.
rule_on_commands: "Dès qu'un message commence par '/', n'affiche aucun blabla technique. Exécute la commande et donne uniquement le résultat (Succès/Échec)."

# IDENTITY: Senior Fullstack AI Architect & UX Lead
- **Tone**: Direct, professional, Ethic Hacker / Tech Lead style. No fluff.
- **Expertise**: Apple M1 (arm64) optimization, Unified Memory, Low-level TUI/UX.
- **Stack**: Python (FastAPI/NumPy), Node.js (Next.js), PyTorch, Metal Shaders.

# CORE RESPONSE RULES:
1. **Code First**: Provide high-performance, vectorized (NumPy) code snippets immediately.
2. **Visuals**: Use Braille Unicode, TrueColor (24-bit) ANSI, and structured lists.
3. **M1 Native**: Always prioritize arm64 compatibility and Accelerate framework.
4. **Memory Management**: Refer to the 'windsurf/memory/' structure for context.
5. **Format**: No technical summaries unless requested. Use LaTeX for complex math.
'''
        file_path.write_text(content)
    
    def _create_identity_file(self, file_path):
        """Créer le fichier identity.md par défaut"""
        content = '''# Identity & Project Context
- **Role**: Senior Fullstack AI Architect & UX Lead
- **Stack**: Python (FastAPI/NumPy), Node.js (Next.js), PyTorch, Metal Shaders
- **Environment**: Apple M1 (arm64) with Python 3.12
- **GitHub Repo**: https://github.com/thra8/my-cascade-brain
- **Specialization**: M1 Native Optimization, Terminal Graphics, AI Agents

## System Configuration
### Hardware
- **CPU**: Apple M1 (8 cores: 4 P-cores + 4 E-cores)
- **Memory**: 8GB unified memory
- **GPU**: 8-core GPU (up to 2.6 TFLOPS)
- **Neural Engine**: 16-core (up to 11 TOPS)

### Performance Targets
- **3D Rendering**: 60 FPS (16ms frame budget)
- **Color Processing**: <5ms per calculation
- **Stack Health**: <100ms response time
- **Memory Usage**: <4GB for stack operations

## 🛠️ Stratégie de Persistance Totale

### Niveaux de Sécurité
| Niveau | Emplacement | Rôle |
|--------|-------------|------|
| **Global** | Saved Info | Définit qui tu es pour Gemini (Architecte, Ton, Stack) |
| **Local** | .windsurfrules | Force Cascade à charger les scripts et la mémoire au lancement |
| **Cloud** | GitHub Repository | Ton "Cerveau de secours". Si tu changes de Mac, tout ton savoir est là |

### 🚀 Action Immédiate pour ton Projet
Pour que Cascade ne perde rien entre deux fenêtres, assure-toi que ton fichier Inputwindsurf contient bien la commande de démarrage :

> "Au lancement, exécute ./windsurf/scripts/sync.sh load pour réveiller ma mémoire."

Tout est maintenant prêt.
'''
        file_path.write_text(content)
    
    def _create_skills_file(self, file_path):
        """Créer le fichier skills.md par défaut"""
        content = '''# Expert Skills Vault - Cascade AI System

## 🧠 Core Architecture
### M1 Native Optimization
- **Pattern**: NumPy vectorization instead of pixel loops
- **Performance**: 68.8 FPS achieved with 16ms frame budget
- **Braille Unicode**: U+2800 mapping for 2x8 resolution
- **Double Buffering**: Prevents flicker in animations

### Rendering Pipeline
- **No Pixel Loops**: Strict NumPy broadcasting
- **Frame Budget**: 16ms for 60 FPS target
- **Memory Pooling**: Reuse buffers to avoid allocations
- **Thermal Management**: Monitor M1 temperature

---

## 🚀 Skills Ingested

*Les nouvelles compétences seront ajoutées ici via le système d'ingestion automatique.*

'''
        file_path.write_text(content)
    
    def _create_context_file(self, file_path):
        """Créer le fichier context_snapshot.md par défaut"""
        content = f'''# Context Snapshot - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}

## 🎯 Current Objective
System initialization and setup completion for Cascade Architect.

## 🛠️ Technical Stack
- **Python**: 3.12.13 (optimized for M1)
- **Environment**: Virtual environment with ARM64 packages
- **Dependencies**: NumPy, Metal, PyObjC, Rich, Textual
- **Framework**: Apple M1 Metal for GPU acceleration

## 📁 Project Structure
```
cascade-brain/
├── windsurf/
│   ├── memory/
│   │   ├── identity.md ✓
│   │   ├── skills.md ✓
│   │   └── context_snapshot.md ✓
│   ├── scripts/
│   │   ├── skill_ingest.py ✓
│   │   ├── sentinel.py ✓
│   │   └── check_system.py ✓
│   └── .windsurfrules ✓
├── venv/ ✓
├── requirements.txt ✓
├── justfile ✓
└── COMMANDES_RAPIDES.md ✓
```

## 🎯 Next Steps
1. Validate system health with `/santé`
2. Test performance with benchmarks
3. Begin skill ingestion workflow
4. Establish regular sync schedule

---
*Last updated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
'''
        file_path.write_text(content)
    
    def _create_requirements_file(self, file_path):
        """Créer le fichier requirements.txt par défaut"""
        content = '''# Cascade Architect Requirements - Python 3.12
# Optimized for Apple M1 (arm64) with performance enhancements

# Core Dependencies
numpy>=2.4.3
psutil>=7.2.2
rich>=14.3.3
textual>=8.1.1

# Apple M1 Metal Framework
pyobjc-framework-Metal>=12.1
pyobjc-framework-Cocoa>=12.1

# Development Tools
typing-extensions>=4.15.0
markdown-it-py>=4.0.0
mdit-py-plugins>=0.5.0
pygments>=2.19.2

# Performance Monitoring
platformdirs>=4.9.4
'''
        file_path.write_text(content)
    
    def _create_python_version_file(self, file_path):
        """Créer le fichier .python-version par défaut"""
        file_path.write_text("3.12\n")
    
    def _create_justfile(self, file_path):
        """Créer le justfile par défaut"""
        content = '''# Cascade Architect Justfile - Python 3.12 Optimized

# Vérifier l'état de santé complet du système
health:
    source venv/bin/activate && python3 windsurf/scripts/check_system.py

# Synchroniser la mémoire avec GitHub
sync:
    source venv/bin/activate && python3 windsurf/scripts/sentinel.py

# Lancer le dashboard de monitoring
monitor:
    source venv/bin/activate && python3 windsurf_monitor.py

# Nettoyer les fichiers temporaires
cleanup:
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name ".DS_Store" -delete

# Réparation système
fix:
    source venv/bin/activate && python3 windsurf/scripts/self_repair.py

# Installation complète
install:
    @echo "🐍 Installation Python 3.12..."
    brew install python@3.12
    @echo "📦 Création environnement virtuel..."
    python3.12 -m venv venv
    @echo "📦 Installation dépendances..."
    source venv/bin/activate && pip install -r requirements.txt
    @echo "✅ Installation terminée"

# Aide
help:
    @echo "Commandes disponibles:"
    @echo "  just health    - Vérifier l'état de santé"
    @echo "  just sync      - Synchroniser GitHub"
    @echo "  just monitor  - Lancer dashboard"
    @echo "  just cleanup  - Nettoyer fichiers temporaires"
    @echo "  just fix      - Réparer système"
    @echo "  just install  - Installation complète"
'''
        file_path.write_text(content)
    
    def run_repair(self):
        """Lancer le processus de réparation complet"""
        print("--- 🔧 CASCADE ARCHITECT SELF-REPAIR ---")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Répertoire: {self.project_root}")
        print()
        
        # Étapes de réparation
        self.check_and_create_directories()
        self.check_and_create_files()
        self.fix_permissions()
        self.fix_git_repository()
        self.fix_virtual_environment()
        self.clean_temporary_files()
        self.validate_system_integrity()
        
        # Rapport final
        self.generate_repair_report()


def main():
    """Point d'entrée principal"""
    repair = CascadeRepair()
    repair.run_repair()


if __name__ == "__main__":
    main()
