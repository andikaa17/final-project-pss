# Final Project Learning Management System (LMS)


Simple LMS adalah sistem manajemen pembelajaran (Learning Management System) berbasis web yang dikembangkan menggunakan Django Rest Framework dan diintegrasikan dengan berbagai teknologi modern untuk mendukung pemrosesan asynchronous, caching, dan analitik. Proyek ini merupakan pengembangan dari sistem LMS dasar yang ditingkatkan dengan fitur-fitur advanced seperti Celery untuk background task, Redis untuk caching, MongoDB untuk penyimpanan log aktivitas, dan RabbitMQ sebagai message broker. Sistem ini memungkinkan pengguna dengan peran yang berbeda (Admin, Instructor, Student) untuk mengelola course, melakukan enrollment, melacak progress belajar, dan menghasilkan sertifikat serta laporan secara otomatis. Fitur-fitur tersebut diproses secara asynchronous menggunakan Celery agar pengguna tidak perlu menunggu lama.


## Model Utama :

| Model | Keterangan |
|-------|------------|
| **User** | Menyimpan data pengguna dengan peran **Admin**, **Instructor**, dan **Student**. |
| **Course** | Menyimpan informasi utama mengenai mata kuliah, seperti nama, deskripsi, harga, dan pengajar. |
| **CourseContent** | Menyimpan materi pembelajaran (lesson) yang terdapat pada setiap course. |
| **CourseMember** | Menyimpan data mahasiswa yang telah melakukan enrollment pada suatu course. |
| **CourseContentCompletion** | Menyimpan progress pembelajaran berdasarkan lesson yang telah diselesaikan oleh mahasiswa. |
| **Comment** | Menyimpan komentar yang diberikan mahasiswa pada materi pembelajaran. |


## Fitur Tambahan (Paket 6 - Async Processing & Notification)

| No | Fitur | Keterangan |
|----|--------|------------|
| 1 | **Email Notification (Async)** | Mengirim email atau mock email secara asynchronous menggunakan Celery. |
| 2 | **Generate Certificate (Async)** | Membuat sertifikat PDF sebagai background task menggunakan ReportLab. |
| 3 | **Export Report (Async)** | Mengekspor laporan dalam format CSV sebagai background task. |
| 4 | **Scheduled Task (Celery Beat)** | Menjalankan task pembaruan statistik course secara otomatis setiap satu jam. |
| 5 | **Task Status Endpoint** | Menyediakan endpoint `/api/tasks/{task_id}` untuk mengecek status task asynchronous. |
| 6 | **Flower Monitoring** | Monitoring worker Celery melalui Flower yang dapat diakses di `http://localhost:5555`. |


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



## Akun Demo

| Role           | Username  | Password       |
| -------------- | --------- | -------------- |
| **Admin**      | `admin`   | `admin123`     |
| **Instructor** | `dosen01` | `dosen123`     |
| **Student**    | `mhs001`  | `mahasiswa123` |




## Endpoint Utama

### Authentication

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| POST | `/api/auth/register` | Registrasi user baru |
| POST | `/api/auth/login` | Login dan mendapatkan JWT token |
| POST | `/api/auth/refresh` | Refresh JWT token |
| GET | `/api/auth/me` | Melihat profil user yang sedang login |

### Courses

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| GET | `/api/courses` | Menampilkan seluruh course |
| POST | `/api/courses` | Membuat course baru (Instructor/Admin) |
| GET | `/api/courses/{id}` | Detail course |
| PATCH | `/api/courses/{id}` | Memperbarui data course |
| DELETE | `/api/courses/{id}` | Menghapus course |
| GET | `/api/courses-cached` | Menampilkan daftar course menggunakan Redis Cache |
| GET | `/api/courses/{id}/contents` | Menampilkan seluruh materi pada course |

### Enrollments & Progress

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| POST | `/api/enrollments` | Enrollment ke course |
| GET | `/api/enrollments/my-courses` | Menampilkan course yang diikuti user |
| POST | `/api/enrollments/{id}/progress` | Memperbarui progress pembelajaran |

### Async Tasks (Celery)

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| POST | `/api/enrollments-async` | Enrollment secara asynchronous dan mengirim email |
| POST | `/api/courses/{id}/complete-async` | Menyelesaikan course dan membuat sertifikat PDF |
| POST | `/api/courses/{id}/export-async` | Mengekspor laporan CSV secara asynchronous |
| POST | `/api/admin/update-stats` | Menjalankan update statistik course |
| GET | `/api/tasks/{task_id}` | Melihat status background task |

### Analytics

| Method | Endpoint | Keterangan |
|--------|----------|------------|
| GET | `/api/analytics/popular-courses` | Menampilkan course paling populer |
| GET | `/api/analytics/my-activities` | Menampilkan aktivitas user |

### Monitoring

| Service | URL | Keterangan |
|---------|-----|------------|
| Flower | `http://localhost:5555` | Monitoring Celery Worker |
| RabbitMQ Management | `http://localhost:15672` | Monitoring RabbitMQ |



## Dokumentasi Lengkap 
dapat dilihat pada file [FINAL_PROJECT_REPORT.md](https://github.com/andikaa17/final-project-pss/blob/master/FINAL_PROJECT_REPORT.md)


