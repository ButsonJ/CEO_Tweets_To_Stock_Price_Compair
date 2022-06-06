"use strict";

document.addEventListener("DOMContentLoaded", function(event) {
    setTimeout(run, 1000)

    let objStock;
    let demoArr = [];
    let demoAr = [];
    let tweetsdb = Array(2);

    function getStockPrice() {
        $.get(`http://localhost:5000/api/v1/get_financial_data?username=elonmusk`,
            function(response) {
                objStock = response;
                let len = objStock.length
                for (let i = len-1 ; i > 0; i--) {
                    demoArr.push(objStock[i].Close);
                }
                return demoArr;
            });
    }

    function getStockDate() {
        $.get(`http://localhost:5000/api/v1/get_financial_data?username=elonmusk`,
            function(response) {
                let objStock = response;
                let len = objStock.length
                let counter = 0;
                
                for (let i = len-1 ; i > 0; i--) {
                    demoAr.push(objStock[i].DateTime);
                }
                return demoAr;
            });

    }

    function getTweet(){
        $.get(`http://localhost:5000/api/v1/get_tweets?username=elonmusk`,
                function (response) {
                    objStock = response;
                    let len = objStock.length
                    for(var i = 0; i <len; i++){
                        tweetsdb[i] = new Array(2);
                    }
                    for (let i = len-1 ; i > 0; i--) {
                        tweetsdb[i][0]=objStock[i].CreatedAt.slice(0,16);
                        tweetsdb[i][1]=objStock[i].TweetLink;
                        tweetsdb[i][2]=objStock[i].TweetText;
                    }
                   
                });

    }
    function displayTweet(index){
        var tmp = demoAr[index];
        var date = tmp.slice(0,16);
        console.log(date);
        console.log(date);
        for(var i = 0; i < tweetsdb.length; i++){
            if(date === tweetsdb[i][0]){
                var links = tweetsdb[i][1];
                console.log(links);
                $(".tweet").append(tweetsdb[i][0], tweetsdb[i][2], tweetsdb[i][1])
            }
        }
    }

    function run() {
        getStockDate();
        getStockPrice();
        getTweet();
        console.log(tweetsdb);
        
        let stockPrice = demoArr;
        let stockDate = demoAr;
        let chartHtml = document.getElementById("mixed-chart")
        console.log(stockPrice);
        let chart = new Chart(chartHtml, {
            type: 'line',
            data: {
                labels: stockDate,
                datasets: [{
                    label: "Stock",
                    type: "line",
                    borderColor: "#8e5ea2",
                    data: stockPrice,
                    fill: false
                }, {
                    label: "Tweet (not amount)",
                    type: "scatter",
                    backgroundColor: "rgba(255, 255, 255 .4)",
                    backgroundColorHover: "#3e95cd",
                    data: stockPrice
                }]
            },
            options: {
                title: {
                    display: true,
                    text: 'Elon Musk'
                },
                legend:false,
                onClick: function(evn){
                    var item = chart.getElementAtEvent(evn);
                    displayTweet(item[0]._index); 

                }
            }
        });
        chartHtml.style.display = "block"
    }

    function search() {
        $("input").on("change paste keyup", function() {
            let inputText = $("input").val()
            if (inputText.length >= 2) {
                resetSearchResults();
                $.get(
                    `http://localhost:5000/api/v1/search?query=${inputText}`,
                    function(response) {
                        //    build results view here
                    }
                )
            }
        });
    }
});