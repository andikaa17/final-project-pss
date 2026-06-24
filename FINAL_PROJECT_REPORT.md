# Final Project Learning Management System (LMS)

## Identitas Mahasiswa

- **Nama:** Andika Apriyanto
- **NIM:** A11.2023.15341
- **Kelas:** A11.4618
- **Repository:** https://github.com/andikaa17/final-project-pss.git

---

## Deskripsi Project

Simple LMS adalah sistem manajemen pembelajaran (Learning Management System) berbasis web yang dikembangkan menggunakan Django Rest Framework dan diintegrasikan dengan berbagai teknologi modern untuk mendukung pemrosesan asynchronous, caching, dan analitik. Proyek ini merupakan pengembangan dari sistem LMS dasar yang ditingkatkan dengan fitur-fitur advanced seperti Celery untuk background task, Redis untuk caching, MongoDB untuk penyimpanan log aktivitas, dan RabbitMQ sebagai message broker.

Sistem ini memungkinkan pengguna dengan peran yang berbeda (Admin, Instructor, Student) untuk mengelola course, melakukan enrollment, melacak progress belajar, dan menghasilkan sertifikat serta laporan secara otomatis. Fitur-fitur tersebut diproses secara asynchronous menggunakan Celery agar pengguna tidak perlu menunggu lama.

---

## Fitur Dasar yang Sudah Berjalan

- Project dapat dijalankan dengan Docker Compose
- Database PostgreSQL berjalan dan migration berhasil
- Authentication JWT berjalan
- Role admin, instructor, student diterapkan dengan benar
- Endpoint course, lesson, enrollment, progress berjalan
- README berisi cara menjalankan, akun demo, dan endpoint utama
- Swagger/OpenAPI dapat diakse
- Struktur project rapi, tidak hardcode konfigurasi sensitif

---

## Fitur Tambahan yang Dipilih - SYNC PROCESSING & NOTIFICATION

| No  | Fitur                             | Fokus Implementasi                       | Poin | Status  |
| --- | --------------------------------- | ---------------------------------------- | ---- | ------- |
| 1   | Email notification async          | Email/mock email dikirim melalui Celery. | 12   | Selesai |
| 2   | Generate certificate/report async | Proses berat sebagai background task.    | 18   | Selesai |
| 3   | Scheduled task                    | Celery beat menjalankan task berkala.    | 15   | Selesai |
| 4   | Task status endpoint              | User mengecek status task                | 12   | Selesai |
| 5   | Flower monitoring                 | Monitoring Celery di Docker Compose      | 8    | Selesai |

\*\*Total Poin: 65

---

## Penjelasan Implementasi - SYNC PROCESSING & NOTIFICATION

Proyek ini mengimplementasikan sistem pemrosesan asynchronous menggunakan Celery dan RabbitMQ untuk menangani tugas-tugas berat di latar belakang. Tujuan utamanya adalah meningkatkan pengalaman pengguna dengan tidak membuat mereka menunggu saat menjalankan proses seperti pengiriman email, pembuatan sertifikat, dan ekspor laporan.

### Email notification async

Fitur ini mengirimkan email notifikasi secara asynchronous saat pengguna berhasil mendaftar ke suatu course. Ketika pengguna mengakses endpoint /api/enrollments-async, sistem langsung mencatat enrollment dan mengembalikan respons tanpa menunggu email terkirim. Tugas pengiriman email kemudian dikirim ke Celery melalui RabbitMQ untuk diproses di latar belakang. Implementasi ini menggunakan task send_enrollment_email yang terdapat pada courses/tasks.py dan dipanggil menggunakan metode .delay() pada endpoint enroll_async. Dengan pendekatan ini, pengguna tidak perlu menunggu hingga email benar-benar terkirim, sehingga respons aplikasi menjadi lebih cepat.

### Generate certificate/report async

Fitur ini menangani pembuatan sertifikat PDF dan laporan CSV secara asynchronous. Pada proses generate certificate, pengguna menyelesaikan course melalui endpoint /api/courses/{id}/complete-async, kemudian Celery Worker langsung memproses pembuatan sertifikat PDF di latar belakang. File PDF yang dihasilkan disimpan di folder media/certificates/. Untuk ekspor laporan, admin atau teacher dapat mengakses endpoint /api/courses/{id}/export-async untuk menghasilkan laporan CSV yang juga diproses secara asynchronous dan disimpan di folder media/reports/. Implementasi ini menggunakan task generate_certificate dengan library reportlab untuk generate PDF, serta task export_course_report dengan library csv untuk generate laporan. Kedua task ini memastikan bahwa proses berat tidak menghambat pengguna lain.

