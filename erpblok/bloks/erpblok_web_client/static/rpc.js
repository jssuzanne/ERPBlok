ERPBlok.RPC = ERPBlok.Model.extend({
    requestID: 0,
    getRequestID: function () {
        this.requestID += 1;
        return this.requestID;
    },
    send_json_rpc_request: function(url, method, params, done, fail) {
        var request = {
            'method': method,
            'params': params,
            'id': this.getRequestID(),
            'jsonrpc': '2.0',
        };
        $.post(url, JSON.stringify(request), function (response) {
            if (response.result) {
                if (done) {
                    done(response.result);
                }
            } else if (response.error) {
                if (fail) {
                    fail(response.error);
                }
            }
        }, "json");
    },
    rpc: function(method, param, done, fail) {
        this.send_json_rpc_request(this.rpc_url, method, param, done, fail);
    },
});
