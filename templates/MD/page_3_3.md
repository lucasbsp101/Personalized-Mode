# <center>Basic Concepts of Artificial Intelligence

### <center>Why python for AI??

1. 
    >*{{ topic_5|safe }}*

2. 
    >*{{ topic_6|safe }}*
   

3.
    >*{{ topic_7|safe }}*
    

---
>> ## <center> *Rich Ecosystem* </center>
>
> + Offers extensive libraries and frameworks (e.g., TensorFlow, PyTorch, Scikit-learn) tailored for AI and machine learning.
>
> + **Strong Community Support**: A large, active community of AI enthusiasts, researchers, and developers sharing knowledge and resources. 
>
> + **Collaborative Environment**: Ensures accessibility to help, tutorials, and insights for continuous learning.

---
## <center> Code example Python Plus IA </center>
```python
from transformers import pipeline

# Cria um classificador de sentimento
classificador = pipeline("sentiment-analysis")

# Texto de exemplo
texto = "Eu adorei o filme! Foi incrível."

# Analisa o sentimento do texto
resultado = classificador(texto)[0]

# Exibe o resultado
print(f"Sentimento: {resultado['label']}")
print(f"Confiança: {resultado['score']:.4f}")
```

---

>**An advantage for using Python is that it comes with some very suitable libraries:**
>> + NumPy (Library for working with Arrays)
>> + SciPy (Library for Statistical Science)
>> + Matplotlib (Graph Plotting Library)
>> + NLTK (Natural Language Toolkit)
>> + TensorFlow (Machine Learning)


---

<center> <img class="fade-in" src="{{ url_for('static', filename='images/D.png') }}" alt="Imagem D"> </center>

---


 <div>
     <center><form action="{{ url_for('page_3_4') }}" method="get">
         <button type="submit">Go to Fourth topic</button>
     </form>
 </div>


---
<div>
   <a href="/page_3_1">BACK</a>
</div>