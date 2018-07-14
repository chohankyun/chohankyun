'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('home_service', function ($q, $http, $cookies, $rootScope, request_service) {
    var home_service = this;

    home_service.carousel_list = function () {
        var module_name = 'home';
        var model_name = 'carousel';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/"
        });
    };

    home_service.post_list = function (order) {
        var module_name = 'home';
        var model_name = 'post';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/" + order + "/"
        });
    };

    home_service.my_post_list = function (order) {
        var module_name = 'home';
        var model_name = 'my_post';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/" + order + "/"
        });
    };

});
