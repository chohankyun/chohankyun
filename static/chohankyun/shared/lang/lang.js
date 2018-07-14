'use strict';

chohankyun.config(function ($translateProvider) {
    $translateProvider.registerAvailableLanguageKeys(['en', 'ko'], {
        'en_*': 'en',
        'ko_*': 'ko',
        '*': 'en'
    }).determinePreferredLanguage();
});
