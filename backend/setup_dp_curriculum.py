"""
Setup Data Professional (DP) Track Curriculum
"""
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'core.settings')
django.setup()

from curriculum.models import Track, Project, ProjectStep, Deliverable


def setup_dp_curriculum():
    """Create DP track with all 3 projects"""
    
    # Create or get DP Track
    dp_track, created = Track.objects.get_or_create(
        code='DP',
        defaults={
            'name': 'Data Professional',
            'description': 'Master data analysis, ETL pipelines, and cloud analytics',
            'icon': 'database',
            'duration_weeks': 12,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created DP Track: {dp_track.name}")
    else:
        print(f"ℹ️  DP Track already exists: {dp_track.name}")
    
    # Project 1: Business Analytics Dashboard
    project1, created = Project.objects.get_or_create(
        track=dp_track,
        number=1,
        defaults={
            'title': 'Business Analytics Dashboard',
            'subtitle': 'Python + PostgreSQL + Apache Superset',
            'description': 'Build an interactive dashboard using Python, PostgreSQL, and Apache Superset. Clean raw CSV data, load into database, write SQL queries, and create visualizations.',
            'project_type': 'INTERNAL',
            'tech_stack': ['Python', 'Pandas', 'PostgreSQL', 'Apache Superset', 'Jupyter Lab'],
            'estimated_hours': 40,
            'order': 1,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created Project 1: {project1.title}")
        
        # Add steps for Project 1
        steps_p1 = [
            {
                'step_number': 1,
                'title': 'Clean Raw CSV Dataset',
                'description': 'Use Jupyter Lab to load, explore, and clean the provided dataset. Handle missing values, fix data types, and remove duplicates.',
                'estimated_minutes': 240,
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Load Data into PostgreSQL',
                'description': 'Connect to your PostgreSQL schema and load the cleaned data using SQLAlchemy or psycopg2.',
                'estimated_minutes': 120,
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Write SQL Queries for KPIs',
                'description': 'Create SQL queries to calculate key metrics, aggregations, and business insights.',
                'estimated_minutes': 240,
                'order': 3
            },
            {
                'step_number': 4,
                'title': 'Connect Superset to PostgreSQL',
                'description': 'Configure Apache Superset to connect to your database schema.',
                'estimated_minutes': 60,
                'order': 4
            },
            {
                'step_number': 5,
                'title': 'Build Interactive Dashboard',
                'description': 'Create visualizations, add filters, and design an interactive dashboard in Superset.',
                'estimated_minutes': 360,
                'order': 5
            },
            {
                'step_number': 6,
                'title': 'Write Insights Report',
                'description': 'Summarize findings in a 1-page PDF report highlighting key insights and recommendations.',
                'estimated_minutes': 120,
                'order': 6
            }
        ]
        
        for step_data in steps_p1:
            ProjectStep.objects.create(project=project1, **step_data)
        
        # Add deliverables for Project 1
        deliverables_p1 = [
            {
                'title': 'Superset Dashboard URL',
                'description': 'Link to your published Superset dashboard',
                'deliverable_type': 'LINK',
                'is_required': True,
                'order': 1
            },
            {
                'title': 'SQL Queries',
                'description': 'GitHub repo or file with your SQL queries',
                'deliverable_type': 'GITHUB',
                'is_required': True,
                'order': 2
            },
            {
                'title': 'PDF Insights Report',
                'description': '1-page report with key findings',
                'deliverable_type': 'FILE',
                'is_required': True,
                'order': 3
            },
            {
                'title': 'Python Cleaning Script',
                'description': 'Optional: Your data cleaning script',
                'deliverable_type': 'GITHUB',
                'is_required': False,
                'order': 4
            }
        ]
        
        for deliv_data in deliverables_p1:
            Deliverable.objects.create(project=project1, **deliv_data)
    
    # Project 2: Automated ETL Pipeline
    project2, created = Project.objects.get_or_create(
        track=dp_track,
        number=2,
        defaults={
            'title': 'Automated ETL Pipeline',
            'subtitle': 'Python + Prefect + PostgreSQL',
            'description': 'Build an automated data pipeline with Prefect orchestration. Extract data from REST API, transform with Pandas, load into PostgreSQL, and schedule with Prefect.',
            'project_type': 'INTERNAL',
            'tech_stack': ['Python', 'Prefect', 'PostgreSQL', 'REST API', 'Pandas'],
            'estimated_hours': 60,
            'order': 2,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created Project 2: {project2.title}")
        
        # Add steps for Project 2
        steps_p2 = [
            {
                'step_number': 1,
                'title': 'Extract Data from REST API',
                'description': 'Use Python requests library to pull data from a public API. Handle pagination and error cases.',
                'estimated_minutes': 240,
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Transform Data with Pandas',
                'description': 'Clean, normalize, and transform the API data. Apply business logic and data validation.',
                'estimated_minutes': 360,
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Load to PostgreSQL',
                'description': 'Insert transformed data into your database schema. Handle upserts and data conflicts.',
                'estimated_minutes': 240,
                'order': 3
            },
            {
                'step_number': 4,
                'title': 'Create Prefect Workflow',
                'description': 'Build a Prefect flow to orchestrate the ETL pipeline.',
                'estimated_minutes': 360,
                'order': 4
            },
            {
                'step_number': 5,
                'title': 'Schedule and Monitor',
                'description': 'Set up scheduling, monitoring, and email notifications in Prefect.',
                'estimated_minutes': 240,
                'order': 5
            }
        ]
        
        for step_data in steps_p2:
            ProjectStep.objects.create(project=project2, **step_data)
        
        # Add deliverables for Project 2
        deliverables_p2 = [
            {
                'title': 'Python ETL Script',
                'description': 'GitHub repository with your ETL code',
                'deliverable_type': 'GITHUB',
                'is_required': True,
                'order': 1
            },
            {
                'title': 'Prefect Workflow DAG',
                'description': 'Screenshot or export of your Prefect workflow',
                'deliverable_type': 'FILE',
                'is_required': True,
                'order': 2
            },
            {
                'title': 'PostgreSQL Table',
                'description': 'Database connection details showing loaded data',
                'deliverable_type': 'TEXT',
                'is_required': True,
                'order': 3
            },
            {
                'title': 'Email Report Screenshot',
                'description': 'Screenshot of automated email report',
                'deliverable_type': 'FILE',
                'is_required': True,
                'order': 4
            }
        ]
        
        for deliv_data in deliverables_p2:
            Deliverable.objects.create(project=project2, **deliv_data)
    
    # Project 3: End-to-End Analytics Solution (Capstone)
    project3, created = Project.objects.get_or_create(
        track=dp_track,
        number=3,
        defaults={
            'title': 'End-to-End Analytics Solution',
            'subtitle': 'BigQuery/Redshift + dbt + Looker/Tableau',
            'description': 'Build a cloud-hosted analytics solution. Combine multiple data sources, load to cloud data warehouse, transform with dbt, and create production dashboards.',
            'project_type': 'CAPSTONE',
            'tech_stack': ['Python', 'BigQuery', 'dbt', 'Looker Studio', 'Airflow'],
            'estimated_hours': 100,
            'order': 3,
            'is_active': True
        }
    )
    
    if created:
        print(f"✅ Created Project 3: {project3.title}")
        
        # Add steps for Project 3
        steps_p3 = [
            {
                'step_number': 1,
                'title': 'Combine Multiple Data Sources',
                'description': 'Extract data from multiple sources (APIs, databases, files). Merge and reconcile data.',
                'estimated_minutes': 480,
                'order': 1
            },
            {
                'step_number': 2,
                'title': 'Load to Cloud Data Warehouse',
                'description': 'Setup BigQuery/Redshift, design schema, and load data. Optimize for query performance.',
                'estimated_minutes': 360,
                'order': 2
            },
            {
                'step_number': 3,
                'title': 'Transform with dbt',
                'description': 'Use dbt to create data models, apply transformations, and build analytics-ready tables.',
                'estimated_minutes': 600,
                'order': 3
            },
            {
                'step_number': 4,
                'title': 'Build Cloud Dashboard',
                'description': 'Create interactive dashboards in Looker/Tableau. Add filters, drill-downs, and export capabilities.',
                'estimated_minutes': 720,
                'order': 4
            }
        ]
        
        for step_data in steps_p3:
            ProjectStep.objects.create(project=project3, **step_data)
        
        # Add deliverables for Project 3
        deliverables_p3 = [
            {
                'title': 'Cloud-Hosted Dashboard URL',
                'description': 'Link to your Looker/Tableau dashboard',
                'deliverable_type': 'LINK',
                'is_required': True,
                'order': 1
            },
            {
                'title': 'SQL Scripts',
                'description': 'GitHub repository with dbt models and SQL scripts',
                'deliverable_type': 'GITHUB',
                'is_required': True,
                'order': 2
            },
            {
                'title': 'PDF Case Study Report',
                'description': 'Comprehensive report with insights and recommendations',
                'deliverable_type': 'FILE',
                'is_required': True,
                'order': 3
            }
        ]
        
        for deliv_data in deliverables_p3:
            Deliverable.objects.create(project=project3, **deliv_data)
    
    print("\n" + "="*50)
    print("DP CURRICULUM SETUP COMPLETE!")
    print("="*50)
    print(f"\nTrack: {dp_track.name}")
    print(f"Projects: {Project.objects.filter(track=dp_track).count()}")
    print(f"Total Steps: {ProjectStep.objects.filter(project__track=dp_track).count()}")
    print(f"Total Deliverables: {Deliverable.objects.filter(project__track=dp_track).count()}")
    print("\nProjects:")
    for p in Project.objects.filter(track=dp_track).order_by('number'):
        print(f"  {p.number}. {p.title} ({p.steps.count()} steps, {p.deliverables.count()} deliverables)")


if __name__ == '__main__':
    setup_dp_curriculum()
