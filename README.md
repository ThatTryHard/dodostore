### PWS : http://orlando-devito-dodostore.pbp.cs.ui.ac.id
### Github : https://github.com/ThatTryHard/dodostore

- 1. Untuk membuat project django baru, pertama saya menggunakan command `python -m venv` env pada direktori utama yang akan saya gunakan untuk menyimpan projek utama saya, yang akan digunakan untuk mengisolasi package dan dependencies agar tidak mengalami conflicts dengan package lain. kemudian saya mengaktifkan virtual environment saya dengan command `env\Scripts\activate`. Dan pada direktori yang sama, saya membuat file `requirements.txt` yang berisikan dependencies untuk projek Djangonya, yaitu django, gunicorn, whitenoise, psycopg2-binary, requests, dan urllib3. Lalu dengan command `pip install -r requirements.txt` yang dijalankan dengan environment yang sedang aktif, akan menginstall semua library ini ke dalam sistem. Setelah semua terinstall, saya menggunakan command `django-admin startproject dodo_store .` untuk menginisiasi projek baru bernama `dodo_store` di direktori utama. Untuk kebutuhan deployment, saya menambahkan host pada `ALLOWED_HOSTS` di `settings.py`, yaitu `localhost` dan `127.0.0.1` agar dapat ditampilkan dalam jaringan saya. Setelah melakukan ini, saya dapat melihat animasi roket ketika membuka http://localhost:8000/ yang menandakan saya berhasil dalam penginstallan Django ini. Setelah semua terinstall, saya menutup servernya dengan command `deactivate` pada Command Prompt saya.

  2. Untuk membuat aplikasi pada project django saya, pertama saya membuka direktori utama proyek Djangonya, kemudian dengan command `env\Scripts\activate` saya mengaktifkan virtual environmentnya. Setelah itu, saya menjalankan command `python manage.py startapp main` untuk membuat aplikasi bernama `main`. Setelah aplikasi main sudah ada di direktori, saya menambahkan `main` kedalam variabel `INSTALLED_APPS` di dalam berkas `settings.py` pada direktori proyek `dodo_store`.

  3. Untuk routing, pertama saya melakukan pengubahan di berkas `urls.py` di dalam direktori proyek `dodo_store` yang berisikan:
    ```python 
    from django.contrib import admin
    from django.urls import path, include

    urlpatterns = [
        path('admin/', admin.site.urls),
        path('', include('main.urls')),
    ]
    ```
     berkas file `urls.py` di direktori proyek `dodo_store` ini mengatur rute URL keseluruhan proyek, saya menggunakan `include` untuk mengimpor semua rute URL yang ada di `main` ke dalam proyek `dodo_store`. Dan pada path `''` diarahkan ke rute `main`, agar dapat diakses langsung.

  4. Untuk membuat model `Product` pada aplikasi `main`, saya membuka berkas `models.py` di direktori aplikasi `main` terlebih dahulu. Kemudian saya menambahkan class Product yang sebagai berikut:
  ```python
  from django.db import models
    
  class Product(models.Model):
      name = models.CharField(max_length=255)  #Product name
      price = models.IntegerField()  # Product price
      description = models.TextField()  # Product description

      stock = models.IntegerField(default=0)  # Product in stock
      category = models.CharField(max_length=100, blank=True, null=True)  # Product category

      def product_info(self):
          return f"{self.name} - Rp. {self.price:,} - {self.stock} is in stock - {self.category} category."
  ```
     dengan `models.Model` sebagai pendefinisian model di Django, dan `Product` sebagai nama model, saya mendefinisikan `name`, `price`, dan `description` sebagai atribut yang diwajibkan dengan menerima tipe data yang sesuai juga.Saya juga menambahkan atribut `stock` dan `category` sebagai atribut tambahan, serta fungsi `product_info()` yang akan mengembalikan informasi dari produknya. Setelah pembuatan model ini, saya membuat beberapa tests di `tests.py` untuk mengecek apakah prosesnya dapat dilakukan dengan tepat. dengan berkas yang sebagai berikut:
     ```python
     from django.test import TestCase, Client
     from django.utils import timezone
     from .models import Product

     class mainTest(TestCase):
         def test_main_url_is_exist(self):
             response = Client().get('')
             self.assertEqual(response.status_code, 200)

         def test_main_using_main_template(self):
             response = Client().get('')
             self.assertTemplateUsed(response, 'main.html')

         def test_nonexistent_page(self):
             response = Client().get('/nonexistant/')
             self.assertEqual(response.status_code, 404)

         def test_product_exist(self):
             product = Product.objects.create(
             name="Aqua",
             price = 4000,
             description = "a bottle of drinking water from the Aqua brand",
             stock = 1000,
             category = "Beverage",
             )
             self.assertTrue("Aqua - Rp. 4,000 - 1000 is in stock - Beverage category." == product.product_info())
     ```
     tests yang dijalankan adalah test untuk mengecek url main, apakah main menggunakan templatenya, test untuk mengecek halaman yang tidak ada, dan test untuk mengecek apakah produk ada atau tidak.

  5. Untuk menghubungkan views dengan template pada proses MVT, dapat dilakukan dengan cara membuat fungsi pada `views.py` di direktori aplikasi `main`. fungsi yang saya implementasikan ada 3, yaitu `show_main` dan `product_list`.
  ```python
  def show_main(request):
      context = {
          'app_name' : 'Dodo Store',
          'name': 'Orlando Devito',
          'class': 'PBP A'
      }

      return render(request, "main.html", context)

  def product_list(request):
      # Take all Product data from the database
      products = Product.objects.all()
      return render(request, 'product_list.html', {'products': products})
  ```
     yang diminta secara detail hanya fungsi `show_main`, yang diminta mengembaikan nama aplikasi, nama saya, dan kelas saya untuk ditampilkan pada berkas `main.html` saya. untuk `product_list` tidak diberikan permintaan yang detail, sehingga saya mengambil semua data dari databasenya, dengan render request yang mengimplementasikan **Context Dictionary** yang berisi list dari tiap product yang ada di database.

  6. untuk routing URL di direktori aplikasi `main`, pertama saya membuat berkas file `urls.py` di direktori `main`, dan mengisi berkasnya sebagai berikut:
  ```python
  from django.urls import path
  from . import views

  app_name = 'main'

  urlpatterns = [
      path('', views.show_main, name='main'),
      path('products/', views.product_list, name='product_list'),
  ]
  ```
     berkas `urls.py` ini mengatur routing untuk tiap URL di aplikasi `main`. Untuk mendefinisikan pola URL, saya mengimpor `path` dari `django.urls`. dan saya menggunakan fungsi `show_main` dan `product_list` dari `main.views` sebagai unit untuk menampilkan data-data ketika URL diakses. `app_name` digunakan untuk menampilkan nama unik di aplikasi.

  7. Untuk mendeploy ke halaman PWS, pertama akses terlebih dahulu alamat https://pbp.cs.ui.ac.id/ dan melakukan registerasi. Setelah registerasi selesai, lakukan login dan akan di redirect ke halaman utama. Setelah itu, saya menekan tombol `+ Create new Project` dan mengisi **Project Name** dengan `dodostore` dan saya menginisiasi pembuatan project baru dengan nama tersebut. Lalu, pada berkas `settings.py` di direktori project `dodo_store`, pada variabel `ALLOWED_HOSTS`, saya menambahkan host baru yaitu `orlando-devito-dodostore.pbp.cs.ui.ac.id` yang merupakan URL depoloyment PWS saya. Setelah itu saya push ke github saya dan menjalankan command `git remote add pws http:/pbp.cs.ui.ac.id/orlando.devito/dodostore` untuk menginisiasi link remote repository baru yang terhubung dengan PWS saya. Setelah itu saya mengakses branch `master` dengan cara menjalankan `git branch -M master`, dan terakhir saya push ke PWS dengan cara menjalankan `git push pws master`. Cara saya mengecek apakah saya berhasil atau tidak yaitu saya melihat status projectnya, jika statusnya `running` dan ketika tombol `View Project` ditekan dan tidak error, berarti bahwa saya telah berhasil push ke PWS saya.

