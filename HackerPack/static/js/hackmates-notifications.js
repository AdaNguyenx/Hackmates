var deleteNotificationUrl = '/notifications/delete/';

var deleteSuccess = function (response, notification) {

    var $selected_notification = notification.closest('nf-');
    $selected_notification.fadeOut(300, function () {
        $(this).remove()
    });
};

// {# Mark notifications as read/ Accept request #}
$(".c-notifications-box").on("click", ".mark-notification", function () {
    var $notification = $(this);
    var mark_action = $notification.attr('data-mark-action');

    var team = $notification.attr('data-team');
    var sender = $notification.attr('data-sender');
    var id = $notification.attr('data-id');

    var mark_post_data = {
        sender: sender,
        team: team,
        id: id,
        action: mark_action,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

    var remove_id = "#nf-" + id;

    $.ajax({
        type: 'POST',
        url: '/',
        data: mark_post_data,
        success: function (response) {
            $(remove_id).fadeOut(300, function () {
                $(this).remove();
                var number_notifications = $("li[class*='notification']").length;
                if (number_notifications) {
                    $('.badge-notify').html(number_notifications);
                }
                else {
                    $('.badge-notify').html('');
                    $('.c-notifications-box').html('<b> No notifications yet. </b>')
                }
            });
            location.reload();
        }
    });
});

// {# Delete notification/ Deny request #}
$(".c-notifications-box").on("click", ".delete-notification", function () {
    var $notification = $(this);
    var id = $notification.attr('data-id');

    var delete_notification_data = {
        id: $notification.attr('data-id'),
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

    var remove_id = "#nf-" + id;

    $.ajax({
        type: 'POST',
        url: deleteNotificationUrl,
        data: delete_notification_data,
        success: function (response) {
            $(remove_id).fadeOut(300, function () {
                $(this).remove();
                var number_notifications = $("li[class*='notification']").length;
                if (number_notifications) {
                    $('.badge-notify').html(number_notifications);
                }
                else {
                    $('.badge-notify').html('');
                    $('.c-notifications-box').html('<b> No notifications yet. </b>')
                }
            });
            location.reload();
        }
    });
});

