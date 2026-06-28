# Final Project Learning Management System (LMS)

Simple LMS adalah sistem manajemen pembelajaran (Learning Management System) berbasis web yang dikembangkan menggunakan Django Rest Framework dan diintegrasikan dengan berbagai teknologi modern untuk mendukung pemrosesan asynchronous, caching, dan analitik. Proyek ini merupakan pengembangan dari sistem LMS dasar yang ditingkatkan dengan fitur-fitur advanced seperti Celery untuk background task, Redis untuk caching, MongoDB untuk penyimpanan log aktivitas, dan RabbitMQ sebagai message broker. Sistem ini memungkinkan pengguna dengan peran yang berbeda (Admin, Instructor, Student) untuk mengelola course, melakukan enrollment, melacak progress belajar, dan menghasilkan sertifikat serta laporan secara otomatis. Fitur-fitur tersebut diproses secara asynchronous menggunakan Celery agar pengguna tidak perlu menunggu lama.

---

## Item Utama :


| Item | Keterangan |
|-------|------------|
| **User** | Menyimpan data pengguna dengan peran **Admin**, **Instructor**, dan **Student**. |
| **Course** | Menyimpan informasi utama mengenai mata kuliah, seperti nama, deskripsi, harga, dan pengajar. |
| **CourseContent** | Menyimpan materi pembelajaran (lesson) yang terdapat pada setiap course. |
| **CourseMember** | Menyimpan data mahasiswa yang telah melakukan enrollment pada suatu course. |
| **CourseContentCompletion** | Menyimpan progress pembelajaran berdasarkan lesson yang telah diselesaikan oleh mahasiswa. |
| **Comment** | Menyimpan komentar yang diberikan mahasiswa pada materi pembelajaran. |


---

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
![rabbitmq](/docs/image-10.png)

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
