angular
    .module('appRoutes', ["ui.router"])
    .config(['$stateProvider', '$urlRouterProvider', function($stateProvider, $urlRouterProvider) {

    $stateProvider.state({
        name: 'events',
        url: '/',
        templateUrl: 'public/components/events/templates/events.template',
        controller: 'EventsController'
    });

    $urlRouterProvider.otherwise('/');
}]);
