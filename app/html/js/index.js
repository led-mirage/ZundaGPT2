import { setFontFamilyAndSize, setCopyright, showBody, setClickEventHandler } from "./util.js";
import { setCurrentLanguage, getTextResource } from "./text-resources.js";

let g_userName = "あなた";
let g_userColor = "#007bff";
let g_userIcon = "";
let g_assistantName = "ずんだ";
let g_assistantColor = "#006400";
let g_assistantIcon = "";
let g_speakerOn = true;
let g_nextMessageIndex = 0;
let g_searchTextIndex = 0;
let g_searchTextTotal = 0;
let g_welcomeTitle = "";
let g_welcomeMessage = "";
let g_aiAgentAvailable = false;
let g_aiAgentCreationError = "";
let g_savedCSS = {};

// 初期化
document.addEventListener("DOMContentLoaded", function() {
    // ツールボタンのクリックイベントハンドラの登録
    setClickEventHandler("prev-button", prevChat);
    setClickEventHandler("next-button", nextChat);
    setClickEventHandler("new-button", newChat);
    setClickEventHandler("cross-search-button", crossFileSearch);
    setClickEventHandler("delete-button", deleteChat);
    setClickEventHandler("speaker-button", toggleSpeaker);
    setClickEventHandler("print-button", printDocument);
    setClickEventHandler("settings-button", settings);

    const textarea = document.getElementById("message");
    textarea.addEventListener("input", autoResize, false);

    const button = document.getElementById("submit-button");
    button.addEventListener("click", function() {
        submit();
        autoResize.call(textarea);
    }, false);

    document.getElementById("message").addEventListener("keydown", function(event) {
        // Enterが押されたが、Shiftが押されていない場合
        if (event.key === "Enter" && !event.shiftKey) {
            const button = document.getElementById("submit-button");
            if (button) {
                if (!button.classList.contains("submit-button-disabled")) {
                    event.preventDefault(); // デフォルトのEnterによる改行を防ぐ
                    submit(); // 送信処理を実行
                    autoResize.call(textarea);
                }
            }
        }
    });

    // キーダウンイベントハンドラの登録
    document.addEventListener("keydown", handleKeyDown);

    // コンテキストメニューイベントハンドラの登録
    document.addEventListener("contextmenu", handleContextMenu);

    autoResize.call(textarea);

    function autoResize() {
        this.style.height = "auto";
        this.style.height = this.scrollHeight - rem2px(2) + "px";
    }
});

// キーダウンイベントハンドラ
function handleKeyDown(event) {
    if ((event.ctrlKey || event.metaKey) && event.shiftKey && event.keyCode === 70) { // Ctrl + Shift + F
        crossFileSearch();
    }
    else if ((event.ctrlKey || event.metaKey) && event.keyCode === 70) { // Ctrl + F
        searchText();
    }
    else if ((event.ctrlKey || event.metaKey) && event.keyCode === 82) { // Ctrl + R
        let result = confirm(getTextResource("replayConfirm"));
        if (result) {
            document.getElementById("chat-messages").innerHTML = "";
            pywebview.api.replay();
        }
    }
    else if (event.keyCode == 27) { // ESC
        var instance = new Mark(document.body);
        g_searchTextIndex = g_searchTextTotal = 0;
        instance.unmark();
    }
    else if (event.keyCode == 114) { // F3
        if (g_searchTextTotal > 0) {
            if (event.shiftKey) {
                g_searchTextIndex--;
                if (g_searchTextIndex < 0) {
                    g_searchTextIndex = g_searchTextTotal - 1;
                }
            }
            else {
                g_searchTextIndex++;
                if (g_searchTextIndex >= g_searchTextTotal) {
                    g_searchTextIndex = 0;
                }
            }
            highlightSearchResult();
        }
    }
}

// コンテキストメニューイベントハンドラ
function handleContextMenu(event) {
    event.preventDefault();

    // 既に表示されているメニューがあれば消す
    const existingMenu = document.querySelector('.contextmenu');
    if (existingMenu) {
        document.body.removeChild(existingMenu);
    }

    let menuContent = "";
    menuContent += `<button id="copy"><i class="fa-regular fa-copy"></i> ${getTextResource("copyContextMenu")}</button><br>`;
    menuContent += `<button id="search"><i class="fa-solid fa-magnifying-glass"></i> ${getTextResource("searchContextMenu")}</button><br>`;
    menuContent += `<button id="summary"><i class="fa-solid fa-compress"></i> ${getTextResource("summaryContextMenu")}</button><br>`;

    const menu = document.createElement("div");
    menu.className = "contextmenu";
    menu.style.visibility = "hidden";
    menu.innerHTML = menuContent;
    document.body.appendChild(menu);
    const menuWidth = menu.offsetWidth;
    const menuHeight = menu.offsetHeight;
    const windowWidth = window.innerWidth;
    const windowHeight = window.innerHeight;
    let xPos = event.pageX;
    let yPos = event.pageY;
    if (xPos + menuWidth > windowWidth) {
        xPos = windowWidth - menuWidth - 10;
    } 
    if (yPos + menuHeight > windowHeight) {
        yPos = windowHeight - menuHeight - 10;
    }
    menu.style.left = `${xPos}px`;
    menu.style.top = `${yPos}px`;
    menu.style.visibility = "visible";

    const copyButton = document.getElementById("copy");
    if (copyButton) {
        copyButton.addEventListener("click", async function(clickEvent) {
            const selectedText = window.getSelection().toString();
            if (selectedText) {
                document.body.removeChild(menu);
                //navigator.clipboard.writeText(selectedText);
                await pywebview.api.copytext_to_clipboard(selectedText);
                showToast(clickEvent, getTextResource("textCopiedMessage"));
            }
            else {
                copyChatAllMessages();
                showToast(clickEvent, getTextResource("allMessageCopiedMessage"));
            }
        });
    }

    const searchButton = document.getElementById("search");
    if (searchButton) {
        searchButton.addEventListener("click", function() {
            document.body.removeChild(menu);
            // 少しタイミングを遅らせないとメニューが消えない
            setTimeout(function() {
                const selectedText = window.getSelection().toString();
                searchText(selectedText);
            }, 100);
        });
    }

    const summaryButton = document.getElementById("summary");
    if (summaryButton) {
        summaryButton.addEventListener("click", function(clickEvent) {
            document.body.removeChild(menu);
            // 少しタイミングを遅らせないとメニューが消えない
            setTimeout(function() {
                summarizeChat(clickEvent);
            }, 100);
        });
    }

    // どこかクリックされたらコンテキストメニューを消す
    document.addEventListener("click", function() {
        if (document.body.contains(menu)) {
            document.body.removeChild(menu);
        }
    }, { once: true });
}

