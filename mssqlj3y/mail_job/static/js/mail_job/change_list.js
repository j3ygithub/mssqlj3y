$(document).ready(function () {
    $("#filter-mail-job").on("keyup", function () {
        var value = $(this).val().toLowerCase();
        $("#table-mail-job tbody tr").filter(function () {
            $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1)
        });
    });
});
$(document).ready(function () {
    $("#field-controller-mail-job").on("change", function () {
        var value = $(this).val();
        if (value == "basic_field") {
            $('#table-mail-job .advanced-field').hide();
        }
        else {
            $('#table-mail-job .advanced-field').show();
        }
    });
});
$(document).ready(function () {
    $("#show-all-controller-mail-job").on("change", function () {
        var value = $(this).val();
        var role = "{{ user }}"
        if (value == "personal") {
            $("#table-mail-job tbody tr").filter(function () {
                $(this).toggle($(this).text().indexOf(role) > -1)
            });
        }
        else {
            $("#table-mail-job tbody tr").show()
        }
    });
});
var showAllMailJob = $("#show-all-controller-mail-job").val();
var role = "{{ user }}"
if (showAllMailJob == 'personal') {
    $("#table-mail-job tbody tr").filter(function () {
        $(this).toggle($(this).text().indexOf(role) > -1)
    });
}