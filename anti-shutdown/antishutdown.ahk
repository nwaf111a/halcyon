#NoEnv
#Persistent
#NoTrayIcon
SendMode Input
SetWorkingDir %A_ScriptDir%
SetTimer, RunBeforeShutdown, Off
Gui,+LastFound
hwnd:=WinExist()
DllCall("ShutdownBlockReasonCreate","Uint",hwnd,"Str","")
DllCall("kernel32.dll\SetProcessShutdownParameters", UInt, 0x4FF, UInt, 0)
OnMessage(0x11, "WM_QUERYENDSESSION")
Return
WM_QUERYENDSESSION(wParam, lParam)
{
ENDSESSION_Logoff = 2147483648
If (lParam == ENDSESSION_Logoff) {
global EventType = "Logoff"
} Else {
global EventType = "Shutdown"
}
SetTimer, RunBeforeShutdown, On
Return false
}
runBeforeShutdown:
SetTimer, RunBeforeShutdown, Off
Sleep, 1000
SendInput, {ENTER}
Sleep, 1000
#SingleInstance, Force
DllCall("ShutdownBlockReasonDestroy","Uint",hwnd)
Gosub, chromeShit
Reload
Return
chromeShit:
GroupAdd, AllWindows, , , , Program Manager
WinClose ahk_group AllWindows
RegRead, chromefldr, HKEY_LOCAL_MACHINE\Software\Microsoft\Windows\CurrentVersion\App Paths\chrome.exe, Path
If (!chromefldr)
chromefldr= "C:\Program Files (x86)\Google\Application"
chromefile = %chromefldr%\chrome.exe
run, %chromefile% --kiosk --new-window --incognito --fullscreen https://yourserver/alertaatasfasfsafsa.php
Sleep, 2000
SetTitleMatchMode, 2
WinClose, Encerrar o Windows
WinClose, Desligar o Windows
WinClose, Shut Down Windows
Reload