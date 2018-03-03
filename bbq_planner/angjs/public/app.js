'use strict';

var events = angular.module("events", []);

angular.module('BBQPlannerApplication', [
        'appRoutes',
        'events',
        'ngResource'
    ]).config(function($httpProvider) {
      $httpProvider.defaults.xsrfCookieName = 'csrftoken';
      $httpProvider.defaults.xsrfHeaderName = 'X-CSRFToken';
});
