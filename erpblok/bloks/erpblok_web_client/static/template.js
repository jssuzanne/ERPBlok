(function () {
    AnyBlokJS.register({classname:'Template', prototype: {
        template: null,
        render_template: function(values={}) {
            return $($.templates('#' + this.template).render(values));
        },
    }});
}) ();
