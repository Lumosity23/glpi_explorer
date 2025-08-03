#!/usr/bin/env python3
"""
Présentation CLI Interactive - GLPI Explorer
Version améliorée avec visualisations Rich intégrées
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
from rich.columns import Columns
from rich.progress import Progress, SpinnerColumn, TextColumn
from rich.tree import Tree
from rich.syntax import Syntax
import time

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
        """Affiche l'en-tête de la présentation avec animation"""
        ascii_logo = """
 ██████╗ ██╗     ██████╗ ██╗    ███████╗██╗  ██╗██████╗ ██╗      ██████╗ ██████╗ ███████╗██████╗ 
██╔════╝ ██║     ██╔══██╗██║    ██╔════╝╚██╗██╔╝██╔══██╗██║     ██╔═══██╗██╔══██╗██╔════╝██╔══██╗
██║  ███╗██║     ██████╔╝██║    █████╗   ╚███╔╝ ██████╔╝██║     ██║   ██║██████╔╝█████╗  ██████╔╝
██║   ██║██║     ██╔═══╝ ██║    ██╔══╝   ██╔██╗ ██╔═══╝ ██║     ██║   ██║██╔══██╗██╔══╝  ██╔══██╗
╚██████╔╝███████╗██║     ██║    ███████╗██╔╝ ██╗██║     ███████╗╚██████╔╝██║  ██║███████╗██║  ██║
 ╚═════╝ ╚══════╝╚═╝     ╚═╝    ╚══════╝╚═╝  ╚═╝╚═╝     ╚══════╝ ╚═════╝ ╚═╝  ╚═╝╚══════╝╚═╝  ╚═╝
        """
        
        header = Panel(
            Align.center(
                Text(ascii_logo, style="bold cyan") + Text("\nPrésentation Technique", style="bold white")
            ),
            border_style="blue"
        )
        self.console.print(header)
        self.console.print()
    
    def show_navigation(self):
        """Affiche les options de navigation avec indicateur de progression"""
        progress_bar = "█" * (self.current_slide + 1) + "░" * (len(self.slides) - self.current_slide - 1)
        nav_text = f"Diapositive {self.current_slide + 1}/{len(self.slides)}\n[{progress_bar}]"
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
        
        # Diagramme de flux amélioré avec colonnes
        panels = []
        
        # Panel 1
        panel1_content = Text.assemble(
            Text("🗄️ ", style="bold blue"),
            Text("API REST\n", style="bold"),
            Text("Source de vérité\nInventaire complet", style="dim")
        )
        panel1 = Panel(panel1_content, title="GLPI", border_style="blue", width=25)
        panels.append(panel1)
        
        # Panel 2  
        panel2_content = Text.assemble(
            Text("🧠 ", style="bold green"),
            Text("Cache Intelligent\n", style="bold"),
            Text("Graphe en mémoire\nRequêtes instantanées", style="dim")
        )
        panel2 = Panel(panel2_content, title="Cache Local", border_style="green", width=25)
        panels.append(panel2)
        
        # Panel 3
        panel3_content = Text.assemble(
            Text("⚡ ", style="bold yellow"),
            Text("Interface CLI\n", style="bold"),
            Text("Exploration rapide\nCommandes intuitives", style="dim")
        )
        panel3 = Panel(panel3_content, title="GLPI Explorer", border_style="yellow", width=25)
        panels.append(panel3)
        
        self.console.print(Columns(panels, equal=True, expand=True))
        
        # Flèches de processus
        arrows = Text("    📥 Chargement (1x)     ➡️     ⚡ Requêtes instantanées     ", 
                     justify="center", style="bold magenta")
        self.console.print(arrows)
        self.console.print()
        
        # Explication avec statistiques
        stats_table = Table(show_header=True, header_style="bold magenta")
        stats_table.add_column("Méthode", style="dim")
        stats_table.add_column("Temps de réponse")
        stats_table.add_column("Requêtes API")
        
        stats_table.add_row("Méthode traditionnelle", "[red]5-30 secondes[/red]", "[red]50-100[/red]")
        stats_table.add_row("GLPI Explorer", "[green]< 1 seconde[/green]", "[green]0 (cache)[/green]")
        
        self.console.print(stats_table)
    
    def slide_2_commandes(self):
        """Diapositive 2: Les Commandes Principales"""
        title = Panel(
            Text(self.slide_titles[1], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Arbre des commandes
        command_tree = Tree("🔧 Commandes GLPI Explorer", style="bold blue")
        
        # Branche Listing
        listing_branch = command_tree.add("📋 Listing & Inspection", style="green")
        listing_branch.add("[cyan]ls[/cyan] [type] - Lister les équipements")
        listing_branch.add("[cyan]get[/cyan] [type] [name] - Détails d'un équipement")
        
        # Branche Navigation
        nav_branch = command_tree.add("🗺️ Navigation & Trace", style="yellow")
        nav_branch.add("[cyan]tr[/cyan] [from] [to] - Tracer un chemin")
        nav_branch.add("[cyan]map[/cyan] [type] [name] - Explorer les connexions")
        
        # Branche Analyse
        analysis_branch = command_tree.add("🔍 Analyse & Audit", style="magenta")
        analysis_branch.add("[cyan]checkup[/cyan] - Audit de conformité")
        analysis_branch.add("[cyan]diff[/cyan] - Changements détectés")
        
        self.console.print(command_tree)
        self.console.print()
        
        # Exemple d'exécution avec simulation
        demo_panel = Panel(
            Text("Démonstration en direct", style="bold"),
            border_style="green"
        )
        self.console.print(demo_panel)
        
        # Simulation de commande
        self.console.print("[green]ubuntu@glpi-explorer:~$[/green] [cyan]ls sw[/cyan]")
        time.sleep(0.5)
        
        # Table des résultats
        result_table = Table(show_header=True, header_style="bold cyan")
        result_table.add_column("Nom", style="bold")
        result_table.add_column("Localisation")
        result_table.add_column("Ports")
        result_table.add_column("Status")
        
        result_table.add_row("SW-FINANCE-01", "Bureau Finance", "24", "[green]●[/green] Actif")
        result_table.add_row("SW-RH-02", "Bureau RH", "48", "[green]●[/green] Actif")
        result_table.add_row("SW-DEV-03", "Salle Serveurs", "24", "[yellow]●[/yellow] Maintenance")
        
        self.console.print(result_table)
    
    def slide_3_defis(self):
        """Diapositive 3: Défis et Optimisations Futures"""
        title = Panel(
            Text(self.slide_titles[2], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Simulation du prompt avec notifications
        prompt_demo = Panel(
            Text.assemble(
                Text("(glpi-explorer|", style="white"),
                Text("Δ3", style="bold red blink"),
                Text(") > ", style="white"),
                Text("_", style="white reverse")
            ),
            title="🔄 Cache \"Vivant\" - Notifications en Temps Réel",
            border_style="red"
        )
        self.console.print(prompt_demo)
        self.console.print()
        
        # Architecture du cache vivant
        architecture_table = Table(show_header=True, header_style="bold magenta")
        architecture_table.add_column("Composant", style="bold")
        architecture_table.add_column("Fonction")
        architecture_table.add_column("Technologie")
        
        architecture_table.add_row("🔄 Refresh Thread", "Mise à jour automatique", "Threading Python")
        architecture_table.add_row("🔍 Diff Engine", "Détection des changements", "Algorithme de comparaison")
        architecture_table.add_row("📢 Notification", "Alerte non-intrusive", "Rich Live Display")
        architecture_table.add_row("💾 Cache Store", "Stockage optimisé", "Structures de données Python")
        
        self.console.print(architecture_table)
        self.console.print()
        
        # Exemple de notification
        notification_example = Panel(
            Text.assemble(
                Text("🆕 ", style="green"),
                Text("Nouvel équipement détecté: ", style="white"),
                Text("SW-MARKETING-04", style="bold cyan"),
                Text("\n🔧 ", style="yellow"),
                Text("Port modifié: ", style="white"),
                Text("SW-FINANCE-01:23 ", style="bold cyan"),
                Text("→ Connecté", style="green"),
                Text("\n❌ ", style="red"),
                Text("Équipement supprimé: ", style="white"),
                Text("OLD-PRINTER-05", style="bold red")
            ),
            title="Exemple de Notifications",
            border_style="yellow"
        )
        self.console.print(notification_example)
    
    def slide_4_vision(self):
        """Diapositive 4: La Vision à Long Terme"""
        title = Panel(
            Text(self.slide_titles[3], style="bold cyan", justify="center"),
            border_style="cyan"
        )
        self.console.print(title)
        self.console.print()
        
        # Roadmap avec timeline
        roadmap_tree = Tree("🚀 Feuille de Route GLPI Explorer", style="bold magenta")
        
        # Phase 1
        phase1 = roadmap_tree.add("📋 Phase 1: Audit & Conformité", style="green")
        phase1.add("✅ Commande [cyan]checkup[/cyan] - Détection d'anomalies")
        phase1.add("✅ Rapport de conformité automatisé")
        phase1.add("✅ Suggestions de correction")
        
        # Phase 2
        phase2 = roadmap_tree.add("🔧 Phase 2: Construction Réseau", style="yellow")
        phase2.add("🔄 Commande [cyan]create[/cyan] - Création d'équipements")
        phase2.add("🔄 Commande [cyan]connect[/cyan] - Gestion des connexions")
        phase2.add("🔄 Validation de nomenclature")
        
        # Phase 3
        phase3 = roadmap_tree.add("🌐 Phase 3: Interface Web", style="blue")
        phase3.add("📋 [cyan]network-map[/cyan] - Visualisation graphique")
        phase3.add("📋 Édition interactive de topologie")
        phase3.add("📋 Synchronisation bidirectionnelle")
        
        self.console.print(roadmap_tree)
        self.console.print()
        
        # Exemple de commande checkup
        checkup_demo = Panel(
            Text("Démonstration: Commande checkup", style="bold"),
            border_style="green"
        )
        self.console.print(checkup_demo)
        
        # Table des anomalies
        anomalies_table = Table(show_header=True, header_style="bold red")
        anomalies_table.add_column("🚨 Priorité", style="bold")
        anomalies_table.add_column("Type d'Anomalie")
        anomalies_table.add_column("Équipement")
        anomalies_table.add_column("Action Recommandée")
        
        anomalies_table.add_row(
            "[red]CRITIQUE[/red]", 
            "Câble orphelin", 
            "C-1025", 
            "Connecter l'extrémité B ou supprimer"
        )
        anomalies_table.add_row(
            "[yellow]MOYENNE[/yellow]", 
            "Nomenclature incorrecte", 
            "Switch-Finance", 
            "Renommer en SW-FINANCE-01"
        )
        anomalies_table.add_row(
            "[yellow]MOYENNE[/yellow]", 
            "Paire IN/OUT manquante", 
            "PP-A01:23", 
            "Créer le port 23 IN correspondant"
        )
        
        self.console.print(anomalies_table)
        
        # Vision finale
        vision_panel = Panel(
            Text.assemble(
                Text("🎯 ", style="bold yellow"),
                Text("Objectif Final: ", style="bold"),
                Text("Un écosystème complet de gestion réseau\n", style="white"),
                Text("De l'inventaire à la construction, en passant par l'audit et la visualisation", style="italic")
            ),
            title="Vision 2024-2025",
            border_style="magenta"
        )
        self.console.print(vision_panel)
    
    def show_menu(self):
        """Affiche le menu de navigation avec icônes"""
        menu_options = [
            "⏭️  [n] Diapositive suivante",
            "⏮️  [p] Diapositive précédente", 
            "🔢 [1-4] Aller à la diapositive",
            "❌ [q] Quitter la présentation"
        ]
        
        menu_text = "\n".join(menu_options)
        menu_panel = Panel(
            Text(menu_text, justify="left"),
            title="🎮 Commandes de Navigation",
            border_style="green"
        )
        self.console.print(menu_panel)
    
    def show_slide_summary(self):
        """Affiche un résumé de toutes les diapositives"""
        summary_table = Table(show_header=True, header_style="bold cyan")
        summary_table.add_column("Diapo", style="bold", width=6)
        summary_table.add_column("Titre")
        summary_table.add_column("Points Clés")
        
        summaries = [
            "Problème → Solution → Architecture",
            "Commandes intuitives et démonstration",
            "Cache vivant et notifications temps réel",
            "Roadmap et vision écosystème complet"
        ]
        
        for i, (title, summary) in enumerate(zip(self.slide_titles, summaries)):
            marker = "👉" if i == self.current_slide else "  "
            summary_table.add_row(f"{marker} {i+1}", title[:40] + "..." if len(title) > 40 else title, summary)
        
        summary_panel = Panel(
            summary_table,
            title="📋 Résumé de la Présentation",
            border_style="blue"
        )
        self.console.print(summary_panel)
    
    def run(self):
        """Lance la présentation interactive"""
        # Message de bienvenue
        welcome = Panel(
            Text.assemble(
                Text("🎉 Bienvenue dans la présentation GLPI Explorer !\n\n", style="bold green"),
                Text("Navigation: ", style="bold"),
                Text("Utilisez [n] et [p] pour naviguer, [q] pour quitter\n", style="white"),
                Text("Appuyez sur [Entrée] pour commencer...", style="italic")
            ),
            title="Présentation Interactive",
            border_style="green"
        )
        
        self.console.print(welcome)
        input()
        
        while True:
            self.clear_screen()
            self.show_header()
            self.show_navigation()
            
            # Affiche la diapositive courante
            self.slides[self.current_slide]()
            
            self.console.print()
            self.show_menu()
            
            # Demande l'action à l'utilisateur
            choice = Prompt.ask("\n🎯 Choisissez une action", default="n")
            
            if choice.lower() == 'q':
                # Message de fin
                end_panel = Panel(
                    Text.assemble(
                        Text("🎊 Merci d'avoir assisté à la présentation !\n\n", style="bold green"),
                        Text("GLPI Explorer: ", style="bold cyan"),
                        Text("De l'inventaire statique à l'analyse dynamique\n", style="white"),
                        Text("Questions ? Contact: equipe-dev@entreprise.com", style="italic")
                    ),
                    title="Fin de Présentation",
                    border_style="green"
                )
                self.console.print(end_panel)
                break
            elif choice.lower() == 'n':
                if self.current_slide < len(self.slides) - 1:
                    self.current_slide += 1
                else:
                    self.console.print("[yellow]⚠️  Vous êtes à la dernière diapositive ![/yellow]")
                    time.sleep(1)
            elif choice.lower() == 'p':
                if self.current_slide > 0:
                    self.current_slide -= 1
                else:
                    self.console.print("[yellow]⚠️  Vous êtes à la première diapositive ![/yellow]")
                    time.sleep(1)
            elif choice.lower() == 's':
                self.clear_screen()
                self.show_slide_summary()
                input("\nAppuyez sur [Entrée] pour continuer...")
            elif choice.isdigit():
                slide_num = int(choice) - 1
                if 0 <= slide_num < len(self.slides):
                    self.current_slide = slide_num
                else:
                    self.console.print(f"[red]❌ Diapositive {choice} n'existe pas ! (1-{len(self.slides)})[/red]")
                    time.sleep(1)

if __name__ == "__main__":
    presentation = GLPIPresentationCLI()
    presentation.run()


