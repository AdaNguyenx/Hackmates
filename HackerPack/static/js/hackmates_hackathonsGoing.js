function getHackathonFunction(id) {
    var going_hackathon = {
        goinghackathonform: 'goinghackathonform',
        hackathon_id: id,
        csrfmiddlewaretoken: csrfmiddlewaretoken
    };

    $.ajax({
        type: 'POST',
        url: '/',
        data: going_hackathon,
        success: function (data) {
            // var boolean = JSON.stringify(data["error"]);
            //
            // if (boolean === "true") {
            //     $(".errorteamform").html("This team name is already taken");
            // }
            // else if (boolean === "false") {
            //     $('.createATeam').modal('hide');
            //     $('.createATeamSuccess').modal('show');
            // }
        },
        error: function (data) {
            // $("#team_form").html("Something went wrong :( Please refresh the page and try again.");
        }
    });
    return false;
}