var d;
function view_gpx(gpx){
	var osm_mapnik = L.tileLayer('http://{s}.tile.osm.org/{z}/{x}/{y}.png', {
    	attribution: '&copy; <a href="http://osm.org/copyright">OpenStreetMap</a> contributors',
	});

	freemap_caratlas = L.tileLayer('http://tiles.freemap.sk/A/{z}/{x}/{y}.jpeg', {
		attribution: "<a href='http://www.freemap.sk'>Freemap Slovakia</a>"
	});
	freemap_cyclemap = L.tileLayer('http://tiles.freemap.sk/C/{z}/{x}/{y}.jpeg', {
		attribution: "<a href='http://www.freemap.sk'>Freemap Slovakia</a>"
	});
	freemap_hiking = L.tileLayer('http://tiles.freemap.sk/T/{z}/{x}/{y}.jpeg', {
		attribution: "<a href='http://www.freemap.sk'>Freemap Slovakia</a>"
	});

	var map = L.map('map', {layers: [freemap_caratlas, freemap_cyclemap, freemap_hiking, osm_mapnik]});

	var baseMaps = {
		"Freemap CarAtlas": freemap_caratlas,
		"Freemap CycleMap": freemap_cyclemap,
		"Freemap Hiking": freemap_hiking,
		"OSM Mapnik": osm_mapnik,
	};

	L.control.layers(baseMaps, {}).addTo(map);
	
	var gpxLayer = new L.GPX(gpx, {
		async: true,
		marker_options: {
		    startIconUrl: '',
		    endIconUrl: '',
    		shadowUrl: ''
		}
	}).on('loaded', function(e) {
		var html = '<span>Distance: ' + (gpxLayer.get_distance()/1000).toFixed(2) + ' km</span><br/>';
		if (gpxLayer.get_total_time()) {
			var totalTime = (0.001*gpxLayer.get_total_time()/3600);
			html += '<span>Total time: ' + totalTime.toFixed(2) + ' h</span><br/>';
			html += '<span>Speed: ' + (gpxLayer.get_distance()/1000/totalTime).toFixed(2)+ ' km/h</span><br/>';
		}
		if (gpxLayer.get_elevation_gain()) {
			html += '<span>Elevation gain: ' + gpxLayer.get_elevation_gain()+ ' m</span><br/>';
		}
		if (gpxLayer.get_elevation_loss()) {
			html += '<span>Elevation loss: ' + gpxLayer.get_elevation_loss()+ ' m</span><br/>';
		}
		$('#trip_stats').html(html);

		map.fitBounds(e.target.getBounds());
		
		try {
			var elevation_data = gpxLayer.get_elevation_data();
			$('#map').after("<canvas id='elevation_profile'></canvas>");
			$('#map').after("<span id='tooltip'>&nbsp;</span>");
			var c = $('#elevation_profile')[0];
			var W = c.width = c.offsetWidth;
			var H = c.height = c.offsetHeight;
			var ctx = c.getContext('2d');
			d = elevation_data;
			var maxElevation = 0;
			var minElevation = 10000;
			var distance = elevation_data[elevation_data.length - 1][0];
			for (i = 0; i < elevation_data.length; i++){
				maxElevation = (elevation_data[i][1] > maxElevation) ? elevation_data[i][1] : maxElevation;
				minElevation = (elevation_data[i][1] < minElevation) ? elevation_data[i][1] : minElevation;				
			}
			var elevation = maxElevation - minElevation;
			var tips = {};
			x = elevation_data[0][0];
			y = elevation_data[0][1];
			ctx.moveTo(10 + x/distance*(W-20), H - (10 + (y-minElevation)/elevation*(H-20)));
			tips[Math.round(10 + x/distance*(W-20))] = elevation_data[0][2];
			for (i = 1; i < elevation_data.length; i++){
				x = elevation_data[i][0];
				y = elevation_data[i][1];
				line = ctx.lineTo(10 + x/distance*(W-20), H - (10 + (y-minElevation)/elevation*(H-20)));
				tips[Math.round(10 + x/distance*(W-20))] = elevation_data[i][2];
			}
			ctx.stroke();
			
			var boundRect = c.getBoundingClientRect();
			var tooltip = $('#tooltip');
			c.onmousemove = function onMousemove(e) {
				var x = e.clientX - boundRect.left;
				if (tips[x]) {
					tooltip.text(tips[x]);
				}
			}
		} catch (e) {
			console.log(e);
		}
	}).addTo(map);
}
