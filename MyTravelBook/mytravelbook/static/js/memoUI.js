const memoText = document.getElementById('memo_text');
const photoInput = document.querySelector('input[name="memo_photo_path"]');
const audioDataInput = document.getElementById('audio-data');
const submitBtn = document.getElementById('submit-btn');

function updateSubmitButtonState() {
    submitBtn.disabled = !(
        memoText.value.trim() || 
        photoInput.files.length > 0 || 
        audioDataInput.value
    );
}

memoText.addEventListener('input', updateSubmitButtonState);
photoInput.addEventListener('change', updateSubmitButtonState);
