# PowerShell voiceover generator using System.Speech.Synthesis
Add-Type -AssemblyName System.Speech
$synth = New-Object System.Speech.Synthesis.SpeechSynthesizer

# Select an installed voice
$voices = $synth.GetInstalledVoices()
Write-Host "Available voices:"
foreach ($v in $voices) {
    Write-Host " - $($v.VoiceInfo.Name) ($($v.VoiceInfo.Culture))"
}

# Configure output audio settings
$synth.Rate = 0  # 0 is normal speed, 1 is slightly faster
$synth.Volume = 100

$testPath = "E:\week 3\video_production\assets\audio\test_voice.wav"
$synth.SetOutputToWaveFile($testPath)
$synth.Speak("Testing audio synthesis for SlothChef demo video.")
$synth.SetOutputToNull()
Write-Host "Audio test file written to $testPath"
