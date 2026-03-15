#!/bin/bash
# Windsurf Memory Sync Tool
# Synchronisation du cerveau Cascade avec GitHub

set -e  # Exit on error

# Configuration
REPO_DIR="$(pwd)"
REMOTE_URL="git@github.com:cascade-ai-system/my-cascade-brain.git"

# Couleurs pour l'affichage
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Fonction d'affichage
print_status() {
    echo -e "${BLUE}🧠 Cascade Brain Sync${NC} | $1"
}

print_success() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Vérifier que le répertoire existe
check_repo_dir() {
    if [ ! -d "$REPO_DIR" ]; then
        print_error "Répertoire windsurf introuvable: $REPO_DIR"
        exit 1
    fi
}

# Initialiser le repository si nécessaire
init_repo() {
    if [ ! -d "$REPO_DIR/.git" ]; then
        print_status "Initialisation du repository Git..."
        cd "$REPO_DIR"
        git init
        git remote add origin "$REMOTE_URL"
        print_success "Repository initialisé"
    else
        cd "$REPO_DIR"
        # Vérifier que le remote existe
        if ! git remote get-url origin >/dev/null 2>&1; then
            git remote add origin "$REMOTE_URL"
            print_success "Remote origin ajouté"
        fi
    fi
}

# Fonction de chargement (Pull)
sync_load() {
    print_status "Chargement des skills depuis GitHub..."
    
    check_repo_dir
    cd "$REPO_DIR"
    
    # Vérifier si on peut faire un pull
    if git rev-parse --git-dir >/dev/null 2>&1; then
        # Fetch pour récupérer les derniers changements
        git fetch origin
        
        # Vérifier s'il y a des changements locaux non commités
        if ! git diff --quiet || ! git diff --cached --quiet; then
            print_warning "Changements locaux détectés"
            print_warning "Sauvegarde locale avec: ./sync.sh save"
            
            # Créer un backup des changements locaux
            BACKUP_DIR="$REPO_DIR/../local_backup_$(date +%Y%m%d_%H%M%S)"
            mkdir -p "$BACKUP_DIR"
            cp -r "$REPO_DIR/memory" "$BACKUP_DIR/"
            print_warning "Backup créé dans: $BACKUP_DIR"
        fi
        
        # Pull des changements
        if git pull origin main; then
            print_success "Skills chargés depuis GitHub"
            
            # Afficher les fichiers chargés
            if [ -f "memory/skills.md" ]; then
                SKILLS_COUNT=$(grep -c "^## " memory/skills.md 2>/dev/null || echo "0")
                print_success "$SKILLS_COUNT skills disponibles"
            fi
            
            if [ -f "memory/identity.md" ]; then
                print_success "Identité Cascade chargée"
            fi
            
            if [ -f "memory/context_snapshot.md" ]; then
                print_success "Contexte actuel chargé"
            fi
            
        else
            print_error "Échec du pull depuis GitHub"
            exit 1
        fi
    else
        print_error "Repository Git non initialisé"
        exit 1
    fi
}

# Fonction de sauvegarde (Push)
sync_save() {
    print_status "Sauvegarde de la mémoire vers GitHub..."
    
    check_repo_dir
    cd "$REPO_DIR"
    
    # Vérifier qu'on est dans un repository Git
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        print_error "Repository Git non initialisé"
        exit 1
    fi
    
    # Ajouter tous les fichiers
    git add .
    
    # Vérifier s'il y a des changements à commit
    if git diff --cached --quiet; then
        print_warning "Aucun changement à sauvegarder"
        return 0
    fi
    
    # Créer le commit
    TIMESTAMP=$(date +'%Y-%m-%d %H:%M:%S')
    COMMIT_MSG="🧠 Evolution: $TIMESTAMP | Cascade Brain Update"
    
    if git commit -m "$COMMIT_MSG"; then
        print_success "Changements commités localement"
        
        # Push vers GitHub
        if git push origin main; then
            print_success "Mémoire synchronisée avec GitHub"
            
            # Afficher les statistiques
            FILES_CHANGED=$(git diff --name-only HEAD~1 HEAD | wc -l)
            print_success "$FILES_CHANGED fichiers synchronisés"
            
        else
            print_error "Échec du push vers GitHub"
            print_warning "Vérifiez votre configuration SSH ou les permissions du repository"
            exit 1
        fi
    else
        print_error "Échec du commit local"
        exit 1
    fi
}

