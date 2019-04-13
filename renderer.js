const zerorpc = require("zerorpc")
const panzoom = require("panzoom")
let client = new zerorpc.Client({ timeout: 600, heartbeatInterval: 6000000 })
client.connect("tcp://127.0.0.1:4242")

var x_slices = 0;
var y_slices = 0;
var z_slices = 0;
var patch_list = [];

let file_selector = document.querySelector('#input-file')
$(file_selector).change(function () {
    generateHTML();
});

let play = document.querySelector('#run');
$(play).on("click", function () {
    timerLoop();
})

var i = 0;
function timerLoop() {
    $(".z-image").each(function () {
        $(this).hide();
    });
    
    setTimeout(function () {
        $(".z-" + i + "").each(function (item) {
            $(this).fadeOut(100);
        });
        $(".z-" + (i + 1) + "").each(function (item) {
            $(this).fadeIn(100);
        });
      i++;
      if (i < z_slices - 1) {
         timerLoop();
      }
   }, 500)
}

function generateHTML() {
    var res = "C:\\Users\\Jonathan Lehto\\Documents\\GitHub\\LungCancerDetection\\tmp\\data.csv";

    data = generateCSV(res);
    var patch_str = "";
    var slices = [];

    let max_num = document.querySelector('.scan-largest');
    $(max_num).text("" + z_slices + "");

    var listHtml = '';
    for (var i = 0; i < 100; i ++) {
        if (patch_list[i] == null) {
            break;
        }
        listHtml += '<li class="patch" id="' + patch_list[i].x_coord + '-' + patch_list[i].y_coord + '-' + patch_list[i].z_coord + '">Prediction: ' + patch_list[i].cancer_perc + '%</li>'; 
    }
    document.querySelector('.patch-listing').insertAdjacentHTML('beforeend', listHtml);
    
    for (var i = 0; i < z_slices; i ++) {
        slices[i] = '';
    }
    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] = '';
    }

    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] += '<div class="z-' + data[ind_patch].z_coord + ' x-' + data[ind_patch].x_coord + ' y-' + data[ind_patch].y_coord + '" style="z-index: 999;display: none; position:absolute;top:' + data[ind_patch].y_coord + 'px;left:' + data[ind_patch].x_coord + 'px; width: 64px; height: 64px; background:rgba(255,0,0,' + (data[ind_patch].cancer_perc / 4) + ');"></div>'
    }

    for (var i = 0; i < z_slices; i++) {
        var htmlStr = '' + slices[i] + '<img style="z-index: 1;position: absolute; display:none;" class="z-' + i + ' z-image" src="./tmp/slices/Z_' + i + '.jpg" />';
        document.querySelector('.slice-container').insertAdjacentHTML('beforeend', htmlStr);
    }

    var max = (x_slices > y_slices) ? x_slices : y_slices;
    for (var i = 0; i < max; i++) {
        var htmlStr = '';
        if (i <= x_slices) {
            htmlStr += '<img style="display:none;" class="x-y-image x-' + i + '" src="./tmp/slices/X_' + i + '.jpg" />';
        }
        if (i <= y_slices) {
            htmlStr += '<img style="display:none;" class="x-y-image y-' + i + '" src="./tmp/slices/Y_' + i + '.jpg" />';
        }

        document.querySelector('.x-y-images').insertAdjacentHTML('beforeend', htmlStr);
    }

    $('.patch').on("click", function () {
        $('.z-image').each(function () {
            $(this).hide();
        });
        $('.x-y-image').each(function () {
            $(this).hide();
        });
        var items = $(this).attr('id').split('-');
        $('.x-' + (items[0] - 1) + '').show();
        $('.y-' + (items[1] - 1) + '').show();
        $('.z-' + (items[2] - 1) + '').show();
    });
}

function generateCSV(location) {
    var fs = require('fs');
    let input = fs.readFileSync(location);
    var inputText = Utf8ArrayToStr(input);
    var lines = inputText.split('\n');
    var patches = [lines.length];

    for (var i in lines) {
        var values = lines[i].split(',');

        for (var j in values) {
            values[j] = values[j].replace(/\"/g, '');
        }

        var patch = {
            x_coord: values[0],
            y_coord: values[1],
            z_coord: values[2],
            cancer_perc: values[3],
        };

        if (values[0] > x_slices) {
            x_slices = values[0];
        }

        if (values[1] > y_slices) {
            y_slices = values[1];
        }
        
        if (values[2] > z_slices) {
            z_slices = values[2];
        }

        var cur_patch = patch;
        for (var j = 0; j < 100; j ++) {
            if (patch_list[j] == null) {
                patch_list[j] = cur_patch;
                break;
            } else {
                if (cur_patch.cancer_perc > patch_list[j].cancer_perc) {
                    var tmp_perc = patch_list[j];
                    patch_list[j] = cur_perc;
                    cur_perc = tmp_perc;
                }
            }
        }

        patches[i] = patch;
    }

    return patches;
/*
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

    return patches;*/
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