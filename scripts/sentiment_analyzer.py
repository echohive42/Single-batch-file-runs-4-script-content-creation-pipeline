import os
import sys
from termcolor import colored
import openai

# Constants
API_KEY = os.getenv('OPENAI_API_KEY')
MODEL = "gpt-4o"
INPUT_DIR = "input"
OUTPUT_DIR = "output"

def initialize_api():
    try:
        openai.api_key = API_KEY
        print(colored("API initialized successfully", "green"))
    except Exception as e:
        print(colored(f"Error initializing API: {str(e)}", "red"))
        sys.exit(1)

def get_content():
    try:
        # Check command line arguments first
        if len(sys.argv) > 1:
            if sys.argv[1] == '--file' and len(sys.argv) > 2:
                with open(sys.argv[2], 'r', encoding='utf-8') as f:
                    return f.read()
            return " ".join(sys.argv[1:])
        
        # Check input directory for text files
        for file in os.listdir(INPUT_DIR):
            if file.endswith('.txt'):
                with open(os.path.join(INPUT_DIR, file), 'r', encoding='utf-8') as f:
                    return f.read()
        
        print(colored("No content found to analyze!", "red"))
        return None

    except Exception as e:
        print(colored(f"Error getting content: {str(e)}", "red"))
        return None

def analyze_sentiment(content):
    try:
        print(colored("Analyzing sentiment and emotional tone...", "cyan"))
        response = openai.chat.completions.create(
            model=MODEL,
            messages=[
                {"role": "system", "content": """You are a sentiment and emotional tone analyzer. Analyze the content and provide:
                1. Overall emotional tone
                2. Sentiment progression throughout the content
                3. Key emotional triggers
                4. Audience emotional impact
                5. Emotional coherence and consistency
                Format your analysis in a clear, structured manner."""},
                {"role": "user", "content": content}
            ]
        )
        return response.choices[0].message.content
    except Exception as e:
        print(colored(f"Error during sentiment analysis: {str(e)}", "red"))
        return None

def main():
    try:
        print(colored("Sentiment Analyzer Starting...", "yellow"))
        
        # Initialize API
        initialize_api()

        # Get content
        content = get_content()
        if not content:
            sys.exit(1)

        # Analyze sentiment
        result = analyze_sentiment(content)
        
        if result:
            with open(os.path.join(OUTPUT_DIR, "sentiment_results.txt"), "w", encoding="utf-8") as f:
                f.write(result)
            print(colored("Sentiment analysis complete and saved!", "green"))
        else:
            print(colored("Sentiment analysis failed!", "red"))
            sys.exit(1)

    except Exception as e:
        print(colored(f"Fatal error in Sentiment Analyzer: {str(e)}", "red"))
        sys.exit(1)

if __name__ == "__main__":
    main() 