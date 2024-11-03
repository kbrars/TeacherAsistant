## Teacher Assistant Project

Öğretmen Asistanı projesi, eğitim yönetimi görevlerini kolaylaştırmayı hedefleyen web tabanlı bir uygulamadır. Bu uygulama ile öğretmenler yapay zeka destekli sınav ve ders içeriği oluşturabilir. Aynı zamanda öğrenci geribildirimi sayesinde daha iyi bir eğitim süreci yürütebilir. 

### Özellikler

Eğitmen portalı ile eğitmen; kendi profili üzerinde bilgi değişikliğini kolaylıkla yapabilir, ilgili konu seçimi yaparak Yapay zeka destekli sınav oluşturabilir, Yapay zeka destekli ilgili konu seçimine özel materyal oluşturabilir, Geri bildirim sekmesinde öğrenciden dersle ilgili gelen geribildirimleri görebilir. 

Öğrenci portalı ile öğrenci; Ders Seçimi yaparak ilgili derse ait ders geri bildirimi yapabilir.

### Takım adı: T-NLP

## Takım üyeleri:
- Kübra Arslan **Github:** [kbrars](https://github.com/kbrars)
- Gülzade Evni  **Github:** [GülzadeEvni](https://github.com/GulzadeEvni)
- Zeynep Baydemir  **Github:** [zeynepbaydemir](https://github.com/zeynepbaydemir)


### Kullanılan Teknolojiler

- **Backend**: Python, Flask, Flask-Session
- **Veritabanı**: PostgreSQL
- **Yapay Zeka Entegrasyonu**: Google Generative AI API (Gemini)
- **Oturum Yönetimi**: Dosya tabanlı oturum saklama
- **Bağımlılıklar**: `package.json` ve `requirements.txt` dosyalarında listelenmiştir

### Dosya Yapısı

##### Ana Dizin

- **README.md**: Projeye genel bakış ve kurulum talimatlarını içerir.
- **backend/**: Backend (sunucu) kodları bu klasörde bulunur.
- **frontend/**: Frontend (istemci) kodları bu klasörde bulunur.

##### Backend Dizini (backend/)

- **main.py**: Backend sunucusunu başlatmak için ana dosya, rotalar ve servisler burada tanımlanır.
- **requirements.txt**: Backend için gereken Python bağımlılıklarını listeler.
- **app/**: Çekirdek backend uygulama dosyalarını içerir:
    - **models/**: Veritabanı modelleri (örneğin, kullanıcılar, dersler).
    - **routes/**: API uç noktaları, frontend’in çağırabileceği.
    - **services/**: İş mantığı veya veri işleme fonksiyonları.
    - **config/**: Veritabanı bağlantıları veya ortam değişkenleri gibi ayarlar.

##### Frontend Dizini (frontend/)

- **package.json**: Frontend için npm bağımlılıklarını ve betikleri içerir.
- **src/**: Frontend kaynak kodlarını barındırır:
    - **components/**: Yeniden kullanılabilir UI bileşenleri (örneğin, butonlar, formlar).
    - **views/**: Uygulamanın sayfa düzeyindeki bileşenleri.
    - **store/**: (Vuex gibi bir durum yönetim aracı varsa) Frontend için global durum.
    - **router/**: Uygulamanın sayfaları arasında geçiş sağlar.
    - **assets/**: Görseller, stiller veya diğer statik dosyalar.

Bu yapı, frontend ve backend görevlerini ayırarak proje geliştirme ve bakımını kolaylaştırır.

## Kurulum

### Gereksinimler

**Python** (3.7 veya üstü) yüklü olmalıdır.
**Node.js** (sürüm 16 veya üstü)

### Adımlar

1. Bu projeyi klonlayın:
```
git clone https://github.com/kbrars/TeacherAsistant.git
cd TeacherAsistant
```
2. Backend bağımlılıklarını kurun
```
cd backend
```

```
pip install -r requirements.txt
```
3. Backend sunucusunu çalıştırın
 ```
flask run
```
4. Frontend bağımlılıklarını kurun
```
cd ../frontend
```

```
npm install
```
5. Frontend sunucusunu çalıştırın
 ```
npm init quasar
```
 ```
quasar dev
```
7. Veritabanı Kurulumu:
Bu proje için kullanılan veritabanını yapılandırmak için `config/database` dosyasını düzenleyin. Kullanılan veritabanı hakkında bilgileri (örneğin, MongoDB, PostgreSQL vb.) burada belirtin.

## Kullanım
`http://localhost:8080` adresinden arayüze erişebilirsiniz.

### Proje içerisinden görseller:

* Kullanıcıların giriş yapabileceği giriş sayfası görseli aşağıda verilmiştir.

![loginpage](https://github.com/user-attachments/assets/ee6db956-e621-4cdd-bb72-ae0c5427d0d6)


* Eğitmenlerin bilgilerini düzenleyebileceği ve şifrelerini değiştirebileceği ekran aşağıda verilmiştir. 

![TeacherPortal](https://github.com/user-attachments/assets/9afd86b1-a5e6-4741-9f42-8e83385371bc)


* Öğrencilerin ders seçimi yaparak dersle ilgili geri bildirimlerini verebildikleri sayfa aşağıda verilmiştir. 

![studentPortal](https://github.com/user-attachments/assets/7cc1b58d-9480-4bb0-b063-b30177de414b)


* Öğrenci ders seçimi yaptıktan ve geri bildirimini oluşturduktan sonra gönder tuşuna basar ve işlemi tamamlamış olur. Bu sırada Eğitmen portalına düşen bildirim aşağıda verilmiştir. Eğitmen portalında yer alan Geri bildirimler sekmesinden eğitmen dersle ilgili geri bildirimleri görebilir.

![feedback](https://github.com/user-attachments/assets/ee4a1529-b822-4cd7-8a9e-c63061460c72)


* Eğitmen Portalını kullanan eğitmen materyal oluştur sekmesine tıklayarak istediği konuyu seçebilir. Konuyu seçtikten sonra da indirilmesi tamamlanan yapay zekanın oluşturduğu içeriğe erişebilir.  

![addmaterial](https://github.com/user-attachments/assets/9d1bfd8e-7e2c-4124-9e52-ebdd98405465)


* Eğitmen portalında yer alan 'Sınav oluştur' sekmesine tıklayarak eğitmen İlgili dersi seçebilir.

![assQuiz1](https://github.com/user-attachments/assets/608d8e4c-3e05-4590-afc7-103d4511e0da)


* Ders seçimi yaptıktan sonra da istediği konuları seçip soru sayısını belirtir. Yapay zeka tarafından ilgili test içeriği oluşturulup bilgisayarına indirilir. 

![addQuiz2](https://github.com/user-attachments/assets/6a79370d-56a2-4cc4-a51d-020925e36b06)


### Gelecekteki Geliştirmeler

- Eğitmenlerin ve öğrencilerin verdikleri geri bildirimler, yapay zeka tarafından analiz edilerek sistem geliştirme önerileri ortaya konulabilir. Bu şekilde otomatik geri bildirim analizi yapılabilir. 

- Mevcut versiyonda öğrenciler geribildirimlerini sadece yazı ile bildirebilmektedirler. Gelecekteki geliştirmeler için görme engeli bulunan öğrenciler de baz alınarak sesli kayıt alınması ve yapay zeka desteği ile sesten yazıya dönüştürme gerçekleştirilmesi planlanmaktadır. 
