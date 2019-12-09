from duckduckgo_api import DuckDuckGoApi


def test_api():
    duck_duck_go = DuckDuckGoApi(debug=False)

    images = duck_duck_go.search("arroz", 100)

    duck_duck_go.print_json(images[0])

    # duck_duck_go.search_and_download("casa", max_results=int(50), max_workers=5)


if __name__ == '__main__':
    test_api()
