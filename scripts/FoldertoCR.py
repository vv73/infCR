# coding: utf8
import os
from pathlib import Path
import re
import sys
import codecs


def printHeader(title):
    outputFile.write("""<?xml version="1.0" encoding="UTF-8"?>
<quiz>
<!-- question: 0  -->
  <question type="category">
    <category>
        <text>$course$/%s</text>

    </category>
  </question>
  """%title)


def printFooter():
    outputFile.write("\n</quiz>")


def printTask(task):
    bad = False
    if not os.path.isfile(task + "/statement.html"):
        print (task + " NO STATEMENT")
    if not os.path.isfile(task + "/caption.txt"):
        print (task + " NO CAPTION")
        caption = task
    else:
        caption = codecs.open(task +'/caption.txt', 'r', encoding='utf8').read()
    if not os.path.isdir(task + "/tests"):
        print(task + " NO TESTS FOLDER")
        bad = True
    else:
        if not os.path.isfile(task + "/tests/01.a"):
            print(task + " NO TESTS")
            bad = True
    if (bad):
        return



    outputFile.write("""<question type="coderunner">
    <name>
      <text>{0}</text>
    </name>
    """.format(str(task)+'. '+caption))

    outputFile.write("<questiontext format=\"html\"><text><![CDATA[")

    outputFile.write('<H1>' + caption + '</H1>\n')
    outputFile.write("<a href=http://informatics.mccme.ru/mod/statements/view3.php?chapterid={0}>{0} на informatics</a>\n".format(task))
    #outputFile.write(Path("./preambula.html").read_text())
    with codecs.open(task + "/statement.html", 'r', encoding='utf8') as f:
        statement = f.read().replace("<span class=\"tex-span\">", "").replace("</span>", "").replace('\n', ' ').replace('\r', '')

    import re
    m = re.search(r'(.*)<div class="section-title">Примеры', statement)
    if m is not None:
        outputFile.write(m.group(1))
    else:
        outputFile.write(statement)
    import fnmatch
    solutions = fnmatch.filter(os.listdir(task), '*.java')
    if (len(solutions)>0):
        with codecs.open(task + "/" + solutions[0], 'r', encoding='utf8') as f:
            solution = f.read()
    else:
        solution = ''

    outputFile.write("""]]></text>
    </questiontext>
    <generalfeedback format="html">
      <text></text>
    </generalfeedback>
    <defaultgrade>1.0000000</defaultgrade>
    <penalty>0.3333333</penalty>
    <hidden>0</hidden>
    <coderunnertype>java_program</coderunnertype>
    <prototypetype>0</prototypetype>
    <allornothing>1</allornothing>
    <penaltyregime>0,0,0,5,10,...</penaltyregime>
    <showsource>0</showsource>
    <answerboxlines>18</answerboxlines>
    <answerboxcolumns>100</answerboxcolumns>
    <useace>1</useace>
    <resultcolumns></resultcolumns>
    <answer><![CDATA[%s]]></answer>
    <combinatortemplate></combinatortemplate>
    <testsplitterre></testsplitterre>
    <enablecombinator></enablecombinator>
    <pertesttemplate></pertesttemplate>
    <language></language>
    <acelang></acelang>
    <sandbox></sandbox>
    <grader></grader>
    <cputimelimitsecs></cputimelimitsecs>
    <memlimitmb></memlimitmb>
    <sandboxparams><![CDATA[{"interpreterargs":["-Xrs", "-Xss24m", "-Xmx200m", "-Djava.security.manager"]}]]></sandboxparams>
    <templateparams></templateparams>

    <testcases>
    """%solution)
    tests = next(os.walk(task + '/tests'))[2]
    i = 0
    for test in tests:
        if re.match("^[0-9]+$", test) is None or i > 100:
            continue
        with codecs.open(task + "/tests/" + test, 'r', encoding='utf8') as f:
            inp = f.read()
        with codecs.open(task + "/tests/" + test + ".a", 'r', encoding='utf8') as f:
            ans = f.read()

        if len(inp) > 10000 or len(ans) > 10000:
            continue
        outputFile.write("""<testcase useasexample="{0}" hiderestiffail="1" mark="1.0000000" >
      <testcode>
                <text></text>
      </testcode>
      <stdin>
                <text><![CDATA[{1}]]></text>
      </stdin>
      <expected>
                <text><![CDATA[{2}]]></text>
      </expected>
      <extra>
                <text></text>
      </extra>
      <display>
                <text>HIDE</text>
      </display>
    </testcase>
     """.format(1 if i < 2 else 0,inp, ans))
        i += 1;
    outputFile.write("""</testcases>
 </question>""")


def printAllTasks():
    tasks = next(os.walk('.'))[1]
    for task in tasks:
        print(task)
        printTask(task)


os.chdir(r'C:\Users\VV\Desktop\tasks')
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
Задачи к § 38 «Целочисленные алгоритмы»
112450 - 112469
Задачи к § 40 «Множества»
112470 - 112481
Задачи к § 41 «Динамические массивы»
112482 - 112490
Задачи к § 42 «Списки»
112510 - 112515
Задачи к § 43 «Стеки, очереди, деки»
112484, 112491 - 112509
Задачи к § 44 «Деревья»
757 - 765, 2790, 3556, 3557, 111240
Задачи к § 46 «Динамическое программирование»
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
#contests = re.sub(r'§', ' ', contests)

contests = contests.split('\n')
for i in range (1, len(contests) -1, 2):
    print (contests[i])
    print (contests[i + 1])
    outputFile = codecs.open(contests[i] + ".xml", "w", "utf-8")
    printHeader(contests[i])
    for task in contests[i+1].split():
        print(task)
        printTask(task)
    printFooter()
    outputFile.close()