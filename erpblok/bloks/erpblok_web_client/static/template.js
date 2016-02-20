(function () {
    ERPBlok.add_mixin('Template', {
        template: null,
        render_template: function(values={}) {
            return $.templates('#' + this.template).render(values);
        },
        render: function () {
            var el = this.render_template({this: this});
            return (<div dangerouslySetInnerHTML={{__html: el}} />)
        },
    });
}) ();
