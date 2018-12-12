import sys
sys.path.append(".")

import sqlite3
import config as cfg

conn = sqlite3.connect(cfg.PATH_DATABASE)

total = conn.execute("""
  SELECT
    participant.name
  FROM survey_key
    JOIN survey ON survey.id = survey_key.id_survey
    JOIN participant ON participant.id = survey_key.id_participant
  WHERE
    survey_key.id_participant NOT NULL
    AND survey.filename LIKE "%001_%"
    AND participant.name NOT LIKE "%stefan eng%"
""").fetchall()

submitted = conn.execute("""
  SELECT
    participant.name
  FROM survey_key
    JOIN survey ON survey.id = survey_key.id_survey
    JOIN participant ON participant.id = survey_key.id_participant
    JOIN submission ON participant.id = submission.id_participant
  WHERE
    survey_key.id_participant NOT NULL
    AND survey.filename LIKE "%001_%"
    AND participant.name NOT LIKE "%stefan eng%"
""").fetchall()

num_total = len(total)
num_submitted = len(submitted)

plot_type="pie"
labels = ["Submitted", "Non-submitted"]
values = [num_submitted, num_total-num_submitted]
