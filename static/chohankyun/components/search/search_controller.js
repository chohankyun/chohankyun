'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('search_controller', function ($scope, $rootScope, $location, $routeParams, post_service, search_service) {
    var search_controller = this;
    var init_page = 1;

    search_controller.total = null;
    search_controller.selected_order = 'changed_datetime';
    search_controller.order_list = [
        {'id': 'changed_datetime', 'name': 'New'},
        {'id': 'recommend_count', 'name': 'Recommend'},
        {'id': 'reply_count', 'name': 'Reply'},
        {'id': 'click_count', 'name': 'Lookup'}
    ];

    var post_list = function (page) {
        if (!angular.isUndefined($routeParams['search_word'])) {
            search_service.post_list($routeParams['search_word'], search_controller.selected_order, page).then(
                function (data) {
                    search_controller.search_list = data;
                    search_controller.total = data.length;
                },
                function (error) {
                    search_controller.message = error.detail;
                    $('#search_message_modal').modal('show')
                });
        }
    }

    post_list(init_page);

    search_controller.click_item = function (search_id) {
        post_service.increase_click_count(search_id).then(
            function (data) {
                $location.path('/post/' + search_id);
            },
            function (error) {
                search_controller.message = error.detail;
                $('#search_message_modal').modal('show')
            });
    }

    search_controller.click_order = function (index) {
        search_controller.selected_order = index;
        post_list(init_page);
    }

    search_controller.get_page = function (page) {
        post_list(page)
    }

    $rootScope.$broadcast("chohankyun.category", '/search/' + $routeParams['search_word']);

});