-  ```mermaid
        graph TD;
            Client -->|Request| urls.py;
            urls.py -->|Maps Request| views.py;
            views.py -->|Access Data| models.py;
            models.py -->|Provides data| views.py;
            views.py -->|Renders data| template.html;
            template.html -->|Sends response| Client;
   ```

    Dari sisi client, menggunakan HTTP protocol dari browser akan meminta request ke `urls.py`, dan Django akan memeriksa `urls.py` untuk mencari URL yang sesuai dengan yang direquest oleh client. ketika sudah sesuai, Django akan mengarahkan request tersebut ke fungsi yang ada di `views.py`, yang bertanggung jawab untuk memproses logika dari requestnya pada aplikasi, dan jika terdapat query data yang dibutuhkan baik untuk diakses saja atau dimanipuasi dari database, dia akan mengakses `models.py`, yang mengelola struktur database dari project Django melalui ORM Django. Jika `views.py` membutuhkan data dari database, `models.py` akan melakukan query untuk mengambil atau meyimpan data. Ketika data sudah diperoleh, `views.py` akan mengirim data tersebut ke template HTML dengan data yang telah diambil dari `models.py` dan dirender menggunakan data tersebut sebagai response HTML yang akan ditampilkan di browser klien, yang dimana browser tersebut akan menampilkan halaman web tersebut ke klien.

