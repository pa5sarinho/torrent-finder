from bs4 import BeautifulSoup
import requests, webbrowser

# Made by passarinho

def search(browse):

    br = browse.replace(' ', '%20')
    url = 'https://www.pirate-bay.net/search?q=' + br
    print('searching...\n')
    # print('getting to',url)

    piratebay = requests.get(url)

    soup = BeautifulSoup(piratebay.content, 'html.parser')

    # Change the focus to the iframe
    frame = soup.find('iframe')
    pirate_bay = requests.get(frame['src'])

    soup = BeautifulSoup(pirate_bay.content, 'html.parser')
    torrent_count = 0
    # Finding and printing the torrent names:
    t_names = soup.find_all('a', attrs={'class': 'detLink'})
    for name in t_names:
        torrent_count += 1
        torrent_title = name.get_text()
        print('[{0}]'.format(torrent_count),torrent_title)

    # Checking all links:
    href = soup.find_all('a', href=True)
    t_links = []
    for a in href:
        ln = a['href']
        # filtering the actual torrent links from other links/stuff on the page:
        if 'torrent' in ln and 'https' in ln:
            t_links.append(ln)

    number = int(input('\nchoose a torrent: '))

    # Getting to the torrent page:
    torrent_choice = requests.get(t_links[number-1])
    pagesoup = BeautifulSoup(torrent_choice.content, 'html.parser')

    def skulls():
        trusted_skull = pagesoup.find('img', attrs={'title': 'Trusted'})
        vip_skull = pagesoup.find('img', attrs={'title': 'VIP'})
        if trusted_skull:
            return 'Trusted'
        elif vip_skull:
            return 'VIP'
        else:
            return 'not sure if trusted'


    title = pagesoup.find('div', attrs={'id': 'title'}).get_text()
    seed = pagesoup.find('dt', string="Seeders:")
    leech = pagesoup.find('dt', string="Leechers:")
    size = pagesoup.find('dt', string="Size:")

    mbs = size.find_next().get_text()
    seeders = seed.find_next().get_text()
    leechers = leech.find_next().get_text()

    print(
        '\nTorrent info:\n',
        'Title:', title+'\n',
        skulls(),
        '\n Seeders:',seeders,
        '\n Leechers:',leechers,
        '\n Size:',mbs
    )

    confirm = input('\nDo you want this torrent? [y][n] ')

    if confirm == 'y':
        print('getting magnet link...')

        # Getting the magnet link
        td = pagesoup.find_all('a', href=True)
        magnet = []
        for t in td:
            m = t['href']
            if 'magnet' in m:
                magnet.append(m)

        webbrowser.open(magnet[0])

    elif confirm == 'n':
        search(browse)


browse = input('Torrent Search: ')
search(browse)
