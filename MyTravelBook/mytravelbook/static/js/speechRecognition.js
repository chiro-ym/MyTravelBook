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
    const memoTextInput = document.getElementById('memo_text');

    btn.addEventListener('click', function() {
        speech.start();
    });

    speech.addEventListener('result', function(e) {
        const transcript = e.results[0][0].transcript;
        memoTextInput.value = transcript;
        // 手動でinputイベントを発火して送信ボタンを有効化
        memoTextInput.dispatchEvent(new Event('input'));
    });

    speech.addEventListener('error', function(e) {
        alert("音声認識のエラーが発生しました。マイクの設定をご確認ください。");
    });

    speech.addEventListener('end', function() {
        console.log("音声認識が終了しました");
    });
});
