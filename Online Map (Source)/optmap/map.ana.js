// map kısmı
   var map = L.map('map').setView([40.75764, 39.60709], 11);
   mapLink =
       '<a href="https://openstreetmap.org">OpenStreetMap</a>';
   L.tileLayer(
       'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
                           attribution:
                    'Black Sea Technical University - PhD. Taha Yasin HATAY - <font color="red">This map was prepared under the scope of TÜBİTAK Project No. 122O785.</font>',
				minZoom: 1,
				maxZoom: 18,
				noWrap: true
       }).addTo(map);
	   
	
var esriLayer = L.tileLayer(
  'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}', {
    attribution: '© <a href="https://www.esri.com/">Esri</a>',
    maxZoom: 19
  }
).addTo(map);