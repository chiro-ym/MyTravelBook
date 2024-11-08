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
                console.log("Data chunk added:", event.data);  // デバッグ用: データ取得を確認
            });

            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;

                console.log("Audio blob created:", audioBlob);  // デバッグ用: Blob作成を確認

                // 音声データをBase64に変換してフォームに追加
                const reader = new FileReader();
                // audioRecorder.js の録音停止後に追加
            reader.onloadend = () => {
            audioDataInput.value = reader.result; // Base64データをセット
            updateSubmitButtonState();  // ボタンの有効化を更新
            console.log("Base64 audio data set:", reader.result);  // デバッグ用: Base64データを確認
            };

                reader.readAsDataURL(audioBlob); // Base64エンコード
            });

            mediaRecorder.start();
            console.log("Recording started...");  // デバッグ用: 録音開始を確認
            recordBtn.disabled = true;
            stopBtn.disabled = false;   
        } catch (error) {
            alert("マイクのアクセスに失敗しました。設定をご確認ください。");
            console.error("Error accessing microphone:", error);  // エラー内容をコンソールに出力
        }
    });

    stopBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            recordBtn.disabled = false;
            stopBtn.disabled = true;
            console.log("Recording stopped.");  // デバッグ用: 録音停止を確認
        }
    });
});

