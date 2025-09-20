// MT5 example: write signal JSON and take screenshot
void WriteSignalAndScreenshot()
  {
   string dir = "C:\\titanovax\\signals\\";
   string shotDir = "C:\\titanovax\\screenshots\\";
   // Ensure directories exist (EA should have created them via deploy.ps1)
   string path = dir + "latest.json";
   string json = "{\"timestamp\": " + IntegerToString(TimeCurrent()) + ", \"symbol\": \"EURUSD\", \"side\": \"BUY\", \"volume\": 0.01, \"price\": 1.12345, \"modelId\": \"demo\", \"model_version\": \"v1\", \"features_hash\": \"sha256:demo\", \"meta\": {\"reason\": \"momentum\", \"confidence\": 0.5}}";
   int fh = FileOpen(path, FILE_WRITE|FILE_TXT|FILE_ANSI);
   if(fh>=0)
     {
      FileWriteString(fh, json);
      FileClose(fh);
     }
   string shot = shotDir + "latest.png";
   ChartScreenShot(0, shot, 800, 600, ALIGN_RIGHT);
  }

// Call from EA
int OnInit()
  {
   WriteSignalAndScreenshot();
   return(INIT_SUCCEEDED);
  }

void OnDeinit(const int reason)
  {
  }

void OnTick()
  {
  }
