<link rel="stylesheet" type="text/css" href="{{ url_for('static', filename='style.css') }}">

# <center> **Basic Concepts of Artificial Intelligence** </center>

---

### <center> How to create a IA model?</center>

---

## Basic Concepts for AI Creation

Now you will see some necessary concepts to create a IA model. Below have a little bit more words than usual, but will be the last page, so get your last breath and let's go! 
To embark on the journey of creating Artificial Intelligence (AI), a foundational understanding of several key concepts is essential. Here's a structured overview:

### I. Core Machine Learning Terminology

1. **Dataset:** The bedrock of machine learning, a collection of **samples** (individual data points or instances) each described by a set of **attributes** (features). The quality and relevance of the dataset are paramount to the performance of any AI model.

2. **Supervised Learning:** A learning paradigm where the AI model learns a mapping function from input attributes to known output values (the **labels**). This requires a dataset where each sample is paired with its corresponding correct output.

3. **Unsupervised Learning:** In contrast to supervised learning, this paradigm involves training models on unlabeled data to discover hidden patterns, structures, or relationships within the data itself.

4. **Reinforcement Learning:** An approach where an agent learns optimal behavior by interacting with an environment, receiving rewards or penalties for its actions. The goal is to maximize cumulative reward over time.

5. **Algorithm:** The specific method or set of rules that a machine learning model uses to learn from data and make predictions or decisions. Different types of problems call for different algorithms.

6. **Model:** The learned representation or function derived from the training process. It embodies the patterns and relationships discovered in the data and is used to make predictions on new, unseen data.

7. **Training:** The iterative process of exposing the model to the training dataset and adjusting its internal parameters to minimize the difference between its predictions and the actual labels (in supervised learning) or to optimize for a specific objective (in unsupervised and reinforcement learning). This process often involves a **loss function** that quantifies the error of the model.

8. **Evaluation:** Assessing the performance of a trained model on a separate **test dataset** (data not used during training) to gauge its ability to generalize to new, unseen data. Various **metrics** are used to quantify performance, depending on the task (e.g., accuracy, precision, recall for classification; mean squared error for regression).

9. **Feature Engineering:** A crucial step involving the selection, transformation, and creation of informative features from the raw data. Well-engineered features can significantly improve the performance and interpretability of a model.

10. **Overfitting:** A common pitfall where a model learns the training data too well, capturing noise and specific details that do not generalize to new data, resulting in poor performance on unseen data.

11. **Library (e.g., Scikit-learn):** A collection of pre-built tools, functions, and modules that provide efficient implementations of machine learning algorithms, data preprocessing techniques, and model evaluation utilities. Python libraries like Scikit-learn (sklearn) are fundamental for practical AI development.

![](C:\Users\Lucas\PycharmProjects\website_personalized\static\images\J.png)

### II. Deep Dive into Classification

**Objective:** The core goal of a classification task is to build a model that can accurately assign data points to one of several predefined, discrete categories or **classes**.

1.  **Mapping Inputs to Classes:** A classification algorithm learns a function that takes a set of input **features** describing a data sample and outputs the predicted class label for that sample.

2.  **Discrete Target Variable:** The variable we aim to predict is categorical, belonging to a finite and distinct set of possible values. Examples include:
    * Binary Classification: "Yes" or "No", "Spam" or "Not Spam".
    * Multiclass Classification: "Cat", "Dog", "Bird"; "Low", "Medium", "High" risk.

**Common Classification Algorithms (Implemented in Scikit-learn):**

* **Logistic Regression:** Although named "regression," it's a linear model for binary classification, estimating the probability of a sample belonging to a particular class using the sigmoid function. It can be extended for multiclass problems.
    * *Key Terms:* Sigmoid function, Probability, Decision boundary.

* **Support Vector Machines (SVM):** A powerful algorithm that seeks to find the optimal hyperplane that best separates different classes in the feature space, maximizing the **margin** between them. **Kernels** can be used to handle non-linearly separable data.
    * *Key Terms:* Hyperplane, Support vectors, Margin, Kernel.

* **Decision Trees:** Tree-like structures where each internal node tests a feature, each branch represents the outcome of the test, and each leaf node holds a class prediction.
    * *Key Terms:* Root node, Internal node, Leaf node, Split, Impurity (Gini, Entropy).

* **Random Forest:** An **ensemble learning** technique that builds multiple decision trees and aggregates their predictions (often through majority voting) to improve robustness and accuracy. **Bagging** is a key concept here.
    * *Key Terms:* Ensemble learning, Bagging, Decision trees.

* **K-Nearest Neighbors (KNN):** A non-parametric, instance-based learning algorithm that classifies a new data point based on the majority class among its *k* closest neighbors in the feature space, as determined by a **distance metric**.
    * *Key Terms:* Distance (Euclidean, Manhattan, etc.), Number of neighbors (*k*).

* **Naive Bayes:** A probabilistic algorithm based on **Bayes' theorem**, assuming conditional independence of features given the class. It's efficient and often used in text classification.
    * *Key Terms:* Bayes' theorem, Prior probability, Conditional probability.

