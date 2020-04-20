$(document).ready(function () {
    var getvalue = 0;
    var r = 150;
    var g = 0;
    var b = 0;

    function changeColor() {
        if (r > 230) {
            r = Math.floor(Math.random() * 50);
        }
        if (g > 240) {
            r = Math.floor(Math.random() * 11);
        }
        if (b > 230) {
            r = Math.floor(Math.random() * 15);
        }
        r = (r + Math.floor(Math.random() * 10));
        g = (r + Math.floor(Math.random() * 13));
        b = (r + Math.floor(Math.random() * 8));
        var color = 'rgb(' + Number(r) + ',' + Number(g) + ',' + Number(b) + ')';
        $('#navbar-in img').css('background-color', color);
        if (getvalue > 100000) {
            getvalue = 0;
        }
    }

    setInterval(changeColor, 100);
    $('#navbar-in').on('mouseover', function () {
        getvalue += 360;
        var howmuch = 'rotate(' + Number(getvalue) + 'deg)';
        $('#navbar-in').css('transform', howmuch);

    });
    $('#navbar-in').on('touchstart', function () {
        getvalue += 360;
        var howmuch = 'rotate(' + Number(getvalue) + 'deg)';
        $('#navbar-in').css('transform', howmuch);

    });

    $('#like').on('click', function () {
        $(this).fadeOut(1000);
    });
});
