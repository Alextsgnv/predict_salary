<h1>Проект предсказания возможной заработной платы вакансии по ключевым навыкам</h1>
<hr>
</br>
</br>
<h3>Суть задачи:</h3>
<p>1. Получить данные с агрегатора вакансий HH.ru</p>
<p>2. Обработать полученные данный</p>
<p>3. Обучить модель</p>
<p>4. Реализовать интерфейс</p>
<p>4. Обернуть обученную модель в контейнер</p>
</br>
</br>
<h3>1. Получение данных с агрегатора вакансий HH.ru</h3>
<hr>
<p>Первым делом необходимо было определиться с вакансией. Тут несколько подводных камней. Первый это указание у вакансии ЗП от работодателя, зачастую работодатель оставляет это поле пустым. Второй это репрезетативность выборки. Важно, чтоб вакансии с одной стороны не были однородны, а с другой не были "мешаниной" распределения различных вакансий, имеющих некоторые похожые навыки.</p>
<p>Так как я работаю с языком программирования Python, я решил взять вакансии на его основе. Т.е. ключевым в поиске вакансии в запросе стало наличие языка Python в названии или описании вакансии. Это как раз позволило достич нужно репрезентативности, так как вакансии с pyrhon  включают всебя разные направления: web-разработчик, ML-разработчик, Data science, разработчик ПО, тестировщик, разработчик игр и др.</p>
<p>Для получения данных был использован механизм HH.ru API предоставленный разработчиками. Основной механизм это использование модуля requests с url "https://api.hh.ru/vacancies" и набором параметров. В качестве параметров были использованы Name: python - "название" вакансии (api ищет совпадение как в названии так и в описании), area: 1 - (Москва) - была использована так как различие в ЗП между Москвой и регионами достаточно большое, only_with_salary: True/False - параметр обозначающий, искать только с указаной ЗП или искать все. В первый случай нужен для обучения модели, второй для ее работы и добавления существующей базы.</p>
<p>Полученые данные затем преобразем в формат JSON  и в последствии записываются в БД postgresql</p>
</br>
</br>
<h3>2. Обработка полученных данных</h3>
<hr>
<p>Данные будем обрабатывать с помощью модуля pandas. Основные данные, с которыми я работал это salary - заработная плата, skills - основные навыки, description - описание вакансии, name - название вакансии, schedule - график работы, employement - режим работы. Основная суть и самая удачная концепция, которую мне удалось применить это получить множество всех навыков, и создать словарь отображающий множество всех навыков в ограниченное множество навыков. Я выделил следующие ("junior_skills", "middle_skills", "senior_skills", "lead_skills", "soft_skills", "quality_skills"). Эти признаки я выделил анализируя множество вакансий и их заработную плату на сайте hh.ru по конкретному навыку. Так же были взяти признаки schedule и employement и перекодированы в как в one hot encode, а так же из названия вакансий были извлечены признаки уровня разработчика ("начальник", "lead",  "техлид", "senior", "ведущий", "middle", "старший", "стажер"). Для удобства заработная плата была преведена к виду x*1000 руб. а так же из дата сета были исключены шумовые показатели ЗП (>400т. и <80т.)</p>
</br>
</br>
<h3>3. Построение модели</h3>
<hr>
<p>После обработки данных я получил готовые 17 признаков на которых можно обучать модели. Я выбрал 3 модели: к-ближайших соседей, случайный лес, градиентный бустинг. Перваую модель я решил использовать, так как считал что одинаковые по ЗП вакансии должны иметь похожие вектора, вторые две модели являются сильными ансемблеевыми моделями, которые способны обычатся на сложных зависимостях.</p>
<h5>Модели и параметры</h5>
<p>1. К-ближайших соседей: число соседей-11, функция поддсчета веса-"distance"(разные коэффициенты веса для близких и дальних векторов)</p>
<p>2. Случайный лес: общее число деревьев-400, минимальное число сэмплов в листе-5, максимальное число используемых признаков-log2(число всех признаков)</p>
<p>3. Градиентный бустинг: общее число деревьев-500, максимальная глубина каждого дерева-3, максимальное число используемых признаков-0.3, коэффициент обучения-0.01</p>
</br>
<p>После обучения на кросс валидации на 10 фолдов были получены следующие результаты (метрика MAE - средняя абсолютная ошибка)</p>
<p>1. Линейная регрессия: 45.6</p>
<p>2. К-ближайших соседей: 50.1</p>
<p>3. Случайный лес: МАЕ = 45.1</p>
<p>4. Градиентный бустинг: 46</p>
<p>В среднем все модели достаточно неплахо справляются с задачей. Есть преддположение, что при увеличении выборки и снятии ограничении по сумме заработной платы ансамблевые алгоритмы будут работать луччше. Из плючов линейной регрессии можно отметить способность к интерполяции.</p>
</br>
</br>
<h3>4. Интерфейс</h3>
<hr>
<p>Для реализации интерфейса был выбран фреймворк Django</p>
<p>Основные реализованные функции</p>
<p>1. Отображение базы данных и результатов модели.</p>
<p>2. Загрузка данных с использованием HH.ru api.</p>
<p>3. Применение базовых моделей и их дообучение на новых данных.</p>
<p>4. Возможность создания собственных моделей и обучение их на данных.</p>
</br>
</br>
<h3>5. Контейнер docker</h3>
<hr>
<p>Файлы dockerfile и docker-compose.yml уже написанны для запуска необходимо из корня проекта вызвать следующие команды</p>
<p>Для первого построения</p>
<p>docker-compose -f docker-compose.prod.yml up -d --build</p>
<p>Для пдальнейшего использования</p>
<p>docker-compose -f docker-compose.prod.yml up -d</p>

 
