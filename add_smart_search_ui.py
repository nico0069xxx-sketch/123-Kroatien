#!/usr/bin/env python3
"""
Fügt Smart-Search UI zur home.html hinzu
"""

smart_search_html = '''
    <!-- AI SMART-SEARCH -->
    <div class="container my-4">
        <div class="row justify-content-center">
            <div class="col-lg-8">
                <div class="smart-search-box" style="background: linear-gradient(135deg, #003167 0%, #004a99 100%); border-radius: 15px; padding: 25px; box-shadow: 0 4px 15px rgba(0,0,0,0.2);">
                    <h5 class="text-white text-center mb-3">
                        <i class="fa fa-magic"></i> {{ smart_search_title|default:"KI-Immobiliensuche" }}
                    </h5>
                    <div class="input-group">
                        <input type="text" id="smart-search-input" class="form-control form-control-lg" 
                               placeholder="{{ smart_search_placeholder|default:'Beschreibe deine Traumimmobilie... z.B. Haus am Meer mit Pool unter 500.000€' }}"
                               style="border-radius: 10px 0 0 10px; border: none; padding: 15px;">
                        <div class="input-group-append">
                            <button id="smart-search-btn" class="btn btn-danger btn-lg" style="border-radius: 0 10px 10px 0; padding: 15px 30px;">
                                <i class="fa fa-search"></i>
                            </button>
                        </div>
                    </div>
                    <div id="smart-search-loading" class="text-center mt-3" style="display: none;">
                        <i class="fa fa-spinner fa-spin text-white"></i>
                        <span class="text-white ml-2">{{ smart_search_loading|default:"Suche läuft..." }}</span>
                    </div>
                </div>
            </div>
        </div>
    </div>
    
    <!-- Smart-Search Ergebnisse -->
    <div id="smart-search-results" class="container my-4" style="display: none;">
        <div class="row">
            <div class="col-12">
                <h5 id="smart-search-message" class="text-center mb-4" style="color: #003167;"></h5>
            </div>
        </div>
        <div id="smart-search-listings" class="row"></div>
    </div>
'''

smart_search_js = '''
<script>
// AI Smart-Search
document.getElementById('smart-search-btn').addEventListener('click', performSmartSearch);
document.getElementById('smart-search-input').addEventListener('keypress', function(e) {
    if (e.key === 'Enter') performSmartSearch();
});

function performSmartSearch() {
    const query = document.getElementById('smart-search-input').value.trim();
    if (!query) return;
    
    const loading = document.getElementById('smart-search-loading');
    const results = document.getElementById('smart-search-results');
    const listings = document.getElementById('smart-search-listings');
    const message = document.getElementById('smart-search-message');
    
    loading.style.display = 'block';
    results.style.display = 'none';
    
    fetch('/api/smart-search/', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': getCookie('csrftoken')
        },
        body: JSON.stringify({ query: query })
    })
    .then(response => response.json())
    .then(data => {
        loading.style.display = 'none';
        
        if (data.status === 'success') {
            message.textContent = data.message;
            listings.innerHTML = '';
            
            if (data.results && data.results.length > 0) {
                data.results.forEach(item => {
                    const card = `
                        <div class="col-md-4 mb-4">
                            <div class="card h-100" style="border-color: #003167;">
                                <img src="${item.image || '/static/images/no-image.png'}" class="card-img-top" alt="${item.title}" style="height: 200px; object-fit: cover;">
                                <div class="card-body">
                                    <h6 class="card-title" style="color: #003167;">${item.title}</h6>
                                    <p class="card-text text-muted">
                                        <i class="fa fa-map-marker"></i> ${item.location}<br>
                                        <i class="fa fa-bed"></i> ${item.bedrooms} | 
                                        <i class="fa fa-bath"></i> ${item.bathrooms} |
                                        <i class="fa fa-map"></i> ${item.area} m²
                                    </p>
                                    <h5 style="color: #c41e3a;">€ ${item.price.toLocaleString()}</h5>
                                    <a href="/property-details/${item.id}/" class="btn btn-sm" style="background-color: #003167; color: white;">Details</a>
                                </div>
                            </div>
                        </div>
                    `;
                    listings.innerHTML += card;
                });
            }
            
            results.style.display = 'block';
            results.scrollIntoView({ behavior: 'smooth' });
        } else {
            alert(data.message || 'Fehler bei der Suche');
        }
    })
    .catch(error => {
        loading.style.display = 'none';
        console.error('Smart-Search Error:', error);
    });
}

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}
</script>
'''

# home.html lesen
with open("templates/main/home.html", "r", encoding="utf-8") as f:
    content = f.read()

# Prüfen ob Smart-Search schon existiert
if "smart-search-box" not in content:
    # Nach dem Carousel einfügen (nach <!-- END CAROUSEL HOMEPAGE -->)
    insert_marker = "<!-- END CAROUSEL HOMEPAGE -->"
    if insert_marker in content:
        content = content.replace(insert_marker, insert_marker + "\n" + smart_search_html)
        print("✅ Smart-Search HTML eingefügt!")
    else:
        # Alternativ: Nach </div> des Carousel
        content = content.replace('<div class="clearfix"></div>', smart_search_html + '\n    <div class="clearfix"></div>', 1)
        print("✅ Smart-Search HTML eingefügt (Alternative Position)!")
    
    # JavaScript vor {% endblock js %} einfügen
    if "{% endblock js %}" in content:
        content = content.replace("{% endblock js %}", smart_search_js + "\n{% endblock js %}")
        print("✅ Smart-Search JavaScript eingefügt!")
    
    with open("templates/main/home.html", "w", encoding="utf-8") as f:
        f.write(content)
else:
    print("⚠️  Smart-Search UI existiert bereits")
