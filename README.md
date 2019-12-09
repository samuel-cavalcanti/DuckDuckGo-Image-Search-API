# DuckDuckGo Image Search API
Uma Api simples para baixar imagens do DuckDuckGo. 

Essa API foi originalmente criada por [Deepan Prabhu Babu](https://github.com/deepanprabhu). 
A qual eu fiz um porte para __python 3.7.5__ e adicionei novas funcionalidades como: apenas
pesquisar as imagens e retornar uma lista de urls e baixar as imagens em multi-threading.
   

## Instalação

```bash
git clone https://github.com/samuel-cavalcanti/DuckDuckGo-Image-Search-API.git
cd DuckDuckGo-Image-Search-API
python setup.py install # python3.7.5
pip install . # Dependendo da situação vai precisar de sudo
```

### Código exemplo

```python

from duckduckgo_images_api.duckduckgo_api import DuckDuckGoApi


def test_api():
    duck_duck_go = DuckDuckGoApi(debug=False)

    images = duck_duck_go.search("arroz", max_results=100)

    duck_duck_go.print_json(images[0])

    duck_duck_go.search_and_download("casa", max_results=50, max_workers=5)


if __name__ == '__main__':
    test_api()
```
link para download do código [test_api.py](exemples/test_api.py)

#### Observações

- parâmetro keywords : é a palavra ou as palavras chave da busca no [duckduckgo](https://duckduckgo.com/)

- parâmetro max_workers : é o número de Threads utilizadas para o download das imagens

- parâmetro output_dir : é a pasta onde será salva as imagens. Por padrão é criada uma pasta chamada __downloads__

# Agradecimentos

[thibauts](https://github.com/thibauts/duckduckgo)     
[rachmadaniHaryono](https://github.com/rachmadaniHaryono)  
[Deepan Prabhu Babu](https://github.com/deepanprabhu)  