// remをpxに変換
function rem2px(rem) {
    var rootFontSize = parseFloat(getComputedStyle(document.documentElement).fontSize);
    return rem * rootFontSize;
}

// IME対策
// IMEがONの状態かつフォーカスがテキストボックスにある状態で、
// 別のアプリを見るなどしてウィンドウのフォーカスが失われ再度戻ってきたときに、
// IMEの変換がテキストボックス内でできなくなる現象に対処
window.onfocus = function() {
    document.getElementById("message").blur();
}

// pywebviewの初期化完了
window.addEventListener("pywebviewready", async function() {
    try {
        const appConfig = await pywebview.api.get_app_config_js();
        initUIComponents(appConfig);

        await pywebview.api.page_loaded();

        if (document.querySelectorAll(".chat-message").length === 0) {
            addWelcome();
        }
    }
    catch (error) {
        console.error("Error: " + error)
    }
})

// コンポーネントの初期化
function initUIComponents(appConfig) {
    saveCSSValue();

    if (appConfig.theme === "dark") {
        document.body.classList.add("dark-mode");
    }

    setCurrentLanguage(appConfig.language);
    setFontFamilyAndSize(appConfig.fontFamily, appConfig.fontSize);
    setCopyright(appConfig.copyright);

    let button = document.getElementById("submit-button");
    if (button) {
        button.textContent = getTextResource("submitButton");
    }

    button = document.getElementById("prev-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("prevButtonTooltip");
        }
    }

    button = document.getElementById("next-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("nextButtonTooltip");
        }
    }

    button = document.getElementById("new-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("newButtonTooltip");
        }
    }

    button = document.getElementById("cross-search-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("crossSearchButtonTooltip");
        }
    }

    button = document.getElementById("delete-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("deleteButtonTooltip");
        }
    }

    button = document.getElementById("speaker-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("speakerOnButtonTooltip");
        }
    }

    button = document.getElementById("print-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("printButtonTooltip");
        }
    }

    button = document.getElementById("settings-button");
    if (button) {
        const tooltip = button.querySelector('.tooltiptext');
        if (tooltip) {
            tooltip.textContent = getTextResource("settingsButtonTooltip");
        }
    }

    let textarea = document.getElementById("message");
    if (textarea) {
        textarea.placeholder = getTextResource("messagePlaceholder");
    }

    showBody();
}

// CSSのカスタムプロパティ値を保存する
function saveCSSValue() {
    const style = getComputedStyle(document.documentElement);
    g_savedCSS = {
        bodyBgcolor: style.getPropertyValue("--body-bgcolor").trim(),
        containerBgcolor: style.getPropertyValue("--container-bgcolor").trim(),
        backgroundImage: style.getPropertyValue("--background-image").trim(),
        backgroundImageOpacity: style.getPropertyValue("--background-image-opacity").trim(),
        headerBgcolor: style.getPropertyValue("--header-bgcolor").trim(),
        headerColor: style.getPropertyValue("--header-color").trim(),
        welcomeTitleColor: style.getPropertyValue("--welcome-title-color").trim(),
        welcomeMessageColor: style.getPropertyValue("--welcome-message-color").trim(),
        speakerNameTextShadow: style.getPropertyValue("--speaker-name-text-shadow").trim(),
        chatMessagesBgcolor: style.getPropertyValue("--chat-messages-bgcolor").trim(),
        messageTextBgcolor: style.getPropertyValue("--message-text-bgcolor").trim(),
        messageTextColor: style.getPropertyValue("--message-text-color").trim(),
        messageTextShadow: style.getPropertyValue("--message-text-shadow").trim(),
        messageTextBorderRadius: style.getPropertyValue("--message-text-border-radius").trim(),
        messageTextEmColor: style.getPropertyValue("--message-text-em-color").trim(),

        darkBodyBgcolor: style.getPropertyValue("--dark-body-bgcolor").trim(),
        darkContainerBgcolor: style.getPropertyValue("--dark-container-bgcolor").trim(),
        darkBackgroundImage: style.getPropertyValue("--dark-background-image").trim(),
        darkBackgroundImageOpacity: style.getPropertyValue("--dark-background-image-opacity").trim(),
        darkHeaderBgcolor: style.getPropertyValue("--dark-header-bgcolor").trim(),
        darkHeaderColor: style.getPropertyValue("--dark-header-color").trim(),
        darkWelcomeTitleColor: style.getPropertyValue("--dark-welcome-title-color").trim(),
        darkWelcomeMessageColor: style.getPropertyValue("--dark-welcome-message-color").trim(),
        darkSpeakerNameTextShadow: style.getPropertyValue("--dark-speaker-name-text-shadow").trim(),
        darkChatMessagesBgcolor: style.getPropertyValue("--dark-chat-messages-bgcolor").trim(),
        darkMessageTextBgcolor: style.getPropertyValue("--dark-message-text-bgcolor").trim(),
        darkMessageTextColor: style.getPropertyValue("--dark-message-text-color").trim(),
        darkMessageTextShadow: style.getPropertyValue("--dark-message-text-shadow").trim(),
        darkMessageTextBorderRadius: style.getPropertyValue("--dark-message-text-border-radius").trim(),
        darkMessageTextEmColor: style.getPropertyValue("--dark-message-text-em-color").trim(),
    }
}

