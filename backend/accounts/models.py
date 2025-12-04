from django.contrib.auth.models import AbstractUser, BaseUserManager, Group as BaseGroup
from django.db import models
from django.core.validators import RegexValidator

class CustomUserManager(BaseUserManager):
    def create_user(self, mobile_number, password=None, **extra_fields):
        if not mobile_number:
            raise ValueError('Mobile number is required')
        if 'email' in extra_fields and extra_fields['email']:
            extra_fields['email'] = self.normalize_email(extra_fields['email'])
        user = self.model(mobile_number=mobile_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, mobile_number, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'Admin')
        return self.create_user(mobile_number, password, **extra_fields)

class CustomUser(AbstractUser):
    ROLE_CHOICES = [
        ('Admin', 'Admin'),
        ('Subadmin', 'Subadmin'),
        ('Teacher', 'Teacher'),
        ('SME', 'SME'),
        ('Student', 'Student'),
        ('Blogger', 'Blogger'),
    ]

    username = None  # Remove username field
    mobile_number = models.CharField(
        'Mobile Number',
        max_length=10,
        unique=True,
        validators=[
            RegexValidator(
                # Use [0-9] to restrict to ASCII digits only (\d also matches other Unicode digits)
                regex=r'^[0-9]{10}$',
                message='Mobile number must be 10 digits',
                code='invalid_mobile_number'
            )
        ]
    )

    # Optional fields set to nullable/blank to avoid migration issues on existing DB rows
    email = models.EmailField('Email Address', unique=True, null=True, blank=False)
    role = models.CharField('Role', max_length=20, choices=ROLE_CHOICES, default='Student')
    district = models.CharField('District', max_length=100, null=True, blank=True)
    state = models.CharField('State', max_length=100, null=True, blank=True)
    pincode = models.CharField(
        'PIN Code',
        max_length=6,
        null=True,
        blank=True,
        validators=[
            RegexValidator(
                # Enforce ASCII digits for PIN code as well
                regex=r'^[0-9]{6}$',
                message='PIN code must be 6 digits',
                code='invalid_pincode'
            )
        ]
    )
    batch_name = models.CharField('Batch Name', max_length=100, blank=True, null=True)
    subjects = models.ManyToManyField(
        'batch.Subject',
        blank=True,
        related_name='specialized_teachers',
        help_text='Select subjects (required for role=Teacher)'
    )
    profile_picture = models.ImageField('Profile Picture', upload_to='profile_pics/', null=True, blank=True)

    full_name = models.CharField('Full name', max_length=150, null=True, blank=False)

    USERNAME_FIELD = 'mobile_number'
    REQUIRED_FIELDS = []

    objects = CustomUserManager()

    def __str__(self):
        full = self.get_full_name()
        # For Teachers show only full name
        if self.role == 'Teacher':
            return full if full else self.mobile_number

        return f"{full} ({self.mobile_number})" if full else self.mobile_number

    def get_full_name(self):
        if getattr(self, 'full_name', None):
            return self.full_name.strip()
        return f"{self.first_name or ''} {self.last_name or ''}".strip()

    def clean(self):
        """Validate required fields: email, first_name, and address (district/state/pincode).

        Also require `subjects` when role is Teacher.
        We keep DB fields nullable to avoid migration pain, but enforce at app level here.
        """
        from django.core.exceptions import ValidationError

        errors = {}

        if self.email is not None and not str(self.email).strip():
            errors['email'] = 'Email is required.'

        # Require single Full name instead of separate first/last
        if not (self.get_full_name() and self.get_full_name().strip()):
            errors['full_name'] = 'Full name is required.'

        # Address: optional (district, state, pincode)

        if self.role == 'Teacher':
            # For M2M, we can't check self.subjects.exists() here because the instance might not be saved yet.
            # Validation for M2M usually happens in forms or serializers.
            pass

        if errors:
            raise ValidationError(errors)


class CustomGroup(BaseGroup):
    """Custom Group model extending Django's default Group"""
    description = models.TextField('Description', blank=True, null=True)
    created_at = models.DateTimeField('Created At', auto_now_add=True)
    updated_at = models.DateTimeField('Updated At', auto_now=True)
    
    class Meta:
        verbose_name = 'Group'
        verbose_name_plural = 'Groups'
        
    def __str__(self):
        return self.name
