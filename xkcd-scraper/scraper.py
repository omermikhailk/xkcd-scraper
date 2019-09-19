from bs4 import BeautifulSoup as bs
import requests
# import os


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

    # Gets all the URLs from the archive table
    archive = soup_obj.find('body').find('div', id='middleContainer')
    archive = archive.find_all('a')

    base_url = 'https://www.xkcd.com'
    # Adds the main page URL to the obtained URL ending
    # eg. 'https://www.xkcd.com' + '/124/'
    archive_links = set(base_url + post['href'] for post in archive)
    # Used set comprehension as that should be faster than using a list (?)
    # Not too sure on that

    return archive_links


def download_img(post_urls: set):
    """
    Downloads all the images from the post_urls, which is a list
    """

    # The 'count' variable will be what our file will be named
    count = 0
    for post in post_urls:
        post_src = requests.get(post)
        # Tries to make sure that the post actually exists
        # by checking the status code
        if post_src.status_code == 200:
            post_soup = bs(post_src.text, 'lxml')
            # Navigates to where the image tags are located on the bag
            # Then we navigate to the first element as .select() will return
            # a list
            post_soup = post_soup.select('body #middleContainer #comic img')[0]

            # 'srcset' is an attribute which has a higher quality image URL
            # however some older comics don't have 'srcset' and have 'src'
            # only
            try:
                img_url = post_soup['srcset']
            except:
                try:
                    img_url = post_soup['src']
                except:
                    # Should probably change this to something else
                    # Should maybe look into the 'logging' module?
                    print(f'Error\t{post}')
                else:
                    img_url = f'https:{img_url}'
                    requests_img = requests.get(img_url)
                    with open(f'{count}.png', 'wb') as f:
                        f.write(requests_img.content)
                        print(f'Downloaded {post}')
            else:
                # Splitting the 'img_url'; as 'srcset' will give a value which
                # has some text and then whitespace and then some text after
                # that by default
                # So using .split() will give us the URL that we actually want,
                # by us accessing the first element
                # eg. "https://www.imgurl.com 2x" to "https://www.imgurl.com"
                img_url = f'https:{img_url.split()[0]}'
                requests_img = requests.get(img_url)
                with open(f'{count}.png', 'wb') as f:
                    f.write(requests_img.content)
                    print(f'Downloaded {post}')
            # Incrementing 'count' so that every image has a different name
            count += 1
        else:
            pass


if __name__ == '__main__':
    main()
