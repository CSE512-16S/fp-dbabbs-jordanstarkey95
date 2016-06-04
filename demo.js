(function(d3) {
	"use strict";

	//Path for local file requests
	var path = "https://cse512-16s.github.io/fp-dbabbs-jordanstarkey95/";

	window.onload = function() {
		document.getElementById("programSearch").onclick = getCourseList;
		document.getElementById("courseSearch").onclick = getCourseSequence;
		document.getElementById("loadingprograms").style.display = "block";
		getQuery(path + "programList.json", fillProgramList);
	};

	function getCourseSequence() {
		var program = document.getElementById("programInput").value.toUpperCase();
		var course = document.getElementById("courseInput").value;
		var pc = program + " " + course;
		// check if program/course is valid
		if (pc.match(/^[A-Z]+[&]*[A-Z]*\s[A-Z]*\s*\d{3}/)) {
			buildTree(program, course);
		} else {
			alert("Invalid input, try again");
		}
	}

	// fill drop down search box with every program in db
	function fillProgramList(ajax) {
		var json = JSON.parse(ajax.responseText);
		var programKeys = Object.keys(json);
		for (var i = 0; i < programKeys.length; i++) {
			var program = document.createElement("option");
			program.value = programKeys[i];
			document.getElementById("programs").appendChild(program);
		}
		document.getElementById("loadingprograms").style.display = "none";
	}

	//
	function getCourseList() {
		document.getElementById("loadingcourses").style.display = "block";

		var myNode = document.getElementById("courses");
		while (myNode.firstChild) {
		    myNode.removeChild(myNode.firstChild);
		}

		getQuery(path + "programList.json", fillCourseList);
	}

	//
	function fillCourseList(ajax) {
		var json = JSON.parse(ajax.responseText);
		var program = document.getElementById("programInput").value;
		var programKeys = Object.keys(json);
		for (var i = 0; i < programKeys.length; i++) {
			if (programKeys[i] == program) {
				var programCourses = json[programKeys[i]];
				for (var j = 0; j < programCourses.length; j++) {
					var course = document.createElement("option");
					course.value = programCourses[j];
					document.getElementById("courses").appendChild(course);
				}
				break;
			}
		}
		document.getElementById("loadingcourses").style.display = "none";
	}

	//asychronous helper function for requests
	function getQuery(file, fn) {
		var ajax = new XMLHttpRequest();
		ajax.onreadystatechange = function() {
			if (ajax.readyState == 4) {
				if (ajax.status == 200) {
					fn(ajax);
				} else {
					ajaxFailed(ajax);
				}
			}
		}
		ajax.open("GET", file, true);
		ajax.send();
	}

	//ajax request hepler function to handle errors
	function ajaxFailed(ajax) {
		if (ajax.status == 410) {
			document.getElementById("nodata").style.display = "block";
		} else {
			document.getElementById("errors").innerHTML = "Server status: " + ajax.status;
		}
	}

	//Standard features for our diagram:
	//size and shape of the svg container with margins included
	var margin = {
			top: 20,
			right: 120,
			bottom: 20,
			left: 120
		},
		width = 1280 - margin.right - margin.left,
		height = 800 - margin.top - margin.bottom;

	//
	var i = 0,
		//click animation
		duration = 750,
		root;

	//Assigns the variable / function tree to the d3.js function for required nodes and links
	var tree = d3.layout.tree()
		.size([height, width - 200]);

	//Declares the function that will be used to draw the links between the nodes.
	//This uses the d3.js diagonal function to help draw a path between two points 
	//such that the line exhibits some nice flowing curves (cubic Bezier) to make the connection
	var diagonal = d3.svg.diagonal()
		.projection(function(d) {
			return [d.y, d.x];
		});

	//Appends our SVG working area to the body of our web page and creates a group elements (<g>) 
	//that will contain our svg objects (our nodes, text and links)
	var svg = d3.select("#tree").append("svg")
		.attr("width", width + margin.right + margin.left)
		.attr("height", height + margin.top + margin.bottom)
		.append("g")
		.attr("transform", "translate(" + margin.left + "," + margin.top + ")");

	function buildTree(program, course) {
		//document.getElementById("loadingtree").style.display = "none";
		//put tree in div element, hide until loaded
		//document.getElementById("tree").innerHTML = "";

		d3.json("merged_file.json", function(error, treeData) {
			if (error) throw error;

			var data = getProgramCourses(treeData, program);

			//change this to course: 3rd parameter should be course
			root = getObjects(data, program + " " + course)

			//Collapse 2+ degree nodes
			function collapse(d) {
				if (Object.keys(d.children).length > 0) {
					d._children = d.children;
					d._children.forEach(collapse);
					d.children = null;
				}
			}

			//Collapse nodes
			root.children.forEach(collapse);
			update(root);
		});
	}

	//
	d3.select(self.frameElement).style("height", "500px");

	function getProgramCourses(data, program) {
		var programKeys = Object.keys(data);
		for (var i = 0; i < programKeys.length; i++) {
			if (Object.keys(data[i]) == program) {
				return data[i][Object.keys(data[i])];
			}
		}
		return objs
	}

	//
	function getObjects(data, pc) {
		pc = pc.replace(/\s/g, "");
		for (var i = 0; i < data.length; i++) {
			name = data[i].name.replace(/\s/g, "");
			if (name == pc) {
				return data[i];
			}
		}
	}

	//Draw tree and info
	function update(source) {
		// Compute the new tree layout by assigning nodes and repsected links
		var nodes = tree.nodes(root).reverse(),
			links = tree.links(nodes);

		// Normalize horizontal spacing
		// this may be where i create same leaf paths*****
		nodes.forEach(function(d) {
			d.y = d.depth * 180;
		});

		// Declare the node with unique ids for retireival
		var node = svg.selectAll("g.node")
			.data(nodes, function(d) {
				return d.id || (d.id = ++i);
			});

		// Enter the nodes, translate to position and assign class node features
		var nodeEnter = node.enter().append("g")
			.attr("class", "node")
			.attr("transform", function(d) {
				return "translate(" + source.y0 + "," + source.x0 + ")";
			})
			//
			.on("click", click);

		//Appends circle shape representing node
		nodeEnter.append("circle")
			.attr("r", 10)
			//Fills with blue if contains children
			.style("fill", function(d) {
				return d._children ? "lightsteelblue" : "#fff";
			});

		//Add text to each node
		nodeEnter.append("text")
			//Places text on left or right if node has no children or children
			.attr("x", function(d) {
				return d.children || d._children ? -13 : 13;
			})
			.attr("dy", ".35em")
			.attr("text-anchor", function(d) {
				return d.children || d._children ? "end" : "start";
			})
			.text(function(d) {
				return d.name;
			})
			.style("fill-opacity", 1);

		// Transition nodes to their new position using animation duration
		var nodeUpdate = node.transition()
			.duration(duration)
			.attr("transform", function(d) {
				return "translate(" + d.y + "," + d.x + ")";
			});

		// Update fill of newly positioned circles on children conditional    
		nodeUpdate.select("circle")
			.attr("r", 10)
			.style("fill", function(d) {
				return d._children ? "lightsteelblue" : "#fff";
			});

		nodeUpdate.select("text")
			.style("fill-opacity", 1);

		// Transition exiting nodes to the parent's new position.
		var nodeExit = node.exit().transition()
			.duration(duration)
			.attr("transform", function(d) {
				return "translate(" + source.y + "," + source.x + ")";
			})
			.remove();

		nodeExit.select("circle")
			.attr("r", 1e-6);

		nodeExit.select("text")
			.style("fill-opacity", 1e-6);

		// Declare the links to make a link based on all the links that have unique target id’s. 
		// Customize link color here
		var link = svg.selectAll("path.link")
			.data(links, function(d) {
				return d.target.id;
			});

		// Enter the links to add diagonal path
		link.enter().insert("path", "g")
			.attr("class", "link")
			.style("stroke", function(d) {
				return d.target.type === "choice" ? "purple" : "lightgrey";
			})
			.attr("d", function(d) {
				var o = {
					x: source.x0,
					y: source.y0
				};
				return diagonal({
					source: o,
					target: o
				});
			});

		// Transition links to their new position.
		link.transition()
			.duration(duration)
			.attr("d", diagonal);

		// Transition exiting nodes to the parent's new position.
		link.exit().transition()
			.duration(duration)
			.attr("d", function(d) {
				var o = {
					x: source.x,
					y: source.y
				};
				return diagonal({
					source: o,
					target: o
				});
			})
			.remove();

		// Stash the old positions for transition.
		nodes.forEach(function(d) {
			d.x0 = d.x;
			d.y0 = d.y;
		});
	}

	// Toggle children on click.
	function click(d) {
		if (d.children) {
			d._children = d.children;
			d.children = null;
		} else {
			d.children = d._children;
			d._children = null;
		}
		update(d);
	}

})(window.d3);