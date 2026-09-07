# Portfolio Web (Tugas Individu PBP)

Proyek web ini dibuat oleh

Nama : Hisyam Prasetyo \
NPM : 2506614763 \
Kelas : PBP D

sebagai tugas individu untuk mata kuliah PBP (Platform-based Programming) Fasilkom UI.
Proyek ini dibuat dengan bantuan AI Chatbot Claude Sonnet 5 dari Anthropic (Lebih detail terkait penggunaan AI tercantum di bagian [AI Disclosure](#ai-disclosure)).

## Cara Menjalankan (Lokal Linux, Mac)

Clone repository ini ke folder lokal.

``` bash
git clone https://github.com/syxm1/myportofolio
cd myportofolio
```

Di bawah direktori `myportofolio`, buat dan aktifkan python virtual environment baru.

```bash
python3 -m venv env
source env/bin/activate
```

Install requirements yang diperlukan.

```bash
pip install -r requirements.txt
```

Run command di bawah untuk mulai menjalakan web.

```bash
python manage.py runserver
```

Buka browser, masuk ke halaman `localhost:8000` untuk memuat web. Virtual environment bisa dinonaktifkan dengan command `deactivate`

```bash
deactivate
```

## AI Disclosure

Proyek ini dibuat dengan menggunakan bantuan AI Claude dengan model Sonnet 5. Strategi prompting yang  dilakukan adalah dengan memberikan attachment berupa file kode yang ingin dikerjakan ke model untuk mengatur konteks kemudian memberikan spesifikasi fitur yang ingin dibuat kepada model dan melakukan review pada kode yang digenerate model.

## Weekly Tracker

- Week 1 (31 Agustus 2026 - 7 September 2026) : Membuat static page untuk section profile, skills, dan experience.

## Pertanyaan Reflektif

### Tugas 1
1. Pada Tutorial dan Tugas 1, Anda diberi kebebasan untuk menentukan tampilan dari website portofolio Anda. Saat Anda merancang struktur HTML yang digunakan, apakah Anda menggunakan elemen semantik HTML5 seperti `<section>`, `<article>`, atau `<aside>`? Jika iya, bagaimana elemen tersebut membantu Anda dalam membuat static web? Jika tidak, mengapa tanpa elemen tersebut sudah memenuhi kebutuhan desain Anda?
```
Pada proyek ini, digunakan beberapa elemen semantik seperti <header> untuk navbar, <main> untuk konten utama, <section> untuk membagi konten pada web menjadi beberapa blok (id="profile" untuk profil, id="skills" untuk daftar skill, dan id="experience" untuk daftar pengalaman), dan <footer> untuk bagian bawah halaman. <nav> juga dipakai di dalam header untuk grup tautan navigasi.

Elemen semantik seperti <section> memang tidak berpengaruh secara visual tetapi dapat berguna untuk developer yang membaca kode untuk memberitahukan 'makna' dari konten di dalamnya (tidak seperti jika hanya menggunakan <div> biasa yang bisa berisi konten dengan makna general).
```
2. Ketika Anda mengatur CSS Anda agar tetap responsive, tantangan tata letak apa yang Anda temukan? Bagaimana Anda mengevaluasi elemen mana yang harus diubah posisinya atau diprioritaskan ukurannya saat berpindah dari tampilan desktop ke mobile?
```
Tantangan utama muncul di bagian skills dan experience. Kartu skill punya lebar tetap yang di mobile terasa terlalu lebar, jadi diperkecil ke 160px lewat breakpoint agar kartu berikutnya tetap terlihat sebagai petunjuk scroll. Di bagian experience, header kartu (judul, subtitle, tanggal) yang sejajar horizontal jadi berdesakan saat judul panjang, sehingga diubah jadi bertumpuk vertikal di layar sempit.
```
3. Website yang Anda buat saat ini adalah static web murni. Batasan apa yang Anda rasakan saat mencoba menyajikan informasi pada portofolio Anda secara optimal? Berdasarkan batasan tersebut, fungsionalitas dinamis apa yang paling ingin Anda persiapkan dan tambahkan pada iterasi proyek selanjutnya?
```
Batasan yang terdapat pada static web murni adalah minimnya interaktivitas yang bisa dilakukan antar user dan web. Fungsionalitas dinamis yang ingin diterapkan di web nantinya adalah opsi untuk user memilih menggunakan tema gelap/terang pada website ini.
```