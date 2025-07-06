#!/usr/bin/env python3
"""
Improved Report Generator with Separate Prompts
Clean separation of logic and content for better maintainability
"""

import asyncio
import json
import os
from typing import List, Dict, Any
from pydantic import BaseModel
from anthropic import Anthropic
from tavily import TavilyClient
from dotenv import load_dotenv

# Import our custom modules
from config import ReportConfig, get_config
from utils.prompt_loader import PromptLoader
from utils.json_parser import parse_report_plan, parse_search_queries
from utils.rate_limiter import get_rate_limiter
from utils.token_manager import create_token_manager, TokenManager

# Load environment variables
load_dotenv()

class Section(BaseModel):
    title: str
    description: str
    needs_research: bool = True
    content: str = ""

class ReportPlan(BaseModel):
    title: str
    sections: List[Section]

class ImprovedReportGenerator:
    """Improved report generator with configurable prompts and templates"""
    
    def __init__(self, config: ReportConfig = None):
        """Initialize with optional configuration"""
        self.config = config or get_config("standard")
        self.prompt_loader = PromptLoader(self.config)
        
        # Initialize API clients
        self.anthropic = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'))
        self.tavily = TavilyClient(api_key=os.getenv('TAVILY_API_KEY'))
        
        # Initialize rate limiter
        self.rate_limiter = get_rate_limiter(self.config.settings)
        
        # Initialize token manager
        if self.config.get("enable_token_management", True):
            model_name = self.config.get("token_model_name", self.config.get("model"))
            self.token_manager = create_token_manager(model_name)
        else:
            self.token_manager = None
        
        # Validate API keys
        if not os.getenv('ANTHROPIC_API_KEY'):
            raise ValueError("ANTHROPIC_API_KEY not found in environment")
        if not os.getenv('TAVILY_API_KEY'):
            raise ValueError("TAVILY_API_KEY not found in environment")
        
        # Create output directory
        os.makedirs(self.config.get("output_directory"), exist_ok=True)
    
    async def generate_report(self, topic: str) -> str:
        """Main entry point - generates complete report"""
        template = self.config.get_prompt_template()
        print(f"🔍 Generating {template} report on: {topic}")
        
        # Step 1: Plan the report structure
        print("📋 Planning report structure...")
        plan = await self._plan_report(topic)
        print(f"✅ Created plan with {len(plan.sections)} sections")
        
        # Step 2: Research and write sections
        for i, section in enumerate(plan.sections, 1):
            print(f"📝 Working on section {i}/{len(plan.sections)}: {section.title}")
            
            if section.needs_research:
                section.content = await self._research_and_write_section(section, topic)
            else:
                section.content = await self._write_contextual_section(section, plan.sections, topic)
        
        # Step 3: Compile final report
        print("📄 Compiling final report...")
        final_report = self._compile_report(plan)
        print("✅ Report generation complete!")
        
        return final_report
    
    async def _plan_report(self, topic: str) -> ReportPlan:
        """Create report structure using template-specific prompts"""
        
        # Get the appropriate planning prompt from prompt loader
        prompt = self.prompt_loader.get_structure_prompt(topic)
        
        try:
            # Create async wrapper for Anthropic API call
            async def anthropic_call():
                return self.anthropic.messages.create(
                    model=self.config.get("model"),
                    max_tokens=self.config.get("max_tokens", 1500),
                    temperature=self.config.get("temperature", 0),
                    messages=[{"role": "user", "content": prompt}]
                )
            
            response = await self.rate_limiter.call_anthropic_api(anthropic_call)
            
            # Extract JSON from response using robust parser
            content = response.content[0].text
            plan_data = parse_report_plan(content)
            
            if plan_data:
                return ReportPlan(**plan_data)
            else:
                raise ValueError("Failed to parse report plan JSON")
            
        except Exception as e:
            print(f"⚠️ Error in planning, using fallback: {e}")
            return self._create_fallback_plan(topic)
    
    def _create_fallback_plan(self, topic: str) -> ReportPlan:
        """Create a fallback plan if JSON parsing fails"""
        template = self.config.get_prompt_template()
        
        if template == "business":
            return ReportPlan(
                title=f"Business Analysis: {topic}",
                sections=[
                    Section(title="Executive Summary", description=f"Overview of {topic}", needs_research=False),
                    Section(title="Market Analysis", description=f"Market analysis of {topic}", needs_research=True),
                    Section(title="Strategic Recommendations", description="Recommendations", needs_research=False)
                ]
            )
        elif template == "academic":
            return ReportPlan(
                title=f"Academic Review: {topic}",
                sections=[
                    Section(title="Abstract", description=f"Abstract for {topic}", needs_research=False),
                    Section(title="Literature Review", description=f"Literature review of {topic}", needs_research=True),
                    Section(title="Conclusion", description="Conclusions", needs_research=False)
                ]
            )
        else:
            return ReportPlan(
                title=f"Research Report: {topic}",
                sections=[
                    Section(title="Introduction", description=f"Overview of {topic}", needs_research=False),
                    Section(title="Main Analysis", description=f"Core analysis of {topic}", needs_research=True),
                    Section(title="Conclusion", description="Summary and insights", needs_research=False)
                ]
            )
    
    async def _research_and_write_section(self, section: Section, topic: str) -> str:
        """Research and write a section using configured prompts"""
        
        # Generate search queries using prompt loader
        queries = await self._generate_search_queries(section, topic)
        
        # Search the web
        search_results = await self._search_web(queries)
        
        # Write section based on research using appropriate prompt
        return await self._write_section_with_sources(section, search_results, topic)
    
    async def _generate_search_queries(self, section: Section, topic: str) -> List[str]:
        """Generate targeted search queries using prompt loader"""
        
        prompt = self.prompt_loader.get_query_generation_prompt(
            section.title, section.description, topic
        )

        try:
            # Create async wrapper for Anthropic API call
            async def anthropic_call():
                return self.anthropic.messages.create(
                    model=self.config.get("model"),
                    max_tokens=500,
                    temperature=self.config.get("temperature", 0),
                    messages=[{"role": "user", "content": prompt}]
                )
            
            response = await self.rate_limiter.call_anthropic_api(anthropic_call)
            
            content = response.content[0].text
            queries = parse_search_queries(content)
            
            if queries:
                return queries
            else:
                raise ValueError("Failed to parse search queries JSON")
            
        except Exception as e:
            print(f"⚠️ Error generating queries, using fallback: {e}")
            return [f"{topic} {section.title}", f"{section.description} 2024"]
    
    async def _search_web(self, queries: List[str]) -> List[Dict[str, Any]]:
        """Search web using Tavily with configured parameters"""
        
        all_results = []
        max_results = self.config.get("max_search_results", 4)
        search_depth = self.config.get("search_depth", "advanced")
        
        for query in queries:
            try:
                print(f"🔍 Searching: {query}")
                
                # Create async wrapper for Tavily API call
                async def tavily_call():
                    return self.tavily.search(
                        query=query,
                        search_depth=search_depth,
                        max_results=max_results,
                        include_raw_content=True
                    )
                
                results = await self.rate_limiter.call_tavily_api(tavily_call)
                
                if 'results' in results:
                    all_results.extend(results['results'])
                    
            except Exception as e:
                print(f"⚠️ Search error for '{query}': {e}")
                continue
        
        # Remove duplicates and limit results
        seen_urls = set()
        unique_results = []
        
        for result in all_results:
            url = result.get('url', '')
            if url not in seen_urls:
                seen_urls.add(url)
                unique_results.append(result)
        
        total_limit = self.config.get("total_source_limit", 12)
        return unique_results[:total_limit]
    
    async def _write_section_with_sources(self, section: Section, search_results: List[Dict], topic: str) -> str:
        """Write section content using prompt loader with token management"""
        
        # Determine section type for appropriate prompting
        section_type = self._determine_section_type(section.title)
        
        # Get the appropriate writing prompt (without sources first)
        initial_prompt = self.prompt_loader.get_section_writing_prompt(
            section.title, section.description, topic, "", section_type
        )
        
        # Optimize sources for context window if token management is enabled
        if self.token_manager:
            optimized_sources, token_usage = self.token_manager.optimize_sources_for_context(
                search_results, initial_prompt
            )
            sources_text = self.token_manager.format_optimized_sources(optimized_sources)
            
            # Show token usage if reporting is enabled
            if self.config.get("token_enable_usage_reporting", True):
                print(f"📊 Token usage for {section.title}: {token_usage.usage_percentage:.1f}%")
                if token_usage.usage_percentage > 85:
                    print(f"⚠️ High token usage detected for {section.title}")
        else:
            # Fallback to original method
            sources_text = self._format_sources(search_results)
        
        # Get the final prompt with optimized sources
        prompt = self.prompt_loader.get_section_writing_prompt(
            section.title, section.description, topic, sources_text, section_type
        )

        try:
            # Create async wrapper for Anthropic API call
            async def anthropic_call():
                return self.anthropic.messages.create(
                    model=self.config.get("model"),
                    max_tokens=self.config.get("max_tokens", 2000),
                    temperature=self.config.get("temperature", 0),
                    messages=[{"role": "user", "content": prompt}]
                )
            
            response = await self.rate_limiter.call_anthropic_api(anthropic_call)
            
            return response.content[0].text
            
        except Exception as e:
            print(f"⚠️ Error writing section: {e}")
            return f"## {section.title}\n\nContent for {section.description} could not be generated due to an error."
    
    def _format_sources(self, search_results: List[Dict]) -> str:
        """Format search results for prompt inclusion (fallback method)"""
        sources_text = ""
        max_sources = self.config.get("max_sources_per_section", 8)
        
        # Use configurable source content limit
        max_source_content = self.config.get("token_max_source_content", 500)
        
        for i, result in enumerate(search_results[:max_sources], 1):
            title = result.get('title', 'Unknown')
            content = result.get('content', result.get('raw_content', ''))[:max_source_content]
            url = result.get('url', '')
            
            sources_text += f"\nSource {i}: {title}\nURL: {url}\nContent: {content}\n---"
        
        return sources_text
    
    def _determine_section_type(self, section_title: str) -> str:
        """Determine section type for appropriate prompt selection"""
        title_lower = section_title.lower()
        
        if "intro" in title_lower:
            return "introduction"
        elif "conclusion" in title_lower:
            return "conclusion"
        elif "executive" in title_lower or "summary" in title_lower:
            return "executive_summary"
        elif "literature" in title_lower or "review" in title_lower:
            return "literature_review"
        elif "abstract" in title_lower:
            return "abstract"
        elif "recommendation" in title_lower:
            return "recommendations"
        elif "technical" in title_lower or "architecture" in title_lower:
            return "technical_overview"
        else:
            return "default"
    
    async def _write_contextual_section(self, section: Section, all_sections: List[Section], topic: str) -> str:
        """Write intro/conclusion using contextual prompts"""
        
        context_sections = [s for s in all_sections if s.needs_research]
        context_text = "\n".join([f"- {s.title}: {s.description}" for s in context_sections])
        
        section_type = self._determine_section_type(section.title)
        
        prompt = self.prompt_loader.get_contextual_section_prompt(
            section.title, section.description, topic, context_text, section_type
        )

        try:
            # Create async wrapper for Anthropic API call
            async def anthropic_call():
                return self.anthropic.messages.create(
                    model=self.config.get("model"),
                    max_tokens=1000,
                    temperature=self.config.get("temperature", 0),
                    messages=[{"role": "user", "content": prompt}]
                )
            
            response = await self.rate_limiter.call_anthropic_api(anthropic_call)
            
            return response.content[0].text
            
        except Exception as e:
            print(f"⚠️ Error writing contextual section: {e}")
            return f"## {section.title}\n\nThis section could not be generated due to an error."
    
    def _compile_report(self, plan: ReportPlan) -> str:
        """Compile all sections into final markdown report"""
        
        report = f"# {plan.title}\n\n"
        
        for section in plan.sections:
            content = section.content
            if content.startswith(f"## {section.title}"):
                report += f"{content}\n\n"
            else:
                report += f"## {section.title}\n\n{content}\n\n"
        
        # Add metadata
        from datetime import datetime
        timestamp_format = self.config.get("timestamp_format", "%Y-%m-%d %H:%M:%S")
        template = self.config.get_prompt_template()
        
        report += f"\n---\n*{template.title()} report generated on {datetime.now().strftime(timestamp_format)}*"
        
        return report

    def save_report(self, report_content: str, filename: str = None) -> str:
        """Save report to configured output directory"""
        if not filename:
            from datetime import datetime
            timestamp_format = self.config.get("timestamp_format", "%Y%m%d_%H%M%S")
            timestamp = datetime.now().strftime(timestamp_format)
            template = self.config.get_prompt_template()
            filename = f"{template}_report_{timestamp}.md"
        
        output_dir = self.config.get("output_directory", "generated_reports")
        filepath = os.path.join(output_dir, filename)
        
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(report_content)
        
        return filepath

