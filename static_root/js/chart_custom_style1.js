/*------------------------------------------------------------------
    File Name: chart_custom_style1.js
    Template Name: Pluto - Responsive HTML5 Template
    Created By: html.design
    Envato Profile: https://themeforest.net/user/htmldotdesign
    Website: https://html.design
    Version: 1.0
-------------------------------------------------------------------*/	

     var color = Chart.helpers.color;
		var barChartData = {
			labels: ['January', 'February', 'March', 'April', 'May', 'June', 'July'],
			datasets: [{
				type: 'bar',
				label: 'Dataset 1',
			backgroundColor: [
                'rgba(255, 152, 0, 1)',
                'rgba(33, 150, 243, 1)',
                'rgba(255, 87, 34, 1)',
                'rgba(0, 150, 136, 1)',
                'rgba(255, 152, 0, 1)',
                'rgba(21, 40, 60, 1)',
				'rgba(9, 113, 184, 1)',
				],
            borderColor: [
                'rgba(255, 152, 0, 1)',
                'rgba(103, 58, 183, 1)',
                'rgba(233, 30, 99, 1)',
                'rgba(0, 150, 136, 1)',
                'rgba(255, 152, 0, 1)',
                'rgba(21, 40, 60, 1)',
				'rgba(9, 113, 184, 1)',
            ],
            data: [
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor(),
				randomScalingFactor()
			]
			}, {
				type: 'line',
				label: 'Dataset 2',
				backgroundColor: [
                     'rgba(30, 208, 133, 0.3)',
                ],
                borderColor: [
                     'rgba(30, 208, 133, 1)',
                ],
				data: [
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor()
				]
			}, {
				type: 'bar',
				label: 'Dataset 3',
				backgroundColor: [
                     'rgba(255, 87, 34, 1)',
                     'rgba(103, 58, 183, 1)',
                     'rgba(233, 30, 99, 1)',
                     'rgba(0, 150, 136, 1)',
                     'rgba(255, 152, 0, 1)',
                     'rgba(21, 40, 60, 1)',
				     'rgba(9, 113, 184, 1)',
				],
                borderColor: [
                     'rgba(255, 87, 34, 1)',
                     'rgba(103, 58, 183, 1)',
                     'rgba(233, 30, 99, 1)',
                     'rgba(0, 150, 136, 1)',
                     'rgba(255, 152, 0, 1)',
                     'rgba(21, 40, 60, 1)',
				     'rgba(9, 113, 184, 1)',
                ],
				data: [
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor(),
					randomScalingFactor()
				]
			}]
		};

		// Define a plugin to provide data labels
		Chart.plugins.register({
			afterDatasetsDraw: function(chart) {
				var ctx = chart.ctx;

				chart.data.datasets.forEach(function(dataset, i) {
					var meta = chart.getDatasetMeta(i);
					if (!meta.hidden) {
						meta.data.forEach(function(element, index) {
							// Draw the text in black, with the specified font
							ctx.fillStyle = 'rgb(0, 0, 0)';

							var fontSize = 0;
							var fontStyle = 'normal';
							var fontFamily = 'Helvetica Neue';
							ctx.font = Chart.helpers.fontString(fontSize, fontStyle, fontFamily);

							// Just naively convert to string for now
							var dataString = dataset.data[index].toString();

							// Make sure alignment settings are correct
							ctx.textAlign = 'center';
							ctx.textBaseline = 'middle';

							var padding = 5;
							var position = element.tooltipPosition();
							ctx.fillText(dataString, position.x, position.y - (fontSize / 2) - padding);
						});
					}
				});
			}
		});

		window.onload = function() {
			var ctx = document.getElementById('canvas').getContext('2d');
			window.myBar = new Chart(ctx, {
				type: 'bar',
				data: barChartData,
				options: {
					responsive: true,
					title: {
						display: false,
						text: 'Chart.js Combo Bar Line Chart'
					},
				}
			});
		};

		document.getElementById('randomizeData').addEventListener('click', function() {
			barChartData.datasets.forEach(function(dataset) {
				dataset.data = dataset.data.map(function() {
					return randomScalingFactor();
				});
			});
			window.myBar.update();
		});
		