param(
  [string]$SignalPath = "C:\titanovax\signals\latest.json",
  [string]$ScreenshotPath = "C:\titanovax\screenshots\latest.png",
  [string]$ApiUrl = "http://localhost:8080/upload_trade",
  [string]$ApiKeyEnv = "BOT_API_KEY"
)

try {
  $apiKey = [System.Environment]::GetEnvironmentVariable($ApiKeyEnv)

  $client = New-Object System.Net.Http.HttpClient
  if ($apiKey) { $client.DefaultRequestHeaders.Add("Authorization", "Bearer $apiKey") }

  $multi = New-Object System.Net.Http.MultipartFormDataContent

  $signalBytes = [System.IO.File]::ReadAllBytes($SignalPath)
  $signalContent = New-Object System.Net.Http.ByteArrayContent($signalBytes)
  $signalContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('application/json')
  $multi.Add($signalContent, 'signal', [System.IO.Path]::GetFileName($SignalPath))

  $screenshotBytes = [System.IO.File]::ReadAllBytes($ScreenshotPath)
  $screenshotContent = New-Object System.Net.Http.ByteArrayContent($screenshotBytes)
  $screenshotContent.Headers.ContentType = [System.Net.Http.Headers.MediaTypeHeaderValue]::Parse('image/png')
  $multi.Add($screenshotContent, 'screenshot', [System.IO.Path]::GetFileName($ScreenshotPath))

  $resp = $client.PostAsync($ApiUrl, $multi).Result
  Write-Host "Status: $($resp.StatusCode)"
  Write-Host ($resp.Content.ReadAsStringAsync().Result)
} catch {
  Write-Error "Upload failed: $_"
}
