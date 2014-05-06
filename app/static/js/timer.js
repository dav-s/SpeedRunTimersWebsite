
function Timer($timer){
    this.$timer = $timer;
    this.sTime=0;
    this.cTime=0;
    this.updateHTML();
}

Timer.prototype.$timer = null;

Timer.prototype.sTime = 0;
Timer.prototype.cTime = 0;

Timer.prototype.start = function(t){
    this.updateTime(t);
    this.initiate();
};

Timer.prototype.tick = function(){
    this.cTime++;
    this.updateHTML();
};

Timer.prototype.updateTime = function(t){
    this.sTime= t.start;
    this.cTime= t.current;
};

Timer.prototype.initiate = function(){
    var that = this
    setInterval(function(){
        that.tick();
    },10);
};

Timer.prototype.updateHTML = function(){
    this.$timer.html("<h2>"+(this.cTime - this.sTime)+"</h2>");
};