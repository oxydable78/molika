
#Install-Module -Name Posh-SSH
Import-Module Posh-SSH

####
$serveur = "192.168.0.5"
$user = "root"
$port = "22"
$path_python = "/root/.local/pipx/venvs/wakeonlan/bin/python"
####

do {
$value = Read-Host "user"

ssh $user@$serveur -p $port " '$path_python' /molika/Molika.py '$value'" 

}while ($true)