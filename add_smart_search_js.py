#!/usr/bin/env python3
"""
Fügt Smart-Search JavaScript zur home.html hinzu
"""

smart_search_js = '''

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
'''

with open("templates/main/home.html", "r", encoding="utf-8") as f:
    content = f.read()

if "performSmartSearch" not in content:
    # Vor </script>\n{% endblock body %} einfügen
    content = content.replace("</script>\n{% endblock body %}", smart_search_js + "</script>\n{% endblock body %}")
    with open("templates/main/home.html", "w", encoding="utf-8") as f:
        f.write(content)
    print("✅ Smart-Search JavaScript hinzugefügt!")
else:
    print("⚠️  JavaScript existiert bereits")
