"""
Configuration settings for the report generator
Centralized place for all configuration options
"""

import os
from typing import Dict, Any

class ReportConfig:
    """Configuration class for report generation"""
    
    # Default settings
    DEFAULT_SETTINGS = {
        # Report template type
        "template": "standard",  # Options: "standard", "business", "academic", "technical"
        
        # Claude model settings
        "model": "claude-3-5-sonnet-20241022",
        "max_tokens": 2000,
        "temperature": 0,
        
        # Search settings
        "search_depth": "advanced",  # Options: "basic", "advanced"
        "max_search_results": 4,
        "max_sources_per_section": 8,
        "total_source_limit": 12,
        
        # Content settings
        "section_word_count": "300-500",
        "intro_word_count": "150-250", 
        "conclusion_word_count": "150-250",
        "executive_summary_word_count": "200-300",
        
        # File settings
        "output_directory": "generated_reports",
        "timestamp_format": "%Y%m%d_%H%M%S",
        
        # Prompt settings
        "prompt_version": "default",
        "language": "english",
        
        # Rate limiting settings
        "enable_rate_limiting": True,
        "anthropic_rate_limit_delay": 1.0,  # Seconds between Anthropic API calls
        "tavily_rate_limit_delay": 0.5,     # Seconds between Tavily API calls
        
        # Retry settings
        "enable_retries": True,
        "max_retries": 3,
        "retry_base_delay": 1.0,
        "retry_max_delay": 60.0,
    }
    
    def __init__(self, custom_settings: Dict[str, Any] = None):
        """Initialize configuration with optional custom settings"""
        self.settings = self.DEFAULT_SETTINGS.copy()
        
        if custom_settings:
            self.settings.update(custom_settings)
    
    def get(self, key: str, default=None):
        """Get a configuration value"""
        return self.settings.get(key, default)
    
    def set(self, key: str, value: Any):
        """Set a configuration value"""
        self.settings[key] = value
    
    def get_prompt_template(self) -> str:
        """Get the prompt template type"""
        return self.get("template", "standard")
    
    def get_word_count_for_section_type(self, section_type: str) -> str:
        """Get word count based on section type"""
        word_count_map = {
            "introduction": self.get("intro_word_count"),
            "conclusion": self.get("conclusion_word_count"),
            "executive_summary": self.get("executive_summary_word_count"),
            "default": self.get("section_word_count")
        }
        return word_count_map.get(section_type, word_count_map["default"])

# Pre-defined configurations for different use cases
BUSINESS_CONFIG = ReportConfig({
    "template": "business",
    "section_word_count": "400-600",
    "executive_summary_word_count": "250-350",
    "max_search_results": 5,
})

ACADEMIC_CONFIG = ReportConfig({
    "template": "academic", 
    "section_word_count": "500-700",
    "intro_word_count": "200-300",
    "conclusion_word_count": "200-300",
    "max_search_results": 6,
    "search_depth": "advanced",
})

TECHNICAL_CONFIG = ReportConfig({
    "template": "technical",
    "section_word_count": "400-600", 
    "max_search_results": 5,
    "max_sources_per_section": 10,
})

QUICK_CONFIG = ReportConfig({
    "template": "standard",
    "section_word_count": "200-300",
    "intro_word_count": "100-150",
    "conclusion_word_count": "100-150", 
    "max_search_results": 3,
})

# Configuration presets
CONFIG_PRESETS = {
    "business": BUSINESS_CONFIG,
    "academic": ACADEMIC_CONFIG,
    "technical": TECHNICAL_CONFIG,
    "quick": QUICK_CONFIG,
    "standard": ReportConfig(),  # Default
}

def get_config(preset_name: str = "standard") -> ReportConfig:
    """Get a configuration preset"""
    return CONFIG_PRESETS.get(preset_name, ReportConfig())

def create_custom_config(**kwargs) -> ReportConfig:
    """Create a custom configuration"""
    return ReportConfig(kwargs)