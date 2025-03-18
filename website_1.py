from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from forms import PersonalDataForm
import sqlite3
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import graphviz
from enum import Enum
import random
import re
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = 'secret_key'

# Cache configuration
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Image processing
def is_image_format_correct(image_path, allowed_formats=('JPEG', 'PNG')):
    try:
        with Image.open(image_path) as img:
            return img.format in allowed_formats
    except IOError:
        return False

# Test result
#repassar depois para um txt também
def calculate_score(answers):
    correct_answers = {
        'AQ1': 'Artificial Intelligence',
        'AQ2': 'Computer Vision',
        'AQ3': 'Artificial Intelligence',
        'AQ4': 'Computer Vision'
    }
    score = sum(1 for key, value in answers.items() if value == correct_answers[key])
    return score

# Model for the people table
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False, index=True)
    age = db.Column(db.Integer)
    learning_preference = db.Column(db.String(50), nullable=False)
    AQ1 = db.Column(db.String(500), nullable=True)
    AQ2 = db.Column(db.String(500), nullable=True)
    AQ3 = db.Column(db.String(500), nullable=True)
    AQ4 = db.Column(db.String(500), nullable=True)
    test_1_score = db.Column(db.Integer, nullable=True)
    test_2_score = db.Column(db.Integer, nullable=True)
    grade_test_1 = db.Column(db.Integer, nullable=True)
    grade_test_2 = db.Column(db.Integer, nullable=True)
    hobbies = db.Column(db.String(500), nullable=True)
    work = db.Column(db.String(500), nullable=True)

# TEST 1
@app.route('/test_1', methods=['GET', 'POST'])
def test_1():
    return render_template('page_2.html', AQ1=session.get('AQ1'), AQ2=session.get('AQ2'))

# TEST 2
@app.route('/test_2', methods=['GET', 'POST'])
def test_2():
    return render_template('page_4.html', AQ3=session.get('AQ3'), AQ4=session.get('AQ4'))

# Analysis of comparison
def generate_comparison_analysis(person):
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Phi-4"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    prompt = (
        f"Compare os resultados dos testes 1 e 2 e forneça uma análise detalhada para a pessoa com as seguintes notas: "
        f"Teste 1: {person.grade_test_1}, Teste 2: {person.grade_test_2}.")

    response = client.complete(
        messages=[UserMessage(content=prompt)],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )

    comparison_analysis = response.choices[0].message.content
    return comparison_analysis


# Validação da syntax mermaid
def is_valid_mermaid_syntax(content):
    try:
        graphviz.Source(content)
        return True
    except Exception as e:
        print(f"Syntax error in text {e}")
        return False


# Removendo parenteses
def remove_parentheses_from_braces(s):
    def replace(match):
        return match.group(0).replace('(', '').replace(')', '')

    return re.sub(r'{[^}]*}', replace, s)


# Personalize content
def generate_custom_content(preference, base_content, hobbies=None, work=None):
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Phi-4"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    if preference == 'Reading, images and diagrams':
        prompt = f"""
        Crie um código mermaid do seguinte texto: {base_content}.
        O diagrama deve conter os principais conceitos. 
        Garanta que a sintaxe esteja correta.
        Retorne APENAS o código mermaid.
        Não usar parênteses dentro de chave, ao gerar código mermaid.

        Exemplo de código mermaid:
        graph TD
            A[Início] --> B(Processo)
            B --> C{{Decisão}}
            C -- Sim --> D[Fim]
            C -- Não --> E[Outro Processo]
            E --> B
        """
        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        mermaid_content = response.choices[0].message.content.strip()

        mermaid_content = remove_parentheses_from_braces(mermaid_content)

        if is_valid_mermaid_syntax(mermaid_content):
            return mermaid_content
        else:
            return "Error: The generated content is not valid Mermaid code."
    elif preference == 'Less Reading and more images':
        prompt = f"Considerando que a pessoa tem hobbies: {hobbies} e trabalha com: {work}, customize o seguinte texto sobre AI para torná-lo mais interessante e relevante para eles: {base_content}. Mantenha o conteúdo informativo e adequado para iniciantes."

        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )

        generated_content = response.choices[0].message.content.strip()
        return generated_content
    else:
        prompt = f"Altere o seguinte texto para a preferência de aprendizado '{preference}': {base_content}"

        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )

        generated_content = response.choices[0].message.content.strip()
        return generated_content


