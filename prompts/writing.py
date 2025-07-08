"""
Content Writing Prompts
Prompts for writing different types of report sections
"""

SECTION_WRITER_PROMPT = """Write a comprehensive section for a research report.

Section Title: {section_title}
Section Focus: {section_description}
Overall Report Topic: {topic}

Guidelines:
- Write {word_count} words
- Use professional, informative tone
- Include specific details and examples from sources
- Use proper markdown formatting
- Start with ## {section_title}
- Include a "Sources" subsection at the end
- Cite sources as numbered references [1], [2], etc.

Available Research Sources:
{sources}

Write the complete section now:"""

INTRODUCTION_WRITER_PROMPT = """Write an introduction section for a research report.

Report Topic: {topic}
Section Title: {section_title}
Section Purpose: {section_description}

Main sections that will be covered:
{context_sections}

Guidelines for introduction:
- Write 150-250 words
- Use professional tone
- Use markdown formatting with ## {section_title}
- Provide overview and context
- Set up the structure of the report
- No citations needed (this synthesizes the report)

Write the complete introduction section now:"""

CONCLUSION_WRITER_PROMPT = """Write a conclusion section for a research report.

Report Topic: {topic}
Section Title: {section_title}
Section Purpose: {section_description}

Main sections that were covered:
{context_sections}

Guidelines for conclusion:
- Write 150-250 words
- Use professional tone
- Use markdown formatting with ## {section_title}
- Summarize key insights and implications
- Provide actionable takeaways
- End with future outlook or recommendations
- No citations needed (this synthesizes the report)

Write the complete conclusion section now:"""

# Business-specific writing prompts
BUSINESS_EXECUTIVE_SUMMARY_PROMPT = """Write an executive summary for a business report.

Report Topic: {topic}
Key sections covered: {context_sections}

Guidelines:
- Write 200-300 words maximum
- Use ## Executive Summary
- Lead with the most important insight
- Include 3-4 key findings
- End with primary recommendation
- Use bullet points for key metrics if relevant
- Write for C-level executives (concise, action-oriented)

Write the executive summary now:"""

BUSINESS_RECOMMENDATIONS_PROMPT = """Write strategic recommendations for a business report.

Report Topic: {topic}
Based on analysis from: {context_sections}

Guidelines:
- Write 200-300 words
- Use ## Strategic Recommendations
- Provide 3-5 specific, actionable recommendations
- Prioritize recommendations by impact/feasibility
- Include implementation considerations
- Use numbered list format for clarity
- Focus on business value and ROI

Write the recommendations section now:"""

# Academic-specific writing prompts
ACADEMIC_ABSTRACT_PROMPT = """Write an academic abstract for a research report.

Report Topic: {topic}
Sections covered: {context_sections}

Guidelines:
- Write 150-200 words
- Use ## Abstract
- Follow standard academic abstract structure:
  * Background/Purpose
  * Methods/Approach
  * Key findings
  * Conclusions/Implications
- Use formal academic tone
- No citations in abstract
- Be precise and concise

Write the academic abstract now:"""

ACADEMIC_LITERATURE_REVIEW_PROMPT = """Write a literature review section for an academic report.

Section Title: {section_title}
Research Focus: {section_description}
Overall Topic: {topic}

Guidelines:
- Write 400-600 words
- Use ## {section_title}
- Organize by themes or chronology
- Synthesize findings from multiple sources
- Identify gaps in current research
- Use formal academic language
- Include extensive citations [1], [2], etc.
- End with transition to current research

Available Research Sources:
{sources}

Write the literature review section now:"""

# Technical-specific writing prompts
TECHNICAL_OVERVIEW_PROMPT = """Write a technical overview section.

Section Title: {section_title}
Technical Focus: {section_description}
Overall Topic: {topic}

Guidelines:
- Write 300-500 words
- Use ## {section_title}
- Include technical specifications and details
- Use precise terminology
- Include code examples or diagrams if relevant
- Focus on architecture and implementation
- Cite technical documentation and sources
- Use clear headings for subsections

Available Technical Sources:
{sources}

Write the technical overview section now:"""
