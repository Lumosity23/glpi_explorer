#!/usr/bin/env python3
"""
Présentation CLI Interactive - GLPI Explorer
"""

import os
import sys
import time
from rich.console import Console
from rich.panel import Panel
from rich.text import Text
from rich.table import Table
from rich.layout import Layout
from rich.prompt import Prompt
from rich.align import Align
from rich.columns import Columns
from rich.tree import Tree

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
            "Le Défi Actuel : Le Passage à l'Échelle",
            "Le Futur : Un Écosystème Complet de Gestion Réseau"
        ]

    def clear_screen(self):
        os.system('clear' if os.name == 'posix' else 'cls')

    def show_header(self):
        header = Panel(
            Align.center(Text("GLPI Explorer - Présentation Technique", style="bold white on blue")),
            border_style="blue"
        )
        self.console.print(header)
        self.console.print()

    def show_navigation(self):
        nav_text = f"Diapositive {self.current_slide + 1}/{len(self.slides)} - {self.slide_titles[self.current_slide]}"
        nav_panel = Panel(
            Text(nav_text, justify="center"),
            title="Navigation",
            border_style="green"
        )
        self.console.print(nav_panel)
        self.console.print()

    def slide_1_problematique(self):
        """Diapositive 1: La Problématique et Notre Approche"""

        # Diagramme de flux
        panel1 = Panel(Text("API REST\n(Source de Vérité)", justify="center"), title="[blue]GLPI[/blue]", width=30)
        arrow1 = Align.center(Text("⬇\nChargement Initial (1x)\n⬇", style="bold green"))
        panel2 = Panel(Text("Graphe de Topologie en Mémoire\n(Le 'Double Numérique')", justify="center"), title="[magenta]Cache Intelligent (ICache)[/magenta]", width=30)
        arrow2 = Align.center(Text("⬇\nRequêtes Instantanées (0 API)\n⬇", style="bold green"))
        panel3 = Panel(Text("Commandes Intuitives\n(trace, ls, get, ...)", justify="center"), title="[cyan]GLPI Explorer (CLI)[/cyan]", width=30)

        diagram = Columns([panel1, panel2, panel3], expand=True, equal=True)
        self.console.print(Align.center(diagram))
        
        self.console.print()
        explanation = Panel(
            Text("Le défi : Transformer notre inventaire GLPI, lent et manuel, en un outil d'analyse réseau rapide et intelligent.\n[bold]Solution :[/bold] GLPI Explorer crée un 'double numérique' intelligent de notre réseau, permettant des réponses en [green]secondes[/green], pas en minutes.",
                 style="italic"),
            title="Explication",
            border_style="yellow"
        )
        self.console.print(explanation)

    def slide_2_commandes(self):
        """Diapositive 2: Les Commandes Principales"""

        command_tree = Tree("🔧 [bold]Commandes Disponibles[/bold]", style="cyan")

        inspection = command_tree.add("🔍 [bold green]Inspection & Listing[/bold green]")
        inspection.add("[cyan]ls / list[/cyan] : Lister les équipements (ex: `ls sw`)")
        inspection.add("[cyan]get / show[/cyan] : Afficher les détails d'un objet (ex: `get pc PC-FINANCE-01`)")

        topo = command_tree.add("🗺️ [bold magenta]Analyse de Topologie[/bold magenta]")
        topo.add("[cyan]trace / tr[/cyan] : Suivre un chemin réseau complet de bout en bout.")
        topo.add("[cyan]map / m[/cyan] : Explorer interactivement les connexions depuis un switch.")

        gestion = command_tree.add("⚙️ [bold yellow]Gestion & Débogage[/bold yellow]")
        gestion.add("[cyan]refresh / r[/cyan] : Mettre à jour le cache depuis GLPI.")
        gestion.add("[cyan]changes[/cyan] : Voir les modifications détectées.")
        gestion.add("[cyan]clear / cls[/cyan] : Nettoyer le terminal.")

        self.console.print(command_tree)
        self.console.print()
        
        demo_panel = Panel(
            Text.assemble(
                Text("(glpi-explorer)> ", style="bold cyan"),
                Text("trace pc PC-FINANCE-01", style="white")
            ) + 
            Text("\n\n[dim]┏━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━┳━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┓\n"
                 "┃ Étape ┃ Équipement       ┃ Port             ┃ Via                            ┃\n"
                 "┡━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━╇━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━┩\n"
                 "│ 1     │ PC-FINANCE-01    │ eth0             │ C-PC-FIN-01 -> WO-B204         │\n"
                 "│ 2     │ WO-B204          │ Port 3 IN -> OUT │ (Interne)                      │\n"
                 "│ 3     │ WO-B204          │ Port 3 OUT       │ C-WO-B204-P3 -> PP-A01         │\n"
                 "│ 4     │ PP-A01           │ Port 12 IN -> OUT│ (Interne)                      │\n"
                 "│ 5     │ PP-A01           │ Port 12 OUT      │ C-PP-A01-P12 -> SW-FINANCE-01  │\n"
                 "│ 6     │ SW-FINANCE-01    │ Gi1/0/12         │ FIN DE LIGNE                   │\n"
                 "└───────┴──────────────────┴──────────────────┴────────────────────────────────┘[/dim]"),
            title="Exemple d'Exécution : `trace`",
            border_style="blue"
        )
        self.console.print(demo_panel)

    def slide_3_defis(self):
        """Diapositive 3: Défis et Optimisations Futures"""
        
        challenge_table = Table(show_header=True, header_style="bold red", title="Le Défi du Passage à l'Échelle")
        challenge_table.add_column("Composant", style="cyan", width=20)
        challenge_table.add_column("Problème Identifié", style="white")
        challenge_table.add_column("Solution Envisagée", style="green")

        challenge_table.add_row(
            "Chargement Initial",
            "Sur +10 000 objets (VKI), le chargement complet du cache est trop lent (> 5 minutes) et gourmand en mémoire.",
            "Chargement 'Paresseux' (Lazy Loading) et optimisation des requêtes API."
        )
        challenge_table.add_row(
            "Réactivité",
            "La recherche dans un cache aussi volumineux pourrait ralentir les commandes.",
            "Utilisation de structures de données optimisées (index, dictionnaires) pour des recherches en temps constant O(1)."
        )
        challenge_table.add_row(
            "Persistance",
            "Le format de sauvegarde actuel (`pickle`) n'est pas optimal pour de très gros volumes.",
            "Étudier un format de cache binaire plus performant ou une mini base de données locale (SQLite)."
        )

        self.console.print(challenge_table)
        self.console.print()
        
        goal_panel = Panel(
             Text("[bold]Objectif :[/bold] Temps de démarrage < 30s et commandes < 1s, même sur l'infrastructure complète du VKI.", justify="center"),
             title="Critère de Succès",
             border_style="yellow"
        )
        self.console.print(goal_panel)

    def slide_4_vision(self):
        """Diapositive 4: La Vision à Long Terme"""

        roadmap_tree = Tree("🚀 [bold]Feuille de Route Future[/bold]", style="magenta")

        phase1 = roadmap_tree.add("Phase 1 : [green]L'Audit[/green]")
        phase1.add("✨ [cyan]Commande 'checkup'[/cyan] : Détecter les câbles orphelins, les erreurs de nomenclature, les incohérences...")

        phase2 = roadmap_tree.add("Phase 2 : [yellow]La Construction[/yellow]")
        phase2.add("✨ [cyan]Commandes 'create' & 'connect'[/cyan] : Provisionner et câbler des équipements depuis le CLI, en garantissant la conformité.")

        phase3 = roadmap_tree.add("Phase 3 : [blue]La Visualisation[/blue]")
        phase3.add("✨ [cyan]Interface 'network-map'[/cyan] : Une application web pour visualiser et explorer le réseau de manière graphique.")
        
        self.console.print(roadmap_tree)
        self.console.print()
        
        vision_panel = Panel(
            Text("Transformer GLPI Explorer d'un outil de [bold]consultation[/bold] à un écosystème complet pour [bold green]auditer[/bold green], [bold yellow]construire[/bold yellow], et [bold blue]visualiser[/bold blue] notre infrastructure réseau.",
                 justify="center"),
            title="Vision Finale",
            border_style="magenta"
        )
        self.console.print(vision_panel)

    def show_menu(self):
        menu_options = [
            "[bold green][n][/bold green]ext",
            "[bold green][p][/bold green]revious",
            "[bold cyan][1-4][/bold cyan] Go to slide",
            "[bold red][q][/bold red]uit"
        ]
        menu_text = " | ".join(menu_options)
        menu_panel = Panel(Text(menu_text, justify="center"), border_style="dim")
        self.console.print(menu_panel)

    def run(self):
        while True:
            self.clear_screen()
            self.show_header()
            self.show_navigation()
            self.slides[self.current_slide]()
            self.console.print()
            self.show_menu()
            
            choice = Prompt.ask("\nAction", default="n")
            
            if choice.lower() == 'q':
                self.console.print("\n[bold green]Merci ![/bold green]")
                break
            elif choice.lower() == 'n':
                self.current_slide = (self.current_slide + 1) % len(self.slides)
            elif choice.lower() == 'p':
                self.current_slide = (self.current_slide - 1 + len(self.slides)) % len(self.slides)
            elif choice.isdigit():
                slide_num = int(choice) - 1
                if 0 <= slide_num < len(self.slides):
                    self.current_slide = slide_num
                else:
                    self.console.print(f"[red]Slide invalide. Entrez un nombre entre 1 et {len(self.slides)}.[/red]")
                    time.sleep(1)

if __name__ == "__main__":
    presentation = GLPIPresentationCLI()
    presentation.run()