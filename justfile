# Cascade Architect Justfile - AXE System Optimized
# Commandes rapides utilisant ax.py (architecture atomique)

# Réparation système complète
fix:
    python3 ax.py fix

# Santé système
health:
    python3 ax.py health

# Synchronisation GitHub
sync:
    python3 ax.py sync

# Nettoyage fichiers temporaires
clean:
    python3 ax.py clean

# Monitoring système
monitor:
    python3 ax.py monitor

# Ingestion de compétences
ingest category title content:
    python3 ax.py ingest {{category}} {{title}} {{content}}

# Clone et analyse de dépôt GitHub
git url:
    python3 ax.py git {{url}}

# Aide
help:
    python3 ax.py help

# Installation complète (Python 3.12 + AXE)
install:
    @echo "🐍 Installation Python 3.12..."
    brew install python@3.12
    @echo "📦 Création environnement virtuel..."
    python3.12 -m venv venv
    @echo "📦 Installation dépendances..."
    source venv/bin/activate && pip install -r requirements.txt
    @echo "⚡ Configuration AXE..."
    python3 ax.py fix
    @echo "✅ Installation AXE terminée"

# Workflow complet - Installation et test
setup: install health
    @echo "🚀 Cascade Architect AXE est prêt!"

# Synchronisation Git
git-sync:
    git add .
    git commit -m "Auto-sync from AXE System"
    git push

# Status du projet
status:
    @echo "📊 Statut du projet Cascade Architect AXE:"
    @echo "==============================="
    @echo "📁 Répertoire: $(pwd)"
    @echo "🐍 Python: $(python3 --version 2>/dev/null || echo 'Non disponible')"
    @echo "⚡ AXE System: $(python3 ax.py health 2>/dev/null | head -5 || echo 'Non disponible')"
    @echo "🔧 Git:"
    @git status --porcelain
    @echo "📝 Dernier sync:"
    @git log -1 --oneline 2>/dev/null || echo "Pas de commits"

# Backup complet
backup:
    @echo "📋 Création d'un backup complet AXE..."
    mkdir -p backups
    tar -czf backups/cascade-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
        ax.py \
        .windsurfrules \
        windsurf/ \
        *.md \
        requirements.txt \
        .python-version \
        justfile
    @echo "✅ Backup créé dans backups/"

# Mise à jour des dépendances
update:
    @echo "📦 Mise à jour des dépendances AXE..."
    source venv/bin/activate && pip install --upgrade numpy psutil rich textual pyobjc-framework-Metal pyobjc-framework-Cocoa

# Diagnostic complet
full-diagnostic: health monitor
    @echo "🔍 Diagnostic AXE complet terminé"

# Mode développement
dev:
    @echo "🚀 Mode développement AXE activé"
    @echo "Commandes disponibles:"
    @echo "  /f - Réparer système"
    @echo "  /h - Santé système"
    @echo "  /s - Synchroniser GitHub"
    @echo "  /i [cat] [title] [content] - Ingestion"

# Mode production
prod:
    @echo "🏭 Mode production AXE"
    just clean
    just health
    just sync
    @echo "✅ Prêt pour la production"

# Test d'ingestion
test-ingest:
    python3 ax.py ingest test "Test AXE" "Test d'ingestion automatique via AXE System"

# Documentation
docs:
    @echo "📚 Documentation Cascade Architect AXE:"
    @echo "==============================="
    @echo "📖 Fichier principal: ax.py"
    @echo "🔧 Configuration: .windsurfrules"
    @echo "🧠 Mémoire: windsurf/memory/"
    @echo "🌐 GitHub: https://github.com/thra8/my-cascade-brain"
    @echo "🐍 Python: 3.12.13 (optimisé pour M1)"
    @echo "⚡ Architecture: Atomique (single file)"

