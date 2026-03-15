#!/usr/bin/env python3
"""
Cascade Monitor - Dashboard de Contrôle TUI
Surveillance de la mémoire et des services sans quitter le terminal
"""

import os
import sys
import time
import psutil
import subprocess
from datetime import datetime
from pathlib import Path
from typing import Dict, List, Any

try:
    from rich.console import Console
    from rich.layout import Layout
    from rich.panel import Panel
    from rich.table import Table
    from rich.progress import Progress, SpinnerColumn, TextColumn
    from rich.live import Live
    from rich.text import Text
    from rich.tree import Tree
    from rich.align import Align
    from rich.columns import Columns
    RICH_AVAILABLE = True
except ImportError:
    RICH_AVAILABLE = False
    print("⚠️ Rich library not found. Install with: pip install rich")
    sys.exit(1)


class CascadeMonitor:
    """Dashboard de surveillance pour Cascade AI System"""
    
    def __init__(self):
        self.console = Console()
        self.project_root = Path.cwd()
        self.windsurf_dir = self.project_root / "windsurf"
        self.memory_dir = self.windsurf_dir / "memory"
        self.logs_dir = self.project_root / "logs"
        
        # Configuration
        self.refresh_interval = 2.0  # seconds
        self.max_memory_lines = 50
        
    def get_system_info(self) -> Dict[str, Any]:
        """Obtenir les informations système"""
        try:
            cpu_percent = psutil.cpu_percent(interval=0.1)
            memory = psutil.virtual_memory()
            disk = psutil.disk_usage('/')
            
            # M1 specific info
            cpu_count = psutil.cpu_count()
            cpu_freq = psutil.cpu_freq()
            
            return {
                "cpu_percent": cpu_percent,
                "cpu_count": cpu_count,
                "cpu_freq": cpu_freq.current if cpu_freq else 0,
                "memory_percent": memory.percent,
                "memory_used": memory.used,
                "memory_total": memory.total,
                "disk_percent": disk.percent,
                "disk_used": disk.used,
                "disk_total": disk.total,
                "load_avg": os.getloadavg() if hasattr(os, 'getloadavg') else (0, 0, 0)
            }
        except Exception as e:
            return {"error": str(e)}
    
    def get_memory_stats(self) -> Dict[str, Any]:
        """Obtenir les statistiques de la mémoire Cascade"""
        try:
            if not self.memory_dir.exists():
                return {"error": "Memory directory not found"}
            
            stats = {
                "files": {},
                "total_files": 0,
                "total_size": 0,
                "last_modified": None,
                "skills_count": 0,
                "identity_loaded": False,
                "context_loaded": False
            }
            
            for file_path in self.memory_dir.glob("*.md"):
                if file_path.is_file():
                    stat = file_path.stat()
                    size = stat.st_size
                    mtime = stat.st_mtime
                    
                    file_name = file_path.name
                    stats["files"][file_name] = {
                        "size": size,
                        "lines": 0,
                        "last_modified": mtime,
                        "exists": True
                    }
                    
                    # Compter les lignes
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            stats["files"][file_name]["lines"] = len(f.readlines())
                    except:
                        pass
                    
                    stats["total_files"] += 1
                    stats["total_size"] += size
                    
                    if stats["last_modified"] is None or mtime > stats["last_modified"]:
                        stats["last_modified"] = mtime
                    
                    # Vérifier les fichiers spécifiques
                    if file_name == "skills.md":
                        # Compter les sections de skills
                        try:
                            with open(file_path, 'r', encoding='utf-8') as f:
                                content = f.read()
                                stats["skills_count"] = content.count("## ")
                        except:
                            pass
                    
                    elif file_name == "identity.md":
                        stats["identity_loaded"] = True
                    
                    elif file_name == "context_snapshot.md":
                        stats["context_loaded"] = True
            
            return stats
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_git_status(self) -> Dict[str, Any]:
        """Obtenir le statut Git"""
        try:
            # Vérifier si on est dans un repository Git
            if not (self.project_root / ".git").exists():
                return {"error": "Not a Git repository"}
            
            # Obtenir le statut
            result = subprocess.run(
                ["git", "status", "--porcelain"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            if result.returncode != 0:
                return {"error": "Git status failed"}
            
            status_lines = result.stdout.strip().split('\n') if result.stdout.strip() else []
            
            # Parser le statut
            modified = 0
            added = 0
            untracked = 0
            
            for line in status_lines:
                if line.startswith('M'):
                    modified += 1
                elif line.startswith('A'):
                    added += 1
                elif line.startswith('??'):
                    untracked += 1
            
            # Obtenir le dernier commit
            result = subprocess.run(
                ["git", "log", "-1", "--format=%h %s"],
                cwd=self.project_root,
                capture_output=True,
                text=True
            )
            
            last_commit = result.stdout.strip() if result.returncode == 0 else "No commits"
            
            return {
                "modified": modified,
                "added": added,
                "untracked": untracked,
                "last_commit": last_commit,
                "clean": modified == 0 and added == 0
            }
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_services_status(self) -> Dict[str, Any]:
        """Obtenir le statut des services"""
        try:
            services = {}
            
            # Vérifier les skills
            skills_dir = self.project_root / "skills"
            if skills_dir.exists():
                for skill_dir in skills_dir.iterdir():
                    if skill_dir.is_dir():
                        skill_name = skill_dir.name
                        script_file = skill_dir / f"{skill_name}.py"
                        
                        if script_file.exists():
                            # Vérifier si le script est exécutable
                            is_executable = os.access(script_file, os.X_OK)
                            
                            services[skill_name] = {
                                "type": "skill",
                                "path": str(script_file),
                                "executable": is_executable,
                                "status": "ready" if is_executable else "not_executable"
                            }
            
            # Vérifier les scripts principaux
            sentinel_script = self.windsurf_dir / "scripts" / "sentinel.py"
            if sentinel_script.exists():
                services["sentinel"] = {
                    "type": "script",
                    "path": str(sentinel_script),
                    "executable": os.access(sentinel_script, os.X_OK),
                    "status": "ready" if os.access(sentinel_script, os.X_OK) else "not_executable"
                }
            
            return services
            
        except Exception as e:
            return {"error": str(e)}
    
    def get_evolution_log(self) -> List[str]:
        """Obtenir le journal d'évolution"""
        try:
            log_file = self.logs_dir / "evolution.log"
            if not log_file.exists():
                return ["No evolution log found"]
            
            with open(log_file, 'r', encoding='utf-8') as f:
                lines = f.readlines()
            
            # Retourner les dernières entrées
            return [line.strip() for line in lines[-10:] if line.strip() and not line.startswith('#')]
            
        except Exception as e:
            return [f"Error reading log: {e}"]
    
    def create_system_panel(self) -> Panel:
        """Créer le panneau système"""
        system_info = self.get_system_info()
        
        if "error" in system_info:
            return Panel(f"Error: {system_info['error']}", title="System Info", border_style="red")
        
        # Créer une table
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        # CPU
        cpu_color = "green" if system_info["cpu_percent"] < 50 else "yellow" if system_info["cpu_percent"] < 80 else "red"
        table.add_row("CPU Usage", f"[{cpu_color}]{system_info['cpu_percent']:.1f}%[/{cpu_color}]")
        table.add_row("CPU Cores", str(system_info["cpu_count"]))
        table.add_row("CPU Frequency", f"{system_info['cpu_freq']:.0f} MHz")
        
        # Memory
        mem_color = "green" if system_info["memory_percent"] < 50 else "yellow" if system_info["memory_percent"] < 80 else "red"
        memory_used_gb = system_info["memory_used"] / (1024**3)
        memory_total_gb = system_info["memory_total"] / (1024**3)
        table.add_row("Memory Usage", f"[{mem_color}]{system_info['memory_percent']:.1f}%[/{mem_color}]")
        table.add_row("Memory Used", f"{memory_used_gb:.1f} GB / {memory_total_gb:.1f} GB")
        
        # Disk
        disk_color = "green" if system_info["disk_percent"] < 50 else "yellow" if system_info["disk_percent"] < 80 else "red"
        disk_used_gb = system_info["disk_used"] / (1024**3)
        disk_total_gb = system_info["disk_total"] / (1024**3)
        table.add_row("Disk Usage", f"[{disk_color}]{system_info['disk_percent']:.1f}%[/{disk_color}]")
        table.add_row("Disk Used", f"{disk_used_gb:.1f} GB / {disk_total_gb:.1f} GB")
        
        # Load Average
        load_avg = system_info["load_avg"]
        table.add_row("Load Average", f"{load_avg[0]:.2f}, {load_avg[1]:.2f}, {load_avg[2]:.2f}")
        
        return Panel(table, title="🖥️ System Info", border_style="blue")
    
    def create_memory_panel(self) -> Panel:
        """Créer le panneau mémoire"""
        memory_stats = self.get_memory_stats()
        
        if "error" in memory_stats:
            return Panel(f"Error: {memory_stats['error']}", title="Memory Stats", border_style="red")
        
        # Créer une table
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        table.add_row("Total Files", str(memory_stats["total_files"]))
        table.add_row("Total Size", f"{memory_stats['total_size'] / 1024:.1f} KB")
        table.add_row("Skills Count", str(memory_stats["skills_count"]))
        table.add_row("Identity Loaded", "✅" if memory_stats["identity_loaded"] else "❌")
        table.add_row("Context Loaded", "✅" if memory_stats["context_loaded"] else "❌")
        
        if memory_stats["last_modified"]:
            last_mod = datetime.fromtimestamp(memory_stats["last_modified"])
            table.add_row("Last Modified", last_mod.strftime("%Y-%m-%d %H:%M:%S"))
        
        # Détails des fichiers
        file_details = []
        for file_name, file_info in memory_stats["files"].items():
            status = "✅" if file_info["exists"] else "❌"
            file_details.append(f"{status} {file_name} ({file_info['lines']} lines)")
        
        if file_details:
            table.add_row("", "")
            table.add_row("Files:", "")
            for detail in file_details[:5]:  # Limiter à 5 fichiers
                table.add_row("", detail)
        
        return Panel(table, title="🧠 Memory Stats", border_style="green")
    
    def create_git_panel(self) -> Panel:
        """Créer le panneau Git"""
        git_status = self.get_git_status()
        
        if "error" in git_status:
            return Panel(f"Error: {git_status['error']}", title="Git Status", border_style="red")
        
        # Créer une table
        table = Table(show_header=False, box=None)
        table.add_column("Metric", style="cyan")
        table.add_column("Value", style="green")
        
        status_color = "green" if git_status["clean"] else "yellow"
        table.add_row("Status", f"[{status_color}]Clean[/{status_color}]" if git_status["clean"] else f"[{status_color}]Modified[/{status_color}]")
        table.add_row("Modified", str(git_status["modified"]))
        table.add_row("Added", str(git_status["added"]))
        table.add_row("Untracked", str(git_status["untracked"]))
        table.add_row("Last Commit", git_status["last_commit"])
        
        return Panel(table, title="📦 Git Status", border_style="yellow")
    
    def create_services_panel(self) -> Panel:
        """Créer le panneau services"""
        services = self.get_services_status()
        
        if "error" in services:
            return Panel(f"Error: {services['error']}", title="Services", border_style="red")
        
        # Créer une table
        table = Table(show_header=True, box=None)
        table.add_column("Service", style="cyan")
        table.add_column("Type", style="blue")
        table.add_column("Status", style="green")
        
        for service_name, service_info in services.items():
            status_color = "green" if service_info["status"] == "ready" else "red"
            status_icon = "✅" if service_info["status"] == "ready" else "❌"
            
            table.add_row(
                service_name,
                service_info["type"],
                f"[{status_color}]{status_icon} {service_info['status']}[/{status_color}]"
            )
        
        if not services:
            table.add_row("No services found", "", "")
        
        return Panel(table, title="⚙️ Services", border_style="magenta")
    
    def create_log_panel(self) -> Panel:
        """Créer le panneau de logs"""
        evolution_log = self.get_evolution_log()
        
        # Créer un tree pour les logs
        tree = Tree("📋 Evolution Log")
        
        for entry in evolution_log[-5:]:  # Limiter à 5 entrées
            if entry.strip():
                tree.add(entry.strip())
        
        return Panel(tree, title="📝 Recent Logs", border_style="cyan")
    
    def create_layout(self) -> Layout:
        """Créer le layout principal"""
        layout = Layout()
        
        # Layout principal
        layout.split_column(
            Layout(name="header", size=3),
            Layout(name="body"),
            Layout(name="footer", size=3)
        )
        
        # Header
        layout["header"].update(Panel(
            Align.center(Text("🧠 CASCADE AI SYSTEM MONITOR", style="bold blue")),
            border_style="blue"
        ))
        
        # Body - grille 2x2
        layout["body"].split_row(
            Layout(name="left"),
            Layout(name="right")
        )
        
        layout["left"].split_column(
            Layout(name="system", size=12),
            Layout(name="memory", size=12)
        )
        
        layout["right"].split_column(
            Layout(name="git", size=8),
            Layout(name="services", size=8),
            Layout(name="logs")
        )
        
        # Footer
        current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        layout["footer"].update(Panel(
            Align.center(Text(f"Last Update: {current_time} | Press Ctrl+C to exit", style="dim")),
            border_style="dim"
        ))
        
        return layout
    
    def update_layout(self, layout: Layout):
        """Mettre à jour le layout avec les données actuelles"""
        layout["system"].update(self.create_system_panel())
        layout["memory"].update(self.create_memory_panel())
        layout["git"].update(self.create_git_panel())
        layout["services"].update(self.create_services_panel())
        layout["logs"].update(self.create_log_panel())
    
    def run(self):
        """Lancer le monitor"""
        self.console.print("🧠 Cascade Monitor - Starting...")
        self.console.print("Press Ctrl+C to exit")
        self.console.print()
        
        layout = self.create_layout()
        
        try:
            with Live(layout, refresh_per_second=1/self.refresh_interval, screen=True) as live:
                while True:
                    self.update_layout(layout)
                    time.sleep(self.refresh_interval)
        except KeyboardInterrupt:
            self.console.print("\n👋 Cascade Monitor stopped")
        except Exception as e:
            self.console.print(f"\n❌ Error: {e}")


def main():
    """Point d'entrée principal"""
    if not RICH_AVAILABLE:
        print("❌ Rich library is required. Install with: pip install rich")
        sys.exit(1)
    
    monitor = CascadeMonitor()
    monitor.run()


if __name__ == "__main__":
    main()
