// Show form
function showFunction(id) {
    $('#form-invited').attr('value', String(id))
}

// Function to create dynamic panels
var users_panel = document.getElementById('users-panel');
var count = 0;
var oldRow = document.createElement('div');
oldRow.className = 'row';


// The same as the function in userPanel.js, but add this button in the panel
// <button class = "btn btn-primary big-register"
//                               id = "jaime5"
//                               data-toggle="modal" data-target="#myModal"
//                               onclick="showFunction(this.id);"> Team Up </button>
function createPanel() {

    var DOWN_ARROW = "https://s3.amazonaws.com/hack-mates/static/images/down-arrow.png";
    var UP_ARROW = "https://s3.amazonaws.com/hack-mates/static/images/up-arrow.png";

    var idString = "id=" + id;
    var tempString = "<div class='col-md-4'" + ">" +
        "<div class='panel panel-default panel-cus center-block' onclick='changeArrow(" +
        id + ")'" + idString + ">" +
        "<div class='custom-panel center-block' data-toggle='collapse'" +
        "data-target='#lower" + id + "'>" +
        "<img src ='" + imagesrc + "' class='img-responsive center-block user-image'>" +
        "<div class = 'carousel-caption'>" + "<h1>" +
        first_name + "</h1>"
        + '<img src = "' + DOWN_ARROW
        + '" class="img-responsive center-block arrow-image" id ="arrow'
        + id + '">'
        + "</div>" + "</div>" +
        "<div id = 'lower" + id + "' class = 'collapse' style='padding:15px;'>" +
        html_fb_link + html_hackathons + html_school + html_about +
        html_ideas  + html_roles + html_languages  + html_frameworks +
        '<button class = "btn btn-primary big-register center-block" id = "' + username +
        '"' + ' data-toggle="modal" data-target="#myModal"' +
        ' onclick="showFunction(this.id);"> Team Up </button>' +
        "</div>" + "</div>" + "</div>";

    var newFeature = document.createElement('div');
    newFeature.innerHTML = tempString;

    if (count > 5) {
        newFeature.setAttribute('style', 'display:none;');
        newFeature.className = 'hiding';
    }

    if (count % 3 === 0) {
        var newRow = document.createElement('div');
        newRow.className = 'row';
        users_panel.appendChild(newRow);
        newRow.appendChild(newFeature);
        oldRow = newRow;
    }
    else {
        oldRow.appendChild(newFeature);
    }
    count++;
}


// Change the arrow direction depending on whether the content is collapsed or not
function changeArrow(id) {
    var DOWN_ARROW = "https://s3.amazonaws.com/hack-mates/static/images/down-arrow.png";
    var UP_ARROW = "https://s3.amazonaws.com/hack-mates/static/images/up-arrow.png";

    idPanel = String('#lower' + id);
    idArrow = String('arrow' + id);

    $(idPanel).on('shown.bs.collapse', function () {
        document.getElementById(idArrow).src = UP_ARROW;
    });
    $(idPanel).on('hide.bs.collapse', function () {
        document.getElementById(idArrow).src = DOWN_ARROW;
    });
}


// Function for load more button
$(function () {
    var hidingCount = 6;
    $("#load").click(function (e) { // click event for load more
        e.preventDefault();
        $(".hiding").slice(hidingCount - 6, hidingCount).show();
        hidingCount += 6;
        if (hidingCount >= num) {
            $("#load").hide()
        }
    });
});

$('#mydiv').children('input').each(function () {
    alert(this.value); // "this" is the current element in the loop
});

// Function to process form submission for team request
var frm = $('#post-form');
frm.submit(function () {
    var dataArray = frm.serializeArray(),
        len = dataArray.length,
        dataObj = {};

    for (i = 0; i < len; i++) {
        dataObj[dataArray[i].name] = dataArray[i].value;
    }

    if (!dataObj['invite-teams']) {
        $("#errorform").html("Please choose a team to invite this HackMate to");
        return false;
    }

    $.ajax({
        type: 'POST',
        url: '/',
        data: frm.serialize(),
        success: function (data) {
            // $("#SOME-DIV").html(data);
            var boolean = JSON.stringify(data["error"]);
            var errormessage = JSON.stringify(data["errormessage"]);
            var invited = JSON.stringify(data["invited"]);

            if (boolean === "true") {
                $("#errorform").html("<b>" + JSON.parse(invited) + "</b>" + " is already in team(s) " + "<b>" + JSON.parse(errormessage) + "</b>");
            }
            else if (boolean === "false") {
                $("#myModal2").modal('show');
                $("#myModal").modal('hide');
                $(".myModal2").html("Successfully invited <b>" + JSON.parse(invited) + "</b> to team(s)");
            }

        },
        error: function (data) {
            $("#post-form").html("Something went wrong :( Please refresh the page and try again");
        }
    });
    return false;
});

