var klaroConfig = {
  elementID: 'klaro',
  storageMethod: 'cookie',
  cookieName: 'klaro',
  cookieExpiresAfterDays: 365,
  default: false, // opt-in
  mustConsent: true,
  acceptAll: true,
  hideDeclineAll: false,
  lang: 'en',
  translations: {
    en: { consentModal: { title: "Privacy settings", description: "We use cookies to provide and improve our services. You can accept or decline non-essential cookies." }, consentNotice: { description: "We use cookies. You can accept or decline non-essential cookies.", learnMore: "Settings" }, acceptAll: "Accept all", decline: "Decline", save: "Save" },
    de: { consentModal: { title: "Datenschutzeinstellungen", description: "Wir verwenden Cookies, um unsere Dienste bereitzustellen und zu verbessern. Du kannst nicht notwendige Cookies ablehnen." }, consentNotice: { description: "Wir verwenden Cookies. Du kannst nicht notwendige Cookies ablehnen.", learnMore: "Einstellungen" }, acceptAll: "Alle akzeptieren", decline: "Ablehnen", save: "Speichern" },
    hr: { consentModal: { title: "Postavke privatnosti", description: "Koristimo kolačiće za pružanje i poboljšanje usluga. Možete odbiti nebitne kolačiće." }, consentNotice: { description: "Koristimo kolačiće. Možete odbiti nebitne kolačiće.", learnMore: "Postavke" }, acceptAll: "Prihvati sve", decline: "Odbij", save: "Spremi" },
    nl: { consentModal: { title: "Privacy-instellingen", description: "We gebruiken cookies om onze diensten te leveren en te verbeteren. U kunt niet-essentiële cookies weigeren." }, consentNotice: { description: "We gebruiken cookies. U kunt niet-essentiële cookies weigeren.", learnMore: "Instellingen" }, acceptAll: "Alles accepteren", decline: "Weigeren", save: "Opslaan" },
    sk: { consentModal: { title: "Nastavenia súkromia", description: "Používame súbory cookie na poskytovanie a zlepšovanie služieb. Môžete odmietnuť nepodstatné súbory cookie." }, consentNotice: { description: "Používame súbory cookie. Môžete odmietnuť nepodstatné súbory cookie.", learnMore: "Nastavenia" }, acceptAll: "Prijať všetko", decline: "Odmietnuť", save: "Uložiť" },
    el: { consentModal: { title: "Ρυθμίσεις απορρήτου", description: "Χρησιμοποιούμε cookies για παροχή και βελτίωση υπηρεσιών. Μπορείτε να απορρίψετε τα μη απαραίτητα cookies." }, consentNotice: { description: "Χρησιμοποιούμε cookies. Μπορείτε να απορρίψετε τα μη απαραίτητα cookies.", learnMore: "Ρυθμίσεις" }, acceptAll: "Αποδοχή όλων", decline: "Απόρριψη", save: "Αποθήκευση" },
    pl: { consentModal: { title: "Ustawienia prywatności", description: "Używamy plików cookie, aby świadczyć i ulepszać usługi. Możesz odrzucić nieistotne pliki cookie." }, consentNotice: { description: "Używamy plików cookie. Możesz odrzucić nieistotne pliki cookie.", learnMore: "Ustawienia" }, acceptAll: "Akceptuj wszystko", decline: "Odrzuć", save: "Zapisz" },
    ru: { consentModal: { title: "Настройки конфиденциальности", description: "Мы используем файлы cookie для предоставления и улучшения услуг. Вы можете отклонить необязательные cookie." }, consentNotice: { description: "Мы используем cookie. Вы можете отклонить необязательные cookie.", learnMore: "Настройки" }, acceptAll: "Принять все", decline: "Отклонить", save: "Сохранить" },
    no: { consentModal: { title: "Personverninnstillinger", description: "Vi bruker informasjonskapsler for å levere og forbedre tjenester. Du kan avslå ikke-nødvendige informasjonskapsler." }, consentNotice: { description: "Vi bruker informasjonskapsler. Du kan avslå ikke-nødvendige.", learnMore: "Innstillinger" }, acceptAll: "Godta alle", decline: "Avslå", save: "Lagre" },
    fr: { consentModal: { title: "Paramètres de confidentialité", description: "Nous utilisons des cookies pour fournir et améliorer nos services. Vous pouvez refuser les cookies non essentiels." }, consentNotice: { description: "Nous utilisons des cookies. Vous pouvez refuser les cookies non essentiels.", learnMore: "Paramètres" }, acceptAll: "Tout accepter", decline: "Refuser", save: "Enregistrer" }
  },
  // Hier definieren wir später Tracking/Services. Für den Start leer lassen:
  apps: []
};
