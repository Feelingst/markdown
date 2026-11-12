@echo off
rem Crea un acceso directo "Jarvis" con icono en el escritorio.
powershell -NoProfile -ExecutionPolicy Bypass -File "%~dp0iniciar-jarvis.ps1" -CrearAccesoDirecto
