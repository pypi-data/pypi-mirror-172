function toggleSideNav() {
    $nav = $('#sideNav');
    if ($nav.hasClass('open')) {
        $nav.removeClass('open');
        $('body').removeClass('nav-open');
    } else {
        $nav.addClass('open');
        $('body').addClass('nav-open');
    }
}

$('#sideNavToggler').on('click', function(e) {
    toggleSideNav();
});

$('#navOverlay').on('click', function(e) {
    toggleSideNav();
});

$('#list_check_all').on('change', function(e) {
    $('.list-check').prop('checked', this.checked).trigger('change');
});

$('.list-check').on('change', function(e) {
    var $row = $(this).parent().parent().parent();

    if (this.checked) {
        $row.addClass('table-active');
    } else {
        var $checkAll = $('#list_check_all');
        if ($checkAll.prop('checked'))
            $checkAll.prop('checked', false);
        
        $row.removeClass('table-active');
    }
});

$(document).ready(function() {
    var $inputs = $('input[type="datetime"]');
    $inputs.addClass('d-none');

    $inputs.each(function(index) {
        var $input = $($inputs[index]);
        var datetime = $input.val();
        var [date, time] = datetime.split(' ') || '';
        var hh, mm, ss = '';
        var ampm = 'am';
        if (time) {
            [hh, mm, ss] = time.split(':');
            hh = parseInt(hh) || 0;
        }
        if (hh > 12) {
            ampm = 'pm';
            hh = hh - 12;
        } else if (hh === 0) {
            hh = 12;
        } else if (hh === 12) {
            ampm = 'pm';
        }

        $(
            '<div class="form-row">' +
            '<div class="col-md-4 mb-2 mb-md-0" data-target="#' + $input.attr('id') + '">' +
            '<input type="date" class="form-control custom-datetime-input" placeholder="Date" data-name="date" value="' + date + '">' +
            '</div>' +
            '<div class="input-group col-md-8" data-target="#' + $input.attr('id') + '">' +
            '<input type="number" class="form-control custom-datetime-input" placeholder="hh" max="12" min="0" data-name="hh" value="' + hh + '">' +
            '<input type="number" class="form-control custom-datetime-input" placeholder="mm" max="59" min="0" data-name="mm" value="' + mm + '">' +
            '<input type="number" class="form-control custom-datetime-input" placeholder="ss" max="59" min="0" data-name="ss" value="' + ss + '">' +
            '<select class="form-control custom-select custom-datetime-input" data-name="ampm" style="max-width:75px;">' +
            '<option value="am"' + (ampm === 'am' ? 'selected' : '') + '>am</option>' +
            '<option value="pm"' + (ampm === 'pm' ? 'selected' : '') + '>pm</option>' +
            '</select>' +
            '</div>' +
            '</div>'
        ).insertAfter($input);
    });

    $('.custom-datetime-input').on('change', function(e) {
        var date = $('.custom-datetime-input[data-name="date"]').val();
        var hh = parseInt($('.custom-datetime-input[data-name="hh"]').val() || 0);
        var mm = ($('.custom-datetime-input[data-name="mm"]').val() || '0').padStart(2, '0');
        var ss = ($('.custom-datetime-input[data-name="ss"]').val() || '0').padStart(2, '0');
        var ampm = $('.custom-datetime-input[data-name="ampm"]').val();

        if (ampm === 'am' && hh === 12)
                hh = 0;
        else if (ampm === 'pm' && hh !== 12) {
            hh = 12 + hh;
        }

        hh = hh.toString().padStart(2, '0');

        var datetime = '';
        if (date)
            datetime = date + ' ' + hh + ':' + mm + ':' + ss;

        var $target = $($(e.target).parent().attr('data-target'));
        $target.val(datetime);
    });
});
