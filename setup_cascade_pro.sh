#!/bin/bash
# ----------------------------------------------------------------
# MASTER SETUP: CASCADE ARCHITECT ENV (M1 Optimized)
# ----------------------------------------------------------------

set -e  # Exit on error

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
PURPLE='\033[0;35m'
CYAN='\033[0;36m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_step() {
    echo -e "${BLUE}🚀 $1${NC}"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_info() {
    echo -e "${PURPLE}ℹ️ $1${NC}"
}

print_header() {
    echo -e "${CYAN}╔══════════════════════════════════════════════════════════════╗${NC}"
    echo -e "${CYAN}║     CASCADE ARCHITECT ENV - M1 OPTIMIZED SETUP          ║${NC}"
    echo -e "${CYAN}╚══════════════════════════════════════════════════════════════╝${NC}"
    echo
}

print_header
print_step "Initialisation de l'infrastructure de mémoire..."

# 1. Création de l'arborescence
print_step "Création de l'arborescence des répertoires..."

mkdir -p windsurf/memory
mkdir -p windsurf/scripts
mkdir -p .github/workflows
mkdir -p .windsurf/logs
mkdir -p .windsurf/memory

print_success "Arborescence créée"

# 2. Création des fichiers de mémoire initiale
print_step "Création des fichiers de mémoire initiale..."

# Identity & Project Context
cat <<'EOF' > windsurf/memory/identity.md
# Identity & Project Context
- **Role**: Senior Fullstack AI Architect & UX Lead
- **Stack**: Python (FastAPI), Node.js (Next.js), PyTorch, Tailwind CSS
- **Environment**: Apple M1 (arm64)
- **GitHub Repo**: [A configurer avec git remote add origin]
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

### API Keys Configuration
- **OPENAI_API_KEY**: ${OPENAI_API_KEY}
- **ANTHROPIC_API_KEY**: ${ANTHROPIC_API_KEY}
- **GEMINI_API_KEY**: ${GEMINI_API_KEY}
- **DUCKDUCKGO_API_KEY**: ${DUCKDUCKGO_API_KEY}

### Database Identifiers
- **PROJECT_DB_ID**: ${PROJECT_DB_ID}
- **MEMORY_DB_ID**: ${MEMORY_DB_ID}
- **CACHE_DB_ID**: ${CACHE_DB_ID}

### Service Endpoints
- **WINDSURF_SERVER**: ${WINDSURF_SERVER}
- **CLAUDE_API_ENDPOINT**: ${CLAUDE_API_ENDPOINT}
- **GITHUB_TOKEN**: ${GITHUB_TOKEN}

## Security Settings
- **Encryption**: AES-256 for sensitive data
- **Authentication**: JWT tokens with 24h expiry
- **Rate Limiting**: 100 requests per minute
- **Audit Logging**: All operations tracked
EOF

print_success "Fichier identity.md créé"

# Skills Vault
cat <<'EOF' > windsurf/memory/skills.md
# Expert Skills Vault - Cascade AI System

## 3D Graphics & Rendering
### M1 Native Optimization
- **Pattern**: NumPy vectorization instead of pixel loops
- **Performance**: 68.8 FPS achieved with 16ms frame budget
- **Braille Unicode**: U+2800 mapping for 2x8 resolution
- **Double Buffering**: Prevents flicker in animations
- **Accelerate Framework**: Apple's vector libraries integration

### Rendering Pipeline
- **No Pixel Loops**: Strict NumPy broadcasting
- **Frame Budget**: 16ms for 60 FPS target
- **Memory Pooling**: Reuse buffers to avoid allocations
- **Thermal Management**: Monitor M1 temperature and adjust load

## Color Systems & Terminal Graphics
### TrueColor Implementation
- **Priority**: 24-bit RGB with ANSI 256 fallback
- **HEX Formats**: Support for #RGB, #RRGGBB, #RRGGBBAA
- **WCAG Compliance**: Contrast ratio calculations for accessibility
- **Unicode Dithering**: Smooth gradients in terminal

