"""
Django management command to enable GitHub integration for DP projects
"""
from django.core.management.base import BaseCommand
from curriculum.models import Project


class Command(BaseCommand):
    help = 'Enable GitHub integration for DP track projects'

    def handle(self, *args, **options):
        self.stdout.write('Enabling GitHub integration for DP projects...')
        
        # Update Project 1
        try:
            project1 = Project.objects.get(track__code='DP', number=1)
            project1.github_template_repo = 'apranova/dp-project1-template'
            project1.auto_create_repo = True
            project1.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Enabled GitHub for Project 1: {project1.title}'))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Project 1 not found'))
        
        # Update Project 2
        try:
            project2 = Project.objects.get(track__code='DP', number=2)
            project2.github_template_repo = 'apranova/dp-project2-template'
            project2.auto_create_repo = True
            project2.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Enabled GitHub for Project 2: {project2.title}'))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Project 2 not found'))
        
        # Update Project 3
        try:
            project3 = Project.objects.get(track__code='DP', number=3)
            project3.github_template_repo = 'apranova/dp-project3-template'
            project3.auto_create_repo = True
            project3.save()
            self.stdout.write(self.style.SUCCESS(f'✅ Enabled GitHub for Project 3: {project3.title}'))
        except Project.DoesNotExist:
            self.stdout.write(self.style.ERROR('❌ Project 3 not found'))
        
        self.stdout.write('\n' + '='*50)
        self.stdout.write(self.style.SUCCESS('GitHub integration enabled for all DP projects!'))
        self.stdout.write('='*50)
        self.stdout.write('\nDP students can now:')
        self.stdout.write('  ✅ Click "Start Project" to create GitHub repo')
        self.stdout.write('  ✅ Work in their own repository')
        self.stdout.write('  ✅ Create Pull Requests for review')
        self.stdout.write('  ✅ Get trainer feedback via GitHub')
        self.stdout.write('  ✅ Follow Git workflow like FSD students')
