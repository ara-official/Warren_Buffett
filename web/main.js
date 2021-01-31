let gJsonData = null;
let gFileList = "";
let MAX_PER = Number(50);
let TARGET_PER = Number(5);
let WEIGHT = 1;
let gCurrentFileName = "";
let million = Number(100000000);
let whetherToBuy = true;
let DEBUG = false;
let jSelectJSON = "#select_json";
let jSelectPER = "#select_PER";
let jSelectWEIGHT = "#select_WEIGHT";
let jCheckNET_INCOME = "#check_NET_INCOME";
let CHECK_NET_INCOME = true;
let gLatestData = {
    fileName: "",
    list: '',
    avgReturnRatio: 0,
    type: ''
}

// window.onload = function ()
$(document).ready(function ()
{
    console.log("["+arguments.callee.name+"] START");

    // path = "file://" + json_path
    // console.log(path)
    ajax_load_list()

    // ajax_load_data("202010140009_NCAV")

    draw_select()
    console.log("["+arguments.callee.name+"] END");
})

function draw_select()
{
    for(let i = 0; i < MAX_PER + 1; i++)
    {
        let option = ""
        if (Number(i) === Number(TARGET_PER))
        {
            option = "selected";
        }
        let draw = "<option value=\"" + i + "\" " + option + ">" + i + "</option>";
        if (DEBUG === true) console.log("draw: " + draw);
        $(jSelectPER).append(draw)
    }

    for(let i = 0; i < 2; i += 0.1)
    {
        let option = ""
        if (Number(i).toFixed(1) === Number(WEIGHT).toFixed(1))
        {
            option = "selected";
        }
        let draw = "<option value=\"" + Number(i).toFixed(1) + "\" " + option + ">" + Number(i).toFixed(1) + "</option>";
        if (DEBUG === true) console.log("draw: " + draw);
        $(jSelectWEIGHT).append(draw)
    }

    let draw_etc = "<option value=\"yes\" selected>YES</option>";
    if (DEBUG === true) console.log("ddraw_etcraw: " + draw_etc);
    $(jCheckNET_INCOME).append(draw_etc);
    draw_etc = "<option value=\"no\">NO</option>";
    if (DEBUG === true) console.log("draw_etc: " + draw_etc);
    $(jCheckNET_INCOME).append(draw_etc);
}

$(jSelectPER).on("change", function(){
    TARGET_PER = Number($(jSelectPER +" option:selected").val())
    if (DEBUG === true) console.log("TARGET_PER: " + TARGET_PER)

    // calculate
    ajax_load_data(gCurrentFileName)
});

$(jSelectWEIGHT).on("change", function(){
    WEIGHT = Number($(jSelectWEIGHT + " option:selected").val())
    if (DEBUG === true) console.log("WEIGHT: " + WEIGHT);

    // calculate
    ajax_load_data(gCurrentFileName)
});

$(jCheckNET_INCOME).on("change", function(){
    let selectedValue = $(jCheckNET_INCOME + " option:selected").val();
    if (selectedValue === "yes")
    {
        CHECK_NET_INCOME = true;
    }
    else
    {
        CHECK_NET_INCOME = false;
    }
    if (DEBUG === true) console.log("CHECK_NET_INCOME: " + CHECK_NET_INCOME + ", selectedValue: " + selectedValue);

    ajax_load_data(gCurrentFileName)
});


function ajax_load_list()
{
    $.ajax({
        url: "../json/list.txt",
        type: "GET",
        async: true,
        dataType: "text",
        cache: false,
        success: function(data){
            display_select_box(data)

            ajax_load_data(gFileList[gFileList.length - 2])
            gLatestData.fileName = gFileList[gFileList.length - 2];

            ajax_load_latest_data();
        },
        error: function(jqXHR, textStatus, errorThrown){console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)}
    });
}

