'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.service('header_model', function ($q, $http, $cookies, $rootScope, request_service) {
    var header_model = this;
    var module_name = 'index';
    var model_name = 'header';
    var prefix = module_name + '/' + model_name;

    header_model.detail = function () {
        return request_service.request({
            'method': "GET",
            'url': prefix + "/detail/"
        });
    };
    
});