# Fonction de statut
sync_status() {
    print_status "Statut de synchronisation..."
    
    check_repo_dir
    cd "$REPO_DIR"
    
    if ! git rev-parse --git-dir >/dev/null 2>&1; then
        print_error "Repository Git non initialisé"
        return 1
    fi
    
    # Statut Git
    echo
    print_status "Statut Git:"
    git status --porcelain | while read line; do
        if [[ $line == M* ]]; then
            print_warning "Modifié: ${line#M }"
        elif [[ $line == A* ]]; then
            print_success "Ajouté: ${line#A }"
        elif [[ $line == ??* ]]; then
            print_warning "Non suivi: ${line#?? }"
        fi
    done
    
    # Statut des fichiers de mémoire
    echo
    print_status "Fichiers de mémoire:"
    
    for file in memory/skills.md memory/identity.md memory/context_snapshot.md; do
        if [ -f "$file" ]; then
            SIZE=$(wc -l < "$file")
            MODIFIED=$(stat -f "%Sm" "$file" 2>/dev/null || stat -c "%y" "$file" 2>/dev/null)
            print_success "✓ $file ($SIZE lignes, modifié: $MODIFIED)"
        else
            print_warning "✗ $file (manquant)"
        fi
    done
    
    # Dernière synchronisation
    echo
    if git log -1 --format="%h %s" >/dev/null 2>&1; then
        LAST_SYNC=$(git log -1 --format="%h %s")
        print_success "Dernière synchronisation: $LAST_SYNC"
    else
        print_warning "Aucune synchronisation précédente"
    fi
}

# Fonction de validation
validate_memory() {
    print_status "Validation de la mémoire..."
    
    check_repo_dir
    
    # Vérifier les fichiers requis
    REQUIRED_FILES=("memory/skills.md" "memory/identity.md" "memory/context_snapshot.md")
    MISSING_FILES=()
    
    for file in "${REQUIRED_FILES[@]}"; do
        if [ ! -f "$REPO_DIR/$file" ]; then
            MISSING_FILES+=("$file")
        fi
    done
    
    if [ ${#MISSING_FILES[@]} -gt 0 ]; then
        print_error "Fichiers manquants:"
        for file in "${MISSING_FILES[@]}"; do
            print_error "  • $file"
        done
        return 1
    fi
    
    # Valider la structure Markdown
    for file in "${REQUIRED_FILES[@]}"; do
        if [ -f "$REPO_DIR/$file" ]; then
            # Vérifier que le fichier commence par #
            if ! head -1 "$REPO_DIR/$file" | grep -q "^#"; then
                print_warning "$file ne commence pas par un titre Markdown"
            fi
            
            # Vérifier que le fichier n'est pas vide
            if [ ! -s "$REPO_DIR/$file" ]; then
                print_warning "$file est vide"
            fi
        fi
    done
    
    print_success "Validation de la mémoire terminée"
    return 0
}

# Fonction d'aide
show_help() {
    echo "🧠 Cascade Brain Sync Tool"
    echo
    echo "Usage: $0 {load|save|status|validate|help}"
    echo
    echo "Commandes:"
    echo "  load     - Charger les skills depuis GitHub"
    echo "  save     - Sauvegarder les nouveaux skills vers GitHub"
    echo "  status   - Afficher le statut de synchronisation"
    echo "  validate - Valider la structure de la mémoire"
    echo "  help     - Afficher cette aide"
    echo
    echo "Exemples:"
    echo "  $0 load     # Charger au démarrage"
    echo "  $0 save     # Sauvegarder après travail"
    echo "  $0 status   # Vérifier le statut"
}

# Point d'entrée principal
case "$1" in
    load)
        sync_load
        ;;
    save)
        sync_save
        ;;
    status)
        sync_status
        ;;
    validate)
        validate_memory
        ;;
    help|--help|-h)
        show_help
        ;;
    *)
        print_error "Commande inconnue: $1"
        echo
        show_help
        exit 1
        ;;
esac
