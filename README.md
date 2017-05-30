# Anime_scrapper 

Allows you to download all episodes of a series from animeheaven.eu . 

First install the required modules 

    pip3 install -r requirements.txt   
    


Run the script with the link of the series as a command line argument . 

You may give a second command line argument specifying the location where to download the files.

        python3 <script> <url> [location]
        


To get all episodes download links as textfile 

     python3 get_epi_filelist.py <url>
        
To download using GUI 

    python3 anime_scraper_GUI.py 

url is link of anime series  having all episodes 

       python3 get_epi_filelist.py http://animeheaven.eu/i.php?a=Hunter%20x%20Hunter%202011%20Dubbed

To prevent scrapy log output in terminal 

    python3 get_epi_filelist.py http://animeheaven.eu/i.php?a=Hunter%20x%20Hunter%202011%20Dubbed  2> /dev/null

 
To download the episodes along with the file location:
      
    python3 download_episodes.py "http://animeheaven.eu/i.php?a=Hunter%20x%20Hunter%202011%20Dubbed path/to/download/file

## NOTE:
Depending upon your system you may need to use `python` or `python3`

# DISCLAIMER:

 **Downloading copyrighted media without the  owner’s permission is illegal is some countries. 
 Under no circumstances is this script intended to encourage illegal activity, 
 and there are no guarantees that this information will    protect you from any legal action**.   
 
 
