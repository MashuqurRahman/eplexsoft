$(document).ready(function() {
    //mobile menu
    $(".mob").click(function() {
        $(".menu-area").addClass("mobile");

        return false;
    });


    $(".closes").click(function() {
        $(".menu-area").removeClass("mobile");

        return false;
    });


    $('.menu li a').click(function() {
        $('.menu li a').removeClass("active");
        $(this).addClass("active");

    });


    $(".menuwidth").click(function() {
        $(".menu-area").toggleClass("menu-short");
        $(".hide-item").toggleClass("show-item");
        $(".small-logo").toggleClass("show-logo");
        $(".dashboard-content").toggleClass("menu-short-body");

    });

    //submenu
    $('nav > ul > li > a').on('click', function(e) {
        e.stopPropagation();
        $('nav ul ul').slideUp();
        $(this).next().is(":visible") || $(this).next().slideDown();
    });

    $(function() {
        var current = window.location.href;

        $(".menu li a").each(function() {
            var link = $(this).prop("href");

            if (current === link) {
                $(".menu li a").removeClass("active");
                $(this).addClass("active");
            }
        });

    });

    // scroll-Top
    $(window).scroll(function() {
        if ($(this).scrollTop() > 500) {
            $('.scrolltotop').fadeIn();
        } else {
            $('.scrolltotop').fadeOut();
        }

    });

    $('.scrolltotop').click(function() {
        $('html,body').animate({ scrollTop: 0 }, 1000);
        return false;
    });

    // fixedtop
    $(window).scroll(function() {
        var headerTopHeight = $(".top-heading").outerHeight();
        var totalHeight = headerTopHeight;
        var utd = $(window).scrollTop();

        if (utd > totalHeight) {
            $(".header-area").addClass("shadows");
        } else {
            $(".header-area").removeClass("shadows");
        }
        return false;
    });



    // slick-slider
    $('.heroslider').slick({
        dots: true,
        infinite: true,
        autoplay: true,
        speed: 800,
        slidesToShow: 1,
        slidesToScroll: 1,
        fade: true,
        arrows: false,
        cssEase: 'linear'
    });


    $('.minus').click(function() {
        var $input = $(this).parent().find('input');
        var count = parseInt($input.val()) - 1;
        count = count < 1 ? 1 : count;
        $input.val(count);
        $input.change();
        return false;
    });
    $('.plus').click(function() {
        var $input = $(this).parent().find('input');
        $input.val(parseInt($input.val()) + 1);
        $input.change();
        return false;
    });

    $('.loves').click(function() {
        $(this).toggleClass('take');
    });


    //slider
    $('.categori-slider').slick({
        dots: false,
        infinite: true,
        autoplay: true,
        slidesToShow: 8,
        slidesToScroll: 1,
        speed: 600,
        focusOnSelect: false,
        arrows: true,
        nextArrow: '<span class="next"><i class="bi bi-chevron-right"></i></span>',
        prevArrow: '<span class="prev"><i class="bi bi-chevron-left"></i></span>',
        responsive: [{
                breakpoint: 1921,
                settings: {
                    slidesToShow: 8,
                }
            }, {
                breakpoint: 1600,
                settings: {
                    slidesToShow: 7,
                }
            }, {
                breakpoint: 1200,
                settings: {
                    slidesToShow: 5,
                }
            }, {
                breakpoint: 992,
                settings: {
                    slidesToShow: 4,
                }
            },
            {
                breakpoint: 768,
                settings: {
                    slidesToShow: 3,
                }
            },
            {
                breakpoint: 480,
                settings: {
                    slidesToShow: 2,
                }
            }
        ]
    });

    $(function() {

        $(".select2").select2({
            tags: true,
        });

    });


    $('#offcanvasExample').on('shown.bs.offcanvas', function() {
        $('.select2').select2({
            dropdownParent: $('#offcanvasExample')
        });
    });

    (function($) {

        $("#min_price1,#max_price1").on('change', function() {
            var min_price_range = parseInt($("#min_price1").val());
            var max_price_range = parseInt($("#max_price1").val());

            if (min_price_range > max_price_range) {
                $('#max_price1').val(min_price_range);
            }

            $("#slider-range1").slider({
                values: [min_price_range, max_price_range]
            });

        });


        $("#min_price1,#max_price1").on("paste keyup", function() {
            var min_price_range = parseInt($("#min_price1").val());
            var max_price_range = parseInt($("#max_price1").val());

            if (min_price_range == max_price_range) {

                max_price_range = min_price_range + 100;

                $("#min_price1").val(min_price_range);
                $("#max_price1").val(max_price_range);
            }

            $("#slider-range1").slider({
                values: [min_price_range, max_price_range]
            });

        });


        $(function() {
            $("#slider-range1").slider({
                range: true,
                orientation: "horizontal",
                min: 1,
                max: 10000,
                values: [1, 10000],
                step: 1,

                slide: function(event, ui) {
                    if (ui.values[0] == ui.values[1]) {
                        return false;
                    }

                    $("#min_price1").val(ui.values[0]);
                    $("#max_price1").val(ui.values[1]);
                }
            });

            $("#min_price1").val($("#slider-range1").slider("values", 0));
            $("#max_price1").val($("#slider-range1").slider("values", 1));

        });

        $("#slider-range1").click(function() {
            var min_price = $('#min_price1').val();
            var max_price = $('#max_price1').val();

        });

    })(jQuery);




    $('#lightSlider').lightSlider({
        gallery: true, // Show Thumbnails Panel
        item: 1, // Items or Images in Main Display Are. (Suitable for Content Slider)
        loop: true, // Repeat Images
        slideMargin: 1, // Spaces Between Main Slides Images
        thumbItem: 4, // Number Of Thumbnails to show on THumbnail Panel
        speed: 800, // Image Change : Slider Speed in Miliseconds ms 
        auto: false, // Auto play Slideshow On
        pause: 5000 // Pause Between Each Slide Change
    });




    $(function() {

    });



    $(function() {
        $('li>img').not('.no-zoom')
            .wrap('<span style="display:inline-block"></span>')
            .css('display', 'block')
            .parent()
            .zoom({
                magnify: 2
            });
    });






});

// SWEET ALERT

function SweetDelete(e,href){
    e.preventDefault()
    var self = $(this)
    Swal.fire({
      title: 'Are you sure?',
      text: "You won't be able to revert this!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#3085d6',
      cancelButtonColor: '#d33',
      confirmButtonText: 'Yes, delete it!'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire(
          'Deleted!',
          'Your file has been deleted.',
          'success',
          
        )
        location.href = href
    
      }
    })
  }


function SweetSendToSteadfast(e,href){
    e.preventDefault()
    var self = $(this)
    Swal.fire({
      title: 'Send this order?',
      text: "This action cannot be undone!",
      icon: 'warning',
      showCancelButton: true,
      confirmButtonColor: '#BA7517',
      cancelButtonColor: 'rgb(231, 52, 52)',
      confirmButtonText: 'Yes, Send it!'
    }).then((result) => {
      if (result.isConfirmed) {
        Swal.fire(
          'Send!',
          'Your order has been send successfully!',
          'success',
          
        )
        location.href = href
    
      }
    })
}
// ADD TO CART

