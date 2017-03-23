
function getList() {

	$.ajax({
		url: "/socialnetwork/get-list-json",
		dataType: "json",
		success: updateList
	});
}
function updateList(item) {
    console.log(item.posts);
    console.log(item.comments);
    var type = false;
    if ($(".comment-box").length) {
        if (($(".comment-box").val() !== "") || (document.activeElement.localName === "textarea"))
            type = true;
    }
    // console.log(type);
    if (type) {
        return;
    }
    $("#posts_container").empty();
    
    var jposts = JSON.parse(item.posts).reverse();
    var jprofiles = JSON.parse(item.profiles);
    var jusers = JSON.parse(item.users);
    var jcurruser = JSON.parse(item.curr_user);
    var jcomment = JSON.parse(item.comments);

    var post = [];
    var post_id = [];
    var profile_user = [];
    var profile_pic = [];
    for (var i = 0 ; i < jposts.length ; i ++) {
        post[i] = jposts[i].fields;
        post_id[i] = jposts[i].pk;
    }
    for (var i = 0 ; i < jprofiles.length ; i ++) {
        profile_user[i] = (jprofiles[i].fields.user);
        profile_pic[i] = jprofiles[i].fields.picture;
    }
    // console.log(profile_user);
    // console.log(post_id);
    var idx = -1;
    for (var i = 0 ; i < jposts.length ; i ++) {
        // console.log(post_id[i]);

        // Pictures and post contents
        var temp = '<div class="h4 bg-info" id="all_posts_info">';
        idx = profile_user.indexOf((post[i].user));
        // console.log(profile_pic[idx]);
        if (profile_pic[idx]){
            temp += '<img src=/socialnetwork/picture/'+ jusers[idx].fields.username +' alt="no pic"  width="60px">';
        } 
            
        else {
            temp += '<img src="http://simpleicon.com/wp-content/uploads/smile.png" alt="no pic" width="60px">';
        }
        // console.log(jusers[idx].fields.username);
        temp += "   " + sanitize(post[i].content);
        temp += '<span class="details"> (posted at '+  new Date(post[i].created_at) +') </span> </div>'
        // $("#posts_container").append(temp);


        // Buttons (delete / profiles)
        temp += "<table> <tr>";
        if (post[i].user === jcurruser[0].pk) {
            temp += "<td>";
            temp += '<button class="btn btn-danger btn-md" type="submit" value="X" onclick="del_post('+ post_id[i] +')">X</button>';
            temp += "</form></td>"

        }
        
        temp += "<td>";
        temp += '<a href="/socialnetwork/show-profile/'+ jusers[idx].fields.username + '">';
        temp += '<button class="btn btn-info btn-md">' + jusers[idx].fields.username + "\'s profile</button>";
        temp += "</a></form></td>";        
        temp += '<td><button id="comment_button" class="btn btn-success btn-md" onclick="add_comment('+ post_id[i] + ')"> Comment on ' + jusers[idx].fields.username + "\'s post</button></td>";
        temp += '<td><textarea id="comment'+ post_id[i] +'" class="comment-box" rows="5" cols="80" name="content" maxlength="160"></textarea></td>';
        temp += "</tr> </table><br/><hr class='hr'></div>";

        for (var j = 0; j < jcomment.length ; j ++){
            if (post_id[i] === jcomment[j].fields.commented_on){
                commenter_id = jcomment[j].fields.user;
                idx2 = profile_user.indexOf((commenter_id));

                temp += "<div class='bg-success text-center' >"
                if (profile_pic[idx2]){
                    temp += '<img src=/socialnetwork/picture/'+ jusers[idx2].fields.username +' alt="no pic"  width="40px">';
                }
                else {
                    temp += '<img src="http://simpleicon.com/wp-content/uploads/smile.png" alt="no pic" width="40px">';
                }
                temp += jcomment[j].fields.content + "(at " + new Date(jcomment[j].fields.created_at) + " by " + jusers[idx2].fields.username;
                temp += "</div></br>"
            }
            
        }
    $("#posts_container").append(temp);
    }
	
}
function add_comment(id) {
    // var input_com = $(".comment-box");
    // input_com.val('');
    var comText = $("#comment" + id);
    var comTextVal = comText.val();
    if ($(".comment-box").length) {
        $(".comment-box").val('');
    }
    
    comText.val('');
    displayError('');

    $.ajax({
        url: "/socialnetwork/add-comment-json/" + id,
        type: "POST",
        data: "content="+comTextVal+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: function(response) {
            // console.log(response);
            if (typeof response === "object") {
                // alert('comment success');
                updateList(response);
            } else {
                // alert('comment bad');
                displayError(response.error);
            }
        }
    });
}

function add_post() {
    // var input_com = $(".comment-box");
    // if (input_com)
    //     input_com.val('');
    if ($(".comment-box").length) {
        $(".comment-box").val('');
    }
    var postText = $("#input");
    var postTextVal = postText.val();
    postText.val('');
    displayError('');
    $.ajax({
        url: "/socialnetwork/add-post-json",
        type: "POST",
        data: "content="+postTextVal+"&csrfmiddlewaretoken="+getCSRFToken(),
        dataType: "json",
        success: function(response) {
            // console.log(response);
            if (typeof response  === "object") {
                // alert('post success');
                updateList(response);
                displayError(response.error);

            } else {
                // alert('post bad');
                displayError(response.error);
            }
        }
    });
}
function del_post(id) {
    if ($(".comment-box").length) {
        $(".comment-box").val('');
    }
    $.ajax({
        url: "/socialnetwork/del-post-json/" + id,
        type: "POST",
        data: "csrfmiddlewaretoken=" + getCSRFToken(),
        dataType: "json",
        success: updateList
    });
}
function displayError(message) {
    $("#error").html(message);
}
function getCSRFToken() {
    var cookies = document.cookie.split(";");
    for (var i = 0 ; i < cookies.length ; i++) {
        if (cookies[i].startsWith("csrftoken=")) {
            return cookies[i].substring("csrftoken=".length, cookies[i].length);
        } 
    }
    return "unknown";
}

function sanitize(s) {
    // Be sure to replace ampersand first
    return s.replace(/&/g, '&amp;')
            .replace(/</g, '&lt;')
            .replace(/>/g, '&gt;')
            .replace(/"/g, '&quot;');
}

window.onload = getList;
window.setInterval(getList, 5000);



