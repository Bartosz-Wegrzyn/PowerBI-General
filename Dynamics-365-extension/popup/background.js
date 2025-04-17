chrome.runtime.onMessage.addListener((message, sender, sendResponse) => {
    if (message.type === 'navigate') {
        chrome.tabs.create({ url: message.url });
    }
});
