

jQuery(function () {

    var socket = io.connect('http://localhost:5037');

    var $status = $("#connection-status");
    var $updates = $("#updates");
    var $users = $("#users");

    socket.on("connect", function () {
        $status.attr("class", "text-success");
        $status.html("Successfully connected.");
        socket.emit("set user", user);
        socket.emit("join race", {race: {id: race.id, name: "none"}});
    });

    socket.on("user join", function(user){
        $updates.html(user.name+" has joined.")
    });

    socket.on("update users", function(users){
        var res="";
        for(var i= 0; i<users.length; i++){
            res+="<li><img src='"+users[i].avatar_url+"&s=15'> "+users[i].name+"</li>\n";
        }
        $users.html(res)

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