# Abre Jarvis como aplicación de escritorio en Windows.
#
# Sirve esta carpeta en http://localhost:8765 y abre Chrome o Edge en modo
# aplicación (ventana propia, sin barra de direcciones) con un perfil dedicado,
# para que el permiso del micrófono y las claves se recuerden entre sesiones.
# El servidor se cierra solo al cerrar la ventana de Jarvis.
#
# Uso: Jarvis.bat (doble clic), o con -CrearAccesoDirecto para poner un
# acceso directo "Jarvis" en el escritorio.
param([switch]$CrearAccesoDirecto)

$ErrorActionPreference = 'Stop'
$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
$Port = 8765
$Url = "http://localhost:$Port/"
$OnWindows = $env:OS -eq 'Windows_NT'
$DataDir = if ($env:LOCALAPPDATA) { Join-Path $env:LOCALAPPDATA 'JarvisTomas' } else { Join-Path $HOME '.jarvis-tomas' }
$ProfileDir = Join-Path $DataDir 'perfil'

function Show-Message([string]$text) {
  try {
    Add-Type -AssemblyName PresentationFramework
    [void][System.Windows.MessageBox]::Show($text, 'Jarvis')
  } catch {
    Write-Host $text
  }
}

if ($CrearAccesoDirecto) {
  $shell = New-Object -ComObject WScript.Shell
  $link = $shell.CreateShortcut((Join-Path ([Environment]::GetFolderPath('Desktop')) 'Jarvis.lnk'))
  $link.TargetPath = Join-Path $Root 'Jarvis.bat'
  $link.WorkingDirectory = $Root
  $link.IconLocation = Join-Path $Root 'jarvis.ico'
  $link.WindowStyle = 7  # minimizado: la consola del .bat no se ve
  $link.Description = 'Jarvis, la asistente de Tomás'
  $link.Save()
  Show-Message 'Listo: tienes un acceso directo "Jarvis" en el escritorio.'
  exit 0
}

$candidates = @(
  "$env:ProgramFiles\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Google\Chrome\Application\chrome.exe",
  "$env:LOCALAPPDATA\Google\Chrome\Application\chrome.exe",
  "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe",
  "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe"
)
$browser = $candidates | Where-Object { $_ -and (Test-Path -LiteralPath $_) } | Select-Object -First 1
if (-not $browser -and -not $env:JARVIS_SIN_NAVEGADOR) {
  Show-Message 'No encuentro Google Chrome ni Microsoft Edge. Instala uno de los dos y vuelve a abrir Jarvis.'
  exit 1
}
$browserArgs = @(
  "--app=$Url",
  "--user-data-dir=`"$ProfileDir`"",
  '--window-size=1200,820',
  '--no-first-run',
  '--no-default-browser-check'
)

function Open-Window {
  if ($browser) { Start-Process -FilePath $browser -ArgumentList $browserArgs }
}

# ¿Sigue abierta la ventana de Jarvis? (procesos del navegador con nuestro perfil)
function Test-WindowOpen {
  if (-not $OnWindows) { return $true }
  $procs = Get-CimInstance Win32_Process -Filter "Name='chrome.exe' OR Name='msedge.exe'" -ErrorAction SilentlyContinue
  return [bool]($procs | Where-Object { $_.CommandLine -like '*JarvisTomas*' } | Select-Object -First 1)
}

$listener = New-Object System.Net.HttpListener
$listener.Prefixes.Add($Url)
try {
  $listener.Start()
} catch {
  # El puerto ya está en uso: lo normal es que Jarvis ya esté abierto. Abrimos otra ventana.
  Open-Window
  exit 0
}

$mime = @{
  '.html' = 'text/html; charset=utf-8'; '.js' = 'text/javascript; charset=utf-8'
  '.css' = 'text/css; charset=utf-8'; '.json' = 'application/json'; '.md' = 'text/plain; charset=utf-8'
  '.png' = 'image/png'; '.jpg' = 'image/jpeg'; '.jpeg' = 'image/jpeg'; '.webp' = 'image/webp'
  '.gif' = 'image/gif'; '.svg' = 'image/svg+xml'; '.ico' = 'image/x-icon'
}
$rootFull = [System.IO.Path]::GetFullPath($Root).TrimEnd('\', '/')
$sep = [System.IO.Path]::DirectorySeparatorChar

function Send-File($ctx) {
  $res = $ctx.Response
  try {
    $rel = [Uri]::UnescapeDataString($ctx.Request.Url.AbsolutePath).TrimStart('/')
    if ($rel -eq '') { $rel = 'index.html' }
    $full = [System.IO.Path]::GetFullPath((Join-Path $rootFull $rel))
    if ($ctx.Request.HttpMethod -ne 'GET' -or -not $full.StartsWith($rootFull + $sep) -or -not (Test-Path -LiteralPath $full -PathType Leaf)) {
      $res.StatusCode = 404
      $bytes = [System.Text.Encoding]::UTF8.GetBytes('No encontrado')
    } else {
      $ext = [System.IO.Path]::GetExtension($full).ToLowerInvariant()
      $res.ContentType = if ($mime.ContainsKey($ext)) { $mime[$ext] } else { 'application/octet-stream' }
      $bytes = [System.IO.File]::ReadAllBytes($full)
    }
    $res.Headers['Cache-Control'] = 'no-cache'
    $res.ContentLength64 = $bytes.Length
    $res.OutputStream.Write($bytes, 0, $bytes.Length)
  } catch {
    try { $res.StatusCode = 500 } catch {}
  } finally {
    $res.Close()
  }
}

Open-Window
$graceUntil = (Get-Date).AddSeconds(20)   # margen para que el navegador arranque
$lastCheck = Get-Date
$pending = $listener.GetContextAsync()
try {
  while ($true) {
    if ($pending.Wait(500)) {
      $ctx = $pending.Result
      $pending = $listener.GetContextAsync()
      Send-File $ctx
    }
    if (((Get-Date) - $lastCheck).TotalSeconds -ge 3) {
      $lastCheck = Get-Date
      if ((Get-Date) -gt $graceUntil -and -not (Test-WindowOpen)) { break }
    }
  }
} finally {
  $listener.Stop()
  $listener.Close()
}
