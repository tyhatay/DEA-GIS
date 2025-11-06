<!DOCTYPE html>
<html lang="tr">
<head>
<title>Dea-Based Efficiency Analysis of Forest Roads Under Forest Function Scenarios</title>
	<link rel="icon" type="image/png" href="https://www.cbsdestek.com/favicon.ico"/>

    <meta name="viewport" content="width=device-width, initial-scale=1.0, maximum-scale=1.0, user-scalable=no">
    <meta charset="utf-8">
	<!---------------------------------------------------------------------------------------------->
	<!------------------------------------ JS Alanı ------------------------------------------------>
	<!---------------------------------------------------------------------------------------------->
	<script src="https://ajax.googleapis.com/ajax/libs/jquery/3.5.1/jquery.min.js"></script>
    <!-----<script src="https://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js"></script>----->
	<script src="https://unpkg.com/leaflet@1.9.2/dist/leaflet.js"></script>
	
	<script src="https://cdnjs.cloudflare.com/ajax/libs/js-polyfills/0.1.43/polyfill.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/leaflet.locatecontrol/dist/L.Control.Locate.min.js" charset="utf-8"></script>
	<script src="https://unpkg.com/leaflet-geosearch/dist/geosearch.umd.js"></script>
	<script type="text/javascript" src="./js/FileSaver.min.js" /></script>	
	<script type="text/javascript" src="./js/position.js"></script>
	<script type="text/javascript" src="./js/leaflet-ajax.js"></script>
	<script type="text/javascript" src="./js/spin.js"></script>
	<script type="text/javascript" src="./js/leaflet.spin.js"></script>
	<script type="text/javascript" src="./js/leaflet-sidebar.js"></script>
	<script type="text/javascript" src="./js/leaflet-easybutton.js"></script>
	<script type="text/javascript" src="./js/label/Leaflet.label.js"></script>
	<script type="text/javascript" src="./js/label/Leaflet.label.js"></script>
	<script type="text/javascript" src="./js/L.Control.Locate.js" charset="utf-8"></script>
	<script type="text/javascript" src="./js/L.Control.Layers.Tree.js"></script>
	<script src="https://unpkg.com/togeojson@0.16.0"></script>
	<script src="https://unpkg.com/leaflet-filelayer@1.2.0"></script>
    <script src="https://unpkg.com/@geoman-io/leaflet-geoman-free@latest/dist/leaflet-geoman.min.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.js"></script>
	<script src="./js/label/BaseMarkerMethods.js"></script>
	<script src="./js/label/Marker.Label.js"></script>
	<script src="./js/label/CircleMarker.Label.js"></script>
	<script src="./js/label/Path.Label.js"></script>
	<script src="./js/label/Map.Label.js"></script>
	<script src="./js/label/FeatureGroup.Label.js"></script>
	<link rel="stylesheet" href="./css/leaflet-search.css" />
	<script src="./js/leaflet-search.js"></script>
	<link rel="stylesheet" href="./css/MarkerCluster.css" />
	<link rel="stylesheet" href="./css/MarkerCluster.Default.css" />
	<script src="./js/leaflet.markercluster-src.js"></script>
	<script src="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/js/bootstrap-datepicker.min.js"></script>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/bootstrap-datepicker/1.9.0/css/bootstrap-datepicker.min.css">
	<script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.js"></script>
	<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet-groupedlayercontrol/0.6.1/leaflet.groupedlayercontrol.min.css">
	<!---------------------------------------------------------------------------------------------->
	<!------------------------------------ CSS Alanı ----------------------------------------------->
	<!---------------------------------------------------------------------------------------------->
    <link href="https://maxcdn.bootstrapcdn.com/font-awesome/4.1.0/css/font-awesome.min.css" rel="stylesheet">
	<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.2/dist/leaflet.css">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/font-awesome@4.7.0/css/font-awesome.min.css">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet.locatecontrol/dist/L.Control.Locate.min.css" />
	<link rel="stylesheet" href="https://unpkg.com/leaflet-geosearch@3.2.1/dist/geosearch.css" />
    <link rel="stylesheet" href="./css/leaflet-sidebar.min.css" />
    <link rel="stylesheet" href="css/style.css" />
	<link rel="stylesheet" href="./css/L.Control.Locate.min.css">
	<link rel="stylesheet" href="./css/L.Control.Layers.Tree.css">
    <link rel="stylesheet" href="./css/leaflet-easybutton.css" rel="stylesheet"/>
    <link rel="stylesheet" href="https://unpkg.com/@geoman-io/leaflet-geoman-free@latest/dist/leaflet-geoman.css">
	<link rel="stylesheet" href="https://cdn.jsdelivr.net/npm/leaflet-easybutton@2/src/easy-button.css">
    <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/normalize/4.2.0/normalize.min.css">
	<link rel="stylesheet" href="https://ppete2.github.io/Leaflet.PolylineMeasure/Leaflet.PolylineMeasure.css" />