### Color Harmonies
- **HSL Space**: Generate complementary, triadic, analogous
- **Accessibility**: Ensure WCAG AA/AAA compliance
- **Terminal Limits**: Work within 256 color fallback
- **Performance**: Vectorized calculations for gradients

## DevOps & System Architecture
### Stack Health Monitoring
- **Port Management**: Check availability before service launch
- **Process Detection**: Identify and kill conflicting processes
- **Resource Monitoring**: CPU, memory, disk, network tracking
- **Auto-Recovery**: Restart failed services automatically

### M1 Optimization Patterns
- **Worker Calculation**: (2 * cpu_count) + 1 for FastAPI
- **CPU Affinity**: P-cores for performance, E-cores for background
- **Memory Limits**: 512MB per worker, <4GB total stack
- **Native Dependencies**: ARM64-specific installations

## AI Agent Architecture
### Devin-like Planning System
- **Think Before Act**: Plan before execution
- **Self-Evolution**: Learn from corrections and feedback
- **Lessons Learned**: Store reusable patterns
- **Scratchpad System**: Organize thoughts and progress

### Multi-Agent Coordination
- **Planner Agent**: o1-like strategic planning
- **Executor Agent**: Claude/GPT-like implementation
- **Cross-Checking**: Validate results between agents
- **Iterative Improvement**: Refine based on feedback

## Memory & Knowledge Management
### Dual Memory System
- **System 1**: Programming concepts, business logic, past interactions
- **System 2**: Reasoning steps, decision processes, tool usage
- **Vector Storage**: Semantic search with embeddings
- **Knowledge Graph**: Relationship mapping between concepts

### MCP Integration
- **Universal Compatibility**: Cursor, Windsurf, Claude Code, VS Code
- **Real-time Communication**: WebSocket synchronization
- **Session Management**: Persistent sessions across IDEs
- **Tool Integration**: Native IDE tool support

## Spec-Driven Development
### Workflow Integration
- **6 Steps**: spec → plan → tasks → implement → review → merge
- **Repository Artifacts**: spec.md, plan.md, tasks.md
- **Work Packages**: Lane-based execution (planned → doing → for_review → done)
- **Git Worktrees**: Isolated parallel development

### Multi-Agent Support
- **12 Agents**: Claude Code, Cursor, Codex, Gemini, Copilot, etc.
- **Agent Management**: Centralized configuration
- **Template Generation**: Agent-specific templates
- **Coordination**: Parallel execution with conflict resolution

## Performance Optimization
### M1 Specific Patterns
- **Accelerate Framework**: Use Apple's vector libraries
- **Memory Alignment**: Optimize for cache efficiency
- **Thermal Throttling**: Monitor and adjust for temperature
- **GPU Utilization**: Balance CPU/GPU workloads

### Terminal Graphics Performance
- **Unicode Rendering**: Use Braille for 2x8 resolution
- **Color Management**: TrueColor with fallbacks
- **Frame Timing**: Consistent 16ms budget
- **Memory Efficiency**: Pool and reuse buffers

## Error Handling & Validation
### Graceful Degradation
- **Fallback Systems**: Multiple levels of functionality
- **Error Recovery**: Automatic retry with backoff
- **User Feedback**: Clear error messages and suggestions
- **Logging**: Comprehensive error tracking

### Validation Patterns
- **Input Validation**: Type checking and sanitization
- **Output Verification**: Result validation before return
- **State Consistency**: Maintain valid system state
- **Resource Cleanup**: Proper resource management

## Integration Patterns
### System Coordination
- **Event-Driven**: React to system changes
- **State Management**: Centralized state tracking
- **Message Passing**: Clear communication between components
- **Modularity**: Independent, reusable components

### Memory Integration
- **Context Loading**: Load relevant memories before tasks
- **Pattern Recognition**: Identify and apply learned patterns
- **Continuous Learning**: Update knowledge base from interactions
- **Compression**: Optimize memory usage
EOF

