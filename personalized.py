#VERSÃO 2

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from forms import PersonalDataForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
import os
import re
from azure.ai.inference import ChatCompletionsClient
from azure.ai.inference.models import UserMessage
from azure.core.credentials import AzureKeyCredential
from flask_caching import Cache

app = Flask(__name__)
app.secret_key = 'secret_key'

app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///database.db')

# Cache configuration
cache = Cache(app, config={'CACHE_TYPE': 'simple'})

# Database configuration
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize the database
db = SQLAlchemy(app)
migrate = Migrate(app, db)

#Student's Project
@app.route('/analyze_sentiment', methods=['POST'])
def analyze_sentiment():
    try:
        data = request.get_json()
        text = data['text']

        endpoint = "https://models.inference.ai.azure.com"
        model_name = "Phi-4"
        token = os.environ["GITHUB_TOKEN"]

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )

        prompt = f"Analyze the sentiment of the following text and return 'positive', 'negative', or 'neutral', and the confidence: {text}"

        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=0.7,
            top_p=0.9,
            max_tokens=500,
            model=model_name
        )

        result = response.choices[0].message.content.strip()

        # Debugging: Exibir a resposta bruta da API
        print(f"API Response (Raw): {result}")

        # Extração de sentimento e confiança usando expressões regulares ajustadas
        try:
            sentiment_match = re.search(r"sentiment of the text is '(\w+)'", result, re.IGNORECASE)
            confidence_match = re.search(r"Confidence:\s*(\w+)", result, re.IGNORECASE)

            if sentiment_match and confidence_match:
                sentiment = sentiment_match.group(1).lower()
                confidence = confidence_match.group(1)
                return jsonify({'sentiment': sentiment, 'confidence': confidence})
            else:
                if not sentiment_match:
                    return jsonify({'error': 'Sentiment not found in API response'}), 500
                if not confidence_match:
                    return jsonify({'error': 'Confidence not found in API response'}), 500
                return jsonify({'error': 'Could not extract sentiment and confidence from API response (regex mismatch)'}), 500

        except Exception as regex_error:
            return jsonify({'error': f'Error during regex extraction: {regex_error}'}), 500

    except Exception as api_error:
        return jsonify({'error': f'Error during API call: {api_error}'}), 500

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
        'AQ1': 'd',
        'AQ2': 'd',
        'AQ3': 'e',
        'AQ4': 'b',
        'AQ5': 'd',
        'AQ6': 'b',
        'AQ7': 'd',
        'AQ8': 'e',
        'AQ9': 'e',
        'AQ10': 'e',
        'AQ11': 'd',
        'AQ12': 'd',
        'AQ13': 'e',
        'AQ14': 'b',
        'AQ15': 'd',
        'AQ16': 'b',
        'AQ17': 'd',
        'AQ18': 'e',
        'AQ19': 'e',
        'AQ20': 'e'
        }
    score = sum(1 for key, value in answers.items() if value == correct_answers[key])
    return score

