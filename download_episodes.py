#!/usr/env/bin python3
############### D I S C L A I M E R ################
#                                                  #
# Downloading copyrighted media without the        #
# owner’s permission is illegal is some countries. #
# Under no circumstances is this script intended   #
# to encourage illegal activity, and there are     #
# no guarantees that this information will         #
# protect you from any legal action.               #
#                                                  #
####################################################


# The script allows you to give 2 command line arguments.
#The first one is the url on animeheaven site that contains list of the episodes.
#The second is optional and should contain a a string which tells the folder where you want to  download

import requests
import re
import sys
from tqdm import tqdm
from bs4 import BeautifulSoup

# The url  which has all the list of episodes in the series
HOME_URL = sys.argv[1]
# HOME_URL = "http://animeheaven.eu/i.php?a=Hunter%20x%20Hunter%202011"

# Episode url prefix
EPISODE_PREFIX = "http://animeheaven.eu/"

# Episode url regex
REGEX = r'\bhttps?://\S+\.(?:mp4)\b'


# Return a list of all pages linked from HOME_URL
# that contain links to .mp4 files.
def get_episode_pages():
    episode_list = list()

    try:
        response = requests.get(HOME_URL)
    except requests.RequestException:
        print(requests.RequestException)
        sys.exit(1)
    source = response.text

    soup = BeautifulSoup(source, 'html.parser')
    results = soup.find_all(class_="infoepbox")

    for result in results:

        episodes = result.find_all("a")

        for episode in episodes:
            rel_episode_url = episode.get('href')
            episode_url = EPISODE_PREFIX + rel_episode_url
            episode_list.append(episode_url)

    return episode_list


# Use regex (argh...) to get the
# first  link on the page that ends with .mp4
# see the regex above.
def get_episode_url(page_link):
    try:
        response = requests.get(page_link)
    except requests.RequestException:
        print(requests.RequestException)
        sys.exit(1)
    match = re.search(REGEX, response.text)
    if match:
        return match.group(0)
    return None


# Download the .mp4 video from the given url
# and save it in the same directory as this script
def download_episode(url):
    # The name of  the file to save the video as episode 23
    episode_no = url.split('--')[1]
    print("Downloading episode no %s" % episode_no)
    name = "Episode-{}.mp4 ".format(episode_no)

    try:
        response = requests.get(url, stream=True)
    except requests.RequestException:
        print(requests.RequestException)
        sys.exit(1)

    if len(sys.argv) == 3:
        name = sys.argv[2] + "/" + name
    scale_factor = 1
    chunk_size = 1024 * 1024 * scale_factor
    total_size = int(response.headers.get('content-length', 0))
    total = round(total_size / chunk_size)
    with open(name, 'wb') as episode_file:
        for data in tqdm(response.iter_content(chunk_size), total=total,
                         unit=' MB'):  # iter_content allows us to download a large file.. It doesn't keep the whole
            # file in memory
            episode_file.write(data)



def main():
    episode_pages = get_episode_pages()
    episode_urls = list()

    print('Get all episodes urls.')

    for episode_page in episode_pages:
        url = get_episode_url(episode_page)
        print(url)
        episode_urls.append(url)

    print('Done!')

    # For testing, only download one .mp4 file
    # because of their size.

    download_episode(episode_urls[0])
    print('Done!')


if __name__ == '__main__':
    main()
