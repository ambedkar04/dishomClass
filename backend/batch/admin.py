from django.contrib import admin
from django.utils.html import format_html
from .models import CourseCategory, Subject, Batch, Chapter
from accounts.models import CustomUser
from unfold.admin import ModelAdmin


@admin.register(CourseCategory)
class CourseCategoryAdmin(ModelAdmin):
    """Admin configuration for CourseCategory."""
    list_display = ('name', 'code', 'batches_count', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'code', 'description')
    ordering = ('name',)
    readonly_fields = ('created_at', 'updated_at')

    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'code', 'description')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def batches_count(self, obj):
        """Display count of batches in this category."""
        return obj.batches.count()
    batches_count.short_description = 'Batches'


class ChapterInline(admin.TabularInline):
    model = Chapter
    fields = ('order', 'title')
    extra = 1
    ordering = ('order',)


@admin.register(Subject)
class SubjectAdmin(ModelAdmin):
    list_display = ('name', 'chapters_count', 'teachers_col', 'sme_col', 'updated_at')

    ordering = ('name',)
    inlines = (ChapterInline,)
    search_fields = ('name', 'teachers__full_name', 'sme__full_name')
    autocomplete_fields = ('sme', 'teachers')
    fieldsets = (
        ('General', {
            'fields': ('name', 'sme', 'teachers'),
        }),
    )

    def formfield_for_manytomany(self, db_field, request, **kwargs):
        formfield = super().formfield_for_manytomany(db_field, request, **kwargs)
        if db_field.name == 'teachers':
            for attr in ('can_add_related', 'can_change_related', 'can_view_related', 'can_delete_related'):
                if hasattr(formfield.widget, attr):
                    setattr(formfield.widget, attr, False)
        return formfield

    def chapters_count(self, obj):
        return obj.chapters.count()
    chapters_count.short_description = 'Chapters'

    def teachers_col(self, obj):
        teachers = list(obj.teachers.all())
        if not teachers:
            return '(No teachers)'
        shown = ", ".join(t.get_full_name() for t in teachers[:3])
        if len(teachers) > 3:
            shown += f" (+{len(teachers)-3} more)"
        full = ", ".join(t.get_full_name() for t in teachers)
        return format_html('<span title="{}">{}</span>', full, shown)
    teachers_col.short_description = 'Teacher'

    def sme_col(self, obj):
        return obj.sme.get_full_name() if obj.sme else '-'
    sme_col.short_description = 'SME'


@admin.register(Chapter)
class ChapterAdmin(ModelAdmin):
    list_display = ('title', 'subject', 'order', 'created_at', 'updated_at')
    list_filter = ('subject', 'created_at')
    search_fields = ('title', 'subject__name')
    ordering = ('subject', 'order') 
    # autocomplete_fields = ('subject',)

@admin.register(Batch)
class BatchAdmin(ModelAdmin):
    list_display = ('thumbnail_small', 'batch_name', 'course_display', 'teacher_list', 'price_display', 'discount_display', 'duration_display')

    readonly_fields = ('thumbnail_preview', 'created_at', 'updated_at', 'discount_percent')
    # Use autocomplete widgets for large user/subject sets. Related admins must set search_fields.
    autocomplete_fields = ('course_category', 'teachers', 'subjects')
    search_fields = ('name', 'course_category__name')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'course_category'),
            'description': 'Enter the basic batch information'
        }),
        ('Teachers & Subjects', {
            'fields': ('teachers', 'subjects'),
            'description': 'Select 1-10 teachers and 1-10 subjects for this batch'
        }),
        ('Thumbnail', {
            'fields': ('thumbnail', 'thumbnail_preview'),
            'classes': ('collapse',),
            'description': 'Upload a banner image (ideal size: 700x300 pixels)'
        }),
        ('Pricing', {
            'fields': ('price', 'offer_price', 'discount_percent')
        }),
        ('Duration', {
            'fields': ('start_date', 'end_date')
        }),
        ('Metadata', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',),
        })
    )

    def get_queryset(self, request):
        """Optimize queries by prefetching related fields."""
        return super().get_queryset(request).prefetch_related('teachers', 'subjects')
    def teacher_list(self, obj):
        """Display list of teachers with count."""
        teachers = list(obj.teachers.all())
        count = len(teachers)
        if count == 0:
            return '(No teachers)'

        shown = ", ".join(t.get_full_name() for t in teachers[:3])
        if count > 3:
            shown += f" (+{count-3} more)"
        return format_html('<span title="{}">{}</span>', 
                         ", ".join(t.get_full_name() for t in teachers),
                         shown)
    teacher_list.short_description = 'Teachers'

    # Removed subject_list from list_display per requirements

    def price_display(self, obj):
        """Format price with currency symbol."""
        return f'₹{obj.price}'
    price_display.admin_order_field = 'price'
    price_display.short_description = 'Price'

    def discount_percent(self, obj):
        """Return discount percent, or '0%' when no offer_price is set."""
        if not obj.offer_price:
            return '0%'
        try:
            discount = obj.get_discount_percentage()
        except Exception:
            return '-'
        return f"{discount}%"
    discount_percent.short_description = 'Discount %'

    def discount_display(self, obj):
        """Show discount percentage if offer price exists."""
        if obj.offer_price:
            discount = obj.get_discount_percentage()
            return format_html(
                '<span style="color: #28a745;">{}% off</span><br>'
                '<small style="color: #6c757d;">₹{}</small>',
                discount, obj.offer_price
            )
        return '-'
    discount_display.short_description = 'Discount'

    def duration_display(self, obj):
        """Format the batch duration."""
        return format_html(
            '{}<br><small style="color: #6c757d;">{}</small>',
            obj.start_date.strftime('%b %d, %Y'),
            obj.end_date.strftime('%b %d, %Y')
        )
    duration_display.short_description = 'Duration'

    def thumbnail_small(self, obj):
        """Small thumbnail preview for list view."""
        if obj.thumbnail:
            return format_html(
                '<img src="{}" style="max-width:100px;border:1px solid #ddd;padding:2px;border-radius:4px;"/>',
                obj.thumbnail.url
            )
        return "No thumbnail"
    thumbnail_small.short_description = 'Thumbnail'

    # Renamed headers/methods for required columns
    def batch_name(self, obj):
        return obj.name
    batch_name.admin_order_field = 'name'
    batch_name.short_description = 'Batch Name'

    def course_display(self, obj):
        return obj.course_category
    course_display.admin_order_field = 'course_category__name'
    course_display.short_description = 'Course'
