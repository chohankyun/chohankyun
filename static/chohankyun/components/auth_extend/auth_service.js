'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('auth_service', function ($q, $http, $cookies, $rootScope, request_service) {
    var auth_service = this;

    auth_service.login = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': "rest-auth/login/",
            'data': data
        }).then(function (data) {
            if (!request_service.use_session) {
                $http.defaults.headers.common.Authorization = 'Token ' + data.token;
                $cookies.put("token", data.token);
            }
            request_service.authenticated = true;
            $rootScope.$broadcast("chohankyun.logged_in", data);
        });
    };

    auth_service.logout = function () {
        return request_service.request({
            'method': "POST",
            'url': "rest-auth/logout/"
        }).then(function (data) {
            delete $http.defaults.headers.common.Authorization;
            $cookies.remove('token');
            request_service.authenticated = false;
            $rootScope.$broadcast("chohankyun.logged_out");
        });
    };

    auth_service.register = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': "rest-auth/registration/",
            'data': data
        });
    };

    auth_service.detail = function (model) {
        var data = model;
        return request_service.request({
            'method': "GET",
            'url': "rest-auth/user/",
        });
    };

    auth_service.update = function (model) {
        var data = model;
        return request_service.request({
            'method': "PATCH",
            'url': "rest-auth/user/",
            'data': data
        });
    };

    auth_service.delete = function (model) {
        var data = model;
        return request_service.request({
            'method': "DELETE",
            'url': "rest-auth/user/",
            'data': data
        });
    };

    auth_service.reset_user = function (model) {
        var data = model;
        return request_service.request({
            'method': "DELETE",
            'url': "rest-auth/user/reset",
            'data': data
        });
    };

    auth_service.change_password = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': "rest-auth/password/change/",
            'data': data
        });
    };

    auth_service.reset_password = function (email) {
        return request_service.request({
            'method': "POST",
            'url': "rest-auth/password/reset/",
            'data': {
                'email': email
            }
        });
    };

    auth_service.find_username = function (email) {
        return request_service.request({
            'method': "POST",
            'url': "rest-auth/username/find/",
            'data': {
                'email': email
            }
        });
    };

});