# Model for the people table
class Person(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    age = db.Column(db.Integer)
    learning_preference = db.Column(db.String(50), nullable=False)
    test_1_score = db.Column(db.Integer, nullable=True)
    test_2_score = db.Column(db.Integer, nullable=True)
    grade_test_1 = db.Column(db.Integer, nullable=True)
    grade_test_2 = db.Column(db.Integer, nullable=True)
    hobbies = db.Column(db.String(500), nullable=True)
    work = db.Column(db.String(500), nullable=True)
    feedback = db.Column(db.String(500), nullable=True)
    AQ1 = db.Column(db.String(500), nullable=True)
    AQ2 = db.Column(db.String(500), nullable=True)
    AQ3 = db.Column(db.String(500), nullable=True)
    AQ4 = db.Column(db.String(500), nullable=True)
    AQ5 = db.Column(db.String(500), nullable=True)
    AQ6 = db.Column(db.String(500), nullable=True)
    AQ7 = db.Column(db.String(500), nullable=True)
    AQ8 = db.Column(db.String(500), nullable=True)
    AQ9 = db.Column(db.String(500), nullable=True)
    AQ10 = db.Column(db.String(500), nullable=True)
    AQ11 = db.Column(db.String(500), nullable=True)
    AQ12 = db.Column(db.String(500), nullable=True)
    AQ13 = db.Column(db.String(500), nullable=True)
    AQ14 = db.Column(db.String(500), nullable=True)
    AQ15 = db.Column(db.String(500), nullable=True)
    AQ16 = db.Column(db.String(500), nullable=True)
    AQ17 = db.Column(db.String(500), nullable=True)
    AQ18 = db.Column(db.String(500), nullable=True)
    AQ19 = db.Column(db.String(500), nullable=True)
    AQ20 = db.Column(db.String(500), nullable=True)

    def calculate_grades(self):
        if self.test_1_score is not None:
            self.grade_test_1 = self.test_1_score * 0.1  # Exemplo de cálculo
        if self.test_2_score is not None:
            self.grade_test_2 = self.test_2_score * 0.1  # Exemplo de cálculo

    def save(self):
        self.calculate_grades()
        db.session.add(self)
        db.session.commit()

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
        f"Compare the results of tests 1 and 2 and "
        f"provide a detailed analysis for the person with the following scores: "
        f"Test 1: {person.grade_test_1}, Test 2: {person.grade_test_2}."
        "Be more mainly"
        "Speak like a teenager, using {person.hobbies} and {person.work} as examples."
        )

    response = client.complete(
        messages=[UserMessage(content=prompt)],
        temperature=1.0,
        top_p=1.0,
        max_tokens=1000,
        model=model_name
    )

    comparison_analysis = response.choices[0].message.content
    return comparison_analysis

# Personalize content
def generate_custom_content(learning_preference, base_content, hobbies=None, work=None):
    if learning_preference == 'Personalized Teaching':
        endpoint = "https://models.inference.ai.azure.com"
        model_name = "Phi-4"
        token = os.environ["GITHUB_TOKEN"]

        client = ChatCompletionsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(token),
        )
        # output with hmtl - deu muito certo as linhas 117 a 121, ele foi muito mais produtivo em linhas e icones
        #apenas a linha 122 ainda nao funciona, testar mais vezes e pesquisar
        prompt = f"""
        Personalize each topic of the content{base_content} based on the person's hobbies{hobbies} and work{work}. 
        Rewrite to teenagers between 18 and 25 years!
        Make it more personal!
        Make it more engaging!
        In the {base_content}, when you read Example:, create an example that is related to the person's hobbies{hobbies} and work{work}.
        Don't send: ``` This HTML document encapsulates your interests and aligns Python's applications with your personal hobbies and academic pursuits, 
        making the content not only informative but also entertaining and relatable.
        Don't send: ```html to {generate_custom_content}
        Don't change the color of fonts, use just white"""

        response = client.complete(
            messages=[UserMessage(content=prompt)],
            temperature=1,
            top_p=1,
            max_tokens=1000,
            model=model_name
        )
        generated_content = response.choices[0].message.content.strip()
        return generated_content #retorna o conteudo personalizado
    else:
        return base_content #retorna o conteudo base

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
def load_specific_topics(filename="base_content.txt", topics_to_load=None):
    """
    Carrega tópicos específicos do arquivo, filtrando por prefixos de título.

    Args:
        filename (str, optional): O nome do arquivo de onde carregar os tópicos.
                                  Padrão é "base_content.txt".
        topics_to_load (list, optional): Uma lista de prefixos de título para filtrar os tópicos.
                                         Se None, usa ["1_1", "1_2"].

    Returns:
        dict: Um dicionário onde as chaves são os títulos dos tópicos encontrados
              e os valores são os corpos dos tópicos.
    """
    if topics_to_load is None:
        topics_to_load = ["1_1", "1_2", "1_3", "1_4"]

    topic_dict = {}
    try:
        with open(filename, "r", encoding="utf-8") as f:
            content = f.read()

        topics = content.split("---TOPIC_SEPARATOR---")

        for topic in topics:
            lines = topic.strip().split("\n", 1)  # Divide pelo título e conteúdo
            if lines:
                title = lines[0].strip()
                print(f"Título encontrado: {title}")
                if title and any(title.startswith(t) for t in topics_to_load):
                    body = lines[1].strip() if len(lines) > 1 else "Conteúdo não encontrado."
                    topic_dict[title] = body
    except FileNotFoundError:
        print(f"Arquivo não encontrado: {filename}")
    except Exception as e:
        print(f"Ocorreu um erro ao processar o arquivo: {e}")

    return topic_dict #retorna o dicionário com os tópicos específicos

