// MT4 example: write signal JSON and take screenshot
void WriteSignalAndScreenshot()
  {
   string dir = "C:\\titanovax\\signals\\";
   string shotDir = "C:\\titanovax\\screenshots\\";
   string path = dir + "latest.json";
   string json = "{\"timestamp\": " + TimeCurrent() + ", \"symbol\": \"EURUSD\", \"side\": \"BUY\", \"volume\": 0.01, \"price\": 1.12345, \"modelId\": \"demo\", \"model_version\": \"v1\", \"features_hash\": \"sha256:demo\", \"meta\": {\"reason\": \"momentum\", \"confidence\": 0.5}}";
   int fh = FileOpen(path, FILE_WRITE|FILE_ANSI);
   if(fh>=0)
     {
      FileWriteString(fh, json);
      FileClose(fh);
     }
   string shot = shotDir + "latest.png";
   ChartScreenShot(0, shot, 800, 600);
  }

int start()
  {
   WriteSignalAndScreenshot();
   return(0);
  }
