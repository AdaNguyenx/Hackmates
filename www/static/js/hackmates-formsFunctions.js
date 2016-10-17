// Function to submit form for creating a team
var team_form = $('#team_form');
team_form.submit(function () {
    var dataArray = team_form.serializeArray(),
        len = dataArray.length,
        dataObj = {};

    for (i = 0; i < len; i++) {
        dataObj[dataArray[i].name] = dataArray[i].value;
    }

    if (!dataObj['name'] || !dataObj['hackathon']) {
        $(".errorteamform").html("Please create a team name or select a hackathon");
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/',
        data: team_form.serialize(),
        success: function (data) {
            var boolean = JSON.stringify(data["error"]);

            if (boolean === "true") {
                $(".errorteamform").html("This team name is already taken");
            }
            else if (boolean === "false") {
                $('.createATeam').modal('hide');
                $('.createATeamSuccess').modal('show');
            }
        },
        error: function (data) {
            $("#team_form").html("Something went wrong :( Please refresh the page and try again.");
        }
    });
    return false;
});

// Function to submit form for sending message to a team
$(".sendTeamButton").click(function () {
    
    var the_team = $(this).parent().attr('id');
    var team_send_data = {
        team: the_team,
        teamsendform: 'teamsendform',
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

    $.ajax({
        type: 'POST',
        url: '/',
        data: team_send_data,
        //success: deleteSuccess(response)
        success: function (data) {
            var the_team = JSON.stringify(data["the_team"]);
            $('.thisIsTeam').html(JSON.parse(the_team));
            $('#sendTeamMessageModal').modal('show');
        }

    });
});

// Function to remove a member from a team
$(".removeTheUser").click(function () {
    console.log("yes");
    var removed_user = $(this).attr('id');
    var team_removed_from = $(this).attr('team-of-the-user');
    $('.removeTheHackMateButton').attr('id', removed_user);
    $('.removeTheHackMateButton').attr('team-of-the-user', team_removed_from);
    $('#removeUserModal').modal('show');


});

$('.removeTheHackMateButton').click(function () {
    var removed_user_bttn = $(this).attr('id');
    var team_removed_from_bttn = $(this).attr('team-of-the-user');

    var remove_the_hackmate_data = {
        removehackmateform: 'removehackmateform',
        remove_user: removed_user_bttn,
        remove_team: team_removed_from_bttn,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

    $.ajax({
        type: 'POST',
        url: '/',
        data: remove_the_hackmate_data,
        success: function (data) {
            var success_removed_user = JSON.stringify(data["removed_user"]);
            var success_removed_team = JSON.stringify(data["removed_team"]);
            $('.thisIsSuccessRemoveUser').html(JSON.parse(success_removed_user));
            $('.thisIsSuccessRemoveTeam').html(JSON.parse(success_removed_team));
            $('#removeUserModal').modal('hide');
            $('#removeUserSuccessModal').modal('show');
        }
    });

});


// Reload modals when created new team and when deleting someone
$('#removeUserSuccessModal').on('hidden.bs.modal', function () {
    location.reload();
});

$('.createATeamSuccess').on('hidden.bs.modal', function () {
     location.reload();
});

