#VERSÃO 2

from flask import Flask, render_template, request, redirect, url_for, session, jsonify
from forms import PersonalDataForm
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from PIL import Image
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
# output with hmtl
        prompt = f"""
        Personalize each topic of the content{base_content} based on the person's hobbies{hobbies} and work{work}. 
        Show the topic title and then the personalized content.
        Just rewrite!
        """
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

""" PROXIMO PASSO: Fazer com que cada TOPIC seja modificado ligeiramente, caso opção 
seja Personalized Teaching, escolhido

SE NÃO, apenas mostrar o conteúdo do arquivo base_content.txt"""

# ROTAS DE PÁGINAS
#TEST DE MD
#ROTAS DE PÁGINAS
# Extract
def extract_topic_content(base_content, topic_number):
    topics = base_content.split('---TOPIC_SEPARATOR---')
    if 1 <= topic_number <= len(topics):
        return topics[topic_number - 1].strip()
    else:
        return None

# Exemplo de rota para uma página com conteúdo personalizado
# DEU CERTO, generic e person. REPLICAR PARA AS PROXIMAS PAGINAS E depois lapidar os conteudos
# ... em cada pagina

#CRIANDO NOVAS PAGINAS

@app.route('/TEST_page_3_1')
def TEST_page_3_1():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_1 = extract_topic_content(base_content, 1) #Each TOPIC SEPARATOR is ONE
    topic_1_2 = extract_topic_content(base_content, 2) # not using yet
    topic_1_3 = extract_topic_content(base_content, 3) # not using yet
    topic_1_4 = extract_topic_content(base_content, 4) # not using yet

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_1:
                topic_1 = generate_custom_content(preference, topic_1, hobbies, work)
            if topic_1_2:
                topic_1_2 = generate_custom_content(preference, topic_1_2, hobbies, work)
            if topic_1_3:
                topic_1_3 = generate_custom_content(preference, topic_1_3, hobbies, work)
            if topic_1_4:
                topic_1_4 = generate_custom_content(preference, topic_1_4, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_1 = "Dados do usuário não encontrados."
        topic_1_2 = "Dados do usuário não encontrados."
        topic_1_3 = "Dados do usuário não encontrados."
        topic_1_4 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_1.html',
                           topic_1=topic_1,
                           topic_1_2=topic_1_2,
                           topic_1_3=topic_1_3,
                           topic_1_4=topic_1_4)

@app.route('/TEST_page_3_2') #OK
def TEST_page_3_2():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_3 = extract_topic_content(base_content, 3)
    topic_2_2 = extract_topic_content(base_content, 2) # not using yet
    topic_2_3 = extract_topic_content(base_content, 1) # not using yet

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_3:
                topic_3 = generate_custom_content(preference, topic_3, hobbies, work)
            if topic_2_2:
                topic_2_2 = generate_custom_content(preference, topic_2_2, hobbies, work)
            if topic_2_3:
                topic_2_3 = generate_custom_content(preference, topic_2_3, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_3 = "Dados do usuário não encontrados."
        topic_2_2 = "Dados do usuário não encontrados."
        topic_2_3 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_2.html',
                           topic_3=topic_3,
                           topic_2_2=topic_2_2,
                           topic_2_3=topic_2_3)

@app.route('/TEST_page_3_3') #OK
def TEST_page_3_3():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_3_10 = extract_topic_content(base_content, 10)
    topic_3_11 = extract_topic_content(base_content, 11)
    topic_3_12 = extract_topic_content(base_content, 12)
    topic_3_13 = extract_topic_content(base_content, 13)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_3_10:
                topic_3_10 = generate_custom_content(preference, topic_3_10, hobbies, work)
            if topic_3_11:
                topic_3_11 = generate_custom_content(preference, topic_3_11, hobbies, work)
            if topic_3_12:
                topic_3_12 = generate_custom_content(preference, topic_3_12, hobbies, work)
            if topic_3_13:
                topic_3_13 = generate_custom_content(preference, topic_3_13, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_3_10 = "Dados do usuário não encontrados."
        topic_3_11 = "Dados do usuário não encontrados."
        topic_3_12 = "Dados do usuário não encontrados."
        topic_3_13 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_3.html',
                           topic_3_10=topic_3_10,
                           topic_3_11=topic_3_11,
                           topic_3_12=topic_3_12,
                           topic_3_13=topic_3_13)

