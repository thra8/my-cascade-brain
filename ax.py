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
        self.dirs = ["ai", "ui", "m1", "backend", "scripts", ".windsurf/logs"]
        self.libs = ["numpy", "textual", "psutil", "rich", "pyobjc-framework-Metal", "pyobjc-framework-Cocoa"]
        self.project_root = Path.cwd()
        
    # --- REPAIR & HEALTH ---
    def repair(self):
        """Repair infrastructure and dependencies"""
        print("🛠️  Repairing infrastructure...")
        
        # Create essential directories
        for d in self.dirs:
            dir_path = Path(d)
            if "memory" in str(d):
                dir_path = Path("windsurf/memory") / d.replace("windsurf/memory/", "")
            dir_path.mkdir(parents=True, exist_ok=True)
            print(f"✅ Directory: {dir_path}")
        
        # Install essential libraries
        try:
            print("📦 Installing libraries...")
            subprocess.check_call([sys.executable, "-m", "pip", "install"] + self.libs)
            print("✅ Libraries installed")
        except subprocess.CalledProcessError as e:
            print(f"❌ Pip error: {e}")
        
        # Create essential files
        self._create_essential_files()
        print("✅ Repair completed")
    
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
        print("  help    - Show this help")
        print("\nSlash Commands:")
        print("  /f      - Fix system")
        print("  /h      - Health check")
        print("  /s      - Sync GitHub")
        print("  /i      - Ingest content")
        print("  /git    - Clone and analyze repository")
        print("\nExamples:")
        print("  python3 ax.py fix")
        print("  python3 ax.py ingest python 'NumPy Tricks' 'Use vectorization instead of loops'")
        print("  python3 ax.py git https://github.com/user/repo.git")
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
    
    if len(sys.argv) < 2:
        ax.help()
        return
    
    cmd = sys.argv[1].lower()
    
    if cmd == "fix":
        ax.repair()
    elif cmd == "health":
        ax.health()
    elif cmd == "sync":
        ax.sync()
    elif cmd == "clean":
        ax.clean()
    elif cmd == "monitor":
        ax.monitor()
    elif cmd == "help":
        ax.help()
    elif cmd == "git":
        if len(sys.argv) < 3:
            print("❌ Usage: python3 ax.py git [GitHub URL]")
            return
        url = sys.argv[2]
        target_path, analysis = ax.git_clone(url)
        if target_path and analysis:
            print(f"\n📊 Analyse complète:")
            print(f"📁 Type: {analysis['type']}")
            print(f"📦 Dépendances: {len(analysis['dependencies'])}")
            print(f"🍎 M1 Compatible: {'✅' if analysis['m1_compatible'] else '❌'}")
            if analysis.get('compatibility_issues'):
                print("⚠️ Issues de compatibilité:")
                for issue in analysis['compatibility_issues']:
                    print(f"   • {issue}")
            print(f"📜 Script: {analysis['installation_script']}")
            print(f"🔗 Points d'intégration: {len(analysis['integration_points'])}")
            print(f"\n🚀 Prochaines étapes:")
            print(f"   cd lab/{analysis['name']}")
            print(f"   ./install_agent.sh")
            for point in analysis['integration_points'][:3]:
                print(f"   • Ingestérer: {point}")
    elif cmd == "ingest":
        if len(sys.argv) < 5:
            print("❌ Usage: python3 ax.py ingest [category] [title] [content]")
            return
        cat = sys.argv[2]
        title = sys.argv[3]
        content = " ".join(sys.argv[4:])
        ax.ingest(cat, title, content)
    else:
        print(f"❌ Unknown command: {cmd}")
        ax.help()


if __name__ == "__main__":
    main()
