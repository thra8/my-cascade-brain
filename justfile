# Cascade Architect Justfile - Python 3.12 Optimized
# Commandes rapides pour le développement et la maintenance

# Vérifier l'état de santé complet du système
health:
    source venv/bin/activate && python3 windsurf/scripts/check_system.py

# Synchroniser la mémoire avec GitHub
sync:
    source venv/bin/activate && python3 windsurf/scripts/sentinel.py

# Lancer le dashboard de monitoring
monitor:
    source venv/bin/activate && python3 windsurf_monitor.py

# Lancer le rendu GPU Metal
gpu:
    source venv/bin/activate && python3 metal_streamer.py

# Démonstration des skills
demo:
    source venv/bin/activate && python3 skills/metal-gpu-rendering/metal_demo.py

# Nettoyer les fichiers temporaires
cleanup:
    find . -name "*.pyc" -delete
    find . -name "__pycache__" -type d -exec rm -rf {} + 2>/dev/null || true
    find . -name ".DS_Store" -delete

# Valider les fichiers de mémoire
validate:
    source venv/bin/activate && python3 windsurf/scripts/skill_ingest.py --validate

# Lister les compétences récentes
skills:
    source venv/bin/activate && python3 windsurf/scripts/skill_ingest.py --list

# Configuration Git
git-setup:
    git remote add origin https://github.com/thra8/my-cascade-brain.git
    git push -u origin main

# Installation complète (Python 3.12)
install:
    @echo "🐍 Installation Python 3.12..."
    brew install python@3.12
    @echo "📦 Création environnement virtuel..."
    python3.12 -m venv venv
    @echo "📦 Installation dépendances..."
    source venv/bin/activate && pip install -r requirements.txt
    @echo "✅ Installation terminée"

# Test de performance terminal
perf-test:
    source venv/bin/activate && python3 -c "import numpy as np, time, sys; [sys.stdout.write(f'\x1b[38;2;{np.random.randint(0,255)};{np.random.randint(0,255)};{np.random.randint(0,255)}m{chr(np.random.randint(33,126))}') or sys.stdout.flush() or time.sleep(0.001) for _ in range(10000)]"

# Test de performance Python 3.12
benchmark:
    @echo "🚀 Benchmark Python 3.12 Performance:"
    @echo "NumPy:"
    source venv/bin/activate && python3 -c "import numpy as np, time; t=time.time(); np.dot(np.random.rand(1000,1000), np.random.rand(1000,1000)); print(f'Temps: {time.time()-t:.3f}s')"
    @echo "Regex:"
    source venv/bin/activate && python3 -c "import re, time; t=time.time(); re.sub(r'<[^>]*>', '', '<html><body>Test</body></html>'*1000); print(f'Temps: {time.time()-t:.4f}s')"
    @echo "Terminal:"
    source venv/bin/activate && python3 -c "import time, sys; t=time.time(); [sys.stdout.write('.') or sys.stdout.flush() for _ in range(1000)]; print(f'\nTemps: {time.time()-t:.3f}s')"

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
    @echo "  just install     - Installation complète Python 3.12"
    @echo "  just perf-test    - Test de performance terminal"
    @echo "  just benchmark   - Benchmark Python 3.12"
    @echo "  just help        - Afficher cette aide"

# Développement - Lancer tous les tests
test: health validate
    @echo "✅ Tests terminés"

# Workflow complet - Installation, configuration, test
setup: install health
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
        justfile \
        requirements.txt \
        .python-version
    @echo "✅ Backup créé dans backups/"

# Status du projet
status:
    @echo "📊 Statut du projet Cascade Architect:"
    @echo "==============================="
    @echo "📁 Répertoire: $(pwd)"
    @echo "� Python: $(source venv/bin/activate && python3 --version 2>/dev/null || echo 'Non activé')"
    @echo "�🔧 Git:"
    @git status --porcelain
    @echo "📊 Fichiers de mémoire:"
    @ls -la windsurf/memory/
    @echo "📝 Dernier sync:"
    @git log -1 --oneline 2>/dev/null || echo "Pas de commits"

# Mise à jour des dépendances
update:
    @echo "📦 Mise à jour des dépendances..."
    source venv/bin/activate && pip install --upgrade numpy psutil rich textual pyobjc-framework-Metal pyobjc-framework-Cocoa

