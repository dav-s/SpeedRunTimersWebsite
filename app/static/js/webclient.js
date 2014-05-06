

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
        $updates.attr("class","text-success");
        $updates.html(user.name+" has joined.");
    });

    socket.on("user leave", function(user){
        $updates.attr("class","text-danger");
        $updates.html(user.name+" has left.");
    });

    socket.on("update users", function(users){
        var res="";
        for(var i= 0; i < users.length; i++){
            res+=getUserDisp(users[i]);
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


function getUserDisp(user){
    return "<li class='list-group-item'><img src='"+user.avatar_url+"&s=15'> <a href='/u/"+user.id+"/'>"+user.name+"</a></li>\n";
}