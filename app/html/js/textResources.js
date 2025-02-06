const textResources = {
    ja: {
        submitButton: "送信",
        stopButton: "停止",
        prevButton: "prev",
        prevButtonTooltip: "前の会話",
        nextButton: "next",
        nextButtonTooltip: "次の会話",
        newButton: "new",
        newButtonTooltip: "新しい会話",
        deleteButton: "🗑️",
        deleteButtonTooltip: "削除",
        speakerOnButton: "🔊",
        speakerOnButtonTooltip: "音声",
        speakerOffButton: "🔇",
        speakerOffButtonTooltip: "音声",
        printButton: "🖨️",
        printButtonTooltip: "印刷",
        settingsButton: "⚙️",
        settingsButtonTooltip: "設定",
        messagePlaceholder: "メッセージを入力...",
        deleteConfirm: "本当に削除しますか？",
        deleteFromHereConfirm: "以降のメッセージを削除しますか？",
        searchPrompt: "検索する文字列を入力してください",
        retryConfirm: "リトライしますか？",
        replayConfirm: "リプレイを開始しますか？",
        copy2clipboardToast: "コピーしました",
        copyContextMenu: "コピー",
        settingsTitle: "設定切替",
        settingsColumnSelect: "選択",
        settingsColumnDisplayName: "表示名",
        settingsColumnDescription: "説明",
    },
    en: {
        submitButton: "Send",
        stopButton: "Stop",
        prevButton: "Prev",
        prevButtonTooltip: "Previous chat",
        nextButton: "Next",
        nextButtonTooltip: "Next chat",
        newButton: "New",
        newButtonTooltip: "Create new chat",
        deleteButton: "🗑️",
        deleteButtonTooltip: "Delete chat",
        speakerOnButton: "🔊",
        speakerOnButtonTooltip: "Voice",
        speakerOffButton: "🔇",
        speakerOffButtonTooltip: "Voice",
        printButton: "🖨️",
        printButtonTooltip: "Print",
        settingsButton: "⚙️",
        settingsButtonTooltip: "Settings",
        messagePlaceholder: "Enter your message…",
        deleteConfirm: "Are you sure you want to delete this chat?",
        deleteFromHereConfirm: "Do you want to delete messages from this point onward?",
        searchPrompt: "Please enter a search term",
        retryConfirm: "Do you want to retry?",
        replayConfirm: "Do you want to start the replay?",
        copy2clipboardToast: "Copied!",
        copyContextMenu: "Copy",
        settingsTitle: "Switch Settings",
        settingsColumnSelect: "Select",
        settingsColumnDisplayName: "Display Name",
        settingsColumnDescription: "Description",
    }
};

let currentLanguage = sessionStorage.getItem("currentLanguage") || "ja";

function setCurrentLanguage(language) {
    if (textResources.hasOwnProperty(language)) {
        currentLanguage = language;
        sessionStorage.setItem("currentLanguage", language);
    } else {
        console.error(`Invalid language: ${language}. Defaulting to 'en'.`);
        currentLanguage = "en";
        sessionStorage.setItem("currentLanguage", "en");
    }
}

function getTextResource(key) {
    const resource = textResources[currentLanguage];
    return resource ? resource[key] || key : key;
}
