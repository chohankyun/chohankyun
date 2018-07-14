'use strict';

chohankyun.config(function ($routeProvider) {
    $routeProvider
        .when('/login', {
            templateUrl: '/static/chohankyun/components/auth_extend/login.html',
            controller: 'login_controller',
            controllerAs: 'login',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/find/:find_word', {
            templateUrl: '/static/chohankyun/components/auth_extend/find.html',
            controller: 'find_controller',
            controllerAs: 'find',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/register', {
            templateUrl: '/static/chohankyun/components/auth_extend/register.html',
            controller: 'register_controller',
            controllerAs: 'register',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/profile', {
            templateUrl: '/static/chohankyun/components/auth_extend/profile.html',
            controller: 'profile_controller',
            controllerAs: 'profile',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/password', {
            templateUrl: '/static/chohankyun/components/auth_extend/password.html',
            controller: 'password_controller',
            controllerAs: 'password',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/home', {
            templateUrl: '/static/chohankyun/components/home/home.html',
            controller: 'home_controller',
            controllerAs: 'home',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/board/home', {
            redirectTo: '/home'
        })
        .when('/board/:category', {
            templateUrl: '/static/chohankyun/components/board/board.html',
            controller: 'board_controller',
            controllerAs: 'board',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/post', {
            templateUrl: '/static/chohankyun/components/post/post.html',
            controller: 'post_controller',
            controllerAs: 'post',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/post/:post_id', {
            templateUrl: '/static/chohankyun/components/post/post.html',
            controller: 'post_controller',
            controllerAs: 'post',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .when('/search/:search_word', {
            templateUrl: '/static/chohankyun/components/search/search.html',
            controller: 'search_controller',
            controllerAs: 'search',
            resolve: {
                authenticated: function (request_service) {
                    return request_service.authentication_status();
                },
            }
        })
        .otherwise({
            redirectTo: '/home'
        })
});