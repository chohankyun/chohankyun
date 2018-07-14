'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('reply_controller', function ($scope, $route, $window, $routeParams, $location, $filter, validate, reply_model) {
    var reply_controller = this;

    reply_controller.model = {
        'id': '',
        'post': '',
        'user': '',
        'username': '',
        'content': '',
        'click_count': 0,
        'recommend_count': 0,
    };

    if ($scope.index.user != null) {
        reply_controller.model.username = $scope.index.user.username;
    }
    reply_controller.local_datetime = $filter('date')(new Date(), 'yyyy-MM-dd');
    reply_controller.is_data = false;
    reply_controller.is_disabled = false;

    if (!angular.isUndefined($routeParams['post_id'])) {
        reply_model.list($routeParams['post_id']).then(
            function (data) {
                reply_controller.reply_list = data;
                reply_controller.is_data = true;
            },
            function (error) {
                reply_controller.message = error.detail;
                $('#reply_message_modal').modal('show');
            });

        reply_controller.model.post = $routeParams['post_id'];
    }

    reply_controller.create = function (formData) {
        reply_controller.errors = [];
        reply_controller.result = null;

        validate.form_validation(formData, reply_controller.errors);

        if (reply_controller.errors.create_reply_editor.length > 0) {
            $('#reply_message_modal').modal('show');
        }

        if (!formData.$invalid) {
            reply_model.create(reply_controller.model).then(
                function (data) {
                    $route.reload();
                },
                function (error) {
                    reply_controller.message = error.detail;
                    $('#reply_message_modal').modal('show');
                });
        }
    }

    reply_controller.update = function (id, index) {
        reply_controller.errors = [];
        reply_controller.messages = [];

        reply_controller.model = reply_controller.reply_list[index];
        reply_controller.model.changed_datetime = '';
        reply_controller.model.created_datetime = '';

        if (angular.isUndefined(reply_controller.model.content)) {
            reply_controller.messages.error = ['required.']
            $('#reply_message_modal').modal('show');
            return;
        }

        reply_model.update(reply_controller.model).then(
            function (data) {
                $route.reload();
            },
            function (error) {
                reply_controller.message = error.detail;
                $('#reply_message_modal').modal('show')
            });
    }

    reply_controller.delete = function (id) {
        $("#confirm_message_modal").modal('show');

        $('#modal-btn-confirm').on('click', function () {
            reply_model.delete(id).then(
                function (data) {
                    $window.location.reload();
                },
                function (error) {
                    reply_controller.message = error.detail;
                    $('#reply_message_modal').modal('show');
                });
        });
    }

    reply_controller.cancel = function () {
        $route.reload();
    }

});