# Rota para processar a pergunta via POST
@app.route('/ask_phi_4', methods=['POST'])
def ask_phi_4():
    question = request.json['question']
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Phi-4"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    prompt = f"Responda à seguinte pergunta sobre inteligência artificial de forma concisa: {question}"

    response = client.complete(
        messages=[UserMessage(content=prompt)],
        temperature=0.7,
        top_p=0.9,
        max_tokens=500,
        model=model_name
    )

    answer = response.choices[0].message.content.strip()
    return jsonify({'answer': answer})

# Função para dividir o conteúdo por tópicos
def load_topics(filename="base_content.txt"):
    with open(filename, "r", encoding="utf-8") as f:
        content = f.read()

    topics = content.split("---TOPIC_SEPARATOR---")
    topic_dict = {}

    for topic in topics:
        lines = topic.strip().split("\n", 1)  # Divide pelo título e conteúdo
        if len(lines) > 1:
            title, body = lines
            topic_dict[title.strip()] = body.strip()

    return topic_dict

TOPICS = load_topics()

# ROTAS DE PÁGINAS
# Personal DATAS - page_1
@app.route('/', methods=['GET', 'POST'])
def index():
    form = PersonalDataForm()
    if request.method == 'POST':
        session['name'] = request.form['name']
        session['hobbies'] = request.form['hobbies']
        session['work'] = request.form['work']
        session['learning_preference'] = request.form['learning_preference']
        session['age'] = request.form['age']

        new_person = Person(
            name=session['name'],
            phone_number=session['phone_number'],
            hobbies=session['hobbies'],
            work=session['work'],
            learning_preference=session['learning_preference'],
            age=session['age']
        )
        db.session.add(new_person)
        db.session.commit()
        session['person_id'] = new_person.id

        return redirect(url_for('page_2'))
    return render_template('page_1.html', form=form)

# TEST 1 - page_2
@app.route('/page_2', methods=['GET', 'POST'])
def page_2():
    if request.method == 'POST':
        answers = {
            'AQ1': request.form['AQ1'],
            'AQ2': request.form['AQ2']
        }
        session['test_1_score'] = calculate_score(answers)

        # Determine the grade for test 2
        if session['test_1_score'] == 4:
            session['grade_test_1'] = 'A'
        elif session['test_1_score'] == 3:
            session['grade_test_1'] = 'B'
        elif session['test_1_score'] == 2:
            session['grade_test_1'] = 'C'
        else:
            session['grade_test_1'] = 'D'

        person_id = session.get('person_id')
        person = db.session.get(Person, person_id)

        if person:
            person.AQ1 = answers['AQ1']
            person.AQ2 = answers['AQ2']
            person.test_1_score = session['test_1_score']
            person.grade_test_1 = session['grade_test_1']
            db.session.commit()

        return render_template('page_2.html', AQ1=session.get('AQ1'), AQ2=session.get('AQ2'))
    return render_template('page_2.html', AQ1=session.get('AQ1'), AQ2=session.get('AQ2'))

# INDEX
@app.route('/page_3')
def page_3():
    with open('index_content.txt', 'r') as f:
        content = [line.strip() for line in f]
    return render_template('page_3.html', content=content)


# TOPIC 1
@app.route('/page_3_1')
def page_3_1():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_1_content = extract_topic_content(base_content, 1)

        if topic_1_content:
            content = generate_custom_content(preference, topic_1_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_1.html', content=content)


# TOPIC 2
@app.route('/page_3_2')
def page_3_2():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 2)  # Get topic 2 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_2.html', content=content)


@app.route('/page_3_3')
def page_3_3():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 3)  # Get topic 3 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_3.html', content=content)


@app.route('/page_3_4')
def page_3_4():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 4)  # Get topic 4 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_4.html', content=content)


