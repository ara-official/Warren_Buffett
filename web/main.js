let gJsonData = null;
let gFileList = "";

// window.onload = function ()
$(document).ready(function ()
{
    console.log("["+arguments.callee.name+"] START");

    // path = "file://" + json_path
    // console.log(path)
    ajax_load_list()

    ajax_load_data("202010140009_NCAV")

    console.log("["+arguments.callee.name+"] END");
})


function ajax_load_list()
{
    $.ajax({
        url: "../json/list.txt",
        type: "GET",
        async: true,
        dataType: "text",
        success: function(data){display_select_box(data)},
        error: function(jqXHR, textStatus, errorThrown){console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)}
    });
}

function ajax_load_data(file_name)
{
    $.ajax({
        // url: 'file:///Users/sonminsik/Desktop/PROGRAMMING/Warren_Buffett/json/202010111651_NCAV.json',
        // url: "http://127.0.0.1:8081/json/202010111651_NCAV.json",
        // url: "../json/202010120158_NCAV.json",
        // url: "../json/202010130035_NCAV.json",
        url: "../json/" + file_name + ".json",
        
        type: "GET",
        async: true,
        // dataType: "json",
        dataType: "text",
        // dataType: "jsonp",
        // crossDomain: true,
    //     success: function(data){console.log(data)},
    //     error: function(jqXHR, textStatus, errorThrown){console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)}
    })
    .done(function(data){
        console.log("["+arguments.callee.name+"] START");

        let gJsonData = JSON.parse(data)

        display_json_data(gJsonData);

        console.log("["+arguments.callee.name+"] END");
    })
    .fail(function(jqXHR, textStatus, errorThrown){
        console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)
    });
}

function display_select_box(list)
{
    gFileList = list.split("\n");

    for (let i = 0; i < gFileList.length; i++)
    {
        let draw = "<option value=\"" + gFileList[i].split(".")[0] + "\">" + gFileList[i] + "</option>";

        $("#select_1").append(draw)
    }
}

function change_select_box()
{
    console.log("["+arguments.callee.name+"] START");

    let select_value = $("#select_1 option:selected").val();
    console.log("select_value: " + select_value);

    ajax_load_data(select_value);

    console.log("["+arguments.callee.name+"] END");
}


function display_json_data(json_data)
{
    // $("#h3_1").html(json_data["date"] + " 추천 종목");

    $("#main_table").empty();

    console.log("["+arguments.callee.name+"] START");
    
    let list = json_data["list"];
    let draw = "<tr>"
        +"<th>"+"index"+"</th>"
        +"<th>"+"종목명"+"</th>"
        +"<th>"+"구매<br>여부"+"</th>"
        +"<th>"+"(유동자산-부채총계)<br>:<br>(시가총액*가중치)"+"</th>"
        +"<th>"+"유동자산"+"</th>"
        +"<th>"+"부채총계"+"</th>"
        +"<th>"+"시가총액"+"</th>"
        +"<th>"+"가<br>중<br>치"+"</th>"
    +"</tr>"

    $("#main_table").append("<thead>");
    $("#main_table").append(draw);
    $("#main_table").append("<thead>");


    let count = 0;
    
    $("#main_table").append("<tbody>");
    for(let i = 0; i < list.length; i++)
    {
        if (list[i]["구매여부"] === "True") // radio button
        {
            count++;
            let cal = (list[i]["유동자산"]-list[i]["부채총계"])/(list[i]["시가총액"]*list[i]["가중치"]);
            let draw = "<tr>"
                +"<td class=\"index\">["+count+"] "+i+"/"+list.length+"</td>"
                +"<td class=\"stock_name\">"+list[i]["종목명"]+"</td>"
                +"<td class=\"buy_or_not\">"+list[i]["구매여부"]+"</td>"
                +"<td class=\"calculation\">"+cal+"</td>"
                +"<td>"+Number(list[i]["유동자산"]).toLocaleString()+"</td>"
                +"<td>"+Number(list[i]["부채총계"]).toLocaleString()+"</td>"
                +"<td>"+Number(list[i]["시가총액"]).toLocaleString()+"</td>"
                +"<td class=\"weight\">"+list[i]["가중치"]+"</td>"
            +"</tr>"

            $("#main_table").append(draw);
        }
    }
    $("#main_table").append("</tbody>");
    console.log("["+arguments.callee.name+"] END");
}