// CSSのカスタムプロパティ値を復元する
function restoreCSSValue() {
    document.documentElement.style.setProperty("--body-bgcolor", g_savedCSS.bodyBgcolor);
    document.documentElement.style.setProperty("--container-bgcolor", g_savedCSS.containerBgcolor);
    document.documentElement.style.setProperty("--background-image", g_savedCSS.backgroundImage);
    document.documentElement.style.setProperty("--background-image-opacity", g_savedCSS.backgroundImageOpacity);
    document.documentElement.style.setProperty("--header-bgcolor", g_savedCSS.headerBgcolor);
    document.documentElement.style.setProperty("--header-color", g_savedCSS.headerColor);
    document.documentElement.style.setProperty("--welcome-title-color", g_savedCSS.welcomeTitleColor);
    document.documentElement.style.setProperty("--welcome-message-color", g_savedCSS.welcomeMessageColor);
    document.documentElement.style.setProperty("--chat-messages-bgcolor", g_savedCSS.chatMessagesBgcolor);
    document.documentElement.style.setProperty("--message-text-bgcolor", g_savedCSS.messageTextBgcolor);
    document.documentElement.style.setProperty("--message-text-color", g_savedCSS.messageTextColor);
    document.documentElement.style.setProperty("--message-text-border-radius", g_savedCSS.messageTextBorderRadius);
    document.documentElement.style.setProperty("--message-text-em-color", g_savedCSS.messageTextEmColor);

    document.documentElement.style.setProperty("--dark-body-bgcolor", g_savedCSS.darkBodyBgcolor);
    document.documentElement.style.setProperty("--dark-container-bgcolor", g_savedCSS.darkContainerBgcolor);
    document.documentElement.style.setProperty("--dark-background-image", g_savedCSS.darkBackgroundImage);
    document.documentElement.style.setProperty("--dark-background-image-opacity", g_savedCSS.darkBackgroundImageOpacity);
    document.documentElement.style.setProperty("--dark-header-bgcolor", g_savedCSS.darkHeaderBgcolor);
    document.documentElement.style.setProperty("--dark-header-color", g_savedCSS.darkHeaderColor);
    document.documentElement.style.setProperty("--dark-welcome-title-color", g_savedCSS.darkWelcomeTitleColor);
    document.documentElement.style.setProperty("--dark-welcome-message-color", g_savedCSS.darkWelcomeMessageColor);
    document.documentElement.style.setProperty("--dark-chat-messages-bgcolor", g_savedCSS.darkChatMessagesBgcolor);
    document.documentElement.style.setProperty("--dark-message-text-bgcolor", g_savedCSS.darkMessageTextBgcolor);
    document.documentElement.style.setProperty("--dark-message-text-color", g_savedCSS.darkMessageTextColor);
    document.documentElement.style.setProperty("--dark-message-text-border-radius", g_savedCSS.darkMessageTextBorderRadius);
    document.documentElement.style.setProperty("--dark-message-text-em-color", g_savedCSS.darkMessageTextEmColor);
}

// CSS変数名から保存済み値を取得する
function getSavedCSSValue(varName) {
    if (!g_savedCSS) return null;

    // 例："--body-bgcolor" → "bodyBgcolor" に変換
    const camelKey = varName
        .replace(/^--/, "") // 先頭の "--" を削除
        .replace(/-([a-z])/g, (_, c) => c.toUpperCase()); // -x を X に変換

    return g_savedCSS[camelKey] ?? null;
}

// 送信ボタン押下時イベントハンドラ
function submit() {
    const button = document.getElementById("submit-button");
    if (button) {
        if (!button.classList.contains("submit-button-disabled")) {
            sendMessage();
        }
        else {
            stopSendMessage();
        }
    }
}

