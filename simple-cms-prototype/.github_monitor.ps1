$owner = 'ravisasu'
$repo = 'simple-cms-prototype'
$branch = 'demo/guided-2025-11-22'
$log = '.\github_actions_monitor.log'

function Get-Runs {
    $url = "https://api.github.com/repos/$owner/$repo/actions/runs?branch=$branch&per_page=10"
    try {
        $resp = Invoke-RestMethod -Headers @{ 'User-Agent' = 'github-actions-monitor' } -Uri $url -UseBasicParsing -ErrorAction Stop
        return $resp.workflow_runs
    } catch {
        Write-Output "Failed to fetch runs: $_"
        return @()
    }
}

# write header
"Monitoring GitHub Actions for $owner/$repo branch $branch" | Tee-Object -FilePath $log -Append

while ($true) {
    $runs = Get-Runs
    $time = Get-Date -Format o
    if ($runs.Count -eq 0) {
        "$time - no runs found or request failed" | Tee-Object -FilePath $log -Append
    } else {
        foreach ($r in $runs) {
            $line = "$time - [$($r.name)] #$($r.id) - status=$($r.status) conclusion=$($r.conclusion) url=$($r.html_url)"
            $line | Tee-Object -FilePath $log -Append
        }
    }
    Start-Sleep -Seconds 30
}
