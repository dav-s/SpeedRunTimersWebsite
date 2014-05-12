var io = require('socket.io').listen(5037);
var request = require('request');

var apikey = "temporary";
var fserver = "http://localhost:5000";

var colors = [
    "red",
    "orange",
    "yellow",
    "green",
    "blue",
    "indigo",
    "violet"
];

var users = {};
var races = {};

function fserreq(urlend, func){
    request({
        url:fserver+urlend,
        method:"POST",
        form:{
            apikey:apikey
        }
    }, func);
}

io.sockets.on("connection", function(socket){

    socket.on("setup", function(data){
        fserreq("/api/u/"+data.uid+"/", function(error, response, body){
            if(!error && response.statusCode == 200){
                users[socket.id]=JSON.parse(body);
                users[socket.id] = users[socket.id];
                users[socket.id].place=1;
                users[socket.id].position=0;
                users[socket.id].times=[];
                users[socket.id].finished=false;
                users[socket.id].color=colors[Math.floor(Math.random()*colors.length)];
                users[socket.id].race= data.rid;
                socket.join(data.rid);
                io.sockets.in(data.rid).emit("user join", users[socket.id]);
                io.sockets.in(data.rid).emit("update users", getUsersInRace(data.rid));
                socket.broadcast.to(data.rid).emit("update timer", getTimeResp(data.rid));
                if(races[data.rid]){
                    socket.emit("set race", races[data.rid].data);
                    if(races[data.rid].hasStarted){
                        socket.emit("start timer", {
                            start:races[data.rid]["start"],
                            current: Date.now()
                        });
                    }
                    io.sockets.in(data.rid).emit("user join", users[socket.id]);
                    io.sockets.in(data.rid).emit("update users", getUsersInRaceInOrder(data.rid));
                    socket.broadcast.to(data.rid).emit("update timer", getTimeResp(data.rid));
                }else{
                    races[data.rid]={};
                    fserreq("/api/r/"+data.rid+"/", function(error, response, body){
                        if(!error && response.statusCode == 200){
                            races[data.rid].data=JSON.parse(body);
                            socket.emit("set race", races[data.rid].data);
                            io.sockets.in(data.rid).emit("user join", users[socket.id]);
                            io.sockets.in(data.rid).emit("update users", getUsersInRaceInOrder(data.rid));
                            socket.broadcast.to(data.rid).emit("update timer", getTimeResp(data.rid));
                        }else{
                            console.log("error: "+body)
                        }
                    });
                }

            }else{
                console.log("error: "+body)
            }
        });
    });

    socket.on("start timer", function(){
        var room = users[socket.id].race;
        var now = Date.now();
        races[room].start = now;
        races[room].hasStarted=true;

        io.sockets.in(room).emit("start timer", {
            start: now,
            current: now
        });

    });

    socket.on("update all", function(){
        var room = users[socket.id].race;
        socket.emit("update timer", getTimeResp(room));
        socket.emit("update users", getUsersInRaceInOrder(room));
    });

    socket.on("split", function(){
        var room = users[socket.id].race;
        var tresp = getTimeResp(room);
        if(users[socket.id].position==races[room].data.split.splits.length-1){
            users[socket.id].times[users[socket.id].position]=tresp.current-tresp.start;
            recalculateUserPositions(room);
            users[socket.id].finished=true;
            io.sockets.in(room).emit("set update", {
                type:"success",
                text:users[socket.id].name+" has finished."
            });

            request({
                url:fserver+"/api/r/"+room+"/results/",
                method:"POST",
                form:{
                    apikey:apikey,
                    res:JSON.stringify({uid: users[socket.id].id, times:users[socket.id].times})
                }
            }, function(err, resp, body){
                if(!err && resp.statusCode == 200) {
                    socket.emit("set update", {
                        type:"success",
                        text:"Results Posted"
                    });
                    if(getNotDoneUsesInRace(room).length==0){
                        races[room].hasStarted=false;
                        finishrace();
                    }
                }else{
                    console.log("error: "+err);
                }
            });
        }if (races[room].hasStarted) {
            users[socket.id].times[users[socket.id].position] = tresp.current - tresp.start;
            users[socket.id].position++;
            recalculateUserPositions(room);
            socket.emit("update timer", tresp);
            socket.emit("update users", getUsersInRaceInOrder(room));
        }
    });

    socket.on("stop", function(){
        finishrace();
    });

    function finishrace(){
        var room = users[socket.id].race;
        races[room].hasStarted=false;
        io.sockets.in(room).emit("stop timer");
        io.sockets.in(room).emit("update timer",getTimeResp(room));
        request({
            url:fserver+"/api/r/"+room+"/results/",
            method:"POST",
            form:{
                apikey:apikey,
                finished:"yes"
            }
        }, function(err, resp, body){
            if(!err && resp.statusCode == 200) {
                io.sockets.in(room).emit("game finished");
            }else{
                console.log("error: "+err);
            }
        });
        races[room].hasStarted=false;
        io.sockets.in(room).emit("stop timer");
        io.sockets.in(room).emit("update timer",getTimeResp(room));
    }


    socket.on("disconnect", function(){
        if(users[socket.id]&&users[socket.id].race){
            var room = users[socket.id].race;
            socket.broadcast.to(room).emit("user leave", users[socket.id]);
            delete users[socket.id];
            if(getUsersInRace(room).length<=0){
                delete races[room];
            }
            socket.broadcast.to(room).emit("update users", getUsersInRaceInOrder(room));
            socket.broadcast.to(room).emit("update timer", getTimeResp(room));
        }
    });
});



function getUsersInRace(room){
    var clients = io.sockets.clients(room);
    var room_users=[];
    for(var i = 0; i < clients.length; i++){
        var tu = users[clients[i].id]
        if(tu){
            room_users.push(tu);
        }
    }
    return room_users;
}

function getNotDoneUsesInRace(room){
    var us = getUsersInRace(room);
    var fin = [];
    for(var i = 0; i < us.length; i++){
        if(!us[i].finished){
            fin.push(us[i]);
        }
    }
    return fin;
}

function getUsersInRaceInOrder(room){
    rus = getUsersInRace(room);
    for(var i =0; i<rus.length; i++){
        for(var j=0; j<rus.length-i-1;j++){
            var fu = rus[j];
            var su = rus[j+1];
            if((su.position>fu.position)||(su.finished&&fu.finished&&su.times[su.times.length-1]<fu.times[fu.times.length-1])){
                rus[j]=su;
                rus[j+1]=fu;
            }
        }
    }
    return rus;
}

function getTimeResp(room){
    if(races[room]&&races[room].start){
        return {start:races[room].start, current:Date.now()};
    }
    return {start:0, current:0};
}


function recalculateUserPositions(room){
    var usio = getUsersInRaceInOrder(room);
    var pcount=0;
    for(var i=0; i<usio.length; i++){
        if(usio[i].finished){
            usio[i].place=++pcount;
            continue;
        }
        if(i!=0&&usio[i].position==usio[i-1].position){
            usio[i].place=pcount;
        }else{
            usio[i].place=++pcount;
        }

    }
}
