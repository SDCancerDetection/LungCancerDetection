const zerorpc = require("zerorpc")
let client = new zerorpc.Client({ timeout: 600, heartbeatInterval: 6000000 })
client.connect("tcp://127.0.0.1:4242")

var x_slices = 0;
var y_slices = 0;
var z_slices = 0;
var patch_list = [];
//C:\Users\Jonathan Lehto\Documents\GitHub\LungCancerDetection\tmp
let file_selector = document.querySelector('#input-file')
$(file_selector).change(function () {
    document.querySelector('.slice-container').innerHTML = "";
    document.querySelector('.x-y-images').innerHTML = "";
    document.querySelector('.patch-listing').innerHTML = "";
    generateHTML("C:\\Users\\Jonathan Lehto\\Documents\\GitHub\\LungCancerDetection\\tmp");
/*    client.invoke("dirSetup", document.getElementById("input-file").files[0].path, 3, (error, res) => {
        if (error) {
          console.log(error)
        } else {
          console.log(res)
          generateHTML(res);
        }
    });*/
});

$("#scan-number").on("change paste keyup", function () {
    setZImage($(this).val());
})

var selectedImage;
var magExists = false;

let play = document.querySelector('#run');
$(play).on("click", function () {
    i = 0;
    selectedImage = null;
    $(".z-image").each(function () {
        $(this).hide();
    });
    $('.canc').each(function () {
        $(this).css({"border": "none", "z-index": "999"})
        $(this).hide();
    });
    timerLoop();
})

var timeout;
var i = 0;
function timerLoop() {
    timeout = setTimeout(function () {
        $(".z-" + i + "").each(function (item) {
            $(this).hide();
        });
        $(".z-" + (i + 1) + "").each(function (item) {
            $(this).show();
        });
      i++;
      if (i < z_slices - 1) {
         timerLoop();
      }
   }, 250)
}

