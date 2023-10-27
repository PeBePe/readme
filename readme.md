# PBP Kelompok A03 - ReadMe
<details>
    <summary>Anggota Kelompok</summary>

## Anggota Kelompok
- Muhammad Daffa'I Rafi Prasetyo (2206029191)
- Rafi Irsyad Saharso (2206082221)
- Khalisha Hana Aida Putri (2206081484)
- Fahmi Ramadhan (2206026473)
- Nabiilah Putri Safa (2206030426)
</details>

<details>
    <summary>Cerita Aplikasi</summary>


## Cerita Aplikasi
Aplikasi ReadMe adalah aplikasi yang kami buat untuk meningkatkan tingkat literasi di kalangan masyarakat Indonesia dari segala usia. Aplikasi ini menawarkan serangkaian fitur yang memungkinkan pengguna untuk berinteraksi dengan dunia literasi dan buku dengan sangat menarik. Berikut adalah beberapa fitur utama dari aplikasi ReadMe:

1. Loyalty Point :
Pengguna akan mendapatkan loyalty points sebagai bentuk penghargaan setiap kali mereka berkontribusi dalam aplikasi. Loyalty points dapat dikumpulkan dan diperoleh melalui berbagai kegiatan seperti memberikan review, membagikan posting, atau membuat quotes. Hal ini dapat memberikan insentif bagi pengguna untuk menambah semangat membaca dan berliterasi.

2. Review Buku:
Pengguna dapat memberikan ulasan terhadap buku-buku yang telah mereka baca. Setiap ulasan memberikan pengguna loyalty points, yang dapat dikumpulkan dan digunakan untuk membeli lebih banyak buku di dalam fitur shop. Ini mendorong pengguna untuk semangat berpartisipasi aktif dalam aplikasi.

3. Posting:
Fitur Posting memungkinkan pengguna untuk berbagi pemikiran, ulasan, diskusi, atau rekomendasi terkait buku. Terdapat fitur like di tiap postingan, dan pengguna mendapatkan loyalty points berdasarkan jumlah like yang diterima. Hal ini tentu dapat menciptakan interaksi sosial yang lebih aktif dan memperluas wawasan literasi.

4. Quotes:
Pengguna dapat membuat quote inspiratif atau berbagi quote dari buku yang mereka suka. Mereka dapat mengutip maksimal tiga quote dari orang lain. Quotes yang dikutip ini akan ditampilkan pada halaman profil pengguna, memberikan pengguna kesempatan untuk berbagi pemikiran dan ide-ide favorit mereka. Loyalty points diberikan berdasarkan jumlah quote buatan pengguna yang dikutip oleh pengguna lain.

5. Shop dan Penggunaan Loyalty Points:
Fitur Shop memungkinkan pengguna untuk menggunakan loyalty points yang mereka kumpulkan untuk mendapatkan buku yang mereka inginkan. Ini menciptakan insentif tambahan bagi pengguna untuk terus berpartisipasi dalam komunitas literasi dan memberikan nilai nyata pada setiap kontribusi mereka.

6. Wishlist:
Pengguna dapat membuat daftar buku yang ingin mereka baca di masa mendatang melalui fitur Wishlist. Hal ini memudahkan pengguna untuk melacak dan menemukan buku-buku yang menarik minat mereka.

Dengan fitur-fitur ini, Kami berharap aplikasi ReadMe tidak hanya menjadi platform literasi yang interaktif tetapi juga dapat membangun komunitas di sekitar kecintaan terhadap membaca. Aplikasi ini bertujuan untuk menciptakan lingkungan yang mendukung pertukaran ide dan pengalaman literasi, menjadikan literasi sebagai pengalaman yang lebih berharga.
</details>

<details>
    <summary>Daftar modul</summary>

