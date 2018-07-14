'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('recommend_model', function ($q, $http, $cookies, $rootScope, request_service) {
    var recommend_model = this;
    var module_name = 'board';
    var model_name = 'recommend';
    var prefix = module_name + '/' + model_name;

    recommend_model.count = function (post_id) {
        return request_service.request({
            'method': "GET",
            'url': prefix + "/count/" + post_id+'/'
        });
    };

    recommend_model.create = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': prefix + "/create/",
            'data': data
        });
    };
    

    recommend_model.delete = function (post_id) {
        return request_service.request({
            'method': "DELETE",
            'url': prefix + "/delete/" + post_id + "/"
        });
    };

});
