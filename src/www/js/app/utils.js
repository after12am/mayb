
var toQuery = function(object) {
    
    var arr = new Array();
    
    for (var name in object) {
        arr.push(name + '=' + object[name]);
    }
    
    return arr.join('&');
}