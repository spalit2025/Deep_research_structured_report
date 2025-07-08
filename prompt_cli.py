#!/usr/bin/env python3
"""
Prompt Versioning CLI Tool
Command-line interface for managing prompt versions and analytics
"""

import argparse
import sys
from typing import Optional

from config import get_config
from utils.prompt_versioning import get_prompt_version_manager


def list_prompts(version_manager):
    """List all prompts and their versions"""
    if not version_manager.prompts:
        print("No prompts found in the versioning system.")
        return

    print("📋 Available Prompts and Versions")
    print("=" * 60)

    for prompt_name, versions in version_manager.prompts.items():
        print(f"\n🔹 {prompt_name}")

        # Find active version
        active_version = None
        for version, prompt_version in versions.items():
            if prompt_version.is_active:
                active_version = version
                break

        for version, prompt_version in versions.items():
            status = "✅ ACTIVE" if version == active_version else "   "
            print(f"   {status} {version} - {prompt_version.description}")
            print(f"        Created: {prompt_version.created_at}")
            print(f"        Usage: {prompt_version.usage_count} times")


def add_prompt_version(
    version_manager, prompt_name: str, version: str, prompt_text: str, description: str
):
    """Add a new prompt version"""
    success = version_manager.add_prompt_version(
        prompt_name=prompt_name,
        version=version,
        prompt_text=prompt_text,
        description=description,
    )

    if success:
        print(f"✅ Added {prompt_name} version {version}")
    else:
        print(f"❌ Failed to add version {version} (may already exist)")
        return False

    # Ask if user wants to set as active
    response = input(f"Set {version} as active version? (y/n): ").lower()
    if response == "y":
        if version_manager.set_active_version(prompt_name, version):
            print(f"✅ Set {version} as active version")
        else:
            print(f"❌ Failed to set {version} as active")

    return True


def set_active_version(version_manager, prompt_name: str, version: str):
    """Set the active version for a prompt"""
    if version_manager.set_active_version(prompt_name, version):
        print(f"✅ Set {prompt_name} active version to {version}")
    else:
        print("❌ Failed to set active version (prompt or version may not exist)")


def show_analytics(version_manager, prompt_name: Optional[str] = None):
    """Show analytics for prompts"""
    if prompt_name:
        # Show analytics for specific prompt
        metrics = version_manager.get_performance_metrics(prompt_name)
        if not metrics:
            print(f"❌ No analytics found for {prompt_name}")
            return

        print(f"📊 Analytics for {prompt_name}")
        print("=" * 60)

        for version, metric in metrics.items():
            print(f"\n🔹 Version {version}")
            print(f"   Usage: {metric.total_usage} times")
            print(f"   Success Rate: {metric.success_rate:.1%}")
            print(f"   Quality Score: {metric.avg_quality_score:.2f}")
            print(f"   Avg Execution Time: {metric.avg_execution_time:.2f}s")

        # Show best performing version
        best = version_manager.get_best_performing_version(prompt_name)
        if best:
            print(f"\n🏆 Best Performing Version: {best}")
    else:
        # Show overall analytics
        report = version_manager.create_performance_report()
        print(report)


def export_prompt_version(
    version_manager, prompt_name: str, version: str, output_file: str
):
    """Export a specific prompt version to a file"""
    prompt_text = version_manager.get_prompt(prompt_name, version)
    if not prompt_text:
        print(f"❌ Prompt {prompt_name} version {version} not found")
        return

    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(prompt_text)
        print(f"✅ Exported {prompt_name} v{version} to {output_file}")
    except Exception as e:
        print(f"❌ Failed to export: {e}")


def import_prompt_version(
    version_manager, prompt_name: str, version: str, input_file: str, description: str
):
    """Import a prompt version from a file"""
    try:
        with open(input_file, encoding="utf-8") as f:
            prompt_text = f.read()

        if add_prompt_version(
            version_manager, prompt_name, version, prompt_text, description
        ):
            print(f"✅ Imported {prompt_name} v{version} from {input_file}")
        else:
            print("❌ Failed to import prompt version")
    except Exception as e:
        print(f"❌ Failed to import: {e}")


