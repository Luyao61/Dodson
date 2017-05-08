from django.db import models


# Create your models here.
class EyewitnessStimuli(models.Model):

    CONFIDENCE_SCORE = ( (60, 60), (80, 80), (100, 100), )
    LINEUP_RACE = (('B', 'black'), ('W', 'white'), )
    LINEUP_NUMBER = (
        ('B1', 'B1'), ('B2', 'B2'), ('B3', 'B3'), ('B4', 'B4'), ('B5', 'B5'), ('B6', 'B6'),
        ('W1', 'W1'), ('W2', 'W2'), ('W3', 'W3'), ('W4', 'W4'), ('W5', 'W5'), ('W6', 'W6'),
    )
    CATEGORY = (('O1', 'O1'), ('Omany', 'Omany'), ('R', 'R'), ('U1', 'U1'), ('F', 'F'), )
    CHOICE = ((1, 1), (2, 2), (3, 3),(4, 4), (5, 5), (6, 6),)

    score = models.IntegerField(choices=CONFIDENCE_SCORE)
    lineup_race = models.CharField(max_length=1, choices=LINEUP_RACE)
    lineup_number = models.CharField(max_length=2, choices=LINEUP_NUMBER)
    category = models.CharField(max_length=10, choices=CATEGORY)
    statement = models.TextField(max_length=100)    # confidence statement and justification
    statementOnly = models.TextField(max_length=100)    # confidence statement only
    chosen_face = models.IntegerField(choices=CHOICE)
    lineup_order = models.CharField(max_length=14)

    def __str__(self):
        return self.category + "; " + self.lineup_number+"; "+ self.statement


class Users(models.Model):
    SEX = (('M', 'Male'), ('F', 'Female'))
    userId = models.CharField(max_length=14, primary_key=True)

    # This if StatementType = true, user will see full statement (confidence statement and justification)
    # This if StatementType = false, user will see statement only
    StatementType = models.BooleanField()

    sex = models.CharField(max_length=1, choices=SEX, null=True)
    birth_year = models.IntegerField(null=True)
    race = models.CharField(max_length=10, null=True)
    device = models.CharField(max_length=10, null=True)
    comments = models.CharField(max_length=100, null=True)

    def __str__(self):
        return self.userId


class Response(models.Model):
    CONFIDENCE_SCORE = ( (0, 0), (20, 20), (40, 40), (60, 60), (80, 80), (100, 100), )
    CATEGORY = (('O1', 'O1'), ('Omany', 'Omany'), ('R', 'R'), ('U1', 'U1'), ('F', 'F'), )

    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    question = models.ForeignKey(EyewitnessStimuli, on_delete=models.CASCADE)
    answer = models.IntegerField(choices=CONFIDENCE_SCORE, null=True)

    category = models.CharField(max_length=10, choices=CATEGORY)

    def __str__(self):
        return self.user.userId
