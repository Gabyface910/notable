# install.ps1
param(
    [string]$InstallPath = "$env:USERPROFILE\notable"
)

# Clone or update the repository
if (Test-Path $InstallPath) {
    Write-Host "Updating notable..."
    cd $InstallPath
    git pull
} else {
    Write-Host "Cloning notable..."
    git clone https://github.com/Gabyface910/notable $InstallPath
}

# Add to PATH if not already there
$PathVar = [Environment]::GetEnvironmentVariable("PATH", "User")
if ($PathVar -notlike "*$InstallPath*") {
    [Environment]::SetEnvironmentVariable("PATH", "$PathVar;$InstallPath", "User")
    Write-Host "Added to PATH"
}

Write-Host "Installation complete! Restart your terminal to use 'notable'"
