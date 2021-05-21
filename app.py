from flask import Flask, render_template, request, redirect
from flask_debugtoolbar import DebugToolbarExtension
from surveys import satisfaction_survey as survey

app = Flask(__name__)

app.config['SECRET_KEY'] = 'secretkey'
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
debug = DebugToolbarExtension(app)

RESPONSES = []


@app.route('/')
def home_page():

    """Shows homepage with start survey button"""
    
    return render_template('start_survey.html', survey=survey)


@app.route('/start-survey', methods=["POST"])
def start_survey():

    """Clears RESPONSES of previous answers, sets to an empty list.  Then redirects to first question of survey."""
    
    RESPONSES.clear()

    return redirect('/questions/0')


@app.route('/answer', methods=["POST"])
def handle_answer():

    """Retrieves answer from form, appends answer to RESPONSES list and redirects to next question"""

    answer = request.form["answer"]
    RESPONSES.append(answer)

    if len(RESPONSES) < len(survey.questions):
        num = len(RESPONSES)
        return redirect(f'/questions/{num}')

    else:
        return redirect('/survey-complete')



@app.route('/questions/<int:qnum>')
def display_question(qnum):

    """Takes you to the first question of the survey after the start button is clicked"""
    
    question = survey.questions[qnum]
    num = qnum

    if RESPONSES is None:
        return redirect('/')
    
    if len(RESPONSES) == len(survey.questions):
        return redirect('/survey-complete')

    if len(RESPONSES) != num:
        return redirect(f'/questions/{ len(RESPONSES) }')

    return render_template('question.html', num=num, question=question)


@app.route('/survey-complete')
def survey_complete_msg():

    """"Displays survey complete message once survey has been completed"""
   
    return render_template('survey-complete.html')