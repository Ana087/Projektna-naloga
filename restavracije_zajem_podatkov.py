import requests
import re
import csv
import os

###############################################################################
# Pomožnia orodja za pridobivanje podatkov s spleta.
###############################################################################

# URL glavne strani
restaurants_frontpage_url = 'https://www.tripadvisor.com/Restaurants-g274873-Ljubljana_Upper_Carniola_Region.html#EATERY_OVERVIEW_BOX'
# mapa, v katero bomo shranili podatke
restaurants_directory = 'restavracije'
# ime datoteke v katero bomo shranili glavno stran
frontpage_filename = 'frontpage.html'
# ime CSV datoteke v katero bomo shranili podatke
csv_filename = 'restavracije.csv'


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


# Definirajte funkcijo, ki prenese glavno stran in jo shrani v datoteko.


def save_frontpage(page, directory, filename):
    """Funkcija shrani vsebino spletne strani na naslovu "page" v datoteko
    "directory"/"filename"."""
    content = download_url_to_string(page)
    save_string_to_file(content, directory, filename)
    return


###############################################################################
# Po pridobitvi podatkov jih želimo obdelati.
###############################################################################


def read_file_to_string(directory, filename):
    """Funkcija vrne celotno vsebino datoteke "directory"/"filename" kot niz"""
    path = os.path.join(directory, filename)
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


# Definirajte funkcijo, ki sprejme niz, ki predstavlja vsebino spletne strani,
# in ga razdeli na dele, kjer vsak del predstavlja en oglas. To storite s
# pomočjo regularnih izrazov, ki označujejo začetek in konec posameznega
# oglasa. Funkcija naj vrne seznam nizov.


def page_to_ads(page_content):
    """Funkcija poišče posamezne oglase, ki se nahajajo v spletni strani in
    vrne njih seznam"""
    rx = re.compile(r'<div class="poi">(.*?)<div class="booking"><\/div>',
                    re.DOTALL)
    ads = re.findall(rx, page_content)
    return ads


# Definirajte funkcijo, ki sprejme niz, ki predstavlja oglas, in izlušči
# podatke o imenu, ceni in opisu v oglasu.


def get_dict_from_ad_block(block):
    """Funkcija iz niza za posamezen oglasni blok izlušči podatke o imenu, ceni
    in opisu ter vrne slovar, ki vsebuje ustrezne podatke
    """
    rx = re.compile(r'title="(?P<name>.*?)"'
                    r'.*?</h3>\s*(?P<description>.*?)\s*</?div'
                    r'.*?class="price">(<span>)?(?P<price>.*?)'
                    r'( €</span>)?</div',
                    re.DOTALL)
    data = re.search(rx, block)
    ad_dict = data.groupdict()
    return ad_dict

#DEBUGGEX


# Definirajte funkcijo, ki sprejme ime in lokacijo datoteke, ki vsebuje
# besedilo spletne strani, in vrne seznam slovarjev, ki vsebujejo podatke o
# vseh oglasih strani.


def ads_from_file(filename, directory):
    """Funkcija prebere podatke v datoteki "directory"/"filename" in jih
    pretvori (razčleni) v pripadajoč seznam slovarjev za vsak oglas posebej."""
    page = read_file_to_string(filename, directory)
    blocks = page_to_ads(page)
    ads = [get_dict_from_ad_block(block) for block in blocks]
    return ads


###############################################################################
# Obdelane podatke želimo sedaj shraniti.
###############################################################################


def write_csv(fieldnames, rows, directory, filename):
    """
    Funkcija v csv datoteko podano s parametroma "directory"/"filename" zapiše
    vrednosti v parametru "rows" pripadajoče ključem podanim v "fieldnames"
    """
    os.makedirs(directory, exist_ok=True)
    path = os.path.join(directory, filename)
    with open(path, 'w') as csv_file:
        writer = csv.DictWriter(csv_file, fieldnames=fieldnames)
        writer.writeheader()
        for row in rows:
            writer.writerow(row)
    return


# Definirajte funkcijo, ki sprejme neprazen seznam slovarjev, ki predstavljajo
# podatke iz oglasa mačke, in zapiše vse podatke v csv datoteko. Imena za
# stolpce [fieldnames] pridobite iz slovarjev.


def write_cat_ads_to_csv(ads, directory, filename):
    """Funkcija vse podatke iz parametra "ads" zapiše v csv datoteko podano s
    parametroma "directory"/"filename". Funkcija predpostavi, da sa ključi vseh
    sloverjev parametra ads enaki in je seznam ads neprazen.
    """
    # Stavek assert preveri da zahteva velja
    # Če drži se program normalno izvaja, drugače pa sproži napako
    # Prednost je v tem, da ga lahko pod določenimi pogoji izklopimo v
    # produkcijskem okolju
    assert ads and (all(j.keys() == ads[0].keys() for j in ads))
    write_csv(ads[0].keys(), ads, directory, filename)


# Celoten program poženemo v glavni funkciji

def main(redownload=False, reparse=True):
    """Funkcija izvede celoten del pridobivanja podatkov:
    1. Oglase prenese iz bolhe
    2. Lokalno html datoteko pretvori v lepšo predstavitev podatkov
    3. Podatke shrani v csv datoteko
    """
    # Najprej v lokalno datoteko shranimo glavno stran
    save_frontpage(cat_directory, frontpage_filename)

    # Iz lokalne (html) datoteke preberemo podatke
    ads = page_to_ads(read_file_to_string(cat_directory, frontpage_filename))
    # Podatke prebermo v lepšo obliko (seznam slovarjev)
    ads_nice = [get_dict_from_ad_block(ad) for ad in ads]
    # Podatke shranimo v csv datoteko
    write_cat_ads_to_csv(ads_nice, cat_directory, csv_filename)


if __name__ == '__main__':
   main()