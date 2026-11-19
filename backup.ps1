Set-Location $PSScriptRoot
.\venv\Scripts\python.exe export_db.py
$stamp = Get-Date -Format "yyyyMMdd_HHmm"
New-Item -ItemType Directory -Path "backups\$stamp" -Force | Out-Null
Copy-Item "database_export\*" "backups\$stamp"
Write-Host "Backup saved in backups\$stamp" -ForegroundColor Green
