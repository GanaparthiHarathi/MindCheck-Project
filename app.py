from flask import Flask, render_template, request, redirect, url_for, flash
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-change-this'

# Depression screening questions (simplified version based on PHQ-9 concepts)
SCREENING_QUESTIONS = [
    " lose interest in activities that you normally enjoy?",
    " feel sad, down, or hopeless?",
    " have difficulty falling asleep, staying asleep, or sleep more than usual?",
    " feel tired or have very little energy?",
    " eat much less or much more than usual?",
    " feel like you were a failure or let yourself or your loved ones down?",
    " find it difficult to concentrate on tasks such as studying, reading, or watching television?",
    " move or speak unusually slowly, or feel so restless that it was hard to sit still?",
    " have thoughts that you would be better off dead or of hurting yourself in some way?"
]

ANSWER_OPTIONS = [
    (0, "Not at all"),
    (1, "Several days"),
    (2, "More than half the days"),
    (3, "Nearly every day")
]

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/screening')
def screening():
    return render_template(
        'questionnaire.html',
        questions=SCREENING_QUESTIONS,
        options=ANSWER_OPTIONS
    )

@app.route('/submit_screening', methods=['POST'])
def submit_screening():
    # Calculate total score
    total_score = 0
    responses = []
    
    for i in range(len(SCREENING_QUESTIONS)):
        answer = int(request.form.get(f'q_{i}', 0))
        total_score += answer
        responses.append(answer)
    
    # Interpret results (simplified interpretation)
    if total_score==0:
        severity="NO Depression"
        recommendation = """
        You appear to have no symptoms of depression.
        Continue maintaining healthy sleep, exercise and social habits.
        """
        color = "success"

    elif total_score <= 4:
        severity = "Minimal"
        recommendation = """
        You appear to have minimal symptoms of depression.
        Continue maintaining healthy sleep, exercise and social habits.
        """
        color = "success"

    elif total_score <= 9:
        severity = "Mild"
        recommendation = """
        You may be experiencing mild symptoms of depression.
        Consider talking with family members, friends, or a counselor.
        """
        color = "warning"

    elif total_score <= 14:
        severity = "Moderate"
        recommendation = """
        Your responses indicate moderate depressive symptoms.
        Seeking guidance from a mental health professional is recommended.
        """
        color = "warning"   

    elif total_score <= 19:
        severity = "Moderately Severe"
        recommendation = """
        Your symptoms appear significant.
        Professional psychological support is strongly recommended.
        """
        color = "danger"

    else:
        severity = "Severe"
        recommendation = """
        Your responses indicate severe depressive symptoms.
        Please seek immediate support from a qualified mental health professional.
        """
        color = "danger"
    
    return render_template('results.html', 
                         score=total_score, 
                         severity=severity,
                         recommendation=recommendation,
                         color=color)

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/submit_contact', methods=['POST'])
def submit_contact():
    name = request.form.get('name')
    email = request.form.get('email')
    message = request.form.get('message')

    flash(f'Thank you {name}! Your message has been received. We will get back to you at {email}.', 'success')

    return redirect(url_for('contact'))

@app.route('/resources')
def resources():
    return render_template('resources.html')

import os

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))