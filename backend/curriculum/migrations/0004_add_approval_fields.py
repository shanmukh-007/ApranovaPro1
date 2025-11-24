# Generated migration for approval fields

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('curriculum', '0003_submission_auto_created_submission_github_pr_number'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprogress',
            name='is_approved',
            field=models.BooleanField(default=False, help_text='Trainer has approved this project'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='approved_at',
            field=models.DateTimeField(blank=True, null=True, help_text='When the project was approved'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='approved_by',
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.SET_NULL,
                related_name='approved_student_projects',
                to=settings.AUTH_USER_MODEL,
                help_text='Trainer who approved this project'
            ),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='needs_revision',
            field=models.BooleanField(default=False, help_text='Project needs revision before approval'),
        ),
        migrations.AddField(
            model_name='studentprogress',
            name='trainer_feedback',
            field=models.TextField(blank=True, help_text='Feedback from trainer'),
        ),
    ]
