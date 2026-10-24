<#
.SYNOPSIS
    SlothChef AI - Automated Video Production Build Script
.DESCRIPTION
    One-click reproduction script to synthesize voiceover audio, generate 
    high-resolution 1080p visual assets, mix the master audio track, and 
    render the final 1080p 30fps demo video (slothchef-demo.mp4) for 
    DEV Hacktoberfest 2026: Week 3 ("Slow and Steady").
.EXAMPLE
    .\render.ps1
#>

Write-Host "==========================================================" -ForegroundColor Cyan
Write-Host "   SlothChef AI -- Automated Video Production Pipeline    " -ForegroundColor Yellow
Write-Host "   DEV Hacktoberfest 2026: Week 3 (Slow and Steady)       " -ForegroundColor Green
Write-Host "==========================================================" -ForegroundColor Cyan

$scriptDir = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $scriptDir

# 1. Verify Python
Write-Host "`n[Step 1/5] Verifying Python Environment..." -ForegroundColor White
$pythonCmd = (Get-Command python -ErrorAction SilentlyContinue).Source
if (-not $pythonCmd) {
    Write-Error "Python not found in PATH. Please install Python 3.10+."
    exit 1
}
Write-Host "Found Python: $pythonCmd" -ForegroundColor Gray

# 2. Generate Sound Effects & Ambient Track
Write-Host "`n[Step 2/5] Generating Ambient Track and Sound Effects..." -ForegroundColor White
python "$scriptDir\generate_sound_effects.py"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate sound effects."
    exit $LASTEXITCODE
}

# 3. Generate Scene Voiceover Tracks
Write-Host "`n[Step 3/5] Synthesizing Voiceover Audio (System.Speech)..." -ForegroundColor White
powershell -ExecutionPolicy Bypass -File "$scriptDir\generate_voiceover.ps1"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to synthesize voiceover."
    exit $LASTEXITCODE
}

# 4. Generate Visual Cards and Thumbnail
Write-Host "`n[Step 4/5] Rendering High-Resolution Graphic Cards..." -ForegroundColor White
python "$scriptDir\generate_cards.py"
if ($LASTEXITCODE -ne 0) {
    Write-Error "Failed to generate graphic cards."
    exit $LASTEXITCODE
}

# 5. Build Master Audio and Final Video Render
Write-Host "`n[Step 5/5] Mixing Audio and Assembling Final 1080p Video..." -ForegroundColor White
python "$scriptDir\build_master_audio.py"
python "$scriptDir\build_video.py"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Video rendering failed."
    exit $LASTEXITCODE
}

$outputFile = "$scriptDir\slothchef-demo.mp4"
if (Test-Path $outputFile) {
    $bytes = (Get-Item $outputFile).Length
    $sizeMB = [math]::Round($bytes / 1MB, 2)
    Write-Host "`n==========================================================" -ForegroundColor Green
    Write-Host "   RENDER COMPLETE: slothchef-demo.mp4                    " -ForegroundColor Green
    Write-Host ("   Location: {0} ({1} MB)" -f $outputFile, $sizeMB) -ForegroundColor Cyan
    Write-Host "   Runtime:  2 minutes 50 seconds (170.0s, 30fps 1080p)   " -ForegroundColor Yellow
    Write-Host "==========================================================" -ForegroundColor Green
} else {
    Write-Error "Output file was not generated."
    exit 1
}
