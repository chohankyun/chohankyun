'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.service('footer_model', function ($q, $http, $cookies, $rootScope, request_service) {
    var footer_model = this;
    var module_name = 'index';
    var model_name = 'footer';
    var prefix = module_name + '/' + model_name;

    footer_model.detail = function () {
        return request_service.request({
            'method': "GET",
            'url': prefix + "/detail/"
        });
    };
    
});
