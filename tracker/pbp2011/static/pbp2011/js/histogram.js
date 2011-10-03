
/* 
 * General utility functions;
*/

/*
 * frameNumToString: 
 *
 *  Convert a frame number to a 4-digit string for display purposes;
 */
function frameNumToString(frameNum) {
    if (frameNum < 10)
	frameNum = "000"+frameNum;
    else if (frameNum < 100)
	frameNum = "00"+frameNum;
    else if (frameNum < 1000)
	frameNum = "0"+frameNum;

    return frameNum;
}

/*
 * histdata_format_date:
 *
 * Convert a date to a string of the form YYY-MM-DD HH:MM 
 * 
 * Would be so much more useful if there were a strftime function... sigh.
 */

function histdata_format_date(date) {
    var year = date.getFullYear();
    var month = date.getMonth();
    var day = date.getDate();
    var hour = date.getHours();
    var min = date.getMinutes();
    if (min < 10) min = '0'+min;

    return ''+year+'-'+month+'-'+day+' '+hour+':'+min;
}

/*
 * getBackgroundColor:
 *
 * Decide what background color to use for the chart based on the time of day.
 */

function getBackgroundColor(date) {
    var hour = date.getHours();
    var min = date.getMinutes();

    var colors_quarter = ["#a0a0a0", "#c0c0c0", "#e0e0e0", "#ffffff"];


    if (hour > 7 && hour < 21)
        return "#ffffff";
    else if (hour > 21 || hour < 7)
        return "#808080";
    else {
        var q = min/15;
        if (hour == 21)
            q = 3 - q;
        return colors_quarter[q];

        return "#c0c0c0";
    }
}

/*
 * Frame tracking - 
 *
 * The user can track particular riders by entering their frame numbers.
 * The frames are stored in a cookie for persistence.
 */

var TrackFrames_cookie = "PBP2011_TrackedFrames";

// A list of the frame numbers;
var TrackFrames = []

// An array of the rider frame data that we have pulled from the server;
var FrameData = []

function AddTrackedFrame(frame_num) {
    var i;

    for (i=0; i<TrackFrames.length; i++) {
	if (TrackFrames[i] == frame_num)
	    break;
    }

    // If the frame is not already in our list, add it;
    if (i == TrackFrames.length) {
	TrackFrames[TrackFrames.length] = frame_num;
	$.cookie(TrackFrames_cookie, TrackFrames);
	BuildTrackList();
    }
}

function RemoveTrackedFrame(frame_num) {

    for (var i=0; i<TrackFrames.length; i++) {
	if (TrackFrames[i] == frame_num) {
	    TrackFrames.splice(i, 1);
	    $.cookie(TrackFrames_cookie, TrackFrames);
	    RemoveTrackedFrameData(frame_num);
	    BuildTrackList();
	    break;
	}
    }
}

function IsFrameTracked(frame_num) {
    for (var i=0; i<TrackFrames.length; i++) {
	if (TrackFrames[i] == frame_num)
	    return true;
    }
    return false;
}

function LoadTrackedFrames() {
    var cookie = $.cookie(TrackFrames_cookie);
    if (cookie) {
	TrackFrames = cookie.split(/,/);
	for (i=0; i<TrackFrames.length; i++) {
	    loadFrameData(TrackFrames[i]);
	}
    }
}

function onFrameDataReceived(result) {
    // The result data is an array of the rider location at each time index for the period of the ride.
    FrameData[FrameData.length] = result;
    AddTrackedFrame(result.framenum);
    BuildTrackList();
}

function loadFrameData(frameNum) {
    $.ajax({
	url: "/histogram/framedata/"+frameNum,
	method: 'GET',
	dataType: 'json',
	success: onFrameDataReceived
    });
};

function RemoveTrackedFrameData(frame_num) {

    for (var i=0; i<FrameData.length; i++) {
	if (FrameData[i].framenum == frame_num) {
	    FrameData.splice(i, 1);
	    break;
	}
    }
}

/*
 * Build the HTML sidebar that holds tracked frame numbers and names;
 */

