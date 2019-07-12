# Monitoring importan emails from ak545
**check_email.py** - Это python-скрипт для мониторинга почтового ящика на предмет поступления в него определённых писем.

## Скриншоты
> Скрипт в работе
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script1.png)
<details>
<summary>Ещё больше</summary>

![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script2.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script3.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script4.png)

> Примеры email
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email1.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email2.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email3.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email4.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email5.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email6.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email7.png)

> Пример оригинального EML email
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/original_email.png)

> Пример Telegram сообщений
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/telegram.png)
</details>

## Описание
Если Вы находитесь здесь, возможно, Вы уже сталкивались с подобной проблемой.

***

<details>
  <summary>TL;DR (предыстория)</summary>

___

Сразу надо сказать, что для связи с общественностью у нашей компании, как и у других, есть публичный почтовый ящик.
Разумеется, он почти на 99% заполняется различным мусором и спамом. 
Но, тем не менее, он нужен. 

И вот, как-то раз, пришёл я на работу после отпуска, и первым же делом стал проверять почту.
И тогда, после удаления тонны спама, я обнаружил одно важное письмо из Роскомнадзора. Хорошо, что я его не удалил, приняв за спам.
В письме говорилось о том, что на одном из наших ресурсов в Сети (ссылку указали), имеется материал, подлежащий удалению. На исполнение требования по устранению нарушения нам дали всего одни сутки с момента отправки данного письма, по истечении которых, в случае невыполнения данного требования, наш сетевой ресурс попал бы в реестр запрещённых в РФ сайтов (не иронизируйте - подобные реестры имеются почти во всех странах). 

Письмо пришло в наш публичный почтовый ящик за трое суток до того, как я вернулся из отпуска. Наш сетевой ресурс к тому времени уже был в реестре запрещённых в РФ сайтов. 

Проблему мы решили моментально - указанный в письме контент удалили, автора контента заблокировали навсегда, ответ в Роскомнадзор о принятых мерах написали, из реестра запрещённых в РФ сайтов наш сетевой ресурс отозвали. 

Но осадочек, как говорится, остался.

Немного подумав, я решил написать этот python скрипт, при помощи которого теперь отслеживаю появление в нашем публичном почтовом ящике важных (с моей точки зрения) писем.
Я добавил этот python скрипт в cron и теперь каждые три часа он производит проверку и анализ входящих писем.

При обнаружении важных писем скрипт рассылает уведомления тем получателям, которых я посчитал нужным назначить ответственными для обработки таких событий. Для этого я доплнительно создал в Telegram общий групповой чат, куда пригласил всех ответственных. Так же добавил в этот чат бота, от имени которого в этом чате автоматически появляются соответствующие уведомления.

</details>

***

**Особенности скрипта:**

- Уведомление (как по email, так и в Telegram чате) при обнаружении важного письма рассылается только один раз. 
- Скрипт понимает, кому следует отправлять email уведомление, а кому нет. 
- Уведомления в чат Telegram приходят всегда (так как это групповой чат и в нём находятся все потенциальные получатели уведомлений). 
- В зависимости от полномочий сотрудников, в групповом чате Telegram появляется: 
    - или полное уведомление (с указанием адреса отправителя, даты, темы и с кратким содержанием текста письма) 
    - или неполное уведомление (с указанием только имён сотрудников, которые должны обработать это событие и которые должны игнорировать его) 
    
    Сотрудникам, которые должны обработать это событие, рекомендуется проверить свои почтовые ящики.
- В email уведомлении содержится служебная информация о важном письме (адрес отправителя, дата, тема и полный текст письма), а так же оригинал важного письма в виде приложения к email в **ZIP**-архиве (без пароля), внутри котрого сам оригинал письма в формате **EML**.
- Скрипт хранит все важные email письма в своём кэше на сервере, где он работает. Как только важное email письмо исчезнет с почтового сервера, например, при работе с почтовым сервером по протоколу POP3, ранее сохранённое в кэше скрипта важное email письмо из этого кэша удаляется, а его архивная **ZIP** копия перемещается в папку истории скрипта. Из этой папки **ZIP** архив уже автоматически не удаляется.
- При массовой рассылке email уведомлений для каждого получателя формируется отдельное письмо. Таким образом в RFC822-заголовках письма (например, в **TO**, **CC** и т.п.) присутствует только один адрес получателя. Email адреса других получателей не раскрываются.

