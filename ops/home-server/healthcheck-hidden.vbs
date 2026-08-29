Set shell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""D:\code\conductor\ops\home-server\healthcheck.ps1"""
exitCode = shell.Run(command, 0, True)
WScript.Quit exitCode
