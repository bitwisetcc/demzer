import pandas as pd
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# Carregar dados
students = pd.read_csv("students.csv")
teachers = pd.read_csv("teachers.csv")
subjects = pd.read_csv("subjects.csv")
courses = pd.read_csv("courses.csv")

total_students = len(students)
total_teachers = len(teachers)
total_courses = len(courses)
total_subjects = len(subjects)

students_gender_count = students['gender'].value_counts().reset_index()
students_gender_count.columns = ['gender', 'count']

teachers_gender_count = teachers['gender'].value_counts().reset_index()
teachers_gender_count.columns = ['gender', 'count']

course_subjects = courses[['name', 'subjects']].copy()
course_subjects['subjects'] = course_subjects['subjects'].str.split()
course_subjects = course_subjects.explode('subjects')


fig = make_subplots(
    rows=3, cols=2,
    specs=[[{"type": "domain"}, {"type": "domain"}],
           [{"type": "xy"}, {"type": "xy"}],
           [{"type": "xy"}, {"type": "xy"}]],
    subplot_titles=[
        "👨‍🎓 Total de Alunos", "👩‍🏫 Total de Professores",
        "📊 Alunos por Gênero", "👥 Professores por Gênero",
        "📚 Disciplinas por Curso", ""
    ]
)

# Indicadores
fig.add_trace(go.Indicator(mode="number", value=total_students,
                           title={"text": "<b>Alunos</b>"},
                           number={"font": {"size": 48, "color": "royalblue"}}), row=1, col=1)

fig.add_trace(go.Indicator(mode="number", value=total_teachers,
                           title={"text": "<b>Professores</b>"},
                           number={"font": {"size": 48, "color": "mediumseagreen"}}), row=1, col=2)

# Alunos por gênero
fig.add_trace(go.Bar(
    x=students_gender_count['gender'],
    y=students_gender_count['count'],
    marker_color=['royalblue', 'deeppink'],
    text=students_gender_count['count'],
    textposition='auto',
), row=2, col=1)

# Professores por gênero
fig.add_trace(go.Bar(
    x=teachers_gender_count['gender'],
    y=teachers_gender_count['count'],
    marker_color='mediumseagreen',
    text=teachers_gender_count['count'],
    textposition='auto',
), row=2, col=2)

# Disciplinas por curso
fig.add_trace(go.Histogram(
    x=course_subjects['name'],
    marker_color='indianred',
), row=3, col=1)

# Layout estilizado
fig.update_layout(
    height=900,
    width=1150,
    title={
        'text': "🎓 <b>Dashboard Educacional DEMZER</b>",
        'x': 0.5,
        'xanchor': 'center',
        'font': {'size': 28}
    },
    paper_bgcolor="#f9f9f9",
    plot_bgcolor="#ffffff",
    font=dict(family="Arial", size=14, color="#333"),
    margin=dict(t=100, b=50, l=50, r=50),
    bargap=0.3,
    showlegend=False
)

fig.show()
