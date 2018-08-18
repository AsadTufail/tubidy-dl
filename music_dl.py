import requests
import bs4
import sys

domain = 'https://tubidy.mobi'


def fetch_page(url):
    '''Get HTML of the page.

    Obtain content from the provided url of the page and returns
    a soup object for working with html.

    Parameter:
    url: url of the page 

    Return:
    A Soup object for parsing HTML
    '''
    try:
        r = requests.get(url)
        soup = bs4.BeautifulSoup(r.content, 'lxml')
        return soup
    except requests.exceptions.ConnectionError:
        sys.exit("Internet is not working....")


def get_titles(name):
    '''Obtain titles of the music track from the page.

    Parameter:
    name: Name of the track

    Return:
    A list containing a pair of tuples in format (music track link and it's title)
    '''
    soup = fetch_page(('{}/search.php?q={}'.format(domain, name)))
    if soup.find('h4').a:
        if 'No results found.' == soup.find('h4').a.text:
            sys.exit("Your music track is not available")
    elif "No results found." in soup.find('div', class_="text-center").find('h4').text:
        sys.exit("Your music track is not available.")
    return [(tracks.parent.get('href'), tracks.parent.text.strip()) for tracks in soup.findAll('h4', class_='media-heading')]


def select_titles(titles):
    '''Select title from the displayed menu.

    Parameter: 
    titles(list): titles containing track info.

    Return:
    Link of the selected title page. 
    '''
    for num, track_info in enumerate(titles):
        print('({}) {}'.format(num, track_info[1]))
    
    track_number = int(input("Please select title number: "))
    return domain + titles[track_number][0]


def select_format(url):
    '''
    Select music format.

    Parameter:
    url: URL of the page.

    Return:
    Link of the selected format
    '''

    music_formats = fetch_page(url).findAll('a', class_='title')
    return [domain+types.get('href') for types in music_formats if 'MP3' in types.text][0]


def download_file(filename, url):
    '''Download file from the given url

    Parameters:
    filename: Filename of the music track
    url: URL of the file to be downloaded
    '''
    r = requests.get(url, stream=True)
    with open(filename + '.m4a', 'wb') as f:
        for chunk in r.iter_content(chunk_size=1024): 
            if chunk: 
                f.write(chunk)


def main():
    track_name = input("Please enter the name of the title: ")
    title_infos = get_titles(track_name)
    selected_title = select_titles(title_infos)
    selected_format = select_format(selected_title)
    download_file(track_name, fetch_page(selected_format).find('a', class_= 'title').get('href'))

if __name__ == '__main__':
    main()
