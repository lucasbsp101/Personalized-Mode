
from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from forms import PersonalDataForm
import sqlite3
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import graphviz


#Imports PHI-4
import os
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
#Imports PHI-4

#Image processing
def is_image_format_correct(image_path, allowed_formats=('JPEG', 'PNG')):
    try:
        with Image.open(image_path) as img:
            if img.format in allowed_formats:
                return True
            else:
                return False
    except IOError:
        return False
#Image processing

app = Flask(__name__)
app.secret_key = 'secret_key'  # Important for using sessions

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)


#Test result
def calculate_score(answers):
    correct_answers = {
        'AQ1': 'Artificial Intelligence',
        'AQ2': 'Computer Vision',
        'AQ3': 'Artificial Intelligence',
        'AQ4': 'Computer Vision'
    }
    score = 0
    for key, value in answers.items():
        if value == correct_answers[key]:
            score += 1
    return score
#Test result

# Model for the people table
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    phone_number = db.Column(db.String(50), nullable=False)
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

# Analysis of comparison
def generate_comparison_analysis(person):
    # Configuração do cliente do modelo phi-4
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Phi-4"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    prompt = f"Compare os resultados dos testes 1 e 2 e forneça uma análise detalhada para a pessoa com as seguintes notas: Teste 1: {person.grade_test_1}, Teste 2: {person.grade_test_2}."

    response = client.complete(
        messages=[UserMessage(content=prompt)],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )

    comparison_analysis = response.choices[0].message.content
    return comparison_analysis
# Analysis of comparison

# Think map creation
# Função para gerar conteúdo personalizado

def generate_custom_content(preference, base_content, hobbies=None, work=None):
    # Configuração do cliente do modelo phi-4
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Phi-4"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    if preference == 'Think Map':
        # Use o modelo phi-4 para gerar o fluxograma diretamente no formato mermaid
        prompt = f"Crie um código mermaid do seguinte texto, garante todas as pontuações, elimine ```mermaid: {base_content}. O diagrama deve conter os principais conceitos. Garanta que a sintaxe esteja correta. Retorne APENAS o código mermaid."
        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )
        mermaid_content = response.choices[0].message.content.strip()

        # Valide o conteúdo mermaid gerado
        if is_valid_mermaid_syntax(mermaid_content):
            return mermaid_content
        else:
            return "Error: The generated content is not valid Mermaid code."
    elif preference == 'Text':
        # Personalize o conteúdo com base nos hobbies e no trabalho
        prompt = f"Considering that the person has hobbies: {hobbies} and works with: {work}, customize the following text about AI to make it more interesting and relevant for them: {base_content}. Keep the content informative and suitable for beginners."

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
        prompt = f"Change the following text to the learning preference '{preference}': {base_content}"

        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=1.0,
            top_p=1.0,
            max_tokens=1000,
            model=model_name
        )

        generated_content = response.choices[0].message.content.strip()
        return generated_content
# Think map creation

# Função para validar a sintaxe mermaid
def is_valid_mermaid_syntax(content):
    try:
        # Tente compilar o conteúdo mermaid usando a biblioteca graphviz
        graphviz.Source(content)
        return True
    except Exception as e:
        print(f"Syntax error in text {e}")
        return False
# Função para validar a sintaxe mermaid


# Page - Personal data
@app.route('/', methods=['GET', 'POST'])
def index():
    form = PersonalDataForm()
    image_path = os.path.join(app.static_folder, 'images', 'a.png')

    if not is_image_format_correct(image_path):
        return "Formato de imagem incorreto. Por favor, use uma imagem JPEG ou PNG.", 400


    if form.validate_on_submit():
        name = form.name.data
        phone_number = form.phone_number.data
        learning_preference = request.form['learning_preference']
        age = request.form['age']
        hobbies = form.hobbies.data
        work = form.work.data

        # Save data to the database
        person = Person(name=name, phone_number=phone_number, learning_preference=learning_preference, age=age, hobbies=hobbies, work=work)
        db.session.add(person)
        db.session.commit()

        # Store data in session
        session['person_id'] = person.id

        return redirect(url_for('test_1'))

    return render_template('personal_data.html', form=form)

