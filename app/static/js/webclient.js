
jQuery(function () {

    var timer = new Timer($("#timer"));

    var socket = io.connect('http://localhost:5037');

    var $status = $("#connection-status");
    var $updates = $("#updates");
    var $users = $("#users");
    var $start_button = $("#start-button");
    var $split_button = $("#split-button");
    var $pbars = $("#progress-bars");
    var $nexty = $("#nexty");
    var $lasty = $("#lasty");

    var race = {};

    var alt_cols = ["#E6E6E6", "#CFCFCF"];

    var cur_users = [];
    var this_user = {};

    function updateUserHTMLList(){
        var res="<tr><th>Place</th>" +
            "<th>User</th></tr>";
        for(var i= 0; i < cur_users.length; i++){
            res+=getUserDisp(cur_users[i]);
        }
        $users.html(res);
    }

    function updateUserProgBars(){
        $pbars.html("");
        for(var i=0; i<cur_users.length; i++){
            var temp = "<div class='col-md-1'><strong>"+cur_users[i].name+":</strong></div><div class='col-md-11'><div class='progress'>";
            var splits = race.split.splits;
            var width = 100/splits.length;
            for(var j = 0; j<splits.length; j++){
                if(j<cur_users[i].position){
                    if(cur_users[i].times[j]){
                        temp += '<div data-toggle="tooltip" class="progress-bar datpop" data-placement="right"' +
                            'title="' + splits[j].name + '"' +
                            'data-content="'+timeToText(cur_users[i].times[j])+'"' +
                            'style="width: ' + width + '%; background-color: ' + (j % 2 ? tinycolor.darken(cur_users[i].color, amount = 5) : cur_users[i].color) + ';">' +
                            '</div>';
                    }else {
                        temp += '<div data-toggle="tooltip" class="progress-bar datpop" data-placement="right"' +
                            'data-content="' + splits[j].name + '"' +
                            'style="width: ' + width + '%; background-color: ' + (j % 2 ? tinycolor.darken(cur_users[i].color, amount = 5) : cur_users[i].color) + ';">' +
                            '</div>';
                    }
                }else{
                    temp+='<div data-toggle="tooltip" class="progress-bar datpop" data-placement="right"'+
                        'data-content="'+splits[j].name+'"' +
                        'style="width: '+width+'%; background-color: '+alt_cols[j%alt_cols.length]+';">' +
                        '</div>';
                }
            }
            $pbars.append(temp+"</div></div>");
        }
        $(".datpop").popover({
            trigger: "hover"
        });
    }

    function updateUpcomingBox(){
        this_user = getUser(uid,cur_users);
        var pos = this_user.position;
        var len = race.split.splits.length-1;
        if(!pos){
            $lasty.html("<h4>None</h4>")
        }else{
            if(race.split.splits[pos-1]) {
                $lasty.html("<h4>" + race.split.splits[pos - 1].name + "</h4>" +
                    "<h4>" + timeToText(this_user.times[pos - 1]) + "</h4>");
            }else{
                $lasty.html("<h4>" + race.split.splits[len].name + "</h4>" +
                    "<h4>" + timeToText(this_user.times[len]) + "</h4>");
            }
        }
        if(pos<=len){
            $nexty.html("<h4>"+race.split.splits[pos].name+"</h4>");
        }else{
            $nexty.html("<h4 class='text-success'>Finished!</h4>");
        }
    }

    $([window, document]).focusin(function(){
        if(timer.isRunning){
            socket.emit("update all");
        }
    });

    $(document).keydown(function(e){
        if(e.which==32){
            if(timer.isRunning){
                socket.emit("split");
            }
            return false;
        }
        return true;
    });


    $start_button.click(function(){
        socket.emit("start timer");
    });

    $split_button.click(function(){
        socket.emit("split");
    });

    socket.on("connect", function () {
        $status.attr("class", "text-success");
        $status.html("Successfully connected.");

        socket.emit("setup", {uid:uid, rid:rid});
    });

    socket.on("set race", function(r){
        race=r;
        updateUserProgBars();
    });

    socket.on("set update", function(data){
        $updates.attr("class", "text-"+data.type);
        $updates.html(data.text);
    });


    socket.on("update timer", function(t){
        timer.updateTime(t);
    });

    socket.on("start timer", function(t){
        $start_button.hide();
        timer.start(t);
        $split_button.show();
        $updates.attr("class", "text-success");
        $updates.html("The timer was started.");
    });

    socket.on("stop timer", function(){
        timer.stop();
        $split_button.hide();
        $updates.attr("class", "text-danger");
        $updates.html("The timer was stopped.");
    });

    socket.on("user join", function(user){
        $updates.attr("class","text-success");
        $updates.html(user.name+" has joined.");
    });

    socket.on("user leave", function(user){
        $updates.attr("class","text-danger");
        $updates.html(user.name+" has left.");
    });

    socket.on("update users", function(users){
        $start_button.show();
        cur_users = users;
        updateUserHTMLList();
        updateUserProgBars();
        updateUpcomingBox();
    });

    socket.on("game finished", function(){
        window.location="/r/"+rid+"/";
    });

    socket.on("error", function (reason) {
        $status.attr("class", "text-danger");
        $status.html("Could not connect.", reason);
    });

    socket.on("disconnect", function () {
        timer.stop();
        $status.attr("class", "text-danger");
        $status.html("Disconnected.");
    });

});


function getUserDisp(user){
    var ttc = tinycolor(user.color);
    ttc.setAlpha(.25);
    return "<tr style='background-color: "+ttc.toRgbString()+"'>" +
        "<td>"+user.place+"</td>" +
        "<td>" +
            "<img src='"+user.avatar_url+"&s=15'> " +
            "<a href='/u/"+user.id+"/'>"+user.name+"</a>" +
        "</td>" +
        "</tr>";
}

function getUser(id, users){
    for(var i=0; i<users.length; i++){
        if(users[i].id==id){
            return users[i];
        }
    }
    return {};
}

