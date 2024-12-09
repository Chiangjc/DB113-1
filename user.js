
function getCookie(name) {
    const cookieArr = document.cookie.split(';');
    for (let i = 0; i < cookieArr.length; i++) {
        let cookie = cookieArr[i].trim();
        if (cookie.startsWith(name + '=')) {
            return cookie.substring(name.length + 1);
        }
    }
    return null;  // 如果cookie找不到，返回null
}

function displayUsername() {
    const username = getCookie('username');
    console.log(username);  // 將用戶名記錄到控制台
    if (username) {
        document.getElementById('user_name').textContent = username;
        document.getElementById('user_name_display').textContent = username;
    } else {
        document.getElementById('user_name').textContent = 'Welcome!';
        document.getElementById('user_name_display').textContent = 'Welcome!';
    }
}

// 在頁面加載時調用displayUsername
window.onload = displayUsername;

