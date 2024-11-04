document.addEventListener('DOMContentLoaded', function() {
    let mediaRecorder;
    let audioChunks = [];

    const recordBtn = document.getElementById('record-btn');
    const stopBtn = document.getElementById('stop-btn');
    const audioPlayback = document.getElementById('audio-playback');

    // 録音開始ボタンのイベントリスナー
    recordBtn.addEventListener('click', async () => {
        try {
            // マイクの使用許可を求める
            const stream = await navigator.mediaDevices.getUserMedia({ audio: true });
            mediaRecorder = new MediaRecorder(stream);

            // 録音データを格納する配列をリセット
            audioChunks = [];

            // 音声データが得られるたびに配列に追加
            mediaRecorder.addEventListener('dataavailable', event => {
                audioChunks.push(event.data);
            });

            // 録音終了時に音声データをBlobとして作成し、再生可能にする
            mediaRecorder.addEventListener('stop', () => {
                const audioBlob = new Blob(audioChunks, { type: 'audio/mp3' });
                const audioUrl = URL.createObjectURL(audioBlob);
                audioPlayback.src = audioUrl;

                // ここで音声ファイルをサーバーに送信する処理も追加可能
                // 例: sendAudioToServer(audioBlob);
            });

            mediaRecorder.start();
            recordBtn.disabled = true;
            stopBtn.disabled = false;
            console.log("録音を開始しました");
        } catch (error) {
            console.error("録音エラー:", error);
            alert("マイクのアクセスに失敗しました。設定をご確認ください。");
        }
    });

    // 録音停止ボタンのイベントリスナー
    stopBtn.addEventListener('click', () => {
        if (mediaRecorder && mediaRecorder.state !== "inactive") {
            mediaRecorder.stop();
            recordBtn.disabled = false;
            stopBtn.disabled = true;
            console.log("録音を停止しました");
        }
    });
});