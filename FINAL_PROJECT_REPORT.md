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

![docker compose up -d](/docs/image.png)

(Membangun ulang image sebelum menjalankan container, semisal kita ngambil clone git dari sini jika sudah pernah atau sudah ada tinggal langsung jalankan)

```bash
 docker compose up -d
```

![jalankan docker ](/docs/image-1.png)

### 3. Pastikan Container Berjalan

```bash
docker ps
```

![docker compose ps](/docs/image-2.png)

### 4. Buat migration dahulu

```bash
docker compose exec app python manage.py makemigrations
```

![makemigrations](/docs/image-3.png)

### 5. Jalankan migration

```bash
docker compose exec app python manage.py migrate
```

![migrate](/docs/image-4.png)

### 6. Seed data (karena database masih kosong setelah migration)

```bash
docker compose exec app python manage.py seed_data
```

![seed_data](/docs/image-5.png)

### 7. Jika Ingin Memberhentikan Project

```bash
docker compose stop
```

![stop](/docs/image-31.png)

### 8. Akses Aplikasi

Django Admin Panel

```text
http://localhost:8000/admin/
```

![django Admin](/docs/image-6.png)

Django Silk

```text
http://localhost:8000/silk/
```

![silk](/docs/image-7.png)

Swagger:

```text
http://localhost:8000/api/docs
```

![swanger](/docs/image-8.png)

Flower :

```text
http://localhost:5555/
```

![flower](/docs/image-9.png)

Rabbit MQ :

```text
http://localhost:15672/
```

![rabbitmq](/docs/image-10.png)

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

### Login API

![Login Mahasiswa](/docs/image-11.png)
![Login Dosen](/docs/image-12.png)
![Login Admin](/docs/image-13.png)

### Email notification async

![Mahasiswa - Enroll Async](/docs/image-14.png)
![Dosen - Enroll Async ](/docs/image-15.png)
![Cek di Celery Berhasil](/docs/image-16.png)
![Log Email Terkirim](/docs/image-17.png)

### Generate certificate/report async

![Complete Course Mahasiswa (Generate Certificate)](/docs/image-18.png)
![Complete Course Dosen (Generate Certificate)](/docs/image-19.png)
![Cek Certificate di Celery Berhasil](/docs/image-20.png)
![Cek File Certificate](/docs/image-21.png)

![Export Complete](/docs/image-22.png)
![Cek Exporty di Celery Berhasil](/docs/image-23.png)
![Cek File report](/docs/image-24.png)

### Scheduled task

![Log Celery Beat Berjalan](/docs/image-25.png)
![Cek di Flower (Task SUCCESS)](/docs/image-26.png)
![Detail Statistics](/docs/image-27.png)

### TASK STATUS ENDPOINT

![Task Status Response](/docs/image-28.png)

### Flower monitoring

![Flower Monitoring](/docs/image-29.png)

### Rabbit MQ

![RabbitMQ Berjalan](/docs/image-30.png)

## Kendala dan Solusi

### Kendala

- File hasil generate Celery tidak sinkron dengan folder di host karena celery-worker tidak memiliki volume mount untuk media, dan task menggunakan path relatif sehingga file tersimpan di root container
- Task export_course_report gagal dengan error NameError: name 'MEDIA_ROOT' is not defined karena MEDIA_ROOT tidak didefinisikan di dalam task, dan Celery Worker tidak membaca variable global yang didefinisikan di luar task
- Endpoint async (enroll_async, complete_course_async, export_report_async) hanya mengembalikan pesan sukses tanpa task_id, sehingga user tidak bisa mengecek status task yang sedang berjalan

### Solusi

- Menambahkan volume mount ./media:/app/media pada service celery-worker di docker-compose.yml setelah itu mengubah path penyimpanan menggunakan settings.MEDIA_ROOT agar file tersimpan di /app/media/ yang ter-mount ke host
- Mengganti MEDIA_ROOT dengan settings.MEDIA_ROOT di dalam task export_course_report, kemudian melakukan restart ulang Celery Worker agar kode terbaru terbaca
- Menambahkan return task_id pada setiap response endpoint async dengan menyimpan hasil task.delay() terlebih dahulu, sehingga user bisa langsung mengecek status task melalui endpoint /tasks/{task_id}

## Kesimpulan

Final project Simple LMS ini memberikan pengalaman berharga dalam memahami implementasi Pemrograman Sistem Skala Besar secara langsung. Proyek ini berhasil mengintegrasikan teknologi modern seperti Docker dengan 8 service, PostgreSQL sebagai database utama, JWT untuk autentikasi tiga role, serta Celery dan RabbitMQ untuk asynchronous processing pada pengiriman email, pembuatan sertifikat PDF, dan ekspor laporan CSV. Celery Beat menjalankan task periodik update statistik, dan tersedia endpoint task status untuk memantau proses async. Redis digunakan untuk cache, MongoDB untuk logging aktivitas, serta Flower dan Django Silk untuk monitoring dan profiling. Dokumentasi API tersedia via Swagger/OpenAPI. Sepanjang pengerjaan, berbagai kendala teknis berhasil diatasi, memperdalam pemahaman tentang Django REST Framework dan arsitektur microservices. Proyek ini menjadi fondasi kuat untuk pengembangan sistem modern ke depannya.

```