## Инсталляция
Для работы скрипта необходим **Python версии 3.6 или выше**.
Разумеется, необходимо сперва установить сам [Python](https://www.python.org/). В Linux он обычно уже установлен. Если нет, установите его, например:

    $ sudo yum install python3
    $ sudo dnf install python3
    $ sudo apt install python3
    $ sudo pacman -S python

Для Apple macOS:
    
    $ xcode-select --install
    
Установите brew:

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Установите Python:

    $ export PATH=/usr/local/bin:/usr/local/sbin:$PATH
    $ brew install python

Примечание: [brew](https://brew.sh/index_ru)

Для Microsoft Windows скачайте [дистрибутив](https://www.python.org/downloads/windows/) и установите его. Я рекомендую скачивать **"Download Windows x86 web-based installer"** если у вас 32-х битная ОС и **"Download Windows x86-64 web-based installer"** если у вас 64-х битная ОС. Во время установки рекомендую отметить все опции (Documentation, pip, tcl/tk and IDLE, Python test suit, py launcher, for all users (requeres elevation)).

Предварительно, возможно понадобится обновить сам **pip** (установщик модулей Python):

    $ python -m pip install --upgrade pip

### Установка зависимостей

    $ pip install colorama

    Если вы планируете использовать socks5 прокси для работы с Telegram, то дополнительно:
    
    $ pip install requests[socks]
    или
    $ pip install PySocks

### Обновление зависимостей

    $ pip install --upgrade colorama

    Если вы планируете использовать socks5 прокси для работы с Telegram, то дополнительно:

    $ pip install --upgrade requests[socks]
    или
    $ pip install --upgrade PySocks

В зависимости от вашего Pyton окружения, ваши действия будут немного иными, например, возможно, вам потребуется указать ключ **--user** (для **pip**) или вместо команд **python** и **pip** использовать команды **python3** и **pip3**. Если вы используете [виртуальные окружения](https://docs.python.org/3/library/venv.html), то скорее всего, все эти действия вам необходимо будет сделать после входа в соответствующее окружение.

## Использование
    $ check_email.py
    или
    $ python check_email.py
    или
    $ chmod +x check_email.py # Один раз
    $ ./check_email.py

### Описание опций
Опций нет. Чем проще, тем лучше.

## Глобальные константы параметров в скрипте
Все параметры находятся внутри срипта. Вам необходимо их настроить.

### Параметры SMTP сервера
**SMTP_SERVER**

Адрес SMTP сервера для отправки email уведолений конкретным получателям (получатели и их свойства описываются в параметре **RECIPIENTS_FULL**)

Примеры:

    SMTP_SERVER = "localhost"
    SMTP_SERVER = "smtp.gmail.com"

**SMTP_PORT**

SMTP порт

Примеры:
    
    SMTP_PORT = 587  # Для STARTTLS
    SMTP_PORT = 465  # Для SSL
    SMTP_PORT = 25   # По умолчанию

**SMTP_SSL**

SMTP сервер использует подключение по SSL

Примеры:

    SMTP_SSL = True

**SMTP_STARTTLS**

SMTP сервер использует подключение по STARTTLS

Примеры:

    SMTP_STARTTLS = True

> Параметры **SMTP_SSL** и **SMTP_STARTTLS** взаимоисключающие. **Нельзя устанавливать значения этих обоих параметров в True!** Активным может быть только один из них, или нисколько. Если они не используются оба, установите их значение в **False**.


**SMTP_SENDER**

Email адрес отправителя

Примеры:

    SMTP_SENDER = "user@gmail.com"

**SMTP_PASSWORD**

SMTP пароль

Примеры:

    SMTP_PASSWORD = "P@ssw0rd"

### Параметры мониторинга
**Внимание!**
Поддерживаются только **IMAP4** сервера!

**CONTROLLED_EMAIL_SERVER**

Адрес IMAP4 сервера

Примеры:

    CONTROLLED_EMAIL_SERVER = "mx.example.com"

**CONTROLLED_EMAIL_ADDRESSES**

Почтовый ящик на IMAP4 сервере, который подлежит мониторингу

Примеры:

    CONTROLLED_EMAIL_ADDRESSES = "public@example.com"

**CONTROLLED_EMAIL_ADDRESSES_PASSWORD**

Пароль от почтового ящика на IMAP4 сервере, который подлежит мониторингу

Примеры:

    CONTROLLED_EMAIL_ADDRESSES_PASSWORD = "P@ssw0rd"


### Список email-адресов для мониторинга

**CONTROLLED_EMAIL_ADDRESSES_SENDERS**

Список email-адресов (или фрагментов таких адресов) при наличии которых отправляем уведомления в Telegram-чат и на email-почту определённым получателям из списка **RECIPIENTS_FULL** 

Примеры:

    CONTROLLED_EMAIL_ADDRESSES_SENDERS = [
        'alisa@example.com',
        'bob@example.com',
        'abuse@example.com',
        'admin@example.com',
        'domain@example.com',
        'zapret-info-out@rkn.gov.ru',
        '@mvd.ru',
    ]

Регулярные выражения и шаблонные маски (wildcard mask) не поддерживаются!


### Список получателей E-mail и Telegram уведолений

**RECIPIENTS_FULL**

Список получателей email и Telegram уведолений.

В этом списке содержатся:
- email адреса получателей email и Telegram уведомлений 
- их имена 
- и списки тех email адресов из списка email-адресов для мониторинга **CONTROLLED_EMAIL_ADDRESSES_SENDERS**, которые для конкретного получателя уведомлений не касаются.

Предполагается, что все перечисленные получатели уведомлений так же находятся в общем групповом Telegram чате (см. раздел **Параметры Telegram**).

Примеры:

    RECIPIENTS_FULL = {
        # E-mail адрес получателя уведомлений
        'alisa@example.com': [
            # Имя получателя уведомлений
            'Alisa',
    
            # Адреса (и фрагменты адресов) входящих писем по которым
            # не отсылаются уведомления для этого получателя
            [
                'alisa@example.com',
                'abuse@example.com',
                'domain@example.com',
                'zapret-info-out@rkn.gov.ru',
                '@mvd.ru',
            ]
        ],
        'bob@example.com': [
            'Bob',
            [
                'bob@example.com',
                'abuse@example.com',
                'domain@example.com',
                'zapret-info-out@rkn.gov.ru',
                '@mvd.ru',
            ]
        ],
        'moderator@example.com': [
            'Moderator',
            [
                'domain@example.com',
                'zapret-info-out@rkn.gov.ru',
                '@mvd.ru',
            ]
        ],
        'abuse@example.com': [
            'Abuse',
            [
                'domain@example.com',
                '@mvd.ru',
            ]
        ],
        'admin@example.com': [
            'Admin',
            []
        ],
    }

Описанная таким образом структура получателей уведомлений в сочетании со списком email-адресов для мониторинга приведёт к следующим результатам при возникновении отслеживаемого события.

    При обнаружиниее в почтовом ящике письма от:

        1. alisa@example.com
        --------------------------
        не получат email уведомлений: 
            Alisa 
        получат email уведомления:
            Bob 
            Moderator
            Abuse
            Admin
        в Telegram-чат будет отправлено неполное уведомление


        2. bob@example.com
        --------------------------
        не получат email уведомлений: 
            Bob 
        получат email уведомления:
            Alisa 
            Moderator
            Abuse
            Admin
        в Telegram-чат будет отправлено неполное уведомление


        3. abuse@example.com
        --------------------------
        не получат email уведомлений: 
            Alisa
            Bob 
        получат email уведомления:
            Moderator
            Abuse
            Admin
        в Telegram-чат будет отправлено неполное уведомление


        4. admin@example.com
        --------------------------
        не получат email уведомлений: 
            -
        получат email уведомления:
            Alisa
            Bob
            Moderator
            Abuse
            Admin
        в Telegram-чат будет отправлено полное уведомление


        5. domain@example.com
        --------------------------
        не получат email уведомлений: 
            Alisa
            Bob
            Moderator
            Abuse
        получат email уведомления:
            Admin
        в Telegram-чат будет отправлено неполное уведомление


        6. zapret-info-out@rkn.gov.ru
        --------------------------
        не получат email уведомлений: 
            Alisa
            Bob
            Moderator
        получат email уведомления:
            Abuse
            Admin
        в Telegram-чат будет отправлено неполное уведомление


        7. @mvd.ru
        --------------------------
        не получат email уведомлений: 
            Alisa
            Bob
            Moderator
            Abuse
        получат email уведомления:
            Admin
        в Telegram-чат будет отправлено неполное уведомление

> Возможно для всего этого есть какой-то умный термин. Но я его не знаю 😏

### Параметры Telegram
**TELEGRAM_MY_TOKEN**

Токен Telegram бота

Примеры:

    TELEGRAM_MY_TOKEN = 'NNNNNNNNN:NNNSSSSaaaaaFFFFFEEE3gggggQQWFFFFF01z'

**TELEGRAM_CHAT_ID**

Идентификатор канала Telegram

Примеры:

    TELEGRAM_CHAT_ID = '-NNNNNNNNN'

Получить помощь по API Telegram: 
[https://core.telegram.org/bots](https://core.telegram.org/bots)
Создать бота можно пообщавшись в Telegram с [**@BotFather**](https://telegram.me/BotFather)

**TELEGRAM_URL**

Telegram API URL

Примеры:

    TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_MY_TOKEN + "/"

**TELEGRAM_PROXIES**

Telegram proxyes

Примеры:

    TELEGRAM_PROXIES = {
     'http': 'socks5://127.0.0.1:9150',
     'https': 'socks5://127.0.0.1:9150',
    }

или

    # Если прокси не используется
    TELEGRAM_PROXIES = {}

**EML_PATH**

Папка для хранения кэша писем.
> На основании наличия данных в этом кэше так же определяется, отправлялось ли ранее уже уведомление.

В этой папке сохраняются все обнаруженные важные письма (**EML**-оригиналы и их **ZIP**-архивы).

Эта папка автоматически очищается от устаревших данных при каждой новой проверке.
Письма, которых уже нет на почтовом сервере перемещаются в папку истории (см. параметр **EML_PATH_READY**): EML-оригиналы удаляются, ZIP-архивы перемещаются. 

**EML_PATH_READY**

Папка для хранения истории писем, когда их уже нет на почтовом сервере (например, когда их загрузили с почтового сервера по протоколу POP3 с удалением оригиналов с сервера).
Уже отсутствующие на почтовом сервере важные письма, таким образом, всё ещё можно при необходимости прочитать.
Папка автоматически не очищается!
Здесь хранятся только **ZIP**-архивы.

## Примечание общего плана
> Строковые значения в **python** можно заключать в кавычки:
 
```python

'одинарные'

"двойные"

'''тройные 
        одинарные
'''

"""тройные 
        двойные
"""

```

## Как добавить скрипт в Linux cron
Для этого создайте **crontab** задачу, которая будет выполняться, например, каждые три часа от имени пользователя (создавать задачи от имени root не лучшая идея):

Предположим, ваш логин в Linux: **user**

Ваша домашняя папка: **/home/user**

Папка, где находится этот скрипт: **/home/user/py**

Чтобы запускать скрипт напрямую, выполните команду:
    
    $ chmod +x /home/user/py/check_email.py

Скорректируйте в первой строке скрипта [Шебанг (Unix)](https://ru.wikipedia.org/wiki/%D0%A8%D0%B5%D0%B1%D0%B0%D0%BD%D0%B3_(Unix)), например:

Показать путь, где расположен python:
    
    $ which python

или

    $ which python3
    
Коррекция пути python в Шебанг:

    #!/usr/bin/python
    #!/usr/bin/python3
    #!/usr/bin/env python
    #!/usr/bin/env python3

Переименуйте скрипт:

    $ mv /home/user/py/check_email.py /home/user/py/check_email

Проверьте запуск скрипта:

    $ /home/user/py/check_email
    $ /home/user/py/./check_email

Если всё нормально, запустите редактор **crontab**, если нет, вернитесь к настройке **Шебанг**:

    $ crontab -u user -e
    Здесь user - это ваш логин в Linux


Если вы, как и я не любите vim (я не видел ни одного человека, в совершенстве владеющего этим редактором, хотя, наверное, он где-то есть), вы можете редактировать задачи в вашем любимом редакторе, например, так:

    $ EDITOR=nano crontab -u user -e
    $ EDITOR=mcedit crontab -u user -e

В файле задач создайте примерно такую запись:

    0 */3 * * * /home/user/py/check_email >/dev/null 2>&1

или

    0 */3 * * * /home/user/py/./check_email >/dev/null 2>&1    

> Примечание:
>
> **>/dev/null 2>&1** - подавление вывода на консоль или куда-либо ещё

или

    # В процессе работы скрипт печатает в консоли служебную информацию
    # Эту информацию можно перенаправить в файл лог
    0 */3 * * * /home/user/py/./check_email >> /home/user/py/check_email.log

Указывайте полные пути к файлу логов и к самому скрипту.

Примечание: [cron](https://ru.wikipedia.org/wiki/Cron)

Посмотреть созданные задачи для пользователя **user** можно так:

    $ crontab -u user -l

Удалить все задачи пользователя **user** можно так:

    $ crontab -u user -r


## Как добавить скрипт в Планировщик заданий Microsoft Windows
Обратитесь за помощью к [документации](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

**Пример:**

Запускать задачу каждую полночь:

`schtasks /Create /SC DAILY /TN "Monitoring importan emails" /TR "'с:\check_email.py'" /ST 23:59`

## Спасибо за идею
[Роскомнадзору](https://rkn.gov.ru/), который отныне выделяет всего одни сутки на принятие мер.

## Лицензия
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Ограничения
Я, автор этого python-скрипта, написал этот скрипт исключительно для своих нужд. Никаких гарантий не предоставляется. Вы можете использовать этот скрипт свободно, без каких либо отчислений, в любых целях, кроме тех, что намеренно приводят ко [злу](https://ru.wikipedia.org/wiki/Зло).

Вы можете вносить любые правки в код скрипта и делать форк этого скрипта, указав в качестве источника вашего вдохновения [меня](https://github.com/ak545).
Я не тщеславен, но хорошее слово и кошке приятно.

## Постскриптум
- Работа скрипта проверялась в Microsoft Windows 10, Linux Fedora 30, Linux Ubuntu Descktop 18.10, Linux CentOS 6/7, Linux Manjaro 18.0.2.
- Программный код скрипта не идеален. Но прошу простить меня за это. На момент написания этого скрипта, Python я изучал всего месяц. Мне нравится этот язык программирования, он намного проще и вместе с тем мощнее, чем другие языки программирования, которыми я владею. 
- Все рекомендации данные мной для Apple macOS могут содержать в себе неточности. Простите, у меня нет под рукой Apple macBook (но вдруг, кто-то подарит мне его?).
- Да здравствует E = mc&sup2; !
- Желаю всем удачи!

## Последняя просьба
Пришло время положить конец Facebook. Работа там не является нейтральной с этической точки зрения: каждый день, когда вы идете туда на работу, вы делаете что-то не так. Если у вас есть учетная запись Facebook, удалите ее. Если ты работаешь в Facebook, увольняйся.

И давайте не будем забывать, что Агентство национальной безопасности должно быть уничтожено.

*(c) [David Fifield](mailto:david@bamsoftware.com)*


---


> Best regards, ak545 ( ru.mail&copy;ak545&sup2; )