- Menurut saya, git termasuk ke dalam sistem kontrol versi yang sangat populer dalam pengembangan perangkat lunak karena fungsinya yang efisien untuk mengelola perubahan kode, memungkinkan kolaborasi, dan melacak semua riwayat proyek. Git menyimpan tiap perubahan yang dilakukan, yang memungkinkan user untuk melihat sejarahnya, kembali ke versi sebelumnya, dan bekerja secara paralel melalui fitur branching dan merging tanpa saling mengganggu. Selain itu, Git mendeteksi dan membantu pengelolaan konflik ketika dua user membuat perubahan pada bagian kode yang sama. Sebagai sistem distribusi, Git memungkinkan user bekerja secara *offline*, sementara repositori utama berfungsi sebagai cadangan proyek. Git juga sering diintegrasikan dengan alat otomatisasi untuk mendukung proses *Continuous Integration* (CI) dan *Continuous Delivery* (CD), yang menguji dan mendistribusikan kode ke produksi. Fitur seperti *pull request* dan *code review* membantu menjaga kualitas dan keamanan kode. Jadi, Git dapat mempermudah pendeteksian bug, mempermudah pemecahan masalah, dan memastikan proyek perangkat lunak tetap terorganisir dan mudah dikelola.

- Menurut saya, Django sering dijadikan pilihan utama dalam pembelajaran pengembangan perangkat lunak karena fiturnya yang lengkap dan ramah bagi pemula. Sebagai framework yang sudah mencakup semua unit, Django menawarkan berbagai fitur bawaan seperti autentikasi, manajemen pengguna, admin panel, ORM, dan routing, sehingga pemula bisa memulai tanpa perlu menginstal dan mempelajari paket tambahan. Django juga merupakan framework *full-stack*, yang memungkinkan pengguna belajar seluruh siklus pengembangan web, mulai dari *backend* hingga *frontend*, dengan pola *Model-View-Template* (MVT) yang terstruktur. Selain itu, Django memiliki dokumentasi yang lengkap dan mudah dipahami, membantu pemula memahami konsep-konsep dasar dengan jelas. Keamanan sistem yang kuat juga dapat melindungi aplikasi dari berbagai ancaman, seperti SQL injection dan XSS, sehingga pemula dapat belajar membangun aplikasi yang aman. Serta dengan komunitas besar dan dukungan aktif dari berbagai tutorial dan kursus juga memudahkan proses pembelajaran. Kombinasi fitur lengkap, dokumentasi kuat, dan skalabilitas ini menurut saya membuat Django menjadi framework yang sangat ideal bagi pemula yang ingin belajar pengembangan perangkat lunak.

- Model pada Django disebut sebagai ORM (*Object-Relational Mapping*) karena memungkinkan pengguna bekerja dengan database menggunakan objek Python, tanpa harus menulis kueri SQL secara langsung. ORM memetakan tabel dalam database ke dalam kelas Python, dengan kolom tabel menjadi atribut kelas tersebut. Ini menyediakan abstraksi database, sehingga pengguna bisa mengelola data tanpa memahami detail teknis dari sistem basis data. Setiap model Django merepresentasikan tabel dalam database, dan operasi CRUD (*Create, Read, Update, Delete*) dilakukan dengan sintaks Pythonic yang sederhana, seperti `Product.objects.create()` untuk menambahkan data atau `Product.objects.all()` untuk membaca data. Django ORM juga mendukung relasi antar model, seperti *one-to-many* atau *many-to-many*, melalui field seperti `ForeignKey` dan `ManyToManyField`. Dengan ORM, pengguna dapat dengan mudah berpindah antara berbagai sistem basis data (seperti *MySQL*, *PostgreSQL*, atau *SQLite*) tanpa harus mengubah kode aplikasi. Fitur-fitur tersebut menjadikan Django ORM sebagai alat yang sangat berguna untuk membuat interaksi dengan database lebih mudah dan aman, serta meningkatkan portabilitas dan efisiensi pengembangan aplikasi.