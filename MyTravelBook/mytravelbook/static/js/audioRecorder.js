document.addEventListener('DOMContentLoaded', function() {
    let mediaRecorder;
    let audioChunks = [];
    let stream;

    const recordBtn = document.getElementById('record-btn');
    const stopBtn = document.getElementById('stop-btn');
    const audioPlayback = document.getElementById('audio-playback');
    const audioDataInput = document.getElementById('audio-data');
    const submitBtn = document.getElementById('submit-btn');

    recordBtn.addEventListener('click', async () => {
        if (!navigator.mediaDevices || !navigator.mediaDevices.getUserMedia) {
            alert("このブラウザは音声録音をサポートしていません");
            return;
        }

        try {
            stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);
            audioChunks = [];

            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;

                // 音声データをBase64に変換してフォームに追加
                const reader = new FileReader();
                reader.onloadend = () => {
                    audioDataInput.value = reader.result; // Base64データをセット
                    submitBtn.disabled = false; // 録音完了後に送信ボタンを有効にする
                };
                reader.readAsDataURL(audioBlob); // Base64エンコード
            });

            mediaRecorder.start();
            recordBtn.disabled = true;
            stopBtn.disabled = false;   
        } catch (error) {
            alert("マイクのアクセスに失敗しました。設定をご確認ください。");
        }
    });

    stopBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            recordBtn.disabled = false;
            stopBtn.disabled = true;
        }
    });
});
