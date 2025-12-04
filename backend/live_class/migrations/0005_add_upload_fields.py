from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('live_class', '0004_liveclass_chapter_liveclass_course_category_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='ytclass',
            name='lecture_video',
            field=models.FileField(blank=True, help_text='Optional: Upload recorded lecture/video file', null=True, upload_to='live_classes/yt/videos/', verbose_name='Lecture Video'),
        ),
        migrations.AddField(
            model_name='ytclass',
            name='class_note',
            field=models.FileField(blank=True, help_text='Optional: Upload class notes (PDF or other)', null=True, upload_to='live_classes/yt/notes/', verbose_name='Class Note'),
        ),
        migrations.AddField(
            model_name='ytclass',
            name='dpp_pdf',
            field=models.FileField(blank=True, help_text='Optional: Upload DPP as PDF', null=True, upload_to='live_classes/yt/dpp/', verbose_name='DPP PDF'),
        ),
        migrations.AddField(
            model_name='liveclass',
            name='lecture_video',
            field=models.FileField(blank=True, help_text='Optional: Upload recorded lecture/video file', null=True, upload_to='live_classes/live/videos/', verbose_name='Lecture Video'),
        ),
        migrations.AddField(
            model_name='liveclass',
            name='class_note',
            field=models.FileField(blank=True, help_text='Optional: Upload class notes (PDF or other)', null=True, upload_to='live_classes/live/notes/', verbose_name='Class Note'),
        ),
        migrations.AddField(
            model_name='liveclass',
            name='dpp_pdf',
            field=models.FileField(blank=True, help_text='Optional: Upload DPP as PDF', null=True, upload_to='live_classes/live/dpp/', verbose_name='DPP PDF'),
        ),
    ]