print_success "Fichier skills.md créé"

# Context Snapshot
cat <<'EOF' > windsurf/memory/context_snapshot.md
# Cascade AI System - Context Snapshot
# Current state and recent activities

## Current Session Context
- **Active Skills**: 9 skills installed and operational
- **Recent Tasks**: Installation of 4 new skills (devin-cursorrules, cipher-memory, spec-kitty, terminal-color-design)
- **System Status**: All systems operational, M1 optimizations applied
- **Memory Integration**: Cipher memory system integrated
- **Development Workflow**: Spec Kitty workflow established

## Skills Status
- **3d-terminal-graphics**: ✅ Operational (68.8 FPS)
- **terminal-color-design**: ✅ Operational (TrueColor + WCAG)
- **devops-stack-orchestrator**: ✅ Operational (Port + Health)
- **devin-cursorrules**: ✅ Operational (Devin-like AI assistant)
- **cipher-memory**: ✅ Operational (Dual memory system)
- **spec-kitty**: ✅ Operational (Spec-driven development)

## Recent Optimizations
- M1 native vectorization for 3D graphics
- TrueColor terminal rendering with WCAG compliance
- Port management with conflict resolution
- Dual memory layer integration
- Multi-agent coordination system

## Next Steps
- Continue optimizing for Mac M1 performance
- Expand skill library with specialized capabilities
- Implement advanced multi-agent workflows
- Enhance self-evolution capabilities

## GitHub Integration
- **Repository**: https://github.com/thra8/my-cascade-brain
- **Sync Status**: ✅ Active
- **Workflow**: Automated via sync.sh
- **Validation**: GitHub Actions enabled

## Environment Configuration
- **Platform**: macOS M1 (ARM64)
- **Python**: 3.11+ with ARM64 optimizations
- **Node.js**: Latest with ARM64 support
- **Git**: Configured with SSH keys
- **Dependencies**: M1 native where applicable
EOF

print_success "Fichier context_snapshot.md créé"

# 3. Création du Sentinel Script (Auto-Sync)
print_step "Création du Sentinel Script (Auto-Sync)..."

cat <<'EOF' > windsurf/scripts/sentinel.py
#!/usr/bin/env python3
"""
Cascade Sentinel - Auto-Sync pour le cerveau sur GitHub
Script de synchronisation automatique de la mémoire
"""

import os
import subprocess
import sys
from datetime import datetime
from pathlib import Path

