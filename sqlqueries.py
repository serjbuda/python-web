import os

queries = [
    "SELECT name, AVG(mark) as avg_mark FROM Students s, Marks m WHERE s.id = m.student_id GROUP BY s.id ORDER BY avg_mark DESC LIMIT 5;",
    "SELECT s.name, AVG(m.mark) as avg_mark FROM Students s, Marks m, Subjects sub WHERE s.id = m.student_id AND m.subject_id = sub.id AND sub.name = 'Math' GROUP BY s.id ORDER BY avg_mark DESC LIMIT 1;",
    "SELECT g.name, AVG(m.mark) as avg_mark FROM Groups g, Students s, Marks m, Subjects sub WHERE g.id = s.group_id AND s.id = m.student_id AND m.subject_id = sub.id AND sub.name = 'Math' GROUP BY g.id;",
    "SELECT AVG(mark) as avg_mark FROM Marks;",
    "SELECT sub.name FROM Teachers t, Subjects sub WHERE t.id = sub.teacher_id AND t.name = 'Smith';",
    "SELECT name FROM Students WHERE group_id = (SELECT id FROM Groups WHERE name = 'Group A');",
    "SELECT s.name, m.mark FROM Students s, Marks m, Subjects sub, Groups g WHERE s.id = m.student_id AND m.subject_id = sub.id AND s.group_id = g.id AND g.name = 'Group A' AND sub.name = 'Math';",
    "SELECT AVG(m.mark) as avg_mark FROM Marks m, Subjects sub, Teachers t WHERE m.subject_id = sub.id AND sub.teacher_id = t.id AND t.name = 'Smith';",
    "SELECT sub.name FROM Students s, Marks m, Subjects sub WHERE s.id = m.student_id AND m.subject_id = sub.id AND s.name = 'John Smith';",
    "SELECT sub.name FROM Students s, Marks m, Subjects sub, Teachers t WHERE s.id = m.student_id AND m.subject_id = sub.id AND sub.teacher_id = t.id AND s.name = 'John Smith' AND t.name = 'Smith';"
]

dir_name = "queries"

if not os.path.exists(dir_name):
    os.makedirs(dir_name)

for i, query in enumerate(queries):
    with open(f"{dir_name}/query_{i+1}.sql", "w") as f:
        f.write(query)
