from flask import Flask, render_template, request, redirect, url_for, session
from models import db, User, Quiz, Result, Score
from config import Config

app = Flask(__name__)
app.config.from_object(Config)
db.init_app(app)


#@app.before_first_request
def create_tables():
    db.create_all()


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        username = request.form['username']
        user = User.query.filter_by(username=username).first()
        if not user:
            user = User(username=username)
            db.session.add(user)
            db.session.commit()
        session['user_id'] = user.id
        return redirect(url_for('quiz'))
    return render_template('index.html')


@app.route('/quiz', methods=['GET', 'POST'])
def quiz():
    user_id = session.get('user_id')
    if not user_id:
        return redirect(url_for('index'))

    questions = Quiz.query.all()
    if request.method == 'POST':
        score = 0
        for question in questions:
            selected = request.form.get(str(question.id))
            if selected == question.correct_answer:
                score += 20
        result = Result(score=score, user_id=user_id)
        db.session.add(result)
        db.session.commit()
        return redirect(url_for('result'))

    return render_template('quiz.html', questions=questions)


@app.route('/result')
def result():
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    last_score = user.results[-1].score
    max_score = max([r.score for r in user.results])

    all_scores = Result.query.all()
    global_high_score = max([r.score for r in all_scores]) if all_scores else 0

    return render_template('result.html',
                           last_score=last_score,
                           max_score=max_score,
                           global_high_score=global_high_score)


@app.route('/submit', methods=['POST'])
def submit():
    username = request.form.get("username")
    answers = request.form.to_dict()
    answers.pop("username", None)

    correct = 0
    for qid, answer in answers.items():
        question = Quiz.query.get(int(qid))
        if question and answer == question.correct_answer:
            correct += 1

    # Yeni skor ekle
    new_score = Score(username=username, score=correct)
    db.session.add(new_score)
    db.session.commit()

    return redirect(url_for("result", username=username))




if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)