// Cookie Consent Banner - JavaScript Logik
// GDPR-konform mit LocalStorage für Einstellungen

class CookieConsentManager {
    constructor() {
        this.consentKey = 'cookie_consent';
        this.currentLanguage = this.detectLanguage();
        this.translations = window.cookieConsentTranslations || {};
        this.init();
    }

    // Sprache erkennen (aus Django Session oder Browser)
    detectLanguage() {
        // Versuche die Sprache aus dem HTML lang-Attribut zu lesen
        const htmlLang = document.documentElement.lang;
        if (htmlLang && this.translations[htmlLang]) {
            return htmlLang;
        }

        // Fallback: Browser-Sprache
        const browserLang = navigator.language.split('-')[0];
        if (this.translations[browserLang]) {
            return browserLang;
        }

        // Default: Kroatisch
        return 'hr';
    }

    // Initialisierung
    init() {
        const consent = this.getConsent();
        
        if (!consent) {
            // Noch keine Einwilligung - Banner anzeigen
            this.createBanner();
            this.showBanner();
        } else {
            // Einwilligung vorhanden - Cookies aktivieren
            this.applyCookieSettings(consent);
            this.createSettingsButton();
        }
    }

    // Consent aus LocalStorage lesen
    getConsent() {
        try {
            const stored = localStorage.getItem(this.consentKey);
            return stored ? JSON.parse(stored) : null;
        } catch (e) {
            return null;
        }
    }

    // Consent in LocalStorage speichern
    saveConsent(consent) {
        try {
            localStorage.setItem(this.consentKey, JSON.stringify({
                ...consent,
                timestamp: new Date().toISOString()
            }));
        } catch (e) {
            console.error('Could not save cookie consent:', e);
        }
    }

    // Banner HTML erstellen
    createBanner() {
        const t = this.translations[this.currentLanguage];
        
        const banner = document.createElement('div');
        banner.id = 'cookie-consent-banner';
        banner.innerHTML = `
            <div class="cookie-consent-wrapper">
                <div class="cookie-consent-header">
                    <h3>${t.title}</h3>
                </div>
                
                <div class="cookie-consent-description">
                    ${t.description}
                </div>
                
                <div class="cookie-consent-buttons">
                    <button class="cookie-consent-btn accept-all" id="cookie-accept-all">
                        ${t.acceptAll}
                    </button>
                    <button class="cookie-consent-btn reject-all" id="cookie-reject-all">
                        ${t.rejectAll}
                    </button>
                    <button class="cookie-consent-btn customize" id="cookie-customize">
                        ${t.customize}
                    </button>
                </div>
                
                <div class="cookie-categories" id="cookie-categories">
                    <!-- Notwendige Cookies -->
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <h4>${t.necessary}</h4>
                            <span class="always-active">${t.alwaysActive}</span>
                        </div>
                        <div class="cookie-category-description">
                            ${t.necessaryDesc}
                        </div>
                    </div>
                    
                    <!-- Analytik Cookies -->
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <h4>${t.analytics}</h4>
                            <label class="cookie-toggle">
                                <input type="checkbox" id="cookie-analytics" checked>
                                <span class="cookie-toggle-slider"></span>
                            </label>
                        </div>
                        <div class="cookie-category-description">
                            ${t.analyticsDesc}
                        </div>
                    </div>
                    
                    <!-- Marketing Cookies -->
                    <div class="cookie-category">
                        <div class="cookie-category-header">
                            <h4>${t.marketing}</h4>
                            <label class="cookie-toggle">
                                <input type="checkbox" id="cookie-marketing">
                                <span class="cookie-toggle-slider"></span>
                            </label>
                        </div>
                        <div class="cookie-category-description">
                            ${t.marketingDesc}
                        </div>
                    </div>
                    
                    <div class="cookie-consent-buttons" style="margin-top: 20px;">
                        <button class="cookie-consent-btn save-settings" id="cookie-save-settings">
                            ${t.saveSettings}
                        </button>
                    </div>
                </div>
                
                <div class="cookie-privacy-link">
                    <a href="/data-protection/" target="_blank">${t.privacyPolicy}</a>
                </div>
            </div>
        `;
        
        document.body.appendChild(banner);
        this.attachEventListeners();
    }

    // Event Listener anhängen
    attachEventListeners() {
        // Accept All
        document.getElementById('cookie-accept-all')?.addEventListener('click', () => {
            this.acceptAll();
        });

        // Reject All
        document.getElementById('cookie-reject-all')?.addEventListener('click', () => {
            this.rejectAll();
        });

        // Customize
        document.getElementById('cookie-customize')?.addEventListener('click', () => {
            this.showCustomize();
        });

        // Save Settings
        document.getElementById('cookie-save-settings')?.addEventListener('click', () => {
            this.saveCustomSettings();
        });
    }

    // Banner anzeigen
    showBanner() {
        setTimeout(() => {
            const banner = document.getElementById('cookie-consent-banner');
            if (banner) {
                banner.classList.add('show');
            }
        }, 500);
    }

    // Banner verstecken
    hideBanner() {
        const banner = document.getElementById('cookie-consent-banner');
        if (banner) {
            banner.classList.remove('show');
            setTimeout(() => {
                banner.remove();
            }, 400);
        }
        this.createSettingsButton();
    }

