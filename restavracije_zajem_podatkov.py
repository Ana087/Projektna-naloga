import requests
import re
import csv
import os

###############################################################################
# Pomožna orodja za pridobivanje podatkov s spleta.
###############################################################################
dodatek = ""

# URL glavne strani
restaurants_frontpage_url = f'https://www.tripadvisor.com/Restaurants-g274873-{dodatek}Ljubljana_Upper_Carniola_Region.html#EATERY_OVERVIEW_BOX'

# mapa, v katei so shranjeni podatki
restaurants_directory = 'restavracije'

# ime datoteke v kateri je shranjena glavna stran
frontpage_filename = 'frontpage.html'

# ime CSV datoteke v kateri so shranjeni podatki
csv_filename = 'restavracije.csv'


# funkcija zamenja html stran
def zamenjaj_stran(st_strani):
    if st_strani == 1:
        dodatek = ""
    else:
        dodatek = f"-oa{30 * (st_strani - 1)}-"
    return dodatek


def download_url_to_string(url):
    """Funkcija kot argument sprejme niz in puskuša vrniti vsebino te spletne
    strani kot niz. V primeru, da med izvajanje pride do napake vrne None.
    """
    try:
        # del kode, ki morda sproži napako
        page_content = requests.get(url).text
    except requests.exceptions.RequestException as e:
        # koda, ki se izvede pri napaki
        # dovolj je če izpišemo opozorilo in prekinemo izvajanje funkcije
        print(e)
        page_content = ""
    # nadaljujemo s kodo če ni prišlo do napake
    return page_content


def save_string_to_file(text, directory, filename):
    """Funkcija zapiše vrednost parametra "text" v novo ustvarjeno datoteko
    locirano v "directory"/"filename", ali povozi obstoječo. V primeru, da je
    niz "directory" prazen datoteko ustvari v trenutni mapi.
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w', encoding='utf-8') as file_out:
        file_out.write(text)
    return None


# funkcija prenese glavno stran in jo shrani v datoteko
def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    content = download_url_to_string(page)
    save_string_to_file(content, directory, filename)
    return

# funkcija potegne določeno html stran
def potegni_strani():
    for stevilo in range(1, 20):
        dodatek = zamenjaj_stran(stevilo)
        frontpage_filename = f"frontpage_{stevilo}.html"
        stran = f'https://www.tripadvisor.com/Restaurants-g274873-{dodatek}Ljubljana_Upper_Carniola_Region.html#EATERY_OVERVIEW_BOX' 
        save_frontpage(stran, restaurants_directory, frontpage_filename)



###############################################################################
# Obdelava podatkov.
###############################################################################


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def page_to_ads(page_content):
    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
    vrne njih seznam"""
    rx = re.compile(r'{"detailPageUrl":"/Restaurant_Review(.*?)"isLocalChefItem":false}',
                    re.DOTALL)
    ads = re.findall(rx, page_content)
    return ads


def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu, oceni, glasovih, tipu in ceni
    ter vrne slovar, ki vsebuje ustrezne podatke
    """
    rx = re.compile(r'"name":"(?P<ime>.*?)".*?'
                    r'"averageRating":(?P<rating>-?\d.?\d*?),.*?'
                    r'"userReviewCount":(?P<glasovi>\d*),.*?'
                    r'"establishmentTypeAndCuisineTags":\[(?P<tip>.*?)\],.*?'
                    r'"priceTag":"?(?P<cena>.*?)"?,.*?',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()
    return ad_dict


# vrne seznam slovarjev s podatki o oglasih
def ads_from_file(filename, directory):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
    page = read_file_to_string(filename, directory)
    blocks = page_to_ads(page)

    ads = [get_dict_from_ad_block(block) for block in blocks]
    return ads


###############################################################################
# Shranjevanje obdelanih podatkov.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'a') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        #writer.writeheader()   # naslov izpiše le enkrat
        for row in rows:
            writer.writerow(row)
    return


def write_restaurants_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da so ključi vseh
    sloverjev parametra ads enaki in je seznam ads neprazen.
    """
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    write_csv(ads[0].keys(), ads, directory, filename)


# glavna funkcija
def main(redownload=False, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Prenese oglase
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo glavno stran
    #save_frontpage(restaurants_frontpage_url, restaurants_directory, frontpage_filename)

    # Iz lokalne (html) datoteke preberemo podatke
    ads = page_to_ads(read_file_to_string(restaurants_directory, frontpage_filename))
    # Podatke prebermo v lepšo obliko (seznam slovarjev)
    ads_nice = [get_dict_from_ad_block(ad) for ad in ads]
    # Podatke shranimo v csv datoteko
    write_restaurants_ads_to_csv(ads_nice, restaurants_directory, csv_filename)


# ustvarjanje csv datoteke
def zanka():
    for stevilo in range(1, 20):
        frontpage_filename = f"frontpage_{stevilo}.html"
        # Iz lokalne (html) datoteke preberemo podatke
        ads = page_to_ads(read_file_to_string(restaurants_directory, frontpage_filename))
        # Podatke prebermo v lepšo obliko (seznam slovarjev)
        ads_nice = [get_dict_from_ad_block(ad) for ad in ads]
        seznam_tipov = []
        # ustvarjanje csv "poddatoteke"
        for slovar in ads_nice:
            if slovar["tip"] != None:
                slovar["tip"] = slovar["tip"].split(",")
            for tip in slovar["tip"]:
                seznam_tipov.append({"ime" : slovar["ime"], "tip" : tip})
            del slovar["tip"]
        
        write_restaurants_ads_to_csv(seznam_tipov, restaurants_directory, "tipi.csv")
            
        # Podatke shranimo v csv datoteko
        write_restaurants_ads_to_csv(ads_nice, restaurants_directory, csv_filename)