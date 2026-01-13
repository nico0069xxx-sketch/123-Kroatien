#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Template für Professional-Registrierung installieren
Führe aus: python3 install_template.py
"""

import os

template_content = '''{% extends 'include/base.html' %}
{% load static %}
{% block body %}

<div style="background-position: center 0%" class="registrationBg bg-theme-overlay">
  <section class="section__breadcrumb">
    <div class="container">
      <div class="row d-flex justify-content-center">
        <div class="col-md-8 text-center">
          <h1 class="text-white">{{ labels.title }}</h1>
          <p class="text-white-50">{{ labels.subtitle }}</p>
        </div>
      </div>
    </div>
  </section>
</div>

<section class="bg-white py-5">
  <div class="container">
    <div class="row justify-content-center">
      <div class="col-lg-8">
        
        {% if success %}
        <div class="alert alert-success text-center py-5">
          <i class="fas fa-check-circle fa-4x text-success mb-3"></i>
          <h3>{{ labels.success_title }}</h3>
          <p class="mb-0">{{ labels.success_message }}</p>
        </div>
        {% else %}
        
        <div class="card shadow-sm">
          <div class="card-body p-4">
            <form id="professionalRegistrationForm" method="post" enctype="multipart/form-data">
              {% csrf_token %}
              
              {% if form.errors %}
              <div class="alert alert-danger">
                <strong>{% if lang == "hr" %}Molimo ispravite greške:{% else %}Bitte korrigieren Sie die Fehler:{% endif %}</strong>
                <ul class="mb-0 mt-2">
                  {% for field in form %}{% for error in field.errors %}<li>{{ field.label }}: {{ error }}</li>{% endfor %}{% endfor %}
                  {% for error in form.non_field_errors %}<li>{{ error }}</li>{% endfor %}
                </ul>
              </div>
              {% endif %}
              
              <h5 class="border-bottom pb-2 mb-4"><i class="fas fa-briefcase text-primary me-2"></i>{% if lang == "hr" %}Vrsta usluge{% else %}Art der Dienstleistung{% endif %}</h5>
              <div class="mb-4">
                <label for="id_professional_type" class="form-label fw-bold">{{ labels.professional_type }} <span class="text-danger">*</span></label>
                {{ form.professional_type }}
              </div>
              
              <h5 class="border-bottom pb-2 mb-4 mt-5"><i class="fas fa-building text-primary me-2"></i>{% if lang == "hr" %}Podaci o tvrtki{% else %}Firmendaten{% endif %}</h5>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_name" class="form-label fw-bold">{{ labels.name }} <span class="text-danger">*</span></label>
                  {{ form.name }}
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_company_name" class="form-label">{{ labels.company_name }}</label>
                  {{ form.company_name }}
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_oib_number" class="form-label">{{ labels.oib_number }}</label>
                  {{ form.oib_number }}
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_website" class="form-label">{{ labels.website }}</label>
                  {{ form.website }}
                </div>
              </div>
              
              <h5 class="border-bottom pb-2 mb-4 mt-5"><i class="fas fa-map-marker-alt text-primary me-2"></i>{% if lang == "hr" %}Lokacija{% else %}Standort{% endif %}</h5>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_city" class="form-label fw-bold">{{ labels.city }} <span class="text-danger">*</span></label>
                  {{ form.city }}
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_region" class="form-label">{{ labels.region }}</label>
                  {{ form.region }}
                </div>
              </div>
              <div class="mb-3">
                <label for="id_address" class="form-label">{{ labels.address }}</label>
                {{ form.address }}
              </div>
              
              <h5 class="border-bottom pb-2 mb-4 mt-5"><i class="fas fa-phone text-primary me-2"></i>{% if lang == "hr" %}Kontakt{% else %}Kontakt{% endif %}</h5>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_email" class="form-label fw-bold">{{ labels.email }} <span class="text-danger">*</span></label>
                  {{ form.email }}
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_phone" class="form-label">{{ labels.phone }}</label>
                  {{ form.phone }}
                </div>
              </div>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_mobile" class="form-label">{{ labels.mobile }}</label>
                  {{ form.mobile }}
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_languages" class="form-label">{{ labels.languages }}</label>
                  {{ form.languages }}
                </div>
              </div>
              
              <h5 class="border-bottom pb-2 mb-4 mt-5"><i class="fas fa-align-left text-primary me-2"></i>{% if lang == "hr" %}Opis{% else %}Beschreibung{% endif %}</h5>
              <div class="mb-3">
                <label for="id_description" class="form-label">{{ labels.description }}</label>
                {{ form.description }}
                <small class="text-muted">{% if lang == "hr" %}Opišite svoje usluge, iskustvo i specijalnosti.{% else %}Beschreiben Sie Ihre Dienstleistungen, Erfahrung und Spezialisierungen.{% endif %}</small>
              </div>
              
              <h5 class="border-bottom pb-2 mb-4 mt-5"><i class="fas fa-image text-primary me-2"></i>{% if lang == "hr" %}Slike{% else %}Bilder{% endif %}</h5>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_company_logo" class="form-label">{{ labels.company_logo }}</label>
                  {{ form.company_logo }}
                  <small class="text-muted">{% if lang == "hr" %}Logo tvrtke (PNG, JPG){% else %}Firmenlogo (PNG, JPG){% endif %}</small>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_profile_image" class="form-label">{{ labels.profile_image }}</label>
                  {{ form.profile_image }}
                  <small class="text-muted">{% if lang == "hr" %}Vaša fotografija{% else %}Ihr Profilbild{% endif %}</small>
                </div>
              </div>
              
              <h5 class="border-bottom pb-2 mb-4 mt-5"><i class="fas fa-file-pdf text-primary me-2"></i>{% if lang == "hr" %}Dokumenti za verifikaciju{% else %}Dokumente zur Verifizierung{% endif %}</h5>
              <div class="row">
                <div class="col-md-6 mb-3">
                  <label for="id_document_type" class="form-label">{{ labels.document_type }}</label>
                  <select name="document_type" id="id_document_type" class="form-control">
                    <option value="">---</option>
                    {% for key, value in labels.document_types.items %}<option value="{{ key }}">{{ value }}</option>{% endfor %}
                  </select>
                </div>
                <div class="col-md-6 mb-3">
                  <label for="id_document" class="form-label">{{ labels.document }}</label>
                  <input type="file" name="document" id="id_document" class="form-control" accept=".pdf,.jpg,.jpeg,.png">
                  <small class="text-muted">PDF, JPG, PNG</small>
                </div>
              </div>
              
              <div class="alert alert-info mt-3">
                <i class="fas fa-info-circle me-2"></i>
                {% if lang == "hr" %}Kako bismo verificirali vaš račun, molimo priložite dokument koji dokazuje vašu djelatnost.{% else %}Um Ihr Konto zu verifizieren, fügen Sie bitte ein Dokument bei, das Ihre Tätigkeit nachweist.{% endif %}
              </div>
              
              <div class="mt-5">
                <div class="form-check mb-4">
                  <input type="checkbox" class="form-check-input" id="privacy" name="privacy" required>
                  <label class="form-check-label" for="privacy">
                    {% if lang == "hr" %}Slažem se s <a href="{% url 'main:data-protection' %}">politikom zaštite podataka</a> i <a href="{% url 'main:agb' %}">uvjetima korištenja</a>. <span class="text-danger">*</span>{% else %}Ich stimme der <a href="{% url 'main:data-protection' %}">Datenschutzerklärung</a> und den <a href="{% url 'main:agb' %}">AGB</a> zu. <span class="text-danger">*</span>{% endif %}
                  </label>
                </div>
                <button type="submit" class="btn btn-primary btn-lg w-100"><i class="fas fa-paper-plane me-2"></i>{{ labels.submit }}</button>
              </div>
            </form>
          </div>
        </div>
        {% endif %}
        
        <div class="mt-5 text-center">
          <p class="text-muted">{% if lang == "hr" %}Nakon uspješne registracije, kontaktirat ćemo vas kako bismo razgovarali o daljnjim koracima.{% else %}Nach erfolgreicher Registrierung setzen wir uns mit Ihnen in Verbindung, um die weiteren Schritte zu besprechen.{% endif %}</p>
        </div>
      </div>
    </div>
  </div>
</section>

<section class="bg-gradient py-5">
  <div class="container">
    <div class="row align-items-center">
      <div class="col-lg-9">
        <h2 class="text-uppercase text-light">{% if lang == "hr" %}JAMČIMO VAM NAJVIŠU POVJERLJIVOST I TRANSPARENTNOST.{% else %}WIR GARANTIEREN IHNEN HÖCHSTE VERTRAULICHKEIT UND TRANSPARENZ.{% endif %}</h2>
        <p class="text-capitalize text-light">{% if lang == "hr" %}Rado ćemo vas diskretno informirati o trenutnoj vrijednosti vaše nekretnine.{% else %}Gerne informieren wir Sie diskret über den aktuellen Wert Ihrer Immobilie.{% endif %}</p>
      </div>
    </div>
  </div>
</section>

<style>
.form-control { border-radius: 4px; border: 1px solid #ced4da; padding: 10px 15px; }
.form-control:focus { border-color: #003167; box-shadow: 0 0 0 0.2rem rgba(0, 49, 103, 0.25); }
.btn-primary { background-color: #003167; border-color: #003167; }
.btn-primary:hover { background-color: #002550; border-color: #002550; }
.card { border: none; border-radius: 8px; }
</style>

{% endblock body %}
'''

filepath = 'templates/main/professional_registration.html'
os.makedirs(os.path.dirname(filepath), exist_ok=True)
with open(filepath, 'w', encoding='utf-8') as f:
    f.write(template_content)
print(f"✅ {filepath} erstellt!")
