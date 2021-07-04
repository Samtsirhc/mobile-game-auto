Start-Process powershell -ArgumentList "-noexit", "-noprofile", "-command & cd ~\Desktop\mobile-game-auto\QBot\go-cqhttp
./go-cqhttp"
Start-Sleep -Seconds 10
Start-Process powershell -ArgumentList "-noexit", "-noprofile", "-command & cd ~\Desktop\mobile-game-auto\QBot\Amiya
nb run"
Start-Sleep -Seconds 10
Start-Process powershell -ArgumentList "-noexit", "-noprofile", "-command & cd ~\Desktop\mobile-game-auto
python http_server.py"