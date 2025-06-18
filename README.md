# Made-in-China Parser_v1.1

Простой парсер для сайта [made-in-china.com](https://www.made-in-china.com), который собирает информацию о компаниях по заданным ключевым словам.  
Приложение написано на Python с использованием Requests, lxml и Streamlit для удобного веб-интерфейса.

---

## Возможности

- Автоматическое определение количества страниц для парсинга
- Сбор информации: название, тип бизнеса, продукция, геолокация
- Экспорт результатов в Excel
- Удобный веб-интерфейс на Streamlit

---

## Установка и запуск
Клонируйте репозиторий:
   ```bash
   git clone https://github.com/Proks1312/made-in-china-parser.git
   cd made-in-china-parser
#Установите зависимости:
py -m pip install -r requirements.txt
py -m pip install streamlit
#Запустите приложение:
py -m streamlit run app.py