@app.route('/page_3_5')
def page_3_5():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 5)  # Get topic 5 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_5.html', content=content)


@app.route('/page_3_6')
def page_3_6():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 6)  # Get topic 6 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_6.html', content=content)


@app.route('/page_3_7')
def page_3_7():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 7)  # Get topic 7 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_7.html', content=content)


@app.route('/page_3_8')
def page_3_8():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 8)  # Get topic 8 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_8.html', content=content)

# TOPIC 9
@app.route('/page_3_9')
def page_3_9():
    with open('base_content.txt', 'r') as f:
        base_content = f.read()
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)

    def extract_topic_content(base_content, topic_number):
        topics = base_content.split('---TOPIC_SEPARATOR---')
        if 1 <= topic_number <= len(topics):
            return topics[topic_number - 1].strip()
        else:
            return None

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        topic_content = extract_topic_content(base_content, 9)  # Get topic 9 content

        if topic_content:
            content = generate_custom_content(preference, topic_content, hobbies, work)
        else:
            content = "Tópico não encontrado."
    else:
        content = "Dados do usuário não encontrados."
    return render_template('page_3_9.html', content=content)

# TEST 2
@app.route('/page_4', methods=['GET', 'POST'])
def page_4():
    if request.method == 'POST':
        answers = {
            'AQ3': request.form['AQ3'],
            'AQ4': request.form['AQ4']
        }
        session['test_2_score'] = calculate_score(answers)

        # Determine the grade for test 2
        if session['test_2_score'] == 4:
            session['grade_test_2'] = 'A'
        elif session['test_2_score'] == 3:
            session['grade_test_2'] = 'B'
        elif session['test_2_score'] == 2:
            session['grade_test_2'] = 'C'
        else:
            session['grade_test_2'] = 'D'

        person_id = session.get('person_id')
        person = db.session.get(Person, person_id)

        if person:
            person.AQ3 = answers['AQ3']
            person.AQ4 = answers['AQ4']
            person.test_2_score = session['test_2_score']
            person.grade_test_2 = session['grade_test_2']
            db.session.commit()

        return render_template('page_4.html', AQ3=session.get('AQ3'), AQ4=session.get('AQ4'))
    return render_template('page_4.html', AQ3=session.get('AQ3'), AQ4=session.get('AQ4'))

@app.route('/last_page')
def last_page():
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)
    if person:
        comparison_analysis = generate_comparison_analysis(person)
    else:
        comparison_analysis = "Análise não disponível."

    return render_template(
        'last_page.html',
        test_1_score=session.get('test_1_score', 0),
        grade_test_1=session.get('grade_test_1', 'N/A'),
        test_2_score=session.get('test_2_score', 0),
        grade_test_2=session.get('grade_test_2', 'N/A'),
        comparison_analysis=comparison_analysis
    )

@app.route('/personal_data')
def personal_data():
    return render_template('personal_data.html')

@app.route('/course_topic/<int:topic_num>')
def course_topic(topic_num):
    page_content = {
        1: {'template': 'page_3_1.html', 'content': 'Conteúdo sobre Python e IA'},
        2: {'template': 'page_3_2.html', 'content': 'Conteúdo sobre IA'},
        3: {'template': 'page_3_3.html', 'content': 'Conteúdo sobre Machine Learning'},
        4: {'template': 'page_3_4.html', 'content': 'Conteúdo sobre Deep Learning'},
        5: {'template': 'page_3_5.html', 'content': 'Conteúdo sobre Natural Language Processing'},
        6: {'template': 'page_3_6.html', 'content': 'Conteúdo sobre Computer Vision'},
        7: {'template': 'page_3_7.html', 'content': 'Conteúdo sobre Image Segmentation Architectures'},
        # Adicione mais páginas conforme necessário
    }

    if topic_num in page_content:
        template_data = page_content[topic_num]
        return render_template(template_data['template'], page_num=topic_num, num_pages=len(page_content),
                               content=template_data['content'])
    else:
        return "Página não encontrada", 404

if __name__ == '__main__':
    app.run(debug=True)