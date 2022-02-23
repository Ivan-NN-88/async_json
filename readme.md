# Обработчик JSON файла

-------------------------------------------
Разработчик: Вихарев Иван Александрович.<br>
Дата: 23.02.2022<br>
-------------------------------------------

## Описание с заметками:

Необходимо написать обработку данного файла json с учетом следующих требований:

1. В файле может быть несколько графов (ключ "robot_graphs" - это массив, где каждый элемент массива отдельный граф).

2. В каждом графе имеется список переменных (ключ "vars") и список нод (ключ "nodes").

3. Каждая нода имеет свой тип (ключ "name", например "base.start", "base.finish" и т.д.).

4. Каждая переменная имеет тип, определенный в ключе "data_type" и уникальный идентификатор "uuid".

5. В каждой ноде есть список используемых аргументов (путь в ноде "data"->"vars"->"inputs" или "data"->"vars"->"outputs").

6. Каждый аргумент ноды может иметь либо значение (присутствует тег "value"), 
либо ссылку на переменную графа (присутствует тег "ref"). 
В теге ref записан идентификатор переменной из ключа графа "vars". Одновременно "value" и "ref" быть не могут.

 

Что требуется выполнить:

1. Требуется выполнить обход графов, внутри каждого графа выполнить обход его переменных и нод.<br>
***Выполнено.***

2. Каждый граф, каждая переменная и каждая нода может быть обработана индивидуальным алгоритмом, 
а может быть обработана и стандартным алгоритмом. 
Т.е. есть стандартный алгоритм, но должна быть возможность расширить код так, чтобы один определенный тип графа, 
ноды или переменной обработать индивидуально. Т.е. требуется спроектировать так, 
чтобы при необходимости было легко добавить обработку нового типа графа, ноды или переменной.<br>
***Выполнено. Код можно расширять хоть унаследованием доп.класса, хоть новым методом***

3. Запускать обработку графов асинхронно параллельно с использованием asyncio. 
Все обработчики нод и переменных должны быть асинхронными.<br>
***Выполнено. Код работает асинхронно.***

4. Для эмуляции задержки обработки переменных и нод добавить задержку в виде asyncio.sleep(0-1) - 
задержка рандомная от 0 до 1 секунды.<br>
 ***Выполнено. Рандомную задержку добавил на все обработчики.***

5. Графы в обработку должны поступить параллельно.<br>
***Выполнено. Графы в обработку поступают параллельно.***

6. В случае возникновения ошибки при обработке любого из графов прерывать выполнение обработки остальных графов
 и прерывать обработку. Ошибка может возникнуть на любом уровне 
 (на уровне обработки переменной или на уровне обработки ноды)<br>
 ***Выполнено. В случае ошибок все сопрограммы прерывают свю работу.***

7. Если в "inputs" или "outputs" ноды имеется аргумент с тегом "ref", то делать проверку, что переменная  графа 
(в теге "vars" графа) имеется с таким uuid. Если не имеется то кидать исключение.<br>
 ***Выполнено. Есть пустые рефы в JSON файле, в коде заложил что пустые рефы == нет рефа.(?) 
 Если не так - поправить 5 сек.***

8. После обработки графа в консоль должен вывестись текст в таком виде:<br>
Граф: name, uuid<br>
Список переменных:<br>
uuid, name, data_type<br>
Список нод:<br>
uuid, name, список_имен_аргументов<br>
 ***Выполнено. Ровно после обработки графа текст выводится в консоль и дублируется в лог.***

9. Для тестирования обработки нескольких графов скопируй в json файле грфа несколько раз и измени в нем uuid.<br>
Пример вывода:<br>
Граф: CycleCheckElement, 5fcb5e89-3bab-4282-b9db-1b2dac346930<br>
Список переменных:<br>
f7d06b6b-c7bc-40d2-817d-65a7ffc59e67, RITA_ENV, base.dictionary<br>
b19dbe2f-dcfb-4685-8100-667fd288bd00, exists, base.bool<br>
...<br>
Список нод:<br>
34aa6278-febc-4e41-ba59-e10d7af57d5c, base.start<br>
18be87a7-5145-421d-be89-d3456e26083d, base.loop_while, condition, loop_mode<br>
...<br>
***Выполнено. Скопировал несколько графов, изменил имена и UUID. Формат вывода именно такой***
 

При проектировании обратить внимание на:

1. Архитектура (использовать подходы ООП и SOLID)<br>
***Выполнено. Код выполнил гибким.***
2. Использование asyncio<br>
***Выполнено. Задействовал asyncio.***
-------------------------------------------


