var io = require('socket.io').listen(5037);

var users = {};

io.sockets.on("connection", function(socket){

    socket.on("set user", function(user){
        users[socket.id] = user;
    });

    socket.on("join race", function(data){
        users[socket.id]["room"] = data.id;
        socket.join(data.id);
        io.sockets.in(data.id).emit("user join", users[socket.id]);
        io.sockets.in(data.id).emit("update users", getUsersInRace(data.id));
    });

    socket.on("disconnect", function(){
        var room = users[socket.id]["room"];
        socket.broadcast.to(room).emit("user leave", users[socket.id]);
        delete users[socket.id];
        io.sockets.in(room).emit("update users", getUsersInRace(room));
    });
});

function getUsersInRace(rid){
    var clients = io.sockets.clients(rid);
    var room_users=[];
    for(var i = 0; i < clients.length; i++){
        room_users.push(users[clients[i].id]);
    }
    return room_users;
}