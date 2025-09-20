Run instructions for orchestration-bridge bot

If you saw an error like:

    can't open file '...\orchestration-bridge\orchestration-bridge\src\telegram_bot\bot.py'

This usually means you tried to run the file with a duplicated path prefix. Use the provided helper to run the bot instead.

From PowerShell (repo folder):

```powershell
Set-Location .\orchestration-bridge
powershell -ExecutionPolicy Bypass -File .\run_bot.ps1
```

Or directly:

```powershell
python .\orchestration-bridge\src\telegram_bot\bot.py
```

Note: Ensure `TELEGRAM_TOKEN` is set in `.env` and dependencies are installed.
