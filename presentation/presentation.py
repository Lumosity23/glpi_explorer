#!/usr/bin/env python3
"""
Présentation CLI Interactive - GLPI Explorer
"""

import os
import sys
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.prompt import Prompt
from rich.align import Align

class GLPIPresentationCLI:
    def __init__(self):
        self.console = Console()
        self.current_slide = 0
        self.slides = [
            self.slide_1_problematique,
            self.slide_2_commandes,
            self.slide_3_defis,
            self.slide_4_vision
        ]
        self.slide_titles = [
            "GLPI Explorer : De l'Inventaire Statique à l'Analyse Dynamique",
            "Un Langage Intuitif pour Explorer le Réseau",
            "Feuille de Route : Vers un Cache \"Vivant\" et Proactif",
            "Le Futur : Un Écosystème Complet de Gestion Réseau"
        ]
    
    def clear_screen(self):
        """Efface l'écran"""
        os.system('clear' if os.name == 'posix' else 'cls')
    
    def show_header(self):
        """Affiche l'en-tête de la présentation"""
        header = Panel(
            Align.center(
                Text("GLPI Explorer - Présentation Technique", style="bold white on blue")
            ),
            border_style="blue"
        )
        self.console.print(header)
        self.console.print()
    
    def show_navigation(self):
        """Affiche les options de navigation"""
        nav_text = f"Diapositive {self.current_slide + 1}/{len(self.slides)}"
        nav_panel = Panel(
            Text(nav_text, justify="center"),
            title="Navigation",
            border_style="green"
        )
        self.console.print(nav_panel)
        self.console.print()
    
    def slide_1_problematique(self):
        """Diapositive 1: La Problématique et Notre Approche"""
        title = Panel(
            Text(self.slide_titles[0], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Diagramme de flux
        panel1_content = Text("API REST", justify="center")
        panel1 = Panel(panel1_content, title="GLPI (Source de Vérité)", border_style="blue")
        
        arrow1 = Text("    ↓ Chargement Initial (1x) ↓    ", justify="center", style="bold green")
        
        panel2_content = Text("Graphe de Topologie en Mémoire", justify="center")
        panel2 = Panel(panel2_content, title="Cache Local Intelligent", border_style="blue")
        
        arrow2 = Text("    ↓ Requêtes Instantanées (en local) ↓    ", justify="center", style="bold green")
        
        panel3_content = Text("GLPI Explorer (CLI)", justify="center")
        panel3 = Panel(panel3_content, title="Interface CLI", border_style="blue")
        
        self.console.print(panel1)
        self.console.print(arrow1)
        self.console.print(panel2)
        self.console.print(arrow2)
        self.console.print(panel3)
        
        self.console.print()
        explanation = Panel(
            Text("Le défi : transformer notre inventaire GLPI en un outil d'analyse réseau rapide et intelligent.\nSolution : GLPI Explorer crée un 'double numérique' intelligent de notre réseau.", 
                 style="italic"),
            title="Explication",
            border_style="yellow"
        )
        self.console.print(explanation)
    
    def slide_2_commandes(self):
        """Diapositive 2: Les Commandes Principales"""
        title = Panel(
            Text(self.slide_titles[1], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Capture 1: list & get
        cmd1 = Panel(
            Text("ubuntu@glpi-explorer:~$ ls sw\nSW reseaux\nSW finance\n\nubuntu@glpi-explorer:~$ get sw \"SW reseaux\"", 
                 style="green"),
            title="Lister & Inspecter",
            border_style="blue"
        )
        self.console.print(cmd1)
        
        # Table pour la commande get
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Port", style="dim", width=10)
        table.add_column("Description")
        table.add_column("Status")
        
        table.add_row("1", "Uplink", "[green]Connecté[/green]")
        table.add_row("2", "Serveur Web", "[green]Connecté[/green]")
        table.add_row("3", "Imprimante Bureau", "[red]Déconnecté[/red]")
        
        self.console.print(table)
        self.console.print()
        
        # Capture 2: trace
        cmd2 = Panel(
            Text("ubuntu@glpi-explorer:~$ tr pc pc3\nTracing path from pc to pc3...\n[blue]PC1 (Salle 1)[/blue] -> [yellow]SW1 (Salle 1)[/yellow] -> [yellow]SW2 (Salle 2)[/yellow] -> [blue]PC3 (Salle 2)[/blue]", 
                 style="green"),
            title="Tracer un Chemin",
            border_style="blue"
        )
        self.console.print(cmd2)
        self.console.print()
        
        # Capture 3: map
        cmd3 = Panel(
            Text("ubuntu@glpi-explorer:~$ map sw \"SW reseaux\"\nSelect port:\n[blue]1: Uplink[/blue]\n[green]2: Serveur Web[/green]\n[red]3: Imprimante Bureau[/red]", 
                 style="green"),
            title="Explorer les Connexions",
            border_style="blue"
        )
        self.console.print(cmd3)
    
    def slide_3_defis(self):
        """Diapositive 3: Défis et Optimisations Futures"""
        title = Panel(
            Text(self.slide_titles[2], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Prompt avec notification delta
        prompt_panel = Panel(
            Text.assemble(
                Text("(glpi-explorer|", style="white"),
                Text("Δ3", style="bold red"),
                Text(") > ", style="white"),
                Text("_", style="white reverse")
            ),
            title="Cache \"Vivant\" - Notification de Changements",
            border_style="red"
        )
        self.console.print(prompt_panel)
        self.console.print()
        
        # Explications
        explanations = [
            "1. Refresh automatique en arrière-plan (threading).",
            "2. Comparaison (\"diff\") avec le cache existant.",
            "3. Notification non-intrusive des changements."
        ]
        
        for explanation in explanations:
            self.console.print(f"  {explanation}")
        
        self.console.print()
        
        challenge_panel = Panel(
            Text("Notre cache actuel est puissant, mais il est statique.\nLe plus grand défi est de le garder synchronisé avec GLPI sans impacter les performances.", 
                 style="italic"),
            title="Défi Principal",
            border_style="yellow"
        )
        self.console.print(challenge_panel)
    
    def slide_4_vision(self):
        """Diapositive 4: La Vision à Long Terme"""
        title = Panel(
            Text(self.slide_titles[3], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Table pour la commande checkup
        checkup_title = Panel(
            Text("Commande 'checkup' - Audit de Conformité", style="bold"),
            border_style="green"
        )
        self.console.print(checkup_title)
        
        table = Table(show_header=True, header_style="bold magenta")
        table.add_column("Priorité", style="dim", width=10)
        table.add_column("Anomalie")
        table.add_column("Équipement")
        table.add_column("Suggestion")
        
        table.add_row("[red]Haute[/red]", "Câble Orphelin", "C-1025", "Connecter l'extrémité B ou supprimer.")
        table.add_row("[yellow]Moyenne[/yellow]", "Erreur Nomenclature", "Switch-Finance", "Renommer en SW-FINANCE-01.")
        table.add_row("[yellow]Moyenne[/yellow]", "Paire IN/OUT Manquante", "PP-A01", "Le port 23 OUT existe mais pas le 23 IN.")
        
        self.console.print(table)
        self.console.print()
        
        # Vision future
        vision_panel = Panel(
            Text("Au-delà de l'exploration :\n• Commande 'checkup' pour auditer la conformité\n• Commandes 'create' et 'connect' pour construire le réseau\n• Interface web 'network-map' pour visualisation graphique", 
                 style="italic"),
            title="Écosystème Complet",
            border_style="magenta"
        )
        self.console.print(vision_panel)
    
    def show_menu(self):
        """Affiche le menu de navigation"""
        menu_options = [
            "[n] Diapositive suivante",
            "[p] Diapositive précédente",
            "[1-4] Aller à la diapositive",
            "[q] Quitter"
        ]
        
        menu_text = "\n".join(menu_options)
        menu_panel = Panel(
            Text(menu_text, justify="left"),
            title="Commandes",
            border_style="green"
        )
        self.console.print(menu_panel)
    
    def run(self):
        """Lance la présentation interactive"""
        while True:
            self.clear_screen()
            self.show_header()
            self.show_navigation()
            
            # Affiche la diapositive courante
            self.slides[self.current_slide]()
            
            self.console.print()
            self.show_menu()
            
            # Demande l'action à l'utilisateur
            choice = Prompt.ask("\nChoisissez une action", default="n")
            
            if choice.lower() == 'q':
                self.console.print("\n[bold green]Merci d'avoir assisté à la présentation ![/bold green]")
                break
            elif choice.lower() == 'n':
                if self.current_slide < len(self.slides) - 1:
                    self.current_slide += 1
            elif choice.lower() == 'p':
                if self.current_slide > 0:
                    self.current_slide -= 1
            elif choice.isdigit():
                slide_num = int(choice) - 1
                if 0 <= slide_num < len(self.slides):
                    self.current_slide = slide_num

if __name__ == "__main__":
    presentation = GLPIPresentationCLI()
    presentation.run()

