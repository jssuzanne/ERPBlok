ERPBlok.HashTagManager = ERPBlok.Model.extend({
    addCallback: {},
    removeCallback: {},
    changeCallback: {},
    init: function() {
        this.load_callback();
    },
    toObject: function (paramString) {
        var params = {};
        var e, a = /\+/g, r = /([^&;=]+)=?([^&;]*)/g,
            d = function (s) { return decodeURIComponent(s.replace(a, " ")); };
        while (e = r.exec(paramString.split('#')[1]))
            params[d(e[1])] = d(e[2]);

        return params;
    },
    fromObject: function (paramObject){
        return Object.keys(paramObject).map(function (k) { 
            return encodeURIComponent(k) + '=' + encodeURIComponent(paramObject[k]);
        });
    },
    load_callback: function() {
        // overload this method to add new callback
    },
    changed: function(newh, oldh) {
        for (var key in newh) {
            if (oldh[key] == undefined) {
                for (var i in this.addCallback[key]) {
                    this.changeCallback[key][i](newh[key]);
                }
            } else {
                for (var i in this.changeCallback[key]) {
                    this.changeCallback[key][i](newh[key], oldh[key]);
                }
            }
        }
        for (var key in oldh) {
            if (newh[key] == undefined) {
                for (var i in this.removeCallback[key]) {
                    this.removeCallback[key][i](oldh[key]);
                }
            }
        }
    },
    update: function(hashs) {
        var hash = window.location.hash;
        if (hash) {
            hash = this.toObject(hash);
        } else {
            hash = {};
        }
        for (var key in hashs) {
            hash[key] = hashs[key];
        }
        hash = this.fromObject(hash);
        hash = '#' + hash.join('&');
        window.location.hash = hash;
    },
    onCallback: function(collection, entry, callback) {
        if (collection[entry] == undefined) {
            collection[entry] = [callback];
        } else {
            collection[entry].push(callback);
        }
    },
    onAdd: function(entry, callback) {
        this.onCallback(this.addCallback, entry, callback);
    },
    onChange: function(entry, callback) {
        this.onCallback(this.changeCallback, entry, callback);
    },
    onRemove: function(entry, callback) {
        this.onCallback(this.removeCallback, entry, callback);
    },
    offCallback: function(collection, entry, callback) {
        if (collection[entry] != undefined) {
            var index = collection[entry].indexOf(callback);
            if (index != -1) { 
                collection[entry].splice(index, 1); 
            }
        }
    },
    offAdd: function(entry, callback) {
        this.offCallback(this.addCallback, entry, callback);
    },
    offChange: function(entry, callback) {
        this.offCallback(this.changeCallback, entry, callback);
    },
    offRemove: function(entry, callback) {
        this.offCallback(this.removeCallback, entry, callback);
    },
});
