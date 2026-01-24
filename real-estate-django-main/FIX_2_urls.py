# DIESE ZEILEN ERSETZEN DIE SITEMAP URLS IN main/urls.py
# Suche nach: path('sitemap', views.sitemap, name='sitemap'),
# Ersetze durch:

    path('sitemap/', views.sitemap, name='sitemap'),
    path('sitemap', views.sitemap, name='sitemap-no-slash'),
