#!/usr/bin/env python3
"""
Enhanced main entry point with template selection
"""

import asyncio
import sys
from rich.console import Console
from rich.panel import Panel
from rich.markdown import Markdown
from rich.table import Table
from rich.prompt import Prompt, Confirm

from report_generator import (
    ImprovedReportGenerator, 
    generate_business_report,
    generate_academic_report, 
    generate_technical_report,
    generate_quick_report
)
from config import get_config, CONFIG_PRESETS

console = Console()

def show_template_options():
    """Display available report templates"""
    table = Table(title="📊 Available Report Templates")
    table.add_column("Template", style="cyan", no_wrap=True)
    table.add_column("Description", style="white")
    table.add_column("Best For", style="green")
    
    table.add_row(
        "standard", 
        "Balanced research report with intro, main sections, conclusion",
        "General research, overviews"
    )
    table.add_row(
        "business", 
        "Executive summary, market analysis, strategic recommendations", 
        "Business analysis, market research"
    )
    table.add_row(
        "academic", 
        "Abstract, literature review, analysis, conclusions",
        "Academic research, scholarly analysis"
    )
    table.add_row(
        "technical", 
        "Technical overview, specifications, implementation details",
        "Technology analysis, system documentation"
    )
    table.add_row(
        "quick", 
        "Shorter sections, faster generation, concise format",
        "Quick insights, rapid analysis"
    )
    
    console.print(table)

async def interactive_mode():
    """Enhanced interactive mode with template selection"""
    
    console.print(Panel.fit(
        "[bold blue]🤖 Enhanced Report Generator[/bold blue]\n"
        "Generate comprehensive research reports with multiple templates",
        title="AI Report Generator v2.0"
    ))
    
    while True:
        try:
            # Show template options
            show_template_options()
            
            # Get template choice
            template_choice = Prompt.ask(
                "\n[cyan]Choose a template[/cyan]",
                choices=["standard", "business", "academic", "technical", "quick"],
                default="standard"
            )
            
            # Get topic from user
            topic = console.input(f"\n[bold cyan]Enter your research topic: [/bold cyan]")
            
            if not topic.strip():
                console.print("[red]Please enter a valid topic.[/red]")
                continue
            
            # Generate report based on template choice
            console.print(f"\n[green]Generating {template_choice} report on: {topic}[/green]")
            
            with console.status(f"[bold green]Generating {template_choice} report..."):
                if template_choice == "business":
                    report = await generate_business_report(topic)
                elif template_choice == "academic":
                    report = await generate_academic_report(topic)
                elif template_choice == "technical":
                    report = await generate_technical_report(topic)
                elif template_choice == "quick":
                    report = await generate_quick_report(topic)
                else:
                    config = get_config("standard")
                    generator = ImprovedReportGenerator(config)
                    report = await generator.generate_report(topic)
            
            # Save report
            config = get_config(template_choice)
            generator = ImprovedReportGenerator(config)
            filename = generator.save_report(report)
            
            # Display success message
            console.print(f"\n[bold green]✅ Report generated successfully![/bold green]")
            console.print(f"[blue]📁 Saved to: {filename}[/blue]")
            console.print(f"[yellow]📋 Template: {template_choice.title()}[/yellow]")
            
            # Ask if user wants to see the report
            show_report = Confirm.ask("\n[cyan]Display report now?[/cyan]", default=True)
            
            if show_report:
                console.print("\n" + "="*80)
                markdown_report = Markdown(report)
                console.print(markdown_report)
                console.print("="*80)
            
            # Ask if user wants to generate another report
            continue_generating = Confirm.ask("\n[cyan]Generate another report?[/cyan]", default=True)
            
            if not continue_generating:
                console.print("[yellow]Thanks for using the Report Generator! 👋[/yellow]")
                break
            
        except KeyboardInterrupt:
            console.print("\n\n[yellow]Operation cancelled.[/yellow]")
            break
        except Exception as e:
            console.print(f"\n[bold red]❌ Error: {e}[/bold red]")
            
            # Ask if user wants to try again
            retry = Confirm.ask("[cyan]Try again?[/cyan]", default=True)
            if not retry:
                break



async def single_report_mode(topic: str, template: str = "standard"):
    """Generate a single report for the given topic"""
    
    console.print(f"[green]Generating {template} report on: {topic}[/green]")
    
    try:
        with console.status(f"[bold green]Generating {template} report..."):
            if template == "business":
                report = await generate_business_report(topic)
            elif template == "academic":
                report = await generate_academic_report(topic)
            elif template == "technical":
                report = await generate_technical_report(topic)
            elif template == "quick":
                report = await generate_quick_report(topic)
            else:
                config = get_config(template)
                generator = ImprovedReportGenerator(config)
                report = await generator.generate_report(topic)
        
        # Save report
        config = get_config(template)
        generator = ImprovedReportGenerator(config)
        filename = generator.save_report(report)
        
        console.print(f"\n[bold green]✅ Report generated successfully![/bold green]")
        console.print(f"[blue]📁 Saved to: {filename}[/blue]")
        console.print(f"[yellow]📋 Template: {template.title()}[/yellow]")
        
        # Display the report
        console.print("\n" + "="*80)
        markdown_report = Markdown(report)
        console.print(markdown_report)
        console.print("="*80)
        
    except Exception as e:
        console.print(f"[bold red]❌ Error: {e}[/bold red]")
        sys.exit(1)

def print_usage():
    """Print usage instructions"""
    console.print(Panel.fit(
        """[bold cyan]Usage Examples:[/bold cyan]

[yellow]Interactive mode:[/yellow]
python main.py

[yellow]Single report:[/yellow]
python main.py "Your Topic Here"
python main.py "AI in Healthcare" --template business

[yellow]Available templates:[/yellow]
standard, business, academic, technical, quick

[yellow]Rate Limiting:[/yellow]
Built-in rate limiting prevents API limit issues automatically.""",
        title="📖 Help"
    ))

def main():
    """Enhanced main function with argument parsing"""
    
    # Simple argument parsing
    args = sys.argv[1:]
    
    if "--help" in args or "-h" in args:
        print_usage()
        return
    
    # Extract template if specified
    template = "standard"
    if "--template" in args:
        template_idx = args.index("--template")
        if template_idx + 1 < len(args):
            template = args[template_idx + 1]
            args.pop(template_idx)  # Remove --template
            args.pop(template_idx)  # Remove template value
    
    # Generate report based on arguments
    if args:
        # Single report mode
        topic = " ".join(args)
        asyncio.run(single_report_mode(topic, template))
    else:
        # Interactive mode
        asyncio.run(interactive_mode())

if __name__ == "__main__":
    main()