#################################################
#init variables
$directory = "C:\Users\omar_\Documents\Elmah\*.xml"
$directory = "\\10.104.5.45\Elmah.Errors\*.xml"
$retentionDate = [datetime]"03/27/2018" #[datetime]::ParseExact("01/02/03", "dd/MM/yy", $null)
$username = "Guillermo"
#################################################
# nothing below here needs to change
"Searching entries for " + $username + " on or after "+$retentionDate.ToString("MMM dd, yyyy")+"..."

Get-ChildItem $directory |? {($_.PSIsContainer -eq $false) -and ($_.LastWriteTime -gt $retentionDate)} | select-string $username
# Get-ChildItem -Recurse -Include *.log | select-string ERROR
