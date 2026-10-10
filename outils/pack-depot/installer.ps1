param([Parameter(Mandatory=$true)][string]$Depot)
$ErrorActionPreference = "Stop"
$Pack = $PSScriptRoot
$Branche = "ajout-catalogue-agents"

if (-not (Test-Path (Join-Path $Depot ".git"))) { throw "Pas de dépôt git dans : $Depot" }
Set-Location $Depot

if (git status --porcelain) { throw "Le dépôt a des modifications non commitées. Commite-les ou mets-les de côté (git stash), puis relance." }
if (git branch --list $Branche) { throw "La branche $Branche existe déjà." }

git checkout -b $Branche
New-Item -ItemType Directory -Force -Path ".claude\skills", ".claude\agents", "outils" | Out-Null
Copy-Item -Recurse -Force (Join-Path $Pack ".claude\skills\*") ".claude\skills\"
Copy-Item -Recurse -Force (Join-Path $Pack ".claude\agents\*") ".claude\agents\"
Copy-Item -Recurse -Force (Join-Path $Pack "outils\catalogue") "outils\"
Copy-Item -Force (Join-Path $Pack "LISEZMOI.md") "outils\catalogue\LISEZMOI-pack.md"

git add .claude outils
git commit -m "Ajoute le catalogue d'agents et de skills (.claude/ et outils/catalogue)"
Write-Host ""
Write-Host "Terminé sur la branche $Branche. Aucun push effectué." -ForegroundColor Green
git log --stat -1 | Select-Object -First 8
