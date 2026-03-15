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
