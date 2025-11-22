$owner = 'ravisasu'
$repo = 'simple-cms-prototype'
$branch = 'demo/guided-2025-11-22'
$url = "https://api.github.com/repos/$owner/$repo/actions/runs?branch=$branch&per_page=10"
try {
    $resp = Invoke-RestMethod -Headers @{ 'User-Agent' = 'github-actions-monitor' } -Uri $url -UseBasicParsing -ErrorAction Stop
    if ($null -eq $resp.workflow_runs -or $resp.workflow_runs.Count -eq 0) {
        Write-Output "No workflow runs found for branch $branch"
        exit 0
    }
    foreach ($r in $resp.workflow_runs) {
        $name = $r.name
        $id = $r.id
        $status = $r.status
        $conclusion = $r.conclusion
        $html = $r.html_url
        Write-Output "Name: $name  ID: $id  Status: $status  Conclusion: $conclusion  URL: $html"
    }
} catch {
    Write-Output "Failed to query GitHub Actions API: $_"
    exit 2
}
