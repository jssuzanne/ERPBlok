function makeNotification(title, options) {
    // Let's check if the browser supports notifications
    if (!("Notification" in window)) {
        console.warn("This browser does not support desktop notification");
    }
    // Let's check if the user is okay to get some notification
    else if (Notification.permission === "granted") {
        // If it's okay let's create a notification
        var notification = new Notification(title, options);
    }
    // Otherwise, we need to ask the user for permission
    else if (Notification.permission !== 'denied') {
        Notification.requestPermission(function (permission) {
        // If the user is okay, let's create a notification
            if (permission === "granted") {
                var notification = new Notification(title, options);
            }
        });
    }
}

function notify(title, body, icon) {
    options = {
        body: body,
    };
    if (icon != undefined) {
        options.icon = icon;
    }
    makeNotification(title, options);
}

function notify_ok(title, body) {
    notify(title, body, '/erpblok-web-client/static/notification/ok.png');
}

function notify_warn(title, body) {
    notify(title, body, '/erpblok-web-client/static/notification/warn.png');
}

function notify_error(title, body) {
    notify(title, body, '/erpblok-web-client/static/notification/error.png');
}
