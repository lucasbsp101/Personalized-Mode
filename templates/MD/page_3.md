# <center> *Basic Concepts of AI - INDEX* <center>

<center> <ul id="fade-list" style="display: inline-block; text-align: left;">
    {% for item in content %}
        <li>{{ item }}</li>
    {% endfor %}
</ul>

<script>
    // Adiciona um delay crescente para cada item da lista
    document.addEventListener("DOMContentLoaded", function() {
        const listItems = document.querySelectorAll("#fade-list li");
        listItems.forEach((item, index) => {
            item.style.animationDelay = `${index * 0.3}s`; // Cada item aparece com 0.3s de diferença
        });
    });
</script>

---

<center><form action="{{ url_for('page_3_1') }}">
    <button type="submit" style="width: 120px;">Go to First topic</button>
</form>

---

<div>
    <a href="/page_2">BACK</a><br><br>
</div>
