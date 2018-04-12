var myVar = setInterval(myTimer, 1000);

function myTimer() {
    var d = new Date();
    document.getElementById("temps").innerHTML = d.toLocaleTimeString();
}

function reload_page() {
    location.reload();
}



function maxWindow() {
	var el = document.documentElement
	, rfs = // for newer Webkit and Firefox
		el.mozRequestFullScreen
		   // el.requestFullScreen
		// || el.webkitRequestFullScreen
		// || el.msRequestFullScreen
	;
	if(typeof rfs!="undefined" && rfs){
		rfs.call(el);
	}

}






/*---- Admin module ----*/

var adminModule = new function() {
	var adminContentElem = document.getElementById("admin-content");
	var isAnimating = false;

	// Toggles whether the admin pane is shown or hidden.
	function togglePane() {
		if (isAnimating)
			return;
		isAnimating = true;
		if (adminContentElem.style.display == "none") {
			adminContentElem.classList.add("showing");
			adminContentElem.style.removeProperty("display");
		} else {
			adminContentElem.classList.add("hiding");
		}
	}

	document.getElementById("admin-menu").onclick = function(ev) {
		togglePane();
		ev.stopPropagation();
	}

	adminContentElem.addEventListener("animationend", function(ev) {
		if (ev.animationName == "fadein") {
			if (adminContentElem.classList.contains("hiding"))
				adminContentElem.style.display = "none";
			adminContentElem.classList.remove("showing");
			adminContentElem.classList.remove("hiding");
			isAnimating = false;
		}
	});

	// For clicking outside the admin box
	adminContentElem.onclick = function(e) {
		if (e.target == adminContentElem)
			togglePane();  // Hiding
	};

	document.getElementById("admin-reload-page-button").onclick = function() {
		window.location.reload(true);
	};

	document.getElementById("admin-refresh-weather-button").onclick = function() {
		weatherModule.sunrisesetTextNode .data = "";
		weatherModule.conditionTextNode  .data = "";
		weatherModule.temperatureTextNode.data = "(Weather loading...)";
		weatherModule.doWeatherRequest();
	};

	document.getElementById("admin-change-wallpaper-button").onclick = function() {
		clockModule.changeWallpaper("random");
		togglePane();
	};

	// Fullscreen API
	(function() {
		function prefixifyFullscreenMember(obj, name) {
			if (name in obj)
				return name;
			name = name.charAt(0).toUpperCase() + name.substring(1);
			var result = null;
			["webkit", "moz", "ms"].forEach(function(prefix) {
				var temp = prefix + name;
				if (prefix == "moz")
					temp = temp.replace(/screen/i, "Screen").replace(/exit/i, "Cancel");
				if (temp in obj)
					result = temp;
			});
			return result;
		}

		function updateButtons() {
			if (document[prefixifyFullscreenMember(document, "fullscreenElement")] == null) {
				document.getElementById("admin-enter-full-screen-item").style.removeProperty("display");
				document.getElementById("admin-exit-full-screen-item").style.display = "none";
			} else {
				document.getElementById("admin-enter-full-screen-item").style.display = "none";
				document.getElementById("admin-exit-full-screen-item").style.removeProperty("display");
			}
		}

		document.querySelector("#admin-enter-full-screen-item a").onclick = function() {
			document.documentElement[prefixifyFullscreenMember(document.documentElement, "requestFullscreen")]();
		};
		document.querySelector("#admin-exit-full-screen-item a").onclick = function() {
			document[prefixifyFullscreenMember(document, "exitFullscreen")]();
		};
		["webkit", "moz", "ms"].forEach(function(prefix) {
			document["on" + prefix + "fullscreenchange"] = function() {
				togglePane();
				updateButtons();
			}
		});
		updateButtons();
	})();
};