@app.route('/TEST_page_3_4') #ok
def TEST_page_3_4():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_3_15 = extract_topic_content(base_content, 15)
    topic_3_16 = extract_topic_content(base_content, 16)
    topic_3_17 = extract_topic_content(base_content, 17)
    topic_3_18 = extract_topic_content(base_content, 18)
    topic_3_19 = extract_topic_content(base_content, 19)
    topic_3_20 = extract_topic_content(base_content, 20)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_3_15:
                topic_3_15 = generate_custom_content(preference, topic_3_15, hobbies, work)
            if topic_3_16:
                topic_3_16 = generate_custom_content(preference, topic_3_16, hobbies, work)
            if topic_3_17:
                topic_3_17 = generate_custom_content(preference, topic_3_17, hobbies, work)
            if topic_3_18:
                topic_3_18 = generate_custom_content(preference, topic_3_18, hobbies, work)
            if topic_3_19:
                topic_3_19 = generate_custom_content(preference, topic_3_19, hobbies, work)
            if topic_3_20:
                topic_3_20 = generate_custom_content(preference, topic_3_20, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_3_15 = "Dados do usuário não encontrados."
        topic_3_16 = "Dados do usuário não encontrados."
        topic_3_17 = "Dados do usuário não encontrados."
        topic_3_18 = "Dados do usuário não encontrados."
        topic_3_19 = "Dados do usuário não encontrados."
        topic_3_20 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_4.html',
                           topic_3_15=topic_3_15,
                           topic_3_16=topic_3_16,
                           topic_3_17=topic_3_17,
                           topic_3_18=topic_3_18,
                           topic_3_19=topic_3_19,
                           topic_3_20=topic_3_20)

@app.route('/TEST_page_3_5') #ok
def TEST_page_3_5():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_1_20 = extract_topic_content(base_content, 20)
    topic_1_21 = extract_topic_content(base_content, 21)
    topic_1_22 = extract_topic_content(base_content, 22)
    topic_1_23 = extract_topic_content(base_content, 23)
    topic_1_24 = extract_topic_content(base_content, 24)
    topic_1_25 = extract_topic_content(base_content, 25)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_1_20:
                topic_1_20 = generate_custom_content(preference, topic_1_20, hobbies, work)
            if topic_1_21:
                topic_1_21 = generate_custom_content(preference, topic_1_21, hobbies, work)
            if topic_1_22:
                topic_1_22 = generate_custom_content(preference, topic_1_22, hobbies, work)
            if topic_1_23:
                topic_1_23 = generate_custom_content(preference, topic_1_23, hobbies, work)
            if topic_1_24:
                topic_1_24 = generate_custom_content(preference, topic_1_24, hobbies, work)
            if topic_1_25:
                topic_1_25 = generate_custom_content(preference, topic_1_25, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_1_20 = "Dados do usuário não encontrados."
        topic_1_21 = "Dados do usuário não encontrados."
        topic_1_22 = "Dados do usuário não encontrados."
        topic_1_23 = "Dados do usuário não encontrados."
        topic_1_24 = "Dados do usuário não encontrados."
        topic_1_25 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_5.html',
                           topic_1_20=topic_1_20,
                           topic_1_21=topic_1_21,
                           topic_1_22=topic_1_22,
                           topic_1_23=topic_1_23,
                           topic_1_24=topic_1_24,
                           topic_1_25=topic_1_25)

