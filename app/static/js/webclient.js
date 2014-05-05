var socket = io.connect('http://localhost:5037');

var $status = $("#connection-status")

jQuery(function () {

    socket.on("connect", function () {
        $status.attr("class", "text-success");
        $status.html("Successfully connected.");
        socket.emit("join race", {race: {id: rid, name: "none"}});
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