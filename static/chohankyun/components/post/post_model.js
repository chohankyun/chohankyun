'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('post_model', function ($q, $http, $cookies, $rootScope, request_service) {
    var post_model = this;
    var module_name = 'board';
    var model_name = 'post';
    var prefix = module_name + '/' + model_name;

    post_model.list = function () {
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/"
        });
    };

    post_model.create = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': prefix + "/create/",
            'data': data
        });
    };

    post_model.update = function (model) {
        var data = model;
        return request_service.request({
            'method': "PATCH",
            'url': prefix + "/update/" + model.id + "/",
            'data': data
        });
    };

    post_model.detail = function (id) {
        return request_service.request({
            'method': "GET",
            'url': prefix + "/detail/" + id + "/"
        });
    };

    post_model.delete = function (id) {
        return request_service.request({
            'method': "DELETE",
            'url': prefix + "/delete/" + id + "/"
        });
    };

});
