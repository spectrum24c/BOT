# run_bot.ps1 - reliably run the Telegram bot and API
Set-Location -Path $PSScriptRoot
$botPath = Join-Path $PSScriptRoot 'src\telegram_bot\bot.py'
if (-Not (Test-Path $botPath)) {
    Write-Error "Bot file not found: $botPath"
    exit 1
}
python $botPath
