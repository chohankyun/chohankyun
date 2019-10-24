'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('index_controller', function ($rootScope, $scope, $window, $route, $location, request_service, auth_service, header_model, footer_model) {
    var index_controller = this;
    index_controller.search_word = null;
    index_controller.authenticated = false;
    index_controller.user = null;
    index_controller.select_index_item = null;
    index_controller.category = null;

    header_model.detail().then(function (data) {
        $rootScope.title = data.title;
    });

    footer_model.detail().then(function (data) {
        $rootScope.copyright = data.copyright;
        $rootScope.address = data.address;
        $rootScope.phone = data.phone;
    });

    index_controller.reload = function () {
        $route.reload();
    }

    index_controller.go_url = function (url) {
        if (index_controller.category == url) {
            $route.reload();
        } else {
            $location.path(url);
        }
    }

    index_controller.logout = function () {
        auth_service.logout().then(function (data) {
            if ($location.path() == $location.path("home").path()) {
                $route.reload();
            } else {
                $location.path("home");
            }
        }, function (error) {
            index_controller.message = error;
            $('#index_message_modal').modal('show')
        });
    }

    index_controller.my_post = function () {
        $rootScope.$broadcast("my_post", index_controller.category);
    };

    index_controller.search = function () {
        if (index_controller.search_word != null && index_controller.search_word != '' && index_controller.search_word.length >= 2) {
            $location.path("/search/" + encodeURIComponent(index_controller.search_word));
        } else {
            index_controller.message = 'Please enter at least 2 characters.';
            $('#index_message_modal').modal('show')
        }
    }

    $scope.$on('chohankyun.logged_out', function () {
        index_controller.authenticated = false;
        index_controller.user = null;
    });

    $scope.$on('chohankyun.logged_in', function (event, data) {
        index_controller.authenticated = true;
        index_controller.user = data.user;
    });

    $scope.$on('chohankyun.category', function (event, data) {
        index_controller.category = data;
    });

    $scope.$on('error', function (event, error) {
        index_controller.message = error;
        $('#index_message_modal').modal('show')
    });

    $scope.$on('loading', function (event, data) {
        index_controller.loading = data;
    });
});
