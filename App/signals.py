from django.db.models.signals import post_save, pre_save
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
from .models import Report, Notification

@receiver(pre_save, sender=Report)
def track_report_status_change(sender, instance, **kwargs):
    """Track status changes to send notifications"""
    if instance.pk:  # Only for existing reports
        try:
            old_report = Report.objects.get(pk=instance.pk)
            instance._old_status = old_report.status
        except Report.DoesNotExist:
            instance._old_status = None
    else:
        instance._old_status = None

@receiver(post_save, sender=Report)
def send_report_notifications(sender, instance, created, **kwargs):
    """Send notifications when report status changes"""
    if created:
        # Welcome notification when report is submitted
        Notification.objects.create(
            user=instance.reporter,
            notification_type='general',
            title='Report Submitted Successfully',
            message=f'Thank you for reporting "{instance.title}". Our team will investigate and verify this environmental issue. You will be notified of any updates.',
            report=instance
        )
        # Send professional HTML email
        try:
            dashboard_url = 'http://127.0.0.1:8000/my-reports/'
            location = f"{instance.latitude}, {instance.longitude}" if instance.latitude and instance.longitude else instance.location_name
            
            html_message = f"""
            <!DOCTYPE html>
            <html>
            <head>
                <meta charset="utf-8">
                <style>
                    body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0fdf4; }}
                    .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                    .header {{ background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 30px; text-align: center; }}
                    .content {{ padding: 30px; }}
                    .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; color: #6b7280; font-size: 12px; }}
                    .btn {{ background-color: #22c55e; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 20px 0; }}
                    .details {{ background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #22c55e; }}
                </style>
            </head>
            <body>
                <div class="container">
                    <div class="header">
                        <h1>🌱 MsituGuard</h1>
                        <h2>Report Submitted Successfully</h2>
                        <p>Thank you for protecting our environment!</p>
                    </div>
                    <div class="content">
                        <h3>Hello {instance.reporter.first_name or instance.reporter.username},</h3>
                        <p>Thank you for submitting your environmental report <strong>"{instance.title}"</strong>.</p>
                        <p>Our team will investigate and verify this issue. You will receive email updates when the status changes.</p>
                        
                        <div class="details">
                            <h4>📄 Report Details:</h4>
                            <p><strong>Type:</strong> {instance.get_report_type_display()}</p>
                            <p><strong>Location:</strong> {location}</p>
                            <p><strong>Status:</strong> <span style="color: #f59e0b;">Under Review</span></p>
                        </div>
                        
                        <div style="text-align: center;">
                            <a href="{dashboard_url}" class="btn">Track Your Report Progress</a>
                        </div>
                        
                        <p style="margin-top: 30px;">Thank you for being an environmental guardian! 🌿</p>
                        
                        <p>Best regards,<br><strong>MsituGuard Team</strong></p>
                    </div>
                    <div class="footer">
                        <p>© 2024 MsituGuard - Environmental Protection Platform</p>
                    </div>
                </div>
            </body>
            </html>
            """
            
            from django.core.mail import EmailMultiAlternatives
            msg = EmailMultiAlternatives(
                subject='🌱 Report Submitted Successfully',
                body=f'Report submitted: {instance.title}. Track progress: {dashboard_url}',
                from_email=settings.DEFAULT_FROM_EMAIL,
                to=[instance.reporter.email]
            )
            msg.attach_alternative(html_message, "text/html")
            msg.send(fail_silently=True)
        except:
            pass
    else:
        # Check if status changed
        old_status = getattr(instance, '_old_status', None)
        if old_status and old_status != instance.status:
            if instance.status == 'verified':
                # The new reward-based email notification is handled in views.py
                # Only create the notification here
                Notification.objects.create(
                    user=instance.reporter,
                    notification_type='report_verified',
                    title='Report Verified ✅',
                    message=f'Great news! Your report "{instance.title}" has been verified by our team. We confirmed this environmental issue exists and are taking action to address it.',
                    report=instance
                )
                    
            elif instance.status == 'resolved':
                # Create notification
                Notification.objects.create(
                    user=instance.reporter,
                    notification_type='report_resolved',
                    title='Report Resolved 🎉',
                    message=f'Excellent! Your report "{instance.title}" has been successfully resolved. Thank you for helping protect our environment. Your contribution makes a difference!',
                    report=instance
                )
                # Send HTML email
                try:
                    dashboard_url = 'http://127.0.0.1:8000/my-reports/'
                    
                    html_message = f"""
                    <!DOCTYPE html>
                    <html>
                    <head>
                        <meta charset="utf-8">
                        <style>
                            body {{ font-family: Arial, sans-serif; margin: 0; padding: 0; background-color: #f0fdf4; }}
                            .container {{ max-width: 600px; margin: 0 auto; background-color: white; }}
                            .header {{ background: linear-gradient(135deg, #22c55e 0%, #16a34a 100%); color: white; padding: 30px; text-align: center; }}
                            .content {{ padding: 30px; }}
                            .footer {{ background-color: #f8fafc; padding: 20px; text-align: center; color: #6b7280; font-size: 12px; }}
                            .btn {{ background-color: #22c55e; color: white; padding: 12px 24px; text-decoration: none; border-radius: 6px; display: inline-block; margin: 20px 0; }}
                            .celebration {{ background-color: #f0fdf4; padding: 20px; border-radius: 8px; margin: 20px 0; border-left: 4px solid #22c55e; text-align: center; }}
                        </style>
                    </head>
                    <body>
                        <div class="container">
                            <div class="header">
                                <h1>🌱 MsituGuard</h1>
                                <h2>🎉 Report Resolved</h2>
                                <p>Environmental issue successfully addressed!</p>
                            </div>
                            <div class="content">
                                <h3>Hello {instance.reporter.first_name or instance.reporter.username},</h3>
                                <div class="celebration">
                                    <h3>🎉 Excellent!</h3>
                                    <p>Your report <strong>"{instance.title}"</strong> has been successfully resolved.</p>
                                    <p>Thank you for helping protect our environment. Your contribution makes a difference!</p>
                                </div>
                                
                                <div style="text-align: center;">
                                    <a href="{dashboard_url}" class="btn">View Your Report Status</a>
                                </div>
                                
                                <p style="margin-top: 30px;">Thank you for being an environmental guardian! 🌿</p>
                                
                                <p>Best regards,<br><strong>MsituGuard Team</strong></p>
                            </div>
                            <div class="footer">
                                <p>© 2024 MsituGuard - Environmental Protection Platform</p>
                            </div>
                        </div>
                    </body>
                    </html>
                    """
                    
                    from django.core.mail import EmailMultiAlternatives
                    msg = EmailMultiAlternatives(
                        subject='🎉 Report Resolved - MsituGuard',
                        body=f'Report resolved: {instance.title}. View status: {dashboard_url}',
                        from_email=settings.DEFAULT_FROM_EMAIL,
                        to=[instance.reporter.email]
                    )
                    msg.attach_alternative(html_message, "text/html")
                    msg.send(fail_silently=True)
                except:
                    pass