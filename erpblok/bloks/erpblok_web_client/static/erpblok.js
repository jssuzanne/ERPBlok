window.ERPBlok = null;
(function () {
    AnyBlokJS.register({classname: 'React', prototype: React.Component.prototype})

    var ERPBLOK = function () {this.init()};
    ERPBLOK.prototype = Object.create({
        init: function () {
            this.react_classes = [];
            this.fields = {};
        },
        declare_react_class: function (classname, fieldType=undefined) {
            if (this.react_classes.indexOf(classname) == -1) {
                this.react_classes.push(classname);
            }
            if (fieldType) this.fields[fieldType] = classname;
        },
        add_field_definition: function (fieldType, classname) {
            this.fields[fieldType] = classname;
        },
        get_field_definition: function (fieldType) {
            var classname = 'FieldString';
            if (this.fields[fieldType]) classname = this.fields[fieldType];
            return AnyBlokJS.compile(classname);
        },
        compile_react_classes: function () {
            for (var index in this.react_classes) {
                var classname = this.react_classes[index];
                AnyBlokJS.register({classname: classname, extend: ['React']})
                window[classname] = AnyBlokJS.compile(classname);
                window[classname].prototype.constructor = function () {
                    if (this.init) {
                        this.init();
                    }
                    React.Component.prototype.constructor.apply(this, arguments);
                    var r = this.getInitialState ? this.getInitialState() : null;
                    this.state = r
                };
            }
        },
    });

    window.ERPBlok = new ERPBLOK()
}) ();
