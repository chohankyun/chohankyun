'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.controller('login_controller', function ($scope, $window, $location, auth_service, validate) {
    var login_controller = this;

    login_controller.model = {'username': '', 'password': ''};
    login_controller.complete = false;

    login_controller.login = function (formData) {
        login_controller.errors = [];
        validate.form_validation(formData, login_controller.errors);

        if (!formData.$invalid) {
            auth_service.login(login_controller.model)
                .then(function (data) {
                    $location.path("/main/home");
                }, function (error) {
                    if (error.status == 406) {
                        login_controller.messages = [error.detail];
                        $('#re_register_message_modal').modal('show');
                    } else {
                        login_controller.messages = validate.server_error(error);
                        $('#login_message_modal').modal('show');
                    }
                });
        }
    };

    login_controller.re_register = function () {
        auth_service.reset_user(login_controller.model).then(
            function (data) {
                $location.path('/register');
            },
            function (error) {
                login_controller.messages = [error.detail];
                $('#login_message_modal').modal('show');
            });
    }
});
