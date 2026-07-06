@echo off
REM Double-click launcher: starts both engines under pm2 (no-op if already
REM running), then attaches the live log stream - the same echo the old bats
REM gave you. Closing this window or Ctrl+C only detaches the view; the
REM engines keep running under pm2.
cd /d %~dp0
call pm2 start ecosystem.config.js
call pm2 logs --lines 50
