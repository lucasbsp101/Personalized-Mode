# <center>Basic Concepts of Artificial Intelligence

## <center> *Application Example*

---

<form method="POST" action="{{ url_for('page_5') }}"></form>

## <center> Sentiment Analysis </center>

#### Here we have an example of a sentiment analysis application. 
> ### What it is this application?
> 
> Sentiment analysis is a natural language processing (NLP) technique that aims to determine the emotional polarity of a text. In other words, it seeks to identify whether a text expresses a positive, negative, or neutral opinion.

> ### __How does it work?__
>
>> ### __Text Preprocessing:__
>>
>>+ The input text is cleaned and prepared for analysis. This may include removing punctuation, special characters, and irrelevant words (stop words).
>>+ The text is divided into smaller units, such as words or phrases.
>
>> ### __Feature Extraction:__
>>
>> The sentiment analysis model extracts relevant features from the text, such as keywords, phrases, and linguistic patterns.
>> These features are used to represent the text numerically, allowing the model to process them.
>
>> ### __Classification:__
>>
>>The sentiment analysis model uses machine learning algorithms to classify the text into one of the sentiment categories (positive, negative, or neutral).
>>The model was trained on a dataset of texts labeled with their respective sentiments, allowing it to learn to associate text features with different emotional polarities.
>>In the case of phi-4, it performs sentiment analysis based on the data it was trained on, using a technique called "zero-shot learning," where the model can perform sentiment analysis without specific training for this task.

>> ### __Confidence Score:__
>>
>>In addition to sentiment classification, the model usually provides a confidence score, indicating the probability of the text belonging to each sentiment category.
>>

>> ### __Applications:__
>>
>>Sentiment analysis has various applications, including:
>>
>>+ Social media monitoring: To understand public opinion about brands, products, or events.
>>+ Customer review analysis: To identify strengths and weaknesses of products or services.
>>+ Hate speech detection: To identify and remove offensive or harmful content.
>>+ Market research: To understand consumer trends and preferences.

## Text Examples:

#### Positive Sentiment:
+ "I loved the movie! The performances were amazing and the story kept me hooked from start to finish."
+ "I received the product today and am extremely satisfied with the quality. I recommend it to everyone!"
+ "What a wonderful day! The sun is shining and I feel very happy."
#### Negative Sentiment:
+ "The service was horrible. I waited for hours and no one helped me. Never going back!"
+ "I am very disappointed with the product. It arrived broken and doesn't work."
+ "What a terrible day! Everything went wrong and I am very frustrated."
#### Neutral Sentiment:
+ "The weather is cloudy today. It might rain later."
+ "I bought a new book at the bookstore. The story seems interesting."
+ "I am going to work. The traffic is a bit congested."
#### Mixed Sentiment:
+ "The movie was good, but the ending left me a bit confused."
+ "The product is great, but the price is too high."
+ "I am happy to have gotten the job, but the salary is not ideal."
#### Sarcastic Sentiment:
+ "What a beautiful day to be stuck in traffic for hours. Love it!"
+ "Wow, what amazing service! I only waited an eternity to be attended."
+ "I love it when the food comes cold. It's so tasty!"

<center> <textarea id="text" rows="4" cols="50"></textarea><br> </center><br>
<center> <button onclick="analyzeSentiment()">Analyze</button><br> </center><br>
<div id="result"></div>





<script>
    function analyzeSentiment() {
        const text = document.getElementById('text').value;
        const resultElement = document.getElementById('result');

        // Mostrar a mensagem de "analisando sentimento"
        resultElement.innerHTML = 'Analisando sentimento, por favor aguarde...';

        fetch('/analyze_sentiment', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({ text: text })
        })
        .then(response => response.json())
        .then(data => {
            // Ocultar a mensagem de "analisando sentimento" e exibir o resultado
            if (data.error) {
                resultElement.innerHTML = `Error: ${data.error}`;
            } else {
                if (data.sentiment && data.confidence) {
                    resultElement.innerHTML = `Sentiment: ${data.sentiment}, Confidence: ${data.confidence}`;
                } else {
                    resultElement.innerHTML = `Error: Sentiment or confidence data missing.`;
                }
            }
        })
        .catch(error => {
            resultElement.innerHTML = `Error: ${error}`;
        });
    }
</script>

## Below is the HTML code for the page and the JavaScript function to analyze sentiment