function BuildTrackList() {
    var html = "";

    // Generate a button based on the frame number;
    function generate_button(frame_num) {
	return '<input type="image" src="/static/misc/images/delete.png" width="20px" name="' + frame_num + '">'
    }

    // Build the tracking list - button, frame number, rider name;
    $.each(FrameData, function(indx, data) {
	button = generate_button(data.framenum);
	html = html + button + frameNumToString(data.framenum) + ' ' + data.name + '<br>';
    });

    // Insert the HTML into the page;
    $('#tracklist').html(html);

    // Add the click callbacks for the delete button;
    $('#tracklist input').click(function(ev) {
	// alert(ev.currentTarget.name);
	RemoveTrackedFrame(ev.currentTarget.name);
    })
}


/*
 * Functions & Data to actually render the main part of the plot;
 */


var frame_y_offset;
var initial_frame_y_offset = 20;

/*
 * renderFrameNum -
 *
 * Draw the litle box with the frame number and the pointer on top;
 */
function renderFrameNum(frameNum, location, status_flag, plot, tag) {

    frameNum = frameNumToString(frameNum);

    // XXX let's load some ride info upfront, don't hardcode this 1230!
    background = (status_flag||location>= 1230)? 'white' : 'red';

    var offset = plot.pointOffset({x:location, y: frame_y_offset});
    tag.append('<div style="position:absolute; left:' + (offset.left-15) + 'px;top:' + (offset.top) + 'px;font-size:smaller; background:'+background+';border:1px solid black;">'+frameNum+'</div>');
    var ctx = plot.getCanvas().getContext("2d");
    ctx.beginPath();
    ctx.moveTo(offset.left, offset.top-10);
    ctx.lineTo(offset.left+5, offset.top);
    ctx.lineTo(offset.left-5, offset.top);
    ctx.lineTo(offset.left, offset.top-10);
    ctx.fillStyle = "#000";
    ctx.fill();
    frame_y_offset += 10;
}

