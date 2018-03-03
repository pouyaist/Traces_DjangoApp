events.controller('EventsController', function($scope, eventsService) {
  eventsService.query().$promise.then(function(data) {
     $scope.events = data;
  });
});
