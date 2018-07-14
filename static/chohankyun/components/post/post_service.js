'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('post_service', function ($q, $http, $cookies, $rootScope, request_service) {
    var post_service = this;

    post_service.increase_click_count = function (id) {
        var module_name = 'board';
        var model_name = 'post';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/increase_click_count/" + id + "/"
        });
    };

});
