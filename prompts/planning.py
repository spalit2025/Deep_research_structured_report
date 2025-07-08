"""
Report Planning Prompts
Prompts for planning report structure and generating search queries
"""

REPORT_STRUCTURE_PROMPT = """Plan a comprehensive research report on: {topic}

Create a report structure with 4-6 sections following this template:
- Introduction (brief overview, no research needed)
- 2-4 main content sections (each needs research)
- Conclusion (summary and insights, no research needed)

Return ONLY valid JSON in this exact format:
{{
    "title": "Professional report title for {topic}",
    "sections": [
        {{"title": "Introduction", "description": "Brief overview of the topic", "needs_research": false}},
        {{"title": "Section Name", "description": "What this section covers", "needs_research": true}},
        {{"title": "Conclusion", "description": "Summary and key insights", "needs_research": false}}
    ]
}}"""

QUERY_GENERATION_PROMPT = """Generate 3-4 specific web search queries for researching this section:

Section: {section_title}
Description: {section_description}
Overall Topic: {topic}

Requirements:
- Queries should be specific and targeted
- Include recent year (2024/2025) where relevant
- Focus on authoritative sources
- Avoid overly broad queries

Return ONLY a JSON array of strings:
["query 1", "query 2", "query 3"]"""

# Alternative planning templates
BUSINESS_STRUCTURE_PROMPT = """Plan a business analysis report on: {topic}

Create a business-focused structure with these sections:
- Executive Summary (no research needed)
- Market Overview (needs research)
- Competitive Analysis (needs research)
- Key Trends & Opportunities (needs research)
- Strategic Recommendations (no research needed)

Return ONLY valid JSON in this exact format:
{{
    "title": "Business Analysis: {topic}",
    "sections": [
        {{"title": "Executive Summary", "description": "High-level overview and key findings", "needs_research": false}},
        {{"title": "Market Overview", "description": "Current market size, growth, and dynamics", "needs_research": true}},
        {{"title": "Competitive Analysis", "description": "Key players and competitive landscape", "needs_research": true}},
        {{"title": "Key Trends & Opportunities", "description": "Emerging trends and market opportunities", "needs_research": true}},
        {{"title": "Strategic Recommendations", "description": "Actionable insights and next steps", "needs_research": false}}
    ]
}}"""

ACADEMIC_STRUCTURE_PROMPT = """Plan an academic research report on: {topic}

Create an academic-style structure with these sections:
- Abstract (no research needed)
- Introduction & Background (needs research)
- Literature Review (needs research)
- Current Research & Findings (needs research)
- Discussion & Analysis (needs research)
- Conclusion & Future Directions (no research needed)

Return ONLY valid JSON in this exact format:
{{
    "title": "Academic Review: {topic}",
    "sections": [
        {{"title": "Abstract", "description": "Summary of the research and key findings", "needs_research": false}},
        {{"title": "Introduction & Background", "description": "Context and foundational knowledge", "needs_research": true}},
        {{"title": "Literature Review", "description": "Review of existing research and publications", "needs_research": true}},
        {{"title": "Current Research & Findings", "description": "Latest research developments and discoveries", "needs_research": true}},
        {{"title": "Discussion & Analysis", "description": "Analysis of findings and implications", "needs_research": true}},
        {{"title": "Conclusion & Future Directions", "description": "Summary and future research directions", "needs_research": false}}
    ]
}}"""