class Sentinel:
    """Agent Sentinel pour la synchronisation automatique"""
    
    def __init__(self):
        self.project_root = Path.cwd()
        self.windsurf_dir = self.project_root / "windsurf"
        self.memory_dir = self.windsurf_dir / "memory"
        
    def log(self, message: str):
        """Journalisation avec timestamp"""
        timestamp = datetime.now().strftime("%H:%M:%S")
        print(f"[{timestamp}] 🛡️ Sentinel: {message}")
    
    def run_command(self, cmd: list, cwd: str = None) -> subprocess.CompletedProcess:
        """Exécuter une commande"""
        try:
            return subprocess.run(
                cmd, 
                capture_output=True, 
                text=True, 
                cwd=cwd or self.project_root
            )
        except Exception as e:
            self.log(f"❌ Erreur commande: {e}")
            return subprocess.CompletedProcess([], 1, "", str(e))
    
    def sync_memory(self):
        """Synchroniser la mémoire avec GitHub"""
        self.log("Synchronisation de la mémoire...")
        
        # Vérifier que le répertoire windsurf existe
        if not self.windsurf_dir.exists():
            self.log("❌ Répertoire windsurf introuvable")
            return False
        
        # Ajouter les fichiers de mémoire
        add_result = self.run_command(["git", "add", "windsurf/memory/", ".windsurfrules"])
        if add_result.returncode != 0:
            self.log("❌ Erreur ajout des fichiers")
            return False
        
        # Vérifier s'il y a des changements
        status_result = self.run_command(["git", "status", "--porcelain"])
        if not status_result.stdout.strip():
            self.log("ℹ️ Aucun changement à synchroniser")
            return True
        
        # Commiter les changements
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        commit_msg = f"🧠 Memory Auto-Update: {timestamp} | Sentinel Sync"
        
        commit_result = self.run_command(["git", "commit", "-m", commit_msg])
        if commit_result.returncode != 0:
            self.log("❌ Erreur commit")
            return False
        
        # Push vers GitHub
        push_result = self.run_command(["git", "push", "origin", "main"])
        if push_result.returncode != 0:
            self.log("❌ Erreur push (vérifier configuration SSH)")
            return False
        
        self.log("✅ Synchronisation complète")
        return True
    
    def validate_memory(self):
        """Valider la structure de la mémoire"""
        self.log("Validation de la mémoire...")
        
        required_files = ["skills.md", "identity.md", "context_snapshot.md"]
        issues = []
        
        for file_name in required_files:
            file_path = self.memory_dir / file_name
            if not file_path.exists():
                issues.append(f"Fichier manquant: {file_name}")
            elif not file_path.read_text().strip():
                issues.append(f"Fichier vide: {file_name}")
        
        if issues:
            self.log("❌ Problèmes de validation:")
            for issue in issues:
                self.log(f"   • {issue}")
            return False
        
        self.log("✅ Mémoire validée")
        return True
    
    def get_memory_stats(self):
        """Obtenir les statistiques de la mémoire"""
        stats = {
            "files": 0,
            "total_size": 0,
            "last_modified": None
        }
        
        if self.memory_dir.exists():
            files = list(self.memory_dir.glob("*.md"))
            stats["files"] = len(files)
            
            for file_path in files:
                size = file_path.stat().st_size
                stats["total_size"] += size
                
                mtime = file_path.stat().st_mtime
                if stats["last_modified"] is None or mtime > stats["last_modified"]:
                    stats["last_modified"] = mtime
        
        return stats

