var io = require('socket.io').listen(5037);

var users = {};

io.sockets.on("connection", function(socket){

    socket.on("set user", function(user){
        users[socket.id] = user;
    });

    socket.on("join race", function(data){
        users[socket.id]["race"] = data.race;
        socket.join(data.race.id);
        io.sockets.in(data.race.id).emit("user join", users[socket.id]);
        io.sockets.in(data.race.id).emit("update users", getUsersInRace(data.id));
    });

    socket.on("disconnect", function(){
        var room = users[socket.id].race.id;
        socket.broadcast.to(room).emit("user leave", users[socket.id]);
        console.log(users);
        delete users[socket.id];
        console.log(users);
        console.log(getUsersInRace(room));
        socket.broadcast.to(room).emit("update users", getUsersInRace(room));
    });
});

function getUsersInRace(room){
    var clients = io.sockets.clients(room);
    var room_users=[];
    for(var i = 0; i < clients.length; i++){
        if(users[clients[i].id]){
            room_users.push(users[clients[i].id]);
        }
    }
    return room_users;
}