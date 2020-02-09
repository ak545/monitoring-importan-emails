#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# Program: Monitoring importan emails
#
# Author: Andrey Klimov < ak545 at mail dot ru >
# https://github.com/ak545
#
# Current Version: 0.1.3
# Date: 01-08-2019 (dd-mm-yyyy)
# Last Fix Date: 10-02-2020 (dd-mm-yyyy)
#
# License:
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
#  GNU General Public License for more details.

import os
import sys
from os.path import basename
from pathlib import Path
import imaplib
import requests
import itertools
import re
import zipfile
from datetime import datetime
import smtplib
import ssl
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import email.message
from email.header import decode_header, make_header
from email.mime.application import MIMEApplication
from email import policy
from email.parser import BytesParser

try:
    from colorama import init
    from colorama import Fore, Back, Style
except ImportError:
    sys.exit(
        """You need colorama!
                install it from http://pypi.python.org/pypi/colorama
                or run pip install colorama"""
    )

# Init colorama
init(autoreset=True)

# Глобальные константы
# Global constants
__version__ = '0.1.3'

FR = Fore.RESET
FLW = Fore.LIGHTWHITE_EX
FLG = Fore.LIGHTGREEN_EX
FLR = Fore.LIGHTRED_EX
FLC = Fore.LIGHTCYAN_EX
FLY = Fore.LIGHTYELLOW_EX
FLM = Fore.LIGHTMAGENTA_EX
FLB = Fore.LIGHTBLUE_EX

BLB = Back.LIGHTBLACK_EX
BR = Back.RESET

SDIM = Style.DIM
SNORMAL = Style.NORMAL
SBRIGHT = Style.BRIGHT
SR = Style.RESET_ALL

REQUEST_HEADERS = {
    'Content-Type': 'application/x-www-form-urlencoded; charset=UTF-8',
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_0) AppleWebKit/537.36 (KHTML, like Gecko) '
                  'Chrome/69.0.3497.57 Safari/537.36',
}

# SMTP параметры
# SMTP options
SMTP_SERVER = 'localhost'
SMTP_PORT = 25
SMTP_SSL = False
SMTP_STARTTLS = False

# SMTP_SERVER = 'smtp.gmail.com'
# SMTP_PORT = 587
# SMTP_SSL = False
# SMTP_STARTTLS = True

# SMTP_SERVER = 'smtp.yandex.ru'
# SMTP_PORT = 465
# SMTP_SSL = True
# SMTP_STARTTLS = False

SMTP_SENDER = 'root'
SMTP_PASSWORD = 'password'

# Параметры для подключения к почтовому серверу
# Parameters for connecting to the mail server
CONTROLLED_EMAIL_SERVER = 'mx.example.com'
CONTROLLED_EMAIL_ADDRESSES = 'public@example.com'
CONTROLLED_EMAIL_ADDRESSES_PASSWORD = 'password'

