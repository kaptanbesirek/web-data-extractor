Web'den Veri Taraması

Bu proje, belirli ülkelerde  mesela kodumda Danimarka, İsveç, Norveç ülkelerinden perakende çorap satıcılarını bulmak ve web sitelerinden iletişim bilgilerini çıkarmak için geliştirilmiş bir web scraper uygulamasıdır.
Google Places API kullanılarak işletmeler bulunur ve web sitelerinden iletişim bilgileri ile e-posta adresleri çıkarılır. Google API kullanma sebebim, her şeyin yasal olmasını sağlamaktır.
Bu projede, belirli anahtar kelimeler ve ülkeler girilerek o ülkelerde arama motoruna yazdığımızda çıkan sayfalardan iletişim bilgileri alınmaya çalışılır.
Temel mantık, mesela global bir şirketin web sitesinde paylaştığı iletişim bilgilerini düşünün; o bilgilere herkes kolaylıkla erişebilir. 
Bu bilgileri hızlı ve düzenli bir şekilde, manuel değil, otomatik olarak bulmak amaçlanmaktadır.

Özellikler:

Birden Fazla Ülke Desteği
Gelişmiş Anahtar Kelime Araması: Ülkeye özel anahtar kelimeler kullanılarak ilgili işletmeler aranır.
CSV Çıktısı: Toplanan veriler bir CSV dosyasına kaydedilir.
Gereksinimler:

Python 3.x
requests, beautifulsoup4 ve urllib3 kütüphaneleri.
Hukuki Uyarı:

Bu proje yalnızca yasal ve etik veri kazıma uygulamaları için kullanılacak şekilde tasarlanmıştır. Yasaları veya hizmet şartlarını ihlal eden verileri kazımak için kullanılmamalıdır. Eğer bu projede herhangi bir hukuki yanlış görürseniz, lütfen bana bildirin ve hemen kaldırırım.

Lisans:

Bu proje açık kaynaklıdır ve ticari olmayan, etik veri kazıma uygulamaları için kullanılabilir.

