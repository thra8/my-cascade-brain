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
        print("  help    - Show this help")
        print("\nExamples:")
        print("  python3 ax.py fix")
        print("  python3 ax.py ingest python 'NumPy Tricks' 'Use vectorization instead of loops'")
        print("  python3 ax.py sync")

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
