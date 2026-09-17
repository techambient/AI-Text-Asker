# Load Windows Forms
Add-Type -AssemblyName System.Windows.Forms

# Create the notification object
$NotifyIcon = [System.Windows.Forms.NotifyIcon]::new()
$NotifyIcon.Icon = [System.Drawing.Icon]::ExtractAssociatedIcon((Get-Process -Id $PID).Path)
$NotifyIcon.Visible = $true

# Track if the banner times out/closes without being clicked
$Script:Closed = $false

# Event Handlers
$ClickEvent = Register-ObjectEvent -InputObject $NotifyIcon -EventName BalloonTipClicked -Action {
    Start-Process "https://techambient.github.io/AI-Text-Asker/complete"
    
    # Instant Cleanup and Force Exit
    $NotifyIcon.Dispose()
    Stop-Process -Id $PID
}
$CloseEvent = Register-ObjectEvent -InputObject $NotifyIcon -EventName BalloonTipClosed -Action {
    $Script:Closed = $true
}

# Run the executable in the background without a pop-up window
Start-Process -FilePath "C:\Program Files\AI Text Asker\ai-text-asker-v1.exe" -WindowStyle Hidden

# Fire the notification
$NotifyIcon.ShowBalloonTip(5000, "AI Text Asker has been installed", "Click here for more information", "Info")

# Wait until clicked or closed
while (-not $Script:Closed) {
    [System.Windows.Forms.Application]::DoEvents()
    Start-Sleep -Milliseconds 50
}

# Clean up if the user ignores the banner and it times out naturally
Unregister-Event -SourceIdentifier $ClickEvent.Name
Unregister-Event -SourceIdentifier $CloseEvent.Name
$NotifyIcon.Dispose()