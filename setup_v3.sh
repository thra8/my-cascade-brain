#!/bin/bash
# AXE System - Migration Native M1 & Python 3.12
echo "🚀 Démarrage de la migration AXE v3..."

# 1. Réinstallation de Homebrew en natif si nécessaire
if [[ $(file $(which brew)) != *"arm64"* ]]; then
    echo "⚠️ Homebrew Rosetta détecté. Migration en cours..."
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
else
    echo "✅ Homebrew est déjà natif."
fi

# 2. Installation de Python 3.12 (Plus rapide de 25%)
echo "🐍 Installation de Python 3.12 via Homebrew..."
brew install python@3.12

# 3. Nettoyage des liens
brew cleanup
echo "✨ Migration terminée. Relance ton terminal."
