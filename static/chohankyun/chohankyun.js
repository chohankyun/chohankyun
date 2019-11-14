'use strict';

var chohankyun = angular.module('chohankyun', [
    'ngCookies',
    'ngResource',
    'ngSanitize',
    'ngRoute',
    'smart-table',
    'angular-timezone-selector',
    'ui.bootstrap.datetimepicker',
    'ui.dateTimeInput',
    'textAngular',
    'ui.toggle',
    'bw.paging',
    'pascalprecht.translate',
]);

chohankyun.run(function (request_service) {
    request_service.initialize('/');
});