<script src="https://ppete2.github.io/Leaflet.PolylineMeasure/Leaflet.PolylineMeasure.js"></script>
<style>
.selectie {
  padding: 6px 6px;
  display: none;
  font: 12px Arial, Helvetica, sans-serif roboto;
  background: white;
  background: rgba(255, 255, 255, 0.8);
  /*box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);*/
  /*border-radius: 5px;*/
  line-height: 24px;
  color: #555;
}
.legend {
  padding: 6px 8px;
  font: 14px Arial, Helvetica, sans-serif;
  background: white;
  background: rgba(255, 255, 255, 0.8);
  /*box-shadow: 0 0 15px rgba(0, 0, 0, 0.2);*/
  /*border-radius: 5px;*/
  line-height: 24px;
  color: #555;
}
.legend h4 {
  text-align: center;
  font-size: 16px;
  margin: 2px 12px 8px;
  color: #777;
}

.legend span {
  position: relative;
  bottom: 3px;
}

.legend i {
  width: 18px;
  height: 18px;
  float: left;
  margin: 0 8px 0 0;
  opacity: 0.7;
}

.legend i.icon {
  background-size: 18px;
  background-color: rgba(255, 255, 255, 1);
}
</style>
</head>
<body>
    <div id="sidebar" class="sidebar collapsed">
        <!-- Nav tabs -->
        <div class="sidebar-tabs">
            <ul role="tablist">
                <li><a href="#home" role="tab" title="Information"><i class="fa fa-bars"></i></a></li>
                <li><a href="#profile" role="tab" title="Information System"><i class="fa fa-info"></i></a></li>
                <li><a href="https://www.tahayasin.com" title="Coder Web Page!" role="tab" target="_blank"><i class="fa fa-university"></i></a></li>
            </ul>

            <ul role="tablist">
				<li><a href="" class="logout" title="Exit"><i class="fa fa-sign-out"></i></a></li>
            </ul>
        </div>

        <!-- Tab panes -->
        <div class="sidebar-content">
            <div class="sidebar-pane" id="home">
                <h1 class="sidebar-header">
                    Dea-Based Efficiency Analysis of Forest Roads Under Forest Function Scenarios
                    <span class="sidebar-close"><i class="fa fa-caret-left"></i></span>
                </h1>

                <div style="text-align: justify;"><p>Hi! </p>
				
				<p>This study examines the relationship between forest roads and forest resources, as well as the relationships between forest roads themselves, which form a systematic network. The aim is to measure the efficiency of forest roads planned and constructed using public resources through Data Envelopment Analysis, utilizing different inputs and outputs. The goal is to ensure the effective and efficient use of this planning and construction process. By evaluating these efficiency scores, efforts to improve existing forest roads will be kept up to date. Furthermore, a package program serving as a guide for planners has been developed, and a program module has been created using Python programming for GIS applications based on programming. <a href="https://github.com/ArresT-AnarchY">github</a>
				<p>Forest roads are planned and constructed according to the technical and geometric standards specified in the Forest Roads Planning, Construction, and Maintenance Circular No. 292. Forest roads planned and constructed based on the timber production function can be evaluated according to different forest functions as a result of this study. It will be a pioneering model that can pave the way for a more consistent use of public resources.
</p>
				
				<p>This system was coded by <a href="http://tahayasin.com">Research Assistant Taha Yasin HATAY</a>. Efficiency scores were determined using data envelopment analysis based on specific variables according to ecological, economic, social, and technical function scenarios for forest roads. For detailed information, you can access the Python and ArcGIS-based data envelopment analysis via <a href="https://github.com/ArresT-AnarchY">GitHub</a>.</p></div>

            </div>

            <div class="sidebar-pane" id="profile">
                <h1 class="sidebar-header">Information System<span class="sidebar-close"><i class="fa fa-caret-left"></i></span></h1>
                        <div class="msg"><br><br>Hello! <b></b><br><br>This section displays the activity values, current values, and projected values for forest roads. When you click on a forest road, click on the <b>“Check out the Efficiency Values!”</b> text. The information system will open.</div>
            </div>
        </div>
    </div>
    <div id="map" class="sidebar-map"></div>

	<script type="text/javascript" src="./optmap/map.ana.js"></script>
	<script type="text/javascript" src="./optmap/map.sidebar.opt.js"></script>
	<script type="text/javascript" src="./optmap/map.profil.layer.js"></script>
	<script type="text/javascript" src="./optmap/map.location-search-mouse.js"></script>
	<script type="text/javascript" src="./optmap/map.geoman.js"></script>
	<script type="text/javascript" src="./optmap/map.download.js"></script>
	<script type="text/javascript" src="./optmap/map.upload.js"></script>
	<script src="https://cdn.jsdelivr.net/npm/bootstrap@5.0.0-beta2/dist/js/bootstrap.bundle.min.js" integrity="sha384-b5kHyXgcpbZJO/tY9Ul7kGkf1S0CWuKcCD38l8YkeH8z8QjE0GmW1gYU5S9FOnJ0" crossorigin="anonymous"></script>

<script>
$(document).ready(function(e){
	$(".logout").click(function(e){
		var url = "index.php";
		var data = { logout : "logout"}
		$.post(url, data)
});
});
$(".year").datepicker({
    format: "yyyy",
    viewMode: "years", 
    minViewMode: "years",
}).on('changeDate', function(e){
    $(this).datepicker('hide');
	$('#dmprogram').show();
}).attr("autocomplete", "off");
</script>
</body>
</html>