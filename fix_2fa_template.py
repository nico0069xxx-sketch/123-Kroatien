template = '''{% extends "include/base.html" %}
{% load static %}
{% block body %}
<div class="container py-5">
  <div class="row justify-content-center">
    <div class="col-md-6">
      <div class="card">
        <div class="card-header text-white" style="background: linear-gradient(135deg, #0D47A1, #0A3A7E);">
          <h4 class="text-white mb-0">
            {% if language == 'hr' %}
              Sigurna prijava - Zastitite svoj racun
            {% elif language == 'en' %}
              Secure Login - Protect Your Account
            {% else %}
              Sichere Anmeldung - Schuetzen Sie Ihr Konto
            {% endif %}
          </h4>
        </div>
        <div class="card-body text-center">
          <p class="mb-4">
            {% if language == 'hr' %}
              Skenirajte ovaj QR kod s aplikacijom za autentifikaciju (npr. Google Authenticator). Nakon toga cete pri svakoj prijavi unijeti 6-znamenkasti kod iz aplikacije.
            {% elif language == 'en' %}
              Scan this QR code with an authenticator app (e.g. Google Authenticator). After that, you will enter a 6-digit code from the app each time you log in.
            {% else %}
              Scannen Sie diesen QR-Code mit einer Authenticator-App (z.B. Google Authenticator). Danach geben Sie bei jeder Anmeldung einen 6-stelligen Code aus der App ein.
            {% endif %}
          </p>
          <img src="data:image/png;base64,{{ qr_code }}" alt="QR Code" class="mb-3" style="max-width: 200px;">
          <p class="small text-muted">
            {% if language == 'hr' %}
              Ili rucno unesite ovaj kod:
            {% elif language == 'en' %}
              Or enter this code manually:
            {% else %}
              Oder geben Sie diesen Code manuell ein:
            {% endif %}
          </p>
          <code class="d-block mb-4">{{ secret }}</code>
          <form method="post" action="{% url 'account:verify_2fa_setup' %}">
            {% csrf_token %}
            <div class="form-group">
              <input type="text" name="code" class="form-control text-center" placeholder="6-stelliger Code" maxlength="6" required>
            </div>
            <button type="submit" class="btn text-white btn-block" style="background: linear-gradient(135deg, #0D47A1, #0A3A7E);">
              {% if language == 'hr' %}Aktiviraj{% elif language == 'en' %}Activate{% else %}Aktivieren{% endif %}
            </button>
          </form>
        </div>
      </div>
    </div>
  </div>
</div>
{% endblock %}'''

with open('templates/account/setup_2fa.html', 'w') as f:
    f.write(template)
print('Template aktualisiert!')
