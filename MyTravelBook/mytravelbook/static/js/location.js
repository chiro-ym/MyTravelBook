const locationField = document.getElementById('memo_location'); // 新しい位置情報のフィールドを取得
const latitudeField = document.getElementById('latitude');
const longitudeField = document.getElementById('longitude');

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition( //位置情報を取得
            (position) => {  // 成功した場合
                latitudeField.value = position.coords.latitude;
                longitudeField.value = position.coords.longitude;
                locationField.value = `Latitude: ${position.coords.latitude}, Longitude: ${position.coords.longitude}`;
            },
            (error) => {  // エラーが発生した場合
                console.error("位置情報の取得に失敗しました:", error);
                alert("位置情報の取得が許可されていない可能性があります。設定を確認してください。");
            }
        );
    } else {
        alert("お使いのブラウザは位置情報取得に対応していません。");
    }
}

document.addEventListener('DOMContentLoaded', getLocation);
