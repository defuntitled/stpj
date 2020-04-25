$(document).ready(function () {
    var getvalue = 0;
    var r = 150;
    var g = 0;
    var b = 0;
    $('#navbar-in').css('transform', 'rotate(360deg)');
    $('#button-reg').on('click', function () {
        $(this).text('Your link is waiting for you at ЭЛЕКТРОМЫЛО');
    });

    $('#summernote').summernote({
        height: 300, // set editor height
        minHeight: null, // set minimum height of editor
        maxHeight: null, // set maximum height of editor
        focus: true // set focus to editable area after initializing summernote
    });

    $('#post-radio1').on('click', function () {
        $('#form-post').css('transition', 'background 0.8s ease');
        $('#form-post').css('background', 'linear-gradient(45deg, #EECFBA, #C5DDE8)');
        if($('#post-radio1').is(':checked')) {
            $("#post-radio2").attr("disabled", true);
            $("#post-radio3").attr("disabled", true);
        } else {
            $("#post-radio2").attr("disabled", false);
            $("#post-radio3").attr("disabled", false);
        }
        $("#post-radio2").removeAttr("checked");
        $("#post-radio3").removeAttr("checked");

    });

    $('#post-radio2').on('click', function () {
        $('#form-post').css('transition', 'background 0.8s ease');
        $('#form-post').css('background', 'radial-gradient(circle, rgba(63,94,251,1) 0%, rgba(252,70,107,1) 100%)');
        if($('#post-radio2').is(':checked')) {
            $("#post-radio1").attr("disabled", true);
            $("#post-radio3").attr("disabled", true);
        } else {
            $("#post-radio1").attr("disabled", false);
            $("#post-radio3").attr("disabled", false);
        }
        $("#post-radio1").removeAttr("checked");
        $("#post-radio3").removeAttr("checked");
    });

    $('#post-radio3').on('click', function () {
        $('#form-post').css('transition', 'background 0.8s ease');
        $('#form-post').css('background', 'radial-gradient(circle, rgba(63,94,251,1) 0%, rgba(26,246,73,1) 100%)');
        if($('#post-radio3').is(':checked')) {
            $("#post-radio1").attr("disabled", true);
            $("#post-radio2").attr("disabled", true);
        } else {
            $("#post-radio1").attr("disabled", false);
            $("#post-radio2").attr("disabled", false);
        }
        $("#post-radio2").removeAttr("checked");
        $("#post-radio1").removeAttr("checked");
    });

    function changeUserName() {
        var x = getRandomInt(1, 6);
        switch (x) {
            case 1:
                $('.username').css('font-family', '"Courier New", Courier, monospace');
                $('.username').css('font-weight', '700');
                $('.username').css('color', 'red');
                break;
            case 2:
                $('.username').css('font-family', 'Yanone Kaffeesatz');
                $('.username').css('font-weight', '700');
                $('.username').css('color', 'aqua');
                break;
            case 3:
                $('.username').css('font-weight', '700');
                $('.username').css('color', 'black');
                break;
            case 4:
                $('.username').css('font-family', "'Lexend Giga', sans-serif");
                $('.username').css('font-weight', '700');
                $('.username').css('color', '#483949');
                break;
        }

    }

    function getRandomInt(min, max) {
        return Math.floor(Math.random() * (max - min)) + min;
    }

    function changeColor2() {


        var randomColor = Math.floor(Math.random() * 16777215).toString(16);

        $('.username').css('color', '#' + randomColor);
    }





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
    setInterval(changeColor2, 100);

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

    var wrapper = document.querySelector(".wrapper");
    var text = document.querySelector(".text");

    var textCont = text.textContent;
    text.style.display = "none";

    for (var i = 0; i < textCont.length; i++) {
        (function (i) {
            setTimeout(function () {
                // Created textNode to append
                var texts = document.createTextNode(textCont[i])
                var span = document.createElement('span');
                span.appendChild(texts);

                span.classList.add("wave");
                wrapper.appendChild(span);

            }, 75 * i);
        }(i));
    }
});
