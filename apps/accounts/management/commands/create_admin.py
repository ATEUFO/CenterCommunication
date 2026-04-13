from django.core.management.base import BaseCommand
from accounts.models import User
from academic.models import Establishment, Classroom


class Command(BaseCommand):
    help = 'Crée les utilisateurs administrateur et de test'

    def add_arguments(self, parser):
        parser.add_argument(
            '--reset',
            action='store_true',
            help='Réinitialise les utilisateurs',
        )

    def handle(self, *args, **options):
        self.stdout.write("\n🔐 CRÉATION DES UTILISATEURS\n")

        # Créer l'admin
        self.create_admin_user()
        self.stdout.write("")

        # Créer les utilisateurs de test
        self.create_test_users()
        self.stdout.write("")

        # Créer les données de test
        self.create_test_data()
        self.stdout.write("")

        self.stdout.write(self.style.SUCCESS("\n✅ UTILISATEURS CRÉÉS AVEC SUCCÈS!\n"))
        
        # Afficher le résumé
        self.list_users()

    def create_admin_user(self):
        """Crée l'utilisateur administrateur"""
        username = 'admin'
        email = 'admin@example.com'
        password = 'admin123'

        if User.objects.filter(username=username).exists():
            self.stdout.write(self.style.WARNING(f"✓ Utilisateur '{username}' existe déjà"))
            return

        admin = User.objects.create_superuser(
            username=username,
            email=email,
            password=password,
            role='ADMIN'
        )
        self.stdout.write(self.style.SUCCESS(f"✅ Admin créé: {username}"))
        self.stdout.write(f"   Email: {email}")
        self.stdout.write(f"   Password: {password}")

    def create_test_users(self):
        """Crée des utilisateurs de test"""
        test_users = [
            {
                'username': 'prof_jean',
                'email': 'jean.dupont@school.com',
                'first_name': 'Jean',
                'last_name': 'Dupont',
                'password': 'prof123',
                'role': 'TEACHER'
            },
            {
                'username': 'etudiant_alice',
                'email': 'alice.martin@school.com',
                'first_name': 'Alice',
                'last_name': 'Martin',
                'password': 'etudiant123',
                'role': 'STUDENT'
            },
            {
                'username': 'etudiant_bob',
                'email': 'bob.bernard@school.com',
                'first_name': 'Bob',
                'last_name': 'Bernard',
                'password': 'etudiant123',
                'role': 'STUDENT'
            },
        ]

        for user_data in test_users:
            username = user_data['username']
            if User.objects.filter(username=username).exists():
                self.stdout.write(self.style.WARNING(f"✓ Utilisateur '{username}' existe déjà"))
                continue

            password = user_data.pop('password')
            user = User.objects.create_user(**user_data)
            user.set_password(password)
            user.save()
            self.stdout.write(self.style.SUCCESS(f"✅ User créé: {username}"))

    def create_test_data(self):
        """Crée des données de test"""
        establishment, created = Establishment.objects.get_or_create(
            name='École Primaire Saint-Joseph',
            defaults={'address': '123 Rue de la Paix, Kinshasa'}
        )
        if created:
            self.stdout.write(self.style.SUCCESS(f"✅ Établissement créé: {establishment.name}"))
        else:
            self.stdout.write(self.style.WARNING(f"✓ Établissement existe: {establishment.name}"))

        classrooms_data = [
            ('CP1', establishment),
            ('CP2', establishment),
            ('CE1', establishment),
        ]

        for class_name, estab in classrooms_data:
            classroom, created = Classroom.objects.get_or_create(
                name=class_name,
                establishment=estab
            )
            if created:
                self.stdout.write(self.style.SUCCESS(f"✅ Classe créée: {classroom.name}"))
            else:
                self.stdout.write(self.style.WARNING(f"✓ Classe existe: {classroom.name}"))

    def list_users(self):
        """Affiche la liste des utilisateurs"""
        self.stdout.write(self.style.HTTP_INFO("📋 UTILISATEURS:"))
        for user in User.objects.all():
            self.stdout.write(f"   • {user.username:20} ({user.get_role_display():12}) - {user.email}")
