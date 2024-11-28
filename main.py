import requests
import webbrowser


class WikipediaSearcher:


    def __init__(self):
        self.base_url = "https://ru.wikipedia.org/w/api.php"

    def search(self, query):

        params = {
            "action": "query",
            "list": "search",
            "srsearch": query,
            "format": "json",
        }

        try:
            response = requests.get(self.base_url, params=params)
            response.raise_for_status()
            data = response.json()
            return data.get("query", {}).get("search", [])
        except requests.RequestException as e:
            print(f"Ошибка при подключении к Википедии: {e}")
            return []


class WikipediaApp:


    def __init__(self):
        self.searcher = WikipediaSearcher()

    def display_results(self, results):

        print("\nРезультаты поиска:")
        for i, result in enumerate(results, start=1):
            print(f"{i}. {result['title']}")

    def open_article(self, title):


        page_url = f"https://ru.wikipedia.org/wiki/{title.replace(' ', '_')}"
        print(f"Открытие страницы: {page_url}")
        webbrowser.open(page_url)

    def run(self):

        while True:
            print("Введите поисковый запрос (или 'exit' для выхода):")
            query = input("> ").strip()

            if not query or query.lower() == "exit":
                print("Выход из программы.")
                break


            search_results = self.searcher.search(query)
            if not search_results:
                print("Ничего не найдено. Попробуйте другой запрос.")
                continue


            self.display_results(search_results)


            print("\nВведите номер статьи, чтобы открыть её в браузере, или '0' для выхода:")
            try:
                choice = int(input("> "))
                if choice == 0:
                    print("Выход из программы.")
                    break
                elif 1 <= choice <= len(search_results):
                    selected_title = search_results[choice - 1]['title']
                    self.open_article(selected_title)
                else:
                    print("Некорректный выбор.")
            except ValueError:
                print("Пожалуйста, введите число.")


if __name__ == "__main__":
    app = WikipediaApp()
    app.run()