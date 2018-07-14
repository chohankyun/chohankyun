'use strict';

var chohankyun = angular.module('chohankyun')

chohankyun.controller('find_controller', function ($scope, $routeParams, $location, auth_service, validate) {
    var find_controller = this;
    var find_type = {'Username': 'Username', 'Password': 'Password'}

    find_controller.model = {'type': '', 'email': ''};

    if (!angular.isUndefined($routeParams['find_word'])) {
        find_controller.model.type = find_type[$routeParams['find_word']];
    }

    find_controller.send_email = function (formData) {
        find_controller.errors = [];

        validate.form_validation(formData, find_controller.errors);

        if (!formData.$invalid) {
            if ($routeParams['find_word'] == 'username') {
                auth_service.find_username(find_controller.model.email)
                    .then(function (data) {
                        find_controller.message = data;
                        $('#find_message_modal').modal('show')
                    }, function (error) {
                        console.log(error);
                        find_controller.message = error.detail;
                        $('#find_message_modal').modal('show')
                    });
            } else {
                auth_service.reset_password(find_controller.model.email)
                    .then(function (data) {
                        find_controller.message = data;
                        $('#find_message_modal').modal('show')
                    }, function (error) {
                        find_controller.message = error.detail;
                        $('#find_message_modal').modal('show')
                    });
            }
        }
    }
});