# Vérification des permissions
fix-perms:
    @echo "🔧 Correction des permissions..."
    chmod +x windsurf/scripts/*.py
    chmod +x *.sh
    chmod +x windsurf_monitor.py
    @echo "✅ Permissions corrigées"

# Diagnostic avancé
full-diagnostic: health perf-test validate benchmark
    @echo "🔍 Diagnostic complet terminé"

# Mode développement
dev:
    @echo "🚀 Mode développement activé (Python 3.12)"
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
    source venv/bin/activate && python3 windsurf/scripts/skill_ingest.py "$(ARGS)"

# Test d'ingestion
test-ingest:
    source venv/bin/activate && python3 windsurf/scripts/skill_ingest.py "Test d'ingestion Python 3.12 - $(date)"

# Reset complet (dangerux)
reset:
    @echo "⚠️  ATTENTION: Ceci va réinitialiser tout!"
    @echo "Appuyez sur Ctrl+C pour annuler..."
    @sleep 5
    git clean -fd
    git reset --hard HEAD
    just setup
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
    @echo "🐍 Python: 3.12.13 (optimisé pour M1)"

# Monitoring en continu
watch:
    @echo "👀 Monitoring continu (Ctrl+C pour arrêter)"
    @while true; do \
        clear; \
        just status; \
        echo "🕐 $(date)"; \
        sleep 30; \
    done

# Performance benchmark complet
full-benchmark:
    @echo "🏃 Benchmark complet Python 3.12:"
    @echo "================================="
    @echo "🔍 Version Python:"
    source venv/bin/activate && python3 --version
    @echo "📊 NumPy Performance:"
    source venv/bin/activate && python3 -c "import numpy as np, time; t=time.time(); result=np.dot(np.random.rand(1000,1000), np.random.rand(1000,1000)); print(f'Matrix multiplication (1000x1000): {time.time()-t:.3f}s')"
    @echo "⚡ Regex Performance:"
    source venv/bin/activate && python3 -c "import re, time; t=time.time(); re.sub(r'<[^>]*>', '', '<html><body>Test</body></html>'*1000); print(f'HTML tag removal (1000x): {time.time()-t:.4f}s')"
    @echo "🖥️ Terminal Performance:"
    source venv/bin/activate && python3 -c "import time, sys; t=time.time(); [sys.stdout.write('.') or sys.stdout.flush() for _ in range(1000)]; print(f'Terminal output (1000 chars): {time.time()-t:.3f}s')"
    @echo "🎨 Color Performance:"
    source venv/bin/activate && python3 -c "import time, sys; t=time.time(); [sys.stdout.write(f'\x1b[38;2;{i%255};{(i*2)%255};{(i*3)%255}m█\x1b[0m') or sys.stdout.flush() for i in range(1000)]; print(f'Color output (1000 chars): {time.time()-t:.3f}s')"
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
    @echo "🐍 Environnement:"
    @if [ ! -d venv ]; then echo "❌ venv non trouvé"; fi
    @if [ ! -f requirements.txt ]; then echo "❌ requirements.txt manquant"; fi
    @echo "✅ Vérification terminée"

# Mode sécurité
security:
    @echo "🔒 Vérification de sécurité:"
    @echo "=========================="
    @echo "� Version Python:"
    @if [ -f venv/bin/python ]; then echo "✅ $(venv/bin/python --version 2>/dev/null | head -1)"; else echo "❌ venv non trouvé"; fi
    @echo "�🔑 Clés API:"
    @if [ -n "$OPENAI_API_KEY" ]; then echo "✅ OPENAI_API_KEY configurée"; else echo "⚠️  OPENAI_API_KEY non configurée"; fi
    @if [ -n "$ANTHROPIC_API_KEY" ]; then echo "✅ ANTHROPIC_API_KEY configurée"; else echo "⚠️  ANTHROPIC_API_KEY non configurée"; fi
    @echo "📁 Permissions:"
    @ls -la windsurf/scripts/*.py | grep -v "rwx"
    @echo "🔐 Git:"
    @git remote -v
    @echo "✅ Vérification sécurité terminée"

# Activation de l'environnement
activate:
    @echo "🔗 Activation environnement virtuel Python 3.12..."
    source venv/bin/activate && echo "✅ Environnement activé"
    @echo "📦 Packages installés:"
    source venv/bin/activate && pip list
