'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('board_service', function ($q, $http, $cookies, $rootScope, request_service) {
    var board_service = this;

    board_service.post_list = function (category, order, page) {
        var module_name = 'board';
        var model_name = 'post';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/" + category + "/" + order + "/?page="+page
        });
    };

    board_service.my_post_list = function (category, order, page) {
        var module_name = 'board';
        var model_name = 'my_post';
        var prefix = module_name + '/' + model_name;
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/" + category + "/" + order + "/?page="+page
        });
    };

});
