#!/usr/bin/env python3
"""Aktualisiert partner_landing.html mit neuem kroatischen Text"""

new_content = '''{% extends 'include/base.html' %}
{% load static %}

{% block title %}Registracija za pružatelje usluga - 123-Kroatien.eu{% endblock %}

{% block body %}
<style>
    .hero-partner {
        background: linear-gradient(135deg, #003167 0%, #004a99 50%, #0066cc 100%);
        color: white;
        padding: 80px 0;
    }
    .hero-partner h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 20px;
        color: white !important;
    }
    .hero-partner .lead {
        font-size: 1.15rem;
        opacity: 0.95;
        color: white !important;
        max-width: 800px;
        margin: 0 auto;
    }
    .benefit-card {
        background: white;
        border-radius: 16px;
        padding: 30px;
        height: 100%;
        box-shadow: 0 10px 40px rgba(0,0,0,0.08);
        transition: transform 0.3s ease;
    }
    .benefit-card:hover {
        transform: translateY(-5px);
    }
    .benefit-icon {
        width: 60px;
        height: 60px;
        background: linear-gradient(135deg, #003167 0%, #0066cc 100%);
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        margin-bottom: 20px;
    }
    .benefit-icon i {
        font-size: 24px;
        color: white;
    }
    .benefit-card h3 {
        font-size: 1.2rem;
        font-weight: 600;
        color: #1a1a1a;
        margin-bottom: 12px;
    }
    .benefit-card p {
        color: #666;
        line-height: 1.7;
    }
    .stats-section {
        background: #f8f9fa;
        padding: 50px 0;
    }
    .stat-number {
        font-size: 2.5rem;
        font-weight: 700;
        color: #003167;
    }
    .stat-label {
        color: #666;
    }
    .cta-section {
        background: linear-gradient(135deg, #003167 0%, #004a99 100%);
        padding: 60px 0;
        color: white;
    }
    .btn-cta {
        background: white;
        color: #003167;
        padding: 15px 40px;
        font-size: 1.1rem;
        font-weight: 600;
        border-radius: 50px;
        text-decoration: none;
        display: inline-block;
        transition: all 0.3s ease;
    }
    .btn-cta:hover {
        background: #f0f0f0;
        color: #003167;
        transform: translateY(-2px);
    }
    .intro-badge {
        background: #28a745;
        color: white;
        padding: 8px 20px;
        border-radius: 50px;
        font-weight: 600;
        font-size: 0.9rem;
        display: inline-block;
        margin-bottom: 20px;
    }
    .provider-icon {
        width: 70px;
        height: 70px;
        background: linear-gradient(135deg, #003167 0%, #0066cc 100%);
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        margin: 0 auto 15px;
    }
    .provider-icon i {
        font-size: 28px;
        color: white;
    }
    .highlight-box {
        background: linear-gradient(135deg, #003167 0%, #0066cc 100%);
        color: white;
        padding: 40px;
        border-radius: 16px;
    }
    .highlight-box h3 {
        color: white !important;
    }
</style>

<!-- HERO SECTION -->
<section class="hero-partner">
    <div class="container text-center">
        <span class="intro-badge">UVODNA FAZA</span>
        <h1>Registracija za pružatelje usluga</h1>
        <p class="lead">
            123-KROATIEN.EU je specijalizirana informacijska platforma za pronalazak 
            provjerenih i verificiranih agenata za nekretnine u Hrvatskoj, 
            namijenjena međunarodnim kupcima iz više europskih zemalja.
        </p>
    </div>
</section>

<!-- STATS SECTION -->
<section class="stats-section">
    <div class="container">
        <div class="row text-center">
            <div class="col-md-3 col-6 mb-3">
                <div class="stat-number">80+</div>
                <div class="stat-label">Tematskih web stranica</div>
            </div>
            <div class="col-md-3 col-6 mb-3">
                <div class="stat-number">12</div>
                <div class="stat-label">Europskih zemalja</div>
            </div>
            <div class="col-md-3 col-6 mb-3">
                <div class="stat-number">12</div>
                <div class="stat-label">Jezika</div>
            </div>
            <div class="col-md-3 col-6 mb-3">
                <div class="stat-number">100%</div>
                <div class="stat-label">Fokus na Hrvatsku</div>
            </div>
        </div>
    </div>
</section>

<!-- INFO SECTION -->
<section class="py-5">
    <div class="container">
        <div class="row g-4">
            <div class="col-lg-6">
                <div class="benefit-card">
                    <div class="benefit-icon"><i class="fa fa-sitemap"></i></div>
                    <h3>Mreža specijaliziranih stranica</h3>
                    <p>Platforma upravlja mrežom od više od 80 tematskih web stranica 
                    vezanih isključivo uz Hrvatsku, unutar kojih se prikazuju profili 
                    registriranih pružatelja usluga u relevantnom kontekstu.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="benefit-card">
                    <div class="benefit-icon"><i class="fa fa-users"></i></div>
                    <h3>Proširene mogućnosti prikaza</h3>
                    <p>Tijekom uvodne faze registrirani agenti za nekretnine, građevinske tvrtke, 
                    arhitekti, odvjetnici i porezni savjetnici imaju pristup proširenim 
                    mogućnostima prikaza svojih profila.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="benefit-card">
                    <div class="benefit-icon"><i class="fa fa-gift"></i></div>
                    <h3>Osnovna registracija bez naknade</h3>
                    <p>Osnovna registracija i osnovni profil dostupni su bez naknade. 
                    Nema skrivenih troškova niti obveza.</p>
                </div>
            </div>
            <div class="col-lg-6">
                <div class="benefit-card">
                    <div class="benefit-icon"><i class="fa fa-balance-scale"></i></div>
                    <h3>Jednaka pravila za sve</h3>
                    <p>Pojedine dodatne funkcije uređuju se tijekom vremena zasebno, 
                    uz jednaka pravila za sve registrirane pružatelje usluga.</p>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- WHO CAN REGISTER -->
<section class="py-5 bg-light">
    <div class="container">
        <h2 class="text-center mb-5">Tko se može registrirati?</h2>
        <div class="row justify-content-center">
            <div class="col-lg-10">
                <div class="row g-4 text-center justify-content-center">
                    <div class="col-lg col-md-4 col-6">
                        <div class="p-3">
                            <div class="provider-icon"><i class="fa fa-home"></i></div>
                            <h6>Agenti za nekretnine</h6>
                        </div>
                    </div>
                    <div class="col-lg col-md-4 col-6">
                        <div class="p-3">
                            <div class="provider-icon"><i class="fa fa-building"></i></div>
                            <h6>Građevinske tvrtke</h6>
                        </div>
                    </div>
                    <div class="col-lg col-md-4 col-6">
                        <div class="p-3">
                            <div class="provider-icon"><i class="fa fa-pencil"></i></div>
                            <h6>Arhitekti</h6>
                        </div>
                    </div>
                    <div class="col-lg col-md-4 col-6">
                        <div class="p-3">
                            <div class="provider-icon"><i class="fa fa-balance-scale"></i></div>
                            <h6>Odvjetnici</h6>
                        </div>
                    </div>
                    <div class="col-lg col-md-4 col-6">
                        <div class="p-3">
                            <div class="provider-icon"><i class="fa fa-calculator"></i></div>
                            <h6>Porezni savjetnici</h6>
                        </div>
                    </div>
                </div>
            </div>
        </div>
    </div>
</section>

<!-- CTA SECTION -->
<section class="cta-section text-center">
    <div class="container">
        <h2 class="text-white mb-4">Registrirajte se u uvodnoj fazi</h2>
        <p class="text-white mb-4" style="opacity:0.9;">
            Osnovna registracija je besplatna. Pristupite proširenim mogućnostima prikaza vašeg profila.
        </p>
        <a href="/hr/hrvatska/registracija/" class="btn-cta">
            Registracija
        </a>
    </div>
</section>

{% endblock body %}
'''

with open('templates/main/partner_landing.html', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("✅ partner_landing.html wurde aktualisiert!")
print("   - Neuer kroatischer Text")
print("   - Gleiches ansprechendes Design")
print("   - 4 Info-Karten mit Icons")
print("   - Provider-Übersicht")
print("   - CTA zur Registrierung")
