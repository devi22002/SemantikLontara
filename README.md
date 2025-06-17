<p align="center">
  <h2 align="center">
    SemantikLontara
  </h2>
  Sistem Pencarian Semantik untuk Transliterasi dan Terjemahan Naskah Lontara Berbasis RDF dan SPARQL  
</p>

## 📌 Deskripsi Proyek
Sistem ini dibangun menggunakan Streamlit untuk menampilkan isi naskah Lontara — termasuk aksara asli, transliterasi Latin, dan terjemahan Bahasa Indonesia — yang terhubung ke SPARQL endpoint berbasis ontologi RDF.

## 🏛 Konteks Naskah
Naskah ini berasal dari Sulawesi Selatan dan berisi tentang Isra' Mi'raj Nabi Muhammad SAW, ditulis dalam aksara Lontara dan dimiliki oleh Nasir Kula, disalin kembali sekitar tahun 1890-an.

## ⚙️ Panduan Instalasi
### 1. Clone Repository
```bash
git clone https://github.com/devi22002/SemantikLontara.git
cd SemantikLontara
```
### 2. Instal Dependensi
```bash
pip install -r requirements.txt
```
### 3. Instalasi dan Run GraphDB (Ontotext)
* Download program GraphDB gratis dari https://graphdb.ontotext.com/
* Ikuti perintah instalasinya kemudian buka di browser menggunakan: http://localhost:7200
* Membuat Repository Baru Pada GraphDB
  1. Pada tab Setup, pilih “Repositories” kemudian “Create new repository”.
  2. Pilih “GraphDB Repository” lalu masukkan “Repository ID” dengan nama “ontology-lontara” setelah itu klik “Create”.
* Import Triples
  1. Dalam Repository yang baru dibuat, masuk ke tab “Import” kemudian pilih “Upload RDF files”.
  2. Upload file RDF (lontara-ontology.ttl).

### 4. Jalankan Aplikasi
```bash
streamlit run App.py
```
> 💡 **Catatan**: Pastikan SPARQL endpoint sudah aktif di `http://localhost:7200/repositories/ontology-lontara`. Jika belum, aplikasi akan menampilkan data lokal sebagai fallback.

## 🧑‍💻 Panduan Pengguna
### 1. Buka Browser
ke alamat yang muncul (biasanya 'http://localhost:8501')
### 2. Gunakan Sidebar untuk memilih:
![image](https://github.com/user-attachments/assets/09945d3f-46e8-49dd-b079-f670fb68296c)

* 🔍 Pencarian: Masukkan kata/frasa untuk mencari transliterasi atau terjemahan.
  ![image](https://github.com/user-attachments/assets/055f80c0-eb60-4581-b306-0bf5668c73a4)
  ![image](https://github.com/user-attachments/assets/72ab0255-761b-4d13-b2d9-653a098ecdd3)
* 📚 Jelajahi Data: Lihat seluruh isi naskah berdasarkan jenisnya (Paragraf, Kalimat, atau Kata).
  ![image](https://github.com/user-attachments/assets/7cd650b3-9e3a-4034-b341-c1abd728c735)
  ![image](https://github.com/user-attachments/assets/470d3b4a-a7b9-46f5-999f-d42bd3f49ddd)


## Lisensi
MIT License 2025