function main() {

    var start_date = new Date(2011, 8, 21, 16, 0); // XXX get from server;
    var end_date =  new Date(2011, 8, 25, 18, 0); // XXX get from server;

    var paused = true;
    var date = start_date;
    var bucketSize = 5;
    var fold = false;

    // XXX get from server;
    var controls = [[0, 0], [221, 0], [310, 0], [364, 0], [449, 0], [525, 0], [618, 0], [703, 0], [782, 0], [867, 0], [921, 0], [1009, 0], [1090, 0], [1165, 0], [1230, 0]
                    ];
    // XXX get from server;
    var refreshment = [[140, 0], [493, 0], [736, 0]];
    // XXX get from server;
    var secret = [];

    function refresh_bucketsize() {
	$('#bucket').empty();
	$('#bucket').append("Bucket size: "+bucketSize+"km");
    }

    $("input#stop").click(function() {
        paused = true;
        $("input#stop").hide();
        $("input#start").show();
    })

    $("input#start").click(function() {
        paused = false;
        $("input#stop").show();
        $("input#start").hide();
        loadDataViaTimer();
    })

    $("input#reset").click(function() {
        paused = true;
        date = start_date;
        $("input#stop").hide();
        $("input#start").show();
	loadData();
    })

    $("input#bucket_plus").click(function() {
	bucketSize += 1;
	refresh_bucketsize();
    })

    $("input#bucket_minus").click(function() {
	if (bucketSize > 1) {
	    bucketSize -= 1;
	    refresh_bucketsize();
	}
    })

    $("input#fold").click(function() {
	fold = this.checked;
    })
    $("input#fold").attr("checked", false)

    $("input#track").click(function() {
	var framenum = parseInt($("input#framenum").val());
	$("input#framenum").val("");
	if (!isNaN(framenum) && !IsFrameTracked(framenum)) {
	    loadFrameData(framenum);
	}
    })

    function filter_controls(controls, cutoff){

	var filtered = [];

	for (var i=0; i<controls.length; i++) {
	    if (controls[i][0] < 615) {
		filtered[filtered.length] = controls[i];
	    }
	}

	return filtered;
    }

    function onDataReceived(result) {
        var ride_data = [];
        var dnf_data = [];
        var step=bucketSize;
        var total_riders = 0;

	/* Start at 1, we don't want to count all the folks at post 0 
	 * and those at the finish;
	 */
	// XXX certainly shouldn't hard-code 1230!
	for (var i=1; (i+step-1)<1230; i+=step) {
            var sum = 0;
	    var dnf_sum = 0;
            for (var j=0; j<step; j++) {
                sum += result.data[i+j];
		dnf_sum += result.dnf_data[i+j];
            }				     
            total_riders += sum;
            ride_data.push([i, sum]);
	    if (dnf_sum > 0) 
		dnf_data.push([i, dnf_sum]);
        }

	var plot_controls = controls;
	var plot_refreshment = refreshment;
	var plot_secret = secret;

	if (fold) {
	    /* Fold the plot data */
	    var start = 0;
	    var end = ride_data.length - 1;
	    while (end > start) {
		ride_data[start][1] += ride_data[end][1];
		start++, end--;
	    }
	    var del_start = Math.floor(ride_data.length/2)+1
	    var del_count = ride_data.length-del_start;
	    ride_data.splice(del_start, del_count);

	    /* Next, remove controls past the fold */
	    plot_controls = filter_controls(controls, 615);
	    plot_refreshment = filter_controls(refreshment, 615);
	    plot_secret = filter_controls(secret, 615);

	    /* Now, fold the DNF data */
	    var middle = 615; // XXX don't hardcode this magic number!
	    for (i=0; i<dnf_data.length; i++) {
		// fold DNF data points that are past the middle;
		if (dnf_data[i][0] > middle+20) {
		    dnf_data[i][0] -= (2 * (dnf_data[i][0]-middle)) - 5;
		}
	    }

	    /* Center the DNF bars over the control location */
	    for (i=0; i<dnf_data.length; i++) {
		dnf_data[i][0] -= (step+1)/2;
	    }
	}

        var plot_data = [
            {
             data: ride_data,
             lines: { show: true}
             },
	    {
	     data: dnf_data,
  	     bars: { show: true, barWidth: step},
	     color: 'red',
	    },
            {
             label: "Controls",
             data: plot_controls,
             points: {show: true},
             color: 'red'
             },
            {
             label: "Food",
             data: plot_refreshment,
             points: {show: true},
             color: 'yellow'
             },
            {data: plot_secret,
             points: {show: true},
             color: 'black'
             }
            ];

        var plot_options = {
            yaxis: {min: 0, max: 300 },
	    grid: {backgroundColor: getBackgroundColor(date)}
        };

        var placeholder = $("#placeholder");

	// draw the chart;
        var plot = $.plot(placeholder, plot_data, plot_options);
	// draw any frame tags we may be tracking;

	frame_y_offset = initial_frame_y_offset;

	var max_distance = controls[controls.length-1][0];
	$.each(FrameData, function(indx, data) {
	    var location_tup = data.data[result.time_index];
	    var location = location_tup[0];
	    var status_flag = location_tup[1];
	    if (fold) {
		if (location > max_distance/2) {
		    location -= 2 * Math.floor((location - max_distance/2));
		}
	    }
	    renderFrameNum(data.framenum, location, status_flag, plot, placeholder);
	})
	$('#date').empty();
	$('#date').append(histdata_format_date(date));
	refresh_bucketsize();
	$('#riders').empty();
	$('#riders').append("Riders:"+total_riders);
    }		

    function loadData() {
        var datestr = histdata_format_date(date);
	$.ajax({
	    url: "/histogram/histdata/"+datestr,
	    method: 'GET',
	    dataType: 'json',
	    success: onDataReceived
	});
    };

    function loadDataViaTimer() {
        if (paused)
            return;

        loadData();
        var next_date = new Date(date.getTime() + 15*60*1000); // Increment date by 15min
        if (next_date < end_date) {
            date = next_date;
            setTimeout(loadDataViaTimer, 200);
        }
    }

    LoadTrackedFrames();
    loadData();
};
