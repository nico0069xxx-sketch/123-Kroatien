# Sitemap Links Fix - Befehle für Nik

Alle Links in der Sitemap brauchen das Sprachpräfix `/{{ language }}/`.

## Hauptseiten (Zeilen 154-159)

```bash
sed -i '' 's|href="/"|href="/{{ language }}/"|' templates/main/sitemap.html
sed -i '' 's|href="/listing/"|href="/{{ language }}/listing/"|' templates/main/sitemap.html
sed -i '' 's|href="/about/"|href="/{{ language }}/about/"|' templates/main/sitemap.html
sed -i '' 's|href="/contact/"|href="/{{ language }}/contact/"|' templates/main/sitemap.html
sed -i '' 's|href="/faq/"|href="/{{ language }}/faq/"|' templates/main/sitemap.html
```

## Rechtliches (Zeilen 186-189)

```bash
sed -i '' 's|href="/imprint/"|href="/{{ language }}/imprint/"|' templates/main/sitemap.html
sed -i '' 's|href="/data-protection/"|href="/{{ language }}/data-protection/"|' templates/main/sitemap.html
sed -i '' 's|href="/agb"|href="/{{ language }}/agb/"|' templates/main/sitemap.html
sed -i '' 's|href="/cancellation-policy"|href="/{{ language }}/cancellation-policy/"|' templates/main/sitemap.html
```

## Benutzer-Bereich (Zeilen 250-252)

```bash
sed -i '' 's|href="/accounts/login"|href="/{{ language }}/accounts/login/"|' templates/main/sitemap.html
sed -i '' 's|href="/makler-dashboard/"|href="/{{ language }}/makler-dashboard/"|' templates/main/sitemap.html
sed -i '' 's|href="/accounts/password-reset/"|href="/{{ language }}/accounts/password-reset/"|' templates/main/sitemap.html
```

## Prüfen

```bash
grep 'href="/' templates/main/sitemap.html | grep -v '{{ language }}'
```

Sollte keine Treffer mehr zeigen (außer externe Links wie sitemap.xml).