**The Classification Workflow:**

1.  **Data Acquisition and Preprocessing:** Gathering relevant, labeled data and preparing it for modeling through cleaning, handling missing values, scaling features, and other necessary transformations.

2.  **Data Splitting:** Dividing the dataset into a **training set** (used to train the model) and a **test set** (used to evaluate its generalization ability). Common splits include 70/30 or 80/20.

3.  **Model Selection:** Choosing an appropriate classification algorithm based on the characteristics of the data, the problem requirements (e.g., interpretability, speed), and prior knowledge or experimentation.

4.  **Model Training:** Feeding the training data to the selected algorithm, allowing it to learn the underlying patterns and relationships between the features and the class labels.

5.  **Model Evaluation:** Assessing the trained model's performance on the unseen test data using relevant **evaluation metrics**.

6.  **Hyperparameter Tuning:** Optimizing the settings of the chosen algorithm (hyperparameters, which are not learned from the data) to further improve the model's performance. Techniques like **GridSearchCV** and **RandomizedSearchCV** are often employed.

7.  **Deployment:** Making the trained and evaluated model available for use in real-world applications to classify new, incoming data.

**Key Evaluation Metrics for Classification:**

These metrics provide quantitative measures of a classification model's effectiveness:

* **Accuracy:** The overall proportion of correctly classified instances.

* **Precision:** Out of all the instances predicted as positive, what proportion was actually positive? (True Positives / (True Positives + False Positives)).

* **Recall (Sensitivity or True Positive Rate - TPR):** Out of all the actual positive instances, what proportion was correctly identified as positive? (True Positives / (True Positives + False Negatives)).

* **F1-Score:** The harmonic mean of precision and recall, providing a balanced measure, especially useful when dealing with imbalanced datasets.

* **Confusion Matrix:** A table that visualizes the performance of a classifier by showing the counts of true positives, true negatives, false positives, and false negatives.

* **ROC (Receiver Operating Characteristic) Curve & AUC (Area Under the Curve):** For binary classifiers, the ROC curve plots the True Positive Rate against the False Positive Rate at various threshold settings, and the AUC summarizes the overall performance of the classifier across all possible thresholds.

This enhanced organization aims to provide a clearer and more structured understanding of the fundamental concepts for AI creation, with a specific focus on classification. Let me know if you'd like to delve deeper into any of these areas!

![](C:\Users\Lucas\PycharmProjects\website_personalized\static\images\K.png)

<form action="{{ url_for('page_4') }}" method="get">
    <center> <button type="submit" class="botao-azul">Go to TEST TWO</button> </center>
</form>
<div>
    <a href="/page_3_6" class="botao-azul">BACK</a><br><br>
</div>

<script>
    // Código JavaScript para os hexágonos interativos aqui
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');

    canvas.width = window.innerWidth;
    canvas.height = window.innerHeight;

    const hexagons = [];
    const numHexagons = 15;
    const hexagonRadius = 15;

    class Hexagon {
    constructor(x, y) {
        this.x = x;
        this.y = y;
        this.vx = (Math.random() * 2 - 1) * 0.5; // Velocidade reduzida
        this.vy = (Math.random() * 2 - 1) * 0.5; // Velocidade reduzida
    }

    draw() {
        ctx.beginPath();
        for (let i = 0; i < 6; i++) {
            const angle = 2 * Math.PI / 6 * i;
            const x = this.x + hexagonRadius * Math.cos(angle);
            const y = this.y + hexagonRadius * Math.sin(angle);
            ctx.lineTo(x, y);
        }
        ctx.closePath();
        ctx.strokeStyle = 'white';
        ctx.stroke();
    }

    update() {
        this.x += this.vx;
        this.y += this.vy;

        if (this.x < 0 || this.x > canvas.width) {
            this.vx *= -1;
        }

        if (this.y < 0 || this.y > canvas.height) {
            this.vy *= -1;
        }

        // Adicionando amortecimento
        this.vx *= 0.98;
        this.vy *= 0.98;
    }
    }

    for (let i = 0; i < numHexagons; i++) {
    const x = Math.random() * canvas.width;
    const y = Math.random() * canvas.height;
    hexagons.push(new Hexagon(x, y));
    }

    function animate() {
    ctx.clearRect(0, 0, canvas.width, canvas.height);

    for (let i = 0; i < hexagons.length; i++) {
        hexagons[i].update();
        hexagons[i].draw();

        for (let j = i + 1; j < hexagons.length; j++) {
            const dx = hexagons[i].x - hexagons[j].x;
            const dy = hexagons[i].y - hexagons[j].y;
            const distance = Math.sqrt(dx * dx + dy * dy);

            if (distance < 200) {
                ctx.beginPath();
                ctx.moveTo(hexagons[i].x, hexagons[i].y);
                ctx.lineTo(hexagons[j].x, hexagons[j].y);
                ctx.strokeStyle = 'rgba(255, 255, 255, 0.5)';
                ctx.stroke();
            }
        }
    }

    requestAnimationFrame(animate);
    }

    animate();

    canvas.addEventListener('mousemove', (event) => {
    for (let i = 0; i < hexagons.length; i++) {
        const dx = event.clientX - hexagons[i].x;
        const dy = event.clientY - hexagons[i].y;
        const distance = Math.sqrt(dx * dx + dy * dy);

        if (distance < 100) {
            hexagons[i].vx += dx * 0.005; // Força reduzida
            hexagons[i].vy += dy * 0.005; // Força reduzida
        }
    }
    });
