var myApp = angular.module('myApp', []).config(function($interpolateProvider) {
    $interpolateProvider.startSymbol('{$');
    $interpolateProvider.endSymbol('$}');
});

myApp.controller('repoCtrl', function ($scope,$http) {
    $scope.all = {};
    $scope.flag = false;
	$scope.repos=function(){
		$http.get('repo').success(function(data){ $scope.all = data; $scope.flag = true });
	}
    $scope.branchs=function(){
		$http.get('branch').success(function(data){ $scope.all = data; $scope.flag = true });
	}
    $scope.commits=function(){
		$http.get('commit').success(function(data){ $scope.all = data; $scope.flag = true });
	}
    $scope.raws=function(){
		$http.get('raw').success(function(data){ $scope.all = data; $scope.flag = true });
	}
});
