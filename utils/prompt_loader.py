"""
Prompt loading utilities
Handles loading and formatting prompts from separate files with versioning support
"""

import importlib
from typing import Dict, Optional

from config import ReportConfig


class PromptLoader:
    """Loads and formats prompts based on configuration with versioning support"""

    def __init__(self, config: ReportConfig):
        self.config = config
        self.template = config.get_prompt_template()
        self.prompt_version = config.get("prompt_version", "default")
        self.enable_versioning = config.get("enable_prompt_versioning", True)

        # Import prompt modules for fallback
        self.planning_prompts = importlib.import_module("prompts.planning")
        self.writing_prompts = importlib.import_module("prompts.writing")

        # Initialize version manager if enabled
        self.version_manager = None
        if self.enable_versioning:
            try:
                from .prompt_versioning import get_prompt_version_manager

                self.version_manager = get_prompt_version_manager(config.settings)
            except Exception as e:
                print(f"⚠️ Failed to initialize prompt versioning: {e}")
                self.enable_versioning = False

    def get_structure_prompt(self, topic: str) -> str:
        """Get the appropriate structure planning prompt"""

        template = self.template.upper()
        prompt_name = f"{template}_STRUCTURE_PROMPT"

        # Try versioned prompt first
        if self.enable_versioning and self.version_manager:
            versioned_prompt = self._get_versioned_prompt(
                prompt_name, fallback_prompt_name="REPORT_STRUCTURE_PROMPT"
            )
            if versioned_prompt:
                return versioned_prompt.format(topic=topic)

        # Fall back to static prompts
        if hasattr(self.planning_prompts, prompt_name):
            prompt = getattr(self.planning_prompts, prompt_name)
        else:
            prompt = self.planning_prompts.REPORT_STRUCTURE_PROMPT

        return prompt.format(topic=topic)

    def get_query_generation_prompt(
        self, section_title: str, section_description: str, topic: str
    ) -> str:
        """Get the query generation prompt"""
        return self.planning_prompts.QUERY_GENERATION_PROMPT.format(
            section_title=section_title,
            section_description=section_description,
            topic=topic,
        )

    def get_section_writing_prompt(
        self,
        section_title: str,
        section_description: str,
        topic: str,
        sources: str,
        section_type: str = "default",
    ) -> str:
        """Get the appropriate section writing prompt"""

        # Determine word count based on section type
        word_count = self.config.get_word_count_for_section_type(section_type)

        # Choose the right prompt based on template and section type
        prompt = self._select_writing_prompt(section_type)

        return prompt.format(
            section_title=section_title,
            section_description=section_description,
            topic=topic,
            sources=sources,
            word_count=word_count,
        )

    def get_contextual_section_prompt(
        self,
        section_title: str,
        section_description: str,
        topic: str,
        context_sections: str,
        section_type: str,
    ) -> str:
        """Get prompt for intro/conclusion sections that use context"""

        if (
            "intro" in section_title.lower()
            or section_type == "introduction"
            or section_type == "executive_summary"
        ):
            if self.template == "business":
                prompt = self.writing_prompts.BUSINESS_EXECUTIVE_SUMMARY_PROMPT
            elif self.template == "academic":
                prompt = self.writing_prompts.ACADEMIC_ABSTRACT_PROMPT
            else:
                prompt = self.writing_prompts.INTRODUCTION_WRITER_PROMPT

        elif (
            section_type == "recommendations"
            or "conclusion" in section_title.lower()
            or section_type == "conclusion"
        ):
            if self.template == "business":
                prompt = self.writing_prompts.BUSINESS_RECOMMENDATIONS_PROMPT
            else:
                prompt = self.writing_prompts.CONCLUSION_WRITER_PROMPT

        else:
            # Default to introduction prompt
            prompt = self.writing_prompts.INTRODUCTION_WRITER_PROMPT

        return prompt.format(
            section_title=section_title,
            section_description=section_description,
            topic=topic,
            context_sections=context_sections,
        )

    def _select_writing_prompt(self, section_type: str) -> str:
        """Select the appropriate writing prompt based on template and section type"""

        # Template-specific prompts
        if self.template == "academic":
            if section_type == "literature_review":
                return self.writing_prompts.ACADEMIC_LITERATURE_REVIEW_PROMPT
            elif section_type == "abstract":
                return self.writing_prompts.ACADEMIC_ABSTRACT_PROMPT

        elif self.template == "technical":
            if section_type in ["overview", "architecture", "implementation"]:
                return self.writing_prompts.TECHNICAL_OVERVIEW_PROMPT

        elif self.template == "business":
            if section_type == "executive_summary":
                return self.writing_prompts.BUSINESS_EXECUTIVE_SUMMARY_PROMPT
            elif section_type == "recommendations":
                return self.writing_prompts.BUSINESS_RECOMMENDATIONS_PROMPT

        # Default to standard section writer
        return self.writing_prompts.SECTION_WRITER_PROMPT

    def _get_versioned_prompt(
        self, prompt_name: str, fallback_prompt_name: str = None
    ) -> Optional[str]:
        """
        Get a versioned prompt with fallback to static prompts

        Args:
            prompt_name: Name of the prompt to retrieve
            fallback_prompt_name: Fallback prompt name if versioned not found

        Returns:
            Prompt text or None if not found
        """
        if not self.version_manager:
            return None

        # Try to get the versioned prompt
        versioned_prompt = self.version_manager.get_prompt(
            prompt_name, self.prompt_version
        )

        if versioned_prompt:
            return versioned_prompt

        # Try fallback prompt name if provided
        if fallback_prompt_name:
            versioned_prompt = self.version_manager.get_prompt(
                fallback_prompt_name, self.prompt_version
            )
            if versioned_prompt:
                return versioned_prompt

        return None

    def log_prompt_usage(
        self,
        prompt_name: str,
        success: bool,
        quality_score: float = 0.0,
        execution_time: float = 0.0,
        section_type: str = "unknown",
    ) -> None:
        """
        Log usage of a prompt for analytics

        Args:
            prompt_name: Name of the prompt that was used
            success: Whether the prompt usage was successful
            quality_score: Quality score (0.0-1.0)
            execution_time: Time taken to execute
            section_type: Type of section (introduction, conclusion, etc.)
        """
        if self.enable_versioning and self.version_manager:
            self.version_manager.log_usage(
                prompt_name=prompt_name,
                version=self.prompt_version,
                success=success,
                quality_score=quality_score,
                execution_time=execution_time,
                template_type=self.template,
                section_type=section_type,
            )

    def migrate_static_prompts_to_versioned(self) -> Dict[str, int]:
        """
        Migrate existing static prompts to the versioning system

        Returns:
            Dictionary mapping prompt names to number of versions added
        """
        if not self.enable_versioning or not self.version_manager:
            return {}

        migration_results = {}

        # Migrate planning prompts
        planning_attrs = [
            attr
            for attr in dir(self.planning_prompts)
            if not attr.startswith("_") and attr.isupper()
        ]

        for attr_name in planning_attrs:
            prompt_text = getattr(self.planning_prompts, attr_name)
            if isinstance(prompt_text, str):
                success = self.version_manager.add_prompt_version(
                    prompt_name=attr_name,
                    version="v1.0_static",
                    prompt_text=prompt_text,
                    description="Migrated from static prompts",
                )
                if success:
                    migration_results[attr_name] = (
                        migration_results.get(attr_name, 0) + 1
                    )

        # Migrate writing prompts
        writing_attrs = [
            attr
            for attr in dir(self.writing_prompts)
            if not attr.startswith("_") and attr.isupper()
        ]

        for attr_name in writing_attrs:
            prompt_text = getattr(self.writing_prompts, attr_name)
            if isinstance(prompt_text, str):
                success = self.version_manager.add_prompt_version(
                    prompt_name=attr_name,
                    version="v1.0_static",
                    prompt_text=prompt_text,
                    description="Migrated from static prompts",
                )
                if success:
                    migration_results[attr_name] = (
                        migration_results.get(attr_name, 0) + 1
                    )

        return migration_results


def create_prompt_loader(config: ReportConfig = None) -> PromptLoader:
    """Factory function to create a prompt loader"""
    if config is None:
        from config import get_config

        config = get_config()

    return PromptLoader(config)


# Convenience functions for quick access
def get_planning_prompt(topic: str, template: str = "standard") -> str:
    """Quick function to get a planning prompt"""
    from config import get_config

    config = get_config(template)
    loader = PromptLoader(config)
    return loader.get_structure_prompt(topic)


def get_writing_prompt(
    section_title: str,
    section_description: str,
    topic: str,
    sources: str,
    template: str = "standard",
    section_type: str = "default",
) -> str:
    """Quick function to get a writing prompt"""
    from config import get_config

    config = get_config(template)
    loader = PromptLoader(config)
    return loader.get_section_writing_prompt(
        section_title, section_description, topic, sources, section_type
    )
