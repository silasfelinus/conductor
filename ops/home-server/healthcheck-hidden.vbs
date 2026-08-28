Set shell = CreateObject("WScript.Shell")
command = "powershell.exe -NoProfile -NonInteractive -ExecutionPolicy Bypass -File ""D:\code\conductor\ops\home-server\healthcheck-runner.ps1"""
shell.Run command, 0, True