function ajax_load_data(file_name)
{
    if (gCurrentFileName != file_name)
    {
        gCurrentFileName = file_name;
    }

    $.ajax({
        // url: 'file:///Users/sonminsik/Desktop/PROGRAMMING/Warren_Buffett/json/202010111651_NCAV.json',
        // url: "http://127.0.0.1:8081/json/202010111651_NCAV.json",
        // url: "../json/202010120158_NCAV.json",
        // url: "../json/202010130035_NCAV.json",
        url: "../json/" + file_name,
        
        type: "GET",
        async: true,
        cache: false,
        // dataType: "json",
        dataType: "text",
        // dataType: "jsonp",
        // crossDomain: true,
    //     success: function(data){console.log(data)},
    //     error: function(jqXHR, textStatus, errorThrown){console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)}
    })
    .done(function(data){
        // console.log("["+arguments.callee.name+"] START");
        console.log("[ajax_load_data: done] START");

        let gJsonData = JSON.parse(data)

        display_json_data(gJsonData);

        // console.log("["+arguments.callee.name+"] END");
        console.log("[ajax_load_data: done] END");
    })
    .fail(function(jqXHR, textStatus, errorThrown){
        console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)
    });
}

function ajax_load_latest_data()
{
    $.ajax({
        // url: 'file:///Users/sonminsik/Desktop/PROGRAMMING/Warren_Buffett/json/202010111651_NCAV.json',
        // url: "http://127.0.0.1:8081/json/202010111651_NCAV.json",
        // url: "../json/202010120158_NCAV.json",
        // url: "../json/202010130035_NCAV.json",
        url: "../json/" + gLatestData.fileName,
        
        type: "GET",
        async: true,
        cache: false,
        // dataType: "json",
        dataType: "text",
        // dataType: "jsonp",
        // crossDomain: true,
    //     success: function(data){console.log(data)},
    //     error: function(jqXHR, textStatus, errorThrown){console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)}
    })
    .done(function(data){
        // console.log("["+arguments.callee.name+"] START");
        console.log("[ajax_load_latest_data: done] START");

        let gJsonData = JSON.parse(data)

        if (gJsonData["list"] === undefined)
        {
            gLatestData.list = gJsonData["data"];
            console.log(gLatestData);
            gLatestData.type = "dic"
        }
        else
        {
            gLatestData.list = gJsonData["list"];
            gLatestData.type = "list"
        }

        // console.log("["+arguments.callee.name+"] END");
        console.log("[ajax_load_latest_data: done] END");
    })
    .fail(function(jqXHR, textStatus, errorThrown){
        console.log("jqXHR: " + jqXHR + ", textStatus: " + textStatus)
    });
}

function display_select_box(list)
{
    gFileList = list.split("\n");
    // console.log(gFileList)
    for (let i = gFileList.length - 2; i >= 0; i--) // NOTE: 0 제외
    {
        let draw = "<option value=\"" + gFileList[i] + "\">" + gFileList[i] + "</option>";
        if (DEBUG === true) console.log("draw: " + draw)
        $(jSelectJSON).append(draw)
    }
}

$(jSelectJSON).on("change", function()
{
    if (DEBUG === true) console.log("["+arguments.callee.name+"] START");

    let select_value = $(jSelectJSON + " option:selected").val();
    if (DEBUG === true) console.log("select_value: " + select_value);

    ajax_load_data(select_value);

    if (DEBUG === true) console.log("["+arguments.callee.name+"] END");
})

