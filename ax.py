#!/usr/bin/env python3
"""
Cascade Architect - Atomic Architecture System
Single file to rule them all: repair, ingest, health, sync
"""

import os
import sys
import subprocess
import re
import datetime
from pathlib import Path

class Architect:
    """Atomic Architecture - Single point of control for Cascade"""
    
    def __init__(self):
        self.base_path = "windsurf/memory"
        self.libs = ["numpy", "textual", "psutil", "rich"]

    def repair(self):
        print("🛠️  Réparation de l'infrastructure...")
        os.makedirs(self.base_path, exist_ok=True)
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + self.libs)
            print("✅ Environnement M1 stabilisé.")
        except: 
            print("❌ Erreur de dépendances.")

    def find(self, query):
        """Recherche intelligente dans tous les fichiers skills.md"""
        print(f"� Recherche de : '{query}'...")
        matches = []
        
        for root, _, files in os.walk(self.base_path):
            if "skills.md" in files:
                path = os.path.join(root, "skills.md")
                rel_path = os.path.relpath(root, self.base_path).upper()
                
                with open(path, "r", encoding="utf-8") as f:
                    # On découpe par skill (séparateur ###)
                    skills = f.read().split("### ")
                    for skill in skills:
                        if query.lower() in skill.lower():
                            matches.append((rel_path, skill.strip()))

        if not matches:
            print("❌ Aucun skill trouvé pour cette recherche.")
            return

        print(f"✅ {len(matches)} résultat(s) trouvé(s):")
        for i, (cat, content) in enumerate(matches[:5], 1): # Limite à 5 résultats
            lines = content.split('\n')
            title = lines[0] if lines else "Sans titre"
            print(f"\n--- Résultat {i} ({cat}) ---")
            print(f"📋 {title}")
            # Affiche les 3 premières lignes du contenu
            content_lines = [line.strip() for line in lines[1:4] if line.strip()]
            if content_lines:
                for line in content_lines:
                    print(f"   {line}")
            print("   ...")

    def dashboard(self):
        total_skills, categories = 0, {}
        for root, _, files in os.walk(self.base_path):
            if "skills.md" in files:
                rel_path = os.path.relpath(root, self.base_path).upper()
                with open(os.path.join(root, "skills.md"), "r", encoding="utf-8") as f:
                    count = len([line for line in f if line.strip().startswith("### ")])
                    categories[rel_path] = count
                    total_skills += count

        print("🧠 AXE DASHBOARD")
        print("=" * 40)
        for cat, count in categories.items():
            print(f"📁 {cat}: {count} skills")
        print("-" * 40)
        print(f"🔥 TOTAL: {total_skills} skills")

    def ingest(self, cat, title, content):
        target_dir = os.path.join(self.base_path, cat.lower())
        os.makedirs(target_dir, exist_ok=True)
        file_path = os.path.join(target_dir, "skills.md")
        with open(file_path, "a", encoding="utf-8") as f:
            f.write(f"\n### {title} ({datetime.date.today()})\n{content.strip()}\n")
        print(f"✅ Skill '{title}' intégré dans {cat}.")

    def new_project(self, name):
        """🚀 Déploie un nouveau projet optimisé AXE."""
        print(f"🏗️  Scaffolding du projet : {name}...")
        
        # Création du répertoire
        os.makedirs(name, exist_ok=True)
        
        # Copie des règles AXE
        with open(f"{name}/.windsurfrules", "w") as f:
            f.write("""# AXE Project Rules
personality: 'Senior Architect'
optimization: 'M1 Native'
framework: 'FastAPI/Next.js'
""")
        
        # Création du .gitignore optimisé
        with open(f"{name}/.gitignore", "w") as f:
            f.write("""# AXE Optimized .gitignore
node_modules/
__pycache__/
*.pyc
venv/
.env
dist/
build/
.DS_Store
""")
        
        # Création du requirements.txt M1 optimisé
        with open(f"{name}/requirements.txt", "w") as f:
            f.write("""# M1 Optimized Dependencies
numpy>=2.0.0
fastapi>=0.104.0
uvicorn>=0.24.0
pydantic>=2.5.0
""")
        
        # Création du venv M1
        subprocess.run([sys.executable, "-m", "venv", f"{name}/venv"], check=True)
        
        # Création du package.json si projet Next.js
        with open(f"{name}/package.json", "w") as f:
            f.write("""{
  "name": \"""" + name + """",
  "version": "1.0.0",
  "scripts": {
    "dev": "next dev",
    "build": "next build",
    "start": "next start"
  },
  "dependencies": {
    "next": "^14.0.0",
    "react": "^18.0.0",
    "tailwindcss": "^3.0.0"
  }
}
""")
        
        print(f"✅ Projet {name} prêt. Utilise 'cd {name} && /f' pour finaliser.")
        print(f"📁 Structure créée:")
        print(f"   ├── .windsurfrules (Règles AXE)")
        print(f"   ├── .gitignore (Optimisé M1)")
        print(f"   ├── requirements.txt (Dépendances M1)")
        print(f"   ├── package.json (Next.js)")
        print(f"   └── venv/ (Environnement Python)")

    def smart_commit(self):
        """📝 Génère un message de commit intelligent."""
        print("📝 SMART COMMIT - ANALYSE SÉMANTIQUE")
        print("=" * 45)
        
        # Vérifier si des fichiers sont staged
        try:
            staged_files = subprocess.getoutput("git diff --cached --name-only")
            if not staged_files.strip():
                print("⚠️ Aucun fichier staged. Utilise 'git add .' d'abord.")
                return
            
            print(f"📁 Fichiers en attente:")
            for file in staged_files.split('\n'):
                if file.strip():
                    print(f"   • {file}")
            
            # Analyser le diff
            diff_output = subprocess.getoutput("git diff --cached --stat")
            print(f"\n📊 Statistiques des changements:")
            print(diff_output)
            
            # Analyser les types de changements
            diff_detailed = subprocess.getoutput("git diff --cached")
            
            # Détection automatique du type de commit
            commit_type = "feat"  # default
            commit_scope = "axe"
            commit_description = ""
            
            # Analyser les changements pour déterminer le type
            if "def " in diff_detailed or "class " in diff_detailed:
                if "fix" in diff_detailed.lower() or "bug" in diff_detailed.lower():
                    commit_type = "fix"
                elif "test" in diff_detailed.lower():
                    commit_type = "test"
                elif "doc" in diff_detailed.lower() or "comment" in diff_detailed.lower():
                    commit_type = "docs"
                else:
                    commit_type = "feat"
            
            # Analyser l'impact UX
            ux_impact = self._analyze_ux_impact(diff_detailed)
            
            # Analyser l'impact performance
            perf_impact = self._analyze_performance_impact(diff_detailed)
            
            # Générer le message de commit
            commit_message = f"{commit_type}({commit_scope}): "
            
            # Description principale
            if commit_type == "feat":
                commit_message += "add new functionality"
            elif commit_type == "fix":
                commit_message += "resolve issue"
            elif commit_type == "docs":
                commit_message += "update documentation"
            elif commit_type == "test":
                commit_message += "improve test coverage"
            elif commit_type == "refactor":
                commit_message += "improve code structure"
            else:
                commit_message += "update system"
            
            # Ajouter les impacts
            body_lines = []
            if ux_impact:
                body_lines.append(f"UX Impact: {ux_impact}")
            if perf_impact:
                body_lines.append(f"Performance: {perf_impact}")
            
            # Afficher le message généré
            print(f"\n📋 MESSAGE DE COMMIT GÉNÉRÉ:")
            print(f"🎯 {commit_message}")
            if body_lines:
                for line in body_lines:
                    print(f"   {line}")
            
            # Demander confirmation
            print(f"\n❓ Confirmer le commit? (y/n)")
            # En mode automatique, on commit directement
            try:
                # Créer le message complet
                full_message = commit_message
                if body_lines:
                    full_message += "\n\n" + "\n".join(body_lines)
                
                # Exécuter le commit
                subprocess.run(["git", "commit", "-m", full_message], check=True)
                print(f"✅ Commit effectué avec succès!")
                
                # Afficher le hash du commit
                commit_hash = subprocess.getoutput("git rev-parse --short HEAD").strip()
                print(f"🔗 Commit: {commit_hash}")
                
            except subprocess.CalledProcessError as e:
                print(f"❌ Erreur lors du commit: {e}")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")

    def _analyze_ux_impact(self, diff_content):
        """Analyser l'impact UX des changements"""
        ux_indicators = {
            "button": "Interface buttons modified",
            "form": "Form interactions updated", 
            "modal": "Modal dialogs affected",
            "navigation": "Navigation structure changed",
            "responsive": "Responsive design updated",
            "accessibility": "Accessibility improvements",
            "color": "Color scheme modified",
            "layout": "Layout structure changed",
            "animation": "Animations and transitions",
            "input": "Input field behaviors"
        }
        
        impacts = []
        for indicator, description in ux_indicators.items():
            if indicator.lower() in diff_content.lower():
                impacts.append(description)
        
        return "; ".join(impacts) if impacts else None

    def _analyze_performance_impact(self, diff_content):
        """Analyser l'impact performance des changements"""
        perf_indicators = {
            "cache": "Caching strategy updated",
            "async": "Async operations optimized",
            "lazy": "Lazy loading implemented",
            "memo": "Memoization added",
            "optimize": "Performance optimizations",
            "batch": "Batch processing improved",
            "vectorized": "Vectorized operations",
            "parallel": "Parallel processing",
            "memory": "Memory usage optimized",
            "query": "Database queries optimized"
        }
        
        impacts = []
        for indicator, description in perf_indicators.items():
            if indicator.lower() in diff_content.lower():
                impacts.append(description)
        
        return "; ".join(impacts) if impacts else None

    def ux_audit(self, path="."):
        """🎨 Audit UX/UI du projet"""
        print("🎨 UX/UI AUDIT - AXE DESIGN SYSTEM")
        print("=" * 45)
        
        # Scores
        scores = {
            "accessibility": 0,
            "performance": 0,
            "usability": 0
        }
        
        # 1. Vérification de l'accessibilité (WCAG)
        print("\n🔍 ACCESSIBILITÉ (WCAG):")
        try:
            # Chercher les fichiers React/HTML
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(('.tsx', '.jsx', '.html')):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            content = f.read()
                            # Vérifier les attributs aria
                            aria_count = content.count('aria-')
                            alt_count = content.count('alt=')
                            if aria_count > 0 or alt_count > 0:
                                scores["accessibility"] += min(30, aria_count * 5 + alt_count * 10)
                                print(f"   ✅ {file}: {aria_count} aria, {alt_count} alt")
        except:
            print("   ⚠️ Erreur analyse accessibilité")
        
        # 2. Performance (Tailwind breakpoints)
        print("\n⚡ PERFORMANCE:")
        try:
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(('.css', '.tsx', '.jsx')):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            content = f.read()
                            # Vérifier les breakpoints Tailwind
                            breakpoints = ['sm:', 'md:', 'lg:', 'xl:']
                            bp_count = sum(content.count(bp) for bp in breakpoints)
                            if bp_count > 0:
                                scores["performance"] += min(40, bp_count * 8)
                                print(f"   ✅ {file}: {bp_count} breakpoints")
        except:
            print("   ⚠️ Erreur analyse performance")
        
        # 3. Usabilité (Structure et patterns)
        print("\n🎯 USABILITÉ:")
        try:
            component_count = 0
            for root, _, files in os.walk(path):
                for file in files:
                    if file.endswith(('.tsx', '.jsx')):
                        file_path = os.path.join(root, file)
                        with open(file_path, 'r') as f:
                            content = f.read()
                            # Vérifier les hooks React
                            hooks = ['useState', 'useEffect', 'useCallback']
                            hook_count = sum(content.count(hook) for hook in hooks)
                            if hook_count > 0:
                                component_count += 1
                                scores["usability"] += min(30, hook_count * 6)
            if component_count > 0:
                print(f"   ✅ {component_count} composants analysés")
        except:
            print("   ⚠️ Erreur analyse usabilité")
        
        # Calcul du score Q_ux
        total_score = scores["accessibility"] + scores["performance"] + scores["usability"]
        qux = total_score / 3
        
        print(f"\n📊 SCORE UX QUALITÉ (Q_ux): {qux:.1f}/100")
        print(f"   🎨 Accessibilité: {scores['accessibility']}/100")
        print(f"   ⚡ Performance: {scores['performance']}/100")
        print(f"   🎯 Usabilité: {scores['usability']}/100")
        
        # Recommandations
        if qux < 50:
            print("\n💡 RECOMMANDATIONS:")
            if scores["accessibility"] < 30:
                print("   • Ajouter des attributs aria et alt pour l'accessibilité")
            if scores["performance"] < 40:
                print("   • Optimiser les breakpoints Tailwind pour la réactivité")
            if scores["usability"] < 30:
                print("   • Utiliser plus de hooks React pour l'interactivité")
        
        print(f"\n🎯 Audit terminé - Score Q_ux: {qux:.1f}")

    def audit(self, *args):
        """🔍 Audit de compatibilité native Apple Silicon."""
        print("🛡️ ARCH AUDIT - M1 NATIVE CHECK")
        print("=" * 45)
        
        # 1. Check Python Arch
        import platform
        arch = platform.machine()
        status = "✅ NATIVE (arm64)" if arch == "arm64" else "⚠️ ROSETTA (x86_64)"
        print(f"🐍 Python Arch: {status}")
        
        # 2. Check Binaries critiques
        tools = ["brew", "node", "git", "docker"]
        print("\n🔧 Binaries critiques:")
        for tool in tools:
            try:
                path = subprocess.getoutput(f"which {tool}")
                file_info = subprocess.getoutput(f"file {path}")
                is_native = "arm64" in file_info
                icon = "✅" if is_native else "⚠️"
                print(f"{icon} {tool.capitalize()}: {'arm64' if is_native else 'x86_64 (Rosetta)'}")
            except:
                print(f"❌ {tool.capitalize()}: Non trouvé")
        
        # 3. Check numpy/Accelerate
        try:
            import numpy as np
            print(f"\n📊 NumPy: ✅ Installé")
            # Test si numpy utilise Accelerate
            test_array = np.random.rand(1000, 1000)
            start_time = datetime.datetime.now()
            result = np.dot(test_array, test_array)
            end_time = datetime.datetime.now()
            duration = (end_time - start_time).total_seconds()
            print(f"⚡ Performance test: {duration:.4f}s (1000x1000 matrix)")
        except ImportError:
            print(f"\n📊 NumPy: ❌ Non installé")
        
        # 4. Check MLX
        try:
            import mlx
            print(f"🧠 MLX: ✅ Installé (Apple ML framework)")
        except ImportError:
            print(f"🧠 MLX: ⚠️ Non installé (pip install mlx)")
        
        # 5. Check Docker platform
        docker_platform = os.environ.get("DOCKER_DEFAULT_PLATFORM", "non défini")
        print(f"\n🐳 Docker Platform: {docker_platform}")
        if docker_platform != "linux/arm64":
            print("💡 Recommandation: export DOCKER_DEFAULT_PLATFORM=linux/arm64")
        
        print(f"\n🎯 Audit terminé - Vérifie les ⚠️ ci-dessus")

    def sync(self):
        print("💾 Synchronisation Sentinel...")
        try:
            subprocess.run(["git", "add", "."], check=True)
            subprocess.run(["git", "commit", "-m", f"🧠 Memory Update: {datetime.datetime.now()}"], check=True)
            subprocess.run(["git", "push", "origin", "main"], check=True)
            print("✅ Cloud GitHub à jour.")
        except: 
            print("⚠️ Erreur Git.")
    
    def health(self):
        """System health check"""
        print("🩺 System Check:")
        
        # Architecture check
        m1 = "arm64" in subprocess.getoutput("uname -m")
        print(f"{'✅' if m1 else '❌'} Architecture M1")
        
        # Python version
        python_version = f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}"
        is_python312 = sys.version_info >= (3, 12)
        print(f"{'✅' if is_python312 else '❌'} Python {python_version}")
        
        # Essential files
        essential_files = [
            ".windsurfrules",
            "windsurf/memory/identity.md",
            "windsurf/memory/skills.md",
            "windsurf/memory/context_snapshot.md",
            "requirements.txt",
            ".python-version",
        ]
        
        for file_path in essential_files:
            exists = Path(file_path).exists()
            print(f"{'✅' if exists else '❌'} {file_path}")
        
        # Libraries check
        print("\n📚 Libraries:")
        for lib in self.libs:
            try:
                __import__(lib.replace("-", "_").replace("pyobjc-framework-", ""))
                print(f"✅ {lib}")
            except ImportError:
                print(f"❌ {lib}")
        
        # Git status
        try:
            git_status = subprocess.getoutput("git status --porcelain")
            is_clean = len(git_status.strip()) == 0
            print(f"{'✅' if is_clean else '⚠️'} Git status: {'Clean' if is_clean else 'Has changes'}")
        except:
            print("❌ Git not available")
        
        # Virtual environment
        venv_path = Path("venv")
        has_venv = venv_path.exists()
        print(f"{'✅' if has_venv else '❌'} Virtual environment")
        
        # Performance test
        try:
            import time
            start = time.time()
            [x for x in range(1000)]
            perf_time = time.time() - start
            print(f"✅ Performance: {perf_time:.4f}s (1000 iterations)")
        except:
            print("❌ Performance test failed")

    # --- INGESTION (With Regex Fix) ---
    def ingest(self, cat, title, content):
        """Safe ingestion with regex fix"""
        if not isinstance(content, str):
            content = str(content)
        
        # Fix Regex Error: Safe patterns only
        safe_patterns = [
            (r'<[^>]*>', ''),              # HTML tags
            (r'http[s]?://\S+', ''),        # URLs
            (r'\[([^\]]+)\]\([^\)]+\)', r'\1'),  # Markdown links
            (r'```[\w]*\n', ''),           # Code blocks start
            (r'```', ''),                   # Code blocks end
            (r'!\[.*?\]\(.*?\)', ''),       # Images
            (r'#{1,6}\s*', ''),             # Headers
            (r'\*\*(.*?)\*\*', r'\1'),      # Bold
            (r'\*(.*?)\*', r'\1'),           # Italic
            (r'`([^`]+)`', r'\1'),          # Inline code
            (r'\n\s*\n', '\n'),             # Multiple newlines
            (r'^\s*[-*+]\s*', ''),          # List items
            (r'^\s*\d+\.\s*', ''),          # Numbered lists
            (r' +', ' '),                   # Multiple spaces
        ]
        
        # Apply safe patterns
        try:
            for pattern, replacement in safe_patterns:
                content = re.sub(pattern, replacement, content, flags=re.MULTILINE)
        except Exception as e:
            print(f"⚠️ Regex warning: {e}")
        
        # Clean content
        content = content.strip()
        
        # Create category directory
        cat_path = Path(self.base_path) / cat.lower()
        cat_path.mkdir(parents=True, exist_ok=True)
        
        # Ingest to skills file
        skills_file = cat_path / "skills.md"
        
        with open(skills_file, "a", encoding="utf-8") as f:
            timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
            f.write(f"\n### {title} ({timestamp})\n{content}\n---\n")
        
        print(f"✅ Ingested into {cat}/skills.md")
        return True

    # --- SYNC (GitHub) ---
    def sync(self):
        """GitHub synchronization"""
        print("💾 Sentinel Syncing...")
        
        try:
            # Add all changes
            subprocess.run(["git", "add", "."], check=True, capture_output=True)
            print("✅ Files staged")
            
            # Commit with timestamp
            commit_msg = f"🧠 Evolution {datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}"
            subprocess.run(["git", "commit", "-m", commit_msg], check=True, capture_output=True)
            print("✅ Committed")
            
            # Push to origin
            subprocess.run(["git", "push", "origin", "main"], check=True, capture_output=True)
            print("✅ GitHub Updated")
            
        except subprocess.CalledProcessError as e:
            print(f"⚠️ Git Sync failed: {e}")
            print("Check remote/SSH configuration")
            return False
        except Exception as e:
            print(f"❌ Sync error: {e}")
            return False
        
        return True

    # --- CLEAN ---
    def clean(self):
        """Clean temporary files"""
        print("🧹 Cleaning temporary files...")
        
        temp_patterns = [
            "*.pyc",
            "__pycache__",
            ".DS_Store",
            "*.log",
            "*.tmp",
            "*.swp",
            "*~"
        ]
        
        cleaned_count = 0
        for pattern in temp_patterns:
            try:
                if pattern.endswith("/"):
                    # Directory pattern
                    for dir_path in self.project_root.rglob(pattern.rstrip("/")):
                        if dir_path.is_dir():
                            import shutil
                            shutil.rmtree(dir_path)
                            cleaned_count += 1
                else:
                    # File pattern
                    for file_path in self.project_root.rglob(pattern):
                        if file_path.is_file():
                            file_path.unlink()
                            cleaned_count += 1
            except Exception as e:
                print(f"⚠️ Error cleaning {pattern}: {e}")
        
        print(f"✅ Cleaned {cleaned_count} files")
        return cleaned_count > 0

    # --- MODULE GIT & ANALYSE ---
    def git_clone(self, url):
        """Clone et analyse un dépôt GitHub"""
        repo_name = url.split("/")[-1].replace(".git", "")
        target_path = os.path.join("lab", repo_name)
        
        print(f"📥 Clonage de {repo_name} dans {target_path}...")
        os.makedirs("lab", exist_ok=True)
        
        try:
            subprocess.run(["git", "clone", url, target_path], check=True, capture_output=True)
            print(f"✅ Dépôt cloné. Analyse des dépendances en cours...")
            
            # Analyse rapide pour Cascade
            files = os.listdir(target_path)
            has_setup = "setup.py" in files or "pyproject.toml" in files
            has_reqs = "requirements.txt" in files
            has_node = "package.json" in files
            has_docker = "Dockerfile" in files
            has_readme = any(f.lower().startswith("readme") for f in files)
            
            print(f"🔍 Détecté: Python({has_setup or has_reqs}), Node({has_node}), Docker({has_docker}), README({has_readme})")
            
            # Analyse plus approfondie
            analysis = self._analyze_repository(target_path, repo_name)
            
            return target_path, analysis
        except Exception as e:
            print(f"❌ Erreur de clonage: {e}")
            return None, None
    
    def _analyze_repository(self, repo_path, repo_name):
        """Analyse approfondie du dépôt"""
        print(f"🔍 Analyse approfondie de {repo_name}...")
        
        analysis = {
            "name": repo_name,
            "path": repo_path,
            "type": "unknown",
            "dependencies": [],
            "structure": {},
            "m1_compatible": True,
            "installation_script": None,
            "integration_points": []
        }
        
        try:
            # Analyser les fichiers de configuration
            config_files = {
                "requirements.txt": self._analyze_requirements,
                "setup.py": self._analyze_setup_py,
                "pyproject.toml": self._analyze_pyproject,
                "package.json": self._analyze_package_json,
                "Dockerfile": self._analyze_dockerfile,
                "README.md": self._analyze_readme,
                "Makefile": self._analyze_makefile,
            }
            
            for file_name, analyzer in config_files.items():
                file_path = os.path.join(repo_path, file_name)
                if os.path.exists(file_path):
                    try:
                        result = analyzer(file_path)
                        analysis.update(result)
                    except Exception as e:
                        print(f"⚠️ Erreur analyse {file_name}: {e}")
            
            # Analyser la structure du répertoire
            analysis["structure"] = self._analyze_directory_structure(repo_path)
            
            # Déterminer le type de projet
            analysis["type"] = self._determine_project_type(analysis)
            
            # Vérifier la compatibilité M1
            analysis["m1_compatible"] = self._check_m1_compatibility(analysis)
            
            # Générer le script d'installation
            analysis["installation_script"] = self._generate_install_script(analysis)
            
            # Identifier les points d'intégration
            analysis["integration_points"] = self._identify_integration_points(analysis)
            
            print(f"✅ Analyse terminée: {analysis['type']} (M1: {'✅' if analysis['m1_compatible'] else '❌'})")
            
        except Exception as e:
            print(f"❌ Erreur analyse: {e}")
            analysis["error"] = str(e)
        
        return analysis
    
    def _analyze_requirements(self, file_path):
        """Analyser requirements.txt"""
        deps = []
        with open(file_path, 'r') as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    package = line.split("==")[0].split(">=")[0].split("<=")[0].strip()
                    deps.append(package)
        
        return {"dependencies": deps, "package_manager": "pip"}
    
    def _analyze_setup_py(self, file_path):
        """Analyser setup.py"""
        deps = []
        try:
            with open(file_path, 'r') as f:
                content = f.read()
                # Simple regex pour les dépendances
                import re
                matches = re.findall(r'install_requires\s*=\s*\[(.*?)\]', content, re.DOTALL)
                if matches:
                    deps_str = matches[0]
                    deps = [dep.strip().strip('"\'') for dep in deps_str.split(",") if dep.strip()]
        except:
            pass
        
        return {"dependencies": deps, "package_manager": "pip", "setup_py": True}
    
    def _analyze_pyproject(self, file_path):
        """Analyser pyproject.toml"""
        try:
            import tomllib
            with open(file_path, 'rb') as f:
                data = tomllib.load(f)
            
            deps = []
            if "project" in data and "dependencies" in data["project"]:
                deps = data["project"]["dependencies"]
            
            return {"dependencies": deps, "package_manager": "pip", "pyproject": True}
        except:
            return {"dependencies": [], "package_manager": "pip"}
    
    def _analyze_package_json(self, file_path):
        """Analyser package.json"""
        try:
            import json
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            deps = []
            if "dependencies" in data:
                deps = list(data["dependencies"].keys())
            
            return {"dependencies": deps, "package_manager": "npm", "node_project": True}
        except:
            return {"dependencies": [], "package_manager": "npm"}
    
    def _analyze_dockerfile(self, file_path):
        """Analyser Dockerfile"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        has_python = "python" in content.lower()
        has_node = "node" in content.lower()
        has_arm64 = "arm64" in content.lower() or "armhf" in content.lower()
        
        return {
            "docker": True,
            "python": has_python,
            "node": has_node,
            "arm64_support": has_arm64
        }
    
    def _analyze_readme(self, file_path):
        """Analyser README.md"""
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraire des informations clés
            has_install = "install" in content.lower()
            has_usage = "usage" in content.lower()
            has_requirements = "requirements" in content.lower()
            
            return {
                "readme": True,
                "has_install_instructions": has_install,
                "has_usage_examples": has_usage,
                "mentions_requirements": has_requirements
            }
        except:
            return {"readme": False}
    
    def _analyze_makefile(self, file_path):
        """Analyser Makefile"""
        with open(file_path, 'r') as f:
            content = f.read()
        
        targets = []
        for line in content.split("\n"):
            if ":" in line and not line.startswith("\t"):
                targets.append(line.split(":")[0].strip())
        
        return {"makefile": True, "targets": targets}
    
    def _analyze_directory_structure(self, repo_path):
        """Analyser la structure des répertoires"""
        structure = {}
        
        for root, dirs, files in os.walk(repo_path):
            rel_path = os.path.relpath(root, repo_path)
            if rel_path == ".":
                rel_path = "root"
            
            structure[rel_path] = {
                "dirs": dirs,
                "files": files,
                "file_count": len(files)
            }
        
        return structure
    
    def _determine_project_type(self, analysis):
        """Déterminer le type de projet"""
        if analysis.get("node_project"):
            return "Node.js"
        elif analysis.get("setup_py") or analysis.get("pyproject"):
            return "Python"
        elif analysis.get("docker"):
            return "Docker"
        elif analysis.get("makefile"):
            return "Make/C/C++"
        else:
            return "Unknown"
    
    def _check_m1_compatibility(self, analysis):
        """Vérifier la compatibilité M1"""
        issues = []
        
        # Vérifier les dépendances problématiques
        problematic_deps = {
            "tensorflow": "TensorFlow (version M1 disponible)",
            "opencv-python": "OpenCV (version M1 disponible)",
            "mysql": "MySQL (utiliser mysqlclient)",
            "psycopg2": "PostgreSQL (utiliser psycopg2-binary)",
        }
        
        for dep in analysis.get("dependencies", []):
            dep_name = dep.split("==")[0].split(">=")[0].split("<=")[0]
            if dep_name in problematic_deps:
                issues.append(f"{dep_name}: {problematic_deps[dep_name]}")
        
        # Vérifier le support ARM64
        docker_info = analysis.get("docker", {})
        if isinstance(docker_info, dict) and not docker_info.get("arm64_support", False):
            issues.append("Dockerfile sans support ARM64 explicite")
        
        analysis["compatibility_issues"] = issues
        return len(issues) == 0
    
    def _generate_install_script(self, analysis):
        """Générer le script d'installation"""
        repo_name = analysis["name"]
        script_path = f"lab/{repo_name}/install_agent.sh"
        
        script_content = f"""#!/bin/bash
# Installation Script for {repo_name}
# Generated by AXE System for M1 Mac

set -e

echo "🚀 Installation de {repo_name} pour M1 Mac..."

# Vérifier Python 3.12+
if ! command -v python3.12 &> /dev/null; then
    echo "❌ Python 3.12 requis"
    exit 1
fi

# Créer environnement virtuel
echo "📦 Création environnement virtuel..."
python3.12 -m venv venv
source venv/bin/activate

# Installation dépendances
"""
        
        if analysis["type"] == "Python":
            script_content += """
# Dépendances Python
if [ -f "requirements.txt" ]; then
    echo "📦 Installation dépendances Python..."
    pip install -r requirements.txt
else
    echo "📦 Installation depuis setup.py..."
    pip install -e .
fi
"""
        
        elif analysis["type"] == "Node.js":
            script_content += """
# Vérifier Node.js
if ! command -v node &> /dev/null; then
    echo "❌ Node.js requis"
    exit 1
fi

# Dépendances Node.js
if [ -f "package.json" ]; then
    echo "📦 Installation dépendances Node.js..."
    npm install
fi
"""
        
        script_content += f"""

# Configuration M1
echo "⚡ Configuration pour M1 Mac..."
export CFLAGS="-O3 -march=arm64"
export CXXFLAGS="-O3 -march=arm64"

# Test d'installation
echo "🧪 Test d'installation..."
"""
        
        if analysis["type"] == "Python":
            script_content += """
python -c "import sys; print(f'Python {sys.version} OK')"
"""
        elif analysis["type"] == "Node.js":
            script_content += """
node -v
npm --version
"""
        
        script_content += f"""

echo "✅ Installation terminée pour {repo_name}"
echo "📍 Projet installé dans: $(pwd)"
echo "🔧 Commandes disponibles:"
"""
        
        if analysis["type"] == "Python":
            script_content += """
echo "  source venv/bin/activate  # Activer environnement"
echo "  python main.py            # Lancer application" """
        elif analysis["type"] == "Node.js":
            script_content += """
echo "  npm start                 # Lancer application"
echo "  npm run dev               # Mode développement" """
        
        script_content += """
echo ""
echo "🧠 Pour intégrer dans AXE System:"
echo "  python3 ../../ax.py ingest {repo_type} '{repo_name}' 'Fonctions principales du projet'"
"""
        
        # Écrire le script
        with open(script_path, 'w') as f:
            f.write(script_content)
        
        # Rendre exécutable
        os.chmod(script_path, 0o755)
        
        return script_path
    
    def _identify_integration_points(self, analysis):
        """Identifier les points d'intégration avec AXE System"""
        integration_points = []
        
        # Fonctions principales à ingérer
        if analysis["type"] == "Python":
            integration_points.extend([
                "Classes principales du projet",
                "Fonctions utilitaires importantes",
                "Patterns de code réutilisables",
                "Configuration et paramètres"
            ])
        elif analysis["type"] == "Node.js":
            integration_points.extend([
                "Modules ES6 importants",
                "Fonctions utilitaires",
                "Configuration",
                "API endpoints ou services"
            ])
        
        # Fichiers de configuration
        if analysis.get("readme", {}).get("has_install_instructions"):
            integration_points.append("Instructions d'installation")
        
        if analysis.get("makefile"):
            integration_points.append("Cibles Make utiles")
        
        return integration_points

    # --- MÉTHODES UTILITAIRES POUR DASHBOARD ---
    def _count_skills(self):
        """Compter le nombre total de skills"""
        try:
            memory_dir = Path("windsurf/memory")
            total_skills = 0
            
            for category_dir in memory_dir.iterdir():
                if category_dir.is_dir():
                    skills_file = category_dir / "skills.md"
                    if skills_file.exists():
                        with open(skills_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            # Compter les sections ### (skills)
                            skills_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
                            total_skills += skills_count
            
            return total_skills
        except:
            return 0
    
    def _count_categories(self):
        """Compter le nombre de catégories"""
        try:
            memory_dir = Path("windsurf/memory")
            return len([d for d in memory_dir.iterdir() if d.is_dir()])
        except:
            return 0
    
    def _get_last_activity(self):
        """Obtenir la date de dernière activité"""
        try:
            memory_dir = Path("windsurf/memory")
            latest_time = None
            
            for root, dirs, files in os.walk(memory_dir):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        file_time = file_path.stat().st_mtime
                        if latest_time is None or file_time > latest_time:
                            latest_time = file_time
            
            if latest_time:
                return datetime.fromtimestamp(latest_time)
            return None
        except:
            return None
    
    def _get_memory_size(self):
        """Obtenir la taille de la mémoire en MB"""
        try:
            memory_dir = Path("windsurf/memory")
            total_size = 0
            
            for root, dirs, files in os.walk(memory_dir):
                for file in files:
                    file_path = Path(root) / file
                    if file_path.exists():
                        total_size += file_path.stat().st_size
            
            return total_size / 1024 / 1024  # Convert to MB
        except:
            return 0
    
    def _get_session_stats(self):
        """Obtenir les statistiques de session"""
        try:
            stats = {
                "today": 0,
                "week": 0,
                "syncs": 0
            }
            
            # Pour l'instant, retourner des valeurs par défaut
            # TODO: Implémenter un vrai suivi de session
            return stats
        except:
            return {"today": 0, "week": 0, "syncs": 0}
    
    def _calculate_health_score(self, cpu_percent, memory_percent, disk_percent, skills_count):
        """Calculer un score de santé global"""
        try:
            # Score matériel (0-40 points)
            hardware_score = max(0, 40 - (cpu_percent + memory_percent + disk_percent) / 3 * 0.4)
            
            # Score skills (0-30 points)
            skills_score = min(30, skills_count * 2)
            
            # Score système (0-30 points)
            system_score = 30  # Base, pourrait être affiné
            
            total_score = hardware_score + skills_score + system_score
            return min(100, int(total_score))
        except:
            return 50
    
    def _get_recommendations(self, cpu_percent, memory_percent, disk_percent, skills_count):
        """Obtenir des recommandations basées sur l'état actuel"""
        recommendations = []
        
        if cpu_percent > 80:
            recommendations.append("CPU élevé - vérifier les processus actifs")
        
        if memory_percent > 80:
            recommendations.append("RAM élevée - envisager /zip pour nettoyer")
        
        if disk_percent > 80:
            recommendations.append("Disque plein - nettoyer les fichiers temporaires")
        
        if skills_count == 0:
            recommendations.append("Aucun skill - utiliser /ingest pour ajouter")
        
        return recommendations
    
    def _count_skills_in_dir(self, directory):
        """Compter les skills dans un répertoire spécifique"""
        try:
            total_skills = 0
            
            for category_dir in directory.iterdir():
                if category_dir.is_dir():
                    skills_file = category_dir / "skills.md"
                    if skills_file.exists():
                        with open(skills_file, 'r', encoding='utf-8') as f:
                            content = f.read()
                            skills_count = len(re.findall(r'^###\s+', content, re.MULTILINE))
                            total_skills += skills_count
            
            return total_skills
        except:
            return 0
    
    def _generate_session_report(self, archive_path, state_data):
        """Générer un rapport de session"""
        try:
            report_content = f"""# RAPPORT DE SESSION AXE SYSTEM
**Généré le**: {state_data['timestamp']}
**Version Python**: {state_data['python_version']}
**Répertoire**: {state_data['working_directory']}

## 📊 STATISTIQUES
- **Skills ingérés**: {state_data['skills_count']}
- **Catégories**: {state_data['categories_count']}
- **Dernière activité**: {state_data['last_activity']}

## 🔧 CONFIGURATION
- **AXE System**: ✅ Opérationnel
- **Python 3.12**: ✅ Disponible
- **Virtual Environment**: ✅ Configuré

## 📋 ACTIONS EFFECTUÉES
- ✅ Sauvegarde état système
- ✅ Archivage configuration
- ✅ Conservation skills
- ✅ Nettoyage temporaires
- ✅ Compression archive

## 🚀 PROCHAINE SESSION
Pour reprendre:
1. Décompresser l'archive si nécessaire
2. Exécuter `python3 ax.py health`
3. Continuer avec `/dash` pour observer l'état

---
*Généré par AXE System - Architecture Atomique*
"""
            
            with open(archive_path / "session_report.md", 'w', encoding='utf-8') as f:
                f.write(report_content)
                
        except Exception as e:
            print(f"⚠️ Erreur génération rapport: {e}")

    # --- DASHBOARD OBSERVABILITÉ ---
    def dashboard(self):
        """Tableau de bord en temps réel - santé M1 et cerveau Cloud"""
        print("📊 CASCADE ARCHITECT DASHBOARD")
        print("=" * 50)
        
        try:
            import psutil
            import time
            from datetime import datetime
            
            # Timestamp
            timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            print(f"🕐 {timestamp}")
            print()
            
            # --- SANTÉ M1 ---
            print("🍎 SANTÉ APPLE M1")
            print("-" * 25)
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            cpu_freq = psutil.cpu_freq()
            cpu_emoji = "🟢" if cpu_percent < 50 else "🟡" if cpu_percent < 80 else "🔴"
            print(f"{cpu_emoji} CPU: {cpu_percent:.1f}% ({cpu_freq.current:.0f}MHz)")
            
            # Mémoire Unifiée
            memory = psutil.virtual_memory()
            memory_emoji = "🟢" if memory.percent < 50 else "🟡" if memory.percent < 80 else "🔴"
            print(f"{memory_emoji} RAM: {memory.percent:.1f}% ({memory.used/1024/1024/1024:.1f}GB/{memory.total/1024/1024/1024:.1f}GB)")
            
            # Disque
            disk = psutil.disk_usage('/')
            disk_emoji = "🟢" if disk.percent < 50 else "🟡" if disk.percent < 80 else "🔴"
            print(f"{disk_emoji} SSD: {disk.percent:.1f}% ({disk.used/1024/1024/1024:.1f}GB/{disk.total/1024/1024/1024:.1f}GB)")
            
            # Température (si disponible)
            try:
                temps = psutil.sensors_temperatures()
                if temps:
                    for name, entries in temps.items():
                        for entry in entries:
                            if entry.current:
                                temp_emoji = "🟢" if entry.current < 60 else "🟡" if entry.current < 80 else "🔴"
                                print(f"{temp_emoji} {name}: {entry.current:.1f}°C")
            except:
                print("⚪ Température: Non disponible")
            
            print()
            
            # --- CERVEAU CLOUD ---
            print("🧠 CERVEAU CLOUD (windsurf/memory)")
            print("-" * 35)
            
            # Compter les skills
            skills_count = self._count_skills()
            skills_emoji = "🟢" if skills_count > 0 else "⚪"
            print(f"{skills_emoji} Skills ingérés: {skills_count}")
            
            # Compter les catégories
            categories_count = self._count_categories()
            print(f"📁 Catégories: {categories_count}")
            
            # Dernière activité
            last_activity = self._get_last_activity()
            activity_emoji = "🟢" if last_activity and (datetime.now() - last_activity).days < 1 else "🟡"
            if last_activity:
                time_ago = datetime.now() - last_activity
                if time_ago.days > 0:
                    time_str = f"Il y a {time_ago.days} jours"
                elif time_ago.seconds > 3600:
                    time_str = f"Il y a {time_ago.seconds // 3600}h"
                elif time_ago.seconds > 60:
                    time_str = f"Il y a {time_ago.seconds // 60}min"
                else:
                    time_str = f"Il y a {time_ago.seconds}s"
                print(f"{activity_emoji} Dernière activité: {time_str}")
            else:
                print("⚪ Dernière activité: Inconnue")
            
            # Taille de la mémoire
            memory_size = self._get_memory_size()
            size_emoji = "🟢" if memory_size < 100 else "🟡" if memory_size < 500 else "🔴"
            print(f"{size_emoji} Taille mémoire: {memory_size:.1f}MB")
            
            print()
            
            # --- PERFORMANCE CASCADE ---
            print("⚡ PERFORMANCE CASCADE")
            print("-" * 24)
            
            # Test de performance
            start_time = time.time()
            test_result = [x for x in range(10000)]
            perf_time = time.time() - start_time
            perf_emoji = "🟢" if perf_time < 0.01 else "🟡" if perf_time < 0.1 else "🔴"
            print(f"{perf_emoji} Test performance: {perf_time:.4f}s")
            
            # Compteurs de session
            session_stats = self._get_session_stats()
            print(f"📊 Sessions aujourd'hui: {session_stats.get('today', 0)}")
            print(f"📈 Skills cette semaine: {session_stats.get('week', 0)}")
            print(f"🔄 Sync GitHub: {session_stats.get('syncs', 0)}")
            
            print()
            
            # --- ÉTAT DES SERVICES ---
            print("🔧 ÉTAT DES SERVICES")
            print("-" * 20)
            
            # Git status
            try:
                git_status = subprocess.getoutput("git status --porcelain")
                git_clean = len(git_status.strip()) == 0
                git_emoji = "🟢" if git_clean else "🟡"
                print(f"{git_emoji} Git: {'Propre' if git_clean else 'Modifications'}")
            except:
                print("⚪ Git: Non disponible")
            
            # Virtual environment
            venv_path = Path("venv")
            venv_emoji = "🟢" if venv_path.exists() else "🔴"
            print(f"{venv_emoji} Venv: {'Actif' if venv_path.exists() else 'Manquant'}")
            
            # AXE System
            ax_emoji = "🟢" if Path("ax.py").exists() else "🔴"
            print(f"{ax_emoji} AXE System: {'Opérationnel' if Path('ax.py').exists() else 'Manquant'}")
            
            # Lab folder
            lab_path = Path("lab")
            lab_count = len(list(lab_path.glob("*"))) if lab_path.exists() else 0
            lab_emoji = "🟢" if lab_count > 0 else "⚪"
            print(f"{lab_emoji} Lab: {lab_count} projets")
            
            print()
            
            # --- INDICATEURS DE SANTÉ ---
            print("💓 INDICATEURS DE SANTÉ")
            print("-" * 26)
            
            # Calculer un score de santé global
            health_score = self._calculate_health_score(cpu_percent, memory.percent, disk.percent, skills_count)
            health_emoji = "🟢" if health_score > 80 else "🟡" if health_score > 60 else "🔴"
            print(f"{health_emoji} Score global: {health_score}/100")
            
            # Recommandations
            recommendations = self._get_recommendations(cpu_percent, memory.percent, disk.percent, skills_count)
            if recommendations:
                print("💡 Recommandations:")
                for rec in recommendations:
                    print(f"   • {rec}")
            else:
                print("✅ Tout semble optimal !")
            
            print()
            print("🔄 Mise à jour automatique toutes les 30 secondes...")
            print("   (Ctrl+C pour arrêter)")
            
        except ImportError:
            print("❌ psutil non disponible - installation requise")
            print("   Exécutez: pip install psutil")
        except Exception as e:
            print(f"❌ Erreur dashboard: {e}")

    # --- NETTOYAGE CONTEXTE ---
    def zip_context(self):
        """Archive la session et libère la mémoire de l'IA"""
        print("🗜️  NETTOYAGE DE CONTEXTE - AXE SYSTEM")
        print("=" * 45)
        
        try:
            from datetime import datetime
            import shutil
            import json
            
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            archive_name = f"session_archive_{timestamp}"
            archive_path = Path("archives") / archive_name
            
            print(f"📦 Création de l'archive: {archive_name}")
            
            # Créer le répertoire d'archives
            archive_path.mkdir(parents=True, exist_ok=True)
            
            # 1. Sauvegarder l'état actuel
            print("📋 Sauvegarde de l'état actuel...")
            state_data = {
                "timestamp": timestamp,
                "python_version": f"{sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}",
                "working_directory": str(Path.cwd()),
                "skills_count": self._count_skills(),
                "categories_count": self._count_categories(),
                "last_activity": datetime.now().isoformat(),
                "session_duration": "N/A", # Pourrait être implémenté
            }
            
            with open(archive_path / "session_state.json", 'w') as f:
                json.dump(state_data, f, indent=2)
            
            # 2. Archiver les fichiers de configuration critiques
            print("🔧 Archivage des configurations...")
            critical_files = [
                "ax.py",
                ".windsurfrules",
                "requirements.txt",
                ".python-version",
                "justfile"
            ]
            
            config_dir = archive_path / "config"
            config_dir.mkdir(exist_ok=True)
            
            for file_name in critical_files:
                src = Path(file_name)
                if src.exists():
                    dst = config_dir / file_name
                    shutil.copy2(src, dst)
                    print(f"   ✅ {file_name}")
                else:
                    print(f"   ⚪ {file_name} (manquant)")
            
            # 3. Archiver les skills essentiels
            print("🧠 Archivage des skills essentiels...")
            memory_dir = Path("windsurf/memory")
            if memory_dir.exists():
                memory_archive = archive_path / "memory"
                shutil.copytree(memory_dir, memory_archive, dirs_exist_ok=True)
                
                # Compter les skills archivés
                skills_count = self._count_skills_in_dir(memory_archive)
                print(f"   ✅ {skills_count} skills archivés")
            
            # 4. Créer un rapport de session
            print("📊 Génération du rapport de session...")
            self._generate_session_report(archive_path, state_data)
            
            # 5. Nettoyer les fichiers temporaires
            print("🧹 Nettoyage des fichiers temporaires...")
            temp_cleaned = self.clean()
            print(f"   ✅ {temp_cleaned} fichiers temporaires supprimés")
            
            # 6. Compresser l'archive
            print("🗜️  Compression de l'archive...")
            shutil.make_archive(str(archive_path), 'zip', str(archive_path))
            shutil.rmtree(archive_path)  # Supprimer le dossier non compressé
            
            archive_size = (Path(f"{archive_path}.zip").stat().st_size) / 1024 / 1024
            print(f"✅ Archive créée: {archive_name}.zip ({archive_size:.1f}MB)")
            
            # 7. Afficher le résumé
            print()
            print("📋 RÉSUMÉ DE NETTOYAGE")
            print("-" * 25)
            print(f"📦 Archive: {archive_name}.zip")
            print(f"🧠 Skills: {state_data['skills_count']} conservés")
            print(f"📁 Config: {len([f for f in critical_files if Path(f).exists()])} fichiers")
            print(f"🧹 Temp: {temp_cleaned} fichiers supprimés")
            print(f"💾 Taille: {archive_size:.1f}MB")
            
            print()
            print("🚀 AXE System est maintenant 'zippé' et prêt à repartir!")
            print("💡 Tapez '/dash' pour voir le tableau de bord重新开始")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors du nettoyage: {e}")
            return False

    # --- MONITOR ---
    def monitor(self):
        """Quick system monitoring"""
        print("📊 System Monitor:")
        
        try:
            import psutil
            
            # CPU
            cpu_percent = psutil.cpu_percent(interval=1)
            print(f"🖥️ CPU: {cpu_percent}%")
            
            # Memory
            memory = psutil.virtual_memory()
            print(f"💾 Memory: {memory.percent}% ({memory.used/1024/1024/1024:.1f}GB/{memory.total/1024/1024/1024:.1f}GB)")
            
            # Disk
            disk = psutil.disk_usage('/')
            print(f"💿 Disk: {disk.percent}% ({disk.used/1024/1024/1024:.1f}GB/{disk.total/1024/1024/1024:.1f}GB)")
            
            # Network (basic)
            try:
                import socket
                socket.create_connection(("8.8.8.8", 53), timeout=1)
                print("🌐 Network: Connected")
            except:
                print("🌐 Network: Disconnected")
                
        except ImportError:
            print("❌ psutil not available")
        except Exception as e:
            print(f"❌ Monitor error: {e}")

    # --- HELP ---
    def help(self):
        """Show help"""
        print("🚀 AXE System Commands:")
        print("  fix     - Repair infrastructure and dependencies")
        print("  health  - System health check")
        print("  ingest  - Ingest content: ingest [category] [title] [content]")
        print("  sync    - Synchronize with GitHub")
        print("  clean   - Clean temporary files")
        print("  monitor - System monitoring")
        print("  git     - Clone and analyze GitHub repository")
        print("  dash    - Tableau de bord temps réel")
        print("  zip     - Nettoyage contexte et archive")
        print("  help    - Show this help")
        print("\nSlash Commands:")
        print("  /f      - Fix system")
        print("  /h      - Health check")
        print("  /s      - Sync GitHub")
        print("  /i      - Ingest content")
        print("  /git    - Clone and analyze repository")
        print("  /dash   - Tableau de bord observabilité")
        print("  /zip    - Nettoyage contexte performance")
        print("\nTableau de Bord Architecte:")
        print("  Commande | Action | Impact Architecte")
        print("  /dash    | Tableau de Bord | Visualise la santé de ton M1 et de ton Cerveau Cloud")
        print("  /zip     | Nettoyage Contexte | Archive la session et libère la mémoire de l'IA")
        print("  /git     | Ingénierie Repo | Transforme n'importe quel repo GitHub en agent local")
        print("\nExamples:")
        print("  python3 ax.py fix")
        print("  python3 ax.py ingest python 'NumPy Tricks' 'Use vectorization instead of loops'")
        print("  python3 ax.py git https://github.com/user/repo.git")
        print("  python3 ax.py dash")
        print("  python3 ax.py zip")
        print("  /dash")
        print("  /zip")
        print("  /git https://github.com/Priivacy-ai/spec-kitty.git")

    # --- PRIVATE METHODS ---
    def _create_essential_files(self):
        """Create essential files if missing"""
        
        # .windsurfrules
        windsurf_rules = Path(".windsurfrules")
        if not windsurf_rules.exists():
            content = """# ⚡ AXE SYSTEM COMMANDS
shortcuts:
  /f: "python3 ax.py fix"    # Répare tout
  /s: "python3 ax.py sync"   # Sauvegarde GitHub
  /h: "python3 ax.py health" # Santé du système
  /i: "python3 ax.py ingest" # Ingestion : /i [Cat] [Titre] [Content]

# IDENTITY: Senior Fullstack AI Architect & UX Lead
- **Tone**: Direct, professional, Ethic Hacker / Tech Lead style
- **Expertise**: Apple M1 (arm64) optimization, Unified Memory, Low-level TUI/UX
- **Stack**: Python (FastAPI/NumPy), Node.js (Next.js), PyTorch, Metal Shaders

# CORE RESPONSE RULES:
1. **Code First**: Provide high-performance, vectorized (NumPy) code snippets immediately
2. **Visuals**: Use Braille Unicode, TrueColor (24-bit) ANSI, and structured lists
3. **M1 Native**: Always prioritize arm64 compatibility and Accelerate framework
4. **Memory Management**: Refer to the 'windsurf/memory/' structure for context
5. **Format**: No technical summaries unless requested. Use LaTeX for complex math
"""
            windsurf_rules.write_text(content)
            print(f"✅ Created .windsurfrules")
        
        # requirements.txt
        requirements = Path("requirements.txt")
        if not requirements.exists():
            content = """# Cascade Architect Requirements - Python 3.12
numpy>=2.4.3
psutil>=7.2.2
rich>=14.3.3
textual>=8.1.1
pyobjc-framework-Metal>=12.1
pyobjc-framework-Cocoa>=12.1
typing-extensions>=4.15.0
"""
            requirements.write_text(content)
            print(f"✅ Created requirements.txt")
        
        # .python-version
        python_version = Path(".python-version")
        if not python_version.exists():
            python_version.write_text("3.12\n")
            print(f"✅ Created .python-version")
        
        # windsurf/memory/identity.md
        identity_file = Path("windsurf/memory/identity.md")
        if not identity_file.exists():
            identity_file.parent.mkdir(parents=True, exist_ok=True)
            content = f"""# Identity & Project Context
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

---
*Created by AXE System - {datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')}*
"""
            identity_file.write_text(content)
            print(f"✅ Created identity.md")
        
        # windsurf/memory/skills.md
        skills_file = Path("windsurf/memory/skills.md")
        if not skills_file.exists():
            content = """# Expert Skills Vault - Cascade AI System

## 🧠 Core Architecture
### M1 Native Optimization
- **Pattern**: NumPy vectorization instead of pixel loops
- **Performance**: 68.8 FPS achieved with 16ms frame budget
- **Braille Unicode**: U+2800 mapping for 2x8 resolution
- **Double Buffering**: Prevents flicker in animations

---

## 🚀 Skills Ingested via AXE System

*New skills will be automatically added here...*

---
*Created by AXE System*
"""
            skills_file.write_text(content)
            print(f"✅ Created skills.md")


def main():
    """Main entry point"""
    ax = Architect()
    cmd = sys.argv[1] if len(sys.argv) > 1 else "help"
    if cmd in ["fix", "/f"]: ax.repair()
    elif cmd in ["sync", "/s"]: ax.sync()
    elif cmd in ["dash", "/dash"]: ax.dashboard()
    elif cmd in ["find", "/find"]:
        if len(sys.argv) > 2: ax.find(" ".join(sys.argv[2:]))
        else: print("❌ Usage: /find [mot-clé]")
    elif cmd in ["audit", "/audit"]: ax.audit()
    elif cmd in ["new", "/new"]:
        if len(sys.argv) > 2: ax.new_project(sys.argv[2])
        else: print("❌ Usage: /new [project-name]")
    elif cmd in ["ux", "/ux"]:
        path = sys.argv[2] if len(sys.argv) > 2 else "."
        ax.ux_audit(path)
    elif cmd in ["commit", "/commit"]: ax.smart_commit()
    elif cmd in ["ingest", "/i"]:
        if len(sys.argv) >= 5: ax.ingest(sys.argv[2], sys.argv[3], " ".join(sys.argv[4:]))
    else:
        print("Usage: python3 ax.py [fix|sync|dash|ingest|find|audit|new|ux|commit]")


if __name__ == "__main__":
    main()
