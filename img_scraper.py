import os
import re
import requests
import PySimpleGUI as sg
from bs4 import BeautifulSoup


class ImgScraper:
    def __init__(self, url, dst=None):
        """
        Download all images from a website.

        :param url: Source website
        :param dst: Destination folder
        """
        self.url = url
        self.destination = dst
        if dst and not os.path.exists(dst):
            os.mkdir(dst)
        self.image_urls = self.images()

    def _get_path(self, file_path):
        """Return a concatenated destination path"""
        return os.path.join(self.destination, file_path) if self.destination else file_path

    def soup(self):
        """Request HTML and parse soup."""
        response = requests.get(self.url)
        return BeautifulSoup(response.text, 'html.parser')

    def images(self):
        """Return a list of image urls found on the webpage."""
        soup = self.soup()
        img_tags = soup.find_all('img')
        return [img['src'] for img in img_tags]

    def download(self):
        """Download images and save to destination."""
        dls = []
        for url in self.image_urls:
            filename = re.search(r'/([\w_-]+[.](jpg|gif|png))$', url)
            if not filename:
                continue
            with open(self._get_path(filename.group(1)), 'wb') as f:
                if 'http' not in url:
                    # sometimes an image source can be relative
                    # if it is provide the base url which also happens
                    # to be the site variable atm.
                    url = '{}{}'.format(self.url, url)
                try:
                    response = requests.get(url)
                    f.write(response.content)
                    dls.append(url)
                    print(url)
                except AttributeError:
                    pass

        print('\nImage scrapping complete ({0})'.format(len(dls)))
        print('\nImages saved to {0}'.format(os.path.abspath(self.destination)))


def main():
    url = sg.PopupGetText('Input the url you would like to scrape images from.')
    ImgScraper(url, 'images').download()


if __name__ == '__main__':
    main()
