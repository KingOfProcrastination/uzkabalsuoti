from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from database import Member, Vote, Law
from config import DB_SESSION, DB_URL

app = Flask(__name__, template_folder='template')
app.secret_key = 'your_secret_key_here'  # needed for session
app.config['SQLALCHEMY_DATABASE_URI'] = DB_URL
db = SQLAlchemy(app)

CATEGORIES = [
    "Ekonomika ir finansai", "Socialinė apsauga, sveikata ir ugdymas", "Infrastruktūra ir aplinkosauga",
    "Valstybės saugumas ir teisėtvarka", "Kultūra", "Tarptautiniai santykiai"
]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        selected_categories = request.form.getlist('categories')
        num_laws = int(request.form.get('num_laws', 5))
        session['selected_categories'] = selected_categories
        session['num_laws'] = num_laws
        return redirect(url_for('vote'))
    return render_template('index.html', categories=CATEGORIES)

@app.route('/vote', methods=['GET', 'POST'])
def vote():
    selected_categories = session.get('selected_categories', [])
    num_laws = session.get('num_laws', 5)
    if not selected_categories:
        return redirect(url_for('index'))

    if request.method == 'POST':
        votes = request.form.to_dict()
        session['votes'] = votes
        return redirect(url_for('results'))

    law_changes = get_random_law_changes(selected_categories, num_laws)
    return render_template('vote.html', law_changes=law_changes)

@app.route('/results')
def results():
    votes = session.get('votes', {})
    if not votes:
        return redirect(url_for('index'))

    member_results, party_results, group_results = calculate_results(votes)
    return render_template('results.html', member_results=member_results, party_results=party_results, group_results=group_results)

def get_random_law_changes(categories, num_laws):
    laws = DB_SESSION.query(Law).filter(Law.document_category.in_(categories), Law.document_importance_score.in_(['7', '8', '9', '10'])).order_by(db.func.random()).limit(num_laws).all()
    return [{"id": law.vote_id, "summary": law.document_summary, "category": law.document_category} for law in laws]

def calculate_results(user_votes):
    member_results = []
    party_results = {}
    group_results = {}

    for vote_key, user_vote in user_votes.items():
        vote_id = int(vote_key.split('_')[1])
        user_vote_value = 3 if user_vote == "Susilaikyti" else (1 if user_vote == "Už" else 2)

        votes = DB_SESSION.query(Vote).filter_by(vote_id=vote_id).all()
        for vote in votes:
            similarity = 1 if user_vote_value == vote.vote else 0
            member = vote.member
            if member.member_id not in [m['id'] for m in member_results]:
                member_results.append({
                    'id': member.member_id,
                    'name': f"{member.name} {member.surname}",
                    'similarity': similarity,
                    'total_votes': 1
                })
            else:
                for m in member_results:
                    if m['id'] == member.member_id:
                        m['similarity'] += similarity
                        m['total_votes'] += 1
                        break

            if member.nominating_party not in party_results:
                party_results[member.nominating_party] = {'similarity': similarity, 'total_votes': 1}
            else:
                party_results[member.nominating_party]['similarity'] += similarity
                party_results[member.nominating_party]['total_votes'] += 1

            if member.group not in group_results:
                group_results[member.group] = {'similarity': similarity, 'total_votes': 1}
            else:
                group_results[member.group]['similarity'] += similarity
                group_results[member.group]['total_votes'] += 1

    for member in member_results:
        member['similarity'] = (member['similarity'] / member['total_votes']) * 100

    party_results = [
        {"name": party, "similarity": (data['similarity'] / data['total_votes']) * 100}
        for party, data in party_results.items()
    ]

    group_results = [
        {"name": group, "similarity": (data['similarity'] / data['total_votes']) * 100}
        for group, data in group_results.items()
    ]

    member_results.sort(key=lambda x: x['similarity'], reverse=True)
    party_results.sort(key=lambda x: x['similarity'], reverse=True)
    group_results.sort(key=lambda x: x['similarity'], reverse=True)

    return member_results[:10], party_results, group_results

if __name__ == '__main__':
    app.run(debug=True)