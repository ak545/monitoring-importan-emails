# Monitoring importan emails from ak545
**check_email.py** - This is a python script to monitor the mailbox for specific emails.

## Screenshots
> Script in working
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script1.png)

<details>
<summary>More</summary>


![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script2.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script3.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/script4.png)

> A samples of the email
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email1.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email2.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email3.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email4.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email5.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email6.png)
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/email7.png)

> A sample of the original EML email
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/original_email.png)

> A sample of the Telegram messages
![](https://github.com/ak545/monitoring-importan-emails/raw/master/images/telegram.png)
</details>

## Description
If you are here, you may have encountered a similar problem.

***

<details>
  <summary>TL;DR (prehistory)</summary>

___

Immediately I must say that our company, like others, has a public mailbox for public relations.
Of course, it is almost 99% filled with various junk and spam.
But, nevertheless, it is needed.

And then, once, I came to work after the holidays, and the very first thing I began to check the mail.
And then, after removing a ton of spam, I found one important letter from Roskomnadzor. It is good that I did not delete it, mistaking for spam.
The letter said that one of our resources on the web (link indicated), there is material to be deleted. We were given only one day from the moment of sending this letter to fulfill the requirement to eliminate the violation, after which, if this requirement was not fulfilled, our network resource would be placed in the registry of sites banned in the Russian Federation (don’t be ironic - almost all countries have such registries).

The letter arrived in our public mailbox three days before I returned from vacation. Our network resource by that time was already in the registry of sites prohibited in the Russian Federation.

We solved the problem instantly - the content specified in the letter was deleted, the content author was blocked forever, the answer was written to the Roskomnadzor, the network resource was withdrawn from the registry of sites prohibited in the Russian Federation.

But the discomfort, as they say, remained.

A little thought, I decided to write this python script, with the help of which now I track the appearance of important (from my point of view) letters in our public mailbox.
I added this python script to cron and now every three hours it checks and analyzes incoming emails.

When important letters are detected, the script sends notifications to those recipients whom I consider necessary to be made responsible for handling such events. For this, I additionally created in Telegram a general group chat, where I invited all those responsible. I also added a bot to this chat, on whose behalf the corresponding notifications automatically appear in this chat.

</details>

***

**Script features:**

- Notification (both by email and in Telegram chat) when an important letter is detected is sent only once. 
- The script understands who should be sent an email notification and who should not. 
- Notifications to the Telegram chat always come (as this is a group chat and it contains all potential recipients of notifications). 
- Depending on the powers of the employees, in the group chat of the Telegram appears: 
    - or full notification (with the address of the sender, date, subject, and a summary of the text of the letter) 
    - or incomplete notification (indicating only the names of employees who must handle this event and who should ignore it) 
    
    Employees who must handle this event are advised to check their mailboxes.
- The email notification contains service information about an important letter (sender address, date, subject and full text of the letter), as well as the original of the important letter as an attachment to an email in a **ZIP** archive (without a password), inside of which is the original **EML** letter .
- The script stores all the important email in its cache on the server where it works. As soon as the important email disappears from the mail server, for example, when working with the mail server using the POP3 protocol, the important email previously stored in the script cache is deleted from this cache, and its archive **ZIP** copy is moved to the history folder of script. **ZIP** archive is not automatically deleted from this folder.
- When sending email notifications for each recipient, a separate letter is generated. Thus, in the RFC822 headers of the letter (for example, in "TO", "CC", etc.) there is only one recipient address. Email addresses of other recipients are not disclosed.

## Installation
The script requires **Python version 3.6 or higher**.
Of course, you need to install it yourself first [Python](https://www.python.org/). On Linux, it is usually already installed. If not, install it, for example:

    $ sudo yum install python3
    $ sudo dnf install python3
    $ sudo apt install python3
    $ sudo pacman -S python

For Apple macOS:

    $ xcode-select --install
    
Install brew:

    $ /usr/bin/ruby -e "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/master/install)"

Install Python:

    $ export PATH=/usr/local/bin:/usr/local/sbin:$PATH
    $ brew install python

Note: [brew](https://brew.sh/)

For Microsoft Windows download the [distribution package](https://www.python.org/downloads/windows/) and install it. I recommend downloading "**Download Windows x86 web-based installer**" if you have a 32-bit OS and "**Download Windows x86-64 web-based installer**" if you have a 64-bit OS. During installation, I recommend checking all options (Documentation, pip, tcl / tk and IDLE, Python test suit, py launcher, for all users (requeres elevation)).

Previously, you may need to update **pip** itself (Python module installer):

    $ python -m pip install --upgrade pip

### Installing dependencies
    $ pip install colorama

    If you plan to use socks5 proxy to work with Telegram, then in addition:

    $ pip install requests[socks]
    or
    $ pip install PySocks

### Dependency update
    $ pip install --upgrade colorama

    If you plan to use socks5 proxy to work with Telegram, then in addition:

    $ pip install --upgrade requests[socks]
    or
    $ pip install --upgrade PySocks

Depending on your Pyton environment, your actions will be slightly different, for example, you may need to specify the **--user** key (for **pip**) or use the **python3** and **pip3** commands instead of the **python** and **pip** commands. If you use [virtual environments](https://docs.python.org/3/library/venv.html), then most likely, you will need to do all of these actions after entering the appropriate environment.

## Usage
    $ check_email.py
    or
    $ python check_email.py
    or
    $ chmod +x check_email.py # Once
    $ ./check_email.py

### Description of options
No options. The simpler the better.

## Global parameter constants in the script

All parameters are inside the script. You need to configure them.

### SMTP server settings
**SMTP_SERVER**

The SMTP server address for sending emails to specific recipients (recipients and their properties are described in the **RECIPIENTS_FULL** parameter)

Samples::

    SMTP_SERVER = "localhost"
    SMTP_SERVER = "smtp.gmail.com"

**SMTP_PORT**

SMTP port

Samples:
    
    SMTP_PORT = 587  # For STARTTLS
    SMTP_PORT = 465  # For SSL
    SMTP_PORT = 25   # Default

**SMTP_SSL**

SMTP server uses SSL connection

Samples:

    SMTP_SSL = True

**SMTP_STARTTLS**

SMTP server uses STARTTLS connection

Samples:

    SMTP_STARTTLS = True

> The **SMTP_SSL** and **SMTP_STARTTLS** parameters are mutually exclusive. **You cannot set these two parameters to True!** Only one of them can be active, or not at all. If they are not used both, set their value to **False**.


**SMTP_SENDER**

Email address of the sender

Samples:

    SMTP_SENDER = "user@gmail.com"

**SMTP_PASSWORD**

SMTP password

Samples:

    SMTP_PASSWORD = "P@ssw0rd"

### Monitoring options
**Attention!**
Only **IMAP4** servers are supported!

**CONTROLLED_EMAIL_SERVER**

IMAP4 server address

Samples:

    CONTROLLED_EMAIL_SERVER = "mx.example.com"

**CONTROLLED_EMAIL_ADDRESSES**

Mailbox on IMAP4 server to be monitored

Samples:

    CONTROLLED_EMAIL_ADDRESSES = "public@example.com"

**CONTROLLED_EMAIL_ADDRESSES_PASSWORD**

Password from the mailbox on the IMAP4 server to be monitored

Samples:

    CONTROLLED_EMAIL_ADDRESSES_PASSWORD = "P@ssw0rd"


### List of email addresses to monitor

**CONTROLLED_EMAIL_ADDRESSES_SENDERS**

A list of email addresses (or fragments of such addresses), in the presence of which we send notifications to Telegram-chat and to email-mail to certain recipients from the list **RECIPIENTS_FULL** 

Samples:

    CONTROLLED_EMAIL_ADDRESSES_SENDERS = [
        'alisa@example.com',
        'bob@example.com',
        'abuse@example.com',
        'admin@example.com',
        'domain@example.com',
        'zapret-info-out@rkn.gov.ru',
        '@mvd.ru',
    ]

Regular expressions and wildcard masks are not supported!


### List of E-mail and Telegram Recipients

**RECIPIENTS_FULL**

List of email and Telegram recipients.

This list contains:
- email addresses of recipients of email and telegram notifications 
- their names 
- and lists of those email addresses from the list of monitoring email addresses **CONTROLLED_EMAIL_ADDRESSES_SENDERS** that are not applicable to a specific recipient of notifications.

It is assumed that all of the listed recipients of notifications are also in the general group Telegram chat (see section **Telegram parameters**).

Samples:

    RECIPIENTS_FULL = {
        # E-mail address of the recipient of notifications
        'alisa@example.com': [
            # Notification Recipient Name
            'Alisa',
    
            # Addresses (and fragments of addresses) of incoming emails
            # to which notifications are sent to this recipient
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

The structure of notification recipients described in this way, combined with a list of monitoring email addresses, will lead to the following results when a monitored event occurs.

    When detected in the mailbox letters from:

        1. alisa@example.com
        --------------------------
        will not receive email notifications: 
            Alisa 
        will receive email notifications:
            Bob 
            Moderator
            Abuse
            Admin
        incomplete notification will be sent to Telegram chat


        2. bob@example.com
        --------------------------
        will not receive email notifications: 
            Bob 
        will receive email notifications:
            Alisa 
            Moderator
            Abuse
            Admin
        incomplete notification will be sent to Telegram chat


        3. abuse@example.com
        --------------------------
        will not receive email notifications: 
            Alisa
            Bob 
        will receive email notifications:
            Moderator
            Abuse
            Admin
        incomplete notification will be sent to Telegram chat


        4. admin@example.com
        --------------------------
        will not receive email notifications: 
            -
        will receive email notifications:
            Alisa
            Bob
            Moderator
            Abuse
            Admin
        full notification will be sent to Telegram chat


        5. domain@example.com
        --------------------------
        will not receive email notifications: 
            Alisa
            Bob
            Moderator
            Abuse
        will receive email notifications:
            Admin
        incomplete notification will be sent to Telegram chat


        6. zapret-info-out@rkn.gov.ru
        --------------------------
        will not receive email notifications: 
            Alisa
            Bob
            Moderator
        will receive email notifications:
            Abuse
            Admin
        incomplete notification will be sent to Telegram chat


        7. @mvd.ru
        --------------------------
        will not receive email notifications: 
            Alisa
            Bob
            Moderator
            Abuse
        will receive email notifications:
            Admin
        incomplete notification will be sent to Telegram chat

> Perhaps for all this there is some clever term. But I don't know him 😏

### Telegram parameters
**TELEGRAM_MY_TOKEN**

Telegram bot token

Samples:

    TELEGRAM_MY_TOKEN = 'NNNNNNNNN:NNNSSSSaaaaaFFFFFEEE3gggggQQWFFFFF01z'

**TELEGRAM_CHAT_ID**

Telegram Channel/Chat ID

Samples:

    TELEGRAM_CHAT_ID = '-NNNNNNNNN'

Get help with Telegram API:
[https://core.telegram.org/bots](https://core.telegram.org/bots)
You can create a bot by talking to Telegram with [**@BotFather**](https://telegram.me/BotFather)

**TELEGRAM_URL**

Telegram API URL

Samples:

    TELEGRAM_URL = "https://api.telegram.org/bot" + TELEGRAM_MY_TOKEN + "/"

**TELEGRAM_PROXIES**

Telegram proxyes

Samples:

    TELEGRAM_PROXIES = {
     'http': 'socks5://127.0.0.1:9150',
     'https': 'socks5://127.0.0.1:9150',
    }

or

    # If the proxy is not used
    TELEGRAM_PROXIES = {}

**EML_PATH**

The folder for storing the cache of letters.
> Based on the availability of data in this cache, it is also determined whether a notification has already been sent..

In this folder all found important letters are saved (**EML** originals and their **ZIP** archives).

This folder is automatically cleared of obsolete data with each new scan.
Emails that are no longer on the mail server are moved to the history folder (see parameter **EML_PATH_READY**): EML originals are deleted, ZIP archives are moved. 

**EML_PATH_READY**

A folder for storing the history of letters when they are no longer on the mail server (for example, when they were downloaded from the mail server using the POP3 protocol).
The important letters that are already missing on the mail server are thus still readable if necessary.
Folder is not automatically cleared!
Only **ZIP** archives are stored here.

## General Note
> **Python** string values can be enclosed in quotes:
 
```python

'single'

"double"

'''triple 
    single
'''

"""triple 
    double
"""

```

## How to add a script to Linux cron
To do this, create a **crontab** task that will be executed, for example, every three hours on behalf of the user (creating tasks as root is not the best idea):

Suppose your Linux username is: **user**

Your home folder: **/home/user**

The folder where this script is located: **/home/user/py**

To run the script directly, run the command:
    
    $ chmod +x /home/user/py/check_email.py

Adjust in the first line of the script [Shebang (Unix)](https://en.wikipedia.org/wiki/Shebang_(Unix)), eg:

Show the path where python is located:
    
    $ which python
    $ which python3
    
Correction python path in Shebang:

    #!/usr/bin/python
    #!/usr/bin/python3
    #!/usr/bin/env python
    #!/usr/bin/env python3

Rename script:

    $ mv /home/user/py/check_email.py /home/user/py/check_email

Check script launch:

    $ /home/user/py/check_email
    $ /home/user/py/./check_email

If everything is fine, run the editor **crontab**, if not, go back to setting **Shebang**:

    $ crontab -u user -e
    Here user - is your Linux login

If you, like me, do not like vim (I have not seen a single person who is fluent in this editor, although it probably exists somewhere), you can edit the tasks in your favorite editor, for example:

    $ EDITOR=nano crontab -u user -e
    $ EDITOR=mcedit crontab -u user -e

In the task editor, create something like this:

    0 */3 * * * /home/user/py/check_email >/dev/null 2>&1

or

    0 */3 * * * /home/user/py/./check_email >/dev/null 2>&1    

> Note:
>
> **>/dev/null 2>&1** - suppress output to console or anywhere

or

    # In the process, the script prints service information in the console
    # This information can be redirected to a log file.
    0 */3 * * * /home/user/py/./check_email >> /home/user/py/check_email.log


Specify the full paths to the log file and to the script itself.

Note: [cron](https://en.wikipedia.org/wiki/Cron)

You can view created tasks for user **user** like this:

    $ crontab -u user -l

Delete all tasks from user **user**, you can:

    $ crontab -u user -r

## How to add a script to Microsoft Windows Task Scheduler
Ask for help to [documentation](https://docs.microsoft.com/en-us/windows/desktop/taskschd/schtasks)

**Sample:**

Run a task every midnight:

`schtasks /Create /SC DAILY /TN ""Monitoring importan emails" /TR "'с:\check_email.py'" /ST 23:59`

## Thanks for the idea
[Roskomnadzor](https://rkn.gov.ru/), who now allocates only one day to take action..

## License
[GNU General Public License v3.0](https://choosealicense.com/licenses/gpl-3.0/)

## Restrictions
I, the author of this python script, wrote this script exclusively for my needs. No warranty is provided. You can use this script freely, without any deductions, for any purpose other than those that intentionally lead to [evil](https://en.wikipedia.org/wiki/Evil).

You can make any changes to the script code and fork this script, indicating [me](https://github.com/ak545) as the source of your inspiration.
I'm not conceited, but even the cat likes a good word.

## Postscriptum
- The script was tested in Microsoft Windows 10, Linux Fedora 30, Linux Ubuntu Descktop 18.10, Linux CentOS 6/7, Linux Manjaro 18.0.2.
- Sorry for my bad English.
- The program code of the script is not perfect. But please forgive me for that. At the time of writing this Python script, I have been studying for only one month. I like this programming language, it is much simpler and at the same time more powerful than other programming languages that I own.
- All recommendations given by me for Apple macOS may contain inaccuracies. Sorry, I don’t have an Apple macBook on hand (but what if someone gives it to me?).
- Glory to the E = mc &sup2; !
- I wish you all good luck!

## A final plea
It's time to put an end to Facebook. Working there is not ethically neutral: every day that you go into work, you are doing something wrong. If you have a Facebook account, delete it. If you work at Facebook, quit.

And let us not forget that the National Security Agency must be destroyed.

*(c) [David Fifield](mailto:david@bamsoftware.com)*


---


> Best regards, ak545 ( ru.mail&copy;ak545&sup2; )