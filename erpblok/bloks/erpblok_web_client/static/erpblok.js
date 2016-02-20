window.ERPBlok = null;
(function () {
    var fnTest = /xyz/.test(function(){xyz();}) ? /\b_super\b/ : /.*/; 

    class ERPBLOK {
        constructor () {
            this.classes = {};
            this.react_classes = {};
            this.mixins = {};
        };
        extend (classname, cls, prototype) {  
            var A = null;
            if (cls == undefined) {
                function init (self) {
                }
                A = new Function('init', 'return function ' + classname + ' () {init(this);}')(init);
                A.prototype = Object.create(prototype);
            } else {
                A = cls;
                for (var name in prototype) {
                    A.prototype[name] = typeof prototype[name] == "function" &&            
                                        fnTest.test(prototype[name]) ?                     
                        (function(name, super_fn, fn) {                         
                            return function() {
                                var tmp = this._super;                          
                                this._super = super_fn;                         
                                var ret = fn.apply(this, arguments);            
                                this._super = tmp;                              
                                return ret;                                     
                            };                                                  
                        })(name, A.prototype[name], prototype[name]) :                 
                        prototype[name]; 
                }
            }
            return A
        };
        add_prototype_for (classname, prototype={}, isareactclass=true) {
            var parent = undefined;
            if (isareactclass) {
                parent = this.react_classes[classname];
            } else {
                parent = this.classes[classname];
            }
            var cls = this.extend(classname, parent, prototype);
            if (isareactclass) {
                this.react_classes[classname] = cls;
            } else {
                this.classes[classname] = cls;
            }
        };
        add_mixin (mixinname, prototype={}) {
            var parent = this.mixins[mixinname];
            var A  = this.extend(mixinname, parent, prototype);
            this.mixins[mixinname] = A;
        }
        apply_mixin (classname, mixinname, isreactclass=true) {
            var mixin = this.mixins[mixinname];
            if (mixin) {
                mixin = mixin.prototype;
            }
            this.add_prototype_for(classname, mixin, isreactclass);
        }
        get_class_for (classname) {
            return this.classes[classname];
        };
        compile_react_classes() {
            var self = this;
            for (var classname in this.react_classes) {
                var cls = self.react_classes[classname],
                    prototype = React.Component.prototype;
                window[classname] = self.extend(classname, cls, prototype);
            }
        };
    };

    window.ERPBlok = new ERPBLOK()
}) ();

// var ERPBlok = new ERPBLOK();
/*
(function () {
    AnyBlokJS.register({
        classname: 'ERPBlok',
        prototype: {
            init: function () {
                this.init_foundation();
                this.init_object();
            },
            init_foundation: function () {
                this.offCanvasLeft = new Foundation.OffCanvas($('#offCanvasLeft.off-canvas'));
                this.offCanvasRight = new Foundation.OffCanvas($('#offCanvasRight.off-canvas'));
                this.dropdownTopBarLarge = new Foundation.DropdownMenu($('#topbar-menu-large'));
                this.accordionMenuLarge = new Foundation.AccordionMenu($('#accordion-menu-large'));
                this.accordionMenuSmall = new Foundation.AccordionMenu($('#accordion-menu-small'));
            },
            init_object: function () {
                var self = this;
                this.hashTagManager = AnyBlokJS.new('HashTagManager', this);
                this.menuManager = AnyBlokJS.new('MenuManager', this);
                this.actionManager = AnyBlokJS.new('ActionManager', this);
                $('.logout').click(function (event) {
                    self.logout ();
                });
                $('.toggle-menu').click(function (event) {
                    var mainmenu = $('#main-menu')
                    var mainapp = $('#main-app')
                    if (mainmenu.hasClass('hide')) {
                        mainmenu.removeClass('hide');
                        mainapp.addClass('large-9');
                    } else {
                        mainmenu.addClass('hide');
                        mainapp.removeClass('large-9');
                    }
                });
            },
            load: function () {
                this.hashTagManager.changed(this.hashTagManager.toObject(window.location.hash), {});
            },
            logout: function () {
                $.ajax({type: "POST",
                        url: "/login/disconnect",
                        data: {}})
                .done(function (url) {
                    window.location = url;
                });
            },
        },
    });
}) ();
*/
