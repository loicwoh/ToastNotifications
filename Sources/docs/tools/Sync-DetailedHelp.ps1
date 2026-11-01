param(
    [string]$Manifest = '_review/docsify-preview/ToastNotifications/api-links.json',
    [string]$BaseUrl = 'https://loicwoh.github.io/ToastNotifications/',
    [switch]$Apply
)
$ErrorActionPreference = 'Stop'
$repoRoot = [IO.Path]::GetFullPath((Join-Path $PSScriptRoot '../../..'))
$entries = Get-Content -LiteralPath $Manifest -Raw | ConvertFrom-Json
$backupRoot = Join-Path $repoRoot ('_review/detailed-help-backup/' + (Get-Date -Format 'yyyyMMdd-HHmmss'))
# Use IDispatch reflection: PowerShell's automatic COM type information lookup
# fails on this LabVIEW installation, while InvokeMember works correctly.
$comType = [type]::GetTypeFromProgID('LabVIEW.Application')
$lvApp = [Activator]::CreateInstance($comType)
function Read-Property($vi, [string]$name) {
    $comType.InvokeMember($name, [Reflection.BindingFlags]::GetProperty, $null, $vi, @())
}
function Write-Property($vi, [string]$name, $value) {
    $comType.InvokeMember($name, [Reflection.BindingFlags]::SetProperty, $null, $vi, @($value)) | Out-Null
}
try {
    foreach ($entry in $entries) {
        $path = [IO.Path]::GetFullPath((Join-Path $repoRoot $entry.source))
        if (-not $path.StartsWith((Join-Path $repoRoot 'Sources') + [IO.Path]::DirectorySeparatorChar) -or [IO.Path]::GetExtension($path) -ne '.vi') {
            throw "Invalid VI path: $path"
        }
        $url = $BaseUrl.TrimEnd('/') + '/' + $entry.route
        $vi = $comType.InvokeMember('GetVIReference', [Reflection.BindingFlags]::InvokeMethod, $null, $lvApp, @($path, '', [int]0))
        try {
            if ((Read-Property $vi 'FPModificationBitSet') -ne 0 -or (Read-Property $vi 'BDModificationBitSet') -ne 0) {
                throw "VI has unsaved changes: $path"
            }
            $current = Read-Property $vi 'HelpDocumentUrl'
            $online = Read-Property $vi 'HelpUseOnline'
            if ($Apply -and ($current -ne $url -or -not $online)) {
                $backup = Join-Path $backupRoot $entry.source
                New-Item -ItemType Directory -Path (Split-Path $backup) -Force | Out-Null
                Copy-Item -LiteralPath $path -Destination $backup
                Write-Property $vi 'HelpDocumentUrl' $url
                Write-Property $vi 'HelpUseOnline' $true
                $comType.InvokeMember('SaveInstrument', [Reflection.BindingFlags]::InvokeMethod, $null, $vi, @()) | Out-Null
                if ((Read-Property $vi 'HelpDocumentUrl') -ne $url -or -not (Read-Property $vi 'HelpUseOnline')) { throw "Help URL verification failed: $path" }
            }
            [pscustomobject]@{ VI=$entry.source; URL=$url; Applied=[bool]$Apply }
        } finally { [Runtime.InteropServices.Marshal]::FinalReleaseComObject($vi) | Out-Null }
    }
} finally { [Runtime.InteropServices.Marshal]::FinalReleaseComObject($lvApp) | Out-Null }
if ($Apply) { Write-Output "Backup: $backupRoot" }
