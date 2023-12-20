// ==UserScript==
// @name         Send Cookies to Server
// @namespace    http://tampermonkey.net/
// @version      0.1
// @description  Send cookies to local server
// @author       YourName
// @match        *://*.v2ex.com/*
// @grant        GM_xmlhttpRequest
// ==/UserScript==

(function() {
    'use strict';

    function sendCookies() {
        GM_xmlhttpRequest({
            method: "POST",
            url: "http://127.0.0.1:5000/receive_cookies", // 确保 URL 和端口与 Flask 服务器匹配
            headers: {"Content-Type": "application/json"},
            data: JSON.stringify({ cookies: document.cookie }),
            onload: function(response) {
                console.log("Cookies sent successfully", response.responseText);
            },
            onerror: function(error) {
                console.error("Error sending cookies", error);
            }
        });
    }

    // 每10分钟发送一次Cookies
    setInterval(sendCookies, 10 * 60 * 1000);
    // 初始启动时也发送一次
    sendCookies();
})();
