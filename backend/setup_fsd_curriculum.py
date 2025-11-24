"""
Setup Full-Stack Developer (FSD) Track Curriculum
Creates the FSD track with all 3 projects and their steps
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from curriculum.models import Track, Project, ProjectStep

def setup_fsd_curriculum():
    print("Setting up FSD Track Curriculum...")
    
    # Create or get FSD track
    track, created = Track.objects.get_or_create(
        code='FSD',
        defaults={
            'name': 'Full-Stack Developer',
            'description': 'Build modern web applications from frontend to deployment',
            'duration_weeks': 12,
            'is_active': True
        }
    )
    
    if created:
        print(f"✓ Created track: {track.name}")
    else:
        print(f"✓ Track already exists: {track.name}")
    
    # Project 1: Responsive Portfolio Website
    project1, created = Project.objects.get_or_create(
        track=track,
        number=1,
        defaults={
            'title': 'Responsive Portfolio Website',
            'subtitle': 'React + Tailwind CSS + Netlify',
            'description': 'Build a professional portfolio website using React and Tailwind CSS, then deploy it to Netlify. Master React components, Tailwind styling, and modern deployment workflows.',
            'project_type': 'INTERNAL',
            'tech_stack': ['React', 'Tailwind CSS', 'Vite', 'Netlify CLI'],
            'estimated_hours': 40,
            'order': 1,
            'is_active': True,
            'github_template_repo': '',
            'auto_create_repo': False
        }
    )
    
    if created:
        print(f"  ✓ Created Project 1: {project1.title}")
        
        # Project 1 Steps
        steps = [
            {
                'step_number': 1,
                'title': 'Setup React Project',
                'description': 'Initialize React project with Vite and install Tailwind CSS. Create new React project with Vite, install Tailwind CSS, configure Tailwind, and create basic project structure.',
                'estimated_minutes': 60,
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Build Portfolio Components',
                'description': 'Create Hero, About, Projects, and Contact sections. Create Hero component with introduction, build About section, add Projects showcase, and create Contact form.',
                'estimated_minutes': 180,
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Make it Responsive',
                'description': 'Ensure the portfolio looks great on all devices. Add mobile navigation, test on different screen sizes, optimize images, and add smooth scrolling.',
                'estimated_minutes': 120,
                'order': 3
            },
            {
                'step_number': 4,
                'title': 'Deploy to Netlify',
                'description': 'Deploy your portfolio using Netlify CLI. Install Netlify CLI, build production version, deploy to Netlify, and configure custom domain (optional).',
                'estimated_minutes': 60,
                'order': 4
            }
        ]
        
        for step_data in steps:
            ProjectStep.objects.create(project=project1, **step_data)
        
        print(f"    ✓ Created {len(steps)} steps for Project 1")
    
    # Project 2: E-Commerce Platform
    project2, created = Project.objects.get_or_create(
        track=track,
        number=2,
        defaults={
            'title': 'E-Commerce Platform',
            'subtitle': 'Full-Stack with Stripe Integration',
            'description': 'Build a full-stack e-commerce platform with React frontend, Django/Spring Boot backend, PostgreSQL database, and Stripe payment integration. Learn REST APIs, authentication, and payment processing.',
            'project_type': 'INTERNAL',
            'tech_stack': ['React', 'Django', 'PostgreSQL', 'Stripe', 'REST API'],
            'estimated_hours': 80,
            'order': 2,
            'is_active': True,
            'github_template_repo': '',
            'auto_create_repo': False
        }
    )
    
    if created:
        print(f"  ✓ Created Project 2: {project2.title}")
        
        steps = [
            {
                'step_number': 1,
                'title': 'Setup Backend API',
                'description': 'Create Django/Spring Boot API with authentication. Initialize backend project, setup PostgreSQL database, create user authentication, and build product API endpoints.',
                'estimated_minutes': 240,
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Build Frontend',
                'description': 'Create React frontend with product catalog and cart. Setup React project, create product listing page, build shopping cart, and add user authentication UI.',
                'estimated_minutes': 300,
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Integrate Stripe',
                'description': 'Add payment processing with Stripe. Setup Stripe account, install Stripe SDK, create checkout flow, and handle payment webhooks.',
                'estimated_minutes': 180,
                'order': 3
            },
            {
                'step_number': 4,
                'title': 'Testing & Deployment',
                'description': 'Write tests and deploy the application. Write unit tests, add integration tests, deploy backend to Heroku/Railway, and deploy frontend to Vercel.',
                'estimated_minutes': 180,
                'order': 4
            }
        ]
        
        for step_data in steps:
            ProjectStep.objects.create(project=project2, **step_data)
        
        print(f"    ✓ Created {len(steps)} steps for Project 2")
    
    # Project 3: Social Dashboard + DevOps (Capstone)
    project3, created = Project.objects.get_or_create(
        track=track,
        number=3,
        defaults={
            'title': 'Social Dashboard + DevOps',
            'subtitle': 'Real-time Features + Cloud Deployment',
            'description': 'Build a real-time social dashboard with WebSockets, containerize with Docker, setup CI/CD pipeline, and deploy to AWS/GCP with Terraform. This capstone project demonstrates production-ready full-stack development.',
            'project_type': 'CAPSTONE',
            'tech_stack': ['React', 'Django', 'WebSockets', 'Redis', 'Docker', 'Terraform', 'AWS/GCP', 'CI/CD'],
            'estimated_hours': 120,
            'order': 3,
            'is_active': True,
            'github_template_repo': '',
            'auto_create_repo': False
        }
    )
    
    if created:
        print(f"  ✓ Created Project 3: {project3.title}")
        
        steps = [
            {
                'step_number': 1,
                'title': 'Build Social Dashboard',
                'description': 'Create dashboard with posts, comments, and real-time notifications. Setup React frontend, build Django/Spring Boot backend, implement WebSocket connections, and add Redis for real-time features.',
                'estimated_minutes': 360,
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Containerize with Docker',
                'description': 'Create Docker containers for all services. Write Dockerfiles, create docker-compose.yml, setup multi-stage builds, and optimize image sizes.',
                'estimated_minutes': 180,
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Setup CI/CD',
                'description': 'Create automated deployment pipeline. Setup GitHub Actions, add automated tests, configure deployment workflow, and add environment variables.',
                'estimated_minutes': 180,
                'order': 3
            },
            {
                'step_number': 4,
                'title': 'Deploy to Cloud',
                'description': 'Deploy to AWS/GCP using Terraform. Write Terraform configuration, setup cloud resources, deploy application, and configure monitoring.',
                'estimated_minutes': 240,
                'order': 4
            },
            {
                'step_number': 5,
                'title': 'Create Demo Video',
                'description': 'Record a demo showcasing all features. Plan demo script, record walkthrough, show real-time features, and explain architecture.',
                'estimated_minutes': 120,
                'order': 5
            }
        ]
        
        for step_data in steps:
            ProjectStep.objects.create(project=project3, **step_data)
        
        print(f"    ✓ Created {len(steps)} steps for Project 3")
    
    print("\n✅ FSD Curriculum setup complete!")
    print(f"Track: {track.name} ({track.code})")
    print(f"Projects: {Project.objects.filter(track=track).count()}")
    print(f"Total Steps: {ProjectStep.objects.filter(project__track=track).count()}")

if __name__ == '__main__':
    setup_fsd_curriculum()
