'use strict';

var chohankyun = angular.module('chohankyun')

chohankyun.controller('profile_controller', function ($scope, $window, $location, $cookies, auth_service, validate) {
    var profile_controller = this;
    profile_controller.model = {'username': '', 'date_joined': '', 'email': '', 'local_last_login': ''};
    profile_controller.is_disabled = true;


    auth_service.session_user().then(function (data) {
        profile_controller.model = data;
    });

    profile_controller.update = function (formData) {
        profile_controller.errors = [];
        validate.form_validation(formData, profile_controller.errors);

        if (!formData.$invalid) {
            auth_service.update(profile_controller.model)
                .then(function (data) {
                    profile_controller.messages = ['Username has been changed.'];
                    $('#profile_change_message_modal').modal('show');
                }, function (error) {
                    profile_controller.messages = [error.detail];
                    $('#profile_message_modal').modal('show');
                });
        }
    };

    $('#profile_change_message_modal').on('hide.bs.modal', function () {
        $window.location.reload();
    });

    profile_controller.delete = function () {
        $("#confirm_message_modal").modal('show');
    };

    profile_controller.confirm = function (formData) {
        profile_controller.confirm_errors = [];
        validate.form_validation(formData, profile_controller.confirm_errors);

        if (!formData.$invalid) {
            auth_service.delete(profile_controller.model.password).then(
                function (data) {
                    $cookies.remove('token');
                    request_service.authenticated = false;
                    $window.location.href = '/';
                },
                function (error) {
                    profile_controller.messages = [error.detail];
                    $('#profile_message_modal').modal('show');
                });
        }
    };

    $("#confirm_message_modal").on("hide.bs.modal", function () {
        profile_controller.model.password = '';
    });
});
