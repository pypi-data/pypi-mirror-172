function getCookie(name) {
    var cookieValue = null;
    if (document.cookie && document.cookie != '') {
        var cookies = document.cookie.split(';');
        for (var i = 0; i < cookies.length; i++) {
            var cookie = jQuery.trim(cookies[i]);
            // Does this cookie string begin with the name we want?
            if (cookie.substring(0, name.length + 1) == (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

function loginWithSSSSignature(payload, login_url, onLoginRequestError, onLoginSuccess, onLoginFail) {
    var request = new XMLHttpRequest();
    request.open('POST', login_url, true);
    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            // Success!
            console.log("success to send payload")
            var resp = JSON.parse(request.responseText);
            console.log(resp)
            if (resp.success) {
                if (typeof onLoginSuccess == 'function') {
                    onLoginSuccess(resp);
                }
            } else {
                if (typeof onLoginFail == 'function') {
                    onLoginFail(resp);
                }
            }
        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status);
            if (typeof onLoginRequestError == 'function') {
                onLoginRequestError(request);
            }
        }
    };

    request.onerror = function () {
        console.log("Autologin failed - there was an error");
        if (typeof onLoginRequestError == 'function') {
            onLoginRequestError(request);
        }
        // There was a connection error of some sort
    };
    request.setRequestHeader('Content-Type', 'application/x-www-form-urlencoded; charset=UTF-8');
    request.setRequestHeader("X-CSRFToken", getCookie('csrftoken'));
    const formData = 'payload=' + window.SSS.activePublicKey + payload;
    request.send(formData);
}

function checkSSS(callback) {
    const publicKey = window.SSS.activePublicKey;
    callback(publicKey.length===64)
}

function SSSLogin(login_url, onTokenRequestFail, onTokenSignFail, onTokenSignSuccess, // used in this function
onLoginRequestError, onLoginFail, onLoginSuccess) {
    var request = new XMLHttpRequest();
    request.open('GET', login_url, true);

    request.onload = function () {
        if (request.status >= 200 && request.status < 400) {
            var resp = JSON.parse(request.responseText);
            var token = resp.data;
            console.log("Token: " + token);
            window.SSS.getActiveAccountToken(
                token).then((payload)=>{
                    //暗号化メッセージ取得
                    console.log("payload:",payload);
                    console.log(typeof(onLoginSuccess))
                    loginWithSSSSignature(payload, login_url ,onLoginRequestError, onLoginSuccess, onLoginFail);
                }).catch((e)=>{
                    //取得失敗(タイムアウトを含む)
                    console.log("error:",e);
                    alert(e);
            });

        } else {
            // We reached our target server, but it returned an error
            console.log("Autologin failed - request status " + request.status);
            if (typeof onTokenRequestFail == 'function') {
                onTokenRequestFail(request);
            }
        }
    };

    request.onerror = function () {
        // There was a connection error of some sort
        console.log("Autologin failed - there was an error");
        if (typeof onTokenRequestFail == 'function') {
            onTokenRequestFail(request);
        }
    };
    request.send();
}