function generateHTML(res) {
    data = generateCSV(res + "\\data.csv");
    var slices = [];

    let max_num = document.querySelector('.scan-largest');
    $(max_num).text("" + (z_slices - 1) + "");

    var listHtml = '';

    for (var i = 0; i < 100; i ++) {
        if (patch_list[i] == null) {
            break;
        }
        listHtml += '<li class="patch" id="' + patch_list[i].x_coord + '-' + patch_list[i].y_coord + '-' + patch_list[i].z_coord + '">Prediction: ' + (patch_list[i].cancer_perc * 100).toFixed(1) + '% (' + patch_list[i].x_coord + 'mm, ' + patch_list[i].y_coord + 'mm, ' + patch_list[i].z_coord + 'mm)</li>'; 
    }
    document.querySelector('.patch-listing').insertAdjacentHTML('beforeend', listHtml);
    
    for (var i = 0; i < z_slices; i ++) {
        slices[i] = '';
    }
    
    for (var ind_patch in data) {
        slices[data[ind_patch].z_coord] = '';
    }

    for (var ind_patch in data) {
        if (data[ind_patch].cancer_perc > 0.95) {
            slices[data[ind_patch].z_coord] += '<div class="canc z-' + data[ind_patch].z_coord + ' x-' + data[ind_patch].x_coord + ' y-' + data[ind_patch].y_coord + '" style="z-index: 999;display: none; position:absolute;top:' + data[ind_patch].y_coord + 'px;left:' + data[ind_patch].x_coord + 'px; width: 64px; height: 64px; background:rgba(255,0,0,' + (data[ind_patch].cancer_perc / 2) + ');"></div>'
        }
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

    clickInit();
}

function setZImage (zIndex) {
    clearTimeout(timeout);
    $('.z-image').each(function () {
        $(this).hide();
    });

    $('.x-y-image').each(function () {
        $(this).hide();
    });

    $('.canc').each(function () {
        $(this).css({"border": "none", "z-index": "999"})
        $(this).hide();
    });

    
    var zimg = $('.z-' + zIndex + '');
    zimg.show();
    selectedImage = $('.z-' + zIndex + '.z-image')[0];

}

function clickInit() {
    $('.patch').on("click", function () {
        var items = $(this).attr('id').split('-');

        setZImage(items[2]);

        var ximg = $(".x-y-image.x-" + (parseInt(items[0]) + 32));
        ximg.show();
        
        var yimg = $(".x-y-image.y-" + (parseInt(items[1]) + 32));
        yimg.show();
        var classStr = '.z-' + items[2] + '.x-' + items[0] + '.y-' + items[1];
        var cancer = $(classStr);
        $(cancer).css({"display": "block", "border": "2px solid #FFF", "z-index": "100"});
    });

    $("#color-toggle").click(function () {
        if (!$(this).is(":checked")) {
            $(".canc").each(function () {
                $(this).addClass("clear")
            });
        } else {
            $(".canc").each(function () {
                $(this).removeClass("clear")
            });
        }
    })
}

function generateCSV(location) {
    var fs = require('fs');
    let input = fs.readFileSync(location);
    var inputText = Utf8ArrayToStr(input);
    var lines = inputText.split('\n');
    var patches = [];

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

        if (parseInt(values[0]) > parseInt(x_slices)) {
            x_slices = values[0];
        }

        if (parseInt(values[1]) > parseInt(y_slices)) {
            y_slices = values[1];
        }

        if (parseInt(values[2]) > parseInt(z_slices)) {
            z_slices = values[2];
        }

        var cur_patch = patch;
        for (var j = 0; j < 100; j ++) {
            if (patch_list[j] == null) {
                patch_list[j] = cur_patch;
                break;
            } else {
                if (cur_patch.cancer_perc > patch_list[j].cancer_perc) {
                    var tmp_patch = patch_list[j];
                    patch_list[j] = cur_patch;
                    cur_patch = tmp_patch;
                }
            }
        }

        patches[i] = patch;
    }

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

function magnify(element, zoom) {
    var img = element;
    var glass, w, h, bw;
    /*create magnifier glass:*/
    glass = document.createElement("DIV");
    glass.setAttribute("class", "img-magnifier-glass");
    glass.setAttribute("id", "magnifier");
    /*insert magnifier glass:*/
    var container = $(".slice-container")[0];
    container.prepend(glass);
    //img.parentElement.insertBefore(glass, container);
    /*set background properties for the magnifier glass:*/
    glass.style.backgroundImage = "url('" + img.src + "')";
    glass.style.backgroundRepeat = "no-repeat";
    glass.style.backgroundSize = (img.width * zoom) + "px " + (img.height * zoom) + "px";
    bw = 3;
    w = glass.offsetWidth / 2;
    h = glass.offsetHeight / 2;
    /*execute a function when someone moves the magnifier glass over the image:*/
    glass.addEventListener("mousemove", moveMagnifier);
    img.addEventListener("mousemove", moveMagnifier);
    /*and also for touch screens:*/
    glass.addEventListener("touchmove", moveMagnifier);
    img.addEventListener("touchmove", moveMagnifier);

    function moveMagnifier(e) {
        var pos, x, y;
        /*prevent any other actions that may occur when moving over the image*/
        e.preventDefault();
        /*get the cursor's x and y positions:*/
        pos = getCursorPos(e);
        x = pos.x - 195;
        y = pos.y - 195;
        /*prevent the magnifier glass from being positioned outside the image:*/
        if (x > img.width - (w / zoom)) {x = img.width - (w / zoom);}
        if (x < w / zoom) {x = w / zoom;}
        if (y > img.height - (h / zoom)) {y = img.height - (h / zoom);}
        if (y < h / zoom) {y = h / zoom;}
        /*set the position of the magnifier glass:*/
        glass.style.left = (x - w) + "px";
        glass.style.top = (y - h) + "px";
        /*display what the magnifier glass "sees":*/
        glass.style.backgroundPosition = "-" + ((x * zoom) - w + bw) + "px -" + ((y * zoom) - h + bw) + "px";
    }

    function getCursorPos(e) {
        var a, x = 0, y = 0;
        e = e || window.event;
        /*get the x and y positions of the image:*/
        a = img.getBoundingClientRect();
        /*calculate the cursor's x and y coordinates, relative to the image:*/
        x = e.pageX - a.left;
        y = e.pageY - a.top;
        /*consider any page scrolling:*/
        x = x - window.pageXOffset;
        y = y - window.pageYOffset;
        return {x : x, y : y};
    }
}

$("#mag").on("click", function () {
    if (!magExists) {
        magExists = true;
        magnify(selectedImage, 3);
    } else {
        magExists = false;
        document.getElementById("magnifier").remove();
    }
})

function changeContrast() {
    var contrast = document.getElementById("contrastSlider").value
    $("#myimage").css("-webkit-filter","contrast(" + contrast + "%)" );
    $("#magnifier").css("-webkit-filter","contrast(" + contrast + "%)" );
    updateContrastValue();
}

function updateContrastValue() {
    var sliderValue = document.getElementById("contrastSlider").value;
    document.getElementById("demo").innerHTML = sliderValue;
}