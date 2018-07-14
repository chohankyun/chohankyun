'use strict';

var chohankyun = angular.module('chohankyun')

chohankyun.controller('register_controller', function ($scope, auth_service, validate) {
    var register_controller = this;
    register_controller.model = {'username': '', 'password1': '', 'password2': '', 'email': ''};

    register_controller.register = function (formData) {
        register_controller.errors = [];
        register_controller.messages = [];

        validate.form_validation(formData, register_controller.errors);

        if (!formData.$invalid) {
            auth_service.register(register_controller.model)
                .then(function (data) {
                    register_controller.messages.detail = [data.detail];
                    $('#register_message_modal').modal('show')
                }, function (error) {
                    register_controller.messages = error;
                    $('#register_message_modal').modal('show')
                });
        }
    }

});