### SCHEDULED TASK - CELERY BEAT

Fitur ini menjalankan tugas secara periodik menggunakan Celery Beat. Terdapat dua tugas utama yang dijadwalkan secara berkala. Pertama, update_course_statistics yang berjalan setiap jam untuk menghitung jumlah member di setiap course dan memperbarui data statistik. Kedua, send_daily_report yang berjalan setiap tengah malam untuk mengirim laporan harian kepada admin melalui email. Konfigurasi jadwal ini ditetapkan di dalam file celery.py menggunakan crontab, dengan schedule crontab(minute=0, hour='\*/1') untuk tugas per jam dan crontab(hour=0, minute=0) untuk tugas harian. Kedua task ini memastikan bahwa pembaruan data dan laporan berjalan otomatis tanpa campur tangan manual.

### TASK STATUS ENDPOINT

Fitur ini memungkinkan pengguna untuk mengecek status tugas asynchronous yang sedang berjalan. Pengguna dapat mengakses endpoint /api/tasks/{task_id} untuk melihat informasi lengkap tentang suatu task, termasuk status saat ini (PENDING, STARTED, SUCCESS, atau FAILURE), pesan status yang informatif, hasil tugas jika sudah selesai, dan waktu penyelesaian jika task telah sukses. Implementasi ini menggunakan AsyncResult dari Celery untuk mengambil informasi task berdasarkan task_id yang diberikan. Endpoint ini sangat berguna bagi pengguna untuk memantau progres tugas yang memakan waktu lama, seperti pembuatan sertifikat atau ekspor laporan.

### FLOWER MONITORING

Fitur ini menyediakan antarmuka monitoring untuk memantau aktivitas Celery secara real-time. Flower dapat diakses melalui http://localhost:5555 dan menampilkan informasi penting seperti status worker yang sedang online, daftar task yang telah dijalankan beserta statusnya (SUCCESS, FAILURE, atau PENDING), serta informasi broker RabbitMQ yang terhubung. Dengan Flower, pengembang dapat dengan mudah memantau kesehatan sistem dan mendeteksi jika terjadi kegagalan pada task-task Celery. Flower berjalan sebagai container terpisah di Docker Compose dan terhubung langsung dengan Celery Worker dan RabbitMQ.

### Kesimpulan

Semua fitur di atas bekerja secara terintegrasi untuk menciptakan sistem asynchronous processing yang handal. Celery bertindak sebagai task queue yang menangani eksekusi tugas di latar belakang, RabbitMQ berfungsi sebagai message broker yang mengantarkan tugas dari Django ke Celery Worker, dan Flower menyediakan antarmuka monitoring untuk memudahkan pengawasan. Seluruh sistem ini dikemas dalam container Docker sehingga mudah dijalankan dan diskalakan. Pendekatan asynchronous ini memastikan bahwa aplikasi tetap responsif meskipun sedang memproses tugas-tugas berat, sehingga memberikan pengalaman pengguna yang lebih baik.

---

## Cara Menjalankan Project

### 1. Clone Repository

```bash
git clone https://github.com/andikaa17/final-project-pss.git
```

### 2. Jalankan Docker Compose

```bash
docker compose up --build
```

(Membangun ulang image sebelum menjalankan container, semisal kita ngambil clone git dari sini jika sudah pernah atau sudah ada tinggal langsung jalankan)

```bash
 docker compose up -d
```

![jalankan docker ](/docs/image-22.png)

### 3. Pastikan Container Berjalan

```bash
docker ps
```

![docker compose ps](/docs/image-21.png)

### 4. Buat migration dahulu

```bash
docker compose exec app python manage.py makemigrations
```

![makemigrations](/docs/image-23.png)

### 5. Jalankan migration

```bash
docker compose exec app python manage.py migrate
```

![migrate](/docs/image-24.png)

### 6. Seed data (karena database masih kosong setelah migration)

```bash
docker compose exec app python manage.py seed_data
```

![seed_data](/docs/image-25.png)

### 7. Jika Ingin Memberhentikan Project

```bash
docker compose stop
```

![stop](/docs/image-26.png)

### 4. Akses Aplikasi

````

Django Admin Panel

```text
http://localhost:8000/admin/
````

Django Silk

```text
http://localhost:8000/silk/
```

Swagger:

```text
http://localhost:8000/api/docs
```

Flower :

```text
http://localhost:5555/
```

Rabbit MQ :

```text
http://localhost:15672/
```

---

## Akun Demo

### Admin

```text
Email    : admin
Password : admin123
```

### Instructor

```text
Email    : dosen01
Password : dosen123
```

### Student

```text
Email    : mhs001
Password : mahasiswa123
```

---

## Endpoint Penting

```http
AUTHENTICATION
  [Login]       POST   /api/auth/login