def main():
    """Point d'entrée principal"""
    sentinel = Sentinel()
    
    print("🛡️ Cascade Sentinel - Auto-Sync")
    print("=" * 40)
    
    try:
        # Validation rapide
        if not sentinel.validate_memory():
            sys.exit(1)
        
        # Synchronisation
        if sentinel.sync_memory():
            # Statistiques
            stats = sentinel.get_memory_stats()
            print(f"\n📊 Statistiques de la mémoire:")
            print(f"   Fichiers: {stats['files']}")
            print(f"   Taille totale: {stats['total_size']} bytes")
            
            if stats["last_modified"]:
                last_mod = datetime.fromtimestamp(stats["last_modified"])
                print(f"   Dernière modification: {last_mod.strftime('%Y-%m-%d %H:%M:%S')}")
            
            print("\n🎯 Système synchronisé avec succès!")
        else:
            print("\n⚠️ Erreur de synchronisation")
            sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n⏹️ Sentinel interrompu")
    except Exception as e:
        print(f"\n❌ Erreur inattendue: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
EOF

print_success "Script sentinel.py créé"

# 4. Création du workflow GitHub Actions
print_step "Création du workflow GitHub Actions..."

cat <<'EOF' > .github/workflows/validate-memory.yml
name: Validate Cascade Memory

on:
  push:
    branches: [ main ]
  pull_request:
    branches: [ main ]

jobs:
  validate-memory:
    runs-on: ubuntu-latest
    
    steps:
    - name: Checkout repository
      uses: actions/checkout@v4
      
    - name: Setup Python
      uses: actions/setup-python@v4
      with:
        python-version: '3.11'
        
    - name: Validate memory structure
      run: |
        echo "🧠 Validation de la mémoire Cascade..."
        
        # Vérifier les fichiers requis
        REQUIRED_FILES=("windsurf/memory/skills.md" "windsurf/memory/identity.md" "windsurf/memory/context_snapshot.md")
        MISSING_FILES=()
        
        for file in "${REQUIRED_FILES[@]}"; do
          if [ ! -f "$file" ]; then
            MISSING_FILES+=("$file")
          fi
        done
        
        if [ ${#MISSING_FILES[@]} -gt 0 ]; then
          echo "❌ Fichiers manquants:"
          for file in "${MISSING_FILES[@]}"; do
            echo "  • $file"
          done
          exit 1
        fi
        
        echo "✅ Tous les fichiers requis sont présents"
        
    - name: Validate Markdown syntax
      run: |
        echo "📝 Validation de la syntaxe Markdown..."
        
        # Installer markdownlint-cli
        npm install -g markdownlint-cli
        
        # Valider les fichiers Markdown
        for file in windsurf/memory/*.md; do
          if [ -f "$file" ]; then
            echo "Validation de $file..."
            markdownlint "$file" || {
              echo "❌ Erreur de syntaxe Markdown dans $file"
              exit 1
            }
            echo "✅ $file valide"
          fi
        done
        
    - name: Check for demo artifacts
      run: |
        echo "🧹 Vérification des artefacts de démo..."
        
        # Chercher les patterns de démo
        DEMO_PATTERNS=("demo completed" "démo terminée" "✅.*demo" "🎉.*demo")
        
        FOUND_DEMO=false
        for pattern in "${DEMO_PATTERNS[@]}"; do
          if grep -r "$pattern" windsurf/memory/; then
            echo "⚠️ Artefacts de démo trouvés: $pattern"
            FOUND_DEMO=true
          fi
        done
        
        if [ "$FOUND_DEMO" = true ]; then
          echo "⚠️ Nettoyage requis avant validation"
        else
          echo "✅ Aucun artefact de démo trouvé"
        fi
        
    - name: Success notification
      run: |
        echo "🎉 Validation de la mémoire Cascade terminée avec succès!"
        echo "📊 Repository: https://github.com/thra8/my-cascade-brain"
        echo "🧠 Le cerveau de Cascade est intact et prêt à l'emploi"
EOF

print_success "Workflow GitHub Actions créé"

# 5. Finalisation
print_step "Finalisation de l'environnement..."

# Permissions
chmod +x windsurf/scripts/*.py

# Git configuration
git init 2>/dev/null || true

# .gitignore
cat <<'EOF' > .gitignore
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
build/
develop-eggs/
dist/
downloads/
eggs/
.eggs/
lib/
lib64/
parts/
sdist/
var/
wheels/
*.egg-info/
.installed.cfg
*.egg

# Node.js
node_modules/
npm-debug.log*
yarn-debug.log*
yarn-error.log*

# Environment
.env
.env.local
.env.development.local
.env.test.local
.env.production.local

# IDE
.vscode/
.idea/
*.swp
*.swo
*~

# OS
.DS_Store
.DS_Store?
._*
.Spotlight-V100
.Trashes
ehthumbs.db
Thumbs.db

# Logs
logs/
*.log

# Temporary files
*.tmp
*.temp
EOF

print_success "Fichiers de configuration créés"

# 6. Vérification finale
print_step "Vérification finale de l'installation..."

echo ""
print_info "✅ Installation terminée avec succès!"
echo ""
print_info "📋 Prochaines étapes recommandées:"
echo "   1. git remote add origin https://github.com/thra8/my-cascade-brain.git"
echo "   2. git push -u origin main"
echo "   3. python3 windsurf/scripts/sentinel.py"
echo ""
print_info "🎯 Alias de terminal recommandés (ajouter à ~/.zshrc):"
echo "   alias brain='python3 $(pwd)/windsurf/scripts/sentinel.py'"
echo "   alias sync='python3 $(pwd)/windsurf/scripts/sentinel.py'"
echo "   alias monitor='python3 $(pwd)/windsurf_monitor.py'"
echo ""
print_info "🔐 Configuration SSH GitHub requise:"
echo "   ssh -T git@github.com"
echo ""
print_success "🚀 Environnement Cascade Architect prêt!"
