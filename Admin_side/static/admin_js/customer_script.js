// Ensure this script is only included once
if (!window.csrfTokenInitialized) {
    window.csrfTokenInitialized = true;

    // Function to get the CSRF token from the cookies
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie !== '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = cookies[i].trim();
                if (cookie.substring(0, name.length + 1) === (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }

    const csrftoken = getCookie('csrftoken');

    // Function to block a user
    function blockUser(userId) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/administration/block/' + userId + '/', true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        var button = document.querySelector(`#block-unblock-btn-${userId}`);
                        if (button) {
                            button.textContent = "Unblock";
                            button.className = "unblock_btn";
                            button.setAttribute('onclick', `unblockUser(${userId})`);
                        }
                    }
                } else {
                    console.error(xhr.responseText);
                }
            }
        };

        xhr.send();
    }

    // Function to unblock a user
    function unblockUser(userId) {
        var xhr = new XMLHttpRequest();
        xhr.open('POST', '/administration/unblock/' + userId + '/', true);
        xhr.setRequestHeader('X-CSRFToken', csrftoken);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function() {
            if (xhr.readyState === 4) {
                if (xhr.status === 200) {
                    var response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        var button = document.querySelector(`#block-unblock-btn-${userId}`);
                        if (button) {
                            button.textContent = "Block";
                            button.className = "block_btn";
                            button.setAttribute('onclick', `blockUser(${userId})`);
                        }
                    }
                } else {
                    console.error(xhr.responseText);
                }
            }
        };

        xhr.send();
    }
}

