import numpy as np
from numpy import genfromtxt
from lineup_test_2.models import EyewitnessStimuli
data = genfromtxt('lineup_test_2/static/data/sheet1_revised.tsv', dtype=str, names=None, delimiter='\t')

for line1 in data:
    q1 = EyewitnessStimuli(score=line1[0].astype(np.int), lineup_race=line1[2], lineup_number=line1[3],
                           category=line1[4], statement=line1[5], statementOnly=line1[6],
                           chosen_face=line1[7].astype(np.int), lineup_order=line1[8])
    q1.save()

q = EyewitnessStimuli(score=100, lineup_race='W', lineup_number='W1', category='Ex', chosen_face=1, lineup_order="1;2;3;4;5;6", statement='smiley face example', statementOnly='example')
q.save()
