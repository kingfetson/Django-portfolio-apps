from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.urls import reverse
from django.utils.text import slugify
from portfolio.models import Portfolio

class SkillCategory(models.Model):
    """
    Categories for organizing skills (e.g., Programming, Design, DevOps, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True, help_text="Brief description of this skill category")
    icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="FontAwesome or other icon class (e.g., 'fas fa-code', 'fas fa-paint-brush')"
    )
    icon_color = models.CharField(
        max_length=20, 
        default='#4a6fa5',
        help_text="Hex color for category icon"
    )
    background_color = models.CharField(
        max_length=20, 
        default='#f0f4f8',
        help_text="Background color for category cards"
    )
    order = models.IntegerField(default=0, help_text="Display order (lower numbers first)")
    is_active = models.BooleanField(default=True)
    show_in_chart = models.BooleanField(
        default=True, 
        help_text="Include this category in skills chart"
    )
    show_on_resume = models.BooleanField(
        default=True, 
        help_text="Show skills in this category on resume"
    )
    
    class Meta:
        ordering = ['order', 'name']
        verbose_name = 'Skill Category'
        verbose_name_plural = 'Skill Categories'
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('skills:category', kwargs={'slug': self.slug})
    
    def active_skills_count(self):
        return self.skills.filter(is_active=True).count()
    
    def average_proficiency(self):
        from django.db.models import Avg
        avg = self.skills.filter(is_active=True).aggregate(Avg('proficiency'))['proficiency__avg']
        return round(avg) if avg else 0


class Skill(models.Model):
    """
    Main skill model representing individual skills (e.g., Python, React, Photoshop, etc.)
    """
    # Proficiency Levels
    PROFICIENCY_LEVELS = [
        ('beginner', 'Beginner (1-2 years)'),
        ('intermediate', 'Intermediate (2-4 years)'),
        ('advanced', 'Advanced (4-6 years)'),
        ('expert', 'Expert (6+ years)'),
        ('master', 'Master/Lead (8+ years)'),
    ]
    
    # Skill Types
    SKILL_TYPES = [
        ('technical', 'Technical Skill'),
        ('soft', 'Soft Skill'),
        ('language', 'Programming Language'),
        ('framework', 'Framework/Library'),
        ('tool', 'Tool/Software'),
        ('database', 'Database'),
        ('cloud', 'Cloud/DevOps'),
        ('design', 'Design/UI/UX'),
        ('methodology', 'Methodology'),
        ('certification', 'Certification'),
        ('other', 'Other'),
    ]
    
    # ========== BASIC INFORMATION ==========
    name = models.CharField(max_length=100, unique=True, help_text="Skill name (e.g., Python, React, Photoshop)")
    slug = models.SlugField(max_length=100, unique=True, help_text="URL-friendly version of skill name")
    
    # Description
    description = models.TextField(
        blank=True, 
        help_text="Detailed description of the skill and your experience with it"
    )
    short_description = models.CharField(
        max_length=200, 
        blank=True,
        help_text="Brief description (appears in tooltips and cards)"
    )
    
    # ========== CATEGORIZATION ==========
    category = models.ForeignKey(
        SkillCategory, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True, 
        related_name='skills',
        help_text="Primary skill category"
    )
    secondary_categories = models.ManyToManyField(
        SkillCategory, 
        blank=True, 
        related_name='secondary_skills',
        help_text="Additional categories"
    )
    skill_type = models.CharField(max_length=20, choices=SKILL_TYPES, default='technical')
    
    # ========== PROFICIENCY & EXPERIENCE ==========
    proficiency_level = models.CharField(
        max_length=20, 
        choices=PROFICIENCY_LEVELS, 
        default='intermediate',
        help_text="Overall proficiency level"
    )
    proficiency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)],
        default=70,
        help_text="Proficiency percentage (1-100)"
    )
    years_of_experience = models.DecimalField(
        max_digits=3, 
        decimal_places=1, 
        default=1.0,
        help_text="Years of experience with this skill"
    )
    last_used = models.DateField(
        null=True, 
        blank=True,
        help_text="When you last used this skill professionally"
    )
    first_learned = models.DateField(
        null=True, 
        blank=True,
        help_text="When you first learned this skill"
    )
    
    # ========== VISUAL REPRESENTATION ==========
    icon_class = models.CharField(
        max_length=100, 
        blank=True,
        help_text="Icon class (e.g., 'fab fa-python', 'fab fa-react', 'fas fa-database')"
    )
    icon_image = models.ImageField(
        upload_to='skills/icons/', 
        blank=True, 
        null=True,
        help_text="Custom icon/image for the skill"
    )
    logo = models.ImageField(
        upload_to='skills/logos/', 
        blank=True, 
        null=True,
        help_text="Official technology logo"
    )
    color = models.CharField(
        max_length=20, 
        blank=True,
        default='#3498db',
        help_text="Primary color for skill badge (hex code)"
    )
    gradient_start = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Gradient start color (for progress bars)"
    )
    gradient_end = models.CharField(
        max_length=20, 
        blank=True,
        help_text="Gradient end color (for progress bars)"
    )
    
    # ========== FEATURING & VISIBILITY ==========
    is_featured = models.BooleanField(
        default=False, 
        help_text="Featured skills appear on homepage"
    )
    is_active = models.BooleanField(
        default=True, 
        help_text="Active skills are visible in portfolio"
    )
    show_on_resume = models.BooleanField(
        default=True, 
        help_text="Include this skill in resume/CV"
    )
    show_in_chart = models.BooleanField(
        default=True, 
        help_text="Include in skills proficiency chart"
    )
    featured_order = models.IntegerField(
        default=0, 
        help_text="Order in featured listings (lower = first)"
    )
    resume_order = models.IntegerField(
        default=0, 
        help_text="Order on resume (lower = first)"
    )
    
    # ========== CERTIFICATIONS & VALIDATION ==========
    has_certification = models.BooleanField(default=False)
    certification_name = models.CharField(max_length=200, blank=True)
    certification_url = models.URLField(blank=True, help_text="Link to certification")
    certification_date = models.DateField(null=True, blank=True)
    certification_expiry = models.DateField(null=True, blank=True)
    
    # ========== PROJECTS & ACHIEVEMENTS ==========
    portfolio = models.ForeignKey(
        Portfolio, 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True, 
        related_name='portfolio_skills'
    )
    project_count = models.IntegerField(
        default=0, 
        editable=False,
        help_text="Number of projects using this skill (auto-calculated)"
    )
    
    notable_achievements = models.TextField(
        blank=True,
        help_text="Notable achievements or projects using this skill"
    )
    best_for = models.TextField(
        blank=True,
        help_text="What this skill is best suited for (one per line)"
    )
    limitations = models.TextField(
        blank=True,
        help_text="Known limitations or areas for improvement"
    )
    
    # ========== LINKS & REFERENCES ==========
    official_website = models.URLField(blank=True, help_text="Official technology website")
    documentation_url = models.URLField(blank=True, help_text="Official documentation")
    github_url = models.URLField(blank=True, help_text="GitHub repository/organization")
    learning_resource = models.URLField(
        blank=True, 
        help_text="Recommended learning resource/tutorial"
    )
    marketplace_url = models.URLField(
        blank=True, 
        help_text="Marketplace/profile (e.g., npm, PyPI, Docker Hub)"
    )
    
    # ========== STATISTICS & METADATA ==========
    views = models.PositiveIntegerField(default=0, help_text="Number of profile views")
    interest_score = models.IntegerField(
        default=50,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
        help_text="Current interest level in using this skill (0-100)"
    )
    market_demand = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Demand'),
            ('medium', 'Medium Demand'),
            ('high', 'High Demand'),
            ('very_high', 'Very High Demand'),
        ],
        default='medium',
        help_text="Current market demand for this skill"
    )
    
    # ========== SKILL DETAILS ==========
    current_version = models.CharField(max_length=50, blank=True, help_text="Current/latest version")
    typical_use_case = models.TextField(
        blank=True,
        help_text="Typical use cases for this skill"
    )
    complementary_skills = models.ManyToManyField(
        'self',
        blank=True,
        symmetrical=True,
        help_text="Skills that complement/are used with this skill"
    )
    alternatives = models.TextField(
        blank=True,
        help_text="Alternative technologies/skills"
    )
    
    # ========== SEO & METADATA ==========
    meta_title = models.CharField(max_length=200, blank=True)
    meta_description = models.CharField(max_length=300, blank=True)
    meta_keywords = models.CharField(max_length=200, blank=True)
    
    # ========== SYSTEM FIELDS ==========
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    last_assessed = models.DateTimeField(
        null=True, 
        blank=True,
        help_text="When this skill was last assessed/updated"
    )
    
    class Meta:
        ordering = ['category__order', 'resume_order', 'name']
        indexes = [
            models.Index(fields=['slug']),
            models.Index(fields=['is_active', 'is_featured']),
            models.Index(fields=['proficiency', 'is_active']),
            models.Index(fields=['skill_type', 'is_active']),
        ]
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        # Auto-generate slug if not provided
        if not self.slug:
            self.slug = slugify(self.name)
        
        # Update project count
        if self.pk:
            from projects.models import Project
            self.project_count = Project.objects.filter(skills_used=self).count()
        
        # Update proficiency level based on percentage
        if self.proficiency < 30:
            self.proficiency_level = 'beginner'
        elif self.proficiency < 60:
            self.proficiency_level = 'intermediate'
        elif self.proficiency < 85:
            self.proficiency_level = 'advanced'
        elif self.proficiency < 95:
            self.proficiency_level = 'expert'
        else:
            self.proficiency_level = 'master'
        
        super().save(*args, **kwargs)
    
    def get_absolute_url(self):
        return reverse('skills:detail', kwargs={'slug': self.slug})
    
    def proficiency_stars(self):
        """Convert proficiency to star rating (1-5 stars)"""
        if self.proficiency >= 90:
            return 5
        elif self.proficiency >= 70:
            return 4
        elif self.proficiency >= 50:
            return 3
        elif self.proficiency >= 30:
            return 2
        else:
            return 1
    
    def experience_level(self):
        """Get experience level based on years"""
        if self.years_of_experience >= 8:
            return "Master/Lead"
        elif self.years_of_experience >= 6:
            return "Expert"
        elif self.years_of_experience >= 4:
            return "Advanced"
        elif self.years_of_experience >= 2:
            return "Intermediate"
        else:
            return "Beginner"
    
    def is_current(self):
        """Check if skill is current (used within last 2 years)"""
        if self.last_used:
            from datetime import date, timedelta
            two_years_ago = date.today() - timedelta(days=730)
            return self.last_used >= two_years_ago
        return True
    
    def get_gradient(self):
        """Get CSS gradient for progress bars"""
        if self.gradient_start and self.gradient_end:
            return f"linear-gradient(90deg, {self.gradient_start}, {self.gradient_end})"
        elif self.color:
            return self.color
        return "#3498db"
    
    def related_projects(self, limit=5):
        """Get projects that use this skill"""
        from projects.models import Project
        return Project.objects.filter(skills_used=self, is_published=True)[:limit]
    
    def related_skills(self, limit=5):
        """Get complementary skills"""
        return self.complementary_skills.filter(is_active=True)[:limit]
    
    def increment_views(self):
        """Increment view count"""
        self.views += 1
        self.save(update_fields=['views'])
    
    def update_proficiency(self, new_proficiency, notes=""):
        """Update proficiency with optional notes"""
        old_proficiency = self.proficiency
        self.proficiency = new_proficiency
        self.save()
        
        # Create proficiency history entry
        SkillProficiencyHistory.objects.create(
            skill=self,
            old_proficiency=old_proficiency,
            new_proficiency=new_proficiency,
            notes=notes
        )
    
    def certification_status(self):
        """Get certification status"""
        if not self.has_certification:
            return "No Certification"
        
        if self.certification_expiry:
            from datetime import date
            if date.today() > self.certification_expiry:
                return "Expired"
            else:
                return "Valid"
        
        return "Certified (No Expiry)"


class SkillProficiencyHistory(models.Model):
    """
    Track changes in skill proficiency over time
    """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='proficiency_history')
    old_proficiency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    new_proficiency = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(100)]
    )
    change_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True, help_text="Reason for change or assessment notes")
    
    class Meta:
        ordering = ['-change_date']
        verbose_name = 'Proficiency History'
        verbose_name_plural = 'Proficiency History'
    
    def __str__(self):
        return f"{self.skill.name}: {self.old_proficiency}% → {self.new_proficiency}%"


class SkillRecommendation(models.Model):
    """
    Skill recommendations for career development
    """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='recommendations')
    recommended_skill = models.ForeignKey(
        Skill, 
        on_delete=models.CASCADE, 
        related_name='recommended_by'
    )
    recommendation_type = models.CharField(
        max_length=20,
        choices=[
            ('complementary', 'Complementary Skill'),
            ('next_level', 'Next Level Skill'),
            ('alternative', 'Alternative Technology'),
            ('specialization', 'Specialization'),
            ('prerequisite', 'Prerequisite'),
        ],
        default='complementary'
    )
    priority = models.CharField(
        max_length=20,
        choices=[
            ('low', 'Low Priority'),
            ('medium', 'Medium Priority'),
            ('high', 'High Priority'),
            ('critical', 'Critical'),
        ],
        default='medium'
    )
    reason = models.TextField(blank=True, help_text="Why this skill is recommended")
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['priority', 'recommendation_type']
        unique_together = ['skill', 'recommended_skill']
    
    def __str__(self):
        return f"{self.skill.name} → {self.recommended_skill.name}"


class SkillGroup(models.Model):
    """
    Group related skills together (e.g., MERN Stack, DevOps Tools, etc.)
    """
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)
    color = models.CharField(max_length=20, default='#6c5ce7')
    skills = models.ManyToManyField(Skill, related_name='groups', blank=True)
    order = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        ordering = ['order', 'name']
    
    def __str__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)


class SkillAssessment(models.Model):
    """
    Self-assessment data for skills
    """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='assessments')
    assessment_date = models.DateField()
    
    # Assessment categories
    theoretical_knowledge = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Theoretical understanding (1-10)"
    )
    practical_experience = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Hands-on experience (1-10)"
    )
    problem_solving = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Problem-solving ability (1-10)"
    )
    teaching_ability = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(10)],
        default=5,
        help_text="Ability to teach others (1-10)"
    )
    
    notes = models.TextField(blank=True, help_text="Assessment notes and observations")
    goals = models.TextField(blank=True, help_text="Learning goals for next assessment")
    next_assessment_date = models.DateField(null=True, blank=True)
    
    class Meta:
        ordering = ['-assessment_date']
        unique_together = ['skill', 'assessment_date']
    
    def __str__(self):
        return f"{self.skill.name} Assessment - {self.assessment_date}"
    
    def overall_score(self):
        """Calculate overall assessment score"""
        scores = [
            self.theoretical_knowledge,
            self.practical_experience,
            self.problem_solving,
            self.teaching_ability
        ]
        return sum(scores) / len(scores)


class SkillBadge(models.Model):
    """
    Badges or achievements for skills
    """
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE, related_name='badges')
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    icon_class = models.CharField(max_length=100, blank=True)
    badge_image = models.ImageField(upload_to='skills/badges/', blank=True, null=True)
    earned_date = models.DateField()
    issuer = models.CharField(max_length=100, blank=True)
    verification_url = models.URLField(blank=True)
    
    class Meta:
        ordering = ['-earned_date']
    
    def __str__(self):
        return f"{self.name} - {self.skill.name}"