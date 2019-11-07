'use strict';

var chohankyun = angular.module('chohankyun');

chohankyun.service('validate', function () {
    return {
        'message': {
            'minlength': 'The value is too small.',
            'maxlength': 'The value is too large.',
            'email': 'Invalid e-mail address.',
            'required': 'Required.',
            'password_confirm': 'Passwords do not match.'
        },
        'more_messages': {
            'demo': {
                'required': 'Here is a sample alternative required message.'
            }
        },
        'check_more_messages': function (name, error) {
            return (this.more_messages[name] || [])[error] || null;
        },
        'validation_messages': function (field, form, error_bin) {
            var messages = [];
            for (var e in form[field].$error) {
                if (form[field].$error[e]) {
                    var special_message = this.check_more_messages(field, e);
                    if (special_message) {
                        messages.push(special_message);
                    } else if (this.message[e]) {
                        messages.push(this.message[e]);
                    } else {
                        messages.push("Error: " + e)
                    }
                }
            }
            var deduped_messages = [];
            angular.forEach(messages, function (el, i) {
                if (deduped_messages.indexOf(el) === -1) deduped_messages.push(el);
            });
            if (error_bin) {
                error_bin[field] = deduped_messages;
            }
        },
        'form_validation': function (form, error_bin) {
            for (var field in form) {
                if (field.substr(0, 1) != "$") {
                    this.validation_messages(field, form, error_bin);
                }
            }
        },
        'server_error': function (error) {
            var messages = [];
            if (error.status == 400 && error.non_field_errors == undefined) {
                delete error.status;
                for (var key in error) {
                    messages.push(key + ': ' + error[key]);
                }
            } else if (error.status == 400 && error.non_field_errors != undefined) {
                messages = error.non_field_errors;
            } else {
                messages = [error.detail];
            }
            return messages;
        }
    }
});