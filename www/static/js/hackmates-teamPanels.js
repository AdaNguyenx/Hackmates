var userTeamPanel = document.getElementById("userTeamPanel");
var teammember_id = 0;
var teammember_count = 0;


function createTeamPanel() {
    var DOWN_ARROW = "https://s3.amazonaws.com/hack-mates/static/images/down-arrow.png";
    var UP_ARROW = "https://s3.amazonaws.com/hack-mates/static/images/up-arrow.png";

    var html_teammember_hackathons = '<p> <b> Going to: </b> ' + teammember_hackathons.toString() + '</p>';
    var html_teammember_about = '<p> <b> About: </b> ' + teammember_about + '</p>';
    var html_teammember_city = '<p> <b> Location: </b> ' + teammember_city + '</p>';
    var html_teammember_school = '<p> <b> School: </b> ' + teammember_school + '</p>';
    var html_teammember_studies = '<p> <b> Studies: </b> ' + teammember_studies + '</p>';
    var html_teammember_interests = '<p> <b> Interests: </b> ' + teammember_interests + '</p>';

    var idString = "id=" + teammember_id;
    var tempString = "<div class='col-md-4'" + ">" +
        "<div class='panel panel-default panel-cus center-block' onclick='changeArrow(" +
        teammember_id + ")'" + idString + ">" +
        "<div class='custom-panel center-block' data-toggle='collapse'" +
        "data-target='#team_lower" + teammember_id + "'>" +
        "<img src ='" + teammember_imagesrc + "' class='img-responsive center-block user-image'>" +
        "<div class = 'carousel-caption'>" + "<h1>" +
        teammember_first_name + "</h1>"
        + '<img src = ' + DOWN_ARROW + ' class="img-responsive center-block arrow-image" id = "arrow'
        + teammember_id + '">'
        + "</div>" + "</div>" +
        "<div id = 'team_lower" + teammember_id + "' class = 'collapse' style='padding:15px;'>" +
        html_teammember_hackathons + html_teammember_about + html_teammember_city +
        html_teammember_school + html_teammember_studies + html_teammember_interests +
        '<button class = "btn btn-danger center-block removeTheUser" id = "' + teammember_username +
        '"' + 'team-of-the-user =' + team_id + '> Remove from team </button>' +
        "</div>" + "</div>" + "</div>";

    var teammember_newFeature = document.createElement('div');
    teammember_newFeature.innerHTML = tempString;

    if (teammember_count % 3 === 0) {
        var teammember_newRow = document.createElement('div');
        teammember_newRow.className = 'row';
        teamName.appendChild(teammember_newRow);
        teammember_newRow.appendChild(teammember_newFeature);
        teammember_oldRow = teammember_newRow;
    }
    else {
        teammember_oldRow.appendChild(teammember_newFeature);
    }
    teammember_count++;
}