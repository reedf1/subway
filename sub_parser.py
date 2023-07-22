import logging

import requests
from bs4 import BeautifulSoup
from tabulate import tabulate

from tqdm import tqdm


class SubParser:
    def __init__(self):
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    def _scrape_sub(self, subreddit: str):
        with requests.get(f"https://old.reddit.com/r/{subreddit}/", headers=self.headers) as response:
            page = response.content

        soup = BeautifulSoup(page, "html.parser")

        content_area = soup.find('div', {"class": "content"})

        meta_front_page = []
        for post in content_area.find_all('a'):
            link = post.attrs.get('href')
            if link:
                if f"old.reddit.com/r/{subreddit}/comments/" in link:
                    meta_front_page.append(link)

        front_page = {}
        for link in (tq := tqdm(meta_front_page)):
            tq.set_description(link)
            scraped_post = self._scrape_post(link)
            front_page.update({scraped_post['post']['title']: scraped_post})

        return front_page

    def _scrape_post(self, link: str):
        with requests.get(link, headers=self.headers) as response:
            page = response.content

        soup = BeautifulSoup(page, "html.parser")

        title = soup.find('title')

        if title.text == 'reddit.com: sign up or log in':
            logging.critical("Hit Reddit Login Page.")

        content_area = soup.find('div', {"class": "content"})
        post_area = content_area.find('div', {'class': 'sitetable linklisting'})
        raw_post = post_area.find('div', {'class', 'md'})

        post = {"title": title.text,
                "content": raw_post.text if raw_post else None}

        comments = []
        comment_area = content_area.find('div', {"class": "commentarea"})
        for raw_comment in comment_area.find_all('div', {"class": "md"}):
            comment = {
                "content": raw_comment.text
            }
            comments.append(comment)
        return {'post': post, 'comments': comments}


if __name__ == "__main__":
    example_payload = {
        'post': {'post': {'title': 'title', 'content': 'content'}, 'comments': [{'content': 'content'}]}}

    example_payload[]

    print(tabulate(example_payload))


