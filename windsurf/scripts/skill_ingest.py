#!/usr/bin/env python3
"""
Skill Ingestion Script - Cascade AI System
Outil pour intégrer de nouvelles compétences dans la mémoire de manière structurée
"""

import sys
import os
import re
from datetime import datetime
from pathlib import Path

SKILLS_FILE = "windsurf/memory/skills.md"
BACKUP_DIR = "windsurf/memory/backups"

class SkillIngestor:
    """Gestionnaire d'ingestion de compétences pour Cascade"""
    
    def __init__(self):
        self.skills_file = Path(SKILLS_FILE)
        self.backup_dir = Path(BACKUP_DIR)
        self.max_section_length = 1000  # Limiter la taille des sections
        
        # Créer les répertoires nécessaires
        self.skills_file.parent.mkdir(parents=True, exist_ok=True)
        self.backup_dir.mkdir(parents=True, exist_ok=True)
        
        # Patterns de nettoyage
        self.cleanup_patterns = [
            (r'```[\w]*\n', ''),  # Supprimer les blocs de code
            (r'```', ''),          # Supprimer les fin de blocs
            (r'!\[.*?\]\(.*?\)', ''),  # Supprimer les images markdown
            (r'<.*?>', ''),        # Supprimer les balises HTML
            (r'\[.*?\]\(#.*?\)', ''),  # Simplifier les liens
            (r'#{1,6}\s*', ''),     # Supprimer les titres markdown
            (r'\*\*(.*?)\*\*', r'\1'),  # Supprimer le gras mais garder le texte
            (r'\*(.*?)\*', r'\1'),     # Supprimer l'italique mais garder le texte
            (r'`([^`]+)`', r'\1'),      # Supprimer le code inline mais garder le texte
            (r'\n\s*\n', '\n'),  # Réduire les sauts de ligne multiples
            (r'^\s*[-*+]\s*', ''), # Supprimer les puces au début
            (r'^\s*\d+\.\s*', ''), # Supprimer les numéros au début
        ]
    
    def backup_skills_file(self):
        """Créer une sauvegarde du fichier skills"""
        if self.skills_file.exists():
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            backup_file = self.backup_dir / f"skills_backup_{timestamp}.md"
            
            with open(self.skills_file, 'r', encoding='utf-8') as src:
                with open(backup_file, 'w', encoding='utf-8') as dst:
                    dst.write(src.read())
            
            print(f"📋 Backup créé: {backup_file}")
            return True
        return False
    
    def clean_content(self, content: str) -> str:
        """Nettoyer et formater le contenu"""
        # Supprimer les patterns indésirables
        for pattern, replacement in self.cleanup_patterns:
            content = re.sub(pattern, replacement, content, flags=re.MULTILINE | re.DOTALL)
        
        # Nettoyer les espaces multiples
        content = re.sub(r' +', ' ', content)
        content = re.sub(r'\n+', '\n', content)
        
        # Mettre en majuscule le début des phrases
        content = '. '.join(sentence.capitalize() for sentence in content.split('. '))
        
        # Supprimer les lignes vides au début et à la fin
        content = content.strip()
        
        return content
    
    def format_content(self, content: str, source: str = "Unknown") -> str:
        """Formater le contenu selon les standards Architect"""
        # Nettoyer le contenu
        cleaned_content = self.clean_content(content)
        
        # Limiter la longueur
        if len(cleaned_content) > self.max_section_length:
            cleaned_content = cleaned_content[:self.max_section_length] + "..."
        
        # Structurer en sections
        formatted_content = f"""
### 📥 {source} - {datetime.now().strftime("%Y-%m-%d %H:%M")}

#### 🎯 Core Concepts
{self._extract_key_concepts(cleaned_content)}

#### ⚡ Implementation Details
{self._extract_implementation_details(cleaned_content)}

#### 🔧 M1 Optimizations
{self._extract_m1_optimizations(cleaned_content)}

#### 📋 Quick Reference
{self._create_quick_reference(cleaned_content)}

---
"""
        
        return formatted_content.strip()
    
    def _extract_key_concepts(self, content: str) -> str:
        """Extraire les concepts clés du contenu"""
        # Extraire les mots-clés techniques
        technical_terms = [
            'Metal', 'GPU', 'M1', 'unified memory', 'zero-copy', 'pyobjc',
            'rendering', 'performance', 'architecture', 'framework'
        ]
        
        concepts = []
        content_lower = content.lower()
        
        for term in technical_terms:
            if term.lower() in content_lower:
                concepts.append(term)
        
        # Extraire les patterns de code
        code_patterns = [
            r'([a-zA-Z_][a-zA-Z0-9_]*(?:\.[a-zA-Z_][a-zA-Z0-9_]*)*)',
            r'(?:using|utilize|leverage|implement|apply)\s+([a-zA-Z_][a-zA-Z0-9_]*)',
        ]
        
        for pattern in code_patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    concepts.extend(match)
                else:
                    concepts.append(match)
        
        # Nettoyer et dédupliquer
        unique_concepts = list(set([c.strip() for c in concepts if len(c.strip()) > 2]))
        
        if unique_concepts:
            return "\n".join(f"- **{concept}**" for concept in unique_concepts[:5])
        else:
            return "- *Analyse du contenu en cours...*"
    
    def _extract_implementation_details(self, content: str) -> str:
        """Extraire les détails d'implémentation"""
        details = []
        
        # Patterns de code simplifiés
        patterns = [
            r'import\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'from\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'([a-zA-Z_][a-zA-Z0-9_]*)\s*\(',
            r'function\s+([a-zA-Z_][a-zA-Z0-9_]*)',
            r'class\s+([A-Z][a-zA-Z0-9_]*)',
        ]
        
        for pattern in patterns:
            matches = re.findall(pattern, content, re.IGNORECASE)
            for match in matches:
                if isinstance(match, tuple):
                    details.extend(match)
                else:
                    details.append(match)
        
        # Nettoyer et dédupliquer
        unique_details = list(set([d.strip() for d in details if len(str(d).strip()) > 2]))
        
        if unique_details:
            return "\n".join(f"- `{detail}`" for detail in unique_details[:5])
        else:
            return "- *Implémentation à analyser...*"
    
    def _extract_m1_optimizations(self, content: str) -> str:
        """Extraire les optimisations M1"""
        m1_keywords = [
            'arm64', 'm1', 'apple silicon', 'accelerate', 'metal', 'unified memory',
            'vectorized', 'simd', 'neon', 'performance', 'optimization', 'numpy'
        ]
        
        optimizations = []
        lines = content.split('\n')
        
        for line in lines:
            line_lower = line.lower()
            if any(keyword in line_lower for keyword in m1_keywords):
                # Nettoyer la ligne
                clean_line = re.sub(r'[^\w\s\.]', '', line).strip()
                if len(clean_line) > 10:
                    optimizations.append(clean_line)
        
        if optimizations:
            return "\n".join(f"- {opt}" for opt in optimizations[:3])
        else:
            return "- *Optimisations M1 à identifier...*"
    
    def _create_quick_reference(self, content: str) -> str:
        """Créer une référence rapide"""
        # Extraire les commandes ou snippets utiles
        command_patterns = [
            r'```bash\n([^`]+)```',
            r'```sh\n([^`]+)```',
            r'```python\n([^`]+)```',
            r'`([^`]+)`',
        ]
        
        commands = []
        for pattern in command_patterns:
            matches = re.findall(pattern, content, re.DOTALL)
            commands.extend(matches)
        
        if commands:
            return "\n".join(f"- `{cmd.strip()[:50]}...`" for cmd in commands[:3])
        else:
            return "- *Référence rapide à créer...*"
    
    def ensure_skills_file_exists(self):
        """S'assurer que le fichier skills existe"""
        if not self.skills_file.exists():
            with open(self.skills_file, 'w', encoding='utf-8') as f:
                f.write("""# Expert Skills Vault - Cascade AI System

## 🧠 Core Architecture
### M1 Native Optimization
- **Pattern**: NumPy vectorization instead of pixel loops
- **Performance**: 68.8 FPS achieved with 16ms frame budget
- **Braille Unicode**: U+2800 mapping for 2x8 resolution
- **Double Buffering**: Prevents flicker in animations

### Rendering Pipeline
- **No Pixel Loops**: Strict NumPy broadcasting
- **Frame Budget**: 16ms for 60 FPS target
- **Memory Pooling**: Reuse buffers to avoid allocations
- **Thermal Management**: Monitor M1 temperature

---

""")
            print(f"📝 Fichier skills.md créé")
    
    def ingest_skill(self, content: str, source: str = "User Input"):
        """Intégrer une nouvelle compétence"""
        try:
            # Créer une sauvegarde
            self.backup_skills_file()
            
            # S'assurer que le fichier existe
            self.ensure_skills_file_exists()
            
            # Formater le contenu
            formatted_content = self.format_content(content, source)
            
            # Ajouter au fichier skills
            with open(self.skills_file, 'a', encoding='utf-8') as f:
                f.write(formatted_content + "\n\n")
            
            print(f"✅ Compétence intégrée avec succès dans {SKILLS_FILE}")
            print(f"📊 Taille du fichier: {self.skills_file.stat().st_size} bytes")
            return True
            
        except Exception as e:
            print(f"❌ Erreur lors de l'ingestion: {e}")
            import traceback
            traceback.print_exc()
            return False
    
    def validate_skills_file(self):
        """Valider la structure du fichier skills"""
        if not self.skills_file.exists():
            print("❌ Fichier skills.md introuvable")
            return False
        
        try:
            with open(self.skills_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Vérifications de base
            if not content.startswith('#'):
                print("⚠️ Le fichier ne commence pas par un titre Markdown")
            
            # Compter les sections
            sections = len(re.findall(r'^##', content, re.MULTILINE))
            subsections = len(re.findall(r'^###', content, re.MULTILINE))
            
            print(f"📊 Validation: {sections} sections, {subsections} sous-sections")
            print(f"📏 Taille: {len(content)} caractères")
            
            return True
            
        except Exception as e:
            print(f"❌ Erreur de validation: {e}")
            return False
    
    def list_recent_skills(self, count: int = 5):
        """Lister les compétences récemment intégrées"""
        if not self.skills_file.exists():
            print("❌ Fichier skills.md introuvable")
            return
        
        try:
            with open(self.skills_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Extraire les sections récentes
            sections = re.findall(r'### 📥 (.+?)\n(.*?)(?=\n###|\n---|$)', content, re.DOTALL)
            
            print(f"📋 {len(sections)} compétences trouvées")
            print(f"📅 {min(count, len(sections))} plus récentes:")
            
            for i, (title, section_content) in enumerate(sections[-count:]):
                preview = section_content.split('\n')[0] if section_content else "Pas de contenu"
                print(f"  {i+1}. {title}")
                print(f"     {preview[:50]}...")
                
        except Exception as e:
            print(f"❌ Erreur: {e}")


def main():
    """Point d'entrée principal"""
    ingestor = SkillIngestor()
    
    if len(sys.argv) > 1:
        # Mode ingestion
        if sys.argv[1] == "--validate":
            ingestor.validate_skills_file()
        elif sys.argv[1] == "--list":
            count = int(sys.argv[2]) if len(sys.argv) > 2 else 5
            ingestor.list_recent_skills(count)
        else:
            # Récupérer le contenu passé par Cascade
            new_content = " ".join(sys.argv[1:])
            source = "User Input"
            
            # Détecter si c'est une URL
            if new_content.startswith(('http://', 'https://')):
                source = f"URL: {new_content[:50]}..."
            
            success = ingestor.ingest_skill(new_content, source)
            
            if success:
                print("🎯 Compétence prête à être synchronisée avec GitHub")
            else:
                sys.exit(1)
    else:
        print("Usage:")
        print("  python3 skill_ingest.py '<contenu>'          # Ingestion de contenu")
        print("  python3 skill_ingest.py --validate           # Valider le fichier")
        print("  python3 skill_ingest.py --list [count]       # Lister les compétences")
        print("\nExemple:")
        print('  python3 skill_ingest.py "NumPy vectorization for M1 optimization"')


if __name__ == "__main__":
    main()
