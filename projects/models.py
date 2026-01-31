from django.db import models
from django.utils.text import slugify
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from portfolio.models import Portfolio
from skills.models import Skill

class ProjectCategory(models.Model):
    """
    Category for organizing projects (e.g., Web Development, Mobile Apps, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Brief description of the category")
    icon_class = models.CharField(
        max_length=100, 
        blank=True, 
        help_text="CSS class for icon (e.g., 'fas fa-globe', 'fas fa-mobile-alt')"
    )
    color = models.CharField(
        max_length=20, 
        blank=True, 
        default='#4a6fa5',
        help_text="Hex color code for category badge"
    )
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True)
    show_in_nav = models.BooleanField(default=True, help_text="Show this category in navigation")
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Project Category'
        verbose_name_plural = 'Project Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('projects:category', kwargs={'category_slug': self.slug})
    
    def project_count(self):
        return self.projects.filter(is_published=True).count()


class Technology(models.Model):
    """
    Technology used in projects (e.g., Django, React, Docker, etc.)
    """
    TECH_TYPES = [
        ('framework', 'Framework/Library'),
        ('language', 'Programming Language'),
        ('database', 'Database'),
        ('tool', 'Tool/Software'),
        ('service', 'Cloud Service'),
        ('other', 'Other'),
    ]
    
    name = models.CharField(max_length=100, unique=True)
    tech_type = models.CharField(max_length=20, choices=TECH_TYPES, default='framework')
    version = models.CharField(max_length=50, blank=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Icon class (e.g., 'fab fa-python', 'fab fa-js-square')"
    )
    logo = models.ImageField(upload_to='technologies/logos/', blank=True, null=True)
    color = models.CharField(max_length=20, blank=True, help_text="Primary brand color in hex")
    website = models.URLField(blank=True)
    documentation_url = models.URLField(blank=True)
    is_popular = models.BooleanField(default=False)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name_plural = 'Technologies'
    
    def __str__(self):
        if self.version:
            return f"{self.name} {self.version}"
        return self.name


class Project(models.Model):
    """
    Main project model for portfolio projects
    """
    # Project Status Choices
    STATUS_CHOICES = [
        ('concept', 'Concept/Idea'),
        ('planning', 'Planning'),
        ('development', 'In Development'),
        ('testing', 'Testing'),
        ('completed', 'Completed'),
        ('live', 'Live & Maintained'),
        ('archived', 'Archived'),
        ('on_hold', 'On Hold'),
    ]
    
    # Project Type Choices
    PROJECT_TYPES = [
        ('web', 'Web Application'),
        ('mobile', 'Mobile Application'),
        ('desktop', 'Desktop Software'),
        ('api', 'API/Backend Service'),
        ('library', 'Library/Package'),
        ('plugin', 'Plugin/Extension'),
        ('game', 'Game Development'),
        ('data', 'Data Science/AI/ML'),
        ('iot', 'IoT/Embedded'),
        ('design', 'UI/UX Design'),
        ('other', 'Other'),
    ]
    
    # Difficulty Level
    DIFFICULTY_LEVELS = [
        ('beginner', 'Beginner'),
        ('intermediate', 'Intermediate'),
        ('advanced', 'Advanced'),
        ('expert', 'Expert'),
    ]
    
    # ========== BASIC INFORMATION ==========
    title = models.CharField(max_length=200, help_text="Project title")
    slug = models.SlugField(max_length=200, unique=True, help_text="URL-friendly version of title")
    
    # Descriptions
    tagline = models.CharField(
        max_length=300, 
        help_text="Brief one-line description (appears in listings)"
    )
    summary = models.TextField(
        help_text="Short summary (2-3 paragraphs, appears on listing cards)"
    )
    full_description = models.TextField(
        help_text="Complete project description with details, challenges, solutions"
    )
    
    # ========== CATEGORIZATION ==========
    category = models.ForeignKey(
        ProjectCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='projects',
        help_text="Primary project category"
    )
    secondary_categories = models.ManyToManyField(
        ProjectCategory, 
        blank=True, 
        related_name='secondary_projects',
        help_text="Additional categories"
    )
    project_type = models.CharField(max_length=20, choices=PROJECT_TYPES, default='web')
    difficulty = models.CharField(max_length=20, choices=DIFFICULTY_LEVELS, default='intermediate')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='completed')
    
    # ========== VISIBILITY & FEATURING ==========
    is_featured = models.BooleanField(
        default=False, 
        help_text="Featured projects appear on homepage"
    )
    is_published = models.BooleanField(
        default=True, 
        help_text="Unpublished projects are not visible to public"
    )
    featured_order = models.IntegerField(
        default=0, 
        help_text="Order in featured listings (lower = first)"
    )
    
    # ========== DATES & TIMELINE ==========
    concept_date = models.DateField(null=True, blank=True, help_text="When the project was conceived")
    start_date = models.DateField(null=True, blank=True, help_text="Development start date")
    completed_date = models.DateField(null=True, blank=True, help_text="When project was completed")
    launch_date = models.DateField(null=True, blank=True, help_text="Public launch date")
    last_updated = models.DateField(null=True, blank=True, help_text="Last significant update")
    
    # ========== MEDIA & VISUALS ==========
    featured_image = models.ImageField(
        upload_to='projects/featured/', 
        null=True, 
        blank=True,
        help_text="Main project image (1200x630px recommended)"
    )
    thumbnail = models.ImageField(
        upload_to='projects/thumbnails/', 
        null=True, 
        blank=True,
        help_text="Small thumbnail (400x300px recommended)"
    )
    logo = models.ImageField(
        upload_to='projects/logos/', 
        null=True, 
        blank=True,
        help_text="Project logo/icon"
    )
    video_url = models.URLField(
        blank=True, 
        help_text="Link to demo video (YouTube/Vimeo)"
    )
    
    # ========== LINKS & REFERENCES ==========
    github_url = models.URLField(blank=True, help_text="GitHub repository URL")
    gitlab_url = models.URLField(blank=True, help_text="GitLab repository URL")
    live_url = models.URLField(blank=True, help_text="Live project URL")
    demo_url = models.URLField(blank=True, help_text="Demo/Preview URL")
    documentation_url = models.URLField(blank=True, help_text="Documentation URL")
    figma_url = models.URLField(blank=True, help_text="Figma design file URL")
    behance_url = models.URLField(blank=True, help_text="Behance project URL")
    download_url = models.URLField(blank=True, help_text="Download link")
    
    # ========== TECHNICAL DETAILS ==========
    technologies = models.ManyToManyField(
        Technology, 
        blank=True, 
        related_name='projects',
        help_text="Technologies used in this project"
    )
    skills_used = models.ManyToManyField(
        Skill, 
        blank=True, 
        related_name='projects',
        help_text="Skills demonstrated in this project"
    )
    
    # ========== TEAM & COLLABORATION ==========
    portfolio = models.ForeignKey(
        Portfolio, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='portfolio_projects'
    )
    is_solo_project = models.BooleanField(default=True)
    team_members = models.TextField(
        blank=True, 
        help_text="Names of team members (one per line)"
    )
    client = models.CharField(max_length=200, blank=True, help_text="Client name (if applicable)")
    collaboration_notes = models.TextField(blank=True, help_text="Notes about team collaboration")
    
    # ========== STATISTICS & METRICS ==========
    lines_of_code = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Approximate lines of code"
    )
    development_hours = models.IntegerField(
        null=True, 
        blank=True, 
        help_text="Estimated development hours"
    )
    views = models.PositiveIntegerField(default=0, help_text="Number of views")
    likes = models.PositiveIntegerField(default=0, help_text="Number of likes")
    shares = models.PositiveIntegerField(default=0, help_text="Number of shares")
    
    # ========== CHALLENGES & ACHIEVEMENTS ==========
    challenges = models.TextField(
        blank=True, 
        help_text="Technical challenges faced and how they were overcome"
    )
    lessons_learned = models.TextField(
        blank=True, 
        help_text="Key lessons learned from this project"
    )
    key_features = models.TextField(
        blank=True, 
        help_text="List of key features (one per line)"
    )
    future_improvements = models.TextField(
        blank=True, 
        help_text="Planned future improvements or features"
    )
    
    # ========== SEO & METADATA ==========
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    canonical_url = models.URLField(blank=True)
    
    # ========== ADMIN & SYSTEM ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    published_at = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        ordering = ['-is_featured', 'featured_order', '-published_at', '-created_at']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['status', 'is_published']),
            models.Index(fields=['is_featured', 'is_published']),
        ]
    
    def __str__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.title)
        
        # Set published_at date when publishing
        if self.is_published and not self.published_at:
            from django.utils import timezone
            self.published_at = timezone.now()
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('projects:detail', kwargs={'slug': self.slug})
    
    def duration(self):
        """Calculate project duration in human-readable format"""
        if self.start_date and self.completed_date:
            delta = self.completed_date - self.start_date
            months = delta.days // 30
            if months > 0:
                return f"{months} month{'s' if months > 1 else ''}"
            return f"{delta.days} day{'s' if delta.days > 1 else ''}"
        elif self.start_date:
            return "Ongoing"
        return "Not specified"
    
    def is_active(self):
        """Check if project is currently active"""
        return self.status in ['development', 'testing', 'live']
    
    def tech_stack(self):
        """Get technologies grouped by type"""
        return self.technologies.all().order_by('tech_type', 'order')
    
    def featured_images(self):
        """Get featured project images"""
        return self.images.filter(is_featured=True).order_by('order')
    
    def all_images(self):
        """Get all project images"""
        return self.images.all().order_by('order')
    
    def documentation_files(self):
        """Get all documentation files"""
        return self.documents.filter(file_type='documentation').order_by('order')
    
    def source_files(self):
        """Get all source code files"""
        return self.documents.filter(file_type='source').order_by('order')
    
    def related_projects(self):
        """Get related projects (same category or technologies)"""
        from django.db.models import Q
        related = Project.objects.filter(
            Q(category=self.category) | 
            Q(technologies__in=self.technologies.all()) |
            Q(skills_used__in=self.skills_used.all())
        ).exclude(id=self.id).distinct()[:4]
        return related
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def increment_likes(self):
        """Increment like count"""
        self.likes += 1
        self.save(update_fields=['likes'])
    
    def progress_percentage(self):
        """Calculate project progress based on status"""
        progress_map = {
            'concept': 10,
            'planning': 25,
            'development': 50,
            'testing': 75,
            'completed': 100,
            'live': 100,
            'archived': 100,
            'on_hold': 30,
        }
        return progress_map.get(self.status, 0)


class ProjectImage(models.Model):
    """
    Images for project gallery
    """
    IMAGE_TYPES = [
        ('screenshot', 'Screenshot'),
        ('design', 'Design Mockup'),
        ('diagram', 'Diagram/Architecture'),
        ('wireframe', 'Wireframe'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='images')
    image = models.ImageField(upload_to='projects/gallery/%Y/%m/')
    caption = models.CharField(max_length=200, blank=True)
    image_type = models.CharField(max_length=20, choices=IMAGE_TYPES, default='screenshot')
    order = models.IntegerField(default=0, help_text="Display order")
    is_featured = models.BooleanField(default=False, help_text="Show as featured image")
    alt_text = models.CharField(max_length=200, blank=True, help_text="Alt text for accessibility")
    
    class Meta:
        ordering = ['order', '-is_featured']
    
    def __str__(self):
        return f"{self.project.title} - {self.caption or 'Image'}"


class ProjectDocument(models.Model):
    """
    Documents related to projects (PDFs, source files, etc.)
    """
    DOCUMENT_TYPES = [
        ('documentation', 'Documentation'),
        ('source', 'Source Code'),
        ('design', 'Design Files'),
        ('report', 'Project Report'),
        ('presentation', 'Presentation'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='documents')
    title = models.CharField(max_length=200)
    file = models.FileField(upload_to='projects/documents/%Y/%m/')
    file_type = models.CharField(max_length=20, choices=DOCUMENT_TYPES, default='documentation')
    description = models.TextField(blank=True)
    file_size = models.CharField(max_length=50, blank=True, editable=False)
    order = models.IntegerField(default=0)
    is_public = models.BooleanField(default=True, help_text="Publicly downloadable")
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"
    
    def save(self, *args, **kwargs):
        # Calculate file size
        if self.file:
            size = self.file.size
            if size < 1024:
                self.file_size = f"{size} B"
            elif size < 1024 * 1024:
                self.file_size = f"{size / 1024:.1f} KB"
            else:
                self.file_size = f"{size / (1024 * 1024):.1f} MB"
        super().save(*args, **kwargs)


class ProjectLink(models.Model):
    """
    External links related to the project
    """
    LINK_TYPES = [
        ('article', 'Article/Blog Post'),
        ('tutorial', 'Tutorial'),
        ('review', 'Review'),
        ('news', 'News Coverage'),
        ('award', 'Award'),
        ('reference', 'Reference'),
        ('other', 'Other'),
    ]
    
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='links')
    title = models.CharField(max_length=200)
    url = models.URLField()
    link_type = models.CharField(max_length=20, choices=LINK_TYPES, default='reference')
    description = models.TextField(blank=True)
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['order', 'title']
    
    def __str__(self):
        return f"{self.project.title} - {self.title}"


class ProjectMilestone(models.Model):
    """
    Important milestones in project development
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='milestones')
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True)
    milestone_date = models.DateField()
    is_major = models.BooleanField(default=False, help_text="Major milestone")
    order = models.IntegerField(default=0)
    
    class Meta:
        ordering = ['milestone_date', 'order']
    
    def __str__(self):
        return f"{self.project.title}: {self.title} ({self.milestone_date})"


class ProjectTestimonial(models.Model):
    """
    Testimonials or feedback about the project
    """
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='testimonials')
    author_name = models.CharField(max_length=100)
    author_title = models.CharField(max_length=100, blank=True)
    author_company = models.CharField(max_length=100, blank=True)
    author_image = models.ImageField(upload_to='testimonials/authors/', blank=True, null=True)
    content = models.TextField()
    rating = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        default=5,
        help_text="Rating from 1 to 5 stars"
    )
    is_featured = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-is_featured', '-rating', '-created_at']
    
    def __str__(self):
        return f"Testimonial from {self.author_name} for {self.project.title}"