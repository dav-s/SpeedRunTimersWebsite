var io = require('socket.io').listen(5037);

var users = {};

io.sockets.on("connection", function(socket){
    socket.on("join race", function(data){
        socket.join(data.rid);
    });

    socket.on("disconnect", function(){

    });
});
