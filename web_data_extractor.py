
import requests
import csv
from bs4 import BeautifulSoup
import re
import time
from urllib3.util.retry import Retry
from requests.adapters import HTTPAdapter


API_KEY = 'your_api_key'
locations = ['Denmark', 'Sweden', 'Norway']  # Aranacak ülkeler
keywords = {
    'Denmark': ['socks', 'socks retailer', 'sock store', 'buy socks online', 'sokker', 'sokker detail', 'sokkerbutik', 'køb sokker online'],
    'Sweden': ['socks', 'socks retailer', 'sock store', 'buy socks online', 'strumpor', 'strumpbutik', 'strumpor återförsäljare', 'köp strumpor online'],
    'Norway': ['socks', 'socks', 'socks retailer', 'sock store', 'buy socks online', 'sokker', 'sokker butikk', 'sokker forhandler', 'kjøp sokker online']
}


session = requests.Session()
retry = Retry(
    total=5, 
    backoff_factor=1,  # Bekleme süresi artırma faktörü
    status_forcelist=[500, 502, 503, 504],  # Hangi hatalarda tekrar edilecek
)
adapter = HTTPAdapter(max_retries=retry)
session.mount('http://', adapter)
session.mount('https://', adapter)

# Web sitesinden e-posta adresini almak için fonksiyon
def get_email_from_website(website):
    if website == 'N/A':
        return 'N/A'
    
    try:
        response = session.get(website, timeout=10)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            email = re.findall(r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b', soup.text)
            return email[0] if email else 'N/A'
    except Exception as e:
        print(f"Hata oluştu: {e}")
        return 'N/A'

contact_info_list = []
total_sites = 0

# Her ülke için anahtar kelimelerle arama yap
for location in locations:
    for keyword in keywords[location]:
        print(f"Arama yapılıyor: {keyword} in {location}")  # Arama yapılırken mesaj yazdır
        url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?query={keyword}+in+{location}&key={API_KEY}'
        
        while True:
            response = session.get(url)
            if response.status_code == 200:
                data = response.json()
                businesses = data.get('results', [])
                print(f"{len(businesses)} işletme bulundu.")  # Bulunan işletme sayısını yazdır
                
                for business in businesses:
                    if total_sites >= 1200:  # 1200 siteye ulaştığımızda işlemi durdur
                        break
                    
                    contact_info = {
                        'Name': business['name'],
                        'Address': business['formatted_address'],
                        'Rating': business.get('rating', 'N/A'),
                        'Link': f"https://www.google.com/maps/place/?q=place_id:{business['place_id']}"
                    }
                    
                    # İşletme detaylarını almak için URL oluşturma
                    details_url = f"https://maps.googleapis.com/maps/api/place/details/json?place_id={business['place_id']}&key={API_KEY}"
                    details_response = session.get(details_url)
                    
                    if details_response.status_code == 200:
                        details_data = details_response.json()
                        if 'result' in details_data:
                            phone = details_data['result'].get('formatted_phone_number', 'N/A')
                            website = details_data['result'].get('website', 'N/A')
                            contact_info['Phone'] = phone
                            contact_info['Website'] = website
                            
                            # Web sitesinden e-posta adresini al
                            contact_info['Email'] = get_email_from_website(website)
                    
                    contact_info_list.append(contact_info)
                    total_sites += 1
                    
                    # İsteği yavaşlatmak için bekleme (rate limiting)
                    time.sleep(2)  # Bekleme süresini artırdık
                
                # Eğer daha fazla sonuç varsa, next_page_token ile yeni sayfayı iste
                if 'next_page_token' in data:
                    next_page_token = data['next_page_token']
                    url = f'https://maps.googleapis.com/maps/api/place/textsearch/json?pagetoken={next_page_token}&key={API_KEY}'
                    time.sleep(2)  # API'den yeni sayfa talep etmeden önce bekleyin
                else:
                    break  # Daha fazla sayfa yoksa döngüyü kır
            else:
                print(f"API isteği başarısız oldu: {response.status_code}")
                break  # API isteği başarısız olursa döngüyü kır

# 1200 site toplanamazsa durumu kontrol et
if total_sites < 1200:
    print(f"Toplamda sadece {total_sites} site bulundu, daha fazla anahtar kelime eklemeyi deneyin.")

# Toplanan iletişim bilgilerini CSV olarak kaydet
if contact_info_list:
    keys = contact_info_list[0].keys()
    with open('socks_retailers.csv', 'w', newline='', encoding='utf-8') as output_file:
        dict_writer = csv.DictWriter(output_file, fieldnames=keys)
        dict_writer.writeheader()
        dict_writer.writerows(contact_info_list)

print(f"Toplam {total_sites} site toplandı ve 'socks_retailers.csv' dosyasına kaydedildi.")
