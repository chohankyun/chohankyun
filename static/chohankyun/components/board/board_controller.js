'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('board_controller', function ($scope, $route, $rootScope, $location, $routeParams, board_service, post_service, category_model) {
    var board_controller = this;
    var init_page = 1;

    $scope.index.select_index_item = null;
    board_controller.my_post = null;
    board_controller.category = null;
    board_controller.selected_order = 'updated_datetime';
    board_controller.order_list = [
        {'id': 'updated_datetime', 'name': 'New'},
        {'id': 'recommend_count', 'name': 'Recommend'},
        {'id': 'reply_count', 'name': 'Reply'},
        {'id': 'click_count', 'name': 'Lookup'}
    ];

    var post_list = function (page) {
        if (!angular.isUndefined($routeParams['category'])) {
            board_controller.category = $routeParams['category'];
            board_service.post_list($routeParams['category'], board_controller.selected_order, page).then(
                function (data) {
                    board_controller.post_list = data;
                },
                function (error) {
                    board_controller.message = error.detail;
                    $('#board_message_modal').modal('show')
                });
        }
    }

    var my_post_list = function (page) {
        board_service.my_post_list(board_controller.my_post, board_controller.selected_order, page).then(
            function (data) {
                board_controller.post_list = data;
            },
            function (error) {
                board_controller.message = error.detail;
                $('#board_message_modal').modal('show')
            });
    }

    category_model.list().then(
        function (data) {
            board_controller.category_list = [{'id': 'home', 'name': 'Home'}, {'id': 'all', 'name': 'All'}].concat(data);
        },
        function (error) {
            board_controller.message = error.detail;
            $('#board_message_modal').modal('show')
        });

    post_list(init_page);

    board_controller.click_order = function (index) {
        board_controller.selected_order = index;
        post_list(init_page)
    }

    board_controller.click_post = function (post_id) {
        post_service.increase_click_count(post_id).then(
            function (data) {
                $location.path('/post/' + post_id);
            },
            function (error) {
                board_controller.message = error.detail;
                $('#board_message_modal').modal('show')
            });
    }

    board_controller.get_page = function (page) {
        if (board_controller.my_post != null) {
            my_post_list(page);
        } else {
            post_list(page);
        }
    }

    $scope.$on('my_post', function (event, data) {
        var category = data.split('/');
        board_controller.my_post = category[category.length - 1];
        my_post_list(init_page);
    });

    $rootScope.$broadcast("chohankyun.category", '/board/' + board_controller.category);

});
