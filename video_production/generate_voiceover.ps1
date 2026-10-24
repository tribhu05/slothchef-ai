Add-Type -AssemblyName System.Speech

$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer
try {
    $synth.SelectVoice("Microsoft David Desktop")
} catch {
    Write-Host "David Desktop not found, using default voice."
}
$synth.Rate = 1
$synth.Volume = 100

$jsonPath = Join-Path $PSScriptRoot "voice_lines.json"
$outputDir = Join-Path $PSScriptRoot "assets\audio"

$content = [System.IO.File]::ReadAllText($jsonPath, [System.Text.Encoding]::UTF8)
$scenes = $content | ConvertFrom-Json

foreach ($s in $scenes) {
    $filePath = Join-Path $outputDir "$($s.id)_voice.wav"
    Write-Host "Synthesizing $($s.id)..."
    $synth.SetOutputToWaveFile($filePath)
    $synth.Speak($s.text)
    $synth.SetOutputToNull()
    Write-Host "Generated $filePath"
}

Write-Host "All 7 scene voiceovers synthesized successfully at Rate 1!"
