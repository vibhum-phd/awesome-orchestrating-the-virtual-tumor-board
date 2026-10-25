<#
  kaggle_push.ps1  -  push the Lab 7 notebooks to Kaggle with the Kaggle CLI (written 25 Oct 2026)
  Lives in board-eval\notebooks\. Uses your own Kaggle CLI login (kaggle.json / access token); never reads the key.

  FIRST TIME (from the repo folder, e.g. the VS Code terminal):
      powershell -ExecutionPolicy Bypass -File .\board-eval\notebooks\kaggle_push.ps1 -DryRun   # show what it would push
      powershell -ExecutionPolicy Bypass -File .\board-eval\notebooks\kaggle_push.ps1 -Wait     # push all 3, run 01, wait, download 01's outputs
    -> 01 is pushed AND RUN (GPU T4 x2, internet on).
    -> 02 and 03 are pushed WITHOUT running (Kaggle "Quick Save"), so they exist on Kaggle but spend no GPU.
       Protocol: 02 runs only after 01's outputs are checked; 03 only after the baseline is validated.

  LATER:
      ... kaggle_push.ps1 -Action Run    -Notebook 02          # push + run 02 when it is its turn
      ... kaggle_push.ps1 -Action Status -Notebook 01          # is it still running?
      ... kaggle_push.ps1 -Action Fetch  -Notebook 01          # download its output zip + log to _kaggle_runs\01\
  Add -Username <kaggle-username> if the script cannot read it from "kaggle config view".
