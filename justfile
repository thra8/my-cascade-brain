# Cascade Architect Justfile
# Commandes rapides pour le développement et la maintenance

# Vérifier l'état de santé complet du système
health:
    python3 windsurf/scripts/check_system.py

# Synchroniser la mémoire avec GitHub
sync:
    python3 windsurf/scripts/sentinel.py

# Lancer le dashboard de monitoring
monitor:
    python3 windsurf_monitor.py

# Lancer le rendu GPU Metal
gpu:
    python3 metal_streamer.py

# Démonstration des skills
demo:
    python3 skills/metal-gpu-rendering/metal_demo.py

# Nettoyer les fichiers temporaires
cleanup:
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name ".DS_Store" -delete

# Valider les fichiers de mémoire
validate:
    python3 windsurf/scripts/skill_ingest.py --validate

# Lister les compétences récentes
skills:
    python3 windsurf/scripts/skill_ingest.py --list

# Configuration Git
git-setup:
    git remote add origin https://github.com/thra8/my-cascade-brain.git
    git push -u origin main

# Installation complète
install:
    ./setup_cascade_pro.sh

# Test de performance terminal
perf-test:
    python3 -c "import numpy as np, time, sys; [sys.stdout.write(f'\x1b[38;2;{np.random.randint(0,255)};{np.random.randint(0,255)};{np.random.randint(0,255)}m{chr(np.random.randint(33,126))}') or sys.stdout.flush() or time.sleep(0.001) for _ in range(10000)]"

# Aide
help:
    @echo "Commandes disponibles:"
    @echo "  just health      - Vérifier l'état de santé du système"
    @echo "  just sync        - Synchroniser avec GitHub"
    @echo "  just monitor     - Lancer le dashboard"
    @echo "  just gpu         - Lancer le rendu GPU Metal"
    @echo "  just demo        - Démonstration des skills"
    @echo "  just cleanup     - Nettoyer les fichiers temporaires"
    @echo "  just validate    - Valider les fichiers de mémoire"
    @echo "  just skills      - Lister les compétences"
    @echo "  just git-setup   - Configurer Git"
    @echo "  just install     - Installation complète"
    @echo "  just perf-test    - Test de performance terminal"
    @echo "  just help        - Afficher cette aide"

# Développement - Lancer tous les tests
test: health validate
    @echo "✅ Tests terminés"

# Workflow complet - Installation, configuration, test
setup: install git-sync health
    @echo "🚀 Cascade Architect est prêt!"

# Synchronisation Git
git-sync:
    git add .
    git commit -m "Auto-sync from Cascade Architect"
    git push

# Backup complet
backup:
    @echo "📋 Création d'un backup complet..."
    mkdir -p backups
    tar -czf backups/cascade-backup-$(date +%Y%m%d_%H%M%S).tar.gz \
        windsurf/ \
        *.md \
        *.py \
        *.sh \
        .gitignore \
        justfile
    @echo "✅ Backup créé dans backups/"

# Status du projet
status:
    @echo "📊 Statut du projet Cascade Architect:"
    @echo "==============================="
    @echo "📁 Répertoire: $(pwd)"
    @echo "🔧 Git:"
    @git status --porcelain
    @echo "📊 Fichiers de mémoire:"
    @ls -la windsurf/memory/
    @echo "📝 Dernier sync:"
    @git log -1 --oneline 2>/dev/null || echo "Pas de commits"

# Mise à jour des dépendances
update:
    @echo "📦 Mise à jour des dépendances..."
    python3 -m pip install --upgrade pyobjc-framework-Metal pyobjc-framework-Cocoa numpy psutil rich

