import requests
from lxml import html
from urllib.parse import quote_plus, quote
import re
import time
import random

def clean_text(text):
    text = text.replace('\xa0', ' ')
    text = text.replace('\n', ' ')
    text = text.replace('\r', ' ')
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

def get_max_page(query):
    query_encoded = quote_plus(query)
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.0.0 Safari/537.36",
        "Mozilla/5.0 (iPhone; CPU iPhone OS 15_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.0 Mobile/15E148 Safari/604.1"]

    url = f"https://www.made-in-china.com/company-search/{query_encoded}/C1//1000.html?pv_id=1itucubjod3b&faw_id=null&bv_id=1itucuell0bf&pbv_id=1itucuae534e"
    headers = {"User-Agent": random.choice(user_agents)}
    try:
        response = requests.get(url, headers=headers, allow_redirects=True, timeout=10)
        final_url = response.url
        match = re.search(r"/C1/(\d+)\.html", final_url)
        if match:
            return int(match.group(1))
        else:
            return 1
    except Exception as e:
        print(f"Ошибка при получении max страницы: {e}")
        return 1

def parse_companies(query, start_page=1, page_count=1,progress_callback=None):
    encoded = quote(query)
    base_url = "https://www.made-in-china.com/company-search/{}/C1//{}.html"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36"
    }

    all_data = []
    last_success_page = start_page - 1  # **Инициализация до стартовой страницы**


    for page in range(start_page, start_page + page_count):
        url = base_url.format(encoded, page)
        print(f"Парсим страницу: {url}")
        try:
            response = requests.get(url, headers=headers, timeout=10)
            response.raise_for_status()
            tree = html.fromstring(response.content)

            containers = tree.xpath("//div[@faw-module='suppliers_list']")
            if not containers:
                print(f"⚠️ На странице {page} не найдено контейнеров с данными.")

            for container in containers:
                names = container.xpath(".//h2/a")
                for name_tag in names:
                    name = clean_text(name_tag.text_content())
                    link = name_tag.get("href")

                    business_type, products, location = "", "", ""

                    rows = container.xpath(".//tr")
                    for row in rows:
                        text = clean_text(row.text_content())
                        if "Main Products" in text:
                            products = text.replace("Main Products:", "").strip()
                        elif "Business Type" in text:
                            business_type = text.replace("Business Type:", "").strip()
                        elif "City/Province" in text:
                            location = text.replace("City/Province:", "").strip()

                    all_data.append({
                        "Название компании": name,
                        "Ссылка": link,
                        "Тип бизнеса": business_type,
                        "Продукция": products,
                        "Геолокация": location
                    })

            last_success_page = page  # Обновляем номер успешно обработанной страницы
            if progress_callback:
                progress_callback(page)

        except Exception as e:
            print(f"❌ Ошибка на странице {page}: {e}")
            print(f"⚠️ Парсинг остановлен. Последняя успешно обработанная страница: {last_success_page}")
            break

        time_to_sleep = random.uniform(1, 3)
        print(f"Ждем {time_to_sleep:.2f} секунды перед следующей страницей...")
        time.sleep(time_to_sleep)

    return all_data, last_success_page

if __name__ == "__main__":
    query = "conveyor belting"
    max_pages = get_max_page(query)
    print(f"Максимально доступно страниц: {max_pages}")

    results = parse_companies(query=query, page_count=min(2, max_pages))
    print(f"Найдено компаний: {len(results)}")

    # Показываем первые 3 компании, если они есть
    if results:
        print("Примеры компаний:")
        for company in results[:3]:
            print(company)
    else:
        print("Нет данных для отображения.")