def test_prompt_version(
    version_manager, prompt_name: str, version: str, test_input: str
):
    """Test a specific prompt version"""
    prompt_text = version_manager.get_prompt(prompt_name, version)
    if not prompt_text:
        print(f"❌ Prompt {prompt_name} version {version} not found")
        return

    print(f"🧪 Testing {prompt_name} v{version}")
    print("=" * 60)

    try:
        # Try to format the prompt with the test input
        formatted_prompt = prompt_text.format(topic=test_input)
        print("✅ Prompt formatted successfully")
        print(f"📝 Preview (first 200 chars):\n{formatted_prompt[:200]}...")

        # Show full length
        print(f"\n📊 Full prompt length: {len(formatted_prompt)} characters")

    except Exception as e:
        print(f"❌ Error formatting prompt: {e}")


def main():
    """Main CLI function"""
    parser = argparse.ArgumentParser(
        description="Manage prompt versions and analytics",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  %(prog)s list                                    # List all prompts
  %(prog)s add SECTION_WRITER_PROMPT v2.0 "..."   # Add new version
  %(prog)s set-active SECTION_WRITER_PROMPT v2.0   # Set active version
  %(prog)s analytics                               # Show all analytics
  %(prog)s analytics -p SECTION_WRITER_PROMPT     # Show specific prompt analytics
  %(prog)s export SECTION_WRITER_PROMPT v2.0 prompt.txt  # Export version
  %(prog)s import SECTION_WRITER_PROMPT v2.1 prompt.txt  # Import version
  %(prog)s test SECTION_WRITER_PROMPT v2.0 "AI in healthcare"  # Test version
        """,
    )

    subparsers = parser.add_subparsers(dest="command", help="Available commands")

    # List command
    subparsers.add_parser("list", help="List all prompts and versions")

    # Add command
    add_parser = subparsers.add_parser("add", help="Add a new prompt version")
    add_parser.add_argument("prompt_name", help="Name of the prompt")
    add_parser.add_argument("version", help="Version identifier")
    add_parser.add_argument(
        "prompt_text", help="Prompt text (use quotes for multi-line)"
    )
    add_parser.add_argument(
        "-d", "--description", default="", help="Version description"
    )

    # Set active command
    set_parser = subparsers.add_parser("set-active", help="Set active version")
    set_parser.add_argument("prompt_name", help="Name of the prompt")
    set_parser.add_argument("version", help="Version to set as active")

    # Analytics command
    analytics_parser = subparsers.add_parser("analytics", help="Show analytics")
    analytics_parser.add_argument("-p", "--prompt", help="Specific prompt to analyze")

    # Export command
    export_parser = subparsers.add_parser(
        "export", help="Export prompt version to file"
    )
    export_parser.add_argument("prompt_name", help="Name of the prompt")
    export_parser.add_argument("version", help="Version to export")
    export_parser.add_argument("output_file", help="Output file path")

    # Import command
    import_parser = subparsers.add_parser(
        "import", help="Import prompt version from file"
    )
    import_parser.add_argument("prompt_name", help="Name of the prompt")
    import_parser.add_argument("version", help="Version identifier")
    import_parser.add_argument("input_file", help="Input file path")
    import_parser.add_argument(
        "-d", "--description", default="Imported version", help="Version description"
    )

    # Test command
    test_parser = subparsers.add_parser("test", help="Test a prompt version")
    test_parser.add_argument("prompt_name", help="Name of the prompt")
    test_parser.add_argument("version", help="Version to test")
    test_parser.add_argument("test_input", help="Test input (e.g., topic)")

    args = parser.parse_args()

    if not args.command:
        parser.print_help()
        return

    # Initialize version manager
    try:
        config = get_config()
        version_manager = get_prompt_version_manager(config.settings)
    except Exception as e:
        print(f"❌ Failed to initialize prompt versioning: {e}")
        return

    # Execute command
    try:
        if args.command == "list":
            list_prompts(version_manager)

        elif args.command == "add":
            add_prompt_version(
                version_manager,
                args.prompt_name,
                args.version,
                args.prompt_text,
                args.description,
            )

        elif args.command == "set-active":
            set_active_version(version_manager, args.prompt_name, args.version)

        elif args.command == "analytics":
            show_analytics(version_manager, args.prompt)

        elif args.command == "export":
            export_prompt_version(
                version_manager, args.prompt_name, args.version, args.output_file
            )

        elif args.command == "import":
            import_prompt_version(
                version_manager,
                args.prompt_name,
                args.version,
                args.input_file,
                args.description,
            )

        elif args.command == "test":
            test_prompt_version(
                version_manager, args.prompt_name, args.version, args.test_input
            )

        else:
            print(f"❌ Unknown command: {args.command}")
            parser.print_help()

    except KeyboardInterrupt:
        print("\n⚠️ Operation cancelled by user")
    except Exception as e:
        print(f"❌ Error: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
