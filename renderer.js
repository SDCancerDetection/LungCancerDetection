const zerorpc = require("zerorpc")
const panzoom = require("panzoom")
let client = new zerorpc.Client({ timeout: 600, heartbeatInterval: 6000000 })
client.connect("tcp://127.0.0.1:4242")

var slice_count = 0;

let file_selector = document.querySelector('#input-file')
$(file_selector).change(function () {
    generateHTML();
});

function generateHTML() {
    var res = "C:\\Users\\Jonathan Lehto\\Documents\\GitHub\\LungCancerDetection\\tmp\\data.csv";

    data = generateCSV(res);
    var patch_str = "";
    var slices = [];

    let max_num = document.querySelector('.scan-largest');
    $(max_num).text("" + slice_count + "");

    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] = '';
    }

    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] += '<div style="position:absolute;top:' + data[ind_patch].y_coord + 'px;left:' + data[ind_patch].x_coord + 'px; width: 64px; height: 64px; background:rgba(255,0,0,' + (data[ind_patch].cancer_perc / 4) + ');"></div>'
    }

    console.log(slices);

    for (var i = 0; i < slice_count; i++) {

        var htmlStr = '<div style="" class="row ' + i + '-th">\
					<div class="column left" style="background-color:#aaa;">\
						<h2>Tools</h2>\
						<p>Other Patient information</p>\
					<div class="btn-group">\
					<button class="button">Zoom In</button>\
					<button class="button">Zoom Out</button>\
					<button class="button">Contrast</button>\
				</div>\
				<p style="clear:both"><br></p>\
				</div>\
					<div class="column middle" style="background-color:#bbb;">\
						<h2>Main Scan Display</h2>\
						<div id="patch-container">\
						' + slices[i] + '\
						</div>\
						<img id="center-img" style="width: 100%; height: 100%;"  src="./tmp/slices/' + i + '.jpg" />\
					</div>\
					<div class="column right" style="background-color:#ccc;">\
						<h2>Other Scan Display options</h2>\
					</div>\
				</div>'
        document.querySelector('#scan-container').insertAdjacentHTML('beforeend', htmlStr);
    }



	/*client.invoke("dirSetup", document.getElementById("input-file").files[0].path, (error, res) => {
		if (error) {
			console.log(error)
		} else {
			
//      let img = document.querySelector('#center-img');
//      img.src = res + "?t=" + new Date().getTime();
		}
	})*/
}

function generateCSV(location) {
    var fs = require('fs');
    let input = fs.readFileSync(location);
    var inputText = Utf8ArrayToStr(input);
    var lines = inputText.split('\n');

    var patches = lines.map(function (line) {

        var values = line.split(',');
        value = values.map(function (value) {
            return value.replace(/\"/g, '');
        });

        var patch = {
            x_coord: values[0],
            y_coord: values[1],
            z_coord: values[2],
            cancer_perc: values[3],
        };

        if (values[2] > slice_count) {
            slice_count = values[2];
        }

        return patch;
    });

    return patches;
}

function Utf8ArrayToStr(array) {
    var out, i, len, c;
    var char2, char3;

    out = "";
    len = array.length;
    i = 0;
    while (i < len) {
        c = array[i++];
        switch (c >> 4) {
            case 0: case 1: case 2: case 3: case 4: case 5: case 6: case 7:
                // 0xxxxxxx
                out += String.fromCharCode(c);
                break;
            case 12: case 13:
                // 110x xxxx   10xx xxxx
                char2 = array[i++];
                out += String.fromCharCode(((c & 0x1F) << 6) | (char2 & 0x3F));
                break;
            case 14:
                // 1110 xxxx  10xx xxxx  10xx xxxx
                char2 = array[i++];
                char3 = array[i++];
                out += String.fromCharCode(((c & 0x0F) << 12) |
                    ((char2 & 0x3F) << 6) |
                    ((char3 & 0x3F) << 0));
                break;
        }
    }

    return out;
}