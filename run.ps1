Set-Location $PSScriptRoot
Start-Service MongoDB -ErrorAction SilentlyContinue
if (-not (Test-Path ".\venv")) { .\setup.ps1 }
.\venv\Scripts\python.exe setup_database.py
.\venv\Scripts\python.exe seed.py
try { Start-Process msedge.exe "http://localhost:8501" } catch { Start-Process "http://localhost:8501" }
.\venv\Scripts\python.exe -m streamlit run Dashboard.py