    // Alle akzeptieren
    acceptAll() {
        const consent = {
            necessary: true,
            analytics: true,
            marketing: true
        };
        this.saveConsent(consent);
        this.applyCookieSettings(consent);
        this.hideBanner();
    }

    // Alle ablehnen
    rejectAll() {
        const consent = {
            necessary: true,  // Notwendige Cookies immer aktiv
            analytics: false,
            marketing: false
        };
        this.saveConsent(consent);
        this.applyCookieSettings(consent);
        this.hideBanner();
    }

    // Anpassen-Dialog anzeigen
    showCustomize() {
        const categories = document.getElementById('cookie-categories');
        if (categories) {
            categories.classList.add('show');
            // Buttons ausblenden
            document.querySelector('.cookie-consent-buttons').style.display = 'none';
        }
    }

    // Benutzerdefinierte Einstellungen speichern
    saveCustomSettings() {
        const consent = {
            necessary: true,  // Immer aktiv
            analytics: document.getElementById('cookie-analytics')?.checked || false,
            marketing: document.getElementById('cookie-marketing')?.checked || false
        };
        this.saveConsent(consent);
        this.applyCookieSettings(consent);
        this.hideBanner();
    }

    // Cookie-Einstellungen anwenden
    applyCookieSettings(consent) {
        // Notwendige Cookies (immer aktiv)
        this.enableNecessaryCookies();

        // Analytik Cookies
        if (consent.analytics) {
            this.enableAnalytics();
        } else {
            this.disableAnalytics();
        }

        // Marketing Cookies
        if (consent.marketing) {
            this.enableMarketing();
        } else {
            this.disableMarketing();
        }

        // Event für andere Skripte
        window.dispatchEvent(new CustomEvent('cookieConsentChanged', {
            detail: consent
        }));
    }

    // Notwendige Cookies aktivieren (Session, CSRF, etc.)
    enableNecessaryCookies() {
        // Django CSRF Token und Session sind immer erlaubt
        console.log('Necessary cookies enabled');
    }

    // Analytics aktivieren (z.B. Google Analytics)
    enableAnalytics() {
        console.log('Analytics cookies enabled');
        
        // Beispiel: Google Analytics laden
        // window.dataLayer = window.dataLayer || [];
        // function gtag(){dataLayer.push(arguments);}
        // gtag('js', new Date());
        // gtag('config', 'GA_MEASUREMENT_ID');
    }

    // Analytics deaktivieren
    disableAnalytics() {
        console.log('Analytics cookies disabled');
        
        // Beispiel: Google Analytics deaktivieren
        // window['ga-disable-GA_MEASUREMENT_ID'] = true;
    }

    // Marketing aktivieren (z.B. Facebook Pixel)
    enableMarketing() {
        console.log('Marketing cookies enabled');
        
        // Beispiel: Facebook Pixel laden
        // !function(f,b,e,v,n,t,s){...}(window,document,'script','https://connect.facebook.net/en_US/fbevents.js');
        // fbq('init', 'YOUR_PIXEL_ID');
        // fbq('track', 'PageView');
    }

    // Marketing deaktivieren
    disableMarketing() {
        console.log('Marketing cookies disabled');
    }

    // Einstellungs-Button erstellen
    createSettingsButton() {
        // Prüfen ob Button schon existiert
        if (document.getElementById('cookie-settings-btn')) {
            return;
        }

        const button = document.createElement('button');
        button.id = 'cookie-settings-btn';
        button.innerHTML = '🍪';
        button.title = 'Cookie-Einstellungen';
        button.setAttribute('aria-label', 'Cookie-Einstellungen öffnen');
        
        button.addEventListener('click', () => {
            this.reopenBanner();
        });

        document.body.appendChild(button);
        
        setTimeout(() => {
            button.classList.add('show');
        }, 500);
    }

    // Banner erneut öffnen
    reopenBanner() {
        // Settings Button entfernen
        const settingsBtn = document.getElementById('cookie-settings-btn');
        if (settingsBtn) {
            settingsBtn.remove();
        }

        // Banner neu erstellen
        this.createBanner();
        
        // Aktuelle Einstellungen laden
        const consent = this.getConsent();
        if (consent) {
            if (document.getElementById('cookie-analytics')) {
                document.getElementById('cookie-analytics').checked = consent.analytics;
            }
            if (document.getElementById('cookie-marketing')) {
                document.getElementById('cookie-marketing').checked = consent.marketing;
            }
        }

        // Banner anzeigen
        this.showBanner();
        
        // Direkt Customize-Ansicht zeigen
        setTimeout(() => {
            this.showCustomize();
        }, 600);
    }

    // Sprache wechseln
    changeLanguage(lang) {
        if (this.translations[lang]) {
            this.currentLanguage = lang;
            
            // Banner aktualisieren wenn sichtbar
            const banner = document.getElementById('cookie-consent-banner');
            if (banner) {
                banner.remove();
                this.createBanner();
                this.showBanner();
            }
        }
    }
}

// Initialisierung wenn DOM bereit ist
if (document.readyState === 'loading') {
    document.addEventListener('DOMContentLoaded', () => {
        window.cookieConsent = new CookieConsentManager();
    });
} else {
    window.cookieConsent = new CookieConsentManager();
}

// Globale Funktion zum Sprachwechsel
window.changeCookieConsentLanguage = function(lang) {
    if (window.cookieConsent) {
        window.cookieConsent.changeLanguage(lang);
    }
};
