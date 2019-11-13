'use strict';

var chohankyun = angular.module('chohankyun')

chohankyun.controller('password_controller', function ($scope, $window, auth_service, validate) {
    var password_controller = this;
    password_controller.model = {'old_password': '', 'new_password1': '', 'new_password2': ''};

    password_controller.change_password = function (formData) {
        password_controller.errors = [];
        validate.form_validation(formData, password_controller.errors);

        if (!formData.$invalid) {
            auth_service.change_password(password_controller.model)
                .then(function (data) {
                    password_controller.messages = [data];
                    $('#password_message_modal').modal('show');
                }, function (error) {
                    password_controller.messages =  validate.server_error(error);
                    $('#password_message_modal').modal('show');
                });
        }
    }

});