#>
[CmdletBinding()]
param(
    [ValidateSet('Setup', 'Run', 'Status', 'Fetch')] [string]$Action = 'Setup',
    [ValidateSet('01', '02', '03')] [string]$Notebook = '01',
    [string]$Username,
    [switch]$Wait,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
$Here = $PSScriptRoot
if (-not $Here) { $Here = (Get-Location).Path }
$RepoRoot = Split-Path -Parent (Split-Path -Parent $Here)
$RunsDir = Join-Path $RepoRoot '_kaggle_runs'
$Accelerator = 'NvidiaTeslaT4'          # Kaggle CLI name for "GPU T4 x2"
$Utf8NoBom = New-Object System.Text.UTF8Encoding $false

$Books = @{
    '01' = @{ File = '01_env_sanity_smoke_kaggle.ipynb'; Title = 'ATR Lab7 01 Env Sanity and Smoke Test'; Zip = 'env_and_pilot_outputs.zip' }
    '02' = @{ File = '02_baseline_kaggle.ipynb';         Title = 'ATR Lab7 02 Baseline CoT and SC';        Zip = 'baseline_outputs.zip' }
    '03' = @{ File = '03_main_grid_kaggle.ipynb';        Title = 'ATR Lab7 03 Main Comparison Grid';       Zip = 'main_grid_outputs.zip' }
}

function Stop-With([string]$msg) { Write-Host ''; Write-Host $msg -ForegroundColor Red; exit 1 }
function Step([string]$msg) { Write-Host ''; Write-Host "--- $msg" -ForegroundColor Cyan }
function Slug([string]$title) { return (($title.ToLowerInvariant() -replace '[^a-z0-9]+', '-').Trim('-')) }
function KernelId([string]$nb) { return "$Username/$(Slug $Books[$nb].Title)" }

# ------------------------------------------------------------------ preflight
if (-not (Get-Command kaggle -ErrorAction SilentlyContinue)) {
    Stop-With 'The kaggle command was not found. Install it with:  pip install -U kaggle   then run this again.'
}
if ($Action -in @('Setup', 'Run')) {
    $help = (& kaggle kernels push --help) | Out-String
    if ($help -notmatch '--no-run' -or $help -notmatch '--accelerator') {
        Stop-With 'Your kaggle CLI is too old (no --no-run / --accelerator). Update it:  pip install -U kaggle'
    }
}
if (-not $Username) {
    $cfg = (& kaggle config view) | Out-String
    $m = [regex]::Match($cfg, '-\s*username:\s*(\S+)')
    if ($m.Success -and $m.Groups[1].Value -ne 'None') { $Username = $m.Groups[1].Value }
}
if (-not $Username) { Stop-With 'Could not read your Kaggle username from "kaggle config view". Run again with -Username <your-kaggle-username>.' }
Write-Host "Kaggle user: $Username" -ForegroundColor Cyan
if ($DryRun) { Write-Host 'DRY RUN: nothing is pushed or downloaded.' -ForegroundColor Cyan }

# ------------------------------------------------------------------ actions
function Push-Notebook([string]$nb, [bool]$run) {
    $b = $Books[$nb]
    $src = Join-Path $Here $b.File
    if (-not (Test-Path -LiteralPath $src)) { Stop-With "Notebook not found: $src" }
    $id = KernelId $nb
    $meta = [ordered]@{
        id = $id; title = $b.Title; code_file = $b.File
        language = 'python'; kernel_type = 'notebook'; is_private = 'true'
        enable_gpu = 'true'; enable_tpu = 'false'; enable_internet = 'true'; machine_shape = $Accelerator
        dataset_sources = @(); competition_sources = @(); kernel_sources = @(); model_sources = @()
    }
    $mode = if ($run) { 'push + RUN (GPU T4 x2, internet on)' } else { 'push only, no run (Quick Save)' }
    Step "$nb  $id  -  $mode"
    if ($DryRun) { Write-Host ($meta | ConvertTo-Json); return }

    $tmp = Join-Path ([System.IO.Path]::GetTempPath()) ('kaggle_push_' + $nb + '_' + [guid]::NewGuid().ToString('N').Substring(0, 8))
    New-Item -ItemType Directory -Path $tmp | Out-Null
    try {
        Copy-Item -LiteralPath $src -Destination (Join-Path $tmp $b.File)
        # kaggle reads this as plain UTF-8: no byte-order mark
        [System.IO.File]::WriteAllText((Join-Path $tmp 'kernel-metadata.json'), ($meta | ConvertTo-Json), $Utf8NoBom)
        $kargs = @('kernels', 'push', '-p', $tmp, '--accelerator', $Accelerator)
        if (-not $run) { $kargs += '--no-run' }
        $out = (& kaggle @kargs) | Out-String
        Write-Host $out.Trim()
        # a run says "successfully pushed", --no-run says "successfully saved without running"
        if ($out -notmatch 'successfully (pushed|saved)') { Stop-With "Push of $nb failed (message above). Nothing else was pushed after it." }
    } finally {
        Remove-Item -LiteralPath $tmp -Recurse -Force -ErrorAction SilentlyContinue   # our own temp folder
    }
}

function Get-Status([string]$nb) {
    $out = (& kaggle kernels status (KernelId $nb)) | Out-String
    Write-Host $out.Trim()
    return $out
}

function Fetch-Output([string]$nb) {
    $dest = Join-Path $RunsDir $nb
    Step "Download outputs of $nb to _kaggle_runs\$nb\"
    if ($DryRun) { return }
    New-Item -ItemType Directory -Path $dest -Force | Out-Null
    # keep the downloads out of git
    $gi = Join-Path $RepoRoot '.gitignore'
    if ((Test-Path -LiteralPath $gi) -and -not ((Get-Content -LiteralPath $gi) -contains '_kaggle_runs/')) {
        [System.IO.File]::AppendAllText($gi, "`r`n# Kaggle run downloads (kaggle_push.ps1)`r`n_kaggle_runs/`r`n", $Utf8NoBom)
        Write-Host '  added _kaggle_runs/ to .gitignore'
    }
    $pattern = [regex]::Escape($Books[$nb].Zip) + '$'
    & kaggle kernels output (KernelId $nb) -p $dest --file-pattern $pattern -o
    Get-ChildItem -LiteralPath $dest | ForEach-Object { Write-Host ("  {0}  ({1:N0} bytes)" -f $_.Name, $_.Length) }
}

switch ($Action) {
    'Setup' {
        Push-Notebook '01' $true
        Push-Notebook '02' $false
        Push-Notebook '03' $false
        $Notebook = '01'
    }
    'Run'    { Push-Notebook $Notebook $true }
    'Status' { [void](Get-Status $Notebook) }
    'Fetch'  { Fetch-Output $Notebook }
}

if ($Wait -and $Action -in @('Setup', 'Run') -and -not $DryRun) {
    Step "Waiting for $Notebook to finish (checks every 60 s, gives up after 3 h; Ctrl+C is safe, the run continues on Kaggle)"
    $deadline = (Get-Date).AddHours(3)
    Start-Sleep -Seconds 30
    while ($true) {
        $s = Get-Status $Notebook
        if ($s -match '(?i)complete') { Fetch-Output $Notebook; break }
        if ($s -match '(?i)error|cancel') {
            Write-Host 'The run stopped with an error. Downloading the log so it can be checked.' -ForegroundColor Yellow
            Fetch-Output $Notebook; break
        }
        if ((Get-Date) -gt $deadline) { Write-Host 'Still running after 3 h. Check later with -Action Status, then -Action Fetch.'; break }
        Start-Sleep -Seconds 60
    }
}

Write-Host ''
Write-Host "Notebooks: https://www.kaggle.com/$Username/code" -ForegroundColor Green