# Vérification des permissions
fix-perms:
    @echo "🔧 Correction des permissions..."
    chmod +x windsurf/scripts/*.py
    chmod +x *.sh
    chmod +x windsurf_monitor.py
    @echo "✅ Permissions corrigées"

# Diagnostic avancé
full-diagnostic: health perf-test validate
    @echo "🔍 Diagnostic complet terminé"

# Mode développement
dev:
    @echo "🚀 Mode développement activé"
    @echo "Terminal 1: just monitor"
    @echo "Terminal 2: just sync"
    @echo "Terminal 3: just gpu"

# Mode production
prod:
    @echo "🏭 Mode production"
    just cleanup
    just validate
    just sync
    @echo "✅ Prêt pour la production"

# Gestion des compétences
ingest-skill:
    @echo "📥 Ingestion de compétence (usage: just ingest-skill 'contenu')"
    @if [ -z "$(ARGS)" ]; then \
        echo "Usage: just ingest-skill 'contenu à ingérer'"; \
        exit 1; \
    fi
    python3 windsurf/scripts/skill_ingest.py "$(ARGS)"

# Test d'ingestion
test-ingest:
    python3 windsurf/scripts/skill_ingest.py "Test d'ingestion automatique - $(date)"

# Reset complet (dangerux)
reset:
    @echo "⚠️  ATTENTION: Ceci va réinitialiser tout!"
    @echo "Appuyez sur Ctrl+C pour annuler..."
    @sleep 5
    git clean -fd
    git reset --hard HEAD
    ./setup_cascade_pro.sh
    @echo "✅ Reset complet terminé"

# Documentation
docs:
    @echo "📚 Documentation Cascade Architect:"
    @echo "==============================="
    @echo "📖 Fichier principal: CASCADE_CONTROL_CENTER.md"
    @echo "🔧 Configuration: .windsurfrules"
    @echo "🧠 Mémoire: windsurf/memory/"
    @echo "🛠️ Scripts: windsurf/scripts/"
    @echo "🌐 GitHub: https://github.com/thra8/my-cascade-brain"

# Monitoring en continu
watch:
    @echo "👀 Monitoring continu (Ctrl+C pour arrêter)"
    @while true; do \
        clear; \
        just status; \
        echo "🕐 $(date)"; \
        sleep 30; \
    done

# Performance benchmark
benchmark:
    @echo "🏃 Benchmark de performance..."
    @echo "NumPy:"
    python3 -c "import numpy as np, time; t=time.time(); np.dot(np.random.rand(1000,1000), np.random.rand(1000,1000)); print(f'Temps: {time.time()-t:.3f}s')"
    @echo "Terminal:"
    python3 -c "import time, sys; t=time.time(); [sys.stdout.write('.') or sys.stdout.flush() for _ in range(1000)]; print(f'\nTemps: {time.time()-t:.3f}s')"
    @echo "✅ Benchmark terminé"

# Vérification des signaux d'alerte
alerts:
    @echo "🚨 Vérification des signaux d'alerte:"
    @echo "================================="
    @echo "🔐 Permissions:"
    @if [ ! -x windsurf/scripts/skill_ingest.py ]; then echo "❌ skill_ingest.py non exécutable"; fi
    @if [ ! -x windsurf/scripts/sentinel.py ]; then echo "❌ sentinel.py non exécutable"; fi
    @if [ ! -x windsurf_monitor.py ]; then echo "❌ windsurf_monitor.py non exécutable"; fi
    @echo "📁 Fichiers critiques:"
    @if [ ! -f .windsurfrules ]; then echo "❌ .windsurfrules manquant"; fi
    @if [ ! -f windsurf/memory/identity.md ]; then echo "❌ identity.md manquant"; fi
    @if [ ! -f windsurf/memory/skills.md ]; then echo "❌ skills.md manquant"; fi
    @echo "🔄 Git:"
    @if [ -z "$(git remote get-url origin 2>/dev/null)" ]; then echo "❌ Pas de remote Git"; fi
    @if [ -n "$(git status --porcelain)" ]; then echo "⚠️  Modifications non commitées"; fi
    @echo "✅ Vérification terminée"

# Mode sécurité
security:
    @echo "🔒 Vérification de sécurité:"
    @echo "=========================="
    @echo "🔑 Clés API:"
    @if [ -n "$OPENAI_API_KEY" ]; then echo "✅ OPENAI_API_KEY configurée"; else echo "⚠️  OPENAI_API_KEY non configurée"; fi
    @if [ -n "$ANTHROPIC_API_KEY" ]; then echo "✅ ANTHROPIC_API_KEY configurée"; else echo "⚠️  ANTHROPIC_API_KEY non configurée"; fi
    @echo "📁 Permissions:"
    @ls -la windsurf/scripts/*.py | grep -v "rwx"
    @echo "🔐 Git:"
    @git remote -v
    @echo "✅ Vérification sécurité terminée"
