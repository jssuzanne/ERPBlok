/*

But 

    AnyBlokJS.register({
        classname: 'My class name',
        extend: [All class names],
        element_name: 'name of the elemnt'
        prototype: {
        }
    });

    AnyBlokJS.new('My class name');
*/

// Jon Resig Class

var AnyBlokJS = {};

(function () {
    
    var extendable = false,
        classId = 0,
        fnTest = /xyz/.test(function(){xyz();}) ? /\b_super\b/ : /.*/;

    function createClass(prototypes) {
        if (!extendable) {
            throw new Error("You must not extend this Class");
        }
        function Class() {
            this._super = null;
            return this;
        }
        var _super = Class.prototype;
        var This = Class;
        var prototype = new This();
        for (var i in prototypes) {
            var prop = prototypes[i];
            for (var name in prop){
                prototype[name] = typeof prop[name] == "function" &&
                                  fnTest.test(prop[name]) ?
                        (function(name, super_fn, fn) {
                            return function() {
                                var tmp = this._super;
                                this._super = super_fn;
                                var ret = fn.apply(this, arguments);
                                this._super = tmp;
                                return ret;
                            };
                        })(name, prototype[name], prop[name]) :
                        prop[name];
            }
        }
        Class.prototype = prototype;
        return Class
    };
    
    AnyBlokJS.class_names = {}
    AnyBlokJS.register = function(declaration) {
        // fix me check we have prototype and classname
        var _class = undefined;
        if (declaration.classname in AnyBlokJS.class_names) {
            _class = AnyBlokJS.class_names[declaration.classname];
        } else {
            _class = {
                prototypes: [],
                extend: [],
                compiled: false,
            }
            this.class_names[declaration.classname] = _class;
        };
        function uncompil_extended(name){
            if (AnyBlokJS.class_names[name].compiled) {
                $.each(AnyBlokJS.class_names, function (cn, obj) {
                    if (cn != name) {
                        if (obj.compiled) {
                            if ($.inArray(name, obj.extend) != -1) {
                                uncompil_extended(cn);
                            }
                        }
                    }
                });
                AnyBlokJS.class_names[name].compiled = false;
            }
        }
        uncompil_extended(declaration.classname);
        _class.Class = undefined;
        if (declaration.extend){
            $.each(declaration.extend, function (index, extend) {
                if (!(extend in _class.extend)) {
                    _class.extend.push(extend);
                }
            });
        }
        _class.prototypes.push(declaration.prototype);
    }
    AnyBlokJS.compile = function (classname) {
        if (!(classname in AnyBlokJS.class_names)){
            throw new Error(classname + "not defined");
        }
        var Class = undefined;
        if (AnyBlokJS.class_names[classname].compiled){
            Class = AnyBlokJS.class_names[classname].Class;
        } else {
            var prototypes = [];
            if (classname != 'CorePrototype') {
                prototypes.push(AnyBlokJS.compile('CorePrototype').prototype);
            }
            $.each(AnyBlokJS.class_names[classname].extend, function (index, extend) {
                prototypes.push(AnyBlokJS.compile(extend).prototype);
            });
            $.each(AnyBlokJS.class_names[classname].prototypes, function (index, prototype) {
                prototypes.push(prototype);
            });
            extendable = true;
            classId = classId + 1;
            prototypes.push({id: classId});
            Class  = createClass(prototypes);
            extendable = false;
            AnyBlokJS.class_names[classname].Class = Class;
            AnyBlokJS.class_names[classname].compiled = true;
        }
        return Class
    }
    AnyBlokJS.new = function (classname) {
        var args = Array.prototype.slice.call(arguments, 1);
        var Class = AnyBlokJS.compile(classname);
        var instance = new (Function.prototype.bind.call(Class));
        instance.Class = {
            classname: classname,
            id: Class.prototype.id,
        };
        instance.init.apply(instance, args);
        return instance
    }

    // load Core prototype  all class depend of this class
    AnyBlokJS.register({
        classname: 'CorePrototype',
        prototype: {
            init: function() {},
            isInstance: function(classname) {
                if (classname in AnyBlokJS.class_names) {
                    if (AnyBlokJS.class_names[classname].compiled) {
                        if (AnyBlokJS.class_names[classname].Class.prototype.id == this.Class.id){
                            return true;
                        }
                    }
                }
                return false;
            },
            isInstanceExtend: function(classname) {
                if (classname in AnyBlokJS.class_names) {
                    if (this.Class.classname in AnyBlokJS.class_names) {
                        if ($.inArray(classname, AnyBlokJS.class_names[this.Class.classname].extend) != -1) {
                            return true;
                        }
                    }
                }
                return false;
            },
        },
    })
})();