// メッセージを送信する
async function sendMessage() {
    if (!g_aiAgentAvailable) {
        alert(g_aiAgentCreationError);
        return;
    }

    const text = document.getElementById("message").value;
    if (text === "") return;

    setSubmitButtonState(true);

    // HTMLにメッセージを追加
    addChatMessage("user", g_userName, g_userColor, text)
    scrollToBottom();
    hideChatRetryButton();
    document.getElementById("message").value = "";

    // Python側に通知
    try {
        await pywebview.api.send_message_to_chatgpt(text);
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// メッセージを送信を中止する
async function stopSendMessage() {
    // Python側に通知
    try {
        await pywebview.api.stop_send_message_to_chatgpt();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// 送信ボタンの状態を設定する
function setSubmitButtonState(isSending) {
    const button = document.getElementById("submit-button");
    if (button) {
        if (isSending) {
            button.textContent = getTextResource("stopButton");
            button.classList.add("submit-button-disabled")
        }
        else {
            button.textContent = getTextResource("submitButton");
            button.classList.remove("submit-button-disabled")
        }
    }
}

// チャットメッセージを下端までスクロールする
function scrollToBottom() {
    const messageContainer = document.querySelector(".chat-messages");
    messageContainer.scrollTop = messageContainer.scrollHeight;
}

// 文字列をHTML用にエスケープする
function escapeHtml(text) {
    return text
        .replace(/&/g, "&amp;")
        .replace(/</g, "&lt;")
        .replace(/>/g, "&gt;")
        .replace(/"/g, "&quot;")
        .replace(/'/g, "&#x27;")
        .replace(/\n/g, "<br>")
        .replace(/ /g, "&nbsp;")
        .replace(/\t/g, "&nbsp;&nbsp;&nbsp;&nbsp;");
}

// TeX用の文字列をエスケープする
function escapeTex(text) {
    return text.replace(/\\/g, "@@@@");
}

// TeX用にエスケープした文字列を元に戻す
function unescapeTex(text) {
    return text.replace(/@@@@/g, "\\");
}

// スピーカーのON/OFF
async function toggleSpeaker() {
    g_speakerOn = !g_speakerOn;
    setSpeakerStateText();

    // Python側に通知
    try {
        await pywebview.api.toggle_speaker();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// スピーカーの状態表示
function setSpeakerStateText() {
    let button = document.getElementById("speaker-button");
    if (g_speakerOn) {
        const tooltipText = getTextResource("speakerOnButtonTooltip");
        button.innerHTML = `<i class='fa-solid fa-volume-high'></i><span class='tooltiptext'>${tooltipText}</span>`;
    }
    else {
        const tooltipText = getTextResource("speakerOffButtonTooltip");
        button.innerHTML = `<i class='fa-solid fa-volume-xmark'></i><span class='tooltiptext'>${tooltipText}</span>`;
    }
}

// Welcomeメッセージの表示をON/OFFする
function showWelcome(show) {
    const welcome = document.getElementById("welcome");
    if (welcome) {
        if (show) {
            welcome.style.display = "flex";
        }
        else {
            welcome.style.display = "none";
        }
    }
}

// Welcomeメッセージブロックを追加する
function addWelcome() {
    // チャットメッセージコンテナを取得
    const chatMessagesContainer = document.getElementById("chat-messages");

    // Welcomeコンテナを作成
    const welcomeContainer = document.createElement("div");
    welcomeContainer.id = "welcome";
    welcomeContainer.classList.add("welcome");
    chatMessagesContainer.appendChild(welcomeContainer);

    // アシスタントアイコンを作成
    if (g_assistantIcon != "") {
        const imgElement = document.createElement("img");
        imgElement.classList.add("welcome-chat-icon");
        imgElement.src = `data:image/png;base64,${g_assistantIcon}`;
        welcomeContainer.appendChild(imgElement);
    }

    // Welcomeタイトルを作成
    const welcomeTitle = document.createElement("div");
    welcomeTitle.id = "welcome-title";
    welcomeTitle.classList.add("welcome-title");
    welcomeTitle.textContent = g_welcomeTitle;
    welcomeContainer.appendChild(welcomeTitle);

    // Welcomeメッセージを作成
    const welcomeMessage = document.createElement("div");
    welcomeMessage.id = "welcome-message";
    welcomeMessage.classList.add("welcome-message");
    welcomeMessage.textContent = g_welcomeMessage;
    welcomeContainer.appendChild(welcomeMessage);
}

// チャットメッセージブロックを追加する
function addChatMessage(role, speakerName, color, messageText) {
    // Welcomeメッセージの非表示
    showWelcome(false);

    // チャットメッセージコンテナを取得
    const chatMessagesContainer = document.getElementById("chat-messages");

    // 新しいチャットメッセージ要素を作成
    const chatMessageElement = document.createElement("div");
    chatMessageElement.classList.add("chat-message");
    chatMessageElement.id = "message-" + g_nextMessageIndex++;

    // 発言者名を表示する要素を作成
    const speakerElement = document.createElement("div");
    speakerElement.classList.add("speaker-name");
    speakerElement.style.color = color;
    speakerElement.textContent = speakerName;

    if (role === "user" || role === "replay_user") {
        if (g_userIcon != "") {
            // ユーザーアイコンをつける
            const imgElement = document.createElement("img");
            imgElement.classList.add("chat-icon");
            imgElement.src = `data:image/png;base64,${g_userIcon}`;
            speakerElement.prepend(imgElement);
        }
    }
    else if (role === "assistant" || role === "replay_assistant") {
        if (g_assistantIcon != "") {
            // アシスタントアイコンをつける
            const imgElement = document.createElement("img");
            imgElement.classList.add("chat-icon");
            imgElement.src = `data:image/png;base64,${g_assistantIcon}`;
            speakerElement.prepend(imgElement);
        }
    }

    // コピーボタンをつける
    const copyElement = document.createElement("button");
    copyElement.classList.add("message-copy-btn");
    copyElement.innerHTML = "<i class='fa-regular fa-copy'></i>";
    copyElement.addEventListener("click", copyChatMessage);
    speakerElement.appendChild(copyElement);

    if (role === "user") {
        // 削除ボタンをつける
        const deleteElement = document.createElement("button");
        deleteElement.classList.add("message-delete-btn");
        deleteElement.innerHTML = "<i class='fa-regular fa-trash-can'></i>";
        deleteElement.addEventListener("click", deleteChatMessage);
        speakerElement.appendChild(deleteElement);
    }
    else {
        // 再回答ボタンをつける
        if (g_aiAgentAvailable) {
            const retryElement = document.createElement("button");
            retryElement.classList.add("chat-reanswer-btn");
            retryElement.innerHTML = "<i class='fa-solid fa-rotate'></i>";
            retryElement.style.display = "none";
            retryElement.addEventListener("click", reAnswerChat);
            speakerElement.appendChild(retryElement);
        }
    }

    // メッセージテキストを表示する要素を作成
    const messageElement = document.createElement("div");
    messageElement.classList.add("message-text");
    if (role === "assistant") {
        let html = convertTextToHtmlWithMarkdown(messageText);
        html = escapeTex(html);
        html = adjustURL(html);
        html = marked.parse(html);
        html = unescapeTex(html);
        messageElement.innerHTML = html;
        messageElement.querySelectorAll("pre code").forEach((block) => {
            hljs.highlightElement(block);
        });
        addTargetBlank(messageElement);
        if (messageText === "") {
            messageElement.style.display = "none";
        }
    }
    else {
        messageElement.classList.add("mathjax_ignore");
        messageElement.innerHTML = escapeHtml(messageText);
    }

    // コードブロックにコピー用ボタンを追加
    addCopyToClipboardButton(messageElement);

    // チャットメッセージ要素に発言者名とメッセージテキストの要素を追加
    chatMessageElement.appendChild(speakerElement);
    chatMessageElement.appendChild(messageElement);

    // 作成したチャットメッセージをコンテナに追加
    chatMessagesContainer.appendChild(chatMessageElement);
}

// チャットメッセージのコードブロックにコピー用ボタンを追加する
function addCopyToClipboardButton(element) {
    element.querySelectorAll("pre").forEach((block) => {
        const button = document.createElement("button");
        button.innerHTML = "<i class='fa-regular fa-copy'></i>";
        button.className = "copy-button";

        const toast = document.createElement("div");
        toast.className = "code-toast";
        toast.textContent = getTextResource("textCopiedMessage");
        button.appendChild(toast);

        button.addEventListener("click", async () => {
            const code = block.querySelector("code");
            //await navigator.clipboard.writeText(code.textContent);
            await pywebview.api.copytext_to_clipboard(code.textContent);
            showCodeToast(toast);
        });

        block.appendChild(button);
    });    
}

// コードをクリップボードにコピーしたときのトーストを表示する
function showCodeToast(toast) {
    toast.classList.add('show');
    setTimeout(() => {
        toast.classList.remove('show');
    }, 2000);
}

// マークダウンテキスト内のコードブロックを保護しながらHTML変換する関数
function convertTextToHtmlWithMarkdown(text) {
    // コードブロックを一時保存
    let codeBlocks = [];
    text = text.replace(/```[\s\S]*?```/g, match => {
        codeBlocks.push(match);
        return `__CODE_BLOCK_${codeBlocks.length-1}__`;
    });

    // バッククォート文字を変換
    text = text.replace(/\\`/g, '\\\''); 

    // コードブロックを戻す
    codeBlocks.forEach((block, i) => {
        text = text.replace(`__CODE_BLOCK_${i}__`, block);
    });

    return text;
}

// markedがリンクに連続する文字列全体をリンクに変換してしまう問題に対処
function adjustURL(text) {
    // コードブロックを一時保存
    let codeBlocks = [];
    text = text.replace(/```[\s\S]*?```/g, match => {
        codeBlocks.push(match);
        return `__CODE_BLOCK_${codeBlocks.length-1}__`;
    });

    // https://またはhttp://では始まらない、www.で始まるドメイン名の前後にバッククォートを入れる
    text = text.replace(/(?<!https?:\/\/)(www\.[\w.]+)/g, " `$1` ");
    // https://またはhttp://で始まるURLの前後に半角スペースをいれる
    text = text.replace(/(https?:\/\/[\w.?=&%+#\/\-]+)/g, ' $1 ');

    // コードブロックを戻す
    codeBlocks.forEach((block, i) => {
        text = text.replace(`__CODE_BLOCK_${i}__`, block);
    });

    return text;
}

// 要素中の<a>タグにtarget="_blank"を設定する
function addTargetBlank(targetElement) {
    const links = targetElement.getElementsByTagName("a");
    for (let i = 0; i < links.length; i++) {
        if (!links[i].hasAttribute("target")) {
            links[i].setAttribute("target", "_blank");
            links[i].setAttribute("title", links[i].getAttribute("href"));
        }
    }
}

// 新規チャット開始
async function newChat() {
    // チャット要素を削除
    document.getElementById("chat-messages").innerHTML = "";

    // Python側に通知
    try {
        await pywebview.api.new_chat();
        addWelcome();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// ひとつ前のチャットに移動する
async function prevChat() {
    try {
        await pywebview.api.prev_chat();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// ひとつ後のチャットに移動する
async function nextChat() {
    try {
        await pywebview.api.next_chat();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// 現在表示しているチャットを削除する
async function deleteChat() {
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    if (messageTextElements.length === 0) return;

    if (!confirm(getTextResource("deleteConfirm"))) return;

    try {
        await pywebview.api.delete_current_chat();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// 設定ボタンが押された
async function settings() {
    try {
        await pywebview.api.move_to_settings();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// 印刷イベントハンドラ
function printDocument() {
    window.print();
}

// テキストを検索する
function searchText(query = "") {
    const searchText = prompt(getTextResource("searchPrompt"), query);
    if (searchText) {
        g_searchTextIndex = 0;
        var instance = new Mark(document.body);
        instance.unmark();
        instance.mark(searchText, {
            each: function(element) {
                // この中の処理は、見つかった各検索結果に対して実行される
            },
            done: function(totalMarks) {
                // 検索が完了した後に実行される処理
                g_searchTextTotal = totalMarks;
                highlightSearchResult(250);
            }
        });
    }
}

// テキスト検索で見つかったテキストのハイライト処理を行う
function highlightSearchResult(delay=0) {
    document.querySelectorAll("mark").forEach((element, index) => {
        if (index === g_searchTextIndex) {
            element.style.color = "red";
            element.style.backgroundColor = ""
            element.scrollIntoView({ behavior: "smooth" });
            setTimeout(() => {
                element.scrollIntoView({ behavior: "smooth" });
            }, delay);
        }
        else {
            element.style.color = "";
            element.style.backgroundColor = "khaki"
        }
    });    
}

// ファイル横断検索機能のエントリポイント
async function crossFileSearch() {
    try {
        await pywebview.api.move_to_cross_file_search();
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// メッセージの削除ボタンが押された
async function deleteChatMessage(event) {
    if (!confirm(getTextResource("deleteFromHereConfirm"))) return;

    hideChatRetryButton();

    let messageDiv = event.target.closest(".chat-message");
    let messageId = messageDiv.id;
    let messageIndex = parseInt(messageId.split("-")[1], 10);

    try {
        await pywebview.api.truncate_messages(messageIndex);
        g_nextMessageIndex = messageIndex;
        while (messageDiv.nextSibling) {
            messageDiv.nextSibling.remove();
        }
        messageDiv.remove();
    }
    catch (error) {
        console.error("Error: " + error)
    }

    showChatRetryButton();
}

// チャットの再回答ボタンが押された
async function reAnswerChat(event) {
    setSubmitButtonState(true);
    let messageDiv = event.target.closest(".chat-message");
    let messageId = messageDiv.id;
    let messageIndex = parseInt(messageId.split("-")[1], 10);
    messageDiv.remove();

    try {
        g_nextMessageIndex = messageIndex;
        await pywebview.api.ask_another_reply_to_chatgpt(messageIndex);
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// チャットの全メッセージのコピーイベントハンドラ
async function copyChatAllMessages() {
    try {
        const chatText = await pywebview.api.get_all_message_text();
        //navigator.clipboard.writeText(chatText);
        await pywebview.api.copytext_to_clipboard(chatText);
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// メッセージのコピーボタンが押された
async function copyChatMessage(event) {
    const button = event.currentTarget;

    let messageDiv = event.target.closest(".chat-message");
    let messageId = messageDiv.id;
    let messageIndex = parseInt(messageId.split("-")[1], 10);

    try {
        const messageText = await pywebview.api.get_message_text(messageIndex);
        //await navigator.clipboard.writeText(messageText);
        await pywebview.api.copytext_to_clipboard(messageText);
        showToast(event, getTextResource("messageCopiedMessage"));
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// チャットを要約する
async function summarizeChat(event) {
    try {
        showProgressModal(getTextResource("summarizingProgressMessage"));
        const summary = await pywebview.api.summarize_chat();
        hideProgressModal();

        if (summary) {
            //await navigator.clipboard.writeText(summary);
            await pywebview.api.copytext_to_clipboard(summary);
            showToast(event, getTextResource("summaryCopiedMessage"), ToastPosition.CenterScreen);
            showSummaryModal(summary);
        }
    }
    catch (error) {
        console.error("Error: " + error)
    }
}

// 要約モーダルを表示する
function showSummaryModal(summary) {
    const modal = document.getElementById("summary-modal");
    const content = document.getElementById("summary-modal-content");
    const closeButton = document.getElementById("summary-modal-close-button");

    if (modal && content && closeButton) {
        content.innerHTML = marked.parse(summary);
        closeButton.addEventListener("click", function() {
            hideSummaryModal();
        });
        modal.style.display = "block";
    }
}

// 要約モーダルを非表示にする
function hideSummaryModal() {
    const modal = document.getElementById("summary-modal");
    if (modal) {
        modal.style.display = "none";
    }
}

// トーストの表示位置
const ToastPosition = {
    ClickPos: "click-pos",
    CenterScreen: "center-screen"
};

// トーストを表示する
function showToast(event, message, position = ToastPosition.ClickPos, duration = 2000) {
    // トースト要素を作成
    const toast = document.createElement("div");
    toast.classList.add("toast");
    toast.textContent = message;

    // トーストをbodyに追加
    document.body.appendChild(toast);
    
    if (position === ToastPosition.ClickPos) {
        // クリック位置の右側に配置
        toast.style.left = `${Math.min(window.innerWidth - toast.offsetWidth, event.pageX + 16)}px`;
        toast.style.top = `${Math.min(window.innerHeight - toast.offsetHeight, event.pageY)}px`;
    }
    else {
        // デフォルトで画面中央に配置
        toast.style.left = `${(window.innerWidth - toast.offsetWidth) / 2}px`;
        toast.style.top = `${(window.innerHeight - toast.offsetHeight) / 2}px`;
    }
    
    // 2秒後に消える
    setTimeout(() => {
        toast.remove();
    }, duration);        
}

// Pythonから呼び出される関数
// カスタムCSSを設定する
function applyCustomCSS(css_js) {
    var el = document.createElement('style');
    el.textContent = css_js;
    document.head.appendChild(el);

    saveCSSValue();
}

// Pythonから呼び出される関数
// 情報をセットする
function setChatInfo(info) {
    g_userName = info.user.name;
    g_userColor = info.user.color;
    g_userIcon = info.user.icon;
    g_assistantName = info.assistant.name;
    g_assistantColor = info.assistant.color;
    g_assistantIcon = info.assistant.icon;
    g_speakerOn = info.system.speaker_on;
    g_nextMessageIndex = 0;
    g_welcomeTitle = info.settings.welcome_title;
    g_welcomeMessage = info.settings.welcome_message;
    g_aiAgentAvailable = info.chat.ai_agent_available;
    g_aiAgentCreationError = info.chat.ai_agent_creation_error;

    let displayName = info.settings.display_name;
    if (displayName === "") {
        displayName = info.assistant.name;
    }
    document.getElementById("settings-name").textContent = displayName;

    setSpeakerStateText();

    if (info.custom_style.enable) {
        setCustomStyleProperty("--background-image", info.custom_style.background_image);
        setCustomStyleProperty("--background-image-opacity", info.custom_style.background_image_opacity);
        setCustomStyleProperty("--body-bgcolor", info.custom_style.body_bgcolor);
        setCustomStyleProperty("--header-color", info.custom_style.header_color);
        setCustomStyleProperty("--welcome-title-color", info.custom_style.welcome_title_color);
        setCustomStyleProperty("--welcome-message-color", info.custom_style.welcome_message_color);
        setCustomStyleProperty("--speaker-name-text-shadow", info.custom_style.speaker_name_text_shadow);
        setCustomStyleProperty("--message-text-bgcolor", info.custom_style.message_text_bgcolor);
        setCustomStyleProperty("--message-text-color", info.custom_style.message_text_color);
        setCustomStyleProperty("--message-text-shadow", info.custom_style.message_text_shadow);
        setCustomStyleProperty("--message-text-border-radius", info.custom_style.message_text_border_radius);
        setCustomStyleProperty("--message-text-em-color", info.custom_style.message_text_em_color);

        if (info.custom_style.background_image) {
            setCustomStyleProperty("--container-bgcolor", "transparent");
            setCustomStyleProperty("--header-bgcolor", "transparent");
            setCustomStyleProperty("--chat-messages-bgcolor", "transparent");
        }
    }
    else {
        restoreCSSValue();
    }
}

function setCustomStyleProperty(prop, val) {
    val = trimCSSValue(val);
    const darkProp = "--dark-" + prop.slice(2);
    if (val) {
        document.documentElement.style.setProperty(prop, val);
        document.documentElement.style.setProperty(darkProp, val);
    }
    else {
        document.documentElement.style.setProperty(prop, getSavedCSSValue(prop));
        document.documentElement.style.setProperty(darkProp, getSavedCSSValue(darkProp));
    }
}

function trimCSSValue(str) {
    let s = str.trim();
    if (s.endsWith(';')) {
        s = s.slice(0, -1);
    }
    return s;
}

// Pythonから呼び出される関数
// AIからのチャット応答を開始する
function startResponse() {
    addChatMessage("assistant", g_assistantName, g_assistantColor, "");
    scrollToBottom();

    // アシスタント名のテキストを点滅させる
    const nameTextElements = document.querySelectorAll("#chat-messages .speaker-name");
    const lastNameTextElements = nameTextElements[nameTextElements.length - 1];
    if(lastNameTextElements) {
        lastNameTextElements.classList.add("flowing-text");
    }

    // 出力途中のテキストを表示するエリアを作成する
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];
    if(lastMessageTextElement) {
        const chunkArea = document.createElement("span");
        chunkArea.setAttribute("chunk-area", "true");
        lastMessageTextElement.appendChild(chunkArea);
    }
}

// Pythonから呼び出される関数
// AIからの応答（チャンク）を表示する
function addChunk(text) {
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];
    if(lastMessageTextElement) {
        lastMessageTextElement.style.display = "block";
    }

    const elms = document.querySelectorAll('[chunk-area="true"]');
    const chunkArea = elms[elms.length - 1];
    if (chunkArea) {
        chunkArea.innerHTML += escapeHtml(text);
        scrollToBottom();        
    }
}

// Pythonから呼び出される関数
// センテンスの読み上げが終わったときに呼び出される
function parsedSentence(sentence) {
    //MathJax.typesetPromise();
}

// Pythonから呼び出される関数
// 段落を受信したときに呼び出される
function parsedParagraph(paragraph) {
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];

    // チャンク出力領域を削除
    document.querySelectorAll('[chunk-area="true"]').forEach(e => e.remove());

    // 仮レンダリングして表示
    let html = marked.parse(paragraph);
    lastMessageTextElement.innerHTML += html;

    // チャンク出力領域を末尾に再作成
    const chunkArea = document.createElement("span");
    chunkArea.setAttribute("chunk-area", "true");
    lastMessageTextElement.appendChild(chunkArea);
}

// Pythonから呼び出される関数
// AIからのチャット応答が終了した
function endResponse(content) {
    setSubmitButtonState(false);
    showChatRetryButton();

    // アシスタント名の点滅を停止させる
    const nameTextElements = document.querySelectorAll("#chat-messages .speaker-name");
    const lastNameTextElements = nameTextElements[nameTextElements.length - 1];
    if(lastNameTextElements) {
        lastNameTextElements.classList.remove("flowing-text");
    }

    // チャンク出力領域を削除
    document.querySelectorAll('[chunk-area="true"]').forEach(e => e.remove());

    // コンテンツの内容をレンダリングして確定する
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];
    if(lastMessageTextElement) {
        lastMessageTextElement.style.display = "block";
        let html = convertTextToHtmlWithMarkdown(content);
        html = escapeTex(html);
        html = adjustURL(html);
        html = marked.parse(html);
        html = unescapeTex(html);
        lastMessageTextElement.innerHTML = html;
        lastMessageTextElement.querySelectorAll("pre code").forEach((block) => {
            hljs.highlightElement(block);
        });
        addTargetBlank(lastMessageTextElement);
        addCopyToClipboardButton(lastMessageTextElement);
    }

    MathJax.typesetPromise();

    // メッセージの先頭にスクロールする
    const lastUserMessageElement = messageTextElements[messageTextElements.length - 2];
    if (lastUserMessageElement) {
        const text = lastUserMessageElement.innerText;
        if (typeof text === "string") {
            const lineCount = text.split("\n").length;
            if (lineCount > 10) {
                scrollToMessage(1);
            }
            else {
                scrollToMessage(2);
            }
        }     
    }
}

// 任意位置のメッセージにスクロール（デフォ: 2番目から最後へ）
function scrollToMessage(offset = 2) {
    const messages = document.querySelectorAll(".chat-messages .chat-message");
    if (messages.length < offset) return;

    const secondLastMessage = messages[messages.length - offset];
    secondLastMessage.scrollIntoView({
        behavior: 'smooth',
        block: 'start'
    });
}

// Pythonから呼び出される関数
// チャット応答で例外が発生した
function handleChatException(message) {
    alert(message);
    endResponse();
}

// Pythonから呼び出される関数
// チャット応答で例外が発生した
async function handleChatTimeoutException(message) {
    if (confirm(`${message}\n` + getTextResource("retryConfirm"))) {
        const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
        const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];
        if (lastMessageTextElement) {
            lastMessageTextElement.textContent = "";
        }

        // Python側に通知
        try {
            await pywebview.api.retry_send_message_to_chatgpt();
        }
        catch (error) {
            console.error("Error: " + error)
        }
    }
    else {
        endResponse()
    }
}

// Pythonから呼び出される関数
// チャットのメッセージを再設定する
function setChatMessages(messages) {
    console.log(messages);
    document.getElementById("chat-messages").innerHTML = "";
    for (let message of messages) {
        let speakerName = "";
        let speakerColor = "";
        if (message.role === "assistant") {
            speakerName = g_assistantName;
            speakerColor = g_assistantColor;
        }
        else {
            speakerName = g_userName;
            speakerColor = g_userColor;
        }
        addChatMessage(message.role, speakerName, speakerColor, message.content);
    }
    MathJax.typesetPromise();
    scrollToBottom();
    showChatRetryButton();
}

// Pythonから呼び出される関数
// 指定されたメッセージに移動する
function moveToMessageAt(messageIndex, highlightText) {
    const element = document.getElementById(`message-${messageIndex}`);
    if (element) {
        element.scrollIntoView({ behavior: "smooth" });
        var instance = new Mark(document.body);
        instance.mark(highlightText);
    }
}

// 再回答ボタンをすべて非表示にする
function hideChatRetryButton() {
    const buttons = document.querySelectorAll(".chat-reanswer-btn");
    buttons.forEach((button, index) => {
        button.style.display = "none";
    });    
}

// 最後の再回答ボタンだけ表示する
function showChatRetryButton() {
    const buttons = document.querySelectorAll(".chat-reanswer-btn");
    buttons.forEach((button, index) => {
        if (index === buttons.length - 1) {
            button.style.display = "inline";
        }
    });
}

// Pythonから呼び出される関数
// リプレイ機能：メッセージブロック開始
function startReplayMessageBlock(role) {
    if (role === "assistant") {
        addChatMessage("replay_assistant", g_assistantName, g_assistantColor, "")
    }
    else {
        addChatMessage("replay_user", g_userName, g_userColor, "")
    }
    scrollToBottom();
}

// Pythonから呼び出される関数
// リプレイ機能：文章追加
function addReplayMessage(text) {
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];
    if(lastMessageTextElement) {
        lastMessageTextElement.innerHTML += escapeHtml(text);
        scrollToBottom();
    }
}

// Pythonから呼び出される関数
// リプレイ機能：メッセージブロック終了
function endReplayMessageBlock(content) {
    const messageTextElements = document.querySelectorAll("#chat-messages .message-text");
    const lastMessageTextElement = messageTextElements[messageTextElements.length - 1];
    if(lastMessageTextElement) {
        let html = convertTextToHtmlWithMarkdown(content);
        html = escapeTex(html);
        html = adjustURL(html);
        html = marked.parse(html);
        html = unescapeTex(html);
        lastMessageTextElement.innerHTML = html;
        lastMessageTextElement.querySelectorAll("pre code").forEach((block) => {
            hljs.highlightElement(block);
        });
        addTargetBlank(lastMessageTextElement);
    }
    MathJax.typesetPromise();
}

// 処理中モーダルを表示する
function showProgressModal(message) {
    const modal = document.getElementById("progress-modal");
    const messageEl = document.getElementById("progress-modal-message");
    messageEl.textContent = message;
    modal.style.display = "block";
}

// 処理中モーダルを非表示にする
function hideProgressModal() {
    const modal = document.getElementById("progress-modal");
    modal.style.display = "none";
}

// Pythonから呼び出される関数（グローバルスコープに登録）
window.applyCustomCSS = applyCustomCSS;
window.setChatInfo = setChatInfo;
window.startResponse = startResponse;
window.addChunk = addChunk;
window.parsedSentence = parsedSentence;
window.parsedParagraph = parsedParagraph;
window.endResponse = endResponse;
window.handleChatException = handleChatException;
window.handleChatTimeoutException = handleChatTimeoutException;
window.setChatMessages = setChatMessages;
window.moveToMessageAt = moveToMessageAt;
window.newChat = newChat;
window.startReplayMessageBlock = startReplayMessageBlock;
window.addReplayMessage = addReplayMessage;
window.endReplayMessageBlock = endReplayMessageBlock;
window.showProgressModal = showProgressModal;
window.hideProgressModal = hideProgressModal;
