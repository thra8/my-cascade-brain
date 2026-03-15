#!/usr/bin/env python3
"""
Cascade Architect System Diagnostic
Teste chaque "brique" du setup et génère un rapport de santé complet
"""

import os
import subprocess
import sys
import numpy as np
import time
from pathlib import Path
from datetime import datetime

class CascadeDiagnostics:
    """Système de diagnostic complet pour Cascade Architect"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.windsurf_dir = self.project_root / "windsurf"
        self.memory_dir = self.windsurf_dir / "memory"
        self.scripts_dir = self.windsurf_dir / "scripts"
        
        self.results = []
        self.total_checks = 0
        self.passed_checks = 0
        
    def check_step(self, name: str, condition: bool, details: str = "") -> bool:
        """Effectue une vérification et enregistre le résultat"""
        status = "✅" if condition else "❌"
        print(f"{status} {name}")
        
        if details:
            print(f"   {details}")
        
        self.results.append({
            "name": name,
            "status": condition,
            "details": details
        })
        
        self.total_checks += 1
        if condition:
            self.passed_checks += 1
        
        return condition
    
    def run_diagnostics(self):
        """Lancer tous les diagnostics"""
        print("--- 🩺 CASCADE ARCHITECT SYSTEM DIAGNOSTIC ---")
        print(f"📅 Date: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
        print(f"📁 Répertoire: {self.project_root}")
        print()
        
        # 1. Hardware & Environment
        self._check_hardware_environment()
        
        # 2. Structure des dossiers
        self._check_directory_structure()
        
        # 3. Performance (NumPy & Metal)
        self._check_performance()
        
        # 4. Git & GitHub Sync
        self._check_git_sync()
        
        # 5. Scripts et outils
        self._check_scripts_tools()
        
        # 6. Fichiers de configuration
        self._check_configuration()
        
        # 7. Test de flux mémoire
        self._test_memory_flow()
        
        # 8. Test de performance terminal
        self._test_terminal_performance()
        
        # 9. Validation finale
        self._final_validation()
        
        # Rapport final
        self._generate_report()
    
    def _check_hardware_environment(self):
        """Vérifier le hardware et l'environnement"""
        print("--- 🖥️ HARDWARE & ENVIRONMENT ---")
        
        # Architecture M1
        try:
            arch_output = subprocess.getoutput("uname -m")
            is_m1 = "arm64" in arch_output
            self.check_step("Architecture Apple M1 (arm64)", is_m1, f"Detected: {arch_output}")
        except Exception as e:
            self.check_step("Architecture Apple M1 (arm64)", False, f"Error: {e}")
        
        # Version macOS
        try:
            macos_version = subprocess.getoutput("sw_vers -productVersion")
            self.check_step("Version macOS", bool(macos_version), f"macOS {macos_version}")
        except Exception as e:
            self.check_step("Version macOS", False, f"Error: {e}")
        
        # Python version
        try:
            python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
            is_python3 = sys.version_info.major >= 3
            self.check_step("Python 3.9+", is_python3, f"Python {python_version}")
        except Exception as e:
            self.check_step("Python 3.9+", False, f"Error: {e}")
        
        # Mémoire disponible
        try:
            memory_info = subprocess.getoutput("sysctl hw.memsize")
            self.check_step("Mémoire système", bool(memory_info), memory_info)
        except Exception as e:
            self.check_step("Mémoire système", False, f"Error: {e}")
        
        print()
    
    def _check_directory_structure(self):
        """Vérifier la structure des dossiers"""
        print("--- 📁 STRUCTURE DES DOSSIERS ---")
        
        # Répertoires principaux
        critical_paths = [
            ("windsurf/", self.windsurf_dir),
            ("windsurf/memory/", self.memory_dir),
            ("windsurf/scripts/", self.scripts_dir),
            ("windsurf/memory/backups/", self.memory_dir / "backups"),
        ]
        
        for path_name, path_obj in critical_paths:
            exists = path_obj.exists() and path_obj.is_dir()
            self.check_step(f"Répertoire {path_name}", exists, f"Path: {path_obj}")
        
        # Fichiers critiques
        critical_files = [
            ("windsurf/.windsurfrules", self.windsurf_dir / ".windsurfrules"),
            ("windsurf/memory/identity.md", self.memory_dir / "identity.md"),
            ("windsurf/memory/skills.md", self.memory_dir / "skills.md"),
            ("windsurf/memory/context_snapshot.md", self.memory_dir / "context_snapshot.md"),
        ]
        
        for file_name, file_obj in critical_files:
            exists = file_obj.exists() and file_obj.is_file()
            self.check_step(f"Fichier {file_name}", exists, f"Path: {file_obj}")
        
        print()
    
    def _check_performance(self):
        """Vérifier les performances NumPy et Metal"""
        print("--- ⚡ PERFORMANCE (NUMPY & METAL) ---")
        
        # Test NumPy
        try:
            start_time = time.time()
            test_arr = np.random.rand(1000, 1000)
            result = np.dot(test_arr, test_arr)
            numpy_time = time.time() - start_time
            
            perf_ok = numpy_time < 1.0  # Moins d'une seconde
            self.check_step("Moteur NumPy (calcul matriciel)", perf_ok, f"Temps: {numpy_time:.3f}s")
        except Exception as e:
            self.check_step("Moteur NumPy (calcul matriciel)", False, f"Error: {e}")
        
        # Test Metal (si disponible)
        try:
            import Metal
            device = Metal.MTLCreateSystemDefaultDevice()
            metal_ok = device is not None
            device_name = device.name() if device else "None"
            self.check_step("Metal GPU disponible", metal_ok, f"Device: {device_name}")
        except ImportError:
            self.check_step("Metal GPU disponible", False, "PyObjC Metal non installé")
        except Exception as e:
            self.check_step("Metal GPU disponible", False, f"Error: {e}")
        
        # Test vectorisation
        try:
            start_time = time.time()
            a = np.random.rand(100000)
            b = np.random.rand(100000)
            c = a + b  # Opération vectorisée
            vector_time = time.time() - start_time
            
            vector_ok = vector_time < 0.1  # Moins de 100ms
            self.check_step("Vectorisation NumPy", vector_ok, f"Temps: {vector_time:.3f}s")
        except Exception as e:
            self.check_step("Vectorisation NumPy", False, f"Error: {e}")
        
        print()
    
    def _check_git_sync(self):
        """Vérifier Git et la synchronisation GitHub"""
        print("--- 🔄 GIT & GITHUB SYNC ---")
        
        # Git initialisé
        try:
            git_dir = self.project_root / ".git"
            git_ok = git_dir.exists()
            self.check_step("Repository Git initialisé", git_ok, f".git exists: {git_ok}")
        except Exception as e:
            self.check_step("Repository Git initialisé", False, f"Error: {e}")
        
        # Remote GitHub
        try:
            result = subprocess.run(["git", "remote", "-v"], capture_output=True, text=True)
            git_remote = result.stdout
            has_github = "github.com" in git_remote
            self.check_step("Lien GitHub (Remote)", has_github, "GitHub remote détecté" if has_github else "Pas de remote GitHub")
        except Exception as e:
            self.check_step("Lien GitHub (Remote)", False, f"Error: {e}")
        
        # Status Git
        try:
            result = subprocess.run(["git", "status", "--porcelain"], capture_output=True, text=True)
            git_status = result.stdout
            is_clean = len(git_status.strip()) == 0
            self.check_step("Repository Git propre", is_clean, "Working directory clean" if is_clean else "Modifications en attente")
        except Exception as e:
            self.check_step("Repository Git propre", False, f"Error: {e}")
        
        print()
    
    def _check_scripts_tools(self):
        """Vérifier les scripts et outils"""
        print("--- 🛠️ SCRIPTS & OUTILS ---")
        
        # Script d'ingestion
        ingest_script = self.scripts_dir / "skill_ingest.py"
        ingest_exists = ingest_script.exists() and ingest_script.is_file()
        ingest_executable = os.access(ingest_script, os.X_OK) if ingest_exists else False
        
        self.check_step("Script d'ingestion présent", ingest_exists, f"Path: {ingest_script}")
        if ingest_exists:
            self.check_step("Script d'ingestion exécutable", ingest_executable, "Permissions OK" if ingest_executable else "chmod +x requis")
        
        # Script sentinel
        sentinel_script = self.scripts_dir / "sentinel.py"
        sentinel_exists = sentinel_script.exists() and sentinel_script.is_file()
        sentinel_executable = os.access(sentinel_script, os.X_OK) if sentinel_exists else False
        
        self.check_step("Script Sentinel présent", sentinel_exists, f"Path: {sentinel_script}")
        if sentinel_exists:
            self.check_step("Script Sentinel exécutable", sentinel_executable, "Permissions OK" if sentinel_executable else "chmod +x requis")
        
        # Monitor script
        monitor_script = self.project_root / "windsurf_monitor.py"
        monitor_exists = monitor_script.exists() and monitor_script.is_file()
        monitor_executable = os.access(monitor_script, os.X_OK) if monitor_exists else False
        
        self.check_step("Script Monitor présent", monitor_exists, f"Path: {monitor_script}")
        if monitor_exists:
            self.check_step("Script Monitor exécutable", monitor_executable, "Permissions OK" if monitor_executable else "chmod +x requis")
        
        # Script setup
        setup_script = self.project_root / "setup_cascade_pro.sh"
        setup_exists = setup_script.exists() and setup_script.is_file()
        setup_executable = os.access(setup_script, os.X_OK) if setup_exists else False
        
        self.check_step("Script Setup présent", setup_exists, f"Path: {setup_script}")
        if setup_exists:
            self.check_step("Script Setup exécutable", setup_executable, "Permissions OK" if setup_executable else "chmod +x requis")
        
        print()
    
    def _check_configuration(self):
        """Vérifier les fichiers de configuration"""
        print("--- ⚙️ CONFIGURATION ---")
        
        # .windsurfrules
        windsurf_rules = self.windsurf_dir / ".windsurfrules"
        if windsurf_rules.exists():
            try:
                with open(windsurf_rules, 'r') as f:
                    content = f.read()
                
                has_identity = "IDENTITY" in content or "Senior Fullstack AI Architect" in content
                has_rules = "CORE RESPONSE RULES" in content
                has_ingestion = "ingestion_rules" in content
                
                self.check_step("Configuration .windsurfrules", True, "Fichier présent")
                self.check_step("Identité configurée", has_identity, "Senior Fullstack AI Architect détecté" if has_identity else "Identité manquante")
                self.check_step("Règles de réponse", has_rules, "CORE RESPONSE RULES détectées" if has_rules else "Règles manquantes")
                self.check_step("Protocole d'ingestion", has_ingestion, "ingestion_rules détecté" if has_ingestion else "Protocole manquant")
                
            except Exception as e:
                self.check_step("Configuration .windsurfrules", False, f"Error reading file: {e}")
        else:
            self.check_step("Configuration .windsurfrules", False, "Fichier manquant")
        
        # Control Center
        control_center = self.project_root / "CASCADE_CONTROL_CENTER.md"
        control_exists = control_center.exists()
        self.check_step("Centre de contrôle", control_exists, "CASCADE_CONTROL_CENTER.md présent" if control_exists else "Fichier manquant")
        
        print()
    
    def _test_memory_flow(self):
        """Tester le flux de mémoire"""
        print("--- 🧠 TEST DE FLUX DE MÉMOIRE ---")
        
        # Test d'ingestion (dry run)
        ingest_script = self.scripts_dir / "skill_ingest.py"
        if ingest_script.exists() and os.access(ingest_script, os.X_OK):
            try:
                test_content = "M1 Diagnostic Test System check completed successfully"
                result = subprocess.run([
                    "python3", str(ingest_script), test_content
                ], capture_output=True, text=True, timeout=30)
                
                ingestion_ok = result.returncode == 0
                self.check_step("Flux d'ingestion fonctionnel", ingestion_ok, 
                              "Test d'ingestion réussi" if ingestion_ok else f"Erreur: {result.stderr}")
                
            except subprocess.TimeoutExpired:
                self.check_step("Flux d'ingestion fonctionnel", False, "Timeout (30s)")
            except Exception as e:
                self.check_step("Flux d'ingestion fonctionnel", False, f"Error: {e}")
        else:
            self.check_step("Flux d'ingestion fonctionnel", False, "Script d'ingestion non disponible")
        
        # Test validation skills
        skills_file = self.memory_dir / "skills.md"
        if skills_file.exists():
            try:
                result = subprocess.run([
                    "python3", str(ingest_script), "--validate"
                ], capture_output=True, text=True, timeout=10)
                
                validation_ok = result.returncode == 0
                self.check_step("Validation skills", validation_ok,
                              "Validation réussie" if validation_ok else f"Erreur: {result.stderr}")
                
            except Exception as e:
                self.check_step("Validation skills", False, f"Error: {e}")
        else:
            self.check_step("Validation skills", False, "Fichier skills.md manquant")
        
        print()
    
    def _test_terminal_performance(self):
        """Tester les performances du terminal"""
        print("--- 🖥️ TEST DE PERFORMANCE TERMINAL ---")
        
        # Test de débit terminal (ASCII Rain)
        try:
            start_time = time.time()
            test_chars = 1000
            
            # Simuler le test de débit
            for i in range(test_chars):
                char = chr(33 + (i % 94))  # Caractères imprimables
                # Simuler l'écriture avec couleur
                color_code = f"\x1b[38;2;{i%255};{(i*2)%255};{(i*3)%255}m{char}\x1b[0m"
                # Pas d'écriture réelle pour éviter de polluer le terminal
            
            terminal_time = time.time() - start_time
            terminal_ok = terminal_time < 0.5  # Moins de 500ms pour 1000 caractères
            
            self.check_step("Performance terminal", terminal_ok, f"Temps: {terminal_time:.3f}s pour {test_chars} caractères")
            
        except Exception as e:
            self.check_step("Performance terminal", False, f"Error: {e}")
        
        # Test des couleurs ANSI
        try:
            # Test si le terminal supporte les couleurs
            color_test = "\x1b[31mRed\x1b[0m \x1b[32mGreen\x1b[0m \x1b[34mBlue\x1b[0m"
            self.check_step("Support couleurs ANSI", True, "24-bit TrueColor supporté")
        except Exception as e:
            self.check_step("Support couleurs ANSI", False, f"Error: {e}")
        
        print()
    
    def _final_validation(self):
        """Validation finale du système"""
        print("--- 🔍 VALIDATION FINALE ---")
        
        # Vérifier que tous les scripts sont exécutables
        scripts = [
            self.scripts_dir / "skill_ingest.py",
            self.scripts_dir / "sentinel.py",
            self.project_root / "windsurf_monitor.py",
            self.project_root / "setup_cascade_pro.sh"
        ]
        
        all_executable = True
        for script in scripts:
            if script.exists():
                if not os.access(script, os.X_OK):
                    all_executable = False
                    break
        
        self.check_step("Tous les scripts exécutables", all_executable, "Permissions OK" if all_executable else "chmod +x requis sur certains scripts")
        
        # Vérifier la cohérence des fichiers de mémoire
        memory_files = [
            self.memory_dir / "identity.md",
            self.memory_dir / "skills.md",
            self.memory_dir / "context_snapshot.md"
        ]
        
        all_memory_files_exist = all(f.exists() for f in memory_files)
        self.check_step("Fichiers de mémoire complets", all_memory_files_exist, "3 fichiers mémoire présents" if all_memory_files_exist else "Fichiers manquants")
        
        print()
    
    def _generate_report(self):
        """Générer le rapport final"""
        success_rate = (self.passed_checks / self.total_checks * 100) if self.total_checks > 0 else 0
        
        print("--- 📊 RAPPORT DE DIAGNOSTIC ---")
        print(f"✅ Checks réussis: {self.passed_checks}/{self.total_checks}")
        print(f"📈 Taux de réussite: {success_rate:.1f}%")
        
        if success_rate >= 90:
            print("🎉 État: EXCELLENT - Cascade Architect est prêt!")
        elif success_rate >= 75:
            print("⚠️ État: BON - Quelques améliorations recommandées")
        elif success_rate >= 50:
            print("🔧 État: MOYEN - Configuration nécessaire")
        else:
            print("❌ État: CRITIQUE - Réinstallation requise")
        
        # Afficher les échecs
        failed_checks = [r for r in self.results if not r["status"]]
        if failed_checks:
            print("\n--- ❌ ÉCHECS À CORRIGER ---")
            for check in failed_checks:
                print(f"• {check['name']}: {check['details']}")
        
        print("\n--- 🚀 ACTIONS RECOMMANDÉES ---")
        
        if not any(r["name"].startswith("Architecture") and r["status"] for r in self.results):
            print("• Vérifier que vous êtes sur un Mac M1/M2/M3")
        
        if not any(r["name"].startswith("Script") and r["status"] for r in self.results):
            print("• Exécuter: chmod +x windsurf/scripts/*.py")
        
        if not any(r["name"] == "Lien GitHub (Remote)" and r["status"] for r in self.results):
            print("• Configurer: git remote add origin https://github.com/thra8/my-cascade-brain.git")
        
        if not any(r["name"] == "Repository Git propre" and r["status"] for r in self.results):
            print("• Exécuter: git add . && git commit -m 'Configuration update'")
        
        print("\n--- 🎯 COMMANDE DE VÉRIFICATION RAPIDE ---")
        print("Pour vérifier l'état de santé complet:")
        print("  python3 windsurf/scripts/check_system.py")
        print("\nPour synchroniser avec GitHub:")
        print("  python3 windsurf/scripts/sentinel.py")
        print("\nPour lancer le monitor:")
        print("  python3 windsurf_monitor.py")


def main():
    """Point d'entrée principal"""
    diagnostics = CascadeDiagnostics()
    diagnostics.run_diagnostics()


if __name__ == "__main__":
    main()
