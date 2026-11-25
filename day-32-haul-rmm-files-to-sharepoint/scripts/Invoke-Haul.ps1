<#
.SYNOPSIS
  HAUL – Hash-checked, App-only, Unattended, Logged.
  Uploads recently changed files from one local folder (top level only) to a SharePoint Online library,
  unattended, from many PCs. Designed to run as SYSTEM from an RMM tool. Windows PowerShell 5.1 compatible.

.DESCRIPTION
  - Auth: Microsoft Entra app registration + certificate (no user name or password in the script).
    The token request uses a PS256-signed client assertion, as described on Microsoft Learn
    ("Microsoft identity platform application authentication certificate credentials").
  - Least privilege: give the app Lists.SelectedOperations.Selected (or Sites.Selected) and grant it
    the "write" role on the one drop-zone library only. See docs/grant-permission.http.
  - Idempotent: a local state file remembers the SHA-256 of every file already uploaded, so unchanged
    files are skipped on the next run.
  - Files go to <TargetFolder>/<COMPUTERNAME>/<file name>, so two PCs never overwrite each other.

.EXIT CODES (for the RMM dashboard)
  0 = success (including "nothing to upload")   1 = some files failed (others uploaded)
  2 = authentication failed                     3 = configuration or certificate problem
  4 = no network / Microsoft 365 unreachable    5 = another HAUL run is still in progress

.EXAMPLE
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Invoke-Haul.ps1 -ConfigPath C:\ProgramData\Haul\haul.config.json
  powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\Invoke-Haul.ps1 -ConfigPath .\haul.config.json -DryRun
#>
[CmdletBinding()]
param(
    [Parameter(Mandatory)][string]$ConfigPath,
    [switch]$DryRun
)

$ErrorActionPreference = 'Stop'
[Net.ServicePointManager]::SecurityProtocol = [Net.SecurityProtocolType]::Tls12   # needed on Server 2016 / PS 5.1

# ---------------------------------------------------------------- logging
$script:LogFile = $null
function Write-Log([string]$Level, [string]$Message) {
    $line = '{0:yyyy-MM-ddTHH:mm:ssZ} [{1}] {2}' -f (Get-Date).ToUniversalTime(), $Level, $Message
    Write-Output $line                                         # shows in the RMM script output
    if ($script:LogFile) { Add-Content -Path $script:LogFile -Value $line -Encoding UTF8 }
}

# ---------------------------------------------------------------- config
try {
    $cfg = Get-Content -Raw -Path $ConfigPath | ConvertFrom-Json
    foreach ($k in 'TenantId','ClientId','CertThumbprint','DriveId','TargetFolder','SourcePath','StatePath','LogPath') {
        if (-not $cfg.$k) { throw "Missing setting '$k' in $ConfigPath" }
    }
    $maxAgeDays = if ($cfg.MaxAgeDays) { [int]$cfg.MaxAgeDays } else { 3 }
    New-Item -ItemType Directory -Force -Path (Split-Path $cfg.LogPath), (Split-Path $cfg.StatePath) | Out-Null
    $script:LogFile = $cfg.LogPath
} catch { Write-Output "CONFIG ERROR: $($_.Exception.Message)"; exit 3 }

# Only one run at a time per machine (RMM schedules can overlap on slow links)
$mutex = New-Object System.Threading.Mutex($false, 'Global\HaulUpload')
if (-not $mutex.WaitOne(0)) { Write-Log 'WARN' 'Another HAUL run is in progress. Exiting.'; exit 5 }

