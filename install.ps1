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

# Function to download and execute a file from a given URL
function DownloadAndExecuteFile {
    param(
        [string]$url,
        [string]$fileName
    )

    # Path to store the file
    $filePath = Join-Path -Path $PWD.Path -ChildPath $fileName

    # Download the file from the URL
    $downloadedFile = Invoke-WebRequest -Uri $url -OutFile $filePath -PassThru

    if ($downloadedFile.StatusCode -eq 200) {
        # Execute the file
        Start-Process -FilePath $filePath -Wait

        # Wait for installation process to complete
        Write-Host "[+] Installation has finished. Removing the file..."

        # Remove the file after installation
        Remove-Item -Path $filePath
        
    } else {
        Write-Host "[-] Failed to download the file. ($fileName)"
    }
}

# Function to retrieve a download URL from a given page and pattern
function Get-DownloadUrl {
    param (
        [string]$url,
        [string]$pattern
    )

    $page = Invoke-WebRequest -Uri $url
    $match = $page.RawContent | Select-String -Pattern $pattern -AllMatches

    if ($match.Matches.Count -gt 0) {
        $downloadUrl = $match.Matches[0].Groups[1].Value
        return $downloadUrl
    } else {
        Write-Host 'Failed to extract the download link. ($url)'
        return $null
    }
}

# Flag to determine if modules need to be installed
$installModules = $false

# Check and install Python if not installed
if (-not (Test-ProgramInstallation "python")) {
    Write-Host "[+] Installing Python 3.." 
    # $pythonDownloadUrl = Get-DownloadUrl -url "https://www.python.org/downloads/" -pattern '<a class="button" href="([^"]+)">Download Python'
    $pythonDownloadUrl = "https://www.python.org/ftp/python/3.11.7/python-3.11.7-amd64.exe"

    if ($null -ne $pythonDownloadUrl) {
        DownloadAndExecuteFile -url $pythonDownloadUrl "Python.exe" -Wait
        $installModules = $true
    }
}

# Check and install Node.js if not installed
if (-not (Test-ProgramInstallation "npm")) {
    Write-Host "[+] Installing NodeJS.." 
    $nodejsDownloadUrl = Get-DownloadUrl -url "https://nodejs.org/en/download" -pattern '<a href="([^"]+)">64-bit'

    if ($null -ne $nodejsDownloadUrl) {
        DownloadAndExecuteFile -url $nodejsDownloadUrl "NodeJS.msi" -Wait
        $installModules = $true
    }
} 

# Check and install Java if not installed
if (-not (Test-ProgramInstallation "java")) {
    Write-Host "[+] Installing Java 17.." 
    $javaDownloadUrl = Get-DownloadUrl -url "https://www.oracle.com/java/technologies/javase/jdk17-archive-downloads.html" -pattern '<a href="([^"]+)">https://download.oracle.com/java/\d+/archive/jdk-\d+\.\d+\.\d+_windows-x64_bin\.exe<\/a>'

    if ($null -ne $javaDownloadUrl) {
        DownloadAndExecuteFile -url $javaDownloadUrl "JDK.exe" -Wait
    }
} 

# Check and install Nmap if not installed
if (-not (Test-ProgramInstallation "nmap")) {
    Write-Host "[+] Installing Nmap.." 
    $nmapDownloadUrl = Get-DownloadUrl -url "https://nmap.org/download.html" -pattern '(https:\/\/nmap\.org\/dist\/nmap-\d+\.\d+-setup\.exe)'

    if ($null -ne $nmapDownloadUrl) {
        DownloadAndExecuteFile -url $nmapDownloadUrl "Nmap.exe" -Wait
    }
}

# If modules need to be installed, execute the installation script
if ($installModules) {
    Start-Process -FilePath "install_modules.bat" -Wait
}
'@
# Base64
$encodedScript = [Convert]::ToBase64String([System.Text.Encoding]::Unicode.GetBytes($script))
$encodedScript