# Page - test_1
@app.route('/test_1', methods=['GET', 'POST'])
def test_1():
    # Check if personal data was entered
    if 'person_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'AQ1' in request.form and 'AQ2' in request.form:
            AQ1 = request.form['AQ1']
            AQ2 = request.form['AQ2']

            # Update test responses in the database
            person = db.session.get(Person, session['person_id'])
            person.AQ1 = AQ1
            person.AQ2 = AQ2
            person.test_1_score = calculate_score({'AQ1': AQ1, 'AQ2': AQ2})
            db.session.commit()

            return redirect(url_for('course', AQ1=AQ1, AQ2=AQ2))
        else:
            return "Form data is missing", 400

    return render_template('test_1.html')


# Page - course
@app.route('/course')
def course():
    if 'person_id' not in session:
        return redirect(url_for('index'))

    AQ1 = request.args.get('AQ1')
    AQ2 = request.args.get('AQ2')
    person = db.session.get(Person, session['person_id'])
    learning_preference = person.learning_preference
    hobbies = person.hobbies
    work = person.work

#Colocar futuramente esse texto em um arquivo txt fora e melhorar
    base_content = """
    AI stands for Artificial Intelligence, a field of computer science dedicated to creating machines capable of performing tasks that would normally require human intelligence.
    There are several subgroups of AI, such as:
    - Machine Learning
    - Artificial Neural Networks
    - Natural Language Processing (NLP)
    - Computer Vision
    AI has applications in various areas, from virtual assistants to autonomous cars.
    """

    custom_content = generate_custom_content(learning_preference, base_content, hobbies, work)
    print("Mermaid Content:", custom_content)  # Adicione esta linha

    if learning_preference == 'Audio':
        return render_template('course_audio.html', AQ1=AQ1, AQ2=AQ2, content=custom_content)
    elif learning_preference == 'Think Map':
        return render_template('course_fluxograma.html', AQ1=AQ1, AQ2=AQ2, mermaid_content=custom_content)
    else:
        return render_template('course.html', AQ1=AQ1, AQ2=AQ2, content=custom_content)

# Page - test_2
@app.route('/test_2', methods=['GET', 'POST'])
def test_2():
    # Check if personal data was entered
    if 'person_id' not in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        if 'AQ3' in request.form and 'AQ4' in request.form:
            AQ1 = request.form['AQ1']
            AQ2 = request.form['AQ2']
            AQ3 = request.form['AQ3']
            AQ4 = request.form['AQ4']

            # Update test responses in the database
            person = db.session.get(Person, session['person_id'])
            person.AQ3 = AQ3
            person.AQ4 = AQ4
            person.test_2_score = calculate_score({'AQ3': AQ3, 'AQ4': AQ4})
            db.session.commit()

            return redirect(url_for('comparison', AQ1=AQ1, AQ2=AQ2, AQ3=AQ3, AQ4=AQ4))
        else:
            return "Form data is missing", 400

    return render_template('test_2.html')

# Page - comparison (developing...)
@app.route('/comparison')
def comparison():
    if 'person_id' not in session:
        return redirect(url_for('index'))

    person = db.session.get(Person, session['person_id'])
    total_questions_test_1 = 2  # Total de perguntas no teste 1
    total_questions_test_2 = 2  # Total de perguntas no teste 2

    grade_test_1 = (person.test_1_score / total_questions_test_1) * 10 if person.test_1_score is not None else 0
    grade_test_2 = (person.test_2_score / total_questions_test_2) * 10 if person.test_2_score is not None else 0

    person.grade_test_1 = grade_test_1
    person.grade_test_2 = grade_test_2
    db.session.commit()

    # Gerar análise de comparação usando o modelo phi-4
    comparison_analysis = generate_comparison_analysis(person)

    return render_template('comparison.html',
                           test_1_score=person.test_1_score,
                           test_2_score=person.test_2_score,
                           grade_test_1=grade_test_1,
                           grade_test_2=grade_test_2,
                           comparison_analysis=comparison_analysis)

# Rota para lidar com a pergunta e obter a resposta do modelo phi-4
@app.route('/ask_phi_4', methods=['POST'])
def ask_phi_4():
    data = request.get_json()
    question = data['question']

    # Configuração do cliente do modelo phi-4
    endpoint = "https://models.inference.ai.azure.com"
    model_name = "Phi-4"
    token = os.environ["GITHUB_TOKEN"]

    client = ChatCompletionsClient(
        endpoint=endpoint,
        credential=AzureKeyCredential(token),
    )

    response = client.complete(
        messages=[UserMessage(content=question)],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )

    answer = response.choices[0].message.content
    return jsonify({'answer': answer})

if __name__ == '__main__':
    app.run(debug=True)