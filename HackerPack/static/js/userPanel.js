// Function to create dynamic panels
var users_panel = document.getElementById('users-panel');
var count = 0;
var oldRow = document.createElement('div');
oldRow.className = 'row';

function createPanel() {

    // Create a panel with specified content
    // This is basically what we are trying to render with this code
    //           <div class = "col-md-4">
    //           <div class = "panel panel-default panel-cus" onclick = "changeArrow();">
    //           <div class = "custom-panel center-block" data-toggle="collapse" data-target="#lower2">
    //               <img src = "../../static/images/hackathons/pixiehacks.png" class="img-responsive">
    //               <div class="carousel-caption">
    //                   <h1> PixieHacks </h1>
    //                   <p> July 9th, 2016 </p>
    //                   <p> New York, NY</p>
    //                       <img src = "../../static/images/down-arrow.png" class="img-responsive center-block" id = "arrow">
    //
    //               </div>
    //
    //           </div>
    //               <div id = "lower2" class = "collapse">
    //                   <p> About </p>
    //                   <p> School </p>
    //               </div>
    //           </div>
    //       </div>

    var up_arrow_url = "https://s3.amazonaws.com/hack-mates/static/images/up-arrow.png";
    var down_arrow_url = "https://s3.amazonaws.com/hack-mates/static/images/down-arrow.png";
    var static_url = 'https://hack-mates.s3.amazonaws.com';

    var idString = "id=" + id;
    var tempString = "<div class='col-md-4'" + ">" +
        "<div class='panel panel-default panel-cus center-block' onclick='changeArrow(" +
        id + ")'" + idString + ">" +
        "<div class='custom-panel center-block' data-toggle='collapse'" +
        "data-target='#lower" + id + "'>" +
        "<img src=" + static_url + imagesrc + " class='img-responsive" +
        " center-block" +
        " user-image'>" +
        "<div class = 'carousel-caption'>" + "<h1>" +
        first_name + "</h1>"
        + '<img src ='
        + down_arrow_url
        + ' class="img-responsive center-block arrow-image" id = "arrow'
        + id + '">'
        + "</div>" + "</div>" +
        "<div id = 'lower" + id + "' class = 'collapse' style='padding:15px;'>" +
        html_school + html_about +
        html_ideas  + html_roles + html_languages  + html_frameworks +
        '<button class = "btn btn-primary big-register center-block"' +
        ' onclick="openRegisterModal();"> Team Up </button>' +
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

    var up_arrow_url = "https://s3.amazonaws.com/hack-mates/static/images/up-arrow.png";
    var down_arrow_url = "https://s3.amazonaws.com/hack-mates/static/images/down-arrow.png";

    idPanel = String('#lower' + id);
    idArrow = String('arrow' + id);

    $(idPanel).on('shown.bs.collapse', function () {
        document.getElementById(idArrow).src = up_arrow_url;
    });
    $(idPanel).on('hide.bs.collapse', function () {
        document.getElementById(idArrow).src = down_arrow_url;
    });
}


// Function for load more button
$(function () {
    var hidingCount = 6;
    $("#load").click(function (e) { // click event for load more
        e.preventDefault();
        $(".hiding").slice(hidingCount - 6, hidingCount).show();
        hidingCount += 6;
        if (hidingCount > num) {
            openRegisterModal();
        }
    });
});