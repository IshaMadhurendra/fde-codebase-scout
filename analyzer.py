import json
import anthropic
from dotenv import load_dotenv

load_dotenv()


def analyze_repo(repo_description: str) -> dict:
    """Analyze a repository using Claude API and return structured JSON analysis."""
    client = anthropic.Anthropic()

    system_prompt = """You are a senior Forward Deployed Engineer (FDE) analyzing a client's codebase for rapid onboarding.
You must respond ONLY with valid JSON — no markdown, no backticks, no explanations outside the JSON.

Analyze the provided codebase description and generate a comprehensive assessment following this exact JSON schema:

{
  "health_score": <integer 0-100>,
  "summary": "<executive summary of the codebase, 2-3 sentences>",
  "architecture": [
    {
      "layer": "<layer name: Frontend, Backend, Database, Auth, Infrastructure, etc.>",
      "tech": "<specific technologies used>",
      "status": "<ok|warn|error>",
      "notes": "<specific observations, issues, or strengths>",
      "connections": ["<other layer names this connects to>"]
    }
  ],
  "file_tree": {
    "<top-level dir>/": {
      "<subdir>/": {"<file>": null},
      "<file>": null
    }
  },
  "quick_wins": [
    {
      "title": "<actionable title>",
      "description": "<detailed description of what to do and why>",
      "impact": "<Critical|High|Medium>",
      "effort_sp": <integer 1-8>,
      "risk": "<Low|Medium|High>",
      "category": "<security|performance|reliability|maintainability|testing>"
    }
  ],
  "onboarding_plan": [
    {
      "week": "Week 1",
      "focus": "<focus area>",
      "tasks": "<comma-separated list of tasks>",
      "story_points": <integer>
    }
  ],
  "mermaid_diagram": "<valid mermaid graph TD diagram showing architecture connections>"
}

Guidelines:
- health_score: Consider code quality, security, test coverage, documentation, dependency freshness, architecture clarity
- architecture: Include 4-6 layers depending on the codebase
- file_tree: Generate a realistic file structure based on the tech stack (15-30 files)
- quick_wins: Provide 5-7 actionable items, sorted by impact
- onboarding_plan: Generate a 3-4 week plan with realistic SP allocation (total 20-35 SP)
- mermaid_diagram: Use graph TD with descriptive node labels and edge labels

Be specific and realistic. Base your analysis on real-world patterns for the given tech stack."""

    user_prompt = f"""Analyze this codebase and provide a full FDE onboarding assessment:

{repo_description}

Remember: respond ONLY with valid JSON, no markdown formatting."""

    try:
        message = client.messages.create(
            model="claude-sonnet-4-20250514",
            max_tokens=4096,
            system=system_prompt,
            messages=[{"role": "user", "content": user_prompt}],
        )

        response_text = message.content[0].text

        # Try to parse JSON, handle potential issues
        try:
            result = json.loads(response_text)
        except json.JSONDecodeError:
            # Try to extract JSON from response if wrapped in backticks
            import re
            json_match = re.search(r'\{[\s\S]*\}', response_text)
            if json_match:
                result = json.loads(json_match.group())
            else:
                raise ValueError("Could not parse JSON from Claude response")

        return result

    except anthropic.APIConnectionError:
        raise ConnectionError("Failed to connect to Anthropic API. Check your internet connection.")
    except anthropic.AuthenticationError:
        raise PermissionError("Invalid API key. Please check your ANTHROPIC_API_KEY in .env file.")
    except anthropic.RateLimitError:
        raise RuntimeError("Rate limit exceeded. Please wait a moment and try again.")
    except Exception as e:
        raise RuntimeError(f"Analysis failed: {str(e)}")
