@echo off
echo Activating Conda Environment...
call conda activate basic3
if errorlevel 1 (
    echo Failed to activate conda environment
    exit /b 1
)

echo Starting Echo Hive Content Processing System...

if not exist "input" mkdir input

:: Clear output directory completely
if exist "output" (
    echo Cleaning previous output...
    rd /s /q "output"
)
mkdir output

echo Starting parallel content analysis...

:: Start processes and capture their PIDs
start /B "Sentiment Analysis" cmd /c "python scripts/sentiment_analyzer.py %* > output/sentiment.log 2>&1"
start /B "Context Analysis" cmd /c "python scripts/context_analyzer.py %* > output/context.log 2>&1"
start /B "Style Analysis" cmd /c "python scripts/style_analyzer.py %* > output/style.log 2>&1"

echo Waiting for analysis to complete...

:: Check completion with better feedback
set max_attempts=30
set attempt=0

:check_completion
set /a attempt+=1
set /a complete=0
if exist "output\sentiment_results.txt" set /a complete+=1
if exist "output\context_results.txt" set /a complete+=1
if exist "output\style_results.txt" set /a complete+=1

echo Progress: %complete%/3 analyzers complete (Attempt %attempt% of %max_attempts%)

if %complete% equ 3 (
    echo All analyses completed successfully!
    goto synthesis
)

if %attempt% geq %max_attempts% (
    echo Analysis timed out after %max_attempts% attempts
    echo Checking log files for errors...
    type output\sentiment.log
    type output\context.log
    type output\style.log
    exit /b 1
)

timeout /t 2 /nobreak > nul
goto check_completion

:synthesis
echo All analyzers complete! Starting synthesis...
python scripts/content_synthesizer.py %*
if errorlevel 1 (
    echo Synthesis failed, check logs for details
    exit /b 1
)

echo Echo Hive processing complete!
pause
