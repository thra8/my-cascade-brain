import inspect
import os, sys, subprocess, datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel

console = Console()

class AXESystem:
    def __init__(self):
        self.base_path = "windsurf/memory"
        self._check_rosetta() # Health Check silencieux au démarrage

    def _check_rosetta(self):
        """[SILENT] Vérifie si Rosetta pollue le processus actuel."""
        is_rosetta = subprocess.getoutput("sysctl -n sysctl.proc_translated") == "1"
        if is_rosetta:
            console.print("[bold red]⚠️ ALERT: Cascade tourne via Rosetta. Perte de perf détectée.[/bold red]")

    def help(self, *args):
        """🚀 Affiche ce menu d'aide (Découverte automatique des outils)."""
        table = Table(title="🚀 AXE COMMAND CENTER v2.3", header_style="bold magenta")
        table.add_column("Commande", style="bold yellow")
        table.add_column("Description / Usage", style="white")

        # --- AUTO-DISCOVERY DES COMMANDES ---
        # On scanne toutes les méthodes de la classe AXESystem
        for name, func in inspect.getmembers(self, predicate=inspect.ismethod):
            if not name.startswith("_") and name != "help":
                # La description est tirée directement de la docstring de la fonction
                description = func.__doc__ or "Aucune description fournie."
                table.add_row(f"/{name}", description.strip().split('\n')[0])
        
        console.print(table)
        
        # --- AUTO-DISCOVERY DES SKILLS (MÉMOIRE) ---
        if os.path.exists(self.base_path):
            categories = [d for d in os.listdir(self.base_path) if os.path.isdir(os.path.join(self.base_path, d))]
            if categories:
                console.print(f"\n[dim]📂 Compétences actives : {', '.join(categories).upper()}[/dim]")

    def audit(self, *args):
        """🛡️ Analyse la sincérité binaire et la santé du système M1."""
        import platform
        arch = platform.machine()
        is_native_os = arch == "arm64"
        
        console.print(Panel(
            f"💻 OS Architecture: [bold green]{arch}[/bold green]\n"
            f"🐍 Python Version: [bold green]{sys.version.split()[0]}[/bold green]",
            title="🛡️ SYSTEM ARCH AUDIT", border_style="cyan"
        ))

        table = Table(box=None, header_style="bold magenta")
        table.add_column("Outil", style="white")
        table.add_column("Chemin", style="dim")
        table.add_column("Architecture", justify="center")

        tools = ["brew", "node", "git", "python3", "docker"]
        for tool in tools:
            path = subprocess.getoutput(f"which {tool}")
            if "not found" in path or not path:
                table.add_row(tool, "❌ Non installé", "[red]-[/red]")
                continue
            
            # Extraction de l'architecture réelle du binaire
            binary_info = subprocess.getoutput(f"file {os.path.realpath(path)}")
            is_arm = "arm64" in binary_info
            
            status = "[green]Natif (arm64) ✅[/green]" if is_arm else "[bold red]Rosetta (x86_64) ⚠️[/bold red]"
            table.add_row(tool, path, status)

        console.print(table)
        
        # Check des processus Rosetta actifs
        rosetta_count = subprocess.getoutput("ps aux | grep oahd | grep -v grep | wc -l").strip()
        if int(rosetta_count) > 0:
            console.print(f"\n[yellow]⚠️ Attention : Rosetta 2 est actif ({rosetta_count} processus).[/yellow]")
        else:
            console.print("\n[green]✨ Zéro processus Rosetta détecté. Environnement 100% pur M1.[/green]")

    def ingest(self, *args):
        """📥 Apprend une nouvelle compétence : /ingest [cat] [titre] [contenu]"""
        if len(args) < 3: 
            console.print("[red]❌ Usage: /ingest [catégorie] [titre] [contenu][/red]")
            return
        
        cat, title, content = args[0], args[1], " ".join(args[2:])
        path = os.path.join(self.base_path, cat.lower(), "skills.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n### {title} ({datetime.date.today()})\n{content.strip()}\n")
        
        console.print(f"✅ Skill '{title}' -> {cat.upper()}")

    def find(self, *args):
        """🔍 Recherche une compétence dans la mémoire : /find [mot-clé]"""
        if not args:
            console.print("[red]❌ Usage: /find [mot-clé][/red]")
            return
            
        query = " ".join(args).lower()
        found = False
        
        # Parcourir tous les fichiers skills.md
        for root, _, files in os.walk(self.base_path):
            if "skills.md" in files:
                path = os.path.join(root, "skills.md")
                with open(path, "r", encoding="utf-8") as f:
                    content = f.read()
                    # Découper par sections ###
                    sections = content.split("### ")
                    for section in sections:
                        if query in section.lower():
                            lines = section.strip().split('\n')
                            title = lines[0] if lines else "Sans titre"
                            console.print(Panel(
                                f"[dim]{os.path.relpath(root, self.base_path).upper()}[/dim]\n\n{section.strip()[:200]}...",
                                title=f"📍 {title}",
                                border_style="green"
                            ))
                            found = True
        
        if not found:
            console.print(f"[yellow]⚠️ Aucune compétence trouvée pour '{query}'[/yellow]")

    def dash(self, *args):
        """📊 Affiche le dashboard de l'état du système."""
        table = Table(title="🧠 AXE DASHBOARD", box=None)
        table.add_column("Catégorie", style="cyan")
        table.add_column("Skills", justify="right", style="green")
        
        total = 0
        for root, _, files in os.walk(self.base_path):
            if "skills.md" in files:
                cat = os.path.relpath(root, self.base_path).upper()
                if cat == ".":
                    cat = "ROOT"
                
                with open(os.path.join(root, "skills.md"), "r", encoding="utf-8") as f:
                    count = len([line for line in f if line.strip().startswith("### ")])
                    table.add_row(cat, str(count))
                    total += count
        
        console.print(Panel(table, subtitle=f"Total: {total}"))

    def sync(self, *args):
        """💾 Synchronise les compétences sur GitHub."""
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            for cmd in [["git", "add", "."], ["git", "commit", "-m", f"🧠 AXE Update: {ts}"], ["git", "push"]]:
                subprocess.run(cmd, capture_output=True, check=True)
            console.print(f"✅ Sentinel Sync OK ({ts})")
        except Exception as e:
            console.print(f"❌ Sync Error: {e}")

    def fix(self, *args):
        """🔧 Répare et installe les dépendances M1."""
        console.print("[bold yellow]🔧 Maintenance AXE...[/bold yellow]")
        os.makedirs(self.base_path, exist_ok=True)
        
        libs = ["numpy", "textual", "psutil", "rich", "mlx"]
        try:
            subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + libs)
            console.print("✅ Environnement M1 stabilisé.")
        except Exception as e:
            console.print(f"❌ Erreur d'installation: {e}")

    def purge(self, *args):
        """🧹 Nettoie les caches Python."""
        console.print("[bold red]🧹 Purge des caches...[/bold red]")
        subprocess.run("find . -name '__pycache__' -exec rm -rf {} +", shell=True)
        console.print("✅ Système nettoyé.")

    def orchestrate(self, *args):
        """👥 Lance un débat technique multi-experts : /orchestrate [sujet]"""
        if not args:
            console.print("[red]❌ Usage: /orchestrate [sujet technique][/red]")
            return
            
        sujet = " ".join(args)
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        
        console.print(Panel(
            f"[bold cyan]👥 ORCHESTRATION MULTI-AGENTS[/bold cyan]\n"
            f"[dim]Sujet : {sujet}[/dim]\n"
            f"[dim]Timestamp : {timestamp}[/dim]",
            title="🎯 Scrum Technique Interne",
            border_style="blue"
        ))
        
        # Créer le répertoire decisions si nécessaire
        decisions_dir = os.path.join(self.base_path, "decisions")
        os.makedirs(decisions_dir, exist_ok=True)
        
        # Perspectives des 3 experts
        experts = {
            "Lead Dev": {
                "focus": "Performance & Scalabilité",
                "concerns": [
                    "Optimisation M1 native",
                    "Gestion mémoire unifiée",
                    "Architecture microservices",
                    "Cache et CDN"
                ]
            },
            "UX Lead": {
                "focus": "Accessibilité & Design",
                "concerns": [
                    "WCAG compliance",
                    "Responsive design",
                    "Performance perçue",
                    "Micro-interactions"
                ]
            },
            "Security Officer": {
                "focus": "Sécurité & Conformité",
                "concerns": [
                    "OWASP Top 10",
                    "Data encryption",
                    "Authentication",
                    "Audit trails"
                ]
            }
        }
        
        # Générer le débat
        debate_content = f"# Orchestration : {sujet}\n\n**Date** : {timestamp}\n\n"
        
        for expert, data in experts.items():
            console.print(f"\n[bold magenta]🎙️ {expert} - {data['focus']}[/bold magenta]")
            
            perspective = f"## {expert}\n**Focus** : {data['focus']}\n\n**Concerns** :\n"
            for concern in data['concerns']:
                bullet = f"• {concern}"
                console.print(f"  {bullet}")
                perspective += f"{bullet}\n"
            
            perspective += f"\n**Recommandation** : Basé sur {data['focus'].lower()}, je recommande...\n\n"
            debate_content += perspective + "---\n\n"
        
        # Recommandation consolidée
        console.print(f"\n[bold green]📋 RECOMMANDATION CONSOLIDÉE[/bold green]")
        recommendation = "## Recommandation Architecte\n\nAprès analyse des 3 perspectives, l'architecture optimale doit :\n\n"
        recommendation += "1. **Performance** : Optimiser pour M1 native avec MLX/Accelerate\n"
        recommendation += "2. **UX** : Garantir WCAG AA et responsive design\n"
        recommendation += "3. **Sécurité** : Implémenter OWASP Top 10 et encryption\n\n"
        recommendation += f"**Décision** : Approche progressive avec validation continue.\n"
        
        console.print(recommendation)
        debate_content += recommendation
        
        # Sauvegarder le compte-rendu
        filename = f"decision_{datetime.datetime.now().strftime('%Y%m%d_%H%M%S')}.md"
        filepath = os.path.join(decisions_dir, filename)
        
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(debate_content)
        
        console.print(f"\n[green]✅ Compte-rendu sauvegardé : {filepath}[/green]")

    def hello(self, *args):
        """👋 Dit bonjour à l'Architecte."""
        console.print("[bold green]👋 Salut Architecte! Prêt pour la mission M1?[/bold green]")

# --- DISPATCHER DYNAMIQUE ---
if __name__ == "__main__":
    axe = AXESystem()
    cmd = sys.argv[1].replace("/", "") if len(sys.argv) > 1 else "help"
    
    # Le dispatcher cherche maintenant directement dans les méthodes de l'objet
    if hasattr(axe, cmd) and not cmd.startswith("_"):
        method = getattr(axe, cmd)
        method(*sys.argv[2:])
    else:
        axe.help()
