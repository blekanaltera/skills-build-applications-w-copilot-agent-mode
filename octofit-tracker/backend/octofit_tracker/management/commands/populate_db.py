from django.core.management.base import BaseCommand
from django.contrib.auth import get_user_model
from djongo import models
from pymongo import MongoClient

# Define models for teams, activities, leaderboard, and workouts
class Team(models.Model):
    name = models.CharField(max_length=100, unique=True)
    class Meta:
        app_label = 'octofit_tracker'

class Activity(models.Model):
    user = models.CharField(max_length=100)
    type = models.CharField(max_length=100)
    duration = models.IntegerField()
    team = models.CharField(max_length=100)
    class Meta:
        app_label = 'octofit_tracker'

class Leaderboard(models.Model):
    team = models.CharField(max_length=100)
    points = models.IntegerField()
    class Meta:
        app_label = 'octofit_tracker'

class Workout(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=50)
    class Meta:
        app_label = 'octofit_tracker'

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        User = get_user_model()
        # Connect to MongoDB
        client = MongoClient('mongodb://localhost:27017')
        db = client['octofit_db']

        # Clear collections
        db.users.delete_many({})
        db.teams.delete_many({})
        db.activities.delete_many({})
        db.leaderboard.delete_many({})
        db.workouts.delete_many({})

        # Create unique index on email
        db.users.create_index('email', unique=True)

        # Sample users (superheroes)
        users = [
            {'username': 'ironman', 'email': 'ironman@marvel.com', 'team': 'marvel'},
            {'username': 'captainamerica', 'email': 'cap@marvel.com', 'team': 'marvel'},
            {'username': 'batman', 'email': 'batman@dc.com', 'team': 'dc'},
            {'username': 'wonderwoman', 'email': 'wonderwoman@dc.com', 'team': 'dc'},
        ]
        db.users.insert_many(users)

        # Teams
        teams = [
            {'name': 'marvel'},
            {'name': 'dc'},
        ]
        db.teams.insert_many(teams)

        # Activities
        activities = [
            {'user': 'ironman', 'type': 'run', 'duration': 30, 'team': 'marvel'},
            {'user': 'captainamerica', 'type': 'cycle', 'duration': 45, 'team': 'marvel'},
            {'user': 'batman', 'type': 'swim', 'duration': 25, 'team': 'dc'},
            {'user': 'wonderwoman', 'type': 'yoga', 'duration': 40, 'team': 'dc'},
        ]
        db.activities.insert_many(activities)

        # Leaderboard
        leaderboard = [
            {'team': 'marvel', 'points': 75},
            {'team': 'dc', 'points': 65},
        ]
        db.leaderboard.insert_many(leaderboard)

        # Workouts
        workouts = [
            {'name': 'Super Strength', 'description': 'Strength workout for heroes', 'difficulty': 'hard'},
            {'name': 'Agility Training', 'description': 'Improve your agility', 'difficulty': 'medium'},
        ]
        db.workouts.insert_many(workouts)

        self.stdout.write(self.style.SUCCESS('octofit_db database populated with test data.'))
