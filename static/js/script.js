

var numberOfItems = $('#loop .card').length
var limitPerPage = 4;
$("#loop .card:gt(" + (limitPerPage  - 1) +")").hide();
var totalPages = Math.round(numberOfItems/limitPerPage)
$('.pagination').append("<li class='current-page page-item active'><a class='page-link' href='javascript:void()'> " + 1 + "</a></li>");

for(var i = 2; i <= totalPages; i++) {
    $(".pagination").append("<li class = 'current-page' class='page-item'><a class='page-link' href='javascript:void()'> " + i + "</a></li>");
}
$(".pagination").append("<li class='page-item'><a class='page-link' href='javascript:void(0)'>Next</a></li>");

$(".pagination li.current-page").on("click", function() {
    if($(this).hasClass("active")){
        return false;
    } else {
        var currentPage = $(this).index();
        $(".pagination li").removeClass('active');
        $(this).addClass("active");
        $("#loop .card").hide();

        var sumTotal = limitPerPage * currentPage;
        for (var i = sumTotal - limitPerPage; i < sumTotal; i++) {
            $("#loop .card:eq(" + i +")").show();
        }
    }
});



