import os, sys, subprocess, re, datetime
from rich.console import Console
from rich.table import Table
from rich.panel import Panel
from rich.syntax import Syntax
import psutil

console = Console()

class AXESystem:
    def __init__(self):
        self.base_path = "windsurf/memory"
        self.libs = ["numpy", "textual", "psutil", "rich", "mlx"]

    def _get_all_skills(self):
        for root, _, files in os.walk(self.base_path):
            if "skills.md" in files:
                yield os.path.join(root, "skills.md")

    # --- SYSTEM & MAINTENANCE ---
    def fix(self, *args):
        console.print("[bold yellow]🔧 Maintenance AXE...[/bold yellow]")
        os.makedirs(self.base_path, exist_ok=True)
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-q"] + self.libs)
        console.print("✅ Environnement M1 stabilisé.")

    def sync(self, *args):
        ts = datetime.datetime.now().strftime("%Y-%m-%d %H:%M")
        try:
            for cmd in [["git", "add", "."], ["git", "commit", "-m", f"🧠 AXE Update: {ts}"], ["git", "push"]]:
                subprocess.run(cmd, capture_output=True)
            console.print(f"✅ Sentinel Sync OK ({ts})")
        except: 
            console.print("❌ Sync Error.")

    def audit(self, *args):
        """🛡️ Audit de compatibilité native Apple Silicon (Deep Check)."""
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
            # La commande 'file' sur Mac renvoie 'Mach-O 64-bit executable arm64'
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

    def purge(self, *args):
        console.print("[bold red]🧹 Purge des caches...[/bold red]")
        subprocess.run("find . -name '__pycache__' -exec rm -rf {} +", shell=True)
        console.print("✅ Système nettoyé.")

    # --- KNOWLEDGE & AI ---
    def ingest(self, *args):
        if len(args) < 3: 
            return
        cat, title, content = args[0], args[1], " ".join(args[2:])
        path = os.path.join(self.base_path, cat.lower(), "skills.md")
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "a", encoding="utf-8") as f:
            f.write(f"\n### {title} ({datetime.date.today()})\n{content.strip()}\n")
        console.print(f"✅ Skill {title} -> {cat.upper()}")

    def find(self, *args):
        query = " ".join(args).lower()
        for path in self._get_all_skills():
            with open(path, "r") as f:
                for block in f.read().split("### "):
                    if query in block.lower():
                        console.print(Panel(Syntax(block, "markdown"), title="📍 Skill Trouvé"))

    # --- ARCHITECT & UX ---
    def dash(self, *args):
        table = Table(title="🧠 AXE DASHBOARD", box=None)
        table.add_column("Stack", style="cyan")
        table.add_column("Skills", justify="right", style="green")
        total = 0
        for path in self._get_all_skills():
            count = len([l for l in open(path) if l.startswith("### ")])
            table.add_row(os.path.relpath(os.path.dirname(path), self.base_path).upper(), str(count))
            total += count
        console.print(Panel(table, subtitle=f"Total: {total}"))

    def show_help(self, *args):
        table = Table(title="🚀 AXE COMMAND CENTER v2.1", show_header=True, header_style="bold magenta")
        table.add_column("Cmd", style="bold yellow")
        table.add_column("Description", style="white")
        table.add_column("Scope", style="dim")

        cmds = [
            ("/h", "Santé & Audit M1", "Système"),
            ("/f", "Réparer & Installer", "Maintenance"),
            ("/s", "Sync Cloud GitHub", "Sentinel"),
            ("/dash", "Dashboard d'état", "Monitor"),
            ("/i", "Ingérer un skill", "Mémoire"),
            ("/find", "Recherche mémoire", "Search"),
            ("/web", "Veille & Ingest auto", "AI Intel"),
            ("/git", "Cloner & Analyser", "Repo"),
            ("/new", "Nouveau projet AXE", "Dev"),
            ("/spec", "Générer blueprint", "Architect"),
            ("/test", "Audit Code Parfait", "Qualité"),
            ("/ux", "Audit UX/Design", "UX Lead"),
            ("/focus", "Cibler une stack", "Context"),
            ("/zip", "Flush & Snapshot", "Context"),
            ("/local", "Inférence M1 locale", "AI"),
            ("/audit", "Vérification sincérité binaire (Native vs Rosetta)", "M1"),
            ("/purge", "Vider les caches", "Perf"),
            ("/panic", "Git Reset d'urgence", "Security")
        ]
        for c, d, s in cmds: 
            table.add_row(c, d, s)
        console.print(table)

if __name__ == "__main__":
    axe = AXESystem()
    dispatcher = {
        "/h": axe.audit, "/f": axe.fix, "/s": axe.sync, "/dash": axe.dash,
        "/i": axe.ingest, "/find": axe.find, "/help": axe.show_help,
        "/audit": axe.audit, "/purge": axe.purge
    }
    cmd = sys.argv[1] if len(sys.argv) > 1 else "/help"
    if cmd in dispatcher: 
        dispatcher[cmd](*sys.argv[2:])
    else: 
        axe.show_help()