function display_json_data(json_data)
{
    // $("#h3_1").html(json_data["date"] + " 추천 종목");

    $("#main_table").empty();

    if (DEBUG === true) console.log("["+arguments.callee.name+"] START");
    
    let draw = "<tr>"
        +"<th>"+"index"+"</th>"
        +"<th>"+"종목명"+"</th>"
        +"<th>"+"주가상승률"+"</th>"
        // +"<th>"+"오늘 종가"+"</th>"
        +"<th>"+"종가"+"</th>"
        // +"<th>"+"구매<br>여부"+"</th>"
        // +"<th>"+"(유동자산-부채총계)<br>:<br>(시가총액*가중치)"+"</th>"
        +"<th>"+"RATIO"+"</th>"
        +"<th class=\"cal_title\">"+"유동자산"+"</th>"
        +"<th class=\"cal_title\">"+"부채총계"+"</th>"
        +"<th class=\"cal_title\">"+"시가총액"+"</th>"
        +"<th>"+"오늘 시가총액"+"</th>"
        // +"<th class=\"cal_title\">"+"가<br>중<br>치"+"</th>"
        +"<th class=\"cal_title\">"+"가중치"+"</th>"
        +"<th class=\"cal_title\">"+"당기순이익</th>"
        +"<th>"+"DIV"+"</th>"
        +"<th>"+"BPS"+"</th>"
        +"<th>"+"PER"+"</th>"
        +"<th>"+"EPS"+"</th>"
        +"<th>"+"PBR"+"</th>"
        +"<th>"+"ROC"+"</th>"
    +"</tr>"

    $("#main_table").append("<thead>");
    $("#main_table").append(draw);
    $("#main_table").append("<thead>");

    let list = json_data["list"];
    let type = "list";
    // console.log(list)
    if (list === undefined)
    {
        type = "dic";
        list = json_data["data"]; // dictionary
        // console.log(list[0]);
        // // console.log(list)
        // for(let key in list)
        // {
        //     if (list.hasOwnProperty(key)) {    
        //         console.log(key, list[key]);
        //     }
        // }
    }

    let count = 0;
    let sumCount = 0;
    let sumOfReturnRatio = 0;

    $("#main_table").append("<tbody>");
    if (type === "list")
    {
        for(let i = 0; i < list.length; i++)
        {
            let display = true;

            // display = (list[i]["구매여부"] === "True");
            display &= ((Number(list[i]["PER"]) > Number(0)) && (Number(list[i]["PER"]) <= Number(TARGET_PER)));
            if (DEBUG === true) console.log("TARGET_PER: " + TARGET_PER + ", display: " + display)
            display |= (list[i]["PER"] === undefined);
            if (CHECK_NET_INCOME === true)
            {
                display &= (Number(list[i]["당기순이익"]) >= 0);
            }
            if (DEBUG === true) console.log("CHECK_NET_INCOME: " + CHECK_NET_INCOME + ", display: " + display)

            if (isNaN(list[i]["시가총액"]))
            {
                display = false;
            }
            if (isNaN(list[i]["유동자산"]))
            {
                display = false;
            }

            if (Boolean(display) === true) // radio button
            {
                // let cal = (list[i]["유동자산"]-list[i]["부채총계"])/(list[i]["시가총액"]*list[i]["가중치"]);
                let cal = (list[i]["유동자산"]-list[i]["부채총계"])/(list[i]["시가총액"]*WEIGHT);
                if (Number(cal) < Number(1))
                {
                    if(DEBUG === true) console.log("cal: " + cal);
                    continue
                }

                // 계산
                let ROC = Number(list[i]["영업이익"]) / (Number(list[i]["비유동자산"]) + Number(list[i]["유동자산"]) - Number(list[i]["유동부채"]));

                let today_market_capital = 0;
                if (gLatestData.type === "dic")
                {
                    for(let nIdx in gLatestData.list)
                    {
                        if (list[i]["종목명"] === gLatestData.list[nIdx]["종목명"])
                        {
                            today_market_capital = gLatestData.list[nIdx]["시가총액"];
                            break;
                        }
                    }
                }
                else
                {
                    for(let nIdx = 0; nIdx < gLatestData.list.length; nIdx++)
                    {
                        if (list[i]["종목명"] === gLatestData.list[nIdx]["종목명"])
                        {
                            today_market_capital = gLatestData.list[nIdx]["시가총액"];
                            break;
                        }
                    }
                }


                count++;
                let sumOfReturn = 0;
                if (Number(today_market_capital) != 0)
                {
                    // sumOfReturn = (Number(today_market_capital) / Number(list[i]["종가"]) * 100 - 100);
                    sumOfReturn = (Number(today_market_capital) / Number(list[i]["시가총액"]) * 100 - 100);
                    sumOfReturnRatio += sumOfReturn;
                    sumCount++;
                }

                let draw = "<tr>"
                    +"<td class=\"index\">["+count+"] "+i+"/"+list.length+"</td>"
                    +"<td class=\"stock_name\">"+list[i]["종목명"]+"</td>"
                    +"<td class=\"stock_name\">"+sumOfReturn.toLocaleString()+"%</td>"
                    +"<td class=\"close_value\">"+Number(list[i]["종가"]).toLocaleString()+"</td>"
                    // +"<td class=\"buy_or_not\">"+list[i]["구매여부"]+"</td>"
                    +"<td class=\"calculation\">"+Number(cal).toFixed(2)+"</td>"
                    +"<td class=\"cal_val\">"+(Number(list[i]["유동자산"]) / million).toFixed(0).toLocaleString()+" 억</td>"
                    +"<td class=\"cal_val\">"+(Number(list[i]["부채총계"]) / million).toFixed(0).toLocaleString()+" 억</td>"
                    +"<td class=\"cal_val\">"+(Number(list[i]["시가총액"]) / million).toFixed(0).toLocaleString()+" 억</td>"
                    +"<td class=\"close_value\">"+Number(today_market_capital / million).toFixed(0).toLocaleString()+" 억</td>"
                    // +"<td class=\"weight\">"+list[i]["가중치"]+"</td>"
                    +"<td class=\"weight\">"+WEIGHT+"</td>"
                    +"<td class=\"net_income\">"+(Number(list[i]["당기순이익"]) / million).toFixed(0).toLocaleString()+"억 (" + (Number(list[i]["당기순이익"])/Number(list[i]["유동자산"]) * 100).toFixed(2) + "%)</td>"
                    +"<td class=\"div\">"+list[i]["DIV"]+"</td>"
                    +"<td class=\"bps\">"+list[i]["BPS"]+"</td>"
                    +"<td class=\"per\">"+list[i]["PER"]+"</td>"
                    +"<td class=\"eps\">"+list[i]["EPS"]+"</td>"
                    +"<td class=\"pbr\">"+Number(list[i]["PBR"]).toFixed(3)+"</td>"
                    +"<td class=\"roc\">"+Number(ROC * 100).toFixed(2)+"%</td>"
                +"</tr>"

                $("#main_table").append(draw);
            }
        }
    }
    else if (type === "dic")
    {
        let stockIdx = 0;
        for(let i in list)
        {
            let display = true;

            // display = (list[i]["구매여부"] === "True");
            display &= ((Number(list[i]["PER"]) > Number(0)) && (Number(list[i]["PER"]) <= Number(TARGET_PER)));
            if (DEBUG === true) console.log("TARGET_PER: " + TARGET_PER + ", display: " + display)
            // display |= (list[i]["PER"] === undefined);
            if (CHECK_NET_INCOME === true)
            {
                display &= (Number(list[i]["당기순이익"]) > 0);
            }
            if (DEBUG === true) console.log("CHECK_NET_INCOME: " + CHECK_NET_INCOME + ", display: " + display)

            if (isNaN(list[i]["시가총액"]))
            {
                display = false;
            }
            if (isNaN(list[i]["유동자산"]))
            {
                display = false;
            }

            if (Boolean(display) === true) // radio button
            {
                // let cal = (list[i]["유동자산"]-list[i]["부채총계"])/(list[i]["시가총액"]*list[i]["가중치"]);
                let cal = (list[i]["유동자산"]-list[i]["부채총계"])/(list[i]["시가총액"]*WEIGHT);
                if (Number(cal) < Number(1))
                {
                    if(DEBUG === true) console.log("cal: " + cal);
                    continue
                }

                // 계산
                let ROC = Number(list[i]["영업이익"]) / (Number(list[i]["비유동자산"]) + Number(list[i]["유동자산"]) - Number(list[i]["유동부채"]));

                let today_market_capital = 0;
                console.log("gLatestData.list.length", gLatestData.list.length);
                if (gLatestData.type === "dic")
                {
                    for(let nIdx in gLatestData.list)
                    {
                        if (i === gLatestData.list[nIdx]["종목명"])
                        {
                            today_market_capital = gLatestData.list[nIdx]["시가총액"];
                            break;
                        }
                    }
                }
                else
                {
                    for(let nIdx = 0; nIdx < gLatestData.list.length; nIdx++)
                    {
                        if (i === gLatestData.list[nIdx]["종목명"])
                        {
                            today_market_capital = gLatestData.list[nIdx]["시가총액"];
                            break;
                        }
                    }
                }

                count++;
                let sumOfReturn = 0;
                if (Number(today_market_capital) != 0)
                {
                    // sumOfReturn = (Number(today_market_capital) / Number(list[i]["종가"]) * 100 - 100);
                    sumOfReturn = (Number(today_market_capital) / Number(list[i]["시가총액"]) * 100 - 100);
                    sumOfReturnRatio += sumOfReturn;
                    sumCount++;
                }

                let draw = "<tr>"
                    +"<td class=\"index\">["+count+"] "+stockIdx+"/"+Object.keys(list).length+"</td>"
                    +"<td class=\"stock_name\">"+i+"</td>"
                    +"<td class=\"stock_name\">"+sumOfReturn.toLocaleString()+"%</td>"
                    +"<td class=\"close_value\">"+Number(list[i]["종가"]).toLocaleString()+"</td>"
                    // +"<td class=\"buy_or_not\">"+list[i]["구매여부"]+"</td>"
                    +"<td class=\"calculation\">"+Number(cal).toFixed(2)+"</td>"
                    +"<td class=\"cal_val\">"+(Number(list[i]["유동자산"]) / million).toFixed(0).toLocaleString()+" 억</td>"
                    +"<td class=\"cal_val\">"+(Number(list[i]["부채총계"]) / million).toFixed(0).toLocaleString()+" 억</td>"
                    +"<td class=\"cal_val\">"+(Number(list[i]["시가총액"]) / million).toFixed(0).toLocaleString()+" 억</td>"
                    +"<td class=\"close_value\">"+Number(today_market_capital / million).toFixed(0).toLocaleString()+" 억</td>"
                    // +"<td class=\"weight\">"+list[i]["가중치"]+"</td>"
                    +"<td class=\"weight\">"+WEIGHT+"</td>"
                    +"<td class=\"net_income\">"+(Number(list[i]["당기순이익"]) / million).toFixed(0).toLocaleString()+"억 (" + (Number(list[i]["당기순이익"])/Number(list[i]["유동자산"]) * 100).toFixed(2) + "%)</td>"
                    +"<td class=\"div\">"+list[i]["DIV"]+"</td>"
                    +"<td class=\"bps\">"+list[i]["BPS"]+"</td>"
                    +"<td class=\"per\">"+list[i]["PER"]+"</td>"
                    +"<td class=\"eps\">"+list[i]["EPS"]+"</td>"
                    +"<td class=\"pbr\">"+Number(list[i]["PBR"]).toFixed(3)+"</td>"
                    +"<td class=\"roc\">"+Number(ROC * 100).toFixed(2)+"%</td>"
                +"</tr>"

                $("#main_table").append(draw);
                stockIdx = stockIdx + 1;
            }
        }
    }

    gLatestData.avgReturnRatio = Number(sumOfReturnRatio / sumCount).toFixed(2);
    $("#expectedReturn_label").text(gLatestData.avgReturnRatio);
    $("#expectedStock_label").text(sumCount);
    $("#main_table").append("</tbody>");
    if (DEBUG === true) console.log("["+arguments.callee.name+"] END");
}

