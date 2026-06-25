from celery import shared_task
from django.core.mail import send_mail
from courses.permissions import get_role
from django.conf import settings
from django.utils import timezone
from io import StringIO
import csv
import os
import logging

logger = logging.getLogger(__name__)

@shared_task
def send_enrollment_email(user_id, course_id, user_email, user_name, course_name):
    """Task 1: Kirim email saat student enroll"""
    try:
        subject = f"Selamat! Anda telah terdaftar di {course_name}"
        message = f"""
        Halo {user_name},
        
        Selamat! Anda berhasil terdaftar di course "{course_name}".
        
        Silakan mulai belajar di dashboard Anda.
        
        Terima kasih telah bergabung!
        """
        
        send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user_email])
        logger.info(f"Email sent to {user_email} for course {course_name}")
        return f"Email sent to {user_email}"
    except Exception as e:
        logger.error(f"Email failed: {e}")
        return None

@shared_task
def generate_certificate(user_id, course_id, user_name, course_name):
    """Task 2: Generate sertifikat PDF - PASTI JALAN"""
    try:
        from reportlab.lib.pagesizes import letter
        from reportlab.pdfgen import canvas

        cert_dir = os.path.join(settings.MEDIA_ROOT, 'certificates')
        os.makedirs(cert_dir, exist_ok=True)

        filename = f"certificate_{user_id}_{course_id}_{int(timezone.now().timestamp())}.pdf"
        filepath = os.path.join(cert_dir, filename)

        c = canvas.Canvas(filepath, pagesize=letter)
        width, height = letter

        c.setStrokeColorRGB(0.8, 0.6, 0.2)
        c.setLineWidth(5)
        c.rect(50, 50, width-100, height-100)

        c.setFont("Helvetica-Bold", 28)
        c.setFillColorRGB(0.5, 0.3, 0.1)
        c.drawCentredString(width/2, height-100, "CERTIFICATE OF COMPLETION")

        c.setFont("Helvetica", 14)
        c.setFillColorRGB(0, 0, 0)
        c.drawCentredString(width/2, height-150, "This certificate is proudly presented to")

        c.setFont("Helvetica-Bold", 24)
        c.setFillColorRGB(0.2, 0.4, 0.6)
        c.drawCentredString(width/2, height-220, user_name)

        c.setFont("Helvetica", 14)
        c.drawCentredString(width/2, height-280, f"for successfully completing the course")

        c.setFont("Helvetica-Bold", 20)
        c.setFillColorRGB(0.5, 0.3, 0.1)
        c.drawCentredString(width/2, height-340, course_name)

        c.setFont("Helvetica", 11)
        c.setFillColorRGB(0.3, 0.3, 0.3)
        c.drawCentredString(width/2, height-430, f"Date: {timezone.now().strftime('%B %d, %Y')}")

        c.save()

        if os.path.exists(filepath):
            logger.info(f" SUCCESS! File: {filepath}")
            return filepath
        else:
            logger.error(f" File NOT FOUND: {filepath}")
            return None

    except Exception as e:
        logger.error(f" FAILED: {str(e)}")
        import traceback
        logger.error(traceback.format_exc())
        return None

@shared_task
def update_course_statistics():
    """Task 3: Update enrollment count (scheduled task - setiap jam)"""
    from courses.models import Course, CourseMember

    results = []
    for course in Course.objects.all():
        count = CourseMember.objects.filter(course_id=course).count()
        results.append(f"Course {course.id} ({course.name}): {count} members")
        logger.info(f"Updated stat: {course.name} -> {count} members")

    return f"Updated {len(results)} courses: {', '.join(results[:5])}..."

@shared_task
def export_course_report(course_id, requester_email, course_name):
    """Task 4: Generate CSV report (async)"""
    from courses.models import CourseMember

    logger.info(f"Starting report export for course: {course_name}")

    
    report_dir = os.path.join(settings.MEDIA_ROOT, 'reports')
    os.makedirs(report_dir, exist_ok=True)
    logger.info(f"Report directory: {report_dir}")

    output = StringIO()
    writer = csv.writer(output)
    writer.writerow(['No', 'Username', 'Email', 'Role', 'Date Joined'])

    members = CourseMember.objects.filter(course_id=course_id).select_related('user_id')
    for idx, member in enumerate(members, 1):
        user = member.user_id
        writer.writerow([
            idx,
            user.username,
            user.email,
            get_role(user),
            user.date_joined.strftime('%Y-%m-%d %H:%M:%S') if user.date_joined else ''
        ])

    filename = f"report_course_{course_id}_{int(timezone.now().timestamp())}.csv"
    filepath = os.path.join(report_dir, filename)

    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(output.getvalue())

    if os.path.exists(filepath):
        file_size = os.path.getsize(filepath)
        logger.info(f" Report exported successfully! Size: {file_size} bytes")
    else:
        logger.error(f" Report file NOT FOUND after save: {filepath}")

    send_mail(
        f"Report for {course_name} is Ready",
        f"Report untuk course '{course_name}' telah siap. Download di: {settings.BASE_URL}/media/reports/{filename}",
        settings.DEFAULT_FROM_EMAIL,
        [requester_email]
    )

    logger.info(f"Report exported: {filepath}")
    return filename