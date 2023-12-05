$script = @'
# Function to test the installation of a program
function Test-ProgramInstallation {
    param (
        [string]$programName
    )

    # Check if the specified program exists
    $command = Get-Command $programName -ErrorAction SilentlyContinue

    # Return true if the program is found, otherwise false
    if ($command) {
        return $true
    } 

    return $false
}

# Array containing possible Python commands
$pythonCommands = @("py", "python", "python3", "py3")
$pythonCommand = $null

# Iterate through the possible Python commands to find the installed one
foreach ($command in $pythonCommands) {
    if (Test-ProgramInstallation $command) {
        $pythonCommand = $command
        break
    }
}

# If a Python command is found, install Python modules
if ($null -ne $pythonCommand) {
    # Check if the .env directory exists
    $envDir = Join-Path -Path $PWD.Path -ChildPath ".env"

    if (Test-Path $envDir) {
        Write-Host "[+] Starting virtual environment.."
        & $pythonCommand -m venv $envDir
        $venvScript = Join-Path -Path $envDir -ChildPath "Scripts\Activate.ps1"
        . $venvScript
    }

    Write-Host "[+] Installing Python modules.."
    & $pythonCommand -m pip install -r requirements.txt
} 

# Check for npm installation and install NodeJS modules if npm is found
if (Test-ProgramInstallation "npm") {
    Write-Host "[+] Installing NodeJS modules.."
    npm install mineflayer minecraft-colors proxy-agent readline socks
}
'@
# Base64
$encodedScript = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($script))
$encodedScript
