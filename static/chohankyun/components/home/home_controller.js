'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('home_controller', function ($scope, $route, $rootScope, $location, $routeParams, home_service, post_service, category_model) {
    var home_controller = this;
    var order_list = ['updated_datetime', 'click_count', 'reply_count', 'recommend_count'];
    var carousel_s = [
        {'image_source': 'http://via.placeholder.com/1600x400?text=First slide', 'description': 'default first image source'},
        {'image_source': 'http://via.placeholder.com/1600x400?text=Second slide', 'description': 'default second image source'},
        {'image_source': 'http://via.placeholder.com/1600x400?text=Third slide', 'description': 'default third image source'}
    ];

    $scope.index.search_word = null;
    $scope.index.select_index_item = null;
    home_controller.category = 'home';

    home_service.carousel_list().then(
        function (data) {
            if (data.length != 0) {
                home_controller.carousel_list = data;
            } else {
                home_controller.carousel_list = carousel_s;
            }
        },
        function (error) {
            home_controller.messages = [error.detail];
            $('#home_message_modal').modal('show')
        });

    category_model.list().then(
        function (data) {
            home_controller.category_list = [{'id': 'home', 'name': 'Home'}, {'id': 'all', 'name': 'All'}].concat(data);
        },
        function (error) {
            home_controller.messages = [error.detail];
            $('#home_message_modal').modal('show')
        });

    angular.forEach(order_list, function (order) {
        home_service.post_list(order).then(
            function (data) {
                home_controller[order] = data;
            },
            function (error) {
                home_controller.messages = [error.detail];
                $('#home_message_modal').modal('show')
            });
    });

    $scope.$on('my_post', function () {
        angular.forEach(order_list, function (order) {
            home_service.my_post_list(order).then(
                function (data) {
                    home_controller[order] = data;
                },
                function (error) {
                    home_controller.messages = [error.detail];
                    $('#home_message_modal').modal('show')
                });
        });
    });

    home_controller.click_post = function (post_id) {
        post_service.increase_click_count(post_id).then(
            function (data) {
                $location.path('/post/' + post_id);
            },
            function (error) {
                home_controller.messages = [error.detail];
                $('#home_message_modal').modal('show')
            });
    };

    $rootScope.$broadcast('chohankyun.category', 'home');

});
