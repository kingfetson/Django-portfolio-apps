# Django Portfolio Apps - Installation & Setup Guide

## 🚀 Quick Start

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Virtual environment (recommended)

### Installation Steps

1. **Clone the Repository**
   ```bash
   git clone <your-repository-url>
   cd Django-portfolio-apps
   ```

2. **Create and Activate Virtual Environment**

   # Create virtual environment
   python -m venv venv

   # Activate it
   # On Windows:
   venv\Scripts\activate
   # On Mac/Linux:
   source venv/bin/activate
   ```

3. **Install Dependencies**
   
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables**
   Create a `.env` file in the project root:
   ```env
   SECRET_KEY=your-secret-key-here
   DEBUG=True
   ALLOWED_HOSTS=localhost,127.0.0.1
   DATABASE_URL=sqlite:///db.sqlite3
   ```

5. **Apply Database Migrations**
   
   python manage.py migrate
   ```

6. **Create Superuser (Admin)**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run Development Server**
   ```bash
   python manage.py runserver
   ```
   Visit: http://localhost:8000

---

## 📦 Installed Apps Overview

### Core Django Apps
| App | Purpose |
|-----|---------|
| `django.contrib.admin` | Django admin interface |
| `django.contrib.auth` | Authentication system |
| `django.contrib.contenttypes` | Content type framework |
| `django.contrib.sessions` | Session management |
| `django.contrib.messages` | Messaging framework |
| `django.contrib.staticfiles` | Static file serving |

### REST Framework & Authentication
- `rest_framework` - Django REST Framework for APIs
- `rest_framework.authtoken` - Token-based authentication

### Portfolio Components
| App | Description | Features |
|-----|-------------|----------|
| `portfolio` | Main portfolio app | Core models, settings |
| `landing` | Landing page | Homepage, hero section |
| `menu` | Navigation system | Dynamic menus, links |
| `blog` | Blog system | Posts, categories, comments |
| `gallery` | Image gallery | Photo collections, albums |
| `resume` | CV/Resume | Work history, education |
| `travel` | Travel journal | Travel logs, locations |
| `store` | E-commerce | Products, cart, orders |
| `pricing` | Pricing plans | Subscription tiers |
| `event` | Events calendar | Event management |
| `dishes` | Food/Recipes | Recipe collection |
| `skills` | Skills showcase | Technical skills, proficiency |
| `projects` | Project portfolio | Project listings, details |
| `api_integrations` | External APIs | Weather, quotes, GitHub |

---

## 🔧 Configuration

### Settings Example
```python
# settings.py
INSTALLED_APPS = [
    # Default Django apps
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    # DRF & auth token
    'rest_framework',
    'rest_framework.authtoken',

    # Portfolio apps
    'portfolio',
    'landing',
    'menu',
    'blog',
    'gallery',
    'resume',
    'travel',
    'store',
    'pricing',
    'event',
    'dishes',
    'skills', 
    'projects',
    'api_integrations',
]

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ]
}
```

### Database Setup

# PostgreSQL example
pip install psycopg2-binary

# Update DATABASES in settings.py
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'portfolio_db',
        'USER': 'your_user',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

---

## 📁 Project Structure
```
Django-portfolio-apps/
├── portfolio/          # Main app
├── landing/           # Landing pages
├── menu/              # Navigation system
├── blog/              # Blog functionality
├── gallery/           # Image galleries
├── resume/            # CV/Resume management
├── travel/            # Travel journal
├── store/             # E-commerce
├── pricing/           # Pricing plans
├── event/             # Event management
├── dishes/            # Recipes collection
├── skills/            # Skills showcase
├── projects/          # Project portfolio
├── api_integrations/  # External API integrations
├── templates/         # Base templates
├── static/            # Static files
├── media/             # Uploaded files
├── requirements.txt   # Python dependencies
└── manage.py          # Django management
```

---

## 🛠️ Management Commands

### Common Operations
```bash
# Make migrations
python manage.py makemigrations

# Apply migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Collect static files
python manage.py collectstatic

# Run tests
python manage.py test

# Start development server
python manage.py runserver

# Create app
python manage.py startapp app_name
```

### App-Specific Commands

# Import portfolio data
python manage.py import_portfolio_data

# Generate sitemap
python manage.py generate_sitemap

# Backup database
python manage.py dbbackup
```

---

## 🔌 API Endpoints

### Available APIs
- `/api/projects/` - Projects listing
- `/api/skills/` - Skills API
- `/api/blog/` - Blog posts
- `/api/gallery/` - Gallery images
- `/api/portfolio/` - Portfolio data
- `/api-auth/` - DRF authentication

### Example API Usage

# Get all projects
curl http://localhost:8000/api/projects/

# Get specific project
curl http://localhost:8000/api/projects/1/

# Authenticated request
curl -H "Authorization: Token your-token-here" http://localhost:8000/api/projects/
```

