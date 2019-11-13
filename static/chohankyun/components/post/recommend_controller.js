'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('recommend_controller', function ($scope, $route, $routeParams, recommend_model) {
    var recommend_controller = this;

    recommend_controller.model = {
        'id': '',
        'post': '',
        'user': '',
        'recommend_count': 0,
    };

    recommend_controller.toggle_value = false;

    var recommend_count = function (post_id) {
        recommend_model.count(post_id).then(
            function (data) {
                recommend_controller.recommend_count = data.recommend_count;
                recommend_controller.toggle_value = data.is_recommend;
            },
            function (error) {
                $scope.post.messages = validate.server_error(error);
                $('#post_message_modal').modal('show')
            });
    };

    if (!angular.isUndefined($routeParams['post_id'])) {
        recommend_count($routeParams['post_id']);
    }

    recommend_controller.recommend = function () {
        if (true == recommend_controller.toggle_value) {
            recommend_controller.model.post = $routeParams['post_id'];
            recommend_model.create(recommend_controller.model).then(
                function (data) {
                    recommend_count(data.post)
                },
                function (error) {
                    $scope.post.messages = validate.server_error(error);
                    $('#post_message_modal').modal('show')
                });
        } else {
            recommend_model.delete($routeParams['post_id']).then(
                function (data) {
                    recommend_count($routeParams['post_id'])
                },
                function (error) {
                    $scope.post.messages = validate.server_error(error);
                    $('#post_message_modal').modal('show')
                });
        }
    }

});
