from bs4 import BeautifulSoup as bs
import requests
import os


def main():
    url = 'https://xkcd.com/archive/'

    src = requests.get(url).text
    soup = bs(src, 'lxml')

    # folder_name = location() + "/xkcd"
    # os.makedirs(folder_name, exist_ok=True)
    # os.chdir(folder_name)

    download_img(archive_list(soup))


# def location():
#     """
#     Asks the user for a path to create the folder for downloaded comics
#     in
#     """
#     path = input('Please enter the path for your comics to be kept')
#
#     return path


def archive_list(soup_obj) -> set:
    """
    Gets a list of URLs of all of the XKCD comics

    Takes in a 'Beautiful Soup' object

    Returns all the post URLs
    """

    archive = soup_obj.find('body').find('div', id='middleContainer')
    archive = archive.find_all('a')

    base_url = 'https://www.xkcd.com'
    archive_links = set(base_url + post['href'] for post in archive)

    return archive_links


def download_img(post_urls: set):
    """
    Downloads all the images from the post_urls, which is a list
    """

    count = 0
    for post in post_urls:
        post_src = requests.get(post)
        if post_src.status_code == 200:
            post_soup = bs(post_src.text, 'lxml')
            post_soup = post_soup.select('body #middleContainer #comic img')[0]

            try:
                img_url = post_soup['srcset']
            except:
                try:
                    img_url = post_soup['src']
                except:
                    print(f'Error\t{post}')
                else:
                    img_url = f'https:{img_url}'
                    requests_img = requests.get(img_url)
                    with open(f'{count}.png', 'wb') as f:
                        f.write(requests_img.content)
                        print(f'Downloaded {post}')
            else:
                img_url = f'https:{img_url.split()[0]}'
                requests_img = requests.get(img_url)
                with open(f'{count}.png', 'wb') as f:
                    f.write(requests_img.content)
                    print(f'Downloaded {post}')
            count += 1
        else:
            pass


if __name__ == '__main__':
    main()
