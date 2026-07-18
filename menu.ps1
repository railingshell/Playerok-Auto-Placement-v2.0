# Playerok Auto Placement Menu
param(
    [Parameter()]
    [string]$Action = "menu"
)

$colors = @{
    Cyan = 'Cyan'
    Green = 'Green'
    White = 'White'
    Gray = 'Gray'
    Yellow = 'Yellow'
    Blue = 'Blue'
    Magenta = 'Magenta'
    Red = 'Red'
    DarkGray = 'DarkGray'
}

function Draw-Header {
    Write-Host ''
    Write-Host '+============================================================+' -ForegroundColor Cyan
    Write-Host '|              Playerok Auto Placement v2.0                  |' -ForegroundColor Cyan
    Write-Host '|                  by @lovesort (rogart)                     |' -ForegroundColor Cyan
    Write-Host '+============================================================+' -ForegroundColor Cyan
    Write-Host '|  Telegram: @rogartproduction                               |' -ForegroundColor Cyan
    Write-Host '|  Plaginy:  t.me/lovesort                                   |' -ForegroundColor Cyan
    Write-Host '+============================================================+' -ForegroundColor Cyan
    Write-Host ''
}

function Draw-Line {
    Write-Host '--------------------------------------------------------------' -ForegroundColor DarkGray
}

function Draw-Box($text) {
    Write-Host '+============================================================+' -ForegroundColor Cyan
    Write-Host ("|  {0,-54}   |" -f $text) -ForegroundColor Cyan
    Write-Host '+============================================================+' -ForegroundColor Cyan
}

function Show-Intro {
    Clear-Host
    Draw-Header
    Write-Host '  [ PRE-BOOT ] Inicializacija sistemy...' -ForegroundColor Cyan
    Write-Host ''
    $steps = @('Zagruzka jadra', 'Podkljuchenie modulej', 'Proverka GitHub API', 'Sinhronizacija dannyh')
    $perc = 25
    foreach ($s in $steps) {
        $filled = [math]::Floor($perc / 2)
        $empty = 50 - $filled
        $bar = '#' * $filled + '-' * $empty
        $num = '{0,3}' -f $perc
        Write-Host '  [ ' -ForegroundColor Cyan -NoNewline
        Write-Host $bar -ForegroundColor Green -NoNewline
        Write-Host ' ] ' -ForegroundColor Cyan -NoNewline
        Write-Host $num -ForegroundColor White -NoNewline
        Write-Host '% - ' -ForegroundColor Gray -NoNewline
        Write-Host $s -ForegroundColor Gray
        $perc += 25
    }
    Write-Host ''
    Write-Host '  [ OK ] ' -ForegroundColor Green -NoNewline
    Write-Host 'Sistema gotova k rabote' -ForegroundColor White
    Start-Sleep -Seconds 1
}

function Show-Menu {
    Clear-Host
    Draw-Header
    Draw-Box 'GLAVNOE MENYU'
    Write-Host ''
    Write-Host '  [1]  ->  ' -ForegroundColor Green -NoNewline
    Write-Host 'Zapustit Telegram bota' -ForegroundColor White
    Write-Host '  [2]  ->  ' -ForegroundColor Cyan -NoNewline
    Write-Host 'Proverit obnovlenija' -ForegroundColor White
    Write-Host '  [3]  ->  ' -ForegroundColor Blue -NoNewline
    Write-Host 'Zapushit izmenenija na GitHub' -ForegroundColor White
    Write-Host '  [4]  ->  ' -ForegroundColor Magenta -NoNewline
    Write-Host 'Sozdat novyj reliz' -ForegroundColor White
    Write-Host '  [5]  ->  ' -ForegroundColor Yellow -NoNewline
    Write-Host 'Otkryt papku proekta' -ForegroundColor White
    Write-Host '  [6]  ->  ' -ForegroundColor Red -NoNewline
    Write-Host 'Vyjti' -ForegroundColor White
    Write-Host ''
    Draw-Line
}

function Start-Bot {
    Clear-Host
    Draw-Header
    Write-Host '  [ SHAG 1 / 2 ] Proverka obnovlenij...' -ForegroundColor Cyan
    Write-Host ''
    python updater.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host '  [ VNIMANIE ] Ne udalos proverit obnovlenija. Zapusk bota vse ravno...' -ForegroundColor Yellow
    }
    Write-Host ''
    Write-Host '  [ SHAG 2 / 2 ] Zapusk Telegram bota...' -ForegroundColor Green
    Write-Host ''
    python bot.py
    Write-Host ''
    Write-Host '  [ INFO ] Bot ostanovlen. Najmite lyubuju klavishu dlja vozvrata v menju.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Check-Updates {
    Clear-Host
    Draw-Header
    Write-Host '  [ PROVERKA ] Otpravka zaprosa k GitHub API...' -ForegroundColor Cyan
    Write-Host ''
    python updater.py
    Write-Host ''
    Write-Host '  [ INFO ] Proverka zavershena. Najmite lyubuju klavishu.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Push-GitHub {
    Clear-Host
    Draw-Header
    $msg = Read-Host '  Vvedite soobshenie kommita'
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = 'Avtoobnovlenie' }
    Write-Host ''
    Write-Host '  [1/3] Dobavlenie fajlov v indeks...' -ForegroundColor Blue
    git add -A
    Write-Host '  [2/3] Sozdanie kommita...' -ForegroundColor Blue
    git commit -m "$msg"
    Write-Host '  [3/3] Otpravka na GitHub...' -ForegroundColor Blue
    git push origin main
    Write-Host ''
    Write-Host '  [ GOTOWO ] ' -ForegroundColor Green -NoNewline
    Write-Host 'Izmenenija otpravleny.' -ForegroundColor White
    Write-Host '  Najmite lyubuju klavishu dlja vozvrata.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Create-Release {
    Clear-Host
    Draw-Header
    Write-Host '  [ RELIZ ] Sozdanie novogo reliza na GitHub...' -ForegroundColor Magenta
    Write-Host ''
    python create_release.py
    Write-Host ''
    Write-Host '  [ INFO ] Operacija zavershena. Najmite lyubuju klavishu.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Open-Folder {
    explorer $PSScriptRoot
    Write-Host '  [ INFO ] Papka otkryta. Najmite lyubuju klavishu.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Exit-App {
    Clear-Host
    Draw-Header
    Write-Host '  [ DO SVIDANIJA ] ' -ForegroundColor Green -NoNewline
    Write-Host 'Spasibo za ispolzovanie!' -ForegroundColor White
    Start-Sleep -Seconds 2
    exit 0
}

if ($Action -eq 'intro') {
    Show-Intro
} elseif ($Action -eq 'menu') {
    Show-Intro
    while ($true) {
        Show-Menu
        $choice = Read-Host '  Vyberite dejstvie [1-6]'
        switch ($choice) {
            '1' { Start-Bot }
            '2' { Check-Updates }
            '3' { Push-GitHub }
            '4' { Create-Release }
            '5' { Open-Folder }
            '6' { Exit-App }
            default {
                Write-Host '  [ OSIBKA ] Nevernyj punkt menju. Poprobujte eshche raz.' -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}
