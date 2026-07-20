param(
    [Parameter()]
    [string]$Action = "menu"
)

# --- Кодировка вывода: UTF-8, чтобы кириллица не превращалась в "?" ---
try { chcp 65001 > $null } catch { }
try {
    [Console]::OutputEncoding = [System.Text.Encoding]::UTF8
    $OutputEncoding = [System.Text.Encoding]::UTF8
} catch { }

function Draw-Header {
    Write-Host ''
    Write-Host '  PAP - Playerok Auto Placement' -ForegroundColor Cyan
    Write-Host '  ===================================' -ForegroundColor DarkCyan
    Write-Host '  Разработчик: ' -ForegroundColor Gray -NoNewline
    Write-Host '@lovesort' -ForegroundColor White
    Write-Host '  Новости:     ' -ForegroundColor Gray -NoNewline
    Write-Host 't.me/rogaartproduction' -ForegroundColor White
    Write-Host '  Плагины:     ' -ForegroundColor Gray -NoNewline
    Write-Host 't.me/lovesort' -ForegroundColor White
    Write-Host ''
}

function Draw-Line {
    Write-Host '  -----------------------------------' -ForegroundColor DarkGray
}

function Show-Intro {
    Clear-Host
    Draw-Header
    Write-Host '  Инициализация системы...' -ForegroundColor Cyan
    Write-Host ''
    $steps = @('Загрузка ядра', 'Подключение модулей', 'Проверка GitHub API', 'Синхронизация данных')
    $perc = 25
    foreach ($s in $steps) {
        $filled = [math]::Floor($perc / 4)
        $empty = 25 - $filled
        $bar = ('#' * $filled) + ('-' * $empty)
        Write-Host '  [ ' -ForegroundColor Cyan -NoNewline
        Write-Host $bar -ForegroundColor Green -NoNewline
        Write-Host (' ] {0,3}% - ' -f $perc) -ForegroundColor Gray -NoNewline
        Write-Host $s -ForegroundColor Gray
        $perc += 25
    }
    Write-Host ''
    Write-Host '  [ OK ] Система готова к работе' -ForegroundColor Green
    Start-Sleep -Seconds 1
}

function Show-Menu {
    Clear-Host
    Draw-Header
    Write-Host '  ГЛАВНОЕ МЕНЮ' -ForegroundColor White
    Draw-Line
    Write-Host '  [1] ' -ForegroundColor Green -NoNewline
    Write-Host ' Запустить Telegram-бота' -ForegroundColor White
    Write-Host '  [2] ' -ForegroundColor Cyan -NoNewline
    Write-Host ' Проверить обновления' -ForegroundColor White
    Write-Host '  [3] ' -ForegroundColor Blue -NoNewline
    Write-Host ' Отправить изменения на GitHub' -ForegroundColor White
    Write-Host '  [4] ' -ForegroundColor Magenta -NoNewline
    Write-Host ' Создать новый релиз' -ForegroundColor White
    Write-Host '  [5] ' -ForegroundColor Yellow -NoNewline
    Write-Host ' Открыть папку проекта' -ForegroundColor White
    Write-Host '  [6] ' -ForegroundColor Green -NoNewline
    Write-Host ' Создать бэкап' -ForegroundColor White
    Write-Host '  [7] ' -ForegroundColor Red -NoNewline
    Write-Host ' Выйти' -ForegroundColor White
    Write-Host ''
    Draw-Line
}

function Start-Bot {
    Clear-Host
    Draw-Header
    Write-Host '  [ Шаг 1 / 2 ]  Проверка обновлений...' -ForegroundColor Cyan
    Write-Host ''
    python updater.py
    if ($LASTEXITCODE -ne 0) {
        Write-Host '  [ ! ] Не удалось проверить обновления. Запускаю бота всё равно...' -ForegroundColor Yellow
    }
    Write-Host ''
    Write-Host '  [ Шаг 2 / 2 ]  Запуск Telegram-бота...' -ForegroundColor Green
    Write-Host ''
    python bot.py
    Write-Host ''
    Write-Host '  Бот остановлен. Нажмите любую клавишу для возврата в меню.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Check-Updates {
    Clear-Host
    Draw-Header
    Write-Host '  Отправка запроса к GitHub API...' -ForegroundColor Cyan
    Write-Host ''
    python updater.py
    Write-Host ''
    Write-Host '  Проверка завершена. Нажмите любую клавишу.' -ForegroundColor Gray
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
    Write-Host '  [ OK ] Изменения отправлены.' -ForegroundColor Green
    Write-Host '  Нажмите любую клавишу для возврата.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Create-Release {
    Clear-Host
    Draw-Header
    Write-Host '  Создание нового релиза на GitHub...' -ForegroundColor Magenta
    Write-Host ''
    python create_release.py
    Write-Host ''
    Write-Host '  Операция завершена. Нажмите любую клавишу.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Open-Folder {
    explorer $PSScriptRoot
    Write-Host '  Папка открыта. Нажмите любую клавишу.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Backup-Data {
    Clear-Host
    Draw-Header
    Write-Host '  Создание архива настроек и данных...' -ForegroundColor Green
    Write-Host ''
    python backup.py create
    Write-Host ''
    Write-Host '  [ ! ] Храните архив в надёжном месте - в нём ключ шифрования.' -ForegroundColor Yellow
    Write-Host '  Нажмите любую клавишу для возврата.' -ForegroundColor Gray
    [void][System.Console]::ReadKey($true)
}

function Exit-App {
    Clear-Host
    Draw-Header
    Write-Host '  Спасибо за использование!' -ForegroundColor Green
    Start-Sleep -Seconds 2
    exit 0
}

if ($Action -eq 'intro') {
    Show-Intro
} elseif ($Action -eq 'menu') {
    Show-Intro
    while ($true) {
        Show-Menu
        $choice = Read-Host '  Выберите действие [1-7]'
        switch ($choice) {
            '1' { Start-Bot }
            '2' { Check-Updates }
            '3' { Push-GitHub }
            '4' { Create-Release }
            '5' { Open-Folder }
            '6' { Backup-Data }
            '7' { Exit-App }
            default {
                Write-Host '  [ X ] Неверный пункт меню. Попробуйте ещё раз.' -ForegroundColor Red
                Start-Sleep -Seconds 1
            }
        }
    }
}