# ROTAS DE PÁGINAS
def extract_topic_content(base_content, topic_number):
    topics = base_content.split('---TOPIC_SEPARATOR---')
    if 1 <= topic_number <= len(topics):
        return topics[topic_number - 1].strip()
    else:
        return None

# Last REVIEW - PAGES
@app.route('/page_3_1') #OK
def page_3_1():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_1 = extract_topic_content(base_content, 1) #Each TOPIC SEPARATOR is ONE
    topic_2 = extract_topic_content(base_content, 2)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_1:
                topic_1 = generate_custom_content(preference, topic_1, hobbies, work)
            if topic_2:
                topic_2 = generate_custom_content(preference, topic_2, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_1 = "Dados pessoais do usuário não encontrados."
        topic_2 = "Dados pessoais do usuário não encontrados."


    return render_template('page_3_1.html',
                           topic_1=topic_1,
                           topic_2=topic_2,)

@app.route('/page_3_2') #OK
def page_3_2():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_3 = extract_topic_content(base_content, 3)
    topic_4 = extract_topic_content(base_content, 4)


    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_3:
                topic_3 = generate_custom_content(preference, topic_3, hobbies, work)
            if topic_4:
                topic_4 = generate_custom_content(preference, topic_4, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo
    else:
        topic_3 = "Dados do usuário não encontrados."
        topic_4 = "Dados do usuário não encontrados."
    return render_template('page_3_2.html',
                           topic_3=topic_3,
                           topic_4=topic_4)

@app.route('/page_3_3') #OK
def page_3_3():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_5 = extract_topic_content(base_content, 5)
    topic_6 = extract_topic_content(base_content, 6)
    topic_7 = extract_topic_content(base_content, 7)


    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_5:
                topic_5 = generate_custom_content(preference, topic_5, hobbies, work)
            if topic_6:
                topic_6 = generate_custom_content(preference, topic_6, hobbies, work)
            if topic_7:
                topic_7 = generate_custom_content(preference, topic_7, hobbies, work)

        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_5 = "Dados do usuário não encontrados."
        topic_6 = "Dados do usuário não encontrados."
        topic_7 = "Dados do usuário não encontrados."


    return render_template('page_3_3.html',
                           topic_5=topic_5,
                           topic_6=topic_6,
                           topic_7=topic_7,
                           )

@app.route('/page_3_4') #
def page_3_4():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_8 = extract_topic_content(base_content, 8)
    topic_9 = extract_topic_content(base_content, 9)
    topic_10 = extract_topic_content(base_content, 10)
    topic_11 = extract_topic_content(base_content, 11)
    topic_12 = extract_topic_content(base_content, 12)
    topic_13 = extract_topic_content(base_content, 13)
    topic_14 = extract_topic_content(base_content, 14)
    topic_21 = extract_topic_content(base_content, 21)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_8:
                topic_8 = generate_custom_content(preference, topic_8, hobbies, work)
            if topic_9:
                topic_9 = generate_custom_content(preference, topic_9, hobbies, work)
            if topic_10:
                topic_10 = generate_custom_content(preference, topic_10, hobbies, work)
            if topic_11:
                topic_11 = generate_custom_content(preference, topic_11, hobbies, work)
            if topic_12:
                topic_12 = generate_custom_content(preference, topic_12, hobbies, work)
            if topic_13:
                topic_13 = generate_custom_content(preference, topic_13, hobbies, work)
            if topic_14:
                topic_14 = generate_custom_content(preference, topic_14, hobbies, work)
            if topic_21:
                topic_21 = generate_custom_content(preference, topic_21, hobbies, work)
            else:
                # Se for Generic Teaching, usa o conteúdo extraído diretamente
                pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_8 = "Dados do usuário não encontrados."
        topic_9 = "Dados do usuário não encontrados."
        topic_10 = "Dados do usuário não encontrados."
        topic_11 = "Dados do usuário não encontrados."
        topic_12 = "Dados do usuário não encontrados."
        topic_13 = "Dados do usuário não encontrados."
        topic_14 = "Dados do usuário não encontrados."
        topic_21 = "Dados do usuário não encontrados."

    return render_template('page_3_4.html',
                           topic_8=topic_8,
                           topic_9=topic_9,
                           topic_10=topic_10,
                           topic_11=topic_11,
                           topic_12=topic_12,
                           topic_13=topic_13,
                           topic_14=topic_14,
                           topic_21=topic_21)

@app.route('/page_3_5') #Ok
def page_3_5():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_16 = extract_topic_content(base_content, 16)
    topic_17 = extract_topic_content(base_content, 17)
    topic_18 = extract_topic_content(base_content, 18)
    topic_19 = extract_topic_content(base_content, 19)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":

            if topic_16:
                topic_16 = generate_custom_content(preference, topic_16, hobbies, work)
            if topic_17:
                topic_17 = generate_custom_content(preference, topic_17, hobbies, work)
            if topic_18:
                topic_18 = generate_custom_content(preference, topic_18, hobbies, work)
            if topic_19:
                topic_19 = generate_custom_content(preference, topic_19, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_16 = "Dados do usuário não encontrados."
        topic_17 = "Dados do usuário não encontrados."
        topic_18 = "Dados do usuário não encontrados."
        topic_19 = "Dados do usuário não encontrados."

    return render_template('page_3_5.html',
                           topic_16=topic_16,
                           topic_17=topic_17,
                           topic_18=topic_18,
                           topic_19=topic_19
                           )

@app.route('/page_3_6')#
def page_3_6():
    return render_template('page_3_6.html')
# V3 - CRIANDO COM MD

# Personal DATAS - page_1
@app.route('/', methods=['GET', 'POST'])
def index():
    form = PersonalDataForm()
    if request.method == 'POST':
        name = request.form['name'].upper()  # Converte o nome para maiúsculas
        hobbies = request.form['hobbies']
        work = request.form['work']
        learning_preference = request.form['learning_preference']
        age = request.form['age']

        # Verifica se já existe um registro com o mesmo nome (em maiúsculas) e preferência de aprendizado
        existing_person = Person.query.filter_by(name=name, learning_preference=learning_preference).first()
        if existing_person:
            # Atualiza o registro existente
            existing_person.hobbies = hobbies
            existing_person.work = work
            existing_person.age = age
            db.session.commit()
            session['person_id'] = existing_person.id
        else:
            # Cria um novo registro
            new_person = Person(
                name=name,
                hobbies=hobbies,
                work=work,
                learning_preference=learning_preference,
                age=age
            )
            db.session.add(new_person)
            db.session.commit()
            session['person_id'] = new_person.id

        session['name'] = name
        session['hobbies'] = hobbies
        session['work'] = work
        session['learning_preference'] = learning_preference
        session['age'] = age

        return redirect(url_for('page_2'))
    return render_template('page_1.html', form=form)

# TEST 1 - page_2
@app.route('/page_2', methods=['GET', 'POST'])
def page_2():
    success_message = None
    if request.method == 'POST':
        answers = {
            'AQ1': request.form['AQ1'],
            'AQ2': request.form['AQ2'],
            'AQ3': request.form['AQ3'],
            'AQ4': request.form['AQ4'],
            'AQ5': request.form['AQ5'],
            'AQ6': request.form['AQ6'],
            'AQ7': request.form['AQ7'],
            'AQ8': request.form['AQ8'],
            'AQ9': request.form['AQ9'],
            'AQ10': request.form['AQ10']
        }
        session['test_1_score'] = calculate_score(answers)

        # Determine the grade for test 1
        total_questions = 10  # total de questões
        session['grade_test_1'] = round(((10 / total_questions) * session['test_1_score']))

        person_id = session.get('person_id')
        person = db.session.get(Person, person_id)

        if person:
            person.AQ1 = answers['AQ1']
            person.AQ2 = answers['AQ2']
            person.AQ3 = answers['AQ3']
            person.AQ4 = answers['AQ4']
            person.AQ5 = answers['AQ5']
            person.AQ6 = answers['AQ6']
            person.AQ7 = answers['AQ7']
            person.AQ8 = answers['AQ8']
            person.AQ9 = answers['AQ9']
            person.AQ10 = answers['AQ10']
            person.test_1_score = session['test_1_score']
            person.grade_test_1 = session['grade_test_1']
            db.session.commit()

        success_message = "DATA SENT SUCCESSFULLY !"

    return render_template('page_2.html', AQ1=session.get('AQ1'), AQ2=session.get('AQ2'), AQ3=session.get('AQ3'), AQ4=session.get('AQ4'), AQ5=session.get('AQ5'), AQ6=session.get('AQ6'), AQ7=session.get('AQ7'), AQ8=session.get('AQ8'), AQ9=session.get('AQ9'), AQ10=session.get('AQ10'), success_message=success_message)

@app.route('/page_3')
def page_3():
    with open('index_content.txt', 'r') as f:
        content = [line.strip() for line in f]
    return render_template('page_3.html', content=content)

# TEST 2
@app.route('/page_4', methods=['GET', 'POST'])
def page_4():
    success_message = None
    if request.method == 'POST':
        answers = {
            'AQ11': request.form['AQ11'],
            'AQ12': request.form['AQ12'],
            'AQ13': request.form['AQ13'],
            'AQ14': request.form['AQ14'],
            'AQ15': request.form['AQ15'],
            'AQ16': request.form['AQ16'],
            'AQ17': request.form['AQ17'],
            'AQ18': request.form['AQ18'],
            'AQ19': request.form['AQ19'],
            'AQ20': request.form['AQ20']
            }
        session['test_2_score'] = calculate_score(answers)
        total_questions = 10
        session['grade_test_2'] = round(((10 / total_questions) * session['test_2_score']))

        person_id = session.get('person_id')
        person = db.session.get(Person, person_id)

        if person:
            person.AQ11 = answers['AQ11']
            person.AQ12 = answers['AQ12']
            person.AQ13 = answers['AQ13']
            person.AQ14 = answers['AQ14']
            person.AQ15 = answers['AQ15']
            person.AQ16 = answers['AQ16']
            person.AQ17 = answers['AQ17']
            person.AQ18 = answers['AQ18']
            person.AQ19 = answers['AQ19']
            person.AQ20 = answers['AQ20']
            person.test_2_score = session['test_2_score']
            person.grade_test_2 = session['grade_test_2']
            db.session.commit()

        success_message = "DATA SENT SUCCESSFULLY !"

    return render_template('page_4.html', AQ11=session.get('AQ11'), AQ12=session.get('AQ12'), AQ13=session.get('AQ13'), AQ14=session.get('AQ14'), AQ15=session.get('AQ15'), AQ16=session.get('AQ16'), AQ17=session.get('AQ17'), AQ18=session.get('AQ18'), AQ19=session.get('AQ19'), AQ20=session.get('AQ20'), success_message=success_message)

# Student's project
@app.route('/page_5')
def page_5():
    return render_template('page_3_6.html')

# Comparison analysis
@app.route('/page_6', methods=['GET', 'POST'])
def page_6():
    person_id = session.get('person_id')
    person = db.session.get(Person, person_id)
    if person:
        comparison_analysis = generate_comparison_analysis(person)
        if request.method == 'POST':
            feedback = request.form.get('feedback')
            person.feedback = feedback
            db.session.commit()
    else:
        comparison_analysis = "Análise não disponível."

    return render_template(
        'page_6.html',
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
        1: {'template': 'page_3_1.html', 'content': 'Content about AI'},
        2: {'template': 'page_3_2.html', 'content': 'Content about Python'},
        3: {'template': 'page_3_3.html', 'content': 'Content about python for AI'},
        4: {'template': 'page_3_4.html', 'content': 'Content about Machine Learning'},
        5: {'template': 'page_3_5.html', 'content': 'Content about Deep Learning'},
        6: {'template': 'page_3_6.html', 'content': 'Content about student"s project'},
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
