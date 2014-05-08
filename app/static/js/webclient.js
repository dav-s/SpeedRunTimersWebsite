
jQuery(function () {

    var timer = new Timer($("#timer"));

    var socket = io.connect('http://localhost:5037');

    var $status = $("#connection-status");
    var $updates = $("#updates");
    var $users = $("#users");
    var $start_button = $("#start-button");
    var $stop_button = $("#stop-button");
    var $pbars = $("#progress-bars");

    var cur_users = [];

    function updateUserHTMLList(){
        var res="";
        for(var i= 0; i < cur_users.length; i++){
            res+=getUserDisp(cur_users[i]);
        }
        $users.html(res);
    }

    function updateUserProgBars(){
        $pbars.html("");
        for(var i=0; i<cur_users.length; i++){
            $pbars.append('<div class="progress">' +
                '<div class="progress-bar" role="progressbar">' +
                '</div>' +
                '</div>');
        }
    }

    $start_button.click(function(){
        socket.emit("start timer");
    });

    $stop_button.click(function(){
        timer.stop();
        $stop_button.hide();
        $start_button.show();
    });

    socket.on("connect", function () {
        $status.attr("class", "text-success");
        $status.html("Successfully connected.");
        socket.emit("set user", user);
        socket.emit("join race", {race: {id: race.id, name: "none"}});
    });

    socket.on("update timer", function(t){
        timer.updateTime(t);
    });

    socket.on("start timer", function(t){
        $start_button.hide();
        timer.start(t);
        $stop_button.show();
        $updates.attr("class", "text-success");
        $updates.html("The timer was started.");
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
        cur_users = users;
        updateUserHTMLList();
        updateUserProgBars()
    });

    socket.on("error", function (reason) {
        $status.attr("class", "text-danger");
        $status.html("Could not connect.", reason);
    });

    socket.on("disconnect", function () {
        $status.attr("class", "text-danger");
        $status.html("Disconnected.");
    });

});


function getUserDisp(user){
    return "<li class='list-group-item'><img src='"+user.avatar_url+"&s=15'> <a href='/u/"+user.id+"/'>"+user.name+"</a></li>\n";
}

