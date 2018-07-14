'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('category_model', function ($q, $http, $cookies, $rootScope, request_service) {
    var category_model = this;
    var module_name = 'board';
    var model_name = 'category';
    var prefix = module_name + '/' + model_name;

    category_model.list = function () {
        return request_service.request({
            'method': "GET",
            'url': prefix + "/list/"
        });
    };
    
});