try {
    Write-Log 'INFO' "HAUL start on $env:COMPUTERNAME (DryRun=$DryRun)"

    # ------------------------------------------------------------ pick files (top level only, last N days)
    if (-not (Test-Path -LiteralPath $cfg.SourcePath)) { Write-Log 'INFO' "Source folder not found: $($cfg.SourcePath). Nothing to do."; exit 0 }
    $cutoff = (Get-Date).AddDays(-$maxAgeDays)
    $files  = @(Get-ChildItem -LiteralPath $cfg.SourcePath -File | Where-Object { $_.LastWriteTime -ge $cutoff })
    Write-Log 'INFO' "$($files.Count) file(s) changed in the last $maxAgeDays day(s)"

    # ------------------------------------------------------------ state (what we already uploaded)
    $state = @{}
    if (Test-Path -LiteralPath $cfg.StatePath) {
        (Get-Content -Raw -LiteralPath $cfg.StatePath | ConvertFrom-Json).PSObject.Properties |
            ForEach-Object { $state[$_.Name] = $_.Value }
    }

    function Read-SharedBytes([string]$Path) {
        # FileShare.ReadWrite lets us read files another program still has open for writing.
        $fs = [IO.File]::Open($Path, 'Open', 'Read', 'ReadWrite')
        try { $ms = New-Object IO.MemoryStream; $fs.CopyTo($ms); return ,$ms.ToArray() } finally { $fs.Dispose() }
    }
    function Get-Sha256([byte[]]$Bytes) {
        $h = [Security.Cryptography.SHA256]::Create()
        try { return ([BitConverter]::ToString($h.ComputeHash($Bytes))).Replace('-', '') } finally { $h.Dispose() }
    }

    $todo = @()
    foreach ($f in $files) {
        try { $bytes = Read-SharedBytes $f.FullName }
        catch { Write-Log 'WARN' "LOCKED, will retry next run: $($f.Name) ($($_.Exception.Message))"; $script:hadFailure = $true; continue }
        $hash = Get-Sha256 $bytes
        if ($state[$f.FullName] -eq $hash) { Write-Log 'INFO' "UNCHANGED, skipped: $($f.Name)"; continue }
        $todo += [pscustomobject]@{ File = $f; Bytes = $bytes; Hash = $hash }
    }
    if ($todo.Count -eq 0) { Write-Log 'INFO' 'Nothing new to upload.'; if ($script:hadFailure) { exit 1 } else { exit 0 } }
    if ($DryRun) { $todo | ForEach-Object { Write-Log 'INFO' "DRYRUN would upload: $($_.File.Name) ($($_.Bytes.Length) bytes)" }; exit 0 }

    # ------------------------------------------------------------ token (certificate, no password)
    function ConvertTo-B64Url([byte[]]$b) { [Convert]::ToBase64String($b).TrimEnd('=').Replace('+','-').Replace('/','_') }
    function Get-GraphToken {
        $cert = Get-Item -LiteralPath "Cert:\LocalMachine\My\$($cfg.CertThumbprint)" -ErrorAction SilentlyContinue
        if (-not $cert -or -not $cert.HasPrivateKey) { throw [System.Configuration.ConfigurationErrorsException]::new('Certificate not found in LocalMachine\My or has no private key') }
        if ($cert.NotAfter -lt (Get-Date).AddDays(30)) { Write-Log 'WARN' "Certificate expires on $($cert.NotAfter.ToString('yyyy-MM-dd')). Rotate it." }
        $sha = [Security.Cryptography.SHA256]::Create()
        $hdr = @{ alg = 'PS256'; typ = 'JWT'; 'x5t#S256' = (ConvertTo-B64Url $sha.ComputeHash($cert.RawData)) }
        $now = [int][double]::Parse((Get-Date -UFormat %s))
        $aud = "https://login.microsoftonline.com/$($cfg.TenantId)/oauth2/v2.0/token"
        $pay = @{ aud = $aud; iss = $cfg.ClientId; sub = $cfg.ClientId; jti = [guid]::NewGuid().ToString(); nbf = $now; iat = $now; exp = $now + 600 }
        $unsigned = (ConvertTo-B64Url ([Text.Encoding]::UTF8.GetBytes(($hdr | ConvertTo-Json -Compress)))) + '.' +
                    (ConvertTo-B64Url ([Text.Encoding]::UTF8.GetBytes(($pay | ConvertTo-Json -Compress))))
        $rsa = [Security.Cryptography.X509Certificates.RSACertificateExtensions]::GetRSAPrivateKey($cert)  # needs a CNG (KSP) key for PSS
        $sig = $rsa.SignData([Text.Encoding]::UTF8.GetBytes($unsigned), [Security.Cryptography.HashAlgorithmName]::SHA256, [Security.Cryptography.RSASignaturePadding]::Pss)
        $body = @{
            client_id = $cfg.ClientId; scope = 'https://graph.microsoft.com/.default'; grant_type = 'client_credentials'
            client_assertion_type = 'urn:ietf:params:oauth:client-assertion-type:jwt-bearer'
            client_assertion = "$unsigned.$(ConvertTo-B64Url $sig)"
        }
        return (Invoke-RestMethod -Method Post -Uri $aud -Body $body -ContentType 'application/x-www-form-urlencoded').access_token
    }

    try { $token = Get-GraphToken }
    catch [System.Configuration.ConfigurationErrorsException] { Write-Log 'ERROR' $_.Exception.Message; exit 3 }
    catch [System.Net.WebException] {
        if (-not $_.Exception.Response) { Write-Log 'ERROR' "No network: $($_.Exception.Message)"; exit 4 }
        Write-Log 'ERROR' "Authentication failed: $($_.Exception.Message)"; exit 2
    }
    catch { Write-Log 'ERROR' "Authentication failed: $($_.Exception.Message)"; exit 2 }
    $auth = @{ Authorization = "Bearer $token" }

    # ------------------------------------------------------------ Graph helper with retry
    function Invoke-Graph([string]$Method, [string]$Uri, $Body, [string]$ContentType = 'application/json', [hashtable]$Headers = $auth) {
        for ($i = 1; $i -le 5; $i++) {
            try { return Invoke-RestMethod -Method $Method -Uri $Uri -Headers $Headers -Body $Body -ContentType $ContentType }
            catch [System.Net.WebException] {
                $resp = $_.Exception.Response
                $code = if ($resp) { [int]$resp.StatusCode } else { 0 }
                if ($code -in 429, 500, 502, 503, 504 -or $code -eq 0) {
                    $wait = if ($resp -and $resp.Headers['Retry-After']) { [int]$resp.Headers['Retry-After'] } else { [math]::Pow(2, $i) * 2 }
                    Write-Log 'WARN' "HTTP $code on attempt $i, waiting $wait s"; Start-Sleep -Seconds $wait; continue
                }
                throw
            }
        }
        throw "Gave up after 5 attempts: $Method $Uri"
    }

    $g = 'https://graph.microsoft.com/v1.0'
    $enc = { param($p) ($p -split '/' | ForEach-Object { [Uri]::EscapeDataString($_) }) -join '/' }
    $pcFolder = "$($cfg.TargetFolder)/$env:COMPUTERNAME"

    # Make sure <TargetFolder>/<COMPUTERNAME> exists (the TargetFolder itself is created once during setup)
    try { Invoke-Graph GET "$g/drives/$($cfg.DriveId)/root:/$(& $enc $pcFolder)" | Out-Null }
    catch {
        $newFolder = @{ name = $env:COMPUTERNAME; folder = @{}; '@microsoft.graph.conflictBehavior' = 'fail' } | ConvertTo-Json
        try { Invoke-Graph POST "$g/drives/$($cfg.DriveId)/root:/$(& $enc $cfg.TargetFolder):/children" $newFolder | Out-Null }
        catch { if ("$_" -notmatch '409') { throw } }   # 409 = someone created it meanwhile: fine
    }

    # ------------------------------------------------------------ upload
    $chunk = 320KB * 16   # 5 MiB, a multiple of 320 KiB as Graph requires
    foreach ($t in $todo) {
        $name = $t.File.Name
        try {
            $itemPath = & $enc "$pcFolder/$name"
            if ($t.Bytes.Length -le 10MB) {
                Invoke-Graph PUT "$g/drives/$($cfg.DriveId)/root:/$($itemPath):/content" $t.Bytes 'application/octet-stream' | Out-Null
            } else {
                $sess = Invoke-Graph POST "$g/drives/$($cfg.DriveId)/root:/$($itemPath):/createUploadSession" (@{ item = @{ '@microsoft.graph.conflictBehavior' = 'replace' } } | ConvertTo-Json)
                for ($o = 0; $o -lt $t.Bytes.Length; $o += $chunk) {
                    $len = [math]::Min($chunk, $t.Bytes.Length - $o)
                    $part = New-Object byte[] $len; [Array]::Copy($t.Bytes, $o, $part, 0, $len)
                    # The uploadUrl is pre-authenticated: don't send the Authorization header to it
                    Invoke-Graph PUT $sess.uploadUrl $part 'application/octet-stream' @{ 'Content-Range' = "bytes $o-$($o + $len - 1)/$($t.Bytes.Length)" } | Out-Null
                }
            }
            $state[$t.File.FullName] = $t.Hash
            Write-Log 'INFO' "UPLOADED: $name -> $pcFolder ($($t.Bytes.Length) bytes)"
        } catch {
            $script:hadFailure = $true
            Write-Log 'ERROR' "FAILED: $name ($($_.Exception.Message))"
        }
    }

    # ------------------------------------------------------------ save state atomically
    $tmp = "$($cfg.StatePath).tmp"
    ($state | ConvertTo-Json) | Set-Content -LiteralPath $tmp -Encoding UTF8
    Move-Item -LiteralPath $tmp -Destination $cfg.StatePath -Force

    if ($script:hadFailure) { Write-Log 'WARN' 'Finished with failures.'; exit 1 }
    Write-Log 'INFO' 'Finished OK.'; exit 0
}
finally { $mutex.ReleaseMutex(); $mutex.Dispose() }
