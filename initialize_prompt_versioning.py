#!/usr/bin/env python3
"""
Prompt Versioning Initialization Script
Migrates existing static prompts to the versioning system and sets up initial versions
"""

from config import get_config
from utils.prompt_loader import PromptLoader
from utils.prompt_versioning import get_prompt_version_manager


def initialize_prompt_versioning():
    """Initialize the prompt versioning system with existing prompts"""
    print("🚀 Initializing Prompt Versioning System")
    print("=" * 60)

    # Get configuration with versioning enabled
    config = get_config("standard")
    config.set("enable_prompt_versioning", True)
    config.set("prompt_version", "v1.0_static")

    # Create prompt loader
    loader = PromptLoader(config)

    if not loader.enable_versioning:
        print("❌ Prompt versioning is not enabled or failed to initialize")
        return

    print("✅ Prompt versioning system initialized")

    # Migrate existing prompts
    print("\n📦 Migrating existing static prompts...")
    migration_results = loader.migrate_static_prompts_to_versioned()

    if migration_results:
        print(f"✅ Successfully migrated {len(migration_results)} prompt types:")
        for prompt_name, count in migration_results.items():
            print(f"   • {prompt_name}: {count} version(s)")
    else:
        print("⚠️ No prompts were migrated (they may already exist)")

    # Set active versions
    print("\n🎯 Setting active versions...")
    version_manager = get_prompt_version_manager(config.settings)

    for prompt_name in migration_results:
        success = version_manager.set_active_version(prompt_name, "v1.0_static")
        if success:
            print(f"   ✅ Set {prompt_name} active version to v1.0_static")

    print("\n📊 Current system status:")
    print(f"   • Total prompt types: {len(version_manager.prompts)}")
    print(f"   • Versioning enabled: {loader.enable_versioning}")
    print(f"   • Analytics enabled: {version_manager.enable_analytics}")

    return loader, version_manager


def demo_prompt_versioning(loader: PromptLoader, version_manager):
    """Demonstrate prompt versioning functionality"""
    print("\n🧪 Demonstrating Prompt Versioning Features")
    print("=" * 60)

    # Test prompt retrieval
    print("\n1. Testing prompt retrieval...")
    structure_prompt = loader.get_structure_prompt("AI in healthcare")
    if structure_prompt:
        print(
            f"   ✅ Successfully retrieved structure prompt ({len(structure_prompt)} chars)"
        )
        print(f"   📝 Preview: {structure_prompt[:100]}...")
    else:
        print("   ❌ Failed to retrieve structure prompt")

    # Add an improved version
    print("\n2. Adding an improved prompt version...")
    improved_prompt = """You are an expert report structure planner. Create a detailed structure for a research report about: {topic}

Your task is to design a comprehensive report structure that provides excellent coverage of the topic while maintaining professional standards.

Consider these aspects:
- Target audience and their needs
- Logical flow and organization
- Depth of analysis required
- Key areas that must be covered

Think step by step about what sections are needed.

Instructions:
1. Return a JSON array of section objects
2. Each section should have:
   - title: Clear section name
   - description: Brief overview of what will be covered
   - needs_research: Boolean indicating if this section requires research

Example format:
        {{
            "title": "Section name",
            "description": "What this section will cover",
            "needs_research": true
        }}

Make the structure engaging, thorough, and well-organized for the topic: {topic}"""

    success = version_manager.add_prompt_version(
        prompt_name="REPORT_STRUCTURE_PROMPT",
        version="v1.2_enhanced",
        prompt_text=improved_prompt,
        description="Enhanced structure prompt with better instructions and clarity, fixed template placeholders",
    )

    if success:
        print("   ✅ Added improved version v1.2_enhanced")

        # Set as active
        version_manager.set_active_version("REPORT_STRUCTURE_PROMPT", "v1.2_enhanced")
        print("   ✅ Set v1.2_enhanced as active version")
    else:
        print("   ⚠️ Improved version may already exist")

    # Test with the new version
    print("\n3. Testing with improved version...")
    config = get_config("standard")
    config.set("prompt_version", "v1.2_enhanced")
    new_loader = PromptLoader(config)

    new_prompt = new_loader.get_structure_prompt("AI in healthcare")
    if new_prompt and new_prompt != structure_prompt:
        print("   ✅ Successfully using improved version")
        print(
            f"   📊 Length difference: {len(new_prompt) - len(structure_prompt)} chars"
        )
    else:
        print("   ⚠️ Still using original version or no difference detected")

    # Simulate some usage for analytics
    print("\n4. Simulating usage for analytics...")
    for i in range(5):
        loader.log_prompt_usage(
            prompt_name="REPORT_STRUCTURE_PROMPT",
            success=True,
            quality_score=0.85 + (i * 0.02),  # Slightly improving scores
            execution_time=1.2 + (i * 0.1),
            section_type="structure",
        )

    print("   ✅ Logged 5 usage events")

    # Show performance metrics
    print("\n5. Performance metrics:")
    metrics = version_manager.get_performance_metrics("REPORT_STRUCTURE_PROMPT")

    for version, metric in metrics.items():
        print(f"   Version {version}:")
        print(f"     • Usage: {metric.total_usage}")
        print(f"     • Success rate: {metric.success_rate:.1%}")
        print(f"     • Quality score: {metric.avg_quality_score:.2f}")

    # Generate performance report
    print("\n6. Generated performance report:")
    report = version_manager.create_performance_report("REPORT_STRUCTURE_PROMPT")
    print(report)


def show_usage_instructions():
    """Show instructions for using the prompt versioning system"""
    print("\n📚 How to Use Prompt Versioning")
    print("=" * 60)

    instructions = """
1. **Set Prompt Version in Config:**
   ```python
   config.set("prompt_version", "v1.1_improved")
   ```

2. **Add New Prompt Versions:**
   ```python
   version_manager.add_prompt_version(
       prompt_name="SECTION_WRITER_PROMPT",
       version="v2.0_experimental",
       prompt_text="Your improved prompt...",
       description="Testing better formatting"
   )

   # Log some test usage
   version_manager.log_prompt_usage(
       prompt_name="SECTION_WRITER_PROMPT",
       version="v2.0_experimental",
       success=True,
       execution_time=1.5,
       quality_score=0.85
   )

   # Get best performing version
   best = version_manager.get_best_performing_version("SECTION_WRITER_PROMPT")

   # Generate reports
   report = version_manager.create_performance_report()
   ```

6. **Configuration Options:**
   - `enable_prompt_versioning`: Enable/disable versioning
   - `enable_prompt_analytics`: Track usage and performance
   - `prompt_version`: Set default version to use
   - `auto_suggest_best_prompts`: Auto-switch to best performers
    """

    print(instructions)


if __name__ == "__main__":
    print("🎯 Prompt Versioning System Setup & Demo")
    print("This script initializes prompt versioning and demonstrates its features\n")

    # Initialize the system
    loader, version_manager = initialize_prompt_versioning()

    if loader and version_manager:
        # Demo the functionality
        demo_prompt_versioning(loader, version_manager)

        # Show usage instructions
        show_usage_instructions()

        print("\n✅ Prompt versioning system is now ready!")
        print(f"📁 Versions stored in: {version_manager.versions_dir}")
        print(f"📊 Analytics logged to: {version_manager.usage_log_file}")
    else:
        print("❌ Failed to initialize prompt versioning system")

    print("\n🎉 Setup complete! You can now use versioned prompts in your reports.")