## Daftar Modul
Berikut adalah modul-modul yang akan kami implementasikan.
1. Modul Review (PIC: Muhammad Daffa'I Rafi Prasetyo) :
    - Pengguna bisa memberikan review terhadap buku. (Create)
    - Pengguna bisa melihat review yang diberikan oleh dirinya dan Pengguna yang lain. (Read)
    - Pengguna bisa menghapus review miliknya. (Delete)
    - Pengguna bisa mengedit review yang diberikan. (Update)
    - Pengguna akan mendapatkan loyalty setiap review yang ia diberikan.
    - Loyalty bisa digunakan untuk menukar buku pada shop.
1. Modul Shop (PIC: Fahmi Ramadhan) :
    - Pengguna bisa melihat list buku yang dapat ditukar beserta stok dll. (View)
    - Pengguna bisa melihat detail buku. (View)
    - Pengguna bisa memasukkan buku ke keranjang. (Create).
    - Pengguna bisa mengedit stok buku yang hendak dibeli pada keranjang. (Update)
    - Pengguna bisa checkout buku yang berhasil masuk ke keranjang, dan buku yang di keranjang akan menjadi kosong. (Delete)
    - Poin loyalty Pengguna akan berkurang sesuai total harga yang tertulis di keranjang. (Update)
    - Setelah berhasil membeli buku, buku yang berada pada toko akan berkurang (Update)
    - Buku yang berhasil di checkout masuk ke inventory Pengguna (Create).
2. Modul Post (PIC: Rafi Irsyad Saharso) :
    - Pengguna bisa membagikan sesuatu dalam bentuk posting yang berkaitan dengan buku (Create)
    - Pengguna bisa melihat postingan orang lain (View)
    - Pengguna bisa mengedit postingan miliknya sendiri (Update)
    - Pengguna bisa menghapus postingan miliknya sendiri (Delete)
    - Pengguna bisa memberikan like terhadap postingan (Update)
    - Pengguna mendapatkan sejumlah loyalty poin tiap like yang di dapat dari postingannya (Update)
3. Modul Quotes (PIC: Khalisha Hana Aida Putri) :
    - Pengguna bisa membuat quotes, hanya 1 quote diperbolehkan untuk 1 akun (Create)
    - Pengguna bisa mencari dan melihat quotes buatan orang lain (View)
    - Pada tampilan daftar quotes, akan ditampilkan berapa banyak quote tersebut digunakan oleh Pengguna lain. (View)
    - Pengguna dapat mengutip quotes buatan orang lain sebanyak maksimal 3 quotes (Update)
    - Quotes yang dikutip oleh pengguna akan tampil pada halaman profile (Update).
    - Pembuat quote akan mendapatkan sejumlah poin loyalty tiap quote buatannya dikutip oleh Pengguna lain. (Update)
    - Pengguna dapat menghapus quotes buatannya sendiri (Delete)
    - Pengguna dapat mengedit quotes buatannya sendiri (Update)
4. Modul Wishlist (PIC: Nabiilah Putri Safa) : 
    - Pengguna bisa menambahkan buku ke wishlist. (Create).
    - Pengguna bisa membuat note saat menambahkan buku ke wishlist (Create).
    - Pengguna bisa mengedit/menghapus note yang sudah dibuat sebelumnya (Update).
    - Terdapat halaman untuk menampilkan buku-buku yang sudah dimasukkan ke wishlist (View).
    - Pengguna bisa menggunakan fitur search untuk mencari buku yang sudah dimasukkan ke wishlist (View).
    - Pengguna bisa menghapus buku dari wishlist (Delete).

</details>

<details>
    <summary>Sumber Dataset</summary>

## Sumber Dataset
[Google Books API](https://developers.google.com/books)

Kami memilih Google Books API karena API tersebut menyediakan akses ke koleksi buku yang sangat luas dan bervariasi, memungkinkan pengguna aplikasi untuk menemukan buku sesuai dengan preferensi mereka. API ini menyediakan informasi lengkap tentang setiap buku, termasuk detail seperti judul, pengarang, ringkasan, dan sampul buku. Dengan kelengkapan data seperti ini, pengguna dapat dengan mudah menelusuri dan menemukan buku yang mereka cari. Google Books API dukungan dan dokumentasi yang baik dan lengkap dari Google, harapannya pengembangan aplikasi nantinya akan menjadi lebih efisien. Keberagaman dan kelengkapan data yang diberikan oleh Google Books API menjadikannya pilihan yang kuat untuk membangun aplikasi yang bertemakan literasi dan berbagi pengalaman membaca.

</details>

<details>
    <summary>Role Pengguna</summary>

## Role Pengguna
Hanya terdapat 1 role pada aplikasi kami yaitu role Pengguna atau User yang dapat mengakses semua fitur diatas. User memiliki akses penuh ke seluruh fitur aplikasi, termasuk memberikan ulasan terhadap buku, membuat posting, menciptakan kutipan, berbelanja dengan loyalty points, dan mengelola daftar buku di Wishlist. Mereka dapat berpartisipasi secara aktif dalam aplikasi kami, berinteraksi dengan pengguna lain, dan mendapatkan loyalty points sebagai bentuk penghargaan atas kontribusi mereka dalam membangun pengalaman berliterasi dan membaca.
</details>