```html
    <html><head><meta charset="utf-8" /><link rel="stylesheet" type="text/css" href="https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor/dist/index.css"/><script src="https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor/dist/js/i18n/en_US.js"></script><script src="https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor/dist/method.min.js"></script></head><body style="width: 1075px;"><div class="vditor-reset" id="preview"><h1 id="Basic-Concepts-of-Artificial-Intelligence"><center>Basic Concepts of Artificial Intelligence<a id="vditorAnchor-Basic-Concepts-of-Artificial-Intelligence" class="vditor-anchor" href="#Basic-Concepts-of-Artificial-Intelligence"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h1>
    <h2 id="-Application-Example"><center> <em>Application Example</em><a id="vditorAnchor--Application-Example" class="vditor-anchor" href="#-Application-Example"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h2>
    <hr />
    <form method="POST" action="{{ url_for('page_5') }}"></form>
    <h2 id="-Sentiment-Analysis-"><center> Sentiment Analysis </center><a id="vditorAnchor--Sentiment-Analysis-" class="vditor-anchor" href="#-Sentiment-Analysis-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h2>
    <h4 id="Here-we-have-an-example-of-a-sentiment-analysis-application-">Here we have an example of a sentiment analysis application.<a id="vditorAnchor-Here-we-have-an-example-of-a-sentiment-analysis-application-" class="vditor-anchor" href="#Here-we-have-an-example-of-a-sentiment-analysis-application-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h4>
    <blockquote>
    <h3 id="What-it-is-this-application-">What it is this application?<a id="vditorAnchor-What-it-is-this-application-" class="vditor-anchor" href="#What-it-is-this-application-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <p>Sentiment analysis is a natural language processing (NLP) technique that aims to determine the emotional polarity of a text. In other words, it seeks to identify whether a text expresses a positive, negative, or neutral opinion.</p>
    </blockquote>
    <blockquote>
    <h3 id="How-does-it-work-"><strong>How does it work?</strong><a id="vditorAnchor-How-does-it-work-" class="vditor-anchor" href="#How-does-it-work-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <blockquote>
    <h3 id="Text-Preprocessing-"><strong>Text Preprocessing:</strong><a id="vditorAnchor-Text-Preprocessing-" class="vditor-anchor" href="#Text-Preprocessing-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <ul>
    <li>The input text is cleaned and prepared for analysis. This may include removing punctuation, special characters, and irrelevant words (stop words).</li>
    <li>The text is divided into smaller units, such as words or phrases.</li>
    </ul>
    </blockquote>
    <blockquote>
    <h3 id="Feature-Extraction-"><strong>Feature Extraction:</strong><a id="vditorAnchor-Feature-Extraction-" class="vditor-anchor" href="#Feature-Extraction-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <p>The sentiment analysis model extracts relevant features from the text, such as keywords, phrases, and linguistic patterns.<br />
    These features are used to represent the text numerically, allowing the model to process them.</p>
    </blockquote>
    <blockquote>
    <h3 id="Classification-"><strong>Classification:</strong><a id="vditorAnchor-Classification-" class="vditor-anchor" href="#Classification-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <p>The sentiment analysis model uses machine learning algorithms to classify the text into one of the sentiment categories (positive, negative, or neutral).<br />
    The model was trained on a dataset of texts labeled with their respective sentiments, allowing it to learn to associate text features with different emotional polarities.<br />
    In the case of phi-4, it performs sentiment analysis based on the data it was trained on, using a technique called &quot;zero-shot learning,&quot; where the model can perform sentiment analysis without specific training for this task.</p>
    </blockquote>
    </blockquote>
    <blockquote>
    <blockquote>
    <h3 id="Confidence-Score-"><strong>Confidence Score:</strong><a id="vditorAnchor-Confidence-Score-" class="vditor-anchor" href="#Confidence-Score-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <p>In addition to sentiment classification, the model usually provides a confidence score, indicating the probability of the text belonging to each sentiment category.</p>
    </blockquote>
    </blockquote>
    <blockquote>
    <blockquote>
    <h3 id="Applications-"><strong>Applications:</strong><a id="vditorAnchor-Applications-" class="vditor-anchor" href="#Applications-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h3>
    <p>Sentiment analysis has various applications, including:</p>
    <ul>
    <li>Social media monitoring: To understand public opinion about brands, products, or events.</li>
    <li>Customer review analysis: To identify strengths and weaknesses of products or services.</li>
    <li>Hate speech detection: To identify and remove offensive or harmful content.</li>
    <li>Market research: To understand consumer trends and preferences.</li>
    </ul>
    </blockquote>
    </blockquote>
    <h2 id="Text-Examples-">Text Examples:<a id="vditorAnchor-Text-Examples-" class="vditor-anchor" href="#Text-Examples-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h2>
    <h4 id="Positive-Sentiment-">Positive Sentiment:<a id="vditorAnchor-Positive-Sentiment-" class="vditor-anchor" href="#Positive-Sentiment-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h4>
    <ul>
    <li>&quot;I loved the movie! The performances were amazing and the story kept me hooked from start to finish.&quot;</li>
    <li>&quot;I received the product today and am extremely satisfied with the quality. I recommend it to everyone!&quot;</li>
    <li>&quot;What a wonderful day! The sun is shining and I feel very happy.&quot;</li>
    </ul>
    <h4 id="Negative-Sentiment-">Negative Sentiment:<a id="vditorAnchor-Negative-Sentiment-" class="vditor-anchor" href="#Negative-Sentiment-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h4>
    <ul>
    <li>&quot;The service was horrible. I waited for hours and no one helped me. Never going back!&quot;</li>
    <li>&quot;I am very disappointed with the product. It arrived broken and doesn't work.&quot;</li>
    <li>&quot;What a terrible day! Everything went wrong and I am very frustrated.&quot;</li>
    </ul>
    <h4 id="Neutral-Sentiment-">Neutral Sentiment:<a id="vditorAnchor-Neutral-Sentiment-" class="vditor-anchor" href="#Neutral-Sentiment-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h4>
    <ul>
    <li>&quot;The weather is cloudy today. It might rain later.&quot;</li>
    <li>&quot;I bought a new book at the bookstore. The story seems interesting.&quot;</li>
    <li>&quot;I am going to work. The traffic is a bit congested.&quot;</li>
    </ul>
    <h4 id="Mixed-Sentiment-">Mixed Sentiment:<a id="vditorAnchor-Mixed-Sentiment-" class="vditor-anchor" href="#Mixed-Sentiment-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h4>
    <ul>
    <li>&quot;The movie was good, but the ending left me a bit confused.&quot;</li>
    <li>&quot;The product is great, but the price is too high.&quot;</li>
    <li>&quot;I am happy to have gotten the job, but the salary is not ideal.&quot;</li>
    </ul>
    <h4 id="Sarcastic-Sentiment-">Sarcastic Sentiment:<a id="vditorAnchor-Sarcastic-Sentiment-" class="vditor-anchor" href="#Sarcastic-Sentiment-"><svg viewBox="0 0 16 16" version="1.1" width="16" height="16"><path fill-rule="evenodd" d="M4 9h1v1H4c-1.5 0-3-1.69-3-3.5S2.55 3 4 3h4c1.45 0 3 1.69 3 3.5 0 1.41-.91 2.72-2 3.25V8.59c.58-.45 1-1.27 1-2.09C10 5.22 8.98 4 8 4H4c-.98 0-2 1.22-2 2.5S3 9 4 9zm9-3h-1v1h1c1 0 2 1.22 2 2.5S13.98 12 13 12H9c-.98 0-2-1.22-2-2.5 0-.83.42-1.64 1-2.09V6.25c-1.09.53-2 1.84-2 3.25C6 11.31 7.55 13 9 13h4c1.45 0 3-1.69 3-3.5S14.5 6 13 6z"></path></svg></a></h4>
    <ul>
    <li>&quot;What a beautiful day to be stuck in traffic for hours. Love it!&quot;</li>
    <li>&quot;Wow, what amazing service! I only waited an eternity to be attended.&quot;</li>
    <li>&quot;I love it when the food comes cold. It's so tasty!&quot;</li>
    </ul>
    <center> <textarea id="text" rows="4" cols="50"></textarea><br> </center><br>
    <center> <button onclick="analyzeSentiment()">Analyze</button><br> </center><br>
    <div id="result"></div>
    <form action="{{ url_for('page_6') }}" method="get">
        <center> <button type="submit">Go to Next page</button> </center>
    </form>
    <div>
        <a href="/page_6">BACK</a><br><br>
    </div>
    <script>
        function analyzeSentiment() {
            const text = document.getElementById('text').value;
            const resultElement = document.getElementById('result');
    
            // Mostrar a mensagem de "Analyzing sentiment"
            resultElement.innerHTML = 'Analyzing sentiment, please wait...';
    
            fetch('/analyze_sentiment', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json'
                },
                body: JSON.stringify({ text: text })
            })
            .then(response => response.json())
            .then(data => {
                // Ocultar a mensagem de "Analyzing sentiment" e exibir o resultado
                if (data.error) {
                    resultElement.innerHTML = `Error: ${data.error}`;
                } else {
                    if (data.sentiment && data.confidence) {
                        resultElement.innerHTML = `Sentiment: ${data.sentiment}, Confidence: ${data.confidence}`;
                    } else {
                        resultElement.innerHTML = `Error: Sentiment or confidence data missing.`;
                    }
                }
            })
            .catch(error => {
                resultElement.innerHTML = `Error: ${error}`;
            });
        }
    </script>
    </div><script>    const previewElement = document.getElementById('preview');    Vditor.setContentTheme('idea-light', 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor/dist/css/content-theme');    Vditor.codeRender(previewElement);    Vditor.highlightRender({"enable":true,"lineNumber":false,"style":"dracula"}, previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor');    Vditor.mathRender(previewElement, { cdn: 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor',math: {"engine":"KaTeX","inlineDigit":true,"macros":{}}});    Vditor.mermaidRender(previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor', 'light');    Vditor.flowchartRender(previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor');    Vditor.graphvizRender(previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor');    Vditor.chartRender(previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor', 'light');    Vditor.mindmapRender(previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor', 'light');    Vditor.abcRender(previewElement, 'https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor');    Vditor.mediaRender(previewElement);    Vditor.speechRender(previewElement); </script>  <script src="https://cdn.jsdelivr.net/gh/shuzijun/markdown-editor@2.0.5/src/main/resources/vditor/dist/js/icons/ant.js"></script></body></html>

```
    
## Below is the code for the sentiment analysis application using Flask and Azure OpenAI.

```PYTHON
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
```


<form action="{{ url_for('page_5') }}" method="get">
    <center> <button type="submit">Go to Next page</button> </center>
</form>


<div>
    <a href="/page_6">BACK</a><br><br>
</div>