---

## 🌐 Frontend Features

### Responsive Design
- Mobile-first approach
- Dark/light theme toggle
- Accessible navigation
- Progressive enhancement

### Widgets & Integrations
- Weather widget
- GitHub activity
- Daily inspirational quotes
- Social media feeds

### Interactive Elements
- Project filters
- Image lightbox
- Contact forms
- Live search
- Comment system

---

## 🚢 Deployment

### Production Checklist
1. ✅ Set `DEBUG = False`
2. ✅ Configure `ALLOWED_HOSTS`
3. ✅ Set up database (PostgreSQL recommended)
4. ✅ Configure static files (Whitenoise or CDN)
5. ✅ Set up email backend
6. ✅ Configure security settings
7. ✅ Set up logging
8. ✅ Configure caching

### Deployment Options
- **Heroku**: `git push heroku main`
- **PythonAnywhere**: Web interface deployment
- **AWS**: Elastic Beanstalk or EC2
- **DigitalOcean**: Django droplet
- **Vercel/Railway**: Serverless options

### Environment Variables for Production
```env
SECRET_KEY=your-production-secret-key
DEBUG=False
ALLOWED_HOSTS=yourdomain.com,www.yourdomain.com
DATABASE_URL=postgres://user:pass@host:port/dbname
EMAIL_HOST=smtp.gmail.com
EMAIL_PORT=587
EMAIL_USE_TLS=True
```

---

## 🔒 Security

### Required Settings

# settings.py - Production security
SECURE_SSL_REDIRECT = True
SESSION_COOKIE_SECURE = True
CSRF_COOKIE_SECURE = True
SECURE_BROWSER_XSS_FILTER = True
SECURE_CONTENT_TYPE_NOSNIFF = True
X_FRAME_OPTIONS = 'DENY'
SECURE_HSTS_SECONDS = 31536000  # 1 year
SECURE_HSTS_INCLUDE_SUBDOMAINS = True
SECURE_HSTS_PRELOAD = True
```

### Regular Maintenance

# Update packages
pip install --upgrade -r requirements.txt

# Check security vulnerabilities
pip-audit

# Run security checks
python manage.py check --deploy


---

## 📊 Database Schema Overview

### Key Models
- **Portfolio**: User profile, contact info
- **Project**: Portfolio projects with details
- **Skill**: Technical skills with proficiency
- **BlogPost**: Articles and tutorials
- **GalleryImage**: Photo gallery items
- **ResumeItem**: Work experience, education
- **TravelLog**: Travel experiences
- **Product**: Store items
- **Event**: Calendar events
- **Dish**: Recipes and cooking

---

## 🆘 Troubleshooting

### Common Issues

1. **Migration Errors**
   ```bash
   # Reset migrations (development only)
   find . -path "*/migrations/*.py" -not -name "__init__.py" -delete
   find . -path "*/migrations/*.pyc" -delete
   python manage.py makemigrations
   python manage.py migrate
   ```

2. **Static Files Not Loading**
   ```bash
   # Collect static files
   python manage.py collectstatic --noinput
   
   # Check STATIC_ROOT and STATIC_URL in settings
   ```

3. **Admin Not Accessible**
   ```bash
   # Create superuser
   python manage.py createsuperuser
   
   # Check admin URL patterns
   ```

4. **API Authentication Issues**
   ```bash
   # Generate API token
   python manage.py drf_create_token username
   ```

---

## 📚 Documentation Links

- [Django Documentation](https://docs.djangoproject.com/)
- [Django REST Framework](https://www.django-rest-framework.org/)
- [Python Documentation](https://docs.python.org/)
- [Bootstrap Documentation](https://getbootstrap.com/docs/)

---

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Write/update tests
5. Update documentation
6. Submit a pull request

---

## 📄 License
[MIT License](LICENSE) - See LICENSE file for details

---

## 🎯 Features Roadmap

### Phase 1 (Complete)
- [x] Basic portfolio structure
- [x] Landing page template
- [x] Navigation system
- [x] Blog functionality

### Phase 2 (In Progress)
- [ ] E-commerce store
- [ ] Advanced gallery
- [ ] Event calendar
- [ ] API integrations

### Phase 3 (Planned)
- [ ] Multi-language support
- [ ] Advanced analytics
- [ ] Mobile app
- [ ] Payment integration

---

## 📞 Support

- **Issues**: [GitHub Issues](https://github.com/your-username/Django-portfolio-apps/issues)
- **Email**: your-email@example.com
- **Documentation**: [Read the Docs](https://your-docs-site.com)

---

*Last Updated: January 2024*