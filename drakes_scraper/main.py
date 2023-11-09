import time
import os
import requests
from bs4 import BeautifulSoup

base_url: str = "https://us.drakes.com"

image_storage_path = "/Users/JoseLevel/Downloads/drakes_images"


def scrape_drakes(page_url: str):
    """Scrapes given page url for all images and calls download_img() on each"""
    url = base_url + page_url
    look_book_dest_path = image_storage_path + "/" + page_url[11:]
    os.mkdir(look_book_dest_path)
    print(f"Url: {url}")
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    img_tags = soup.find_all('img')
    # Clean img_tags to remove false hits
    img_tags = list(filter(lambda item: item.get('src') is not None and "https:" in item.get('src'), img_tags))

    for img in img_tags:
        print(img)
    print(f"Found {len(img_tags)} images")
    for index, img in enumerate(img_tags):
        img_url = img.get('src')
        print(f"Image_url: {img_url}")
        image_dest_path = look_book_dest_path + '/image_' + str(index)
        download_img(img_url=img_url, image_dest=image_dest_path)
        time.sleep(1)


def download_img(img_url: str, image_dest: str):
    """Downloads the image to the default folder"""
    response = requests.get(img_url)

    if response.status_code == 200:  # Successful
        image_data = response.content
        with open(image_dest + ".jpg", 'wb') as f:
            f.write(image_data)
        print(f"Image downloaded successfully")
    else:
        print(f"Failed to download image. status code: {response.status_code}")


def get_look_book_urls(page_url: str):
    """gets all the lookbook urls on the page"""
    response = requests.get(page_url)
    soup = BeautifulSoup(response.text, 'html.parser')

    anchor_tags = soup.find_all('a', href=True)
    # print(f"\tanchor_tags found: {len(anchor_tags)}")
    anchor_tags = list(filter(lambda items: "Read more " in items.text, anchor_tags))
    # print(f"\ttags with 'Read More' in text: {len(anchor_tags)}")
    look_book_tags = list(filter(lambda items: "lookbook" in items['href'] or "look-book" in items['href'], anchor_tags))
    return look_book_tags


def iterate_through_editorial(refresh_only=True):
    """traverse editorial(/news) pages. TODO: if refresh_only is True(default)
    we stop if we find an article we already have downloaded"""
    lookbooks = []
    news_url: str = "/blogs/news/?page="
    for i in range(1, 163):  # Todo: revert to 1 stop number
        news_page_url: str = base_url + news_url + str(i)
        print(news_page_url)
        new_lb = get_look_book_urls(news_page_url)
        print(f"\tGot {len(new_lb)} lookbook(s) from this page")
        lookbooks.extend(new_lb)
    print(f"Total lookbooks: {len(lookbooks)}")
    return lookbooks


if __name__ == '__main__':
    all_lookbooks = iterate_through_editorial()
    for lookbook in all_lookbooks:
        lookbook_url = lookbook['href']
        print(lookbook_url)
    # lookbook_url = "/blogs/news/drakes-for-hodinkee-the-lookbook-2023"
        scrape_drakes(lookbook_url)
    print("Done!")
