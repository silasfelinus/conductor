@echo off
REM Double-click launcher: starts ComfyUI and the agents under pm2 (no-op if
REM already running), then attaches the live log stream - the same echo the old
REM bats gave you. Closing this window or Ctrl+C only detaches the view; the
REM processes keep running under pm2.
cd /d %~dp0
call pm2 start ecosystem.config.js
call pm2 logs --lines 50
