from django.db import models
from django.contrib.auth.models import User

# =========================
# MODEL COURSE
# =========================

class Course(models.Model):
    name = models.CharField("nama matkul", max_length=100)
    description = models.TextField("deskripsi", default='-')
    price = models.IntegerField("harga", default=10000)
    image = models.ImageField("gambar", null=True, blank=True)

    teacher = models.ForeignKey(
        User,
        verbose_name="pengajar",
        on_delete=models.RESTRICT
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = "Mata Kuliah"
        verbose_name_plural = "Mata Kuliah"
        indexes = [
            models.Index(fields=['price'], name='idx_course_price'),
            models.Index(fields=['teacher', 'price'], name='idx_course_teacher_price'),
        ]


ROLE_OPTIONS = [
    ('std', "Siswa"),
    ('ast', "Asisten"),
]


class CourseMember(models.Model):
    course_id = models.ForeignKey(
        Course,
        verbose_name="matkul",
        on_delete=models.RESTRICT
    )

    user_id = models.ForeignKey(
        User,
        verbose_name="siswa",
        on_delete=models.RESTRICT
    )

    roles = models.CharField(
        "peran",
        max_length=3,
        choices=ROLE_OPTIONS,
        default='std'
    )

    def __str__(self):
        return f"{self.user_id} - {self.course_id} ({self.roles})"


class CourseContent(models.Model):
    name = models.CharField("judul konten", max_length=200)
    description = models.TextField("deskripsi", default='-')

    video_url = models.CharField(
        'URL Video',
        max_length=200,
        null=True,
        blank=True
    )

    file_attachment = models.FileField(
        "File",
        null=True,
        blank=True
    )

    course_id = models.ForeignKey(
        Course,
        verbose_name="matkul",
        on_delete=models.RESTRICT
    )

    parent_id = models.ForeignKey(
        "self",
        verbose_name="induk",
        on_delete=models.RESTRICT,
        null=True,
        blank=True
    )

    def __str__(self):
        return self.name


class Comment(models.Model):
    content_id = models.ForeignKey(
        CourseContent,
        verbose_name="konten",
        on_delete=models.CASCADE
    )

    member_id = models.ForeignKey(
        CourseMember,
        verbose_name="pengguna",
        on_delete=models.CASCADE
    )

    comment = models.TextField('komentar')

    def __str__(self):
        return f"Komentar oleh {self.member_id} pada {self.content_id}"


class CourseContentCompletion(models.Model):
    member_id = models.ForeignKey(
        CourseMember,
        verbose_name="anggota kelas",
        on_delete=models.CASCADE
    )

    content_id = models.ForeignKey(
        CourseContent,
        verbose_name="konten",
        on_delete=models.CASCADE
    )

    completed = models.BooleanField(default=True)
    completed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.member_id} selesai {self.content_id}"

    class Meta:
        unique_together = ("member_id", "content_id")


# =========================
# TASK MAPPING
# =========================

class TaskMapping(models.Model):
    task_id = models.CharField(
        max_length=255,
        unique=True,
        db_index=True
    )

    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='tasks'
    )

    course = models.ForeignKey(
        Course,
        on_delete=models.CASCADE,
        null=True,
        blank=True
    )

    task_type = models.CharField(
        max_length=50
    )  

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    class Meta:
        db_table = 'task_mappings'
        indexes = [
            models.Index(fields=['task_id', 'user']),
        ]

    def __str__(self):
        return f"{self.task_type} - {self.task_id} - {self.user.username}"