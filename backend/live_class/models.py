from django.db import models
from django.utils.html import mark_safe
from batch.models import Batch, CourseCategory, Subject, Chapter

class YTClass(models.Model):
    """
    Model for YouTube Live Classes.
    Stores the YouTube video URL/ID and provides an iframe for embedding.
    """
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='yt_classes')
    course_category = models.ForeignKey(
        CourseCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Course'
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Subject'
    )
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Chapter'
    )
    teacher = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Teacher'},
        verbose_name='Teacher'
    )
    
    title = models.CharField(max_length=255)
    youtube_url = models.URLField(help_text="Enter the full YouTube Live Class URL")
    lecture_video = models.FileField(
        'Lecture Video', upload_to='live_classes/yt/videos/', null=True, blank=True,
        help_text='Optional: Upload recorded lecture/video file'
    )
    class_note = models.FileField(
        'Class Note', upload_to='live_classes/yt/notes/', null=True, blank=True,
        help_text='Optional: Upload class notes (PDF or other)'
    )
    dpp_pdf = models.FileField(
        'DPP PDF', upload_to='live_classes/yt/dpp/', null=True, blank=True,
        help_text='Optional: Upload DPP as PDF'
    )

    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
        
    class Meta:
        verbose_name = "YT Class"
        verbose_name_plural = "YT Classes"
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.title} ({self.batch.name})"

    def get_video_id(self):
        """Extracts video ID from YouTube URL."""
        if "v=" in self.youtube_url:
            return self.youtube_url.split("v=")[1].split("&")[0]
        elif "youtu.be/" in self.youtube_url:
            return self.youtube_url.split("youtu.be/")[1].split("?")[0]
        return None

    def get_iframe(self):
        """Returns the HTML iframe for the YouTube video."""
        video_id = self.get_video_id()
        if video_id:
            # Add proper parameters to fix YouTube error 153
            # Use enablejsapi=1 and origin parameter to fix player configuration error
            iframe_url = f"https://www.youtube.com/embed/{video_id}?enablejsapi=1&origin=http://localhost:8000&widget_referrer=http://localhost:8000"
            return mark_safe(
                f'<iframe width="560" height="315" '
                f'src="{iframe_url}" '
                f'frameborder="0" '
                f'allow="accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture; web-share" '
                f'allowfullscreen '
                f'referrerpolicy="strict-origin-when-cross-origin">'
                f'</iframe>'
            )
        return "Invalid YouTube URL"


class LiveClass(models.Model):
    """
    Model for VideoSDK Live Classes.
    Stores configuration for VideoSDK meetings.
    """
    batch = models.ForeignKey(Batch, on_delete=models.CASCADE, related_name='live_classes')
    course_category = models.ForeignKey(
        CourseCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Course'
    )
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Subject'
    )
    chapter = models.ForeignKey(
        Chapter, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        verbose_name='Chapter'
    )
    teacher = models.ForeignKey(
        'accounts.CustomUser',
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        limit_choices_to={'role': 'Teacher'},
        verbose_name='Teacher'
    )
    
    title = models.CharField(max_length=255)
    meeting_id = models.CharField(max_length=100, help_text="VideoSDK Meeting ID")
    lecture_video = models.FileField(
        'Lecture Video', upload_to='live_classes/live/videos/', null=True, blank=True,
        help_text='Optional: Upload recorded lecture/video file'
    )
    class_note = models.FileField(
        'Class Note', upload_to='live_classes/live/notes/', null=True, blank=True,
        help_text='Optional: Upload class notes (PDF or other)'
    )
    dpp_pdf = models.FileField(
        'DPP PDF', upload_to='live_classes/live/dpp/', null=True, blank=True,
        help_text='Optional: Upload DPP as PDF'
    )

    started_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    class Meta:
        verbose_name = "Live Class"
        verbose_name_plural = "Live Classes"
        ordering = ['-started_at']

    def __str__(self):
        return f"{self.title} ({self.batch.name})"
