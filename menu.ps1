# Playerok Auto Placement Menu
param(
    [Parameter()]
    [string]$Action = "menu"
)

function Draw-Header {
    Write-Host ''
    Write-Host '+============================================================+' -ForegroundColor Cyan
    Write-Host '|              Playerok Auto Placement v2.0                  |' -ForegroundColor Cyan
    Write-Host '|                  by @lovesort (rogart)                     |' -ForegroundColor Cyan
    Write-Host '+============================================================+' -ForegroundColor Cyan
    Write-Host '|  Telegram: @rogartproduction                               |' -ForegroundColor Cyan
    Write-Host '|  Плагины:  t.me/lovesort                                   |' -ForegroundColor Cyan
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
    Write-Host '  [ PRE-BOOT ] Инициализация системы...' -ForegroundColor Cyan
    Write-Host ''
    $steps = @('Загрузка ядра', 'Подключение модулей', 'Проверка GitHub API', 'Синхронизация данных')
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
    Write-Host 'Система готова к работе' -ForegroundColor White
    Start-Sleep -Seconds 1
}

function Show-Menu {
    Clear-Host
    Draw-Header
    Draw-Box 'ГЛАВНОЕ МЕНЮ'
    Write-Host ''
    Write-Host '  [1]  ->  ' -ForegroundColor Green -NoNewline
    Write-Host 'Запустить Telegram бота' -ForegroundColor White
    Write-Host '  [2]  ->  ' -ForegroundColor Cyan -NoNewline
    Write-Host 'Проверить обновления' -ForegroundColor White
    Write-Host '  [3]  ->  ' -ForegroundColor Blue -NoNewline
    Write-Host 'Запушить изменения на GitHub' -ForegroundColor White
    Write-Host '  [4]  ->  ' -ForegroundColor Magenta -NoNewline
    Write-Host 'Создать новый релиз' -ForegroundColor White
    Write-Host '  [5]  ->  ' -ForegroundColor Yellow -NoNewline
    Write-Host 'Открыть папку проекта' -ForegroundColor White
    Write-Host '  [6]  ->  ' -ForegroundColor Red -NoNewline
    Write-Host 'Выйти' -ForegroundColor White
    Write-Host ''
    Draw-Line
}

function Start-Bot {
    Clear-Host
    Draw-Header
    Write-Host '  [ ШАГ 1 / 2 ] Проверка обновлений...' -ForegroundColor Cyan
    Write-Host ''
    python updater.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host '  [ ВНИМАНИЕ ] Не удалось проверить обновления. Запуск бота всё равно...' -ForegroundColor Yellow
    }
    Write-Host ''
    Write-Host '  [ ШАГ 2 / 2 ] Запуск Telegram бота...' -ForegroundColor Green
    Write-Host ''
    python bot.py
    Write-Host ''
    Write-Host '  [ ИНФО ] Бот остановлен. Нажмите любую клавишу для возврата в меню.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Check-Updates {
    Clear-Host
    Draw-Header
    Write-Host '  [ ПРОВЕРКА ] Отправка запроса к GitHub API...' -ForegroundColor Cyan
    Write-Host ''
    python updater.py
    Write-Host ''
    Write-Host '  [ ИНФО ] Проверка завершена. Нажмите любую клавишу.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Push-GitHub {
    Clear-Host
    Draw-Header
    $msg = Read-Host '  Введите сообщение коммита'
    if ([string]::IsNullOrWhiteSpace($msg)) { $msg = 'Автообновление' }
    Write-Host ''
    Write-Host '  [1/3] Добавление файлов в индекс...' -ForegroundColor Blue
    git add -A
    Write-Host '  [2/3] Создание коммита...' -ForegroundColor Blue
    git commit -m "$msg"
    Write-Host '  [3/3] Отправка на GitHub...' -ForegroundColor Blue
    git push origin main
    Write-Host ''
    Write-Host '  [ ГОТОВО ] ' -ForegroundColor Green -NoNewline
    Write-Host 'Изменения отправлены.' -ForegroundColor White
    Write-Host '  Нажмите любую клавишу для возврата.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Create-Release {
    Clear-Host
    Draw-Header
    Write-Host '  [ РЕЛИЗ ] Создание нового релиза на GitHub...' -ForegroundColor Magenta
    Write-Host ''
    python create_release.py
    Write-Host ''
    Write-Host '  [ ИНФО ] Операция завершена. Нажмите любую клавишу.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Open-Folder {
    explorer $PSScriptRoot
    Write-Host '  [ ИНФО ] Папка открыта. Нажмите любую клавишу.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Exit-App {
    Clear-Host
    Draw-Header
    Write-Host '  [ ДО СВИДАНИЯ ] ' -ForegroundColor Green -NoNewline
    Write-Host 'Спасибо за использование!' -ForegroundColor White
    Start-Sleep -Seconds 2
    exit 0
}

if ($Action -eq 'intro') {
    Show-Intro
} elseif ($Action -eq 'menu') {
    Show-Intro
    while ($true) {
        Show-Menu
        $choice = Read-Host '  Выберите действие [1-6]'
        switch ($choice) {
            '1' { Start-Bot }
            '2' { Check-Updates }
            '3' { Push-GitHub }
            '4' { Create-Release }
            '5' { Open-Folder }
            '6' { Exit-App }
            default {
                Write-Host '  [ ОШИБКА ] Неверный пункт меню. Попробуйте ещё раз.' -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}