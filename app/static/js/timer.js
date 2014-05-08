
function Timer($timer){
    this.$timer = $timer;
    this.updateHTML();
}

Timer.prototype.$timer = null;

Timer.prototype.sTime = 0;
Timer.prototype.cTime = 0;

Timer.prototype.tickLength=100;

Timer.prototype.isRunning = false;

Timer.prototype.interval = null;

Timer.prototype.start = function(t){
    this.updateTime(t);
    this.initiate();
};

Timer.prototype.tick = function(){
    this.cTime+=this.tickLength;
    this.updateHTML();
};

Timer.prototype.updateTime = function(t){
    this.sTime= t.start;
    this.cTime= t.current;
};

Timer.prototype.initiate = function(){
    this.isRunning=true;
    var that = this
    this.interval = setInterval(function(){
        if(!that.isRunning){

        }
        that.tick();
    },that.tickLength);
};

Timer.prototype.updateHTML = function(){
    this.$timer.html("<h2>"+formatTime(this.cTime - this.sTime)+"</h2>");
};

Timer.prototype.stop = function(){
    this.isRunning=false;
    clearInterval(this.interval);
};

function formatTime(time){
    return time;
}