@app.route('/TEST_page_3_6') #ok
def TEST_page_3_6():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_1_25 = extract_topic_content(base_content, 25)
    topic_1_26 = extract_topic_content(base_content, 26)
    topic_1_27 = extract_topic_content(base_content, 27)
    topic_1_28 = extract_topic_content(base_content, 28)
    topic_1_29 = extract_topic_content(base_content, 29)
    topic_1_30 = extract_topic_content(base_content, 30)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_1_25:
                topic_1_25 = generate_custom_content(preference, topic_1_25, hobbies, work)
            if topic_1_26:
                topic_1_26 = generate_custom_content(preference, topic_1_26, hobbies, work)
            if topic_1_27:
                topic_1_27 = generate_custom_content(preference, topic_1_27, hobbies, work)
            if topic_1_28:
                topic_1_28 = generate_custom_content(preference, topic_1_28, hobbies, work)
            if topic_1_29:
                topic_1_29 = generate_custom_content(preference, topic_1_29, hobbies, work)
            if topic_1_30:
                topic_1_30 = generate_custom_content(preference, topic_1_30, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_1_25 = "Dados do usuário não encontrados."
        topic_1_26 = "Dados do usuário não encontrados."
        topic_1_27 = "Dados do usuário não encontrados."
        topic_1_28 = "Dados do usuário não encontrados."
        topic_1_29 = "Dados do usuário não encontrados."
        topic_1_30 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_6.html',
                           topic_1_25=topic_1_25,
                           topic_1_26=topic_1_26,
                           topic_1_27=topic_1_27,
                           topic_1_28=topic_1_28,
                           topic_1_29=topic_1_29,
                           topic_1_30=topic_1_30)

@app.route('/TEST_page_3_7') #ok
def TEST_page_3_7():
    with open('base_content.txt', 'r', encoding='utf-8') as f:
        base_content = f.read()

    person_id = session.get('person_id')  # Obtém o ID da pessoa da sessão
    person = db.session.get(Person, person_id)  # Obtém a pessoa do banco de dados

    topic_1_35 = extract_topic_content(base_content, 35)
    topic_1_36 = extract_topic_content(base_content, 36)
    topic_1_37 = extract_topic_content(base_content, 37)
    topic_1_38 = extract_topic_content(base_content, 38)
    topic_1_39 = extract_topic_content(base_content, 39)
    topic_1_40 = extract_topic_content(base_content, 40)

    if person:
        preference = person.learning_preference
        hobbies = person.hobbies
        work = person.work

        if preference == "Personalized Teaching":
            if topic_1_35:
                topic_1_35 = generate_custom_content(preference, topic_1_35, hobbies, work)
            if topic_1_36:
                topic_1_36 = generate_custom_content(preference, topic_1_36, hobbies, work)
            if topic_1_37:
                topic_1_37 = generate_custom_content(preference, topic_1_37, hobbies, work)
            if topic_1_38:
                topic_1_38 = generate_custom_content(preference, topic_1_38, hobbies, work)
            if topic_1_39:
                topic_1_39 = generate_custom_content(preference, topic_1_39, hobbies, work)
            if topic_1_40:
                topic_1_40 = generate_custom_content(preference, topic_1_40, hobbies, work)
        else:
            # Se for Generic Teaching, usa o conteúdo extraído diretamente
            pass  # Não precisa fazer nada, pois já extraímos o conteúdo

    else:
        topic_1_35 = "Dados do usuário não encontrados."
        topic_1_36 = "Dados do usuário não encontrados."
        topic_1_37 = "Dados do usuário não encontrados."
        topic_1_38 = "Dados do usuário não encontrados."
        topic_1_39 = "Dados do usuário não encontrados."
        topic_1_40 = "Dados do usuário não encontrados."

    return render_template('TEST_page_3_7.html',
                           topic_1_35=topic_1_35,
                           topic_1_36=topic_1_36,
                           topic_1_37=topic_1_37,
                           topic_1_38=topic_1_38,
                           topic_1_39=topic_1_39,
                           topic_1_40=topic_1_40)

#CRIANDO NOVAS PAGINAS

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

        # Determine the grade for test 1
        total_questions = 2  # total de questões
        session['grade_test_1'] = round(((10 / total_questions) * session['test_1_score']))

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

        topic_content = extract_topic_content(base_content, 5)# N 5 indica a posição do titulo desde inicio

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
        # replace lines 589 to 596
        total_questions = 2  # total de questões
        session['grade_test_2'] = round(((10 / total_questions) * session['test_2_score']))

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