</script>

<script>
    (function() {
        const loadingOverlay = document.getElementById('loading-overlay');

        // Função para mostrar o overlay
        function showLoader() {
            if (loadingOverlay) {
                loadingOverlay.style.display = 'flex'; // Primeiro torna o elemento 'flex'
                // Força um reflow para garantir que display:flex seja aplicado antes da opacidade
                void loadingOverlay.offsetWidth;
                loadingOverlay.classList.add('visible'); // Adiciona a classe para iniciar a transição de opacidade
            }
        }

        // --- Gatilhos para mostrar o loader ---

        // 1. Para links normais que navegam para outra página
        document.querySelectorAll('a[href]').forEach(link => {
            // Ignora links internos da página (#) e links que abrem em nova aba
            if (link.getAttribute('href') &&
                !link.getAttribute('href').startsWith('#') &&
                (!link.target || link.target.toLowerCase() === '_self'))
            {
                link.addEventListener('click', function(event) {
                    // Verifica se não é um link especial (ex: mailto, tel)
                    const protocol = link.protocol;
                    if (protocol === 'http:' || protocol === 'https:') {
                        showLoader();
                        // Não prevenimos o default, o navegador navegará normalmente
                    }
                });
            }
        });

        // 2. Para submissões de formulário que causam navegação
        document.querySelectorAll('form').forEach(form => {
            form.addEventListener('submit', function(event) {
                // Verifica se o formulário NÃO está sendo tratado por AJAX específico
                // (No seu page_1.html, o submit principal é AJAX, então este listener não deve ativá-lo)
                // Este listener pegará os submits dos botões "Go to Next page" em page_2 e page_4, por exemplo.
                const isAjaxForm = form.querySelector('button[onclick^="submitForm"]'); // Verifica se é o form AJAX de page_1

                if (!isAjaxForm) {
                     // Pequeno delay para garantir que o loader apareça antes da navegação iniciar
                     // Útil para transições rápidas.
                     setTimeout(showLoader, 10); // Mostra após 10ms
                }
            });
        });

        // --- Lógica para esconder o loader ---

        // Esconde o loader se o usuário voltar usando o botão do navegador
        // O evento 'pageshow' é disparado quando a página é exibida, incluindo via bfcache
        window.addEventListener('pageshow', function(event) {
            // event.persisted é true se a página foi carregada do back/forward cache
            // Se veio do cache, significa que o usuário voltou, então escondemos o loader.
            if (loadingOverlay && loadingOverlay.classList.contains('visible')) {
                 loadingOverlay.classList.remove('visible');
                 // Espera a transição de opacidade terminar antes de setar display: none
                 setTimeout(() => {
                     // Verifica novamente caso algo tenha mudado rapidamente
                     if (!loadingOverlay.classList.contains('visible')) {
                        loadingOverlay.style.display = 'none';
                     }
                 }, 300); // Tempo igual à duração da transição CSS (0.3s)
            }
        });

        // Caso especial para o formulário AJAX em page_1.html
        // (Se você estiver em page_1.html, este código será relevante)
        if (typeof submitForm === 'function') {
            const originalSubmitForm = submitForm; // Guarda a função original
            window.submitForm = function() { // Sobrescreve a função global
                showLoader(); // Mostra o loader ANTES de iniciar o fetch

                const form = document.querySelector('form[action="{{ url_for('index') }}"]');
                const formData = new FormData(form);

                fetch(form.action, {
                    method: 'POST',
                    body: formData
                }).then(response => {
                    if (response.ok) {
                        // Navega para a próxima página APÓS o sucesso do POST
                        // O loader continuará visível até a page_2 carregar
                        window.location.href = "{{ url_for('page_2') }}";
                        // Não escondemos o loader aqui, pois a navegação vai acontecer
                    } else {
                        // Se der erro no POST, esconde o loader e mostra alerta
                        alert('Error sending data. Please try again.');
                        if (loadingOverlay) {
                            loadingOverlay.classList.remove('visible');
                            setTimeout(() => {
                                 if (!loadingOverlay.classList.contains('visible')) {
                                    loadingOverlay.style.display = 'none';
                                 }
                            }, 300);
                        }
                    }
                }).catch(error => {
                    // Se der erro na rede/fetch, esconde o loader e mostra alerta
                    console.error('Error:', error);
                    alert('Error sending data. Please try again.');
                    if (loadingOverlay) {
                        loadingOverlay.classList.remove('visible');
                        setTimeout(() => {
                             if (!loadingOverlay.classList.contains('visible')) {
                                loadingOverlay.style.display = 'none';
                             }
                        }, 300);
                    }
                });
            }
        }

    })();
</script>