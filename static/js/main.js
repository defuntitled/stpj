(function ($) {
    $('.button').css('margin', '6%');
    $('.button').first().css('background-color', '#00FF99');
    $('.button').first().css('font-weight', '800');
    $('.button').first().css('color', 'black');
    $('.button').on('mouseover', function () {
        $(this).css('background-color', '#8B008B');
        $(this).css('color', 'white');
        $(this).css('font-weight', '1000');
    });
    $('.button').on('mouseout', function () {
        $(this).css('background-color', '#ef8376');
        $(this).css('font-weight', '400');
    });
    $('.button').on('mouseout', function () {
        $('.button').first().css('background-color', '#00FF99');
        $('.button').first().css('font-weight', '800');
        $('.button').first().css('color', 'black');
    });


    var $window = $(window),
        $body = $('body'),
        settings = {

            // Carousels
            carousels: {
                speed: 4,
                fadeIn: true,
                fadeDelay: 250
            },

        };

    breakpoints({
        wide: ['1281px', '1680px'],
        normal: ['961px', '1280px'],
        narrow: ['841px', '960px'],
        narrower: ['737px', '840px'],
        mobile: [null, '736px']
    });

    // Фон картинки во время загрузки
    $window.on('load', function () {
        window.setTimeout(function () {
            $body.removeClass('is-preload');
        }, 100);
    });

    // Dropdowns.
    $('#nav > ul').dropotron({
        mode: 'fade',
        speed: 350,
        noOpenerFade: true,
        alignment: 'center'
    });

    // Scrolly.
    $('.scrolly').scrolly();
})(jQuery);
