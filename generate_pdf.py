#!/usr/bin/env python3
"""
PDF Generation Tool for Advisor Documents
Converts Markdown to beautiful PDFs using Pandoc and LaTeX
"""

import argparse
import subprocess
import sys
from pathlib import Path

# Get the directory where this script lives
SCRIPT_DIR = Path(__file__).parent.absolute()
TEMPLATES_DIR = SCRIPT_DIR / "templates"
FILTERS_DIR = SCRIPT_DIR / "filters"

TEMPLATES = {
    "professional": TEMPLATES_DIR / "professional.tex",
    "minimal": TEMPLATES_DIR / "minimal.tex",
    "report": TEMPLATES_DIR / "report.tex",
    "tufte1": TEMPLATES_DIR / "tufte1.tex",
    "tufte2": TEMPLATES_DIR / "tufte2.tex",
    "tufte3": TEMPLATES_DIR / "tufte3.tex",
    "tufte": TEMPLATES_DIR / "tufte.tex",
}

def list_templates():
    """List available templates."""
    print("\nAvailable templates:")
    for name, path in TEMPLATES.items():
        status = "✓" if path.exists() else "✗"
        print(f"  {status} {name}")
    print()

def generate_pdf(input_file, output_file=None, template="professional"):
    """Generate PDF from Markdown using Pandoc and LaTeX."""
    
    input_path = Path(input_file)
    if not input_path.exists():
        print(f"Error: Input file '{input_file}' not found")
        sys.exit(1)
    
    if template not in TEMPLATES:
        print(f"Error: Template '{template}' not found")
        print("Use --list-templates to see available templates")
        sys.exit(1)
    
    template_path = TEMPLATES[template]
    if not template_path.exists():
        print(f"Error: Template file '{template_path}' not found")
        sys.exit(1)
    
    # Determine output filename
    if output_file is None:
        output_file = input_path.with_suffix('.pdf')
    output_path = Path(output_file)
    
    # Default logo path
    logo_path = SCRIPT_DIR / "assets" / "esri-logo.png"
    
    print(f"Generating PDF...")
    print(f"  Input:    {input_path}")
    print(f"  Template: {template}")
    print(f"  Output:   {output_path}")
    if logo_path.exists():
        print(f"  Logo:     Using Esri logo")
    
    # Build Pandoc command
    cmd = [
        "pandoc",
        str(input_path),
        "-o", str(output_path),
        "--pdf-engine=pdflatex",
        "--template", str(template_path),
        "--variable", "geometry:margin=1in",
        "-f", "markdown-task_lists",  # Disable task list extension
    ]
    
    # Add wikilink filter
    wikilink_filter = FILTERS_DIR / "remove-wikilinks.lua"
    if wikilink_filter.exists():
        cmd.extend(["--lua-filter", str(wikilink_filter)])
    
    # Add checkbox filter
    checkbox_filter = FILTERS_DIR / "remove-checkboxes.lua"
    if checkbox_filter.exists():
        cmd.extend(["--lua-filter", str(checkbox_filter)])
    
    # Add actions-to-margin filter for tufte templates
    if "tufte" in template:
        actions_filter = FILTERS_DIR / "actions-to-margin.lua"
        if actions_filter.exists():
            cmd.extend(["--lua-filter", str(actions_filter)])
    
    # Add logo if it exists (not for tufte templates)
    if logo_path.exists() and "tufte" not in template:
        # Convert Windows path to forward slashes for LaTeX
        logo_path_str = str(logo_path).replace('\\', '/')
        cmd.extend(["--variable", f"logo={logo_path_str}"])
    
    try:
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            check=True
        )
        print(f"\n✓ Successfully generated: {output_path}")
        return True
        
    except subprocess.CalledProcessError as e:
        print(f"\n✗ Error generating PDF:")
        print(e.stderr)
        return False
    except FileNotFoundError:
        print("\n✗ Error: Pandoc not found in PATH")
        print("Please ensure Pandoc is installed and accessible")
        return False

def main():
    parser = argparse.ArgumentParser(
        description="Generate beautiful PDFs from Markdown files",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s document.md
  %(prog)s document.md --template minimal
  %(prog)s document.md -o output.pdf --template formal
        """
    )
    
    parser.add_argument(
        "input",
        nargs="?",
        help="Input Markdown file"
    )
    
    parser.add_argument(
        "-o", "--output",
        help="Output PDF file (default: same name as input)"
    )
    
    parser.add_argument(
        "-t", "--template",
        default="professional",
        choices=list(TEMPLATES.keys()),
        help="LaTeX template to use (default: professional)"
    )
    
    parser.add_argument(
        "--list-templates",
        action="store_true",
        help="List available templates"
    )
    
    args = parser.parse_args()
    
    if args.list_templates:
        list_templates()
        return
    
    if not args.input:
        parser.print_help()
        return
    
    success = generate_pdf(args.input, args.output, args.template)
    sys.exit(0 if success else 1)

if __name__ == "__main__":
    main()
