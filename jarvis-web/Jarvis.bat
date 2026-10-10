@echo off
rem Abre Jarvis en su propia ventana (Chrome o Edge en modo aplicacion).
start "" powershell -NoProfile -ExecutionPolicy Bypass -WindowStyle Hidden -File "%~dp0iniciar-jarvis.ps1"
