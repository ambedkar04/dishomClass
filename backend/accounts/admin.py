from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth import get_user_model
from django.utils.translation import gettext_lazy as _
from django.utils.safestring import mark_safe
from unfold.admin import ModelAdmin
from .models import CustomGroup

CustomUser = get_user_model()

@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin, ModelAdmin):
    list_display = (
        'profile_thumbnail',
        'mobile_number',
        'full_name',
        'email',
        'role',
        'batch_name',
        'get_address',
        'is_active',
        'joining_date',
    )
    list_filter = ('role', 'is_active', 'is_staff', 'state')
    ordering = ('mobile_number',)
    readonly_fields = ('profile_thumbnail',)
    search_fields = ('mobile_number', 'email', 'full_name', 'batch_name', 'district', 'state')
    
    list_per_page = 50
    actions = ('activate_selected', 'deactivate_selected')
    
    # Define the fieldsets for the add and change forms
    fieldsets = (
        (None, {'fields': ('mobile_number', 'password')}),
    (_('Personal info'), {'fields': ('full_name', 'email')}),
    (_('Profile'), {'fields': ('profile_thumbnail', 'profile_picture')}),
    (_('Role & Batch'), {'fields': ('role', 'batch_name', 'subjects')}),
        (_('Address'), {'fields': ('district', 'state', 'pincode')}),
        (_('Permissions'), {
            'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions'),
        }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),
    )
    
    # Fields for adding a new user
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('mobile_number', 'email', 'password1', 'password2', 'full_name',
                      'role', 'batch_name', 'subjects', 'profile_picture', 'district', 'state', 'pincode'),
        }),
    )

    def get_address(self, obj):
        parts = []
        if getattr(obj, 'district', None):
            parts.append(obj.district)
        if getattr(obj, 'state', None):
            parts.append(obj.state)
        if getattr(obj, 'pincode', None):
            parts.append(obj.pincode)
        return ', '.join(parts) if parts else ''
    get_address.short_description = 'Address'

    def profile_thumbnail(self, obj):
        if getattr(obj, 'profile_picture', None):
            # Add a subtle border so the thumbnail stands out in the admin
            return mark_safe(
                f"<img src='{obj.profile_picture.url}' width='30' height='30' "
                f"style='object-fit:cover;border-radius:50%;border:1px solid #ddd;padding:1px;' />"
            )
        return ''
    profile_thumbnail.short_description = 'Profile Pic'
    

    def full_name(self, obj):
        # Use model's get_full_name if available, fall back to first+last
        name = ''
        try:
            name = obj.get_full_name()
        except Exception:
            name = f"{obj.first_name or ''} {obj.last_name or ''}".strip()
        return name
    full_name.short_description = 'Full name'

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        return qs.prefetch_related('groups')

    def joining_date(self, obj):
        return obj.date_joined.strftime('%d/%m/%Y')
    joining_date.short_description = 'Joining Date'
    joining_date.admin_order_field = 'date_joined'

    def activate_selected(self, request, queryset):
        updated = queryset.update(is_active=True)
        self.message_user(request, _(f"Activated {updated} users."))
    activate_selected.short_description = _('Activate selected users')

    def deactivate_selected(self, request, queryset):
        updated = queryset.update(is_active=False)
        self.message_user(request, _(f"Deactivated {updated} users."))
    deactivate_selected.short_description = _('Deactivate selected users')

    class Media:
        css = {
            'all': ('accounts/css/accounts.css',)
        }
        js = ('accounts/js/accounts.js',)
   

@admin.register(CustomGroup)
class CustomGroupAdmin(ModelAdmin):
    list_display = ('name', 'description', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('name', 'description')
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        (None, {'fields': ('name', 'description')}),
        (_('Timestamps'), {'fields': ('created_at', 'updated_at')}),
    )
   
