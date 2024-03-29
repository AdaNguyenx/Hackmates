/**
 * django-notify-x.
 */

// Variable declaration;

// AJAX call URLs
var updateNotificationUrl;
var markNotificationUrl;
var markAllNotificationUrl;
var deleteNotificationUrl = '/notifications/delete';

// Class selectors
var nfListClassSelector;
var nfClassSelector;
var nfBoxListClassSelector;
var nfBoxClassSelector;
var nfListSelector = nfBoxListClassSelector + ", " + nfListClassSelector;
var nfSelector = nfClassSelector + ", " + nfBoxClassSelector;

var markNotificationSelector;
var markAllNotificationSelector;
var deleteNotificationSelector = '.delete-notification';

// Class details
var readNotificationClass;
var unreadNotificationClass;

// Ajax success functions.
var markSuccess;
var markAllSuccess;
var deleteSuccess;
var updateSuccess;

var notificationUpdateTimeInterval;

// Django's implementation for AJAX-CSRF protection.
// https://docs.djangoproject.com/en/dev/ref/csrf/#ajax
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
var csrftoken = getCookie('csrftoken');

function csrfSafeMethod(method) {
    // these HTTP methods do not require CSRF protection
    return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
}

function sameOrigin(url) {
    // test that a given url is a same-origin URL
    // url could be relative or scheme relative or absolute
    var host = document.location.host; // host + port
    var protocol = document.location.protocol;
    var sr_origin = '//' + host;
    var origin = protocol + sr_origin;
    // Allow absolute or scheme relative URLs to same origin
    return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
        (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
        !(/^(\/\/|http:|https:).*/.test(url));
}

$.ajaxSetup({
    beforeSend: function (xhr, settings) {
        if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
            // Send the token to same-origin, relative URLs only.
            // Send the token only if the method warrants CSRF protection
            // Using the CSRFToken value acquired earlier
            xhr.setRequestHeader("X-CSRFToken", csrftoken);
        }
    }
});


// Delete a notification using AJAX.
$(document).ready(function () {

    //$(deleteNotificationSelector).on('click', function () {
    $(nfListSelector).delegate(deleteNotificationSelector, 'click', function () {
        var $notification = $(this);

        var delete_notification_data = {
            id: $notification.attr('data-id'),
            csrftoken: csrftoken
        };

        $.ajax({
            type: 'POST',
            url: deleteNotificationUrl,
            data: delete_notification_data,
            //success: deleteSuccess(response)
            success: function (response) {
                deleteSuccess(response, $notification);
            }
        });
    });
});

$(".mark-notification").click(function () {
    
});