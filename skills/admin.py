from django.contrib import admin
from .models import (
    SkillCategory, Skill, SkillProficiencyHistory, 
    SkillRecommendation, SkillGroup, SkillAssessment, SkillBadge
)

@admin.register(SkillCategory)
class SkillCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active', 'show_in_chart', 'show_on_resume')
    list_editable = ('order', 'is_active', 'show_in_chart', 'show_on_resume')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name', 'description')

@admin.register(Skill)
class SkillAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'proficiency_level', 'proficiency', 
                   'years_of_experience', 'is_featured', 'is_active')
    list_filter = ('skill_type', 'proficiency_level', 'is_featured', 'is_active', 'category')
    list_editable = ('proficiency', 'is_featured', 'is_active')
    search_fields = ('name', 'description', 'short_description')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('secondary_categories', 'complementary_skills')
    readonly_fields = ('project_count', 'views')
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'description', 'short_description')
        }),
        ('Categorization', {
            'fields': ('category', 'secondary_categories', 'skill_type')
        }),
        ('Proficiency', {
            'fields': ('proficiency_level', 'proficiency', 'years_of_experience',
                      'first_learned', 'last_used')
        }),
        ('Visuals', {
            'fields': ('icon_class', 'icon_image', 'logo', 'color', 
                      'gradient_start', 'gradient_end')
        }),
        ('Visibility', {
            'fields': ('is_featured', 'is_active', 'show_on_resume', 
                      'show_in_chart', 'featured_order', 'resume_order')
        }),
        ('Certifications', {
            'fields': ('has_certification', 'certification_name', 
                      'certification_url', 'certification_date', 
                      'certification_expiry')
        }),
        ('Links', {
            'fields': ('official_website', 'documentation_url', 'github_url',
                      'learning_resource', 'marketplace_url')
        }),
        ('Details', {
            'fields': ('current_version', 'typical_use_case', 
                      'complementary_skills', 'alternatives',
                      'notable_achievements', 'best_for', 'limitations')
        }),
        ('Stats', {
            'fields': ('project_count', 'views', 'interest_score', 
                      'market_demand', 'created_at', 'updated_at')
        }),
    )

# Register other models...
@admin.register(SkillProficiencyHistory)
class SkillProficiencyHistoryAdmin(admin.ModelAdmin):
    list_display = ('skill', 'old_proficiency', 'new_proficiency', 'change_date')
    list_filter = ('change_date',)
    search_fields = ('skill__name', 'notes')

@admin.register(SkillGroup)
class SkillGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'order', 'is_active')
    list_editable = ('order', 'is_active')
    prepopulated_fields = {'slug': ('name',)}
    filter_horizontal = ('skills',)