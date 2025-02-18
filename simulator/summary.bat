@echo off
for /l %%i in (1,1,100) do (
    python app.py >> output.csv
)
pause
