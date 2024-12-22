import os
import sys
from termcolor import colored
import openai
import json
from datetime import datetime

# Constants
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4o"
OUTPUT_DIR = "output"
REQUIRED_FILES = [
    "sentiment_results.txt",
    "context_results.txt",
    "style_results.txt"
]

def initialize_api():
    try:
        openai.api_key = API_KEY
        print(colored("API initialized successfully", "green"))
    except Exception as e:
        print(colored(f"Error initializing API: {str(e)}", "red"))
        sys.exit(1)

def collect_analyses():
    try:
        analyses = {}
        for filename in REQUIRED_FILES:
            file_path = os.path.join(OUTPUT_DIR, filename)
            if not os.path.exists(file_path):
                print(colored(f"Missing required analysis file: {filename}", "red"))
                return None
            with open(file_path, 'r', encoding='utf-8') as f:
                analyses[filename] = f.read()
        return analyses

    except Exception as e:
        print(colored(f"Error collecting analyses: {str(e)}", "red"))
        return None

def synthesize_analyses(analyses):
    try:
        print(colored("Synthesizing all analyses...", "cyan"))
        
        # Prepare context from all analyses
        context = "\n\n".join([f"=== {title} ===\n{content}" 
                             for title, content in analyses.items()])
        
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": """You are a content synthesis expert. Create a comprehensive report that:
                1. Synthesizes insights from sentiment, context, and style analyses
                2. Identifies patterns and relationships across analyses
                3. Provides holistic content understanding
                4. Generates actionable recommendations
                5. Highlights key findings and implications
                Format your synthesis in a clear, structured manner with sections."""},
                {"role": "user", "content": context}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(colored(f"Error during synthesis: {str(e)}", "red"))
        return None

def save_final_report(synthesis, analyses):
    try:
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        report_dir = os.path.join(OUTPUT_DIR, f"final_report_{timestamp}")
        os.makedirs(report_dir, exist_ok=True)

        # Save synthesis
        with open(os.path.join(report_dir, "synthesis.txt"), "w", encoding="utf-8") as f:
            f.write(synthesis)

        # Save individual analyses
        for filename, content in analyses.items():
            with open(os.path.join(report_dir, f"source_{filename}"), "w", encoding="utf-8") as f:
                f.write(content)

        # Create index file
        index = {
            "timestamp": timestamp,
            "synthesis": "synthesis.txt",
            "source_files": list(analyses.keys())
        }
        with open(os.path.join(report_dir, "index.json"), "w", encoding="utf-8") as f:
            json.dump(index, f, indent=2)

        return report_dir

    except Exception as e:
        print(colored(f"Error saving final report: {str(e)}", "red"))
        return None

def main():
    try:
        print(colored("Content Synthesizer Starting...", "yellow"))
        
        # Initialize API
        initialize_api()

        # Collect all analyses
        analyses = collect_analyses()
        if not analyses:
            print(colored("Failed to collect all required analyses!", "red"))
            sys.exit(1)

        # Synthesize analyses
        synthesis = synthesize_analyses(analyses)
        
        if synthesis:
            # Save final report
            report_dir = save_final_report(synthesis, analyses)
            if report_dir:
                print(colored(f"Final synthesis report generated in: {report_dir}", "green"))
            else:
                print(colored("Failed to save final report!", "red"))
                sys.exit(1)
        else:
            print(colored("Synthesis failed!", "red"))
            sys.exit(1)

    except Exception as e:
        print(colored(f"Fatal error in Content Synthesizer: {str(e)}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main() 