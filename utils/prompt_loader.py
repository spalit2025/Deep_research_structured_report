"""
Prompt loading utilities
Handles loading and formatting prompts from separate files
"""

import importlib
from typing import Dict, Any
from config import ReportConfig

class PromptLoader:
    """Loads and formats prompts based on configuration"""
    
    def __init__(self, config: ReportConfig):
        self.config = config
        self.template = config.get_prompt_template()
        
        # Import prompt modules
        self.planning_prompts = importlib.import_module("prompts.planning")
        self.writing_prompts = importlib.import_module("prompts.writing")
    
    def get_structure_prompt(self, topic: str) -> str:
        """Get the appropriate structure planning prompt"""
        
        template = self.template.upper()
        prompt_name = f"{template}_STRUCTURE_PROMPT"
        
        # Try to get template-specific prompt, fall back to default
        if hasattr(self.planning_prompts, prompt_name):
            prompt = getattr(self.planning_prompts, prompt_name)
        else:
            prompt = self.planning_prompts.REPORT_STRUCTURE_PROMPT
        
        return prompt.format(topic=topic)
    
    def get_query_generation_prompt(self, section_title: str, section_description: str, topic: str) -> str:
        """Get the query generation prompt"""
        return self.planning_prompts.QUERY_GENERATION_PROMPT.format(
            section_title=section_title,
            section_description=section_description,
            topic=topic
        )
    
    def get_section_writing_prompt(self, section_title: str, section_description: str, 
                                 topic: str, sources: str, section_type: str = "default") -> str:
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
            word_count=word_count
        )
    
    def get_contextual_section_prompt(self, section_title: str, section_description: str,
                                    topic: str, context_sections: str, section_type: str) -> str:
        """Get prompt for intro/conclusion sections that use context"""
        
        if "intro" in section_title.lower() or section_type == "introduction":
            if self.template == "business":
                prompt = self.writing_prompts.BUSINESS_EXECUTIVE_SUMMARY_PROMPT
            elif self.template == "academic":
                prompt = self.writing_prompts.ACADEMIC_ABSTRACT_PROMPT
            else:
                prompt = self.writing_prompts.INTRODUCTION_WRITER_PROMPT
        
        elif section_type == "executive_summary":
            if self.template == "business":
                prompt = self.writing_prompts.BUSINESS_EXECUTIVE_SUMMARY_PROMPT
            elif self.template == "academic":
                prompt = self.writing_prompts.ACADEMIC_ABSTRACT_PROMPT
            else:
                prompt = self.writing_prompts.INTRODUCTION_WRITER_PROMPT
        
        elif "conclusion" in section_title.lower() or section_type == "conclusion":
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
            context_sections=context_sections
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

def get_writing_prompt(section_title: str, section_description: str, topic: str, 
                      sources: str, template: str = "standard", section_type: str = "default") -> str:
    """Quick function to get a writing prompt"""
    from config import get_config
    config = get_config(template)
    loader = PromptLoader(config)
    return loader.get_section_writing_prompt(section_title, section_description, topic, sources, section_type)