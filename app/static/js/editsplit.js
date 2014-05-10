var rownum=1;

jQuery(function(){

    var $arb = $("#add-row-button");
    var $rrb = $("#remove-row-button");
    var $table = $("#ftable");
    var $hidey = $("#number");


    $table.append(getRowHTML(rownum));

    $arb.click(function(){
        rownum++;
        $table.append(getRowHTML(rownum));
        $hidey.attr("value", rownum);
    });

    $rrb.click(function(){
        if(rownum>1){
            rownum--;
            $hidey.attr("value", rownum);
            $table.find("tr:last-child").remove();
        }
    });
});

function getRowHTML(n){
    return "<tr><td>"+n+"</td>" +
        "<td><input type='text' class='form-control' id='name"+n+"' name='name"+n+"' placeholder='Enter name "+n+"' required></td>" +
        "<td><input type='time' class='form-control' id='time"+n+"' name='time"+n+"' placeholder='Enter best time "+n+"'></td></tr>";
}
