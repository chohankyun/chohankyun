'use strict';

var chohankyun = angular.module('chohankyun')

chohankyun.controller('login_controller', function ($scope, $window, $location, auth_service, validate) {
    var login_controller = this;

    login_controller.model = {'username': '', 'password': ''};
    login_controller.complete = false;

    login_controller.login = function (formData) {
        login_controller.errors = [];
        login_controller.messages = [];

        validate.form_validation(formData, login_controller.errors);

        if (!formData.$invalid) {
            auth_service.login(login_controller.model)
                .then(function (data) {
                    $location.path("/main/home");
                }, function (error) {
                    login_controller.messages = error.non_field_errors;

                    if (error.status == 406) {
                        $('#re_register_message_modal').modal('show');
                    } else {
                        $('#login_message_modal').modal('show');
                    }
                });
        }
    }

    login_controller.re_register = function () {
        auth_service.reset_user(login_controller.model).then(
            function (data) {
                $location.path('/register');
                $window.location.reload();
            },
            function (error) {
                login_controller.messages = [error.detail];
                $("#re_register_message_modal").modal('hide');
                $('#login_message_modal').modal('show');
            });
    }
});