# Monitoring en continu
watch:
    @echo "👀 Monitoring continu AXE (Ctrl+C pour arrêter)"
    @while true; do \
        clear; \
        just status; \
        echo "🕐 $(date)"; \
        sleep 30; \
    done

# Performance benchmark
benchmark:
    @echo "🏃 Benchmark AXE Performance:"
    @echo "=========================="
    @echo "🔍 Version Python:"
    python3 --version
    @echo "📊 Santé système:"
    python3 ax.py health
    @echo "⚡ Monitoring:"
    python3 ax.py monitor
    @echo "✅ Benchmark terminé"

# Vérification des signaux d'alerte
alerts:
    @echo "🚨 Vérification des signaux d'alerte AXE:"
    @echo "================================="
    @echo "🔐 Fichiers critiques:"
    @if [ ! -f ax.py ]; then echo "❌ ax.py manquant"; else echo "✅ ax.py présent"; fi
    @if [ ! -f .windsurfrules ]; then echo "❌ .windsurfrules manquant"; else echo "✅ .windsurfrules présent"; fi
    @if [ ! -d windsurf/memory ]; then echo "❌ windsurf/memory manquant"; else echo "✅ windsurf/memory présent"; fi
    @echo "🔄 Git:"
    @if [ -z "$(git remote get-url origin 2>/dev/null)" ]; then echo "❌ Pas de remote Git"; else echo "✅ Remote GitHub configuré"; fi
    @if [ -n "$(git status --porcelain)" ]; then echo "⚠️  Modifications non commitées"; else echo "✅ Repository propre"; fi
    @echo "🐍 Environnement:"
    @if [ ! -d venv ]; then echo "❌ venv non trouvé"; else echo "✅ venv présent"; fi
    @if [ ! -f requirements.txt ]; then echo "❌ requirements.txt manquant"; else echo "✅ requirements.txt présent"; fi
    @echo "✅ Vérification terminée"

# Mode sécurité
security:
    @echo "🔒 Vérification de sécurité AXE:"
    @echo "=========================="
    @echo "🐍 Version Python:"
    python3 --version
    @echo "🔑 Clés API:"
    @if [ -n "$OPENAI_API_KEY" ]; then echo "✅ OPENAI_API_KEY configurée"; else echo "⚠️  OPENAI_API_KEY non configurée"; fi
    @if [ -n "$ANTHROPIC_API_KEY" ]; then echo "✅ ANTHROPIC_API_KEY configurée"; else echo "⚠️  ANTHROPIC_API_KEY non configurée"; fi
    @echo "📁 Permissions:"
    @ls -la ax.py | grep -v "rwx"
    @echo "🔐 Git:"
    @git remote -v
    @echo "✅ Vérification sécurité terminée"

# Activation de l'environnement
activate:
    @echo "🔗 Activation environnement virtuel Python 3.12..."
    source venv/bin/activate && echo "✅ Environnement activé"
    @echo "📦 Packages installés:"
    source venv/bin/activate && pip list

# Aide complète
help:
    @echo "🚀 Commandes AXE System:"
    @echo "======================"
    @echo "Commandes principales:"
    @echo "  just fix      - Réparer infrastructure"
    @echo "  just health   - Santé système"
    @echo "  just sync     - Synchroniser GitHub"
    @echo "  just clean    - Nettoyer fichiers temporaires"
    @echo "  just monitor  - Monitoring système"
    @echo "  just help     - Afficher cette aide"
    @echo ""
    @echo "Commandes avancées:"
    @echo "  just install  - Installation complète"
    @echo "  just setup    - Installation + test"
    @echo "  just benchmark - Performance tests"
    @echo "  just backup   - Backup complet"
    @echo ""
    @echo "Ingestion:"
    @echo "  just ingest python 'NumPy Tricks' 'Vectorization explanation'"
    @echo ""
    @echo "Monitoring:"
    @echo "  just watch    - Monitoring continu"
    @echo "  just status   - Statut projet"
    @echo "  just alerts   - Signaux d'alerte"
