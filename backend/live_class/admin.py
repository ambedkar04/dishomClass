import importlib
admin = importlib.import_module('django.contrib.admin')
format_html = importlib.import_module('django.utils.html').format_html
from typing import Any
from typing import TYPE_CHECKING, Any, Optional, cast
from .models import YTClass, LiveClass

if TYPE_CHECKING:
    BaseModelAdmin = Any
    from accounts.models import CustomUser
else:
    from unfold.admin import ModelAdmin as BaseModelAdmin

@admin.register(YTClass)
class YTClassAdmin(BaseModelAdmin):
    list_display = ('title', 'course_display', 'batch', 'subject_display', 'chapter_display', 'teacher_display', 'video_col', 'notes_col', 'dpp_col')
    list_filter = ('batch', 'course_category', 'subject', 'teacher')

    readonly_fields = ('iframe_preview',)
    
    # Horizontal tabs: Batch Info then Class Info
    fieldsets = (
        ('Batch Info', {
            'fields': ('title', 'course_category', 'batch', 'subject', 'chapter', 'teacher'),
            'classes': ('tab',),
        }),
        ('Class Info', {
            'fields': ('youtube_url', 'lecture_video', 'class_note', 'dpp_pdf', 'is_active', 'iframe_preview'),
            'classes': ('tab',),
        }),
    )

    @admin.display(description="Course")
    def course_display(self, obj: YTClass) -> str:
        return obj.course_category.name if obj.course_category else "-"

    @admin.display(description="Subject")
    def subject_display(self, obj: YTClass) -> str:
        return obj.subject.name if obj.subject else "-"

    @admin.display(description="Chapter")
    def chapter_display(self, obj: YTClass) -> str:
        return str(obj.chapter) if obj.chapter else "-"

    @admin.display(description="Teacher")
    def teacher_display(self, obj: YTClass) -> str:
        teacher: Optional['CustomUser'] = cast(Optional['CustomUser'], obj.teacher)
        if teacher:
            return teacher.get_full_name() or getattr(teacher, 'username', None) or "-"
        return "-"

    @admin.display(description="Video Preview")
    def iframe_preview(self, obj: YTClass) -> str:
        return cast(str, obj.get_iframe())

    @admin.display(description="Video")
    def video_col(self, obj: YTClass) -> str:
        has = bool(obj.lecture_video)
        color = '#16a34a' if has else '#dc2626'
        symbol = '✓' if has else '✗'
        return format_html("<span style='color:{};font-weight:bold;'>{}</span>", color, symbol)

    @admin.display(description="Notes")
    def notes_col(self, obj: YTClass) -> str:
        has = bool(obj.class_note)
        color = '#16a34a' if has else '#dc2626'
        symbol = '✓' if has else '✗'
        return format_html("<span style='color:{};font-weight:bold;'>{}</span>", color, symbol)

    @admin.display(description="DPP")
    def dpp_col(self, obj: YTClass) -> str:
        has = bool(obj.dpp_pdf)
        color = '#16a34a' if has else '#dc2626'
        symbol = '✓' if has else '✗'
        return format_html("<span style='color:{};font-weight:bold;'>{}</span>", color, symbol)

    def get_form(self, request: Any, obj: Optional[YTClass] = None, change: bool = False, **kwargs: Any):
        form = super().get_form(request, obj, change, **kwargs)
        f = cast(Any, form)
        base_fields = getattr(f, 'base_fields', {})
        for name in ('title', 'youtube_url'):
            field = base_fields.get(name)
            if field is not None:
                field.required = True
                field.label = f"{field.label} *"
        return form

@admin.register(LiveClass)
class LiveClassAdmin(BaseModelAdmin):
    list_display = ('title', 'course_display', 'batch', 'subject_display', 'chapter_display', 'teacher_display', 'video_col', 'notes_col', 'dpp_col')
    list_filter = ('batch', 'course_category', 'subject', 'teacher')
    
    # Horizontal tabs: Batch Info then Class Info
    fieldsets = (
        ('Batch Info', {
            'fields': ('title', 'course_category', 'batch', 'subject', 'chapter', 'teacher'),
            'classes': ('tab',),
        }),
        ('Class Info', {
            'fields': ('meeting_id', 'lecture_video', 'class_note', 'dpp_pdf', 'is_active'),
            'classes': ('tab',),
        }),
    )

    @admin.display(description="Course")
    def course_display(self, obj: LiveClass) -> str:
        return obj.course_category.name if obj.course_category else "-"

    @admin.display(description="Subject")
    def subject_display(self, obj: LiveClass) -> str:
        return obj.subject.name if obj.subject else "-"

    @admin.display(description="Chapter")
    def chapter_display(self, obj: LiveClass) -> str:
        return str(obj.chapter) if obj.chapter else "-"

    @admin.display(description="Teacher")
    def teacher_display(self, obj: LiveClass) -> str:
        teacher: Optional['CustomUser'] = cast(Optional['CustomUser'], obj.teacher)
        if teacher:
            return teacher.get_full_name() or getattr(teacher, 'username', None) or "-"
        return "-"

    @admin.display(description="Video")
    def video_col(self, obj: LiveClass) -> str:
        has = bool(obj.lecture_video)
        color = '#16a34a' if has else '#dc2626'
        symbol = '✓' if has else '✗'
        return format_html("<span style='color:{};font-weight:bold;'>{}</span>", color, symbol)

    @admin.display(description="Notes")
    def notes_col(self, obj: LiveClass) -> str:
        has = bool(obj.class_note)
        color = '#16a34a' if has else '#dc2626'
        symbol = '✓' if has else '✗'
        return format_html("<span style='color:{};font-weight:bold;'>{}</span>", color, symbol)

    @admin.display(description="DPP")
    def dpp_col(self, obj: LiveClass) -> str:
        has = bool(obj.dpp_pdf)
        color = '#16a34a' if has else '#dc2626'
        symbol = '✓' if has else '✗'
        return format_html("<span style='color:{};font-weight:bold;'>{}</span>", color, symbol)

    def get_form(self, request: Any, obj: Optional[LiveClass] = None, change: bool = False, **kwargs: Any):
        form = super().get_form(request, obj, change, **kwargs)
        f = cast(Any, form)
        base_fields = getattr(f, 'base_fields', {})
        for name in ('title', 'meeting_id'):
            field = base_fields.get(name)
            if field is not None:
                field.required = True
                field.label = f"{field.label} *"
        return form
