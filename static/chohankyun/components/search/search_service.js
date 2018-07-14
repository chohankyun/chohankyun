'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.service('search_service', function ($q, $http, $cookies, $rootScope, request_service) {
    var search_service = this;

    search_service.post_list = function (search_word, order_by, page) {
        var module_name = 'search';
        var model_name = 'post';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/"+ search_word + "/"+ order_by + "/?page="+page
        });
    };

});
