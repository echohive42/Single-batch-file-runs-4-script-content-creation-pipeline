# Echo Hive

Echo Hive is a parallel content analysis system that processes text through multiple specialized analyzers simultaneously and synthesizes the results into a comprehensive report.

## Overview

The system consists of three parallel analyzers:

- **Sentiment Analyzer**: Analyzes emotional tone and impact
- **Context Analyzer**: Evaluates themes and messaging
- **Style Analyzer**: Examines writing style and structure

These analyses are then combined by a Content Synthesizer to produce a final report.

## ❤️ Support & Get 400+ AI Projects

This is one of 400+ fascinating projects in my collection! [Support me on Patreon](https://www.patreon.com/c/echohive42/membership) to get:

- 🎯 Access to 400+ AI projects (and growing daily!)
  - Including advanced projects like [2 Agent Real-time voice template with turn taking](https://www.patreon.com/posts/2-agent-real-you-118330397)
- 📥 Full source code & detailed explanations
- 📚 1000x Cursor Course
- 🎓 Live coding sessions & AMAs
- 💬 1-on-1 consultations (higher tiers)
- 🎁 Exclusive discounts on AI tools & platforms (up to $180 value)

## Prerequisites

- Python 3.8+
- Conda (for environment management)
- OpenAI API key

## Installation

1. Clone this repository:

```bash
git clone [repository-url]
cd Echo-Hive
```

2. Set up your environment:

```bash
# Create and activate your conda environment (use your preferred name instead of 'basic3')
conda create -n your_env_name python=3.8
conda activate your_env_name

# Install required packages
pip install -r requirements.txt
```

3. Set your OpenAI API key as an environment variable:

```bash
set OPENAI_API_KEY=your-api-key-here
```

## Batch File Explanation

The `run_echo_hive.bat` script orchestrates the entire analysis process:

1. **Environment Activation**:

   ```batch
   call conda activate basic3
   ```

   > ⚠️ Important: Modify this line to use your conda environment name instead of 'basic3'
   >
2. **Directory Setup**:

   - Creates 'input' and 'output' directories if they don't exist
   - Clears any existing results from previous runs
3. **Parallel Processing**:

   - Launches three analyzer scripts simultaneously
   - Each analyzer runs in the background and logs to separate files

   ```batch
   start /B "Sentiment Analysis" cmd /c "python scripts/sentiment_analyzer.py %* > output/sentiment.log 2>&1"
   ```
4. **Progress Monitoring**:

   - Checks for completion of each analyzer (max 30 attempts, 2 seconds apart)
   - Shows progress updates: "Progress: X/3 analyzers complete"
   - Times out after 60 seconds if not all analyzers complete
5. **Synthesis**:

   - Once all analyzers complete, runs the content synthesizer
   - Creates a timestamped final report directory

## Usage

1. Place your text file(s) in the `input` directory or prepare to input text via command line
2. Run the batch file: (you can double click this file as well if you set sample.txt in input folder)

```bash
run_echo_hive.bat
```

   Or with direct text input:

```bash
run_echo_hive.bat "Your text content here"
```

   Or with a specific file:

```bash
run_echo_hive.bat --file path/to/your/file.txt
```

3. Check the `output` directory for results:
   - Individual analyzer results
   - Final synthesis report in a timestamped directory

## Output Structure

The `output` directory contains the following files and directories:

- **sentiment**: This directory contains results from the Sentiment Analyzer.

The `sentiment` directory contains the following files:

- **sentiment.log**: This file contains logs from the Sentiment Analyzer.

The `output` directory also contains the following files:

- **context.log**: This file contains logs from the Context Analyzer.
- **style.log**: This file contains logs from the Style Analyzer.
- **synthesizer.log**: This file contains logs from the Content Synthesizer.

The final synthesis report is stored in a timestamped directory in the `output` directory.
