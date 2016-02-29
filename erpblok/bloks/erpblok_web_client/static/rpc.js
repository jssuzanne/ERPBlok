(function() {
    AnyBlokJS.register({
        classname: 'RPC',
        prototype: {
            requestID: 0,
            getRequestID: function () {
                this.requestID += 1;
                return this.requestID;
            },
            send_json_rpc_request: function(url, method, params, done, fail) {
                var self = this,
                    request = {
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
                        } else {
                            if (self.client) {
                                self.client.errorManager.open(response.error);
                            }
                        }
                    }
                }, "json");
            },
            rpc: function(method, param, done, fail) {
                if (this.rpc_url) {
                    this.send_json_rpc_request(this.rpc_url, method, param, done, fail);
                }
            },
        },
    });
}) ();
