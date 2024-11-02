document.addEventListener('DOMContentLoaded', function() {
    if (!window.webkitSpeechRecognition) {
        alert("このブラウザでは音声認識がサポートされていない可能性があります。");
        return;
    }

    const speech = new webkitSpeechRecognition();
    speech.lang = 'ja-JP';
    speech.interimResults = true;
    speech.continuous = false;

    const btn = document.getElementById('btn');
    const content = document.getElementById('content');
    const memoTextInput = document.getElementById('memo_text');

    btn.addEventListener('click', function() {
        speech.start();
    });

    speech.addEventListener('result', function(e) {
        const transcript = e.results[0][0].transcript;
        content.textContent = transcript;
        memoTextInput.value = transcript;
    });

    speech.addEventListener('error', function(e) {
        alert("音声認識のエラーが発生しました。マイクの設定をご確認ください。");
    });

    speech.addEventListener('end', function() {
        console.log("音声認識が終了しました");
    });
});
