# Тестовое задание для EVOSOFT
## Описание
Проект состоит из двух парсеров:
- selenium_parcer
- musk_parser
## selenium_parcer:
- ищет информацию на сайте nseindia.com 
- сохраняет ее в csv файл
- имитирует простой пользовательский сценарий
## selenium_parcer:
- ищет и передает текст последних 10 твитов Илона

## Стек технологий
- Python 3.11
- selenium 4.7.0
- selenium-stealth 1.0.6
- selenium-wire 5.1.0
## Запуск проекта
Клонировать репозиторий:
```git clone git@github.com:Glebchik57/parsers_for_EvoSoft.git```

Cоздать и активировать виртуальное окружение:

```python3 -m venv env```

```source env/bin/activate```


```python3 -m pip install --upgrade pip```

Установить зависимости из файла requirements.txt:

```pip install -r requirements.txt```
```
В файле .env необходимо прописать следующие переменные:
```
LOGIN = Логин
PASSWORD = Пароль
IP_ADRESS = Ip адрес для запуска selenium_parser
PORT = Порт для запуска selenium_parser

FR_IP_ADRESS = Ip адрес для запуска musk_parser
FR_PORT = Порт для запуска musk_parser
```
Запустить selenium_parser:
```
python selenium_parser.py
```
Либо musk_parser:
```
python musk_parser.py
```
## Авторы
- [Sevostyanov Gleb](https://github.com/Glebchik57)

**Содержание**

[TOC]