# Список получателей E-mail и Telegram уведолений
# List of E-mail and Telegram Recipients
RECIPIENTS_FULL = {
    # E-mail адрес получателя уведомлений
    # E-mail address of the recipient of notifications
    'alisa@example.com': [
        # Имя получателя уведомлений
        # Notification Recipient Name
        'Alisa',

        # Адреса (и фрагменты адресов) входящих писем по которым
        # не отсылаются уведомления для этого получателя

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
            '@rkn.gov.ru',
            '@mvd.ru',
        ]
    ],
    'moderator@example.com': [
        'Moderator',
        [
            'domain@example.com',
            '@rkn.gov.ru',
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

# Список email-адресов (или фрагментов таких адресов) при наличии
# которых отправляем уведомления в Telegram-чат и на email-почту
# определённым получателям из списка RECIPIENTS_FULL

# A list of email addresses (or fragments of such addresses) in the
# presence of which we send notifications to Telegram-chat and to
# email-mail to certain recipients from the RECIPIENTS_FULL list
CONTROLLED_EMAIL_ADDRESSES_SENDERS = [
    'alisa@example.com',
    'bob@example.com',
    'abuse@example.com',
    'admin@example.com',
    'domain@example.com',
    '@rkn.gov.ru',
    '@mvd.ru',
]

# Опции для Telegram бота
# Telegram bot options
TELEGRAM_PROXIES = {}
# TELEGRAM_PROXIES = {
#     'http': 'socks5://127.0.0.1:9150',
#     'https': 'socks5://127.0.0.1:9150',
# }

# Токен Telegram-бота
# Получить помощь по регистрации Telegram бота
# можно здесь:  https://core.telegram.org/bots,
# а так же общаясь с @BotFather в Telegram.

# Telegram bot token
# You can get help with Telegram bot registration
# here: https://core.telegram.org/bots,
# as well as talking to @BotFather in Telegram.
TELEGRAM_MY_TOKEN = '<INSERT YOUR TOKEN>'

# Идентификатор Telegram-канала
# ID of the Telegram channel
TELEGRAM_CHAT_ID = '<INSERT YOUR CHANNEL ID>'

# URL для запросов на api.telegram.org
# URL for api.telegram.org requests
TELEGRAM_URL = 'https://api.telegram.org/bot' + TELEGRAM_MY_TOKEN + '/'

SEP = os.sep
pathname = os.path.dirname(sys.argv[0]).rstrip(SEP)

# Папка для хранения актуального кэша писем.
# По этому кэшу определяется, отправлялось
# ли ранее уже уведомление.
# Эта папка автоматически очищается при каждой новой проверке:
# Письма, которых уже нет на сервере перемещаются в папку истории
# (EML-файлы удаляются, ZIP-файлы перемещаются).

# Folder for storing the current letter cache. This cache is used
# to determine whether the notification has been sent before.
# This folder is automatically cleared for each new check:
# Mails that are no longer on the server are moved to the
# history folder (EML files are deleted, ZIP files are moved).
EML_PATH = pathname + SEP + 'data' + SEP

# Папка для хранения истории писем, когда их уже нет на сервере
# (например, когда их скачали с почтового сервера по протоколу
# POP3 с удалением оригиналов с сервера).
# Уже отсутствующие на сервере важные письма, таким образом,
# всё ещё можно при острой необходимости прочитать.
# Папка автоматически не очищается!
# Здесь хранятся только ZIP-файлы.

# Folder for storing the history of letters when they are no
# longer on the server (for example, when they were downloaded
# from the mail server via POP3 protocol with removal of originals
# from the server). Already absent on a server the important letters,
# thus, it is still possible at an acute necessity to read.
# The folder is not automatically cleared! Only ZIP-files
# are stored here.
EML_PATH_READY = pathname + SEP + 'data' + SEP + 'ready' + SEP


def sanitize_filename(s, restricted=False, is_id=False):
    """
    Изменяет строку (s) так, чтобы её можно было использовать,
    как часть имени файла.
    Параметр restricted изменит строку на основании более
    строгого подмножества разрешенных для файловой системы
    символов (accent_chars).
    Параметр is_id позволяет не изменять идентификаторы
    (если это возможно).

    Modifies the string (s) so that it can be used as part of
    the file name.
    The restricted parameter will change the string based on
    a more strict subset of the allowed characters (accent_chars)
    for the file system.
    The is_id parameter allows not to change identifiers
    (if possible).

    :param s: string
    :param restricted: bool
    :param is_id: bool
    :return: string
    """

    def replace_insane(char):
        accent_chars = dict(zip('ÂÃÄÀÁÅÆÇÈÉÊËÌÍÎÏÐÑÒÓÔÕÖŐØŒÙÚÛÜŰÝÞßàáâãäåæçèéêëìíîïðñò'
                                'óôõöőøœùúûüűýþÿ',
                                itertools.chain(
                                    'AAAAAA',
                                    ['AE'],
                                    'CEEEEIIIIDNOOOOOOO',
                                    ['OE'],
                                    'UUUUUYP',
                                    ['ss'],
                                    'aaaaaa',
                                    ['ae'],
                                    'ceeeeiiiionooooooo',
                                    ['oe'],
                                    'uuuuuypy'
                                )))
        if restricted and char in accent_chars:
            return accent_chars[char]
        if char == '?' or ord(char) < 32 or ord(char) == 127:
            return ''
        elif char == '"':
            return '' if restricted else '\''
        elif char == ':':
            return '_-' if restricted else ' -'
        elif char in '\\/|*<>':
            return '_'
        if restricted and (char in '!&\'()[]{}$;`^,#' or char.isspace()):
            return '_'
        if restricted and ord(char) > 127:
            return '_'
        return char

    # Handle timestamps
    s = re.sub(r'[0-9]+(?::[0-9]+)+',
               lambda m: m.group(0).replace(':', '_'), s)
    result = ''.join(map(replace_insane, s))
    if not is_id:
        while '__' in result:
            result = result.replace('__', '_')
        result = result.strip('_')
        # Common case of "Foreign band name - English song title"
        if restricted and result.startswith('-_'):
            result = result[2:]
        if result.startswith('-'):
            result = '_' + result[len('-'):]
        result = result.lstrip('.')
        if not result:
            result = '_'
    return result


def send_telegram(text: str, date_time: str = None) -> str:
    """
    Отправка сообщения в Telegram-чат через Telegram-бота
    Sending a message to a Telegram chat via a Telegram bot
    :param text: str
    :param date_time: str
    :return: str
    """
    if date_time:
        today = date_time
    else:
        today = '{:%d.%m.%Y %H:%M:%S}'.format(datetime.now())
    # today = 'Date and time of discovery: ' + today
    today = 'Дата и время обнаружения: ' + today

    hl = '{:-<8}'.format('')

    message = ''
    fix_text = text.replace('<', '&lt;').replace('>', '&gt;')

    # message += '\n☢ <b>An important letter was found!</b><pre>' + today + '\n'
    message += '\n☢ <b>Обнаружено важное письмо!</b><pre>' + today + '\n'
    message += hl + '\n'
    message += fix_text
    message += '</pre>\n'
    if message != '':
        message += '\n'

    params = {'chat_id': TELEGRAM_CHAT_ID, 'parse_mode': 'html', 'text': message}

    if len(TELEGRAM_PROXIES) > 0:
        response = requests.post(TELEGRAM_URL + 'sendMessage', data=params, proxies=TELEGRAM_PROXIES,
                                 headers=REQUEST_HEADERS)
    else:
        response = requests.post(TELEGRAM_URL + 'sendMessage', data=params,
                                 headers=REQUEST_HEADERS)

    return response


def send_email(message, recipient, attached_file=None, date_time=None, subject=None):
    """
    Отправка e-mail получателю
    Sending a email to the recipient
    :param message: str
    :param recipient: list
    :param attached_file: str
    :param date_time: str
    :param subject: str
    :return: None
    """
    msg_mime = MIMEMultipart('alternative')
    msg_mime['From'] = SMTP_SENDER
    msg_mime['To'] = recipient[1] + ' <' + recipient[0] + '>'
    if subject:
        # msg_mime['Subject'] = 'An important letter was found: [ ' + str(subject).strip() + ' ]'
        msg_mime['Subject'] = 'Обнаружено важное письмо: [ ' + str(subject).strip() + ' ]'
    else:
        # msg_mime['Subject'] = 'An important letter was found!'
        msg_mime['Subject'] = 'Обнаружено важное письмо!'

    body_text = '%BODY%'
    body_html = """\
    <!DOCTYPE HTML PUBLIC "-//W3C//DTD HTML 4.01 Transitional//EN" "http://www.w3.org/TR/html4/loose.dtd">
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=UTF-8" />
    </head>
    <html>
      <body marginwidth="0" \
      marginheight="0" leftmargin="0" topmargin="0" style="background-color:#F6F6F6; \
      font-family:Arial,serif; margin:0; padding:0; min-width: 100%; \
      -webkit-text-size-adjust:none; -ms-text-size-adjust:none;">
        <div style="width: auto; color:#000; background-color: #F4F5F7; \
        padding: 50px; display: inline-block;">
        %BODY%
        </div>
      </body>
    </html>
    """

    if date_time:
        today = date_time
    else:
        today = '{:%d.%m.%Y %H:%M:%S}'.format(datetime.now())
    # today = 'Date and time of discovery: ' + today
    today = 'Дата и время обнаружения: ' + today

    hl = '{:-<8}'.format('')

    eml_text = ''
    if attached_file:
        if Path(attached_file).is_file():
            with open(attached_file, 'rb+') as file:
                eml_msg = BytesParser(policy=policy.default).parse(file)
            eml_text_b = eml_msg.get_body()
            if eml_text_b:
                eml_text = eml_text_b.get_content()
                if eml_text:
                    eml_text = re.sub(r'<br.*?>', '\n', eml_text)
                    eml_text = re.sub(r'<.*?>', '', eml_text)
                    eml_text = str(eml_text).strip()

    # Для простой части
    # For part plain
    b_txt = ''
    # b_txt += '\nAn important letter was found!\n'
    b_txt += '\nОбнаружено важное письмо!\n'
    b_txt += today + '\n'
    b_txt += hl + '\n'
    b_txt += message.rstrip('\n') + '\n'
    b_txt += hl + '\n'
    # b_txt += 'The text of the original message:\n'
    b_txt += 'Текст оригинального сообщения:\n'
    b_txt += hl + '\n'
    b_txt += eml_text + '\n'
    body_text = body_text.replace('%BODY%', b_txt)

    # Для html части
    # For part html
    b_html = ''
    # b_html += '<br><b>An important letter was found!</b><br>'
    b_html += '<br><b>Обнаружено важное письмо!</b><br>'
    b_html += '<pre style="white-space: pre-wrap; word-wrap: break-word;">'
    b_html += today + '\n'
    b_html += hl + '\n'
    b_html += message.rstrip('\n') + '\n'
    b_html += hl + '\n'
    # b_html += 'The text of the original message:\n'
    b_html += 'Текст оригинального сообщения:\n'
    b_html += hl + '\n'
    b_html += eml_text + '\n'
    b_html += '</pre>'
    body_html = body_html.replace('%BODY%', b_html)

    part_plain = MIMEText(body_text, 'plain')
    part_html = MIMEText(body_html, 'html')

    msg_mime.attach(part_plain)
    msg_mime.attach(part_html)

    if attached_file:
        if Path(attached_file).is_file():
            eml_zipfile = Path(attached_file)
            eml_zipfile = eml_zipfile.with_suffix('.zip')

            if not Path(eml_zipfile).is_file():
                with zipfile.ZipFile(eml_zipfile, 'w', zipfile.ZIP_DEFLATED) as zipf:
                    zipf.write(attached_file, basename(attached_file))

            with open(eml_zipfile, 'rb+') as file:
                eml_part = MIMEApplication(
                    file.read(),
                    Name=basename(eml_zipfile)
                )

            if Path(eml_zipfile).is_file():
                # print(f'\nEmail is sent      : {FLG}{recipient[0]} ({recipient[1]}){FR}\n'
                #       f'The attachment     : {FLG}{basename(eml_zipfile)} ({basename(attached_file)})')
                print(f'\nОтправляется письмо: {FLG}{recipient[0]} ({recipient[1]}){FR}\n'
                      f'Вложение           : {FLG}{basename(eml_zipfile)} ({basename(attached_file)})')
                print('{:-<80}'.format(''))
                eml_part['Content-Disposition'] = 'attachment; filename="%s"' % basename(eml_zipfile)
                msg_mime.attach(eml_part)

    summary_message = msg_mime.as_string()

    server = None
    context = None
    # Пробуем подключиться к SMTP-серверу для отправки email
    # Try to connect to the SMTP server to send email
    try:
        if SMTP_SSL or SMTP_STARTTLS:
            # Если используется SSL или STARTTLS
            # If using SSL or STARTTLS

            # Создать безопасный SSL-контекст
            # Create a secure SSL context
            context = ssl.create_default_context()

            if SMTP_SSL:
                # Если используется SSL
                # If using SSL
                server = smtplib.SMTP_SSL(
                    host=SMTP_SERVER, port=SMTP_PORT, context=context)
        else:
            # Если используется обычное подключение
            # If using normal connection
            server = smtplib.SMTP(SMTP_SERVER, SMTP_PORT)
            server.ehlo()

        if SMTP_STARTTLS:
            # Если используется STARTTLS
            # If STARTTLS is used

            # Безопасное соединение
            # Secure the connection
            server.starttls(context=context)
            server.ehlo()

        server.login(SMTP_SENDER, SMTP_PASSWORD)
        server.sendmail(SMTP_SENDER, recipient[0], summary_message)
    except Exception as e:
        # Печать любых сообщения об ошибках на стандартный вывод
        # Print any error messages to stdout
        print(f'{FLR}{e}')
    finally:
        server.quit()


def main():
    try:
        Path(EML_PATH).mkdir(parents=True, exist_ok=True)
    except:
        # print(f'Error creating folder: {FLR}{EML_PATH}')
        print(f'Ошибка создания папки: {FLR}{EML_PATH}')
        sys.exit(-1)

    try:
        Path(EML_PATH_READY).mkdir(parents=True, exist_ok=True)
    except:
        # print(f'Error creating folder: {FLR}{EML_PATH_READY}')
        print(f'Ошибка создания папки: {FLR}{EML_PATH_READY}')
        sys.exit(-1)

    letters_on_the_server_list = []
    letters_on_the_cache_list = []

    # Создать список файлов в кэше
    # Create Cached File List
    for (_, _, filenames) in os.walk(EML_PATH):
        for i in filenames:
            filename, file_extension = os.path.splitext(i)
            if '.eml' in file_extension:
                letters_on_the_cache_list.append(filename)
        break

    # Начало...
    # Begin...

    # Подключение к IMAP4 серверу
    # Connect to IMAP4 server
    mail = imaplib.IMAP4_SSL(CONTROLLED_EMAIL_SERVER)
    try:
        r, data = mail.login(CONTROLLED_EMAIL_ADDRESSES, CONTROLLED_EMAIL_ADDRESSES_PASSWORD)
        if r != "OK":
            str_e = str(data)
            str_e = str_e.strip("b'").strip("'")
            # print(f'{FLR}Error login        : {str_e}')
            print(f'{FLR}Ошибка подключения : {str_e}')
    except (imaplib.IMAP4.error, OSError) as e:
        str_e = str(e)
        str_e = str_e.strip("b'").strip("'")
        # print(f'{FLR}Error login        : {str_e}')
        print(f'{FLR}Ошибка подключения : {str_e}')
        sys.exit(-1)

    # Получить список каталогов "INBOX", "Sent", и т.п.
    # Get the list of catalogs "INBOX", "Sent", etc.
    mail.list()

    # Переходим в папку INBOX
    # Go to the INBOX folder
    _, select_data = mail.select('INBOX')
    select_data[0].decode('utf-8')

    # Получить список id писем через пробел
    # Get the list id of letters through a space
    _, data = mail.search(None, 'ALL')
    ids = data[0]
    id_list = ids.split()
    count = len(id_list)

    print(f'{SR}')
    print('{:-<80}'.format(''))
    # print(f'Start scan         : {FLC}{"{:%d.%m.%Y %H:%M:%S}".format(datetime.now())}')
    print(f'Начало сканирования: {FLC}{"{:%d.%m.%Y %H:%M:%S}".format(datetime.now())}')
    # print(f'Total letters      : {FLG}{count}')
    print(f'Всего писем        : {FLG}{count}')
    print('{:-<80}'.format(''))

    count_found = 0

    if count > 0:
        # Анализ имеющихся писем
        # Analysis of available letters
        for item in id_list:
            email_id = item.decode('utf-8').strip()
            
            if email_id == '':
                continue

            # Получить письмо
            # Флаг "Невидимый" не сбрасывается
            # Get a letter
            # "Unseen" flag is not reset
            _, data = mail.fetch(email_id, '(BODY.PEEK[])')

            # Необработанное содержимое письма
            # Raw message content
            raw_email = data[0][1]

            # Парсинг содержимого письма
            # Parsing the contents of the letter
            msg = email.message_from_bytes(
                      raw_email,
                      _class=email.message.EmailMessage
                  )

            # Получить дату письма
            # Get the date of the letter
            str_date = ''
            if msg['Date'] is not None:
                timestamp = email.utils.parsedate_tz(msg['Date'])
                year, month, day, hour, minute, second = timestamp[:6]

                str_date = '{0:02d}.'.format(day)
                str_date += '{0:02d}.'.format(month)
                str_date += '{0:04d} '.format(year)
                str_date += '{0:02d}:'.format(hour)
                str_date += '{0:02d}:'.format(minute)
                str_date += '{0:02d}'.format(second)

            # Получить адрес отправителя письма
            # Get the sender address
            msg_from_decoded = ''
            if msg['From'] is not None:
                str_from = str(msg["From"])
                if '=?' in str_from.strip():
                    msg_from_decoded = str(
                        make_header(decode_header(str_from))
                    )
                else:
                    msg_from_decoded = str_from

                msg_from_decoded = (
                    msg_from_decoded
                    .replace("\n", "")
                    .replace("\r", "")
                    .replace("\t", "")
                    .strip()
                )

            # Получить декодированную тему письма
            # Get a decoded letter subject
            subj = ""
            if msg["Subject"]:
                str_subj = str(msg["Subject"])
                if '=?' in str_subj.strip():
                    subj = str(make_header(
                        decode_header(str_subj))
                    )
                else:
                    subj = str_subj

                subj = (
                    subj
                    .replace("\n", "")
                    .replace("\r", "")
                    .replace("\t", "")
                    .strip()
                )

            # Анализ данных письма
            # Analysis of the letter data
            is_important_letter = False
            for control_email in CONTROLLED_EMAIL_ADDRESSES_SENDERS:
                # Является ли письмо важным?
                # (проверяем, имеется ли адрес отправителя или фрагмент
                # адреса отправителя в списке отслеживаемых важных
                # писем CONTROLLED_EMAIL_ADDRESSES_SENDERS)

                # Is the letter important?
                # (check if the sender's address or the fragment of the
                # sender's address is in the list of monitored important
                # letters CONTROLLED_EMAIL_ADDRESSES_SENDERS)
                if control_email in msg_from_decoded:
                    # Если да, устнавливаем флаг важности письма
                    # If yes, set the letter importance flag
                    is_important_letter = True
                    break

            if is_important_letter:
                # Если письмо ВАЖНОЕ
                # If the letter is IMPORTANT

                # Дата и время обнаружения
                # Date and time of discovery
                date_time_discovery = '{:%d.%m.%Y %H:%M:%S}'.format(datetime.now())

                count_found += 1

                # Установить флаг "Уведомления уже отправлялись"
                # Set the flag "Notifications have already been sent"
                is_notifications_have_already_been_sent = True

                # Message-ID письма
                # Message-ID of the letter
                str_domain = msg_from_decoded.split('@')[-1].strip('>').strip()
                message_id = f'{str_date.replace(":", ".")}@{str_domain}'
                message_id = sanitize_filename(message_id)

                print(f'From               : {FLG}{msg_from_decoded}')
                print(f'Date               : {FLG}{str_date}')
                print(f'Subject            : {FLG}{subj}')

                # Добавить ID письма в список "письма на сервере"
                # Add letter ID to the list of "letters on the server"
                letters_on_the_server_list.append(message_id)

                # Сохранить оригинал письма в .EML формате в
                # папку кэша (если его там ещё нет)
                # Save the original letter in .EML format to
                # the cache folder (if it is not already there)
                eml_file = EML_PATH + message_id + '.eml'

                if not Path(eml_file).is_file():
                    # Сбросить флаг "Уведомления уже отправлялись"
                    # Unset the flag "Notifications have already been sent"
                    is_notifications_have_already_been_sent = False

                    # Сохранить оригинал письма в формате .EML в
                    # папке кэша
                    # Save the original letter in the .EML format in
                    # the cache folder
                    with open(eml_file, 'wb+') as file:
                        file.write(raw_email)

                    # Добавить ID письма в список "письма в кэше"
                    # Add letter ID to the list "letters on the cache"
                    letters_on_the_cache_list.append(message_id)

                if is_notifications_have_already_been_sent:
                    # Если уведомления уже отправлялись,
                    # повторно получателей не уведомлять
                    # If notifications have already been sent,
                    # do not notify recipients again
                    # print(f'\nSkipped            : {FLY}{message_id}{FR}\n'
                    #       f'Cause              : {FLY}Notifications for '
                    #       f'this email have already been sent')
                    print(f'\nПропускается       : {FLY}{message_id}{FR}\n'
                          f'Причина            : {FLY}Уведомления по этому '
                          f'письму ранее уже отправлялись')
                    print('{:-<80}'.format(''))
                    continue

                warning_msg = f'From   : {msg_from_decoded}\n'
                warning_msg += f'Date   : {str_date}\n'
                warning_msg += f'Subject: {subj}\n'

                email_msg = warning_msg

                if Path(eml_file).is_file():
                    # Читать сырой текст оригинального
                    # письма из файла в кэше
                    # Read the raw text of the original
                    # letter from the file in the cache
                    with open(eml_file, 'rb+') as file:
                        eml_msg = BytesParser(policy=policy.default).parse(file)

                    # Конвертировать сырой текст письма в читаемый текст
                    # Convert raw letter text to readable text
                    eml_text_part = ''
                    eml_text_part_b = eml_msg.get_body()
                    if eml_text_part_b is not None:
                        eml_text_part = eml_text_part_b.get_content()
                        if eml_text_part is not None:
                            eml_text_part = re.sub(r'<br.*?>', '\n', eml_text_part)
                            eml_text_part = re.sub(r'<.*?>', '', eml_text_part)

                            # Ограничить длину текста (для показа только
                            # фрагмента текста в Telegram-чате)
                            # Limit the length of the text (to display only
                            # a fragment of the text in the Telegram-chat)
                            eml_text_part = str(eml_text_part)[:142].strip()

                    if eml_text_part is not None and eml_text_part != '':
                        warning_msg += '{:-<8}\n'.format('')
                        # warning_msg += 'Summary           :\n'
                        warning_msg += 'Краткое содержание:\n'
                        warning_msg += '{:-<8}\n'.format('')
                        warning_msg += eml_text_part + '...\n'

                warning_msg += '{:-<8}\n'.format('')
                # warning_msg += 'This event applies to all!\n'
                # warning_msg += 'See the full text of the letter in your email.'
                warning_msg += 'Это событие касается всех!\n'
                warning_msg += 'Полный текст письма смотрите в своей почте.'

                # Установить флаг "Отправить полное telegram-уведомление"
                # Set the flag "Send full telegram notification"
                is_send_full_telegram_notification = True

                # Обнулить список получателей для
                # полного Telegram-уведомления
                # Zero the list of recipients for
                # a full Telegram notification
                recepints_for_full_telegram_notification_list = []

                # Обнулить список получателей для
                # неполного Telegram-уведомления
                # Zero the list of recipients for
                # incomplete Telegram notifications
                recepints_for_incomplete_telegram_notification_list = []

                # Отправка персональных Email-уведомлениий получателям
                # Send personal email notifications to recipients
                for recipient_data in RECIPIENTS_FULL.items():
                    # Email получателя
                    # Email of recipient
                    recepient_email = recipient_data[0]

                    # Имя получателя
                    # Name of recipient
                    recepient_name = recipient_data[1][0]

                    if recepient_name.strip() == '':
                        # Если имя получателя отсутствует
                        # If the recipient's name is missing
                        # recepient_name = 'Unknown'
                        recepient_name = 'Вася Пупкин'

                    # Список адресов входящих писем или их фрагментов,
                    # запрещенных для этого получателя
                    # The list of addresses of incoming letters or their
                    # fragments prohibited for this recipient
                    prohibited_email_list = recipient_data[1][1]

                    # Находится ли данное письмо в списке адресов входящих
                    # писем, запрещённых для этого получателя?
                    # Is this letter in the list of addresses of incoming
                    # emails prohibited for this recipient?
                    is_prohibited = False
                    prohibited_part = ''
                    for prohibited_email in prohibited_email_list:
                        if prohibited_email in msg_from_decoded:
                            is_prohibited = True
                            prohibited_part = prohibited_email
                            break

                    # Создать список получателя для def send_email()
                    # Create a recipient list for def send_email ()
                    # to_list[0] - email получателя, email of recipient
                    # to_list[1] - имя получателя, name of recipient
                    to_list = [recepient_email, recepient_name]

                    if not is_prohibited:
                        # По этому письму для данного получателя МОЖНО
                        # отправить Email уведомление
                        # By this letter for this recipient you can
                        # send an email notification

                        # Отправить email-уведомление получателю
                        # Send email to recipient
                        send_email(email_msg, to_list, attached_file=eml_file,
                                   date_time=date_time_discovery, subject=subj)

                        # Добаить имя получателя в список получателей
                        # полного уведомления в Telegram-чате
                        # Add the recipient name to the list of recipients
                        # of the full notification in the Telegram chat
                        recepints_for_full_telegram_notification_list.append(to_list[1])
                    else:
                        # По этому письму для данного получателя ЗАПРЕЩЕНО
                        # отправить Email уведомление
                        # For this recipient, it is FORBIDDEN
                        # to send an Email Notification

                        # Добавить имя получателя в список получателей
                        # неполного уведомления в Telegram-чате
                        # Add recipient name to the list of recipients
                        # of incomplete notification in Telegram chat
                        recepints_for_incomplete_telegram_notification_list.append(to_list[1])

                        # Сбросить флаг "Отправить полное telegram-уведомление"
                        # Unset the flag "Send full telegram notification"
                        is_send_full_telegram_notification = False
                        # print(f'\nSkipped letter     : {FLR}{to_list[0]} ({to_list[1]}){FR}\n'
                        #       f'Cause              : Incoming letter {FLG}{msg_from_decoded}{FR} '
                        #       f'is in the list of prohibited '
                        #       f'for this recipient ({FLR}{prohibited_part}{FR})')
                        print(f'\nПропускается письмо: {FLR}{to_list[0]} ({to_list[1]}){FR}\n'
                              f'Причина            : Входящее письмо {FLG}{msg_from_decoded}{FR} '
                              f'находится в списке запрещённых для '
                              f'этого получателя ({FLR}{prohibited_part}{FR})')
                        print('{:-<80}'.format(''))

                # Отправка общего уведомления в Telegram-чат
                # Sending general notification to Telegram chat
                if is_send_full_telegram_notification:
                    # Отправка полного уведомления в Telegram-чат
                    # Sending full notification to Telegram chat
                    send_telegram(warning_msg, date_time=date_time_discovery)
                else:
                    # Отправка неполного уведомления в Telegram-чат
                    # Sending an incomplete notification to Telegram chat
                    warning_msg = ''
                    for name in recepints_for_full_telegram_notification_list:
                        warning_msg += name + '\n'
                    warning_msg += '{:-<8}\n'.format('')
                    # warning_msg += 'This event is only for recipients listed above!\n'
                    # warning_msg += 'E-mail notification has been sent to all of you.\n'
                    # warning_msg += 'The full text of the letter can be viewed in your email.\n'
                    warning_msg += 'Это событие только для получателей, перечисленных выше!\n'
                    warning_msg += 'Всем вам отправлено уведомление по e-mail.\n'
                    warning_msg += 'Полный текст письма можно посмотреть в своей почте.\n'

                    warning_msg += '\n{:-<8}\n'.format('')

                    # Добавить в Telegram-уведомление имена получателей,
                    # которых данное письмо не касается
                    # Add to the Telegram-notification the names of recipients
                    # whom this letter does not concern.
                    for name in recepints_for_incomplete_telegram_notification_list:
                        warning_msg += name + '\n'

                    warning_msg += '{:-<8}\n'.format('')
                    # warning_msg += 'This event has nothing to do with you.!'
                    warning_msg += 'Это событие не имеет к вам ' \
                                   'никакого отношения!'

                    # Отправка неполного уведомления в Telegram-чат
                    # Sending an incomplete notification to Telegram chat
                    send_telegram(warning_msg, date_time=date_time_discovery)

        mail.close()

    # Отключение от IMA4-сервера
    # Disconnect from IMA4 server
    mail.logout()

    # Подчистить по необходимости кэш
    # Clean up by need cache
    for id_on_the_cache in letters_on_the_cache_list:
        if id_on_the_cache not in letters_on_the_server_list:
            # Если письмо находится в кэше, но на IMA4-сервере
            # в папке "INBOX" его уже нет
            # If the message is in the cache, but on the
            # IMA4 server in the "INBOX" folder it is no longer there

            # EML-файл, подлежащий удалению из кэша
            # EML file to be removed from the cache
            f_eml_src = EML_PATH + id_on_the_cache + '.eml'

            # ZIP-файл, подлежащий перемещению в папку истории
            # ZIP file to be moved to the history folder
            f_zip_src = EML_PATH + id_on_the_cache + '.zip'
            f_zip_dst = EML_PATH_READY + id_on_the_cache + '.zip'

            try:
                # Удаление EML-файла из кэша
                # Remove EML file from cache
                # print(f'Remove             : {f_eml_src}')
                print(f'Удаление           : {f_eml_src}')
                if os.path.isfile(f_eml_src):
                    os.remove(f_eml_src)
            except OSError as e:
                # print(f'Error deleting file {FLR}{f_eml_src}')
                print(f'Ошибка удаления файла {FLR}{f_eml_src}')
                print(f'{FLR}{e.filename}{FR}: {FLR}{e.strerror}')
                sys.exit(-1)

            try:
                # Перемещение ZIP-файла в папку истории (ready)
                # Move the ZIP file to the history folder (ready)
                # print(f'Move               : {f_zip_src} в {f_zip_dst}')
                print(f'Перемещение        : {f_zip_src} в {f_zip_dst}')
                if os.path.isfile(f_zip_src):
                    os.rename(f_zip_src, f_zip_dst)
            except OSError as e:
                # print(f'Error moving file {FLR}{f_zip_src}{FR} в {FLR}{f_zip_dst}')
                print(f'Ошибка перемещения файла {FLR}{f_zip_src}{FR} в {FLR}{f_zip_dst}')
                print(f'{FLR}{e.filename}{FR}: {FLR}{e.strerror}')
                sys.exit(-1)

    # Печать статистики
    # Printing statistics
    if count_found > 0:
        print('\n{:-<80}'.format(''))

    # print(f'Total important    : {FLG}{count_found}')
    # print(f'End of scan        : {FLC}{"{:%d.%m.%Y %H:%M:%S}".format(datetime.now())}')
    print(f'Из них важных      : {FLG}{count_found}')
    print(f'Конец сканирования : {FLC}{"{:%d.%m.%Y %H:%M:%S}".format(datetime.now())}')
    print('{:-<80}\n'.format(''))
    print(f'{SR}')

    # Конец ¯\_(ツ)_/¯
    # End ༼ つ ◕_◕ ༽つ


if __name__ == '__main__':
    # Check Python Version
    if sys.version_info < (3, 6):
        print('Error. Python version 3.6 and above required')
        sys.exit(-1)

    main()
    sys.exit(0)
