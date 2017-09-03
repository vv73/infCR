import requests
from bs4 import BeautifulSoup
import time

import os
import re
from pathlib import Path

from contextlib import closing
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By



def getSubmit(task, lang=None):
    url = 'http://informatics.mccme.ru/mod/statements/view3.php?chapterid=%s&status_id=0&submit' % task
    if lang is not None:
        url = url + '&lang_id=%s' % lang

    with closing(webdriver.Firefox()) as browser:
         submits = browser.get(url)
         try:
             element_present = EC.presence_of_element_located((By.ID, 'Searchresult'))
             WebDriverWait(browser, 300).until(element_present)
             time.sleep(5)
         except TimeoutException:
             print("Timed out waiting for page to load")
             return None
         submits = browser.page_source

    soup = BeautifulSoup(submits, "html.parser")
    table = soup.find('table',['BlueTable'])
    rows = table.findChildren(['tr'])
    if (len(rows) > 1):
        cell = rows[1].findChild('td')
        return cell.string
    else:
        if lang is None:
            return None
        else:
            return getSubmit(task)

def getCaptionAndStatement(task):
    task = str(task)
    url = 'http://informatics.mccme.ru/mod/statements/view3.php?chapterid=%s' % task

    r = requests.get(url)
    soup = BeautifulSoup(r.content, "html.parser")
    caption = soup.find('div', class_='statements_chapter_title')
    caption = re.search(r'\. (.*)\s*$', caption.contents[0]).group(1)
    statement = soup.find('div', class_='problem-statement')
    if not os.path.isdir(task):
        os.mkdir(task)
    with open (task + '\caption.txt', "wt", encoding='utf-8') as f:
        f.write(caption)
    with open(task + '\statement.html', "wt", encoding='utf-8') as f:
        f.write("".join([str(item) for item in statement.contents]))

def getTests(task):
    task = str(task)
    submit = getSubmit(task, 18)
    if submit is None:
        print (task + " ERROR")
        return
    url = 'http://informatics.mccme.ru/py/protocol/get_submit_archive/' + submit.replace('-','/')
    cookies = dict(MoodleSession='o8gsapj3iam7ran3nn1pj68lu5', MoodleSessionTest='E9HElt55Lq', MOODLEID_='%25EA%25C0%2514E%25BD3%25A6%2518')
    r = requests.post(url, cookies=cookies, data = { 'all_tests':'yes', 'sources':'yes'})
    if str(r.content[:2], encoding="utf8") != "PK":
        print(str(r.content, encoding="utf8"))
        r = requests.post(url, cookies=cookies, data={'all_tests': 'yes'})
    with open(task + '/tests.zip', 'wb') as f:
        f.write(r.content)
    import zipfile
    zip_ref = zipfile.ZipFile(task + '/tests.zip', 'r')
    zip_ref.extractall(task)
    zip_ref.close()
    print(task + " ok")

def auth(login, password):
    pass

def getAllTests(folder):
    errors = 0
    tasks = next(os.walk(folder))[1]
    for task in tasks:
        if os.path.isfile(task + ".zip"):
            with open(task + ".zip", 'rb') as fh:
                signature = str(fh.read()[:2], encoding="utf8")
                if signature != "PK":
                    errors += 1
                    print (signature + " " + task + " RETAKE")
                    getTests(task)

        else:
            getTests(task)
    return errors

def getAll(folder):
    errors = 0
    tasks = next(os.walk(folder))[1]
    for task in tasks:
            getCaptionAndStatement(task)

def getTasks(tasklist):
    for task in tasklist:
        print (task)
        if os.path.isdir(task + '/tests'):
            continue
        getCaptionAndStatement(task)
        getTests(task)

os.chdir(r'C:\Users\VV\Desktop\tasks')

#894
#1620
#112628
#116629

contests = """
Задачи к § 56 «Вычисления»
112145 - 112152
Задачи к § 57 «Ветвления»
112156 - 112173
Задачи к § 58 «Циклы»
112202 - 112232
Задачи к § 59 «Процедуры»
112174 - 112188
Задачи к § 60 «Функции»
112189 - 112198, 112201, 112200, 112240
Задачи к § 61 «Рекурсия»
112182 - 112186, 112212, 112213, 112267,112245 - 112266
Задачи к § 62 «Массивы»
112268 - 112288
Задачи к § 63 «Алгоритмы обработки массивов»
112288 - 112312
Задачи к § 64 «Сортировка»
112313 - 112327
Задачи к § 65 «Двоичный поиск»
1 - 4, 111402 - 111404, 111728, 111704, 111734, 111787, 672, 887, 1722, 490, 414, 1923
Задачи к § 66 «Символьные строки»
112336 - 112362
Задачи к § 66 «Символьные строки», часть II
112406 - 112424
Задачи к § 67 «Матрицы»
112363 - 112384, 112389, 112385-112390
Задачи к § 68 «Работа с файлами»
112391 - 112405
Условия задач Задачи к § 38 «Целочисленные алгоритмы»
112450 - 112469
Условия задач Задачи к § 40 «Множества»
112470 - 112481
Условия задач Задачи к § 41 «Динамические массивы»
112482 - 112490
Условия задач Задачи к § 42 «Списки»
112510 - 112515
Условия задач Задачи к § 43 «Стеки, очереди, деки»
112484, 112491 - 112509
Условия задач Задачи к § 44 «Деревья»
757 - 765, 2790, 3556, 3557, 111240
Условия задач Задачи к § 46 «Динамическое программирование»
112601 - 112627
"""
import re
def repl(match):
    s = ""
    for i in range(int(match.group(1)), int(match.group(2)) + 1):
        s += str(i) + " "
    return s
contests = re.sub(r'(\d+) - (\d+)', repl, contests)
contests = re.sub(r',', ' ', contests)
print (contests.split('\n'))
tasklist = re.findall(r'\d+', contests)
print(tasklist)
getTasks(tasklist)

#for i in range (5, 6):
#   getAllCaptions('\\Users\\VV\\Desktop\\21_08_2017\\my-' + str(i))
#errors = -1
#while errors != 0:
#    errors = 0
#    for i in range (5, 6):
#        errors += getAllTests('\\Users\\VV\\Desktop\\21_08_2017\\my-' + str(i))