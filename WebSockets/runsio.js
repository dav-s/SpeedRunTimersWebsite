var io = require('socket.io').listen(5037);

var users = {};
var races = {};

io.sockets.on("connection", function(socket){

    socket.on("set user", function(user){
        users[socket.id] = user;
    });

    socket.on("join race", function(data){
        users[socket.id]["race"] = data.race;
        socket.join(data.race.id);
        if(races[data.race.id]){
           socket.emit("start timer", {
               start:races[data.race.id],
               current: Date.now()
           });
        }
        io.sockets.in(data.race.id).emit("user join", users[socket.id]);
        io.sockets.in(data.race.id).emit("update users", getUsersInRace(data.id));
        socket.broadcast.to(data.race.id).emit("update timer", getTimeResp(data.race.id));
    });

    socket.on("start timer", function(){
        var room = users[socket.id].race.id;
        races[room]=Date.now();
        io.sockets.in(room).emit("start timer", {
            start: Date.now(),
            current: Date.now()
        });
    });

    socket.on("disconnect", function(){
        var room = users[socket.id].race.id;
        socket.broadcast.to(room).emit("user leave", users[socket.id]);
        delete users[socket.id];
        if(getUsersInRace(room).length<=0){
            delete races[room];
        }
        socket.broadcast.to(room).emit("update users", getUsersInRace(room));
        socket.broadcast.to(room).emit("update timer", getTimeResp(room));
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

function getTimeResp(room){
    return {start:races[room], current:Date.now()};
}