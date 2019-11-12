'use strict';
//$cookies 관련 api 는  최신 api 로 수정했음
var chohankyun = angular.module('chohankyun');

chohankyun.service('auth_service', function ($q, $http, $cookies, $rootScope, request_service) {
    var auth_service = this;

    auth_service.login = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': "api_auth/login/",
            'data': data
        }).then(function (data) {
            $cookies.put("token", data.token);
            request_service.authenticated = true;
            $rootScope.$broadcast("chohankyun.logged_in", data);
        });
    };

    auth_service.logout = function () {
        $cookies.remove('token');
        request_service.authenticated = false;
        $rootScope.$broadcast("chohankyun.logged_out");
    };

    auth_service.session_user = function (model) {
        return request_service.request({
            'method': "GET",
            'url': "api_auth/session/user/",
        });
    };

    auth_service.register = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': "api_auth/register/",
            'data': data
        });
    };

    auth_service.update = function (model) {
        var data = model;
        return request_service.request({
            'method': "PATCH",
            'url': "api_auth/session/user/update/",
            'data': data
        }).then(function (data) {
            $cookies.put("token", data.token);
            request_service.authenticated = true;
            $rootScope.$broadcast("chohankyun.logged_in", data);
        });
    };

    auth_service.delete = function (model) {
        var data = model;
        return request_service.request({
            'method': "DELETE",
            'url': "api_auth/session/user/delete/",
            'data': data
        });
    };

    auth_service.reset_user = function (model) {
        var data = model;
        return request_service.request({
            'method': "DELETE",
            'url': "api_auth/user/reset/",
            'data': data
        });
    };

    auth_service.change_password = function (model) {
        var data = model;
        return request_service.request({
            'method': "POST",
            'url': "api_auth/password/change/",
            'data': data
        });
    };

    auth_service.reset_password = function (email) {
        return request_service.request({
            'method': "POST",
            'url': "api_auth/password/reset/",
            'data': {
                'email': email
            }
        });
    };

    auth_service.find_username = function (email) {
        return request_service.request({
            'method': "POST",
            'url': "api_auth/username/find/",
            'data': {
                'email': email
            }
        });
    };

});
