(function () {
    AnyBlokJS.register({
        classname: 'UrlSearchManager',
        prototype: {
            toObject: function (paramString) {
                var params = {};
                var e, a = /\+/g, r = /([^&;=]+)=?([^&;]*)/g,
                    d = function (s) { return decodeURIComponent(s.replace(a, " ")); };
                while (e = r.exec(paramString.split('?')[1]))
                    params[d(e[1])] = d(e[2]);

                return params;
            },
            get: function(tag) {
                var search = window.location.search;
                if (search) {
                    search = this.toObject(search);
                } else {
                    search = {};
                }
                return search[tag];
            },
        },
    });
}) ();
