import unittest
from duckduckgo_images_api.duckduckgo_api import DuckDuckGoApi

from pathlib import Path


class DuckDuckGoApiIntegrationSuiteCase(unittest.TestCase):

    def test_search_home_images(self):

        api = DuckDuckGoApi()
        max_results = 100
        images = api.search(keywords="home", max_results=max_results)

        self.assertTrue(0 < len(images) <= max_results)

    def test_search_and_download_rice_images(self):

        api = DuckDuckGoApi()

        output = "downloads_test"
        max_results = 20

        api.search_and_download(
            output_dir=output,
            keywords="rice", max_workers=5, max_results=max_results)

        output_path = Path(output)

        self.assertTrue(output_path.is_dir())

        files = [f for f in output_path.iterdir() if f.is_file()]

        for image_file in output_path.iterdir():
            image_file.unlink()  # unlink means remove file or symbolic link

        output_path.rmdir() # delete dir

        self.assertTrue(0 < len(files) <= max_results)
