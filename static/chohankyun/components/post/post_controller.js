'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('post_controller', function ($scope, $q, $window, $routeParams, $location, $filter, validate, category_model, post_model) {
    var post_controller = this;

    post_controller.model = {
        'id': '',
        'user': '',
        'username': '',
        'category': '',
        'category_name': '',
        'subject': '',
        'content': '',
        'reply_count': 0,
        'click_count': 0,
        'recommend_count': 0,
    };

    if ($scope.index.user != null) {
        post_controller.model.username = $scope.index.user.username;
    }
    post_controller.local_datetime = $filter('date')(new Date(), 'yyyy-MM-dd');
    post_controller.is_disabled = false;
    post_controller.is_data = false;

    var category_list = category_model.list();
    var post_detail = null;
    if (!angular.isUndefined($routeParams['post_id'])) {
        post_detail = post_model.detail($routeParams['post_id']);
    }

    $q.all([category_list, post_detail, $scope.change]).then(
        function (response) {
            post_controller.category_list = response[0];

            if (response[1] != null) {
                post_controller.model = response[1];
                if (post_controller.model.id != '') {
                    post_controller.local_datetime = post_controller.model.local_datetime;
                    post_controller.is_disabled = true;
                    post_controller.is_data = true;
                }
            }
        });

    post_controller.create = function (formData) {
        post_controller.errors = [];
        post_controller.result = null;

        validate.form_validation(formData, post_controller.errors);
        if (post_controller.errors.category.length > 0
            || post_controller.errors.subject.length > 0
            || post_controller.errors.content.length > 0) {
            $('#post_message_modal').modal('show')
        }

        if (!formData.$invalid) {
            if (post_controller.model.id == '') {
                post_model.create(post_controller.model).then(
                    function (data) {
                        $location.path($scope.index.category);
                    },
                    function (error) {
                        post_controller.errors = error;
                        $('#post_message_modal').modal('show');
                    });
            } else {
                post_model.update(post_controller.model).then(
                    function (data) {
                        $location.path($scope.index.category);
                    },
                    function (error) {
                        post_controller.errors = error;
                        $('#post_message_modal').modal('show');
                    });
            }
        }
    }


    post_controller.delete = function (id) {
        $("#confirm_message_modal").modal('show');

        $('#modal-btn-confirm').on('click', function () {
            post_model.delete(id).then(
                function (data) {
                    $location.path($scope.index.category);
                    $window.location.reload();
                },
                function (error) {
                    post_controller.errors = error;
                    $('#post_message_modal').modal('show');
                });
        });
    }

    post_controller.cancel = function () {
        $location.path($scope.index.category);

    }

});