ASYNC TASKS (Celery)
  [Enroll Async]         POST   /api/enrollments-async
  [Complete Course]      POST   /api/courses/{id}/complete-async
  [Export Report]        POST   /api/courses/{id}/export-async
  [Update Stats]         POST   /api/admin/update-stats
  [Task Status]          GET    /api/tasks/{task_id}

MONITORING
  [Flower]               GET    http://localhost:5555
  [RabbitMQ]             GET    http://localhost:15672

```

---

## Screenshot / Bukti Pengujian

### Swagger Documentation

![Swagger](/docs/image-20.png)

### Login API

![Login Mahasiswa](image.png)
![Login Dosen](/docs/image-1.png)
![Login Admin](/docs/image-2.png)

### Email notification async

![Mahasiswa - Enroll Async](/docs/image-3.png)
![Dosen - Enroll Async ](/docs/image-4.png)
![Cek di Celery Berhasil](/docs/image-5.png)
![Log Email Terkirim](/docs/image-6.png)

### Generate certificate/report async

![Complete Course Mahasiswa (Generate Certificate)](/docs/image-7.png)
![Complete Course Dosen (Generate Certificate)](/docs/image-8.png)
![Cek Certificate di Celery Berhasil](/docs/image-9.png)
![Cek File Certificate](/docs/image-10.png)

![Export Complete](/docs/image-11.png)
![Cek Exporty di Celery Berhasil](/docs/image-12.png)
![Cek File report](/docs/image-13.png)

### Scheduled task

![Log Celery Beat Berjalan](/docs/image-14.png)
![Cek di Flower (Task SUCCESS)](/docs/image-15.png)
![Detail Statistics](/docs/image-16.png)

### TASK STATUS ENDPOINT

![Task Status Response](/docs/image-17.png)

### Flower monitoring

![Flower Monitoring](/docs/image-18.png)

### Rabbit MQ

## ![RabbitMQ Berjalan](/docs/image-19.png)

## Kendala dan Solusi

### Kendala

- Container tidak bisa terhubung ke PostgreSQL karena konfigurasi host masih localhost
- File hasil generate Celery tidak sinkron dengan folder host
- Celery menggunakan Redis sebagai broker, padahal tugas meminta RabbitMQ

### Solusi

- Mengubah HOST di settings.py menjadi database sesuai nama service di docker-compose.yml
- Menambahkan volume mount ./media:/app/media pada service celery-worker dan menggunakan MEDIA_ROOT di tasks.py
- Mengubah CELERY_BROKER_URL dari redis:// menjadi amqp://rabbitmq:1234@rabbitmq:5672//

## Kesimpulan

FMengerjakan final project Simple LMS ini memberikan pengalaman yang sangat berharga dalam memahami implementasi Pemrograman Sistem Skala Besar secara langsung. Proyek ini berhasil mengintegrasikan berbagai teknologi modern seperti Docker untuk containerization dengan 8 service yang berjalan terintegrasi, PostgreSQL sebagai database utama, JWT untuk autentikasi dengan tiga role (Admin, Instructor, Student), serta Celery dan RabbitMQ untuk asynchronous processing dalam pengiriman email notifikasi, pembuatan sertifikat PDF, dan ekspor laporan CSV. Celery Beat digunakan untuk menjalankan task periodik seperti update statistik course secara otomatis, dan terdapat endpoint task status untuk memantau proses async yang sedang berjalan. Selain itu, Redis dimanfaatkan sebagai cache untuk optimasi query, MongoDB untuk logging aktivitas pengguna, serta Flower dan Django Silk untuk monitoring Celery dan profiling query database. Dokumentasi API tersedia melalui Swagger/OpenAPI dan seluruh konfigurasi sensitif dikelola menggunakan environment variables. Sepanjang pengerjaan, berbagai kendala teknis berhasil diatasi, mulai dari konfigurasi Docker Compose, implementasi JWT authentication, hingga integrasi Celery untuk background task. Pengalaman ini tidak hanya memperdalam pemahaman tentang Django REST Framework, tetapi juga membuka wawasan tentang bagaimana aplikasi skala enterprise dibangun dengan arsitektur microservices yang scalable, reliable, dan terintegrasi dengan berbagai teknologi pendukung. Secara keseluruhan, proyek ini menjadi fondasi yang kuat dalam memahami pengembangan sistem modern dan siap diaplikasikan pada proyek-proyek selanjutnya.
