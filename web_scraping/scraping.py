from bs4 import BeautifulSoup as bs
import requests
import libtorrent as lt
import time
import datetime 
import re  

def download(link):

    ses = lt.session()
    ses.listen_on(6881, 6891)
    params = {
        'save_path': '/home/becode',
        'storage_mode': lt.storage_mode_t(2)}

    print(link)

    handle = lt.add_magnet_uri(ses, link, params)
    ses.start_dht()

    begin = time.time()
    print(datetime.datetime.now())

    print ('Downloading Metadata...')
    while (not handle.has_metadata()):
        time.sleep(1)
    print ('Got Metadata, Starting Torrent Download...')

    print("Starting", handle.name())

    while (handle.status().state != lt.torrent_status.seeding):
        s = handle.status()
        state_str = ['queued', 'checking', 'downloading metadata', \
                'downloading', 'finished', 'seeding', 'allocating']
        print ('%.2f%% complete (down: %.1f kb/s up: %.1f kB/s peers: %d) %s ' % \
                (s.progress * 100, s.download_rate / 1000, s.upload_rate / 1000, \
                s.num_peers, state_str[s.state]))
        time.sleep(5)

    end = time.time()
    print(handle.name(), "COMPLETE")

    print("Elapsed Time: ",int((end-begin)//60),"min :", int((end-begin)%60), "sec")
    print(datetime.datetime.now())  

def scraper():
    #inputs
    choice = input('Available tracker : piratebay ' )
    search = input('What do you want to download ? : ')
    number = input('How many torrents do you want to download ? : ')
    if choice == '1':

        url = 'https://thepiratebay.party/search/' + search
        page = requests.get(url)
        soup = bs(page.text, 'lxml')
        torrents = soup.find(id="searchResult")
        trs = torrents.find_all("tr")
        magnets = []
        names = []
        sizes = []
        seeds = []

        for tr in trs[1:int(number)+1]:
            magnets.append(tr.nobr.a['href'])
            name = tr.find_all('td')
            names.append(name[1].a.text)
            sizes.append(name[4].text)
            seeds.append(name[5].text)

            print("Torrents found : ")
        for key,val in enumerate(names):
            print("[" + str(key) + "]" + val + "[" + sizes[key] + "] (" + seeds[key] + " seeds)")
  
        which = input('Which torrents do you want to download ? (0/1/2/3...) : ')

        choices = re.findall(r'\d+', which)

        print("Will download : ")
        for key,val in enumerate(choices):
            print("[" + str(val) + "]" + names[int(val)] + "[" + sizes[int(val)] + "] (" + seeds[int(val)] + " seeds)")
        for each in choices:
            download(magnets[int(each)])

    elif choice == '2':
        url = 'https://www.1377x.to/search/' + search + '/1/'
        page = requests.get(url)
        soup = bs(page.text, 'lxml')
        torrents = soup.find_all('tr')
        magnets = []
        names = []
        sizes = []
        seeds = []
        for each in torrents[1:int(number)+1]:
            
            url = 'https://www.1377x.to' + each.find_all('a')[1].get('href')
            page = requests.BeautifulSoupget(url)
            soup = (page.text, 'lxml')
            magnet = soup.find(class_='col-9 page-content')
            magnet = magnet.li.a.get('href')
            magnets.append(magnet)
            name = soup.find(class_='box-info-heading clearfix')
            name = name.h1.text
            names.append(name)
            size = soup.find(class_='list')
            size = size.find_all('li')[3].span.text
            sizes.append(size)
            seed = soup.find(class_='seeds')
            seeds.append(seed.text)
        print("Torrents found : ")
        for key,val in enumerate(names):
            print("[" + str(key) + "]" + val + "[" + sizes[key] + "] (" + seeds[key] + " seeds)")
        which = input('Which torrents do you want to download ? (0/1/2/3...) : ')
        choices = re.findall(r'\d+', which)
        print("Will download : ")
        for key,val in enumerate(choices):
            print("[" + str(val) + "]" + names[int(val)] + "[" + sizes[int(val)] + "] (" + seeds[int(val)] + " seeds)")
        for each in choices:
            download(magnets[int(each)])
scraper()

