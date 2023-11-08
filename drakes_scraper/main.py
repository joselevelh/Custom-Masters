import time
import os
import requests
from bs4 import BeautifulSoup

base_url: str = "https://us.drakes.com/blogs/news/"
image_storage_path = "/Users/JoseLevel/Downloads/drakes_images"


def scrape_drakes(page_url: str):
    """Scrapes given page url for all images and calls download_img() on each"""
    url = base_url + page_url
    look_book_dest_path = image_storage_path + "/" + page_url
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
        time.sleep(.5)


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


def get_look_book_urls():
    """gets all the lookbook urls on the page"""
    pass


def iterate_through_editorial():
    """traverse editorial(/news) pages"""
    pass


if __name__ == '__main__':
    lookbook_url = "drakes-for-hodinkee-the-lookbook-2023"
    scrape_drakes(lookbook_url)
    print("Done!")
