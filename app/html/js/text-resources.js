const textResources = {
    // 日本語
    ja: {
        // 汎用
        okButton: "OK",
        cancelButton: "Cancel",
        closeButton: "閉じる",
        // メイン画面
        submitButton: "送信",
        stopButton: "停止",
        prevButtonTooltip: "前の会話",
        nextButtonTooltip: "次の会話",
        newButtonTooltip: "新しい会話",
        crossSearchButtonTooltip: "ファイル横断検索",
        deleteButtonTooltip: "削除",
        speakerOnButtonTooltip: "音声オン",
        speakerOffButtonTooltip: "音声オフ",
        printButtonTooltip: "印刷",
        settingsButtonTooltip: "設定",
        messagePlaceholder: "メッセージを入力...",
        deleteConfirm: "本当に削除しますか？",
        deleteFromHereConfirm: "以降のメッセージを削除しますか？",
        searchPrompt: "検索する文字列を入力してください",
        retryConfirm: "リトライしますか？",
        replayConfirm: "リプレイを開始しますか？",
        copyContextMenu: "コピー",
        textCopiedMessage: "コピーしました",
        messageCopiedMessage: "メッセージをコピーしました",
        allMessageCopiedMessage: "すべてのメッセージをコピーしました",
        searchContextMenu: "検索",
        summaryContextMenu: "チャットの要約",
        summarizingProgressMessage: "チャットを要約しています...",
        summaryCopiedMessage: "要約をクリップボードにコピーしました",
        // 設定画面
        settingsTitle: "設定切替",
        settingsColumnSelect: "選択",
        settingsColumnDisplayName: "表示名",
        settingsColumnDescription: "説明",
        // ファイル横断検索画面
        crossFileSearchTitle: "ファイル横断検索",
        crossFileSearchColumnResult: "検索結果",
        crossFileSearchColumnLogFile: "ログファイル",
        searchPlaceHolder: "検索文字列を入力してください",
        searchResultsFound: "検索結果：${count} 件",
    },
    // 英語
    en: {
        // General
        okButton: "OK",
        cancelButton: "Cancel",
        closeButton: "Close",
        // Main Screen
        submitButton: "Send",
        stopButton: "Stop",
        prevButtonTooltip: "Previous chat",
        nextButtonTooltip: "Next chat",
        newButtonTooltip: "Create new chat",
        crossSearchButtonTooltip: "Cross-File Search",
        deleteButtonTooltip: "Delete chat",
        speakerOnButtonTooltip: "Voice On",
        speakerOffButtonTooltip: "Voice Off",
        printButtonTooltip: "Print",
        settingsButtonTooltip: "Settings",
        messagePlaceholder: "Enter your message…",
        deleteConfirm: "Are you sure you want to delete this chat?",
        deleteFromHereConfirm: "Do you want to delete messages from this point onward?",
        searchPrompt: "Please enter a search term",
        retryConfirm: "Do you want to retry?",
        replayConfirm: "Do you want to start the replay?",
        copyContextMenu: "Copy",
        textCopiedMessage: "Copied!",
        messageCopiedMessage: "Message copied!",
        allMessageCopiedMessage: "All messages copied!",
        searchContextMenu: "Search",
        summaryContextMenu: "Chat Summary",
        summarizingProgressMessage: "Summarizing chat...",
        summaryCopiedMessage: "Summary copied to clipboard",
        // Settings Screen
        settingsTitle: "Switch Settings",
        settingsColumnSelect: "Select",
        settingsColumnDisplayName: "Display Name",
        settingsColumnDescription: "Description",
        // Cross-File Search Screen
        crossFileSearchTitle: "Cross-File Search",
        crossFileSearchColumnResult: "Search Result",
        crossFileSearchColumnLogFile: "Log File",
        searchPlaceHolder: "Enter search term",
        searchResultsFound: "Results found: ${count}",
    },
    // フィンランド語
    fi: {
        // Yleistä (一般)
        okButton: "OK",
        cancelButton: "Peruuta",
        closeButton: "Sulje",
        // Päänäyttö (メイン画面)
        submitButton: "Lähetä",
        stopButton: "Pysäytä",
        prevButtonTooltip: "Edellinen keskustelu",
        nextButtonTooltip: "Seuraava keskustelu",
        newButtonTooltip: "Luo uusi keskustelu",
        crossSearchButtonTooltip: "Hae tiedostoista",
        deleteButtonTooltip: "Poista keskustelu",
        speakerOnButtonTooltip: "Ääni päälle",
        speakerOffButtonTooltip: "Ääni pois",
        printButtonTooltip: "Tulosta",
        settingsButtonTooltip: "Asetukset",
        messagePlaceholder: "Kirjoita viesti...",
        deleteConfirm: "Haluatko varmasti poistaa tämän keskustelun?",
        deleteFromHereConfirm: "Haluatko poistaa viestit tästä eteenpäin?",
        searchPrompt: "Syötä hakutermi",
        retryConfirm: "Haluatko yrittää uudelleen?",
        replayConfirm: "Haluatko aloittaa uudelleen toiston?",
        copyContextMenu: "Kopioi",
        textCopiedMessage: "Kopioitu!",
        messageCopiedMessage: "Viesti kopioitu!",
        allMessageCopiedMessage: "Kaikki viestit kopioitu!",
        searchContextMenu: "Hae",
        summaryContextMenu: "Keskustelun yhteenveto",
        summarizingProgressMessage: "Tiivistetään keskustelua...",
        summaryCopiedMessage: "Yhteenveto kopioitu leikepöydälle",
        // Asetusnäyttö (設定画面)
        settingsTitle: "Vaihda asetuksia",
        settingsColumnSelect: "Valitse",
        settingsColumnDisplayName: "Näytettävä nimi",
        settingsColumnDescription: "Kuvaus",
        // Tiedostojen välinen haku (ファイル横断検索)
        crossFileSearchTitle: "Tiedostojen välinen haku",
        crossFileSearchColumnResult: "Hakutulos",
        crossFileSearchColumnLogFile: "Lokitiedosto",
        searchPlaceHolder: "Syötä hakutermi",
        searchResultsFound: "Hakutulokset: ${count}",
    },
    // スペイン語
    es: {
        // General (汎用)
        okButton: "OK",
        cancelButton: "Cancelar",
        closeButton: "Cerrar",
        // Pantalla principal (メイン画面)
        submitButton: "Enviar",
        stopButton: "Detener",
        prevButtonTooltip: "Chat anterior",
        nextButtonTooltip: "Siguiente chat",
        newButtonTooltip: "Crear nuevo chat",
        crossSearchButtonTooltip: "Búsqueda entre archivos",
        deleteButtonTooltip: "Eliminar chat",
        speakerOnButtonTooltip: "Activar voz",
        speakerOffButtonTooltip: "Desactivar voz",
        printButtonTooltip: "Imprimir",
        settingsButtonTooltip: "Configuración",
        messagePlaceholder: "Escribe tu mensaje...",
        deleteConfirm: "¿Estás seguro de que deseas eliminar este chat?",
        deleteFromHereConfirm: "¿Deseas eliminar los mensajes desde este punto en adelante?",
        searchPrompt: "Por favor, ingresa un término de búsqueda",
        retryConfirm: "¿Deseas intentarlo nuevamente?",
        replayConfirm: "¿Deseas comenzar la reproducción?",
        copyContextMenu: "Copiar",
        textCopiedMessage: "¡Copiado!",
        messageCopiedMessage: "¡Mensaje copiado!",
        allMessageCopiedMessage: "¡Todos los mensajes copiados!",
        searchContextMenu: "Buscar",
        summaryContextMenu: "Resumen del chat",
        summarizingProgressMessage: "Resumiendo el chat...",
        summaryCopiedMessage: "Resumen copiado al portapapeles",
        // Pantalla de configuración (設定画面)
        settingsTitle: "Cambiar configuración",
        settingsColumnSelect: "Seleccionar",
        settingsColumnDisplayName: "Nombre visible",
        settingsColumnDescription: "Descripción",
        // Pantalla de búsqueda entre archivos (ファイル横断検索画面)
        crossFileSearchTitle: "Búsqueda entre archivos",
        crossFileSearchColumnResult: "Resultado de la búsqueda",
        crossFileSearchColumnLogFile: "Archivo de registro",
        searchPlaceHolder: "Por favor, ingresa un término de búsqueda",
        searchResultsFound: "Resultados encontrados: ${count}",
    },
    // ドイツ語
    de: {
        // Allgemeines (汎用)
        okButton: "OK",
        cancelButton: "Abbrechen",
        closeButton: "Schließen",
        // Hauptbildschirm (メイン画面)
        submitButton: "Senden",
        stopButton: "Stopp",
        prevButtonTooltip: "Vorheriger Chat",
        nextButtonTooltip: "Nächster Chat",
        newButtonTooltip: "Neuen Chat erstellen",
        crossSearchButtonTooltip: "Dateiübergreifende Suche",
        deleteButtonTooltip: "Chat löschen",
        speakerOnButtonTooltip: "Ton einschalten",
        speakerOffButtonTooltip: "Ton ausschalten",
        printButtonTooltip: "Drucken",
        settingsButtonTooltip: "Einstellungen",
        messagePlaceholder: "Nachricht eingeben...",
        deleteConfirm: "Möchten Sie diesen Chat wirklich löschen?",
        deleteFromHereConfirm: "Möchten Sie die Nachrichten ab hier löschen?",
        searchPrompt: "Bitte geben Sie einen Suchbegriff ein",
        retryConfirm: "Möchten Sie es erneut versuchen?",
        replayConfirm: "Möchten Sie die Wiederholung starten?",
        copyContextMenu: "Kopieren",
        textCopiedMessage: "Kopiert!",
        messageCopiedMessage: "Nachricht kopiert!",
        allMessageCopiedMessage: "Alle Nachrichten kopiert!",
        searchContextMenu: "Suchen",
        summaryContextMenu: "Chat-Zusammenfassung",
        summarizingProgressMessage: "Chat wird zusammengefasst...",
        summaryCopiedMessage: "Zusammenfassung in die Zwischenablage kopiert",
        // Einstellungsbildschirm (設定画面)
        settingsTitle: "Einstellungen ändern",
        settingsColumnSelect: "Auswählen",
        settingsColumnDisplayName: "Anzeigename",
        settingsColumnDescription: "Beschreibung",
        // Dateiübergreifende Suche (ファイル横断検索)
        crossFileSearchTitle: "Dateiübergreifende Suche",
        crossFileSearchColumnResult: "Suchergebnis",
        crossFileSearchColumnLogFile: "Protokolldatei",
        searchPlaceHolder: "Suchbegriff eingeben",
        searchResultsFound: "Ergebnisse gefunden: ${count}",
    },
    // フランス語
    fr: {
        // Général (汎用)
        okButton: "OK",
        cancelButton: "Annuler",
        closeButton: "Fermer",
        // Écran principal (メイン画面)
        submitButton: "Envoyer",
        stopButton: "Arrêter",
        prevButtonTooltip: "Conversation précédente",
        nextButtonTooltip: "Conversation suivante", 
        newButtonTooltip: "Nouvelle conversation",
        crossSearchButtonTooltip: "Recherche inter-fichiers",
        deleteButtonTooltip: "Supprimer",
        speakerOnButtonTooltip: "Voix activée",
        speakerOffButtonTooltip: "Voix désactivée",
        printButtonTooltip: "Imprimer",
        settingsButtonTooltip: "Paramètres",
        messagePlaceholder: "Saisissez votre message...",
        deleteConfirm: "Voulez-vous vraiment supprimer ?",
        deleteFromHereConfirm: "Voulez-vous supprimer les messages à partir d'ici ?",
        searchPrompt: "Veuillez saisir le texte à rechercher",
        retryConfirm: "Voulez-vous réessayer ?",
        replayConfirm: "Voulez-vous commencer la relecture ?",
        copyContextMenu: "Copier",
        textCopiedMessage: "Copié !",
        messageCopiedMessage: "Message copié !",
        allMessageCopiedMessage: "Tous les messages copiés !",
        searchContextMenu: "Rechercher",
        summaryContextMenu: "Résumé du chat",
        summarizingProgressMessage: "Résumé du chat en cours...",
        summaryCopiedMessage: "Résumé copié dans le presse-papiers",
        // Écran des paramètres (設定画面)
        settingsTitle: "Changer les paramètres",
        settingsColumnSelect: "Sélection",
        settingsColumnDisplayName: "Nom d'affichage",
        settingsColumnDescription: "Description",
        // Écran de recherche inter-fichiers (ファイル横断検索)
        crossFileSearchTitle: "Recherche inter-fichiers",
        crossFileSearchColumnResult: "Résultat de recherche",
        crossFileSearchColumnLogFile: "Fichier journal",
        searchPlaceHolder: "Saisissez le terme de recherche",
        searchResultsFound: "Résultats trouvés : ${count}",
    },
};

let currentLanguage = sessionStorage.getItem("currentLanguage") || "ja";

export function setCurrentLanguage(language) {
    if (textResources.hasOwnProperty(language)) {
        currentLanguage = language;
        sessionStorage.setItem("currentLanguage", language);
    } else {
        console.error(`Invalid language: ${language}. Defaulting to 'en'.`);
        currentLanguage = "en";
        sessionStorage.setItem("currentLanguage", "en");
    }
}

export function getTextResource(key) {
    const resource = textResources[currentLanguage];
    return resource ? resource[key] || key : key;
}
