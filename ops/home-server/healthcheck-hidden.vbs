Set shell = CreateObject("WScript.Shell")
Set processEnv = shell.Environment("PROCESS")
If Len(processEnv("KR_BASE_URL")) = 0 Then
    processEnv("KR_BASE_URL") = "https://kindrobots.org"
End If
command = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""D:\code\conductor\ops\home-server\healthcheck.ps1"""
exitCode = shell.Run(command, 0, True)
WScript.Quit exitCode
