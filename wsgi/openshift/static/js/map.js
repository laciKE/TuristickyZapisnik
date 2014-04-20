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