# Factory functions for different report types
async def generate_business_report(topic: str) -> str:
    """Generate a business-focused report"""
    from config import BUSINESS_CONFIG
    generator = ImprovedReportGenerator(BUSINESS_CONFIG)
    return await generator.generate_report(topic)

async def generate_academic_report(topic: str) -> str:
    """Generate an academic-style report"""
    from config import ACADEMIC_CONFIG
    generator = ImprovedReportGenerator(ACADEMIC_CONFIG)
    return await generator.generate_report(topic)

async def generate_technical_report(topic: str) -> str:
    """Generate a technical report"""
    from config import TECHNICAL_CONFIG
    generator = ImprovedReportGenerator(TECHNICAL_CONFIG)
    return await generator.generate_report(topic)

async def generate_quick_report(topic: str) -> str:
    """Generate a quick, shorter report"""
    from config import QUICK_CONFIG
    generator = ImprovedReportGenerator(QUICK_CONFIG)
    return await generator.generate_report(topic)

# Example usage with different templates
async def demo_different_templates():
    """Demonstrate different report templates"""
    topic = "Artificial Intelligence in Healthcare"
    
    print("🏢 Generating Business Report...")
    business_report = await generate_business_report(topic)
    
    print("\n🎓 Generating Academic Report...")
    academic_report = await generate_academic_report(topic)
    
    print("\n⚙️ Generating Technical Report...")
    technical_report = await generate_technical_report(topic)
    
    print("\n⚡ Generating Quick Report...")
    quick_report = await generate_quick_report(topic)
    
    print("\n✅ All reports generated successfully!")
    return {
        "business": business_report,
        "academic": academic_report, 
        "technical": technical_report,
        "quick": quick_report
    }

if __name__ == "__main__":
    # Demo the improved generator
    asyncio.run(demo_different_templates())