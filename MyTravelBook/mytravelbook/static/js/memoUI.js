const memoText = document.getElementById('memo_text');
const photoInput = document.getElementById('photo-input');
const audioDataInput = document.getElementById('audio-data');
const submitBtn = document.getElementById('submit-btn');
const photoPreview = document.getElementById('photo-preview');
const previewImage = document.getElementById('preview-image');
// 録音関連
const recordBtn = document.getElementById('record-btn');
const stopBtn = document.getElementById('stop-btn');
const audioPlayback = document.getElementById('audio-playback');
let mediaRecorder;
let audioChunks = [];
let stream;
let isRecording = false;

// 録音開始・停止ボタン
recordBtn.addEventListener('click', async () => {
    if (isRecording) {
        mediaRecorder.stop();
        recordBtn.textContent = '録音開始';
        stopBtn.style.display = 'none';
    } else {
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

                const reader = new FileReader();
                reader.onloadend = () => {
                    audioDataInput.value = reader.result;  // Base64データをフォームにセット
                    updateSubmitButtonState();  // ボタンの状態更新
                };
                reader.readAsDataURL(audioBlob);
            });

            mediaRecorder.start();
            recordBtn.textContent = '録音停止';
            stopBtn.style.display = 'inline-block';  // 停止ボタンを表示
        } catch (error) {
            alert("マイクのアクセスに失敗しました。設定をご確認ください。");
            console.error("Error accessing microphone:", error);
        }
    }
    isRecording = !isRecording;
});

// 録音停止ボタン
stopBtn.addEventListener('click', () => {
    if (mediaRecorder && isRecording) {
        mediaRecorder.stop();  // 録音を停止
        recordBtn.textContent = '録音開始';  // ボタンを元に戻す
        recordingStatus.style.display = 'none';  // 録音中メッセージを非表示
        stopBtn.disabled = true;  // 停止ボタンを無効化
    }
});

function updateSubmitButtonState() {
    submitBtn.disabled = !(
        memoText.value.trim() || 
        photoInput.files.length > 0 || 
        audioDataInput.value
    );
}

// 写真プレビュー
function updatePhotoPreview() {
    const file = photoInput.files[0];
    if (file) {
        const reader = new FileReader();
        reader.onload = function (e) {
            previewImage.src = e.target.result;
            previewImage.style.display = 'block';
        };
        reader.readAsDataURL(file);
        previewImage.src = '';
        previewImage.style.display = 'none';
    }
}

memoText.addEventListener('input', updateSubmitButtonState);
photoInput.addEventListener('change', () => {
    updatePhotoPreview(); 
    updateSubmitButtonState();
});
