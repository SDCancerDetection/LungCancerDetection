const zerorpc = require("zerorpc")
const panzoom = require("panzoom")
let client = new zerorpc.Client({ timeout: 600, heartbeatInterval: 6000000 })
client.connect("tcp://127.0.0.1:4242")

var slice_count = 0;

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
    $(".x-1").show();
    $(".y-1").show();
    
    setTimeout(function () {
        //let current = document.querySelector('.z-' + i + '');
        //let next = document.querySelector('.z-' + (i + 1) + '');
        $(".z-" + i + "").each(function (item) {
            $(this).fadeOut(100);
        });
        $(".z-" + (i + 1) + "").each(function (item) {
            $(this).fadeIn(100);
        });
      i++;
      if (i < slice_count - 1) {
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
    $(max_num).text("" + slice_count + "");

    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] = '';
    }

    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] += '<div class="z-' + data[ind_patch].z_coord + ' x-' + data[ind_patch].x_coord + ' y-' + data[ind_patch].y_coord + '" style="z-index: 999;display: none; position:absolute;top:' + data[ind_patch].y_coord + 'px;left:' + data[ind_patch].x_coord + 'px; width: 64px; height: 64px; background:rgba(255,0,0,' + (data[ind_patch].cancer_perc / 4) + ');"></div>'
    }

    for (var i = 0; i < slice_count; i++) {
        var htmlStr = '' + slices[i] + '<img style="z-index: 1;position: absolute; display:none;" class="z-' + i + '" src="./tmp/slices/Z_' + i + '.jpg" />';
        document.querySelector('.slice-container').insertAdjacentHTML('beforeend', htmlStr);
    }

    for (var i = 0; i < 390; i++) {
        var htmlStr = '<img style="display:none;" class="x-y-image x-' + i + '" src="./tmp/slices/X_' + i + '.jpg" />\
                    <img style="display:none;" class="x-y-image y-' + i + '" src="./tmp/slices/Y_' + i + '.jpg" />';
        document.querySelector('.x-y-images').insertAdjacentHTML('beforeend', htmlStr);
    }
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

        if (values[2] > slice_count) {
            slice_count = values[2];
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