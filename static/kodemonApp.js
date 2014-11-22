var kodemonApp = angular.module('kodemonApp', []);

kodemonApp.controller('MessagesCtrl', ['$scope', '$http', function ($scope, $http) {		
	new Highcharts.Chart({
        chart: {
            type: 'scatter',
            zoomType: 'xy',
            renderTo: 'chart'
        },
        title: {
            text: 'Execution times by Kodemon'
        },
        xAxis: {
            title: {
                enabled: true,
                text: 'Timestamp'
            },
            startOnTick: true,
            endOnTick: true,
            showLastLabel: true
        },
        yAxis: {
            title: {
                text: 'Execution Time'
            }
        },
        legend: {
            layout: 'vertical',
            align: 'left',
            verticalAlign: 'top',
            x: 100,
            y: 70,
            floating: true,
            backgroundColor: (Highcharts.theme && Highcharts.theme.legendBackgroundColor) || '#FFFFFF',
            borderWidth: 1
        },
        plotOptions: {
            scatter: {
                marker: {
                    radius: 5,
                    states: {
                        hover: {
                            enabled: true,
                            lineColor: 'rgb(100,100,100)'
                        }
                    }
                },
                states: {
                    hover: {
                        marker: {
                            enabled: false
                        }
                    }
                },
                tooltip: {
                    headerFormat: '<b>{series.name}</b><br>',
                    pointFormat: '{point.x} timestamp, {point.y} execution time'
                }
            }
        },
        series: [{name:'', data:[]}]
	});
	
	$scope.setChartKey = function(key){
		var rawdataset;
		for(var i = 0; i < $scope.messages.length; i++){
			if($scope.messages[i].key == key)
				rawdataset = $scope.messages[i].execution_times
		}
		var dataset = [];
		for(var i = 0; i < rawdataset.length; i++)
			dataset.push([rawdataset[i].timestamp, rawdataset[i].execution_time])
		
		var chart = Highcharts.charts[0];
		
        chart.series[0].update({name: key, data: dataset});
	}

	$scope.messages = []
	$http.get('api/v1/messages/keys').
		success(function(data, status, headers, config){
			for(var i = 0; i < data.length; i++){
				$http.get('api/v1/messages/execution_times/' + data[i]).
					error(function(d, status, headers, config){
						console.log('Failed to GET execution_times for ' + data[i]);
					}).
                    then(function(res){
                        d = res.data
                        $scope.messages.push({key: d.key, execution_times: d.execution_times})
                    });
			}
		}).
		error(function(data, status, headers, config){
			console.log('Failed to GET keys');